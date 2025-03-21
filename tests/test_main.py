from fastapi.testclient import TestClient
from main import app_f

client = TestClient(app_f)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
