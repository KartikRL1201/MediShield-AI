import uuid
from sqlalchemy import Column, String, Boolean, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
from app.core.database import Base

class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    brand_name = Column(String, index=True, nullable=False)
    generic_name = Column(String, index=True, nullable=False)
    composition = Column(Text, nullable=True)
    strength = Column(String, nullable=True)
    manufacturer = Column(String, nullable=True)
    side_effects = Column(Text, nullable=True)
    food_interactions = Column(Text, nullable=True)
    alcohol_interaction = Column(Text, nullable=True)
    pregnancy_warning = Column(Text, nullable=True)
    storage = Column(String, nullable=True)
    prescription_required = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
