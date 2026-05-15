"""Unit tests for booking Pydantic models."""

import pytest
from pydantic import ValidationError
from app.models.booking import BookingCreate, BookingResponse


class TestBookingCreate:
    """Test suite for BookingCreate request model."""
    
    def test_valid_booking_create(self):
        """Test creating a valid booking with all required fields."""
        booking = BookingCreate(
            name="John Doe",
            phone="9876543210",
            service="Wedding Photography",
            event_date="2024-06-15",
            event_time="10:00 AM",
            location="Rajahmundry"
        )
        
        assert booking.name == "John Doe"
        assert booking.phone == "9876543210"
        assert booking.service == "Wedding Photography"
        assert booking.event_date == "2024-06-15"
        assert booking.event_time == "10:00 AM"
        assert booking.location == "Rajahmundry"
        assert booking.message == ""
    
    def test_booking_create_with_message(self):
        """Test creating a booking with optional message field."""
        booking = BookingCreate(
            name="Jane Smith",
            phone="9123456789",
            service="Photoshoot",
            event_date="2024-07-20",
            event_time="2:00 PM",
            location="Hyderabad",
            message="Looking forward to the session!"
        )
        
        assert booking.message == "Looking forward to the session!"
    
    def test_booking_create_missing_required_field(self):
        """Test that missing required fields raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            BookingCreate(
                name="John Doe",
                phone="9876543210",
                service="Wedding Photography",
                event_date="2024-06-15",
                event_time="10:00 AM"
                # location is missing
            )
        
        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["loc"] == ("location",)
        assert errors[0]["type"] == "missing"
    
    def test_booking_create_empty_string_validation(self):
        """Test that empty strings fail min_length validation."""
        with pytest.raises(ValidationError) as exc_info:
            BookingCreate(
                name="",  # Empty string should fail min_length=1
                phone="9876543210",
                service="Wedding Photography",
                event_date="2024-06-15",
                event_time="10:00 AM",
                location="Rajahmundry"
            )
        
        errors = exc_info.value.errors()
        assert any(
            error["loc"] == ("name",) and "at least 1 character" in str(error["msg"]).lower()
            for error in errors
        )
    
    def test_booking_create_all_fields_empty_strings(self):
        """Test that all required fields with empty strings fail validation."""
        with pytest.raises(ValidationError) as exc_info:
            BookingCreate(
                name="",
                phone="",
                service="",
                event_date="",
                event_time="",
                location=""
            )
        
        errors = exc_info.value.errors()
        # All 6 required fields should have validation errors
        assert len(errors) == 6
        field_names = {error["loc"][0] for error in errors}
        assert field_names == {"name", "phone", "service", "event_date", "event_time", "location"}


class TestBookingResponse:
    """Test suite for BookingResponse model."""
    
    def test_valid_booking_response(self):
        """Test creating a valid booking response with all fields."""
        response = BookingResponse(
            id="123e4567-e89b-12d3-a456-426614174000",
            name="John Doe",
            phone="9876543210",
            service="Wedding Photography",
            event_date="2024-06-15",
            event_time="10:00 AM",
            location="Rajahmundry",
            message="Looking forward to it!",
            created_at="2024-01-15T10:30:00Z"
        )
        
        assert response.id == "123e4567-e89b-12d3-a456-426614174000"
        assert response.name == "John Doe"
        assert response.phone == "9876543210"
        assert response.service == "Wedding Photography"
        assert response.event_date == "2024-06-15"
        assert response.event_time == "10:00 AM"
        assert response.location == "Rajahmundry"
        assert response.message == "Looking forward to it!"
        assert response.created_at == "2024-01-15T10:30:00Z"
    
    def test_booking_response_missing_field(self):
        """Test that missing required fields in response raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            BookingResponse(
                id="123e4567-e89b-12d3-a456-426614174000",
                name="John Doe",
                phone="9876543210",
                service="Wedding Photography",
                event_date="2024-06-15",
                event_time="10:00 AM",
                location="Rajahmundry",
                message=""
                # created_at is missing
            )
        
        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["loc"] == ("created_at",)
        assert errors[0]["type"] == "missing"
    
    def test_booking_response_empty_message(self):
        """Test that empty message is allowed in response."""
        response = BookingResponse(
            id="123e4567-e89b-12d3-a456-426614174000",
            name="John Doe",
            phone="9876543210",
            service="Wedding Photography",
            event_date="2024-06-15",
            event_time="10:00 AM",
            location="Rajahmundry",
            message="",
            created_at="2024-01-15T10:30:00Z"
        )
        
        assert response.message == ""
