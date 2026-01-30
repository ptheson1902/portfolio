"""Chat router for AI-powered Q&A."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database.connection import get_db
from ..models.schemas import ChatRequest, ChatResponse
from ..services.ai_service import AIService

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    Ask questions about the portfolio.
    AI reads from database and provides context-aware answers.
    Public endpoint - no authentication required.
    """
    ai_service = AIService(db)
    return ai_service.chat(
        question=request.question,
        lang=request.lang,
        role=request.role,
        mode=request.mode
    )
