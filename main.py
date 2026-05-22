from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.router.chat_route import router as chat_router
from api.router.voice_route import router as voice_router




app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://arronwh-website.vercel.app","*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Voice-Session-Id", "X-Voice-Transcript", "X-Voice-Text"],
)
app.include_router(chat_router)
app.include_router(voice_router)
