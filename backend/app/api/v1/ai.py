from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, get_current_user
from app.schemas.ai import AIQueryRequest, AIQueryResponse
from app.services.ai_service import ask_medical_question
from app.models.user import User

router = APIRouter()

@router.post("/ask", response_model=AIQueryResponse)
def ask_ai(
    request: AIQueryRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    RAG AI Endpoint:
    Accepts a list of medicines and a user query.
    Retrieves facts from the database and uses an LLM to formulate a simplified, strictly grounded answer.
    """
    if not request.medicines:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Must provide at least one medicine to query about.")
        
    answer = ask_medical_question(request.medicines, request.query, db)
    
    return AIQueryResponse(answer=answer)
