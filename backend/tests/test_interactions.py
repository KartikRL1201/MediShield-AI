import time
from fastapi.testclient import TestClient

def test_exact_match_and_duplicates(client: TestClient):
    # Test grouping exact matches into duplicates
    payload = {"medicines": ["paracetamol", "dolo", "crocin"]}
    response = client.post("/api/v1/interactions/check", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    assert len(data["duplicates"]) == 1
    assert data["duplicates"][0]["generic_name"] == "paracetamol"
    assert set(data["duplicates"][0]["brands_found"]) == {"paracetamol", "dolo", "crocin"}
    assert data["status"] == "Safe"

def test_regex_stripper(client: TestClient):
    # Test that numbers, mg, xr, and advance are stripped out
    payload = {"medicines": ["dolo 650", "crocin advance", "paracetamol 500mg"]}
    response = client.post("/api/v1/interactions/check", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    # Should resolve down to paracetamol and flag as duplicate
    assert len(data["duplicates"]) == 1
    assert data["duplicates"][0]["generic_name"] == "paracetamol"
    # Note: the engine preserves the original brand names in the duplicate list
    assert set(data["duplicates"][0]["brands_found"]) == {"dolo 650", "crocin advance", "paracetamol 500mg"}
    assert len(data["unknown_medicines"]) == 0

def test_fuzzy_fallback(client: TestClient):
    # Test slightly misspelled drug caught by LIKE query
    # In conftest, we added 'ibuprofen'. Let's search for 'ibuprofe'
    payload = {"medicines": ["ibuprofe"]}
    response = client.post("/api/v1/interactions/check", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    # Since ibuprofen is in the mock user's allergy profile, it should trigger Dangerous!
    assert "ibuprofen" in data["allergies_triggered"]
    assert data["status"] == "Dangerous"

def test_allergy_trigger(client: TestClient):
    # The authenticated user has an ibuprofen allergy
    payload = {"medicines": ["advil", "motrin"]}
    response = client.post("/api/v1/interactions/check", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    assert len(data["allergies_triggered"]) == 1
    assert data["allergies_triggered"][0] == "ibuprofen"
    assert data["status"] == "Dangerous"

def test_drug_interactions(client: TestClient):
    # Test clinical interaction between Aspirin and Warfarin
    payload = {"medicines": ["aspirin", "warfarin"]}
    response = client.post("/api/v1/interactions/check", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    assert len(data["interactions"]) == 1
    assert data["interactions"][0]["severity"] == "High"
    assert data["status"] == "Dangerous"

def test_unknown_medicines(client: TestClient):
    payload = {"medicines": ["fake_drug_123", "random_drug_xyz"]}
    response = client.post("/api/v1/interactions/check", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    assert len(data["unknown_medicines"]) == 2
    assert "fake_drug_123" in data["unknown_medicines"]
    assert data["status"] == "Unknown"

def test_performance_speed(client: TestClient):
    # Run the regex stripper, DB lookup, and duplicate engine, and measure time
    payload = {"medicines": ["dolo 650", "crocin advance", "paracetamol 500mg"]}
    
    start_time = time.time()
    response = client.post("/api/v1/interactions/check", json=payload)
    end_time = time.time()
    
    execution_time_ms = (end_time - start_time) * 1000
    print(f"\nExecution Time: {execution_time_ms:.2f} ms")
    
    # Ensure it runs in under 100ms
    assert execution_time_ms < 100
    assert response.status_code == 200
