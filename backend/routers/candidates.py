from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.db_models import Candidate, User
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/api/candidates", tags=["Candidates"])

@router.get("/")
def get_candidates(db: Session = Depends(get_db)):
    return db.query(Candidate).all()

@router.get("/my-quizzes/{user_id}")
def get_my_quizzes(user_id: int, db: Session = Depends(get_db)):
    # Kullanıcının oluşturduğu aday profillerini (ve dolayısıyla sınav sonuçlarını) getir
    results = db.query(Candidate).filter(Candidate.user_id == user_id).all()
    return results

@router.get("/{candidate_id}")
def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Aday bulunamadı")
    return candidate

class QuizSubmit(BaseModel):
    quiz_id: int
    answers: List[int]

@router.post("/{candidate_id}/quiz/submit")
def submit_quiz(candidate_id: int, req: QuizSubmit, db: Session = Depends(get_db)):
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Aday bulunamadı")
    
    # Basit skor hesaplama (Gerçekte Quiz tablosundan kontrol edilir)
    # Burada test amaçlı her zaman %85 veriyoruz veya rastgele bir mantık
    candidate.quiz_score = 85 
    db.commit()
    return {"score": 85}
