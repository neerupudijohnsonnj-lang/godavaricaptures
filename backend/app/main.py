"""Main FastAPI application for Godavari Captures API."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import bookings, contact

app = FastAPI(title="Godavari Captures API")

# CORS configuration for public access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for public site
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Health check endpoint
@app.get("/api/")
async def health_check():
    """Health check endpoint to verify API is operational.
    
    Returns:
        dict: Status object with "ok" value
    """
    return {"status": "ok"}

# Include routers with /api prefix
app.include_router(bookings.router, prefix="/api", tags=["bookings"])
app.include_router(contact.router, prefix="/api", tags=["contact"])
