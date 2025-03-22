import pytest
from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()
MONGODB = os.getenv("MONGODB_URI")

@pytest.fixture(scope="module")
def mongo_client():
    """Fixture para crear y cerrar la conexión a MongoDB"""
    try:
        client = MongoClient(MONGODB, serverSelectionTimeoutMS=6000)  
        client.admin.command("ping")  # Prueba la conexión
        return client
    except Exception as e:
        pytest.fail(f"No se pudo conectar a MongoDB: {e}")

def test_mongodb_connection(mongo_client):
    """Prueba la conexión a MongoDB"""
    dbs = mongo_client.list_database_names()
    assert isinstance(dbs, list), "No se pudo obtener la lista de bases de datos"