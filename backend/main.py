from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import candidates, upload, chat, auth, messages
import os
from config import settings

app = FastAPI(
    title="AI Talent Hub API",
    description="LinkedIn-benzeri AI destekli yetenek platformu. RAG + MongoDB Atlas.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs(settings.upload_dir, exist_ok=True)

app.include_router(auth.router)
app.include_router(candidates.router)
app.include_router(upload.router)
app.include_router(chat.router)
app.include_router(messages.router)

@app.get("/")
def root():
    return {
        "platform": "AI Talent Hub",
        "version": "2.0.0",
        "database": "MongoDB Atlas (Single DB)",
        "docs": "/docs"
    }
