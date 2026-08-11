from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

from sqlalchemy.dialects.postgresql import UUID

class UserAllergy(Base):
    __tablename__ = "user_allergies"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    generic_name = Column(String, index=True, nullable=False)

    user = relationship("User", back_populates="allergies")
