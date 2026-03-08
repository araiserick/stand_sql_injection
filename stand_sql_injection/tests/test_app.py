"""
Module: test_app.py
Description: This module contains unit tests for the FastAPI application defined in app.py.
"""

from fastapi.testclient import TestClient

from src.app import app

def test_health_check():
    """
    Test the health check endpoint.
    """
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
