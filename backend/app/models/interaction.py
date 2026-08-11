import uuid
from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class DrugInteraction(Base):
    __tablename__ = "interactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    drug_a = Column(String, index=True, nullable=False)
    drug_b = Column(String, index=True, nullable=False)
    severity = Column(String, nullable=False) # e.g., 'Mild', 'Moderate', 'Severe'
    reason = Column(Text, nullable=False)
    recommendation = Column(Text, nullable=False)
