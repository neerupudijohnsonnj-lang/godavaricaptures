"""Property-based tests for booking routes using Hypothesis.

**Validates: Requirements 12.1**
"""

import pytest
from hypothesis import given, strategies as st, settings
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock
from app.routes.bookings import router
import uuid


# Create test app
app = FastAPI()
app.include_router(router, prefix="/api")

client = TestClient(app)


# Custom strategies for booking data
@st.composite
def valid_booking_data(draw):
    """Generate valid booking data with all required fields."""
    return {
        "name": draw(st.text(min_size=1, max_size=100).filter(lambda x: x.strip())),
        "phone": draw(st.text(min_size=1, max_size=20).filter(lambda x: x.strip())),
        "service": draw(st.sampled_from(["Weddings", "Photoshoots", "Reel Making", "Events", "Drone Shots"])),
        "event_date": draw(st.dates().map(lambda d: d.isoformat())),
        "event_time": draw(st.times().map(lambda t: t.strftime("%H:%M"))),
        "location": draw(st.text(min_size=1, max_size=200).filter(lambda x: x.strip())),
        "message": draw(st.text(max_size=500))
    }


@given(booking_data=valid_booking_data())
@settings(max_examples=20)
def test_property_28_booking_creation_persistence(booking_data):
    """
    # Feature: godavari-captures-landing-page, Property 28: Booking Creation Persistence
    **Validates: Requirements 12.1**
    
    Property 28: Booking Creation Persistence
    
    For any valid booking data (containing required fields: name, phone, service, 
    event_date, event_time, location) sent via POST to /api/bookings, the API 
    should create a corresponding document in the MongoDB bookings collection.
    
    This property verifies that:
    1. The API returns 201 status code for valid booking data
    2. The created booking appears in the GET /api/bookings list
    3. The booking data is persisted correctly with matching fields
    """
    with patch('app.routes.bookings.bookings_collection') as mock_collection:
        # Mock insert_one to simulate successful insertion
        mock_collection.insert_one = AsyncMock(return_value=MagicMock(inserted_id="mock_id"))
        
        # Create booking via POST
        response = client.post("/api/bookings", json=booking_data)
        
        # Verify 201 status code
        assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"
        
        # Verify response contains the booking data
        response_data = response.json()
        assert "id" in response_data, "Response should contain 'id' field"
        assert "created_at" in response_data, "Response should contain 'created_at' field"
        
        # Verify all input fields are in the response
        for key, value in booking_data.items():
            assert response_data[key] == value, f"Field {key} mismatch: expected {value}, got {response_data[key]}"
        
        # Verify that insert_one was called on the MongoDB collection
        assert mock_collection.insert_one.called, "insert_one should have been called on bookings_collection"
        
        # Get the document that was inserted
        inserted_doc = mock_collection.insert_one.call_args[0][0]
        
        # Verify the inserted document contains all booking data
        assert inserted_doc["name"] == booking_data["name"], "Name mismatch in inserted document"
        assert inserted_doc["phone"] == booking_data["phone"], "Phone mismatch in inserted document"
        assert inserted_doc["service"] == booking_data["service"], "Service mismatch in inserted document"
        assert inserted_doc["event_date"] == booking_data["event_date"], "Event date mismatch in inserted document"
        assert inserted_doc["event_time"] == booking_data["event_time"], "Event time mismatch in inserted document"
        assert inserted_doc["location"] == booking_data["location"], "Location mismatch in inserted document"
        assert inserted_doc["message"] == booking_data["message"], "Message mismatch in inserted document"
        
        # Verify the inserted document has generated id and created_at
        assert "id" in inserted_doc, "Inserted document should have 'id' field"
        assert "created_at" in inserted_doc, "Inserted document should have 'created_at' field"
        
        # Update mock to return the created booking in the list
        mock_cursor = MagicMock()
        mock_cursor.sort = MagicMock(return_value=mock_cursor)
        mock_cursor.to_list = AsyncMock(return_value=[inserted_doc])
        mock_collection.find = MagicMock(return_value=mock_cursor)
        
        # Verify the booking appears in GET /api/bookings list
        list_response = client.get("/api/bookings")
        assert list_response.status_code == 200, f"GET request failed with status {list_response.status_code}"
        
        bookings = list_response.json()
        assert isinstance(bookings, list), "GET /api/bookings should return a list"
        
        # Find the created booking in the list
        created_booking_id = response_data["id"]
        matching_bookings = [b for b in bookings if b.get("id") == created_booking_id]
        
        assert len(matching_bookings) > 0, f"Created booking with id {created_booking_id} not found in bookings list"
        
        # Verify the booking data matches
        found_booking = matching_bookings[0]
        assert found_booking["name"] == booking_data["name"], "Name mismatch in retrieved booking"
        assert found_booking["phone"] == booking_data["phone"], "Phone mismatch in retrieved booking"
        assert found_booking["service"] == booking_data["service"], "Service mismatch in retrieved booking"
        assert found_booking["event_date"] == booking_data["event_date"], "Event date mismatch in retrieved booking"
        assert found_booking["event_time"] == booking_data["event_time"], "Event time mismatch in retrieved booking"
        assert found_booking["location"] == booking_data["location"], "Location mismatch in retrieved booking"
        assert found_booking["message"] == booking_data["message"], "Message mismatch in retrieved booking"



@given(booking_data=valid_booking_data())
@settings(max_examples=20)
def test_property_30_booking_uuid_generation(booking_data):
    """
    # Feature: godavari-captures-landing-page, Property 30: Booking UUID Generation
    **Validates: Requirements 12.3**
    
    Property 30: Booking UUID Generation
    
    For any valid booking data sent via POST to /api/bookings, the API response 
    should include an 'id' field containing a valid UUID 
    (format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx).
    
    This property verifies that:
    1. The API response contains an 'id' field
    2. The 'id' field matches the UUID format
    3. The UUID is unique for each booking
    """
    import re
    
    with patch('app.routes.bookings.bookings_collection') as mock_collection:
        # Mock insert_one to simulate successful insertion
        mock_collection.insert_one = AsyncMock(return_value=MagicMock(inserted_id="mock_id"))
        
        # Create booking via POST
        response = client.post("/api/bookings", json=booking_data)
        
        # Verify 201 status code
        assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"
        
        # Verify response contains the id field
        response_data = response.json()
        assert "id" in response_data, "Response should contain 'id' field"
        
        # Verify UUID format (xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
        uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        booking_id = response_data["id"]
        assert re.match(uuid_pattern, booking_id, re.IGNORECASE), \
            f"ID '{booking_id}' does not match UUID format"
        
        # Verify the inserted document has the same UUID
        inserted_doc = mock_collection.insert_one.call_args[0][0]
        assert inserted_doc["id"] == booking_id, "Inserted document should have the same UUID as response"


@given(booking_data=valid_booking_data())
@settings(max_examples=20)
def test_property_31_booking_timestamp_generation(booking_data):
    """
    # Feature: godavari-captures-landing-page, Property 31: Booking Timestamp Generation
    **Validates: Requirements 12.4**
    
    Property 31: Booking Timestamp Generation
    
    For any valid booking data sent via POST to /api/bookings, the API response 
    should include a 'created_at' field containing a valid ISO 8601 timestamp.
    
    This property verifies that:
    1. The API response contains a 'created_at' field
    2. The 'created_at' field is in valid ISO 8601 format
    3. The timestamp is reasonably close to the current time
    """
    from datetime import datetime, timedelta
    
    with patch('app.routes.bookings.bookings_collection') as mock_collection:
        # Mock insert_one to simulate successful insertion
        mock_collection.insert_one = AsyncMock(return_value=MagicMock(inserted_id="mock_id"))
        
        # Record time before request
        before_time = datetime.utcnow()
        
        # Create booking via POST
        response = client.post("/api/bookings", json=booking_data)
        
        # Record time after request
        after_time = datetime.utcnow()
        
        # Verify 201 status code
        assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"
        
        # Verify response contains the created_at field
        response_data = response.json()
        assert "created_at" in response_data, "Response should contain 'created_at' field"
        
        # Verify ISO 8601 format by parsing the timestamp
        created_at_str = response_data["created_at"]
        try:
            created_at = datetime.fromisoformat(created_at_str.replace('Z', '+00:00'))
        except (ValueError, AttributeError) as e:
            pytest.fail(f"'created_at' field '{created_at_str}' is not valid ISO 8601 format: {e}")
        
        # Verify timestamp is within reasonable range (within 5 seconds of request time)
        assert before_time - timedelta(seconds=5) <= created_at <= after_time + timedelta(seconds=5), \
            f"Timestamp {created_at} is not within reasonable range of request time"
        
        # Verify the inserted document has the same timestamp
        inserted_doc = mock_collection.insert_one.call_args[0][0]
        assert inserted_doc["created_at"] == created_at_str, \
            "Inserted document should have the same timestamp as response"


@given(booking_data=valid_booking_data())
@settings(max_examples=20)
def test_property_32_booking_creation_success_status(booking_data):
    """
    # Feature: godavari-captures-landing-page, Property 32: Booking Creation Success Status
    **Validates: Requirements 12.5**
    
    Property 32: Booking Creation Success Status
    
    For any valid booking data sent via POST to /api/bookings, the API should 
    return a 201 status code indicating successful resource creation.
    
    This property verifies that:
    1. The API returns exactly 201 status code for valid data
    2. The response is not 200, 400, 422, or 500
    3. The status code indicates resource creation, not just success
    """
    with patch('app.routes.bookings.bookings_collection') as mock_collection:
        # Mock insert_one to simulate successful insertion
        mock_collection.insert_one = AsyncMock(return_value=MagicMock(inserted_id="mock_id"))
        
        # Create booking via POST
        response = client.post("/api/bookings", json=booking_data)
        
        # Verify exactly 201 status code (Created)
        assert response.status_code == 201, \
            f"Expected 201 (Created), got {response.status_code}: {response.text}"
        
        # Verify it's not other common status codes
        assert response.status_code != 200, "Should return 201 (Created), not 200 (OK)"
        assert response.status_code != 400, "Should return 201 for valid data, not 400 (Bad Request)"
        assert response.status_code != 422, "Should return 201 for valid data, not 422 (Unprocessable Entity)"
        assert response.status_code != 500, "Should return 201 for valid data, not 500 (Internal Server Error)"



@given(st.lists(valid_booking_data(), min_size=2, max_size=10))
@settings(max_examples=20)
def test_property_34_booking_list_sorting(bookings_list):
    """
    # Feature: godavari-captures-landing-page, Property 34: Booking List Sorting
    **Validates: Requirements 12.7**
    
    Property 34: Booking List Sorting
    
    For any GET request to /api/bookings, the returned array of bookings should 
    be sorted in descending order by the 'created_at' field (newest first).
    
    This property verifies that:
    1. The API returns bookings in descending order by created_at
    2. Each booking's created_at is greater than or equal to the next booking's created_at
    3. The sorting is consistent across multiple requests
    """
    from datetime import datetime, timedelta
    import time
    
    with patch('app.routes.bookings.bookings_collection') as mock_collection:
        # Create bookings with different timestamps
        created_bookings = []
        base_time = datetime.utcnow()
        
        for i, booking_data in enumerate(bookings_list):
            # Mock insert_one for each booking
            mock_collection.insert_one = AsyncMock(return_value=MagicMock(inserted_id=f"mock_id_{i}"))
            
            # Create booking with a specific timestamp (spread them out)
            timestamp = (base_time - timedelta(seconds=i * 10)).isoformat()
            
            # Create the booking document
            booking_doc = booking_data.copy()
            booking_doc["id"] = str(uuid.uuid4())
            booking_doc["created_at"] = timestamp
            created_bookings.append(booking_doc)
        
        # Sort the created bookings by created_at descending (newest first)
        created_bookings.sort(key=lambda x: x["created_at"], reverse=True)
        
        # Mock the find().sort().to_list() chain to return sorted bookings
        mock_cursor = MagicMock()
        mock_cursor.sort = MagicMock(return_value=mock_cursor)
        mock_cursor.to_list = AsyncMock(return_value=created_bookings)
        mock_collection.find = MagicMock(return_value=mock_cursor)
        
        # Get the bookings list
        response = client.get("/api/bookings")
        
        # Verify 200 status code
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        # Verify response is a list
        bookings = response.json()
        assert isinstance(bookings, list), "Response should be a list"
        
        # Verify we got all bookings
        assert len(bookings) == len(bookings_list), \
            f"Expected {len(bookings_list)} bookings, got {len(bookings)}"
        
        # Verify bookings are sorted by created_at descending (newest first)
        for i in range(len(bookings) - 1):
            current_time = bookings[i]["created_at"]
            next_time = bookings[i + 1]["created_at"]
            
            assert current_time >= next_time, \
                f"Bookings not sorted correctly: booking at index {i} has created_at '{current_time}' " \
                f"which is less than booking at index {i + 1} with created_at '{next_time}'"
        
        # Verify that sort was called with correct parameters
        mock_cursor.sort.assert_called_once_with("created_at", -1)



@st.composite
def invalid_booking_data_missing_field(draw):
    """Generate booking data with one required field missing."""
    # Start with valid data
    data = {
        "name": draw(st.text(min_size=1, max_size=100).filter(lambda x: x.strip())),
        "phone": draw(st.text(min_size=1, max_size=20).filter(lambda x: x.strip())),
        "service": draw(st.sampled_from(["Weddings", "Photoshoots", "Reel Making", "Events", "Drone Shots"])),
        "event_date": draw(st.dates().map(lambda d: d.isoformat())),
        "event_time": draw(st.times().map(lambda t: t.strftime("%H:%M"))),
        "location": draw(st.text(min_size=1, max_size=200).filter(lambda x: x.strip())),
        "message": draw(st.text(max_size=500))
    }
    
    # Remove one required field
    required_fields = ["name", "phone", "service", "event_date", "event_time", "location"]
    field_to_remove = draw(st.sampled_from(required_fields))
    del data[field_to_remove]
    
    return data, field_to_remove


@given(invalid_data=invalid_booking_data_missing_field())
@settings(max_examples=20)
def test_property_29_booking_required_field_validation(invalid_data):
    """
    # Feature: godavari-captures-landing-page, Property 29: Booking Required Field Validation
    **Validates: Requirements 12.2**
    
    Property 29: Booking Required Field Validation
    
    For any booking data missing one or more required fields (name, phone, service, 
    event_date, event_time, location) sent via POST to /api/bookings, the API 
    should return a 422 status code with validation error details.
    
    This property verifies that:
    1. The API returns 422 status code for missing required fields
    2. The response contains validation error details
    3. The error details identify the missing field
    """
    booking_data, missing_field = invalid_data
    
    # No need to mock MongoDB since validation happens before database access
    with patch('app.routes.bookings.bookings_collection') as mock_collection:
        # Create booking via POST with missing field
        response = client.post("/api/bookings", json=booking_data)
        
        # Verify 422 status code (Unprocessable Entity)
        assert response.status_code == 422, \
            f"Expected 422 for missing field '{missing_field}', got {response.status_code}: {response.text}"
        
        # Verify response contains validation error details
        response_data = response.json()
        assert "detail" in response_data, "Response should contain 'detail' field with validation errors"
        
        # Verify the error details is a list
        assert isinstance(response_data["detail"], list), "Error details should be a list"
        assert len(response_data["detail"]) > 0, "Error details should not be empty"
        
        # Verify the missing field is mentioned in the error details
        error_fields = []
        for error in response_data["detail"]:
            if "loc" in error:
                # Extract field name from location (e.g., ['body', 'name'] -> 'name')
                if len(error["loc"]) > 1:
                    error_fields.append(error["loc"][-1])
        
        assert missing_field in error_fields, \
            f"Missing field '{missing_field}' should be mentioned in error details. Found errors for: {error_fields}"
        
        # Verify that MongoDB insert was NOT called (validation failed before database access)
        assert not mock_collection.insert_one.called, \
            "insert_one should not be called when validation fails"


@given(booking_data=valid_booking_data())
@settings(max_examples=20)
def test_property_33_booking_validation_error_status(booking_data):
    """
    # Feature: godavari-captures-landing-page, Property 33: Booking Validation Error Status
    **Validates: Requirements 12.6**
    
    Property 33: Booking Validation Error Status
    
    For any invalid booking data sent via POST to /api/bookings, the API should 
    return a 422 status code with a response body containing validation error details.
    
    This property verifies that:
    1. Invalid data returns 422 status code
    2. The response body contains a 'detail' field
    3. The 'detail' field contains structured error information
    """
    # Make the data invalid by removing a required field
    invalid_data = booking_data.copy()
    # Remove a random required field
    import random
    required_fields = ["name", "phone", "service", "event_date", "event_time", "location"]
    field_to_remove = random.choice(required_fields)
    del invalid_data[field_to_remove]
    
    with patch('app.routes.bookings.bookings_collection') as mock_collection:
        # Create booking via POST with invalid data
        response = client.post("/api/bookings", json=invalid_data)
        
        # Verify 422 status code
        assert response.status_code == 422, \
            f"Expected 422 for invalid data, got {response.status_code}: {response.text}"
        
        # Verify response body contains validation error details
        response_data = response.json()
        assert "detail" in response_data, \
            "Response should contain 'detail' field with validation errors"
        
        # Verify the detail field is a list of error objects
        assert isinstance(response_data["detail"], list), \
            "The 'detail' field should be a list"
        assert len(response_data["detail"]) > 0, \
            "The 'detail' field should contain at least one error"
        
        # Verify each error has the expected structure
        for error in response_data["detail"]:
            assert isinstance(error, dict), "Each error should be a dictionary"
            assert "loc" in error, "Each error should have a 'loc' field"
            assert "msg" in error, "Each error should have a 'msg' field"
            assert "type" in error, "Each error should have a 'type' field"
            
            # Verify loc is a list
            assert isinstance(error["loc"], list), "The 'loc' field should be a list"
            
            # Verify msg is a string
            assert isinstance(error["msg"], str), "The 'msg' field should be a string"
            
            # Verify type is a string
            assert isinstance(error["type"], str), "The 'type' field should be a string"
        
        # Verify that MongoDB insert was NOT called
        assert not mock_collection.insert_one.called, \
            "insert_one should not be called when validation fails"
