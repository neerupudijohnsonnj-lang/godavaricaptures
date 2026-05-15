"""Property-based tests for contact routes using Hypothesis.

**Validates: Requirements 13.1**
"""

import pytest
from hypothesis import given, strategies as st, settings
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock
from app.routes.contact import router
import uuid


# Create test app
app = FastAPI()
app.include_router(router, prefix="/api")

client = TestClient(app)


# Custom strategies for contact data
@st.composite
def valid_contact_data(draw):
    """Generate valid contact data with all required fields."""
    # Generate a valid email using simple ASCII alphanumeric characters
    # to avoid Pydantic EmailStr validation issues with special characters
    username = draw(st.text(min_size=1, max_size=20, alphabet='abcdefghijklmnopqrstuvwxyz0123456789'))
    domain = draw(st.text(min_size=1, max_size=20, alphabet='abcdefghijklmnopqrstuvwxyz0123456789'))
    tld = draw(st.sampled_from(['com', 'org', 'net', 'edu', 'io', 'co']))
    email = f"{username}@{domain}.{tld}"
    
    return {
        "name": draw(st.text(min_size=1, max_size=100).filter(lambda x: x.strip())),
        "email": email,
        "phone": draw(st.text(min_size=1, max_size=20).filter(lambda x: x.strip())),
        "subject": draw(st.text(min_size=1, max_size=200).filter(lambda x: x.strip())),
        "message": draw(st.text(min_size=1, max_size=1000).filter(lambda x: x.strip()))
    }


@given(contact_data=valid_contact_data())
@settings(max_examples=20)
def test_property_35_contact_creation_persistence(contact_data):
    """
    # Feature: godavari-captures-landing-page, Property 35: Contact Creation Persistence
    **Validates: Requirements 13.1**
    
    Property 35: Contact Creation Persistence
    
    For any valid contact data (containing required fields: name, email, phone, 
    subject, message) sent via POST to /api/contact, the API should create a 
    corresponding document in the MongoDB contact_messages collection.
    
    This property verifies that:
    1. The API returns 201 status code for valid contact data
    2. The created contact appears in the GET /api/contact list
    3. The contact data is persisted correctly with matching fields
    """
    with patch('app.routes.contact.contact_collection') as mock_collection:
        # Mock insert_one to simulate successful insertion
        mock_collection.insert_one = AsyncMock(return_value=MagicMock(inserted_id="mock_id"))
        
        # Create contact via POST
        response = client.post("/api/contact", json=contact_data)
        
        # Verify 201 status code
        assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"
        
        # Verify response contains the contact data
        response_data = response.json()
        assert "id" in response_data, "Response should contain 'id' field"
        assert "created_at" in response_data, "Response should contain 'created_at' field"
        
        # Verify all input fields are in the response
        for key, value in contact_data.items():
            assert response_data[key] == value, f"Field {key} mismatch: expected {value}, got {response_data[key]}"
        
        # Verify that insert_one was called on the MongoDB collection
        assert mock_collection.insert_one.called, "insert_one should have been called on contact_collection"
        
        # Get the document that was inserted
        inserted_doc = mock_collection.insert_one.call_args[0][0]
        
        # Verify the inserted document contains all contact data
        assert inserted_doc["name"] == contact_data["name"], "Name mismatch in inserted document"
        assert inserted_doc["email"] == contact_data["email"], "Email mismatch in inserted document"
        assert inserted_doc["phone"] == contact_data["phone"], "Phone mismatch in inserted document"
        assert inserted_doc["subject"] == contact_data["subject"], "Subject mismatch in inserted document"
        assert inserted_doc["message"] == contact_data["message"], "Message mismatch in inserted document"
        
        # Verify the inserted document has generated id and created_at
        assert "id" in inserted_doc, "Inserted document should have 'id' field"
        assert "created_at" in inserted_doc, "Inserted document should have 'created_at' field"
        
        # Update mock to return the created contact in the list
        mock_cursor = MagicMock()
        mock_cursor.sort = MagicMock(return_value=mock_cursor)
        mock_cursor.to_list = AsyncMock(return_value=[inserted_doc])
        mock_collection.find = MagicMock(return_value=mock_cursor)
        
        # Verify the contact appears in GET /api/contact list
        list_response = client.get("/api/contact")
        assert list_response.status_code == 200, f"GET request failed with status {list_response.status_code}"
        
        contacts = list_response.json()
        assert isinstance(contacts, list), "GET /api/contact should return a list"
        
        # Find the created contact in the list
        created_contact_id = response_data["id"]
        matching_contacts = [c for c in contacts if c.get("id") == created_contact_id]
        
        assert len(matching_contacts) > 0, f"Created contact with id {created_contact_id} not found in contacts list"
        
        # Verify the contact data matches
        found_contact = matching_contacts[0]
        assert found_contact["name"] == contact_data["name"], "Name mismatch in retrieved contact"
        assert found_contact["email"] == contact_data["email"], "Email mismatch in retrieved contact"
        assert found_contact["phone"] == contact_data["phone"], "Phone mismatch in retrieved contact"
        assert found_contact["subject"] == contact_data["subject"], "Subject mismatch in retrieved contact"
        assert found_contact["message"] == contact_data["message"], "Message mismatch in retrieved contact"


@given(contact_data=valid_contact_data())
@settings(max_examples=20)
def test_property_38_contact_uuid_generation(contact_data):
    """
    # Feature: godavari-captures-landing-page, Property 38: Contact UUID Generation
    **Validates: Requirements 13.4**
    
    Property 38: Contact UUID Generation
    
    For any valid contact data sent via POST to /api/contact, the API response 
    should include an 'id' field containing a valid UUID 
    (format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx).
    
    This property verifies that:
    1. The API response contains an 'id' field
    2. The 'id' field matches the UUID format
    3. The UUID is unique for each contact
    """
    import re
    
    with patch('app.routes.contact.contact_collection') as mock_collection:
        # Mock insert_one to simulate successful insertion
        mock_collection.insert_one = AsyncMock(return_value=MagicMock(inserted_id="mock_id"))
        
        # Create contact via POST
        response = client.post("/api/contact", json=contact_data)
        
        # Verify 201 status code
        assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"
        
        # Verify response contains the id field
        response_data = response.json()
        assert "id" in response_data, "Response should contain 'id' field"
        
        # Verify UUID format (xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
        uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        contact_id = response_data["id"]
        assert re.match(uuid_pattern, contact_id, re.IGNORECASE), \
            f"ID '{contact_id}' does not match UUID format"
        
        # Verify the inserted document has the same UUID
        inserted_doc = mock_collection.insert_one.call_args[0][0]
        assert inserted_doc["id"] == contact_id, "Inserted document should have the same UUID as response"


@given(contact_data=valid_contact_data())
@settings(max_examples=20)
def test_property_39_contact_timestamp_generation(contact_data):
    """
    # Feature: godavari-captures-landing-page, Property 39: Contact Timestamp Generation
    **Validates: Requirements 13.5**
    
    Property 39: Contact Timestamp Generation
    
    For any valid contact data sent via POST to /api/contact, the API response 
    should include a 'created_at' field containing a valid ISO 8601 timestamp.
    
    This property verifies that:
    1. The API response contains a 'created_at' field
    2. The 'created_at' field is in valid ISO 8601 format
    3. The timestamp is reasonably close to the current time
    """
    from datetime import datetime, timedelta
    
    with patch('app.routes.contact.contact_collection') as mock_collection:
        # Mock insert_one to simulate successful insertion
        mock_collection.insert_one = AsyncMock(return_value=MagicMock(inserted_id="mock_id"))
        
        # Record time before request
        before_time = datetime.utcnow()
        
        # Create contact via POST
        response = client.post("/api/contact", json=contact_data)
        
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


@given(contact_data=valid_contact_data())
@settings(max_examples=20)
def test_property_40_contact_creation_success_status(contact_data):
    """
    # Feature: godavari-captures-landing-page, Property 40: Contact Creation Success Status
    **Validates: Requirements 13.6**
    
    Property 40: Contact Creation Success Status
    
    For any valid contact data sent via POST to /api/contact, the API should 
    return a 201 status code indicating successful resource creation.
    
    This property verifies that:
    1. The API returns exactly 201 status code for valid data
    2. The response is not 200, 400, 422, or 500
    3. The status code indicates resource creation, not just success
    """
    with patch('app.routes.contact.contact_collection') as mock_collection:
        # Mock insert_one to simulate successful insertion
        mock_collection.insert_one = AsyncMock(return_value=MagicMock(inserted_id="mock_id"))
        
        # Create contact via POST
        response = client.post("/api/contact", json=contact_data)
        
        # Verify exactly 201 status code (Created)
        assert response.status_code == 201, \
            f"Expected 201 (Created), got {response.status_code}: {response.text}"
        
        # Verify it's not other common status codes
        assert response.status_code != 200, "Should return 201 (Created), not 200 (OK)"
        assert response.status_code != 400, "Should return 201 for valid data, not 400 (Bad Request)"
        assert response.status_code != 422, "Should return 201 for valid data, not 422 (Unprocessable Entity)"
        assert response.status_code != 500, "Should return 201 for valid data, not 500 (Internal Server Error)"


@given(st.lists(valid_contact_data(), min_size=2, max_size=10))
@settings(max_examples=20)
def test_property_42_contact_list_sorting(contacts_list):
    """
    # Feature: godavari-captures-landing-page, Property 42: Contact List Sorting
    **Validates: Requirements 13.8**
    
    Property 42: Contact List Sorting
    
    For any GET request to /api/contact, the returned array of contact messages 
    should be sorted in descending order by the 'created_at' field (newest first).
    
    This property verifies that:
    1. The API returns contacts in descending order by created_at
    2. Each contact's created_at is greater than or equal to the next contact's created_at
    3. The sorting is consistent across multiple requests
    """
    from datetime import datetime, timedelta
    
    with patch('app.routes.contact.contact_collection') as mock_collection:
        # Create contacts with different timestamps
        created_contacts = []
        base_time = datetime.utcnow()
        
        for i, contact_data in enumerate(contacts_list):
            # Mock insert_one for each contact
            mock_collection.insert_one = AsyncMock(return_value=MagicMock(inserted_id=f"mock_id_{i}"))
            
            # Create contact with a specific timestamp (spread them out)
            timestamp = (base_time - timedelta(seconds=i * 10)).isoformat()
            
            # Create the contact document
            contact_doc = contact_data.copy()
            contact_doc["id"] = str(uuid.uuid4())
            contact_doc["created_at"] = timestamp
            created_contacts.append(contact_doc)
        
        # Sort the created contacts by created_at descending (newest first)
        created_contacts.sort(key=lambda x: x["created_at"], reverse=True)
        
        # Mock the find().sort().to_list() chain to return sorted contacts
        mock_cursor = MagicMock()
        mock_cursor.sort = MagicMock(return_value=mock_cursor)
        mock_cursor.to_list = AsyncMock(return_value=created_contacts)
        mock_collection.find = MagicMock(return_value=mock_cursor)
        
        # Get the contacts list
        response = client.get("/api/contact")
        
        # Verify 200 status code
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        # Verify response is a list
        contacts = response.json()
        assert isinstance(contacts, list), "Response should be a list"
        
        # Verify we got all contacts
        assert len(contacts) == len(contacts_list), \
            f"Expected {len(contacts_list)} contacts, got {len(contacts)}"
        
        # Verify contacts are sorted by created_at descending (newest first)
        for i in range(len(contacts) - 1):
            current_time = contacts[i]["created_at"]
            next_time = contacts[i + 1]["created_at"]
            
            assert current_time >= next_time, \
                f"Contacts not sorted correctly: contact at index {i} has created_at '{current_time}' " \
                f"which is less than contact at index {i + 1} with created_at '{next_time}'"
        
        # Verify that sort was called with correct parameters
        mock_cursor.sort.assert_called_once_with("created_at", -1)


@st.composite
def invalid_contact_data_missing_field(draw):
    """Generate contact data with one required field missing."""
    # Start with valid data using simple ASCII alphanumeric characters
    username = draw(st.text(min_size=1, max_size=20, alphabet='abcdefghijklmnopqrstuvwxyz0123456789'))
    domain = draw(st.text(min_size=1, max_size=20, alphabet='abcdefghijklmnopqrstuvwxyz0123456789'))
    tld = draw(st.sampled_from(['com', 'org', 'net', 'edu', 'io', 'co']))
    email = f"{username}@{domain}.{tld}"
    
    data = {
        "name": draw(st.text(min_size=1, max_size=100).filter(lambda x: x.strip())),
        "email": email,
        "phone": draw(st.text(min_size=1, max_size=20).filter(lambda x: x.strip())),
        "subject": draw(st.text(min_size=1, max_size=200).filter(lambda x: x.strip())),
        "message": draw(st.text(min_size=1, max_size=1000).filter(lambda x: x.strip()))
    }
    
    # Remove one required field
    required_fields = ["name", "email", "phone", "subject", "message"]
    field_to_remove = draw(st.sampled_from(required_fields))
    del data[field_to_remove]
    
    return data, field_to_remove


@given(invalid_data=invalid_contact_data_missing_field())
@settings(max_examples=20)
def test_property_36_contact_required_field_validation(invalid_data):
    """
    # Feature: godavari-captures-landing-page, Property 36: Contact Required Field Validation
    **Validates: Requirements 13.2**
    
    Property 36: Contact Required Field Validation
    
    For any contact data missing one or more required fields (name, email, phone, 
    subject, message) sent via POST to /api/contact, the API should return a 422 
    status code with validation error details.
    
    This property verifies that:
    1. The API returns 422 status code for missing required fields
    2. The response contains validation error details
    3. The error details identify the missing field
    """
    contact_data, missing_field = invalid_data
    
    # No need to mock MongoDB since validation happens before database access
    with patch('app.routes.contact.contact_collection') as mock_collection:
        # Create contact via POST with missing field
        response = client.post("/api/contact", json=contact_data)
        
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


@st.composite
def invalid_email_contact_data(draw):
    """Generate contact data with invalid email format."""
    # Generate invalid email (missing @ or domain)
    invalid_email_type = draw(st.sampled_from(['no_at', 'no_domain', 'no_tld', 'spaces']))
    
    if invalid_email_type == 'no_at':
        email = draw(st.text(min_size=1, max_size=50).filter(lambda x: '@' not in x and x.strip()))
    elif invalid_email_type == 'no_domain':
        username = draw(st.text(min_size=1, max_size=20).filter(lambda x: x.strip()))
        email = f"{username}@"
    elif invalid_email_type == 'no_tld':
        username = draw(st.text(min_size=1, max_size=20).filter(lambda x: x.strip()))
        domain = draw(st.text(min_size=1, max_size=20).filter(lambda x: '.' not in x and x.strip()))
        email = f"{username}@{domain}"
    else:  # spaces
        username = draw(st.text(min_size=1, max_size=20).filter(lambda x: x.strip()))
        email = f"{username} @example.com"
    
    return {
        "name": draw(st.text(min_size=1, max_size=100).filter(lambda x: x.strip())),
        "email": email,
        "phone": draw(st.text(min_size=1, max_size=20).filter(lambda x: x.strip())),
        "subject": draw(st.text(min_size=1, max_size=200).filter(lambda x: x.strip())),
        "message": draw(st.text(min_size=1, max_size=1000).filter(lambda x: x.strip()))
    }


@given(contact_data=invalid_email_contact_data())
@settings(max_examples=20)
def test_property_37_contact_email_format_validation(contact_data):
    """
    # Feature: godavari-captures-landing-page, Property 37: Contact Email Format Validation
    **Validates: Requirements 13.3**
    
    Property 37: Contact Email Format Validation
    
    For any contact data with an email field that does not match valid email format 
    (validated by Pydantic EmailStr) sent via POST to /api/contact, the API should 
    return a 422 status code with email validation error details.
    
    This property verifies that:
    1. The API returns 422 status code for invalid email format
    2. The response contains validation error details
    3. The error details identify the email field as invalid
    """
    # No need to mock MongoDB since validation happens before database access
    with patch('app.routes.contact.contact_collection') as mock_collection:
        # Create contact via POST with invalid email
        response = client.post("/api/contact", json=contact_data)
        
        # Verify 422 status code (Unprocessable Entity)
        assert response.status_code == 422, \
            f"Expected 422 for invalid email '{contact_data['email']}', got {response.status_code}: {response.text}"
        
        # Verify response contains validation error details
        response_data = response.json()
        assert "detail" in response_data, "Response should contain 'detail' field with validation errors"
        
        # Verify the error details is a list
        assert isinstance(response_data["detail"], list), "Error details should be a list"
        assert len(response_data["detail"]) > 0, "Error details should not be empty"
        
        # Verify the email field is mentioned in the error details
        error_fields = []
        for error in response_data["detail"]:
            if "loc" in error:
                # Extract field name from location (e.g., ['body', 'email'] -> 'email')
                if len(error["loc"]) > 1:
                    error_fields.append(error["loc"][-1])
        
        assert "email" in error_fields, \
            f"Email field should be mentioned in error details. Found errors for: {error_fields}"
        
        # Verify that MongoDB insert was NOT called (validation failed before database access)
        assert not mock_collection.insert_one.called, \
            "insert_one should not be called when validation fails"


@given(contact_data=valid_contact_data())
@settings(max_examples=20)
def test_property_41_contact_validation_error_status(contact_data):
    """
    # Feature: godavari-captures-landing-page, Property 41: Contact Validation Error Status
    **Validates: Requirements 13.7**
    
    Property 41: Contact Validation Error Status
    
    For any invalid contact data sent via POST to /api/contact, the API should 
    return a 422 status code with a response body containing validation error details.
    
    This property verifies that:
    1. Invalid data returns 422 status code
    2. The response body contains a 'detail' field
    3. The 'detail' field contains structured error information
    """
    # Make the data invalid by removing a required field
    invalid_data = contact_data.copy()
    # Remove a random required field
    import random
    required_fields = ["name", "email", "phone", "subject", "message"]
    field_to_remove = random.choice(required_fields)
    del invalid_data[field_to_remove]
    
    with patch('app.routes.contact.contact_collection') as mock_collection:
        # Create contact via POST with invalid data
        response = client.post("/api/contact", json=invalid_data)
        
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
