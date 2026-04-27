from fastapi import APIRouter, Body, HTTPException
from models.schemas import ChatRequest, ChatResponse
from services.chat_service import chat_service

router = APIRouter(prefix="/api/chat", tags=["Chatbot"])

@router.post("/{candidate_id}", response_model=ChatResponse)
async def chat_with_candidate(candidate_id: int, request: ChatRequest):
    """Adaya soru sor (RAG destekli)"""
    result = await chat_service.get_response(candidate_id, request.message)
    
    return ChatResponse(
        response=result["response"],
        candidate_id=candidate_id,
        sources=result["sources"]
    )

@router.get("/{candidate_id}/history")
async def get_chat_history(candidate_id: int):
    """Sohbet geçmişi (İleride DB'den çekilecek şekilde geliştirilebilir)"""
    return []

@router.post("/{candidate_id}/stream")
async def chat_stream(candidate_id: int, request: ChatRequest):
    """Streaming yanıt (SSE) - WP7 Gelecek Geliştirme"""
    return {"message": "Streaming yakında eklenecek."}
