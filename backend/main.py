from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import candidates, upload, chat
import os
from config import settings

app = FastAPI(
    title="AI Profil Chatbot API",
    description="LinkedIn benzeri yetenek platformunun RAG destekli backend servisi.",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Klasörlerin oluşturulması
os.makedirs(settings.upload_dir, exist_ok=True)
os.makedirs(settings.chroma_db_dir, exist_ok=True)

# SQL dbs directory logic
db_path = settings.database_url.replace("sqlite:///", "")
if db_path.startswith("./"):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Router'ların eklenmesi
app.include_router(candidates.router)
app.include_router(upload.router)
app.include_router(chat.router)

@app.get("/")
def read_root():
    return {"message": "AI Profil Chatbot API'sine Hoş Geldiniz! Swagger UI için /docs sayfasına gidin."}
