import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base
from app.api.dependencies import get_current_user, get_db
from app.models.medicine import Medicine
from app.models.interaction import DrugInteraction
from app.models.user import User
from app.models.allergy import UserAllergy

# Use in-memory SQLite for extremely fast, isolated tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

from sqlalchemy.pool import StaticPool

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    # Create the tables
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    # Mock Database Entries for Edge Cases
    # Generic base forms
    paracetamol = Medicine(brand_name="paracetamol", generic_name="paracetamol")
    dolo = Medicine(brand_name="dolo", generic_name="paracetamol")
    crocin = Medicine(brand_name="crocin", generic_name="paracetamol")
    
    ibuprofen = Medicine(brand_name="ibuprofen", generic_name="ibuprofen")
    advil = Medicine(brand_name="advil", generic_name="ibuprofen")
    motrin = Medicine(brand_name="motrin", generic_name="ibuprofen")
    
    aspirin = Medicine(brand_name="aspirin", generic_name="aspirin")
    warfarin = Medicine(brand_name="warfarin", generic_name="warfarin")
    
    db.add_all([paracetamol, dolo, crocin, ibuprofen, advil, motrin, aspirin, warfarin])
    
    # Mock Interaction (Aspirin + Warfarin = Dangerous Bleeding Risk)
    interaction = DrugInteraction(
        drug_a="aspirin",
        drug_b="warfarin",
        severity="High",
        reason="Increased risk of bleeding.",
        recommendation="Avoid combination if possible."
    )
    db.add(interaction)
    
    db.commit()
    
    yield db
    
    # Teardown
    db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    # Mock an authenticated user with an Ibuprofen allergy
    mock_user = User(email="test@example.com")
    mock_user.allergies = [UserAllergy(generic_name="ibuprofen")]

    def override_get_current_user():
        return mock_user

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    
    with TestClient(app) as c:
        yield c
