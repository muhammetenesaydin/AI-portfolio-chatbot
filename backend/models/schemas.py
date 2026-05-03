from pydantic import BaseModel
from typing import List, Optional

class CandidateBase(BaseModel):
    name: str
    skills: List[str]
    experience_years: int

class CandidateCreate(CandidateBase):
    pass

class CandidateResponse(CandidateBase):
    id: int
    quiz_score: Optional[int] = None

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    candidate_id: int
    sources: List[str]
