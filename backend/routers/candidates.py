from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.schemas import CandidateResponse
from models.db_models import Candidate, Quiz
from database import get_db

router = APIRouter(prefix="/api/candidates", tags=["Candidates"])

@router.get("/", response_model=List[CandidateResponse])
async def get_candidates(db: Session = Depends(get_db)):
    """Tüm adayları listele."""
    candidates = db.query(Candidate).all()
    # Pydantic için uygun formata dönüştür
    res = []
    for c in candidates:
        res.append(CandidateResponse(
            id=c.id,
            name=c.name,
            skills=c.skills if c.skills else [],
            experience_years=c.experience_years or 0,
            quiz_score=c.quiz_score
        ))
    return res

@router.get("/{id}", response_model=dict)
async def get_candidate(id: int, db: Session = Depends(get_db)):
    """Aday detayını ve ilişkili quiz'i getir."""
    candidate = db.query(Candidate).filter(Candidate.id == id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Aday bulunamadı")
    
    quiz = db.query(Quiz).filter(Quiz.candidate_id == id).first()
    
    return {
        "candidate": {
            "id": candidate.id,
            "name": candidate.name,
            "skills": candidate.skills,
            "experience_years": candidate.experience_years,
            "quiz_score": candidate.quiz_score
        },
        "quiz": quiz.questions if quiz else None
    }

@router.delete("/{id}")
async def delete_candidate(id: int, db: Session = Depends(get_db)):
    """Adayı sil."""
    candidate = db.query(Candidate).filter(Candidate.id == id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Aday bulunamadı")
        
    db.delete(candidate)
    db.commit()
    return {"status": "Aday başarıyla silindi"}

@router.get("/search")
async def search_candidates(q: str, db: Session = Depends(get_db)):
    """Aday ara (skills veya isime göre - basit %LIKE%)."""
    search_term = f"%{q}%"
    candidates = db.query(Candidate).filter(Candidate.name.ilike(search_term)).all()
    
    res = []
    for c in candidates:
        res.append({
            "id": c.id,
            "name": c.name,
            "skills": c.skills or [],
            "experience_years": c.experience_years or 0
        })
    return res
