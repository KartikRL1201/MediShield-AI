import pytest
from app.services.interaction_service import check_interactions
from sqlalchemy.orm import Session
from app.models.interaction import DrugInteraction

class MockSessionInteractions:
    def __init__(self, db_data):
        self.db_data = db_data

    def query(self, *args):
        return self

    def filter(self, *args):
        return self

    def first(self):
        # We need a way to return the interaction if it matches.
        # But `check_interactions` loops over combinations and calls `filter(...)`.
        # For a simple mock, we'll just check if a flag was set or return a specific item.
        return self.db_data.pop(0) if self.db_data else None

def test_check_interactions_no_conflict():
    db = MockSessionInteractions([]) # No interactions found in DB
    medicines = ["Amoxicillin", "Vitamin C"]
    result = check_interactions(medicines, db)
    
    assert len(result.interactions) == 0
    assert result.status == "Safe"

def test_check_interactions_with_conflict():
    # Mocking the DB returning a high severity interaction
    mock_interaction = DrugInteraction(
        drug_a="ASPIRIN",
        drug_b="WARFARIN",
        severity="High",
        reason="Increased risk of bleeding",
        recommendation="Avoid combination"
    )
    db = MockSessionInteractions([mock_interaction])
    medicines = ["Aspirin", "Warfarin"]
    result = check_interactions(medicines, db)
    
    assert len(result.interactions) == 1
    assert result.interactions[0].severity == "High"
    assert "Aspirin" in result.interactions[0].drug_a or "Aspirin" in result.interactions[0].drug_b
