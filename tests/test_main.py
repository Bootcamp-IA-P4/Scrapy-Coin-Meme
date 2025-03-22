from fastapi.testclient import TestClient
import sys
import os
#from main import app
from app_base.main import app
# Agregar la carpeta raíz al sys.path para importar 'app'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
