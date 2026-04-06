
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse
from src.config.config_chat_model import ChatModels
from src.config.config_audio_model import AudioModel


load_dotenv()
audio_model = AudioModel()
import json

app = FastAPI()

@app.get("/stream-transcription")
def stream_transcription():

    event = audio_model.audio_to_text("Battle Symphony (Official Lyric Video) - Linkin Park.mp3")

    def generate():
        for seg in event.segments:
            yield json.dumps({
                "start": seg.start,
                "end": seg.end,
                "text": seg.text
            }) + "\n"

    return StreamingResponse(generate(), media_type="application/json")