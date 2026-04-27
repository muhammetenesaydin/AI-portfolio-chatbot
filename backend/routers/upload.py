from fastapi import APIRouter, UploadFile, File, Depends, Header
from sqlalchemy.orm import Session
from database import get_db
from models.db_models import Candidate
from services.cv_parser import extract_candidate_data
from services.rag_engine import index_candidate_cv
from services.quiz_engine import generate_quiz
import os
import shutil
import uuid

router = APIRouter(prefix="/api/upload", tags=["Upload"])

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/")
async def upload_cv(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db),
    user_id: str = Header(None) # Frontend'den gelen user_id
):
    if not user_id:
        # Geçici çözüm: Eğer header yoksa (eski frontend), ID 1 varsay (Test için)
        user_id = 1
    
    user_id = int(user_id)
    file_ext = file.filename.split(".")[-1]
    file_name = f"{uuid.uuid4()}.{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, file_name)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 1. CV Analizi
    candidate_data = extract_candidate_data(file_path)
    
    # 2. PROFİL KONTROLÜ (GÜNCELLEME VEYA OLUŞTURMA)
    existing_candidate = db.query(Candidate).filter(Candidate.user_id == user_id).first()
    
    if existing_candidate:
        print(f"LOG: Mevcut aday profili (ID: {existing_candidate.id}) güncelleniyor...")
        existing_candidate.name = candidate_data.get("name", existing_candidate.name)
        existing_candidate.experience_years = candidate_data.get("experience_years", 0)
        existing_candidate.skills = candidate_data.get("skills", [])
        existing_candidate.summary = candidate_data.get("summary", "")
        # Yeni CV yüklendiği için puanı sıfırlayalım ki yeni sınava girsin
        existing_candidate.quiz_score = 0 
        target_candidate = existing_candidate
    else:
        print("LOG: Yeni aday profili oluşturuluyor...")
        new_candidate = Candidate(
            user_id=user_id,
            name=candidate_data.get("name", "Bilinmeyen Aday"),
            experience_years=candidate_data.get("experience_years", 0),
            skills=candidate_data.get("skills", []),
            summary=candidate_data.get("summary", ""),
            quiz_score=0
        )
        db.add(new_candidate)
        target_candidate = new_candidate

    db.commit()
    db.refresh(target_candidate)

    # 3. RAG / Atlas İndeksleme (Eskilerin üzerine yazar veya yeni ekler)
    index_candidate_cv(target_candidate.id, file_path)

    # 4. Quiz Üretme
    quiz = generate_quiz(target_candidate.id, candidate_data.get("summary", ""))

    return {
        "message": "CV başarıyla işlendi",
        "candidate_id": target_candidate.id,
        "quiz": quiz
    }
