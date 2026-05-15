"""Unit tests for booking routes."""

import pytest
from datetime import datetime
import uuid


def test_booking_route_imports():
    """Test that booking route module can be imported."""
    from app.routes.bookings import router, create_booking
    
    assert router is not None
    assert create_booking is not None


def test_booking_response_structure():
    """Test that BookingResponse model has all required fields."""
    from app.models.booking import BookingResponse
    
    # Create a sample booking response
    booking_data = {
        "id": str(uuid.uuid4()),
        "name": "Test User",
        "phone": "1234567890",
        "service": "Wedding Photography",
        "event_date": "2024-06-15",
        "event_time": "14:00",
        "location": "Rajahmundry",
        "message": "Looking forward to the event",
        "created_at": datetime.utcnow().isoformat()
    }
    
    booking = BookingResponse(**booking_data)
    
    assert booking.id == booking_data["id"]
    assert booking.name == booking_data["name"]
    assert booking.phone == booking_data["phone"]
    assert booking.service == booking_data["service"]
    assert booking.event_date == booking_data["event_date"]
    assert booking.event_time == booking_data["event_time"]
    assert booking.location == booking_data["location"]
    assert booking.message == booking_data["message"]
    assert booking.created_at == booking_data["created_at"]


def test_booking_create_validation():
    """Test that BookingCreate model validates required fields."""
    from app.models.booking import BookingCreate
    from pydantic import ValidationError
    
    # Valid booking data
    valid_data = {
        "name": "Test User",
        "phone": "1234567890",
        "service": "Wedding Photography",
        "event_date": "2024-06-15",
        "event_time": "14:00",
        "location": "Rajahmundry",
        "message": "Test message"
    }
    
    booking = BookingCreate(**valid_data)
    assert booking.name == "Test User"
    
    # Test missing required field
    invalid_data = valid_data.copy()
    del invalid_data["name"]
    
    with pytest.raises(ValidationError):
        BookingCreate(**invalid_data)
    
    # Test empty string for required field
    invalid_data = valid_data.copy()
    invalid_data["name"] = ""
    
    with pytest.raises(ValidationError):
        BookingCreate(**invalid_data)
