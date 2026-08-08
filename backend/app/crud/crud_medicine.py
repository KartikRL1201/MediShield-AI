from sqlalchemy.orm import Session
from sqlalchemy import or_
import uuid
from app.models.medicine import Medicine
from app.schemas.medicine import MedicineCreate, MedicineUpdate

def get_medicine(db: Session, medicine_id: str) -> Medicine | None:
    try:
        uid = uuid.UUID(medicine_id)
    except ValueError:
        return None
    return db.query(Medicine).filter(Medicine.id == uid).first()

def get_medicines(db: Session, skip: int = 0, limit: int = 100, search: str | None = None):
    query = db.query(Medicine)
    if search:
        # Simple case-insensitive search on brand and generic name
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Medicine.brand_name.ilike(search_term),
                Medicine.generic_name.ilike(search_term)
            )
        )
    return query.offset(skip).limit(limit).all()

def create_medicine(db: Session, obj_in: MedicineCreate) -> Medicine:
    db_obj = Medicine(**obj_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_medicine(db: Session, db_obj: Medicine, obj_in: MedicineUpdate) -> Medicine:
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_medicine(db: Session, medicine_id: str) -> bool:
    db_obj = get_medicine(db, medicine_id)
    if db_obj:
        db.delete(db_obj)
        db.commit()
        return True
    return False
