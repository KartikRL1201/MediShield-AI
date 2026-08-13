import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class FrequencyEnum(str, enum.Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    AS_NEEDED = "as_needed"

class DoseStatusEnum(str, enum.Enum):
    PENDING = "pending"
    TAKEN = "taken"
    SKIPPED = "skipped"
    SNOOZED = "snoozed"
    MISSED = "missed" # Status when 1 hour has passed without action

class MedicineSchedule(Base):
    __tablename__ = "medicine_schedules"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    medicine_name = Column(String, nullable=False)
    dosage = Column(String, nullable=False)
    frequency = Column(SQLEnum(FrequencyEnum), default=FrequencyEnum.DAILY, nullable=False)
    time_of_day = Column(String, nullable=False) # e.g. "08:00"
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    user = relationship("User", backref="schedules")
    dose_logs = relationship("DoseLog", back_populates="schedule", cascade="all, delete-orphan")

class DoseLog(Base):
    __tablename__ = "dose_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    schedule_id = Column(String, ForeignKey("medicine_schedules.id", ondelete="CASCADE"), nullable=False)
    scheduled_for = Column(DateTime, nullable=False)
    action_taken_at = Column(DateTime, nullable=True)
    status = Column(SQLEnum(DoseStatusEnum), default=DoseStatusEnum.PENDING, nullable=False)

    schedule = relationship("MedicineSchedule", back_populates="dose_logs")
