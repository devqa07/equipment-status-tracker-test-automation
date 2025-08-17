"""
Add Equipment API Test
Tests the POST /api/equipment endpoint
"""

import pytest
import json
import allure
from api_client.equipment_api import EquipmentAPIClient
from helpers.test_data import create_equipment_payload, load_test_data
from helpers.validations import (
    validate_equipment_response,
    assert_equipment_created,
    assert_status_code,
    assert_response_time,
    assert_content_type
)
from helpers.constants import (
    STATUS_CREATED,
    STATUS_BAD_REQUEST,
    STATUS_NOT_FOUND,
    STATUS_INTERNAL_SERVER_ERROR,
    MAX_RESPONSE_TIME,
    CONTENT_TYPE_JSON,
    ADD_EQUIPMENT_ENDPOINT,
    EQUIPMENT_STATUS_ACTIVE,
    INVALID_STATUS,
    INVALID_ENDPOINT_SUFFIX
)
from tests.base_test import BaseAPITest


class TestAddEquipment(BaseAPITest):
    """Test cases for adding new equipment"""
    
    @pytest.mark.smoke
    @pytest.mark.add_equipment
    def test_add_equipment_with_active_status(self, api_client: EquipmentAPIClient):
        """Add equipment with Active status"""
        # Arrange - Get status from test data and create valid test data
        test_data = load_test_data()
        active_status = test_data["status_options"][0]  # "Active"
        equipment_data = create_equipment_payload(status=active_status)
        
        url = f"{api_client.base_url}{ADD_EQUIPMENT_ENDPOINT}"
        self._log_request("POST", url, dict(api_client.session.headers), equipment_data)
        
        with allure.step("Send POST request to add equipment with Active status"):
            response, response_data = api_client.add_equipment_with_response(equipment_data)
            self._log_response(response, response_data)
        
        with allure.step("Validate response structure and data"):
            # 1. Check HTTP status code
            assert_status_code(response, STATUS_CREATED)
            
            # 2. Check response time (Performance validation)
            assert_response_time(response, MAX_RESPONSE_TIME)
            
            # 3. Check content type
            assert_content_type(response, CONTENT_TYPE_JSON)
            
            # 4. Validate response structure (Data integrity)
            validate_equipment_response(response_data)
            
            # 5. Verify equipment was created correctly
            assert_equipment_created(response_data, equipment_data)
            
            # 6. Verify status is Active
            assert response_data["data"]["status"] == active_status, f"Expected status '{active_status}', got '{response_data['data']['status']}'"
    
    @pytest.mark.regression
    @pytest.mark.add_equipment
    def test_add_equipment_with_idle_status(self, api_client: EquipmentAPIClient):
        """Add equipment with Idle status"""
        # Arrange - Get status from test data and create valid test data
        test_data = load_test_data()
        idle_status = test_data["status_options"][1]  # "Idle"
        equipment_data = create_equipment_payload(status=idle_status)
        
        url = f"{api_client.base_url}{ADD_EQUIPMENT_ENDPOINT}"
        self._log_request("POST", url, dict(api_client.session.headers), equipment_data)
        
        with allure.step("Send POST request to add equipment with Idle status"):
            response, response_data = api_client.add_equipment_with_response(equipment_data)
            self._log_response(response, response_data)
        
        with allure.step("Validate response structure and data"):
            # 1. Check HTTP status code
            assert_status_code(response, STATUS_CREATED)
            
            # 2. Check response time (Performance validation)
            assert_response_time(response, MAX_RESPONSE_TIME)
            
            # 3. Check content type
            assert_content_type(response, CONTENT_TYPE_JSON)
            
            # 4. Validate response structure (Data integrity)
            validate_equipment_response(response_data)
            
            # 5. Verify equipment was created correctly
            assert_equipment_created(response_data, equipment_data)
            
            # 6. Verify status is Idle
            assert response_data["data"]["status"] == idle_status, f"Expected status '{idle_status}', got '{response_data['data']['status']}'"
    
    @pytest.mark.regression
    @pytest.mark.add_equipment
    def test_add_equipment_with_maintenance_status(self, api_client: EquipmentAPIClient):
        """Add equipment with Under Maintenance status"""
        # Arrange - Get status from test data and create valid test data
        test_data = load_test_data()
        maintenance_status = test_data["status_options"][2]  # "Under Maintenance"
        equipment_data = create_equipment_payload(status=maintenance_status)
        
        # Print request details
        print(f"\n=== REQUEST (Under Maintenance Status) ===")
        print(f"URL: POST {api_client.base_url}{ADD_EQUIPMENT_ENDPOINT}")
        print(f"Payload: {json.dumps(equipment_data, indent=2)}")
        
        # Act - Send API request
        response, response_data = api_client.add_equipment_with_response(equipment_data)
        
        # Print response details
        print(f"\n=== RESPONSE ===")
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {json.dumps(response_data, indent=2)}")
        
        # Assert - Validate response
        # 1. Check HTTP status code
        assert_status_code(response, STATUS_CREATED)
        
        # 2. Check response time (Performance validation)
        assert_response_time(response, MAX_RESPONSE_TIME)
        
        # 3. Check content type
        assert_content_type(response, CONTENT_TYPE_JSON)
        
        # 4. Validate response structure (Data integrity)
        validate_equipment_response(response_data)
        
        # 5. Verify equipment was created correctly
        assert_equipment_created(response_data, equipment_data)
        
        # 6. Verify status is Under Maintenance
        assert response_data["data"]["status"] == maintenance_status, f"Expected status '{maintenance_status}', got '{response_data['data']['status']}'"
    
    @pytest.mark.regression
    @pytest.mark.add_equipment
    def test_add_equipment_missing_name(self, api_client: EquipmentAPIClient):
        """Missing required field (name)"""
        # Arrange - Get status from test data and create payload without name
        test_data = load_test_data()
        valid_status = test_data["status_options"][0]  # "Active"
        invalid_data = {
            "status": valid_status,
            "location": "Test Location"
        }
        
        url = f"{api_client.base_url}{ADD_EQUIPMENT_ENDPOINT}"
        self._log_request("POST", url, dict(api_client.session.headers), invalid_data)
        
        with allure.step("Send POST request with missing name field"):
            response = api_client._make_request("POST", ADD_EQUIPMENT_ENDPOINT, data=invalid_data)
            self._log_response(response)
        
        with allure.step("Validate error response"):
            assert_status_code(response, STATUS_BAD_REQUEST)
    
    @pytest.mark.regression
    @pytest.mark.add_equipment
    def test_add_equipment_missing_status(self, api_client: EquipmentAPIClient):
        """Missing required field (status)"""
        # Arrange - Create payload without status
        invalid_data = {
            "name": "Test Equipment",
            "location": "Test Location"
        }
        
        print(f"\n=== REQUEST (Missing Status) ===")
        print(f"Payload: {json.dumps(invalid_data, indent=2)}")
        
        # Act - Send invalid request
        response = api_client._make_request("POST", ADD_EQUIPMENT_ENDPOINT, data=invalid_data)
        
        print(f"\n=== RESPONSE ===")
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
        
        # Assert - Should return 400 Bad Request
        assert_status_code(response, STATUS_BAD_REQUEST)
    
    @pytest.mark.regression
    @pytest.mark.add_equipment
    def test_add_equipment_missing_location(self, api_client: EquipmentAPIClient):
        """Missing required field (location)"""
        # Arrange - Get status from test data and create payload without location
        test_data = load_test_data()
        valid_status = test_data["status_options"][0]  # "Active"
        invalid_data = {
            "name": "Test Equipment",
            "status": valid_status
        }
        
        print(f"\n=== REQUEST (Missing Location) ===")
        print(f"Payload: {json.dumps(invalid_data, indent=2)}")
        
        # Act - Send invalid request
        response = api_client._make_request("POST", ADD_EQUIPMENT_ENDPOINT, data=invalid_data)
        
        print(f"\n=== RESPONSE ===")
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
        
        # Assert - Should return 400 Bad Request
        assert_status_code(response, STATUS_BAD_REQUEST)
    
    @pytest.mark.regression
    @pytest.mark.add_equipment
    def test_add_equipment_invalid_status(self, api_client: EquipmentAPIClient):
        """Invalid status value"""
        # Arrange - Create payload with invalid status
        invalid_data = {
            "name": "Test Equipment",
            "status": INVALID_STATUS,
            "location": "Test Location"
        }
        
        print(f"\n=== REQUEST (Invalid Status) ===")
        print(f"Payload: {json.dumps(invalid_data, indent=2)}")
        
        # Act - Send invalid request
        response = api_client._make_request("POST", ADD_EQUIPMENT_ENDPOINT, data=invalid_data)
        
        print(f"\n=== RESPONSE ===")
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
        
        # Assert - Should return 400 Bad Request
        assert_status_code(response, STATUS_BAD_REQUEST)
    
    @pytest.mark.regression
    @pytest.mark.add_equipment
    def test_add_equipment_empty_payload(self, api_client: EquipmentAPIClient):
        """Empty request payload"""
        # Arrange - Empty payload
        empty_data = {}
        
        print(f"\n=== REQUEST (Empty Payload) ===")
        print(f"Payload: {json.dumps(empty_data, indent=2)}")
        
        # Act - Send empty request
        response = api_client._make_request("POST", ADD_EQUIPMENT_ENDPOINT, data=empty_data)
        
        print(f"\n=== RESPONSE ===")
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
        
        # Assert - Should return 400 Bad Request
        assert_status_code(response, STATUS_BAD_REQUEST)
    
    @pytest.mark.regression
    @pytest.mark.add_equipment
    def test_add_equipment_wrong_http_method(self, api_client: EquipmentAPIClient):
        """Wrong HTTP method (PUT instead of POST)"""
        # Arrange - Valid data but wrong method
        valid_data = create_equipment_payload()
        
        print(f"\n=== REQUEST (Wrong Method - PUT) ===")
        print(f"Method: PUT {api_client.base_url}{ADD_EQUIPMENT_ENDPOINT}")
        print(f"Payload: {json.dumps(valid_data, indent=2)}")
        
        # Act - Send PUT request instead of POST
        response = api_client._make_request("PUT", ADD_EQUIPMENT_ENDPOINT, data=valid_data)
        
        print(f"\n=== RESPONSE ===")
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
        
        # Assert - Should return 405 Method Not Allowed or 400 Bad Request
        assert response.status_code in [STATUS_BAD_REQUEST, 405], f"Expected 400 or 405, got {response.status_code}"
    
    @pytest.mark.regression
    @pytest.mark.add_equipment
    def test_add_equipment_malformed_json(self, api_client: EquipmentAPIClient):
        """Malformed JSON in request"""
        # Arrange - Malformed JSON
        malformed_data = f'{{"name": "Test", "{INVALID_ENDPOINT_SUFFIX}": "{EQUIPMENT_STATUS_ACTIVE}", "location": "Test"}}'
        
        print(f"\n=== REQUEST (Malformed JSON) ===")
        print(f"Payload: {malformed_data}")
        
        # Act - Send malformed JSON
        url = f"{api_client.base_url}{ADD_EQUIPMENT_ENDPOINT}"
        response = api_client.session.post(
            url=url,
            data=malformed_data,
            headers={"Content-Type": "application/json"},
            timeout=api_client.timeout
        )
        
        print(f"\n=== RESPONSE ===")
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
        
        # Assert - Should return 400 Bad Request
        assert_status_code(response, STATUS_BAD_REQUEST)
    
    @pytest.mark.regression
    @pytest.mark.add_equipment
    def test_add_equipment_special_characters(self, api_client: EquipmentAPIClient):
        """Special characters in fields"""
        # Arrange - Create payload with special characters
        special_data = {
            "name": "Test@#$%^&*()_+{}|:<>?[]\\;'\",./",
            "status": EQUIPMENT_STATUS_ACTIVE,
            "location": "Location@#$%^&*()_+{}|:<>?[]\\;'\",./"
        }
        
        print(f"\n=== REQUEST (Special Characters) ===")
        print(f"Payload: {json.dumps(special_data, indent=2)}")
        
        # Act - Send request with special characters
        response = api_client._make_request("POST", ADD_EQUIPMENT_ENDPOINT, data=special_data)
        
        print(f"\n=== RESPONSE ===")
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
        
        # Assert - Should return 201 Created
        assert response.status_code in [STATUS_CREATED], f"Expected 201, got {response.status_code}"