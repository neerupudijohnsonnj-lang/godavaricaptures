"""Property-based tests for general API behavior."""

from hypothesis import given, strategies as st, settings
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch
from app.main import app

client = TestClient(app)


@settings(max_examples=100)
@given(
    name=st.text(min_size=1, max_size=100),
    phone=st.text(min_size=1, max_size=20),
    service=st.sampled_from(["Weddings", "Photoshoots", "Reel Making", "Events", "Drone Shots"]),
    event_date=st.dates().map(lambda d: d.isoformat()),
    event_time=st.times().map(lambda t: t.strftime("%H:%M")),
    location=st.text(min_size=1, max_size=200),
    message=st.text(max_size=500)
)
def test_property_43_mongodb_id_exclusion_bookings(name, phone, service, event_date, event_time, location, message):
    """
    **Validates: Requirements 12.8**
    
    Feature: godavari-captures-landing-page, Property 43: MongoDB ID Exclusion from API Responses
    
    For any document returned by GET /api/bookings, the response object should not contain 
    a '_id' field (MongoDB's internal identifier should be excluded).
    """
    with patch('app.routes.bookings.bookings_collection') as mock_collection:
        # Mock insert_one to simulate successful insertion
        mock_collection.insert_one = AsyncMock(return_value=MagicMock(inserted_id="mock_id"))
        
        # Create a booking first
        booking_data = {
            "name": name,
            "phone": phone,
            "service": service,
            "event_date": event_date,
            "event_time": event_time,
            "location": location,
            "message": message
        }
        
        create_response = client.post("/api/bookings", json=booking_data)
        
        # Only test if creation was successful
        if create_response.status_code == 201:
            # Verify the created booking doesn't have _id
            created_booking = create_response.json()
            assert "_id" not in created_booking, "Created booking response should not contain '_id' field"
            
            # Mock the find().sort().to_list() chain to return bookings with _id in MongoDB
            # but verify they are excluded from the API response
            mock_booking_with_id = created_booking.copy()
            mock_booking_with_id["_id"] = "mongodb_object_id_12345"  # Simulate MongoDB _id
            
            mock_cursor = MagicMock()
            mock_cursor.sort = MagicMock(return_value=mock_cursor)
            mock_cursor.to_list = AsyncMock(return_value=[mock_booking_with_id])
            mock_collection.find = MagicMock(return_value=mock_cursor)
            
            # Verify GET /api/bookings doesn't return _id
            list_response = client.get("/api/bookings")
            assert list_response.status_code == 200
            bookings = list_response.json()
            
            for booking in bookings:
                assert "_id" not in booking, f"Booking in list should not contain '_id' field: {booking}"


@settings(max_examples=100)
@given(
    name=st.text(min_size=1, max_size=100),
    email=st.emails(),
    phone=st.text(min_size=1, max_size=20),
    subject=st.text(min_size=1, max_size=200),
    message=st.text(min_size=1, max_size=1000)
)
def test_property_43_mongodb_id_exclusion_contacts(name, email, phone, subject, message):
    """
    **Validates: Requirements 13.9**
    
    Feature: godavari-captures-landing-page, Property 43: MongoDB ID Exclusion from API Responses
    
    For any document returned by GET /api/contact, the response object should not contain 
    a '_id' field (MongoDB's internal identifier should be excluded).
    """
    with patch('app.routes.contact.contact_collection') as mock_collection:
        # Mock insert_one to simulate successful insertion
        mock_collection.insert_one = AsyncMock(return_value=MagicMock(inserted_id="mock_id"))
        
        # Create a contact message first
        contact_data = {
            "name": name,
            "email": email,
            "phone": phone,
            "subject": subject,
            "message": message
        }
        
        create_response = client.post("/api/contact", json=contact_data)
        
        # Only test if creation was successful
        if create_response.status_code == 201:
            # Verify the created contact doesn't have _id
            created_contact = create_response.json()
            assert "_id" not in created_contact, "Created contact response should not contain '_id' field"
            
            # Mock the find().sort().to_list() chain to return contacts with _id in MongoDB
            # but verify they are excluded from the API response
            mock_contact_with_id = created_contact.copy()
            mock_contact_with_id["_id"] = "mongodb_object_id_67890"  # Simulate MongoDB _id
            
            mock_cursor = MagicMock()
            mock_cursor.sort = MagicMock(return_value=mock_cursor)
            mock_cursor.to_list = AsyncMock(return_value=[mock_contact_with_id])
            mock_collection.find = MagicMock(return_value=mock_cursor)
            
            # Verify GET /api/contact doesn't return _id
            list_response = client.get("/api/contact")
            assert list_response.status_code == 200
            contacts = list_response.json()
            
            for contact in contacts:
                assert "_id" not in contact, f"Contact in list should not contain '_id' field: {contact}"
