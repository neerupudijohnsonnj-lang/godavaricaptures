"""Pydantic models for booking requests and responses."""

from pydantic import BaseModel, Field


class BookingCreate(BaseModel):
    """Request model for creating a new booking.
    
    All fields except message and event_time are required with minimum length validation.
    """
    name: str = Field(..., min_length=1)
    phone: str = Field(..., min_length=1)
    service: str = Field(..., min_length=1)
    event_date: str = Field(..., min_length=1)
    event_time: str = ""
    location: str = Field(..., min_length=1)
    message: str = ""


class BookingResponse(BaseModel):
    """Response model for booking data.
    
    Includes all booking fields plus generated id and created_at timestamp.
    """
    id: str
    name: str
    phone: str
    service: str
    event_date: str
    event_time: str
    location: str
    message: str
    created_at: str
