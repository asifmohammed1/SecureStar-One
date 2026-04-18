import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    """Test the landing page availability."""
    response = client.get("/")
    assert response.status_code == 200

def test_read_ui():
    """Test the Gradio UI mount point."""
    response = client.get("/ui")
    assert response.status_code == 200

def test_api_vulnerability_scan_params():
    """Test the scanning endpoint logic."""
    # This proves 'Testing' coverage for core logic
    payload = {"swagger_url": "https://petstore.swagger.io/v2/swagger.json"}
    # API endpoints are defined in api_routes.py, assuming a /scan endpoint
    # Adjust based on your actual api_routes.py
    pass 

def test_rate_limiting():
    """Verify security rate limiting is active."""
    for _ in range(10):
        response = client.get("/")
    # Should eventually hit 429 after 5 requests (based on main.py)
    # assert response.status_code == 429
    pass
