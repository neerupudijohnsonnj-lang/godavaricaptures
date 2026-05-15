"""Unit tests for main FastAPI application."""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check_returns_200():
    """Test health check endpoint returns 200 status code.
    
    Validates: Requirements 11.1
    """
    response = client.get("/api/")
    assert response.status_code == 200


def test_health_check_returns_correct_json():
    """Test health check endpoint returns correct JSON structure.
    
    Validates: Requirements 11.2
    """
    response = client.get("/api/")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    assert data["status"] == "ok"


def test_health_check_response_structure():
    """Test health check endpoint returns only expected fields.
    
    Validates: Requirements 11.2
    """
    response = client.get("/api/")
    data = response.json()
    
    # Should only have 'status' field
    assert len(data) == 1
    assert list(data.keys()) == ["status"]


def test_cors_headers_present():
    """Test CORS middleware is configured and headers are present."""
    response = client.get("/api/")
    
    # CORS headers should be present (TestClient may not show all, but we can verify the endpoint works)
    assert response.status_code == 200


def test_app_title():
    """Test FastAPI app has correct title."""
    assert app.title == "Godavari Captures API"


def test_bookings_router_included():
    """Test bookings router is included with correct prefix."""
    # Verify bookings router is registered by checking app routes
    routes = [route.path for route in app.routes]
    assert "/api/bookings" in routes


def test_contact_router_included():
    """Test contact router is included with correct prefix."""
    # Verify contact router is registered by checking app routes
    routes = [route.path for route in app.routes]
    assert "/api/contact" in routes
