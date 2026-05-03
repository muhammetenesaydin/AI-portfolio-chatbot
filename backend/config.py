from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    llm_provider: str = os.getenv("LLM_PROVIDER", "gemini")
    
    # Gemini
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    
    # OpenAI (fallback)
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    openai_embedding_model: str = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    
    # Ollama (offline fallback)
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3")

    # MongoDB Atlas — TEK VERİTABANI
    mongodb_uri: str = os.getenv("MONGODB_URI", "")
    mongodb_db_name: str = os.getenv("MONGODB_DB_NAME", "ai_talent_hub")
    mongodb_collection_name: str = os.getenv("MONGODB_COLLECTION_NAME", "cv_vectors")
    mongodb_index_name: str = os.getenv("MONGODB_INDEX_NAME", "vector_index")

    # Dosya yükleme
    upload_dir: str = os.getenv("UPLOAD_DIR", "./data/uploads")
    db_dir: str = os.getenv("DB_DIR", "./data/db")

settings = Settings()
