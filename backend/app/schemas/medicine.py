from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

class MedicineBase(BaseModel):
    brand_name: str
    generic_name: str
    composition: Optional[str] = None
    strength: Optional[str] = None
    manufacturer: Optional[str] = None
    side_effects: Optional[str] = None
    food_interactions: Optional[str] = None
    alcohol_interaction: Optional[str] = None
    pregnancy_warning: Optional[str] = None
    storage: Optional[str] = None
    prescription_required: bool = False

class MedicineCreate(MedicineBase):
    pass

class MedicineUpdate(BaseModel):
    brand_name: Optional[str] = None
    generic_name: Optional[str] = None
    composition: Optional[str] = None
    strength: Optional[str] = None
    manufacturer: Optional[str] = None
    side_effects: Optional[str] = None
    food_interactions: Optional[str] = None
    alcohol_interaction: Optional[str] = None
    pregnancy_warning: Optional[str] = None
    storage: Optional[str] = None
    prescription_required: Optional[bool] = None

class Medicine(MedicineBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
