from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings
import chromadb
import os

db_url = settings.database_url
if db_url.startswith("sqlite:///./"):
    os.makedirs(os.path.dirname(db_url.replace("sqlite:///", "")), exist_ok=True)

engine = create_engine(db_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ChromaDB Initialization
chroma_client = chromadb.PersistentClient(path=settings.chroma_db_dir)
