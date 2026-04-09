import asyncio
import base64
import json
import os
from contextlib import suppress
from typing import Any, Optional
from urllib.parse import quote

import websockets
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
REALTIME_MODEL = os.getenv("OPENAI_REALTIME_MODEL", "gpt-realtime")
VOICE = os.getenv("OPENAI_VOICE", "marin")
INPUT_SAMPLE_RATE = int(os.getenv("INPUT_SAMPLE_RATE", "24000"))

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is required")

DEFAULT_SYSTEM_PROMPT = """
You are a live voice call agent.
Speak naturally, clearly, and briefly.
Keep answers short unless the user explicitly asks for detail.
Do not use markdown.
If the user interrupts, stop cleanly and continue naturally.
If you need to clarify something, ask one short question.
"""

app = FastAPI(title="OpenAI Realtime Call Agent Bridge")


def build_realtime_url(call_id: Optional[str] = None) -> str:
    """
    Normal live session:
      wss://api.openai.com/v1/realtime?model=gpt-realtime

    SIP-controlled call session:
      wss://api.openai.com/v1/realtime?call_id=...
    """
    if call_id:
        return f"wss://api.openai.com/v1/realtime?call_id={quote(call_id)}"
    return f"wss://api.openai.com/v1/realtime?model={quote(REALTIME_MODEL)}"


def build_session_update(instructions: str) -> dict[str, Any]:
    """
    Session shape based on current Realtime docs.
    Input/output are PCM. We enable VAD so the model can reply automatically.
    """
    return {
        "type": "session.update",
        "session": {
            "type": "realtime",
            "model": REALTIME_MODEL,
            "instructions": instructions,
            "output_modalities": ["audio", "text"],
            "audio": {
                "input": {
                    "format": {
                        "type": "audio/pcm",
                        "rate": INPUT_SAMPLE_RATE,
                    },
                    "turn_detection": {
                        "type": "semantic_vad",
                    },
                },
                "output": {
                    "format": {
                        "type": "audio/pcm",
                    },
                    "voice": VOICE,
                },
            },
        },
    }


def build_text_message(text: str) -> dict[str, Any]:
    return {
        "type": "conversation.item.create",
        "item": {
            "type": "message",
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": text,
                }
            ],
        },
    }


def build_response_create(output_modalities: Optional[list[str]] = None) -> dict[str, Any]:
    payload: dict[str, Any] = {"type": "response.create"}
    if output_modalities:
        payload["response"] = {"output_modalities": output_modalities}
    return payload


def extract_assistant_item_id(event: dict[str, Any]) -> Optional[str]:
    """
    Try to capture the assistant item id so the client can truncate
    unplayed audio during interruptions.
    """
    # Common event shapes
    for key in ("item", "output_item"):
        item = event.get(key)
        if isinstance(item, dict) and item.get("role") == "assistant" and item.get("id"):
            return item["id"]

    # Final response shape
    response = event.get("response")
    if isinstance(response, dict):
        output = response.get("output", [])
        if isinstance(output, list):
            for item in output:
                if isinstance(item, dict) and item.get("role") == "assistant" and item.get("id"):
                    return item["id"]

    return None


async def send_json_safe(ws: WebSocket, payload: dict[str, Any]) -> None:
    try:
        await ws.send_json(payload)
    except Exception:
        # client is likely gone
        pass


async def send_bytes_safe(ws: WebSocket, chunk: bytes) -> None:
    try:
        await ws.send_bytes(chunk)
    except Exception:
        pass


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.websocket("/ws/call-agent")
async def call_agent_bridge(client_ws: WebSocket):
    await client_ws.accept()

    # Optional:
    # If you are controlling an OpenAI SIP call, pass ?call_id=...
    call_id = client_ws.query_params.get("call_id")
    instructions = client_ws.query_params.get("instructions") or DEFAULT_SYSTEM_PROMPT

    openai_url = build_realtime_url(call_id=call_id)
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }

    state: dict[str, Any] = {
        "last_assistant_item_id": None,
    }

    try:
        async with websockets.connect(
            openai_url,
            additional_headers=headers,
            max_size=None,
            ping_interval=20,
            ping_timeout=20,
        ) as openai_ws:
            # Initialize the session immediately
            await openai_ws.send(json.dumps(build_session_update(instructions)))

            await send_json_safe(
                client_ws,
                {
                    "type": "bridge.ready",
                    "input_audio_format": "pcm16le",
                    "sample_rate": INPUT_SAMPLE_RATE,
                    "channels": 1,
                    "output_audio_format": "pcm16le",
                    "voice": VOICE,
                    "model": REALTIME_MODEL,
                    "call_id": call_id,
                },
            )

            async def client_to_openai() -> None:
                """
                Accepts:
                - binary frames: raw PCM16LE mono audio
                - JSON text frames:
                    {"type":"user_text","text":"hello"}
                    {"type":"commit"}
                    {"type":"truncate","item_id":"...","audio_end_ms":1200}
                    {"type":"session.update","session":{...}}
                    {"type":"response.create"}
                """
                while True:
                    message = await client_ws.receive()

                    if message["type"] == "websocket.disconnect":
                        raise WebSocketDisconnect()

                    if message.get("bytes") is not None:
                        pcm_chunk = message["bytes"]
                        if not pcm_chunk:
                            continue

                        b64_audio = base64.b64encode(pcm_chunk).decode("ascii")
                        event = {
                            "type": "input_audio_buffer.append",
                            "audio": b64_audio,
                        }
                        await openai_ws.send(json.dumps(event))
                        continue

                    text_payload = message.get("text")
                    if text_payload is None:
                        continue

                    try:
                        data = json.loads(text_payload)
                    except json.JSONDecodeError:
                        await send_json_safe(
                            client_ws,
                            {"type": "error", "message": "Invalid JSON from client"},
                        )
                        continue

                    msg_type = data.get("type")

                    if msg_type == "user_text":
                        text = (data.get("text") or "").strip()
                        if not text:
                            continue

                        await openai_ws.send(json.dumps(build_text_message(text)))
                        await openai_ws.send(json.dumps(build_response_create()))
                        continue

                    if msg_type == "commit":
                        # Only needed if you disable VAD / use push-to-talk
                        await openai_ws.send(json.dumps({"type": "input_audio_buffer.commit"}))
                        await openai_ws.send(json.dumps(build_response_create()))
                        continue

                    if msg_type == "truncate":
                        item_id = data.get("item_id") or state.get("last_assistant_item_id")
                        audio_end_ms = data.get("audio_end_ms")

                        if not item_id or audio_end_ms is None:
                            await send_json_safe(
                                client_ws,
                                {
                                    "type": "error",
                                    "message": "truncate requires item_id (or tracked item) and audio_end_ms",
                                },
                            )
                            continue

                        truncate_event = {
                            "type": "conversation.item.truncate",
                            "item_id": item_id,
                            "content_index": 0,
                            "audio_end_ms": int(audio_end_ms),
                        }
                        await openai_ws.send(json.dumps(truncate_event))
                        continue

                    if msg_type == "session.update":
                        session = data.get("session")
                        if not isinstance(session, dict):
                            await send_json_safe(
                                client_ws,
                                {"type": "error", "message": "session.update requires a session object"},
                            )
                            continue

                        await openai_ws.send(
                            json.dumps(
                                {
                                    "type": "session.update",
                                    "session": session,
                                }
                            )
                        )
                        continue

                    if msg_type == "response.create":
                        response = data.get("response")
                        event: dict[str, Any] = {"type": "response.create"}
                        if isinstance(response, dict):
                            event["response"] = response
                        await openai_ws.send(json.dumps(event))
                        continue

                    if msg_type == "ping":
                        await send_json_safe(client_ws, {"type": "pong"})
                        continue

                    await send_json_safe(
                        client_ws,
                        {
                            "type": "error",
                            "message": f"Unknown client message type: {msg_type}",
                        },
                    )

            async def openai_to_client() -> None:
                """
                Forwards OpenAI realtime events to the client.

                Output strategy:
                - assistant audio chunks => sent as binary frames
                - everything else => sent as JSON
                """
                async for raw_message in openai_ws:
                    try:
                        event = json.loads(raw_message)
                    except json.JSONDecodeError:
                        await send_json_safe(
                            client_ws,
                            {"type": "error", "message": "Received invalid JSON from OpenAI"},
                        )
                        continue

                    event_type = event.get("type")

                    assistant_item_id = extract_assistant_item_id(event)
                    if assistant_item_id:
                        state["last_assistant_item_id"] = assistant_item_id

                    # Audio bytes from the model
                    if event_type in ("response.output_audio.delta", "response.audio.delta"):
                        delta = event.get("delta")
                        if delta:
                            try:
                                audio_chunk = base64.b64decode(delta)
                                await send_bytes_safe(client_ws, audio_chunk)
                            except Exception:
                                await send_json_safe(
                                    client_ws,
                                    {
                                        "type": "error",
                                        "message": "Failed to decode assistant audio chunk",
                                    },
                                )
                        continue

                    # Give client the tracked item id when interruption starts
                    if event_type == "input_audio_buffer.speech_started":
                        event["last_assistant_item_id"] = state.get("last_assistant_item_id")

                    # Forward all non-audio events as JSON
                    await send_json_safe(client_ws, event)

            task_up = asyncio.create_task(client_to_openai())
            task_down = asyncio.create_task(openai_to_client())

            done, pending = await asyncio.wait(
                {task_up, task_down},
                return_when=asyncio.FIRST_COMPLETED,
            )

            for task in pending:
                task.cancel()
                with suppress(asyncio.CancelledError):
                    await task

            for task in done:
                exc = task.exception()
                if exc:
                    raise exc

    except WebSocketDisconnect:
        pass
    except Exception as e:
        await send_json_safe(
            client_ws,
            {
                "type": "error",
                "message": str(e),
            },
        )
    finally:
        with suppress(Exception):
            await client_ws.close()