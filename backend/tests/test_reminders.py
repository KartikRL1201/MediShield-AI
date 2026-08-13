import pytest
from datetime import datetime, timedelta
from app.services.reminder_service import calculate_adherence
from app.models.reminder import DoseLog, DoseStatusEnum, MedicineSchedule

class MockSession:
    def __init__(self, logs):
        self.logs = logs

    def query(self, *args):
        return self

    def join(self, *args):
        return self

    def filter(self, *args):
        return self

    def all(self):
        return self.logs

def test_adherence_perfect_score():
    logs = [
        DoseLog(status=DoseStatusEnum.TAKEN),
        DoseLog(status=DoseStatusEnum.TAKEN),
        DoseLog(status=DoseStatusEnum.TAKEN)
    ]
    db = MockSession(logs)
    result = calculate_adherence(db, "user1")
    
    assert result["total_scheduled"] == 3
    assert result["total_taken"] == 3
    assert result["total_missed"] == 0
    assert result["adherence_percentage"] == 100.0

def test_adherence_mixed_score():
    logs = [
        DoseLog(status=DoseStatusEnum.TAKEN),
        DoseLog(status=DoseStatusEnum.MISSED),
        DoseLog(status=DoseStatusEnum.SKIPPED),
        DoseLog(status=DoseStatusEnum.TAKEN)
    ]
    db = MockSession(logs)
    result = calculate_adherence(db, "user1")
    
    assert result["total_scheduled"] == 4
    assert result["total_taken"] == 2
    assert result["total_missed"] == 2
    assert result["adherence_percentage"] == 50.0

def test_adherence_empty():
    logs = []
    db = MockSession(logs)
    result = calculate_adherence(db, "user1")
    
    assert result["total_scheduled"] == 0
    assert result["total_taken"] == 0
    assert result["total_missed"] == 0
    assert result["adherence_percentage"] == 100.0
