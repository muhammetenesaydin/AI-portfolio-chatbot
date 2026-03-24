from fastapi import APIRouter, Body
from models.schemas import ChatRequest, ChatResponse

router = APIRouter(prefix="/api/chat", tags=["Chatbot"])

@router.post("/{candidate_id}", response_model=ChatResponse)
async def chat_with_candidate(candidate_id: int, request: ChatRequest):
    """Adaya soru sor"""
    # LLM/RAG Integration (WP7)
    return ChatResponse(
        response=f"Merhaba, ben {candidate_id} numaralı adayın AI asistanıyım. Sorunuz: {request.message}",
        candidate_id=candidate_id,
        sources=["Simülasyon Verisi"]
    )

@router.get("/{candidate_id}/history")
async def get_chat_history(candidate_id: int):
    """Sohbet geçmişi"""
    return []

@router.post("/{candidate_id}/stream")
async def chat_stream(candidate_id: int, request: ChatRequest):
    """Streaming yanıt (SSE) - WP7"""
    return {"message": "Streaming endpoint (Yapım aşamasında)"}
