"""Contact routes for creating and retrieving contact messages."""

from fastapi import APIRouter, status
from app.models.contact import ContactCreate, ContactResponse
from app.database import contact_collection
from datetime import datetime
from typing import List
import uuid

router = APIRouter()


@router.post("/contact", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(contact: ContactCreate):
    """Create a new contact message.
    
    Generates UUID for contact id and ISO 8601 timestamp for created_at.
    Stores the contact message in MongoDB and returns the created contact.
    
    Args:
        contact: ContactCreate model with contact details
        
    Returns:
        ContactResponse with generated id and created_at timestamp
    """
    # Convert Pydantic model to dict
    contact_dict = contact.model_dump()
    
    # Generate UUID for contact id
    contact_dict["id"] = str(uuid.uuid4())
    
    # Generate ISO 8601 timestamp for created_at
    contact_dict["created_at"] = datetime.utcnow().isoformat()
    
    # Insert document into MongoDB contact_messages collection
    await contact_collection.insert_one(contact_dict)
    
    # Remove MongoDB _id from response
    contact_dict.pop("_id", None)
    
    return contact_dict


@router.get("/contact", response_model=List[ContactResponse], status_code=status.HTTP_200_OK)
async def list_contacts():
    """Retrieve all contact messages sorted by created_at descending.
    
    Returns:
        List of ContactResponse objects sorted by created_at (newest first)
    """
    # Retrieve all contacts from MongoDB, sorted by created_at descending
    cursor = contact_collection.find().sort("created_at", -1)
    contacts = await cursor.to_list(length=None)
    
    # Remove MongoDB _id from each contact
    for contact in contacts:
        contact.pop("_id", None)
    
    return contacts
