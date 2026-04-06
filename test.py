"""from dotenv import load_dotenv
from src.config.config_chat_model import ChatModels
# from src.config.config_audio_model import AudioModel


load_dotenv()
# audio_model = AudioModel()
chat_model = ChatModels()

llm = chat_model.LoadOpenaiChatModel(model_name='gpt-4.1-2025-04-14', temperature = 0.7)
response = llm.invoke('hi')

print(response.content)

# path = 'Battle Symphony (Official Lyric Video) - Linkin Park.mp3'
# event = audio_model.audio_to_text(path)


# segments = []
# for seg in event.segments:
#     segments= {
#     "start": seg.start,
#     "end": seg.end,
#     "text": seg.text
#     }
#     print(segments)"""


from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json
import asyncio

from src.config.config_chat_model import ChatModels

load_dotenv()

app = FastAPI()

chat_model = ChatModels()
llm = chat_model.LoadOpenaiChatModel(
    model_name="gpt-4.1-2025-04-14",
    temperature=0.7,
    streaming = True
)


class ChatRequest(BaseModel):
    message: str


async def sse_generator(user_message: str):
    """
    SSE format:
    event: <event_name>
    data: <payload>

    blank line is required after each event
    """
    try:
        # optional start event
        yield f"event: start\ndata: {json.dumps({'status': 'started'})}\n\n"

        # LangChain streaming
        async for chunk in llm.astream(user_message):
            # chunk can be AIMessageChunk
            text = getattr(chunk, "content", "")

            if not text:
                continue

            # send token/chunk to client
            payload = {"content": text}
            yield f"event: token\ndata: {json.dumps(payload, ensure_ascii=False)}\n\n"

            # gives event loop a chance for proper cancellation/flush
            await asyncio.sleep(0)

        # done event
        yield f"event: done\ndata: {json.dumps({'status': 'completed'})}\n\n"

    except Exception as e:
        error_payload = {"error": str(e)}
        yield f"event: error\ndata: {json.dumps(error_payload, ensure_ascii=False)}\n\n"


@app.post("/chat/stream")
async def chat_stream(payload: ChatRequest):
    return StreamingResponse(
        sse_generator(payload.message),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # useful behind nginx
        },
    )
