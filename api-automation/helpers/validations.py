"""
Validation utilities for Equipment Status Tracker API tests
"""

import json
from typing import Dict, Any, List
from jsonschema import validate, ValidationError

def validate_equipment_response(response_data: Dict[str, Any]) -> bool:
    """
    Validate equipment response structure
    Args:
        response_data: Response data from API
    Returns:
        True if valid, raises exception if invalid
    """
    expected_schema = {
        "type": "object",
        "properties": {
            "success": {"type": "boolean"},
            "data": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "minimum": 1},
                    "name": {"type": "string", "minLength": 1},
                    "status": {"type": "string", "minLength": 1},
                    "location": {"type": "string", "minLength": 1},
                    "lastUpdated": {
                        "type": "string",
                        "pattern": r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$"
                    }
                },
                "required": ["id", "name", "status", "location", "lastUpdated"]
            }
        },
        "required": ["success", "data"]
    }
    
    try:
        validate(instance=response_data, schema=expected_schema)
        return True
    except ValidationError as e:
        raise AssertionError(f"Response validation failed: {e.message}")

def validate_equipment_list_response(response_data: Dict[str, Any]) -> bool:
    """
    Validate equipment list response structure
    Args:
        response_data: Response data from API containing list of equipment
    Returns:
        True if valid, raises exception if invalid
    """
    expected_schema = {
        "type": "object",
        "properties": {
            "success": {"type": "boolean"},
            "data": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "name": {"type": "string"},
                        "status": {"type": "string"},
                        "location": {"type": "string"},
                        "lastUpdated": {"type": "string"}
                    },
                    "required": ["id", "name", "status", "location", "lastUpdated"]
                }
            }
        },
        "required": ["success", "data"]
    }
    
    try:
        validate(instance=response_data, schema=expected_schema)
        return True
    except ValidationError as e:
        raise AssertionError(f"Equipment list response validation failed: {e.message}")


def validate_get_all_equipment_response(response_data: Dict[str, Any]) -> None:
    """
    Comprehensive validation for GET /api/equipment response
    Args:
        response_data: Response data from GET /api/equipment API
    Raises:
        AssertionError: If validation fails
    """
    # 1. Basic structure validation
    assert "success" in response_data, "Response should contain 'success' field"
    assert "data" in response_data, "Response should contain 'data' field"
    assert "count" in response_data, "Response should contain 'count' field"
    
    # 2. Data type validation
    assert isinstance(response_data["success"], bool), "Success should be boolean"
    assert isinstance(response_data["data"], list), "Data should be a list"
    assert isinstance(response_data["count"], int), "Count should be an integer"
    
    # 3. Business logic validation
    assert response_data["success"] is True, "Success should be true"
    assert response_data["count"] >= 0, "Count should be non-negative"
    
    # 4. Validate each equipment item
    if response_data["data"]:
        for equipment in response_data["data"]:
            # Check required fields exist
            assert "id" in equipment, "Equipment should have ID"
            assert "name" in equipment, "Equipment should have name"
            assert "status" in equipment, "Equipment should have status"
            assert "location" in equipment, "Equipment should have location"
            assert "lastUpdated" in equipment, "Equipment should have lastUpdated"
            
            # Validate data types
            assert isinstance(equipment["id"], int), "Equipment ID should be integer"
            assert isinstance(equipment["name"], str), "Equipment name should be string"
            assert isinstance(equipment["status"], str), "Equipment status should be string"
            assert isinstance(equipment["location"], str), "Equipment location should be string"
            assert isinstance(equipment["lastUpdated"], str), "Equipment lastUpdated should be string"
            
            # Validate business rules
            assert equipment["id"] > 0, "Equipment ID should be positive"
            assert equipment["status"] in ["Active", "Idle", "Under Maintenance"], \
                f"Invalid status: {equipment['status']}"
            
            # Validate lastUpdated format (ISO 8601)
            import re
            iso_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{3})?Z$'
            assert re.match(iso_pattern, equipment["lastUpdated"]), \
                f"lastUpdated should be in ISO 8601 format, got: {equipment['lastUpdated']}"
    
    # 5. Count validation
    if response_data["data"]:
        assert response_data["count"] == len(response_data["data"]), \
            f"Count should match data length. Expected: {len(response_data['data'])}, Got: {response_data['count']}"
    else:
        assert response_data["count"] == 0, "Count should be 0 for empty list"

def assert_equipment_created(created_equipment: Dict[str, Any], original_payload: Dict[str, str]) -> None:
    """
    Assert that equipment was created correctly
    Args:
        created_equipment: Equipment data from API response
        original_payload: Original payload sent to API
    """
    # Check response structure
    assert "success" in created_equipment, "Success field should be present"
    assert "data" in created_equipment, "Data field should be present"
    assert created_equipment["success"] is True, "Success should be True"
    
    equipment_data = created_equipment["data"]
    
    # Check required fields exist
    assert "id" in equipment_data, "Equipment ID should be present"
    assert "lastUpdated" in equipment_data, "Last updated timestamp should be present"
    
    # Check data matches payload exactly
    assert equipment_data["name"] == original_payload["name"], "Equipment name should match input"
    assert equipment_data["status"] == original_payload["status"], "Equipment status should match input"
    assert equipment_data["location"] == original_payload["location"], "Equipment location should match input"
    
    # Check ID format (should be an integer and not null)
    assert isinstance(equipment_data["id"], int), "Equipment ID should be an integer"
    assert equipment_data["id"] is not None, "Equipment ID should not be null"
    assert equipment_data["id"] > 0, "Equipment ID should be positive"
    
    # Check lastUpdated format (ISO 8601 timestamp)
    import re
    timestamp_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$'
    assert re.match(timestamp_pattern, equipment_data["lastUpdated"]), \
        f"lastUpdated should be in ISO 8601 format, got: {equipment_data['lastUpdated']}"

def assert_status_code(response, expected_status: int) -> None:
    """
    Assert response status code
    Args:
        response: API response object
        expected_status: Expected HTTP status code
    """
    assert response.status_code == expected_status, \
        f"Expected status code {expected_status}, got {response.status_code}"

def assert_response_time(response, max_time: float = 5.0) -> None:
    """
    Assert response time is within acceptable limits
    Args:
        response: API response object
        max_time: Maximum acceptable response time in seconds
    """
    response_time = response.elapsed.total_seconds()
    assert response_time < max_time, \
        f"Response time {response_time}s exceeds maximum {max_time}s"

def assert_content_type(response, expected_type: str = "application/json") -> None:
    """
    Assert response content type
    Args:
        response: API response object
        expected_type: Expected content type
    """
    content_type = response.headers.get("content-type", "")
    assert expected_type in content_type, \
        f"Expected content type {expected_type}, got {content_type}"

def validate_error_response(response_data: Dict[str, Any]) -> bool:
    """
    Validate error response structure
    Args:
        response_data: Error response from API
    Returns:
        True if valid error response
    """
    error_schema = {
        "type": "object",
        "properties": {
            "error": {"type": "string"},
            "message": {"type": "string"}
        },
        "required": ["error", "message"]
    }
    
    try:
        validate(instance=response_data, schema=error_schema)
        return True
    except ValidationError as e:
        raise AssertionError(f"Error response validation failed: {e.message}")

def validate_equipment_status_update_response(response_data: Dict[str, Any]) -> None:
    """
    Validate equipment status update response structure
    Args:
        response_data: Response data from status update API
    """
    # Check response structure
    assert "success" in response_data, "Success field should be present"
    assert "data" in response_data, "Data field should be present"
    assert response_data["success"] is True, "Success should be True"
    
    data = response_data["data"]
    
    # Check equipment data
    assert "equipment" in data, "Equipment data should be present"
    equipment = data["equipment"]
    
    # Validate equipment fields
    assert "id" in equipment, "Equipment ID should be present"
    assert "name" in equipment, "Equipment name should be present"
    assert "status" in equipment, "Equipment status should be present"
    assert "location" in equipment, "Equipment location should be present"
    assert "lastUpdated" in equipment, "Equipment lastUpdated should be present"
    
    # Check history entry
    assert "historyEntry" in data, "History entry should be present"
    history = data["historyEntry"]
    
    # Validate history fields
    assert "id" in history, "History ID should be present"
    assert "equipmentId" in history, "Equipment ID in history should be present"
    assert "previousStatus" in history, "Previous status should be present"
    assert "newStatus" in history, "New status should be present"
    assert "timestamp" in history, "Timestamp should be present"
    assert "changedBy" in history, "Changed by should be present"
    
    # Validate data types
    assert isinstance(equipment["id"], int), "Equipment ID should be an integer"
    assert isinstance(history["id"], int), "History ID should be an integer"
    assert isinstance(history["equipmentId"], int), "History equipment ID should be an integer"
    
    # Validate timestamps
    import re
    iso_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{3})?Z$'
    assert re.match(iso_pattern, equipment["lastUpdated"]), \
        f"Equipment lastUpdated should be in ISO 8601 format, got: {equipment['lastUpdated']}"
    assert re.match(iso_pattern, history["timestamp"]), \
        f"History timestamp should be in ISO 8601 format, got: {history['timestamp']}"
    
    # Validate status values
    valid_statuses = ["Active", "Idle", "Under Maintenance"]
    assert equipment["status"] in valid_statuses, f"Equipment status should be one of {valid_statuses}"
    assert history["newStatus"] in valid_statuses, f"New status should be one of {valid_statuses}"
    assert history["previousStatus"] in valid_statuses, f"Previous status should be one of {valid_statuses}"


def validate_equipment_history_response(response_data: Dict[str, Any]) -> None:
    """
    Validate equipment history response structure
    Args:
        response_data: Response data from history API
    """
    # Check response structure
    assert "success" in response_data, "Success field should be present"
    assert "data" in response_data, "Data field should be present"
    assert response_data["success"] is True, "Success should be True"

    data = response_data["data"]

    # Check equipment history data
    assert "equipmentId" in data, "Equipment ID should be present"
    assert "history" in data, "History array should be present"
    assert "total" in data, "Total count should be present"
    assert "limit" in data, "Limit should be present"
    assert "offset" in data, "Offset should be present"
    assert "hasMore" in data, "HasMore flag should be present"

    # Validate data types
    assert isinstance(data["equipmentId"], int), "Equipment ID should be an integer"
    assert isinstance(data["total"], int), "Total should be an integer"
    assert isinstance(data["limit"], int), "Limit should be an integer"
    assert isinstance(data["offset"], int), "Offset should be an integer"
    assert isinstance(data["hasMore"], bool), "HasMore should be a boolean"
    assert isinstance(data["history"], list), "History should be a list"

    # Validate history entries
    for history_entry in data["history"]:
        assert "id" in history_entry, "History entry ID should be present"
        assert "equipmentId" in history_entry, "History entry equipment ID should be present"
        assert "previousStatus" in history_entry, "Previous status should be present"
        assert "newStatus" in history_entry, "New status should be present"
        assert "timestamp" in history_entry, "Timestamp should be present"
        assert "changedBy" in history_entry, "Changed by should be present"

        # Validate data types
        assert isinstance(history_entry["id"], int), "History entry ID should be an integer"
        assert isinstance(history_entry["equipmentId"], int), "History entry equipment ID should be an integer"

        # Validate timestamps
        import re
        iso_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{3})?Z$'
        assert re.match(iso_pattern, history_entry["timestamp"]), \
            f"History entry timestamp should be in ISO 8601 format, got: {history_entry['timestamp']}"

        # Validate status values
        valid_statuses = ["Active", "Idle", "Under Maintenance"]
        assert history_entry["newStatus"] in valid_statuses, f"New status should be one of {valid_statuses}"
        assert history_entry["previousStatus"] in valid_statuses, f"Previous status should be one of {valid_statuses}"
