from fastapi.testclient import TestClient

from scripts.api.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to VarPipe-Dx API"}

def test_get_samples():
    response = client.get("/samples")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_variants():
    response = client.get("/variants?gene=BRCA1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
