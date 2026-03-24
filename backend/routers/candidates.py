from fastapi import APIRouter
from typing import List
from models.schemas import CandidateResponse

router = APIRouter(prefix="/api/candidates", tags=["Candidates"])

@router.get("/", response_model=List[CandidateResponse])
async def get_candidates():
    """Tüm adayları listele."""
    return []

@router.get("/{id}", response_model=CandidateResponse)
async def get_candidate(id: int):
    """Aday detayını getir."""
    return CandidateResponse(id=id, name="Enes Kaya", skills=["Python", "FastAPI", "React Native"], experience_years=3, quiz_score=85)

@router.delete("/{id}")
async def delete_candidate(id: int):
    """Adayı sil."""
    return {"status": "Aday silindi"}

@router.get("/search")
async def search_candidates(q: str):
    """Aday ara."""
    return []
