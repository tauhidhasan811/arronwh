import json
import uuid
from urllib.parse import quote

from fastapi import APIRouter, File, Form, Header, HTTPException, UploadFile
from fastapi.responses import Response

from src.services.voice_agent import QuoteFollowUpVoiceAgent, TemporaryVoiceMemory


router = APIRouter(prefix="/api/voice", tags=["Voice Agent"])

voice_memory = TemporaryVoiceMemory()
voice_agent: QuoteFollowUpVoiceAgent | None = None


def _get_voice_agent() -> QuoteFollowUpVoiceAgent:
    global voice_agent
    if voice_agent is None:
        voice_agent = QuoteFollowUpVoiceAgent()
    return voice_agent


def _parse_quote_data(raw_quote_data: str):
    try:
        return json.loads(raw_quote_data)
    except json.JSONDecodeError:
        return raw_quote_data


@router.post("/quote-follow-up")
async def quote_follow_up_voice(
    quote_data: str = Form(...),
    audio: UploadFile = File(...),
    session_id: str | None = Form(None),
    x_voice_session_id: str | None = Header(default=None),
):
    """
    Receives a customer's voice message for an abandoned quote follow-up,
    stores recent turns temporarily by session id, and returns an MP3 voice response.
    """
    try:
        active_session_id = session_id or x_voice_session_id or str(uuid.uuid4())
        audio_bytes = await audio.read()

        if not audio_bytes:
            raise HTTPException(status_code=400, detail="Audio file is required.")

        previous_chat = voice_memory.get_history(active_session_id)
        response_audio, transcript, answer_text = await _get_voice_agent().handle_voice_follow_up(
            audio_bytes=audio_bytes,
            filename=audio.filename or "voice-input.webm",
            content_type=audio.content_type or "application/octet-stream",
            quote_data=_parse_quote_data(quote_data),
            previous_chat=previous_chat,
        )

        voice_memory.append(
            session_id=active_session_id,
            user_query=transcript,
            ai_response=answer_text,
        )

        return Response(
            content=response_audio,
            media_type="audio/mpeg",
            headers={
                "X-Voice-Session-Id": active_session_id,
                "X-Voice-Transcript": quote(transcript[:800]),
                "X-Voice-Text": quote(answer_text[:1200]),
            },
        )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.delete("/quote-follow-up/{session_id}")
async def clear_quote_follow_up_session(session_id: str):
    voice_memory.clear(session_id)
    return {"message": "Voice conversation history cleared.", "session_id": session_id}
