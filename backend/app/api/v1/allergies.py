from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_current_user, get_db
from app.models.user import User
from app.models.allergy import UserAllergy
from pydantic import BaseModel
from typing import List

router = APIRouter()

class AllergyItem(BaseModel):
    generic_name: str

class AllergyResponse(BaseModel):
    allergies: List[str]

@router.get("/", response_model=AllergyResponse)
def get_allergies(current_user: User = Depends(get_current_user)):
    allergies = [a.generic_name for a in current_user.allergies]
    return AllergyResponse(allergies=allergies)

@router.post("/", response_model=AllergyResponse)
def add_allergy(allergy: AllergyItem, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    generic = allergy.generic_name.lower().strip()
    
    # Check if already exists
    existing = db.query(UserAllergy).filter(
        UserAllergy.user_id == current_user.id,
        UserAllergy.generic_name == generic
    ).first()
    
    if not existing:
        new_allergy = UserAllergy(user_id=current_user.id, generic_name=generic)
        db.add(new_allergy)
        db.commit()
        db.refresh(current_user)
        
    return AllergyResponse(allergies=[a.generic_name for a in current_user.allergies])

@router.delete("/{generic_name}", response_model=AllergyResponse)
def delete_allergy(generic_name: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    generic = generic_name.lower().strip()
    existing = db.query(UserAllergy).filter(
        UserAllergy.user_id == current_user.id,
        UserAllergy.generic_name == generic
    ).first()
    
    if existing:
        db.delete(existing)
        db.commit()
        db.refresh(current_user)
        
    return AllergyResponse(allergies=[a.generic_name for a in current_user.allergies])
