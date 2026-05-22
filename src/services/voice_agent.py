import time
from dataclasses import dataclass, field
from typing import Any

from openai import AsyncOpenAI
from starlette.concurrency import run_in_threadpool

from src.config.config_chat_model import ChatModels
from src.services.prompt_templete import PromptGenerator


@dataclass
class VoiceConversation:
    history: list[dict[str, str]] = field(default_factory=list)
    updated_at: float = field(default_factory=time.time)


class TemporaryVoiceMemory:
    def __init__(self, ttl_seconds: int = 60 * 30, max_items: int = 8):
        self.ttl_seconds = ttl_seconds
        self.max_items = max_items
        self._sessions: dict[str, VoiceConversation] = {}

    def get_history(self, session_id: str) -> list[dict[str, str]]:
        self._cleanup()
        session = self._sessions.get(session_id)
        if not session:
            return []
        session.updated_at = time.time()
        return session.history[-self.max_items :]

    def append(self, session_id: str, user_query: str, ai_response: str) -> None:
        self._cleanup()
        session = self._sessions.setdefault(session_id, VoiceConversation())
        session.history.append({
            "user_query": user_query,
            "ai_response": ai_response,
        })
        session.history = session.history[-self.max_items :]
        session.updated_at = time.time()

    def clear(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)

    def _cleanup(self) -> None:
        now = time.time()
        expired_ids = [
            session_id
            for session_id, session in self._sessions.items()
            if now - session.updated_at > self.ttl_seconds
        ]
        for session_id in expired_ids:
            self._sessions.pop(session_id, None)


class QuoteFollowUpVoiceAgent:
    def __init__(
        self,
        *,
        transcription_model: str = "gpt-4o-mini-transcribe",
        speech_model: str = "gpt-4o-mini-tts",
        voice: str = "alloy",
    ):
        self.client = AsyncOpenAI()
        self.chat_model = ChatModels().GetChatModel()
        self.prompt_generator = PromptGenerator()
        self.transcription_model = transcription_model
        self.speech_model = speech_model
        self.voice = voice

    async def handle_voice_follow_up(
        self,
        *,
        audio_bytes: bytes,
        filename: str,
        content_type: str,
        quote_data: Any,
        previous_chat: list[dict[str, str]],
    ) -> tuple[bytes, str, str]:
        transcript = await self._transcribe_audio(
            audio_bytes=audio_bytes,
            filename=filename,
            content_type=content_type,
        )
        answer_text = await self._get_contextual_answer(
            user_query=transcript,
            quote_data=quote_data,
            previous_chat=previous_chat,
        )
        audio_output = await self._text_to_speech(answer_text)
        return audio_output, transcript, answer_text

    async def _transcribe_audio(
        self,
        *,
        audio_bytes: bytes,
        filename: str,
        content_type: str,
    ) -> str:
        transcription = await self.client.audio.transcriptions.create(
            model=self.transcription_model,
            file=(filename, audio_bytes, content_type),
        )
        return str(transcription.text).strip()

    async def _get_contextual_answer(
        self,
        *,
        user_query: str,
        quote_data: Any,
        previous_chat: list[dict[str, str]],
    ) -> str:
        prompt = self.prompt_generator.VoiceAgentPrompt(
            user_query=user_query,
            quote_data=quote_data,
            previous_chat=previous_chat,
        )
        response = await run_in_threadpool(self.chat_model.invoke, prompt)
        return str(getattr(response, "content", response)).strip()

    async def _text_to_speech(self, text: str) -> bytes:
        response = await self.client.audio.speech.create(
            model=self.speech_model,
            voice=self.voice,
            input=text,
            response_format="mp3",
        )
        return response.read()
