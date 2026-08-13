import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal, Base, engine
from app.models.user import User
from app.core.security import get_password_hash

# Set up test database
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def setup_db():
    db = SessionLocal()
    # Create test user
    user = db.query(User).filter(User.email == "testapi@example.com").first()
    if not user:
        user = User(
            email="testapi@example.com",
            password_hash=get_password_hash("password123"),
            first_name="API",
            last_name="Test"
        )
        db.add(user)
        db.commit()
    yield db
    db.close()

def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "MediShield AI API is running"}

def test_login_success(client, setup_db):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "testapi@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_failure(client, setup_db):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "testapi@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401

def test_protected_route_without_token(client):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401
