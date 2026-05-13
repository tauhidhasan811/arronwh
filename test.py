import os
import json
import base64
import asyncio
import websockets

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

REALTIME_URL = (
    "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview"
)





@app.websocket("/ws")
async def websocket_endpoint(client_ws: WebSocket):

    await client_ws.accept()

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "OpenAI-Beta": "realtime=v1",
    }

    try:
        async with websockets.connect(
            REALTIME_URL,
            additional_headers=headers
        ) as openai_ws:

            # Configure realtime session
            await openai_ws.send(json.dumps({
                "type": "session.update",
                "session": {
                    "instructions": (
                        "You are a realtime AI voice assistant. "
                        "Keep responses short and natural."
                    ),
                    "voice": "alloy",
                    "input_audio_format": "pcm16",
                    "output_audio_format": "pcm16",
                    "turn_detection": {
                        "type": "server_vad"
                    }
                }
            }))

            async def receive_from_client():
                while True:
                    audio_chunk = await client_ws.receive_bytes()

                    encoded_audio = base64.b64encode(audio_chunk).decode()

                    await openai_ws.send(json.dumps({
                        "type": "input_audio_buffer.append",
                        "audio": encoded_audio
                    }))

            async def send_to_client():
                async for message in openai_ws:

                    data = json.loads(message)

                    print("OpenAI Event:", data.get("type"))

                    # Audio response
                    if data.get("type") == "response.audio.delta":

                        audio_bytes = base64.b64decode(data["delta"])

                        await client_ws.send_bytes(audio_bytes)

                    # Text response
                    elif data.get("type") == "response.text.delta":

                        print(data["delta"], end="", flush=True)

                    # Error logging
                    elif data.get("type") == "error":

                        print("ERROR:", data)

            await asyncio.gather(
                receive_from_client(),
                send_to_client()
            )

    except WebSocketDisconnect:
        print("Client disconnected")

    except Exception as e:
        print("ERROR:", str(e))
