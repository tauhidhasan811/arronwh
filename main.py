"""import json
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse
from src.config.config_chat_model import ChatModels
from src.config.config_audio_model import AudioModel


load_dotenv()
audio_model = AudioModel()


app = FastAPI()

@app.get("/stream-transcription")
def stream_transcription():

    event = audio_model.audio_to_text("Battle Symphony (Official Lyric Video) - Linkin Park.mp3")

    return event
    # def generate():
    #     for seg in event.segments:
    #         yield json.dumps({
    #             "start": seg.start,
    #             "end": seg.end,
    #             "text": seg.text
    #         }) + "\n"

    # return StreamingResponse(generate(), media_type="application/json")"""


import json
from fastapi import FastAPI
from src.config.config_audio_model import AudioModel
from fastapi.responses import StreamingResponse

app = FastAPI()
audio_model = AudioModel()

@app.get("/stream-transcription")
def stream_transcription():
    def generate():
        for event in audio_model.audio_to_text_stream("Battle Symphony (Official Lyric Video) - Linkin Park.mp3"):
            payload = {"type": getattr(event, "type", None)}

            if hasattr(event, "delta"):
                payload["delta"] = event.delta
            if hasattr(event, "text"):
                payload["text"] = event.text

            yield json.dumps(payload) + "\n"

    return StreamingResponse(generate(), media_type="application/x-ndjson")