"""Booking routes for creating and retrieving bookings."""

from fastapi import APIRouter, status, BackgroundTasks
from app.models.booking import BookingCreate, BookingResponse
from app.email_service import send_booking_email
from datetime import datetime
from typing import List
import uuid

router = APIRouter()

# In-memory storage for bookings (temporary solution)
bookings_storage = []


@router.post("/bookings", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
async def create_booking(booking: BookingCreate, background_tasks: BackgroundTasks):
    """Create a new booking.
    
    Generates UUID for booking id and ISO 8601 timestamp for created_at.
    Stores the booking in memory, queues email notification in background, and returns immediately.
    
    Args:
        booking: BookingCreate model with booking details
        background_tasks: FastAPI background tasks for async email sending
        
    Returns:
        BookingResponse with generated id and created_at timestamp
    """
    # Convert Pydantic model to dict
    booking_dict = booking.model_dump()
    
    # Generate UUID for booking id
    booking_dict["id"] = str(uuid.uuid4())
    
    # Generate ISO 8601 timestamp for created_at
    booking_dict["created_at"] = datetime.utcnow().isoformat()
    
    # Store in memory
    bookings_storage.append(booking_dict)
    
    # Send email notification in background (non-blocking)
    background_tasks.add_task(send_booking_email, booking_dict)
    
    # Return immediately without waiting for email
    return booking_dict


@router.get("/bookings", response_model=List[BookingResponse], status_code=status.HTTP_200_OK)
async def list_bookings():
    """Retrieve all bookings sorted by created_at descending.
    
    Returns:
        List of BookingResponse objects sorted by created_at (newest first)
    """
    # Sort bookings by created_at descending
    sorted_bookings = sorted(bookings_storage, key=lambda x: x["created_at"], reverse=True)
    
    return sorted_bookings
