import time
import wave
from base64 import b64encode
from dataclasses import dataclass, field
from io import BytesIO
from struct import pack, unpack_from
from typing import Any

from openai import AsyncOpenAI
from starlette.concurrency import run_in_threadpool

from src.config.config_chat_model import ChatModels
from src.services.prompt_templete import PromptGenerator


@dataclass
class VoiceConversation:
    history: list[dict[str, str]] = field(default_factory=list)
    quote_data: Any = None
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

    def resolve_quote_data(self, session_id: str, quote_data: Any) -> Any:
        self._cleanup()
        session = self._sessions.setdefault(session_id, VoiceConversation())

        if self._has_quote_data(quote_data):
            session.quote_data = quote_data

        session.updated_at = time.time()
        return session.quote_data

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

    @staticmethod
    def _has_quote_data(quote_data: Any) -> bool:
        if quote_data is None:
            return False
        if isinstance(quote_data, str):
            return bool(quote_data.strip())
        if isinstance(quote_data, (dict, list, tuple, set)):
            return bool(quote_data)
        return True


class QuoteFollowUpVoiceAgent:
    def __init__(
        self,
        *,
        transcription_model: str = "gpt-4o-mini-transcribe",
        speech_model: str = "gpt-4o-mini-tts",
        voice: str = "shimmer",
        speech_instructions: str = (
            "Speak in a clear, polite, formal, gentle, feminine-sounding voice. "
            "Use a warm human customer-care tone, natural pacing, and crisp pronunciation. "
            "Sound calm, respectful, and reassuring without sounding robotic or overly sales-focused."
        ),
    ):
        self.client = AsyncOpenAI()
        self.chat_model = ChatModels().GetChatModel()
        self.prompt_generator = PromptGenerator()
        self.transcription_model = transcription_model
        self.speech_model = speech_model
        self.voice = voice
        self.speech_instructions = speech_instructions

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

    async def handle_twilio_voice_follow_up(
        self,
        *,
        audio_mulaw_bytes: bytes,
        quote_data: Any,
        previous_chat: list[dict[str, str]],
    ) -> tuple[str, str, str]:
        wav_audio = self._twilio_mulaw_to_wav(audio_mulaw_bytes)
        transcript = await self._transcribe_audio(
            audio_bytes=wav_audio,
            filename="twilio-input.wav",
            content_type="audio/wav",
        )
        answer_text = await self._get_contextual_answer(
            user_query=transcript,
            quote_data=quote_data,
            previous_chat=previous_chat,
        )
        twilio_audio = await self._text_to_twilio_mulaw(answer_text)
        return twilio_audio, transcript, answer_text

    async def handle_initial_voice_message(
        self,
        *,
        quote_data: Any,
        previous_chat: list[dict[str, str]],
    ) -> tuple[bytes, str]:
        prompt = self.prompt_generator.InitialVoiceAgentPrompt(
            quote_data=quote_data,
            previous_chat=previous_chat,
        )
        response = await run_in_threadpool(self.chat_model.invoke, prompt)
        answer_text = str(getattr(response, "content", response)).strip()
        audio_output = await self._text_to_speech(answer_text)
        return audio_output, answer_text

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

    async def _text_to_speech(self, text: str, *, response_format: str = "mp3") -> bytes:
        response = await self.client.audio.speech.create(
            model=self.speech_model,
            voice=self.voice,
            input=text,
            instructions=self.speech_instructions,
            response_format=response_format,
        )
        return response.read()

    async def _text_to_twilio_mulaw(self, text: str) -> str:
        pcm_24khz = await self._text_to_speech(text, response_format="pcm")
        pcm_8khz = _resample_pcm16_mono(pcm_24khz, source_rate=24000, target_rate=8000)
        mulaw_audio = _pcm16_to_mulaw(pcm_8khz)
        return b64encode(mulaw_audio).decode("ascii")

    @staticmethod
    def _twilio_mulaw_to_wav(audio_mulaw_bytes: bytes) -> bytes:
        pcm_audio = _mulaw_to_pcm16(audio_mulaw_bytes)
        wav_buffer = BytesIO()
        with wave.open(wav_buffer, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(8000)
            wav_file.writeframes(pcm_audio)
        return wav_buffer.getvalue()


def _mulaw_to_pcm16(mulaw_audio: bytes) -> bytes:
    pcm = bytearray()
    for byte in mulaw_audio:
        value = (~byte) & 0xFF
        sign = value & 0x80
        exponent = (value >> 4) & 0x07
        mantissa = value & 0x0F
        sample = ((mantissa << 3) + 0x84) << exponent
        sample -= 0x84
        if sign:
            sample = -sample
        pcm.extend(pack("<h", sample))
    return bytes(pcm)


def _pcm16_to_mulaw(pcm_audio: bytes) -> bytes:
    bias = 0x84
    clip = 32635
    mulaw = bytearray()
    sample_count = len(pcm_audio) // 2

    for index in range(sample_count):
        sample = unpack_from("<h", pcm_audio, index * 2)[0]
        sign = 0x80 if sample < 0 else 0
        if sample < 0:
            sample = -sample
        sample = min(sample, clip) + bias
        exponent = min(max(sample.bit_length() - 8, 0), 7)
        mantissa = (sample >> (exponent + 3)) & 0x0F
        mulaw.append((~(sign | (exponent << 4) | mantissa)) & 0xFF)

    return bytes(mulaw)


def _resample_pcm16_mono(
    pcm_audio: bytes,
    *,
    source_rate: int,
    target_rate: int,
) -> bytes:
    if source_rate == target_rate:
        return pcm_audio

    samples = [
        unpack_from("<h", pcm_audio, index)[0]
        for index in range(0, len(pcm_audio) - 1, 2)
    ]
    if not samples:
        return b""

    target_length = max(1, round(len(samples) * target_rate / source_rate))
    if target_length == 1:
        return pack("<h", samples[0])

    ratio = source_rate / target_rate
    output = bytearray()
    for target_index in range(target_length):
        source_position = target_index * ratio
        left_index = int(source_position)
        right_index = min(left_index + 1, len(samples) - 1)
        fraction = source_position - left_index
        sample = round(samples[left_index] * (1 - fraction) + samples[right_index] * fraction)
        output.extend(pack("<h", sample))

    return bytes(output)
