from sqlalchemy.orm import Session
import uuid
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: str) -> User | None:
    try:
        uid = uuid.UUID(user_id)
    except ValueError:
        return None
    return db.query(User).filter(User.id == uid).first()

def create_user(db: Session, user_in: UserCreate) -> User:
    hashed_password = get_password_hash(user_in.password)
    db_user = User(
        email=user_in.email,
        password_hash=hashed_password,
        first_name=user_in.first_name,
        last_name=user_in.last_name,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
