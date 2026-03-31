from fastapi import APIRouter, UploadFile, File, BackgroundTasks, Depends
from sqlalchemy.orm import Session
import shutil
import os
from config import settings
from database import get_db
from models.db_models import Candidate, Quiz
from services.cv_parser import cv_parser
from services.quiz_engine import quiz_engine
from services.rag_engine import rag_engine

router = APIRouter(prefix="/api/upload", tags=["Upload"])

def process_cv_background(file_path: str, candidate_id: int, db: Session):
    try:
        # 1. Metin Çıkarımı
        raw_text = cv_parser.parse_file(file_path)
        
        # 2. LLM ile Aday Bilgilerini Çıkarma
        candidate_info = quiz_engine.extract_candidate_info(raw_text)
        
        # 3. Veritabanını Güncelleme
        candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
        if candidate:
            candidate.name = candidate_info.name
            candidate.skills = candidate_info.skills
            candidate.experience_years = candidate_info.experience_years
            candidate.raw_text = raw_text
            db.commit()

        # 4. RAG Vektörleştirme
        rag_engine.index_cv(candidate_id, raw_text)

        # 5. Quiz Üretimi ve Kaydı
        quiz_data = quiz_engine.generate_quiz_from_text(raw_text, candidate_info.skills)
        new_quiz = Quiz(candidate_id=candidate_id, questions=quiz_data)
        db.add(new_quiz)
        db.commit()
    except Exception as e:
        print(f"Background işlemi hatası: {e}")

@router.post("/")
async def upload_cv(
    background_tasks: BackgroundTasks, 
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """CV/Portfolyo yükle (PDF, DOCX) ve RAG pipeline ile entegre et."""
    file_location = os.path.join(settings.upload_dir, file.filename)
    
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Önce adayı dummy olarak DB'ye ekle
    new_cand = Candidate(name="İşleniyor...", skills=[], experience_years=0)
    db.add(new_cand)
    db.commit()
    db.refresh(new_cand)

    # Arka planda Metin okuma -> Vector DB -> Quiz pipeline'ını çalıştır
    background_tasks.add_task(process_cv_background, file_location, new_cand.id, db)

    return {"message": "Dosya başarıyla yüklendi, yapay zeka tarafından işleniyor.", "candidate_id": new_cand.id}

@router.post("/sample")
async def upload_sample():
    """Örnek veri yükle"""
    return {"status": "Örnek veriler sisteme eklendi."}
