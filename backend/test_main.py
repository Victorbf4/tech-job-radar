from fastapi.testclient import TestClient
from app.main import app  # Importamos tu aplicación FastAPI

# Creamos un cliente de prueba que simulará ser el frontend
client = TestClient(app)

def test_get_jobs():
    # Simulamos una petición GET a tu endpoint
    response = client.get("/api/jobs")
    
    # 1. Verificamos que el servidor responda con un OK (200)
    assert response.status_code == 200
    
    # 2. Verificamos que la respuesta sea una lista (JSON array)
    assert isinstance(response.json(), list)