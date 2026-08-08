from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, get_current_user
from app.schemas.medicine import Medicine, MedicineCreate, MedicineUpdate
from app.crud import crud_medicine
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[Medicine])
def get_medicines(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """
    Search Medicine API:
    Retrieves a list of medicines. Optionally pass a `search` query parameter to filter by brand or generic name.
    """
    return crud_medicine.get_medicines(db, skip=skip, limit=limit, search=search)


@router.post("/", response_model=Medicine, status_code=status.HTTP_201_CREATED)
def create_medicine(
    medicine_in: MedicineCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create Medicine API:
    Adds a new drug to the catalog. Requires authentication.
    """
    return crud_medicine.create_medicine(db, obj_in=medicine_in)


@router.get("/{medicine_id}", response_model=Medicine)
def get_medicine_details(
    medicine_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Medicine Details API:
    Fetches the full profile for a specific medicine by ID, including interactions and side effects.
    """
    medicine = crud_medicine.get_medicine(db, medicine_id=medicine_id)
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return medicine


@router.put("/{medicine_id}", response_model=Medicine)
def update_medicine(
    medicine_id: str,
    medicine_in: MedicineUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update Medicine API:
    Updates specific fields of an existing medicine (e.g., adding a newly discovered interaction).
    """
    medicine = crud_medicine.get_medicine(db, medicine_id=medicine_id)
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    
    return crud_medicine.update_medicine(db, db_obj=medicine, obj_in=medicine_in)


@router.delete("/{medicine_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_medicine(
    medicine_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete Medicine API:
    Removes a medicine from the database.
    """
    success = crud_medicine.delete_medicine(db, medicine_id=medicine_id)
    if not success:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return None
