"""Pydantic models for contact requests and responses."""

from pydantic import BaseModel, EmailStr, Field


class ContactCreate(BaseModel):
    """Request model for creating a new contact message.
    
    All fields are required with minimum length validation.
    Email field uses EmailStr for format validation.
    """
    name: str = Field(..., min_length=1)
    email: EmailStr
    phone: str = Field(..., min_length=1)
    subject: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1)


class ContactResponse(BaseModel):
    """Response model for contact message data.
    
    Includes all contact fields plus generated id and created_at timestamp.
    """
    id: str
    name: str
    email: str
    phone: str
    subject: str
    message: str
    created_at: str
