from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.interaction import InteractionCheckRequest, InteractionCheckResponse
from app.services.interaction_service import check_interactions

router = APIRouter()

@router.post("/check", response_model=InteractionCheckResponse)
def check_drug_interactions(
    request: InteractionCheckRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Drug Interaction Check API:
    Accepts a list of medication names and returns all known interactions using a highly scalable combinatorial matching algorithm.
    """
    try:
        return check_interactions(request.medicines, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to check interactions: {str(e)}")
