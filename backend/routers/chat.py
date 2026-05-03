from fastapi import APIRouter
from pydantic import BaseModel
from services.chat_service import chat_service

router = APIRouter(prefix="/api/chat", tags=["Chatbot"])

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    candidate_id: str
    sources: list = []

@router.post("/{candidate_id}")
async def chat_with_candidate(candidate_id: str, request: ChatRequest):
    """Adaya soru sor (RAG + Gemini destekli). candidate_id MongoDB ObjectId string."""
    result = await chat_service.get_response(candidate_id, request.message)
    return {
        "response": result["response"],
        "candidate_id": candidate_id,
        "sources": result.get("sources", [])
    }

@router.get("/{candidate_id}/history")
async def get_chat_history(candidate_id: str):
    """Sohbet geçmişi — İleride MongoDB'den çekilecek."""
    return []
