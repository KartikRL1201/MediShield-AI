from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.reminder import (
    ScheduleCreate, ScheduleResponse, 
    DoseLogUpdate, DoseLogResponse, 
    AdherenceScoreResponse
)
from app.services.reminder_service import (
    create_schedule, get_or_generate_todays_logs, 
    update_dose_status, calculate_adherence
)

router = APIRouter()

@router.post("/schedule", response_model=ScheduleResponse, status_code=status.HTTP_201_CREATED)
def add_schedule(
    request: ScheduleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new medicine schedule/reminder rule."""
    return create_schedule(db, current_user.id, request)

@router.get("/today", response_model=List[DoseLogResponse])
def get_todays_schedule(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all medicine doses for today. 
    Automatically evaluates if any pending doses are >1 hour late and marks them MISSED.
    """
    logs = get_or_generate_todays_logs(db, current_user.id)
    # We need to map schedule details into the response
    response_logs = []
    for log in logs:
        response_logs.append(DoseLogResponse(
            id=log.id,
            schedule_id=log.schedule_id,
            medicine_name=log.schedule.medicine_name,
            dosage=log.schedule.dosage,
            scheduled_for=log.scheduled_for,
            action_taken_at=log.action_taken_at,
            status=log.status
        ))
    return response_logs

@router.put("/log/{log_id}", response_model=DoseLogResponse)
def update_log_status(
    log_id: str,
    update_data: DoseLogUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Mark a dose as Taken, Skipped, or Snoozed.
    If Snoozed, pass `snooze_minutes` to push it back.
    """
    try:
        log = update_dose_status(db, current_user.id, log_id, update_data)
        return DoseLogResponse(
            id=log.id,
            schedule_id=log.schedule_id,
            medicine_name=log.schedule.medicine_name,
            dosage=log.schedule.dosage,
            scheduled_for=log.scheduled_for,
            action_taken_at=log.action_taken_at,
            status=log.status
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/adherence", response_model=AdherenceScoreResponse)
def get_adherence_score(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Calculate the user's overall adherence percentage."""
    return calculate_adherence(db, current_user.id)
