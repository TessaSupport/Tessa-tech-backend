from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        'message': 'Welcome to the Terra Customer Support AI Agent API',
        'status': 'healthy, API is running',
        'docs': '/docs',
        'redoc': '/redoc'
    }

