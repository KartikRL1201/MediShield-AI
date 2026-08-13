from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.reminder import FrequencyEnum, DoseStatusEnum

# Schedule Schemas
class ScheduleCreate(BaseModel):
    medicine_name: str
    dosage: str
    frequency: FrequencyEnum = FrequencyEnum.DAILY
    time_of_day: str = Field(..., description="Time in HH:MM format", example="08:00")

class ScheduleResponse(BaseModel):
    id: str
    medicine_name: str
    dosage: str
    frequency: FrequencyEnum
    time_of_day: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# DoseLog Schemas
class DoseLogUpdate(BaseModel):
    status: DoseStatusEnum
    snooze_minutes: Optional[int] = Field(None, description="Number of minutes to snooze if status is 'snoozed'. Typically 15, 30, 45, or 60.")

class DoseLogResponse(BaseModel):
    id: str
    schedule_id: str
    medicine_name: str
    dosage: str
    scheduled_for: datetime
    action_taken_at: Optional[datetime]
    status: DoseStatusEnum
    
    class Config:
        from_attributes = True

# Adherence Schema
class AdherenceScoreResponse(BaseModel):
    total_scheduled: int
    total_taken: int
    total_missed: int
    adherence_percentage: float
