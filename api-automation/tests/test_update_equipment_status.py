"""
Test cases for updating equipment status
"""

import pytest
import allure
import json
from api_client.equipment_api import EquipmentAPIClient

from helpers.validations import (
    assert_status_code, 
    assert_response_time, 
    assert_content_type,
    validate_equipment_status_update_response
)
from helpers.constants import (
    STATUS_OK,
    MAX_RESPONSE_TIME,
    CONTENT_TYPE_JSON,
    UPDATE_STATUS_ENDPOINT,
    TEST_EQUIPMENT_ID,
    INVALID_EQUIPMENT_ID,
    TEST_OPERATOR,
    PERFORMANCE_TEST_OPERATOR,
    EQUIPMENT_STATUS_ACTIVE,
    EQUIPMENT_STATUS_IDLE,
    INVALID_STATUS,
    INVALID_ENDPOINT_SUFFIX
)
from tests.base_test import BaseAPITest


class TestUpdateEquipmentStatus(BaseAPITest):
    """Test cases for updating equipment status"""

    @pytest.fixture
    def valid_status_data(self):
        """Fixture for valid status update data"""
        return {
            "status": EQUIPMENT_STATUS_ACTIVE,
            "changedBy": TEST_OPERATOR
        }

    @pytest.fixture
    def invalid_status_data(self):
        """Fixture for invalid status update data"""
        return {
            "status": INVALID_STATUS,
            "changedBy": TEST_OPERATOR
        }

    @pytest.fixture
    def incomplete_status_data(self):
        """Fixture for incomplete status update data (missing changedBy)"""
        return {
            "status": EQUIPMENT_STATUS_ACTIVE
        }

    @pytest.fixture
    def performance_status_data(self):
        """Fixture for performance test status update data"""
        return {
            "status": EQUIPMENT_STATUS_IDLE,
            "changedBy": PERFORMANCE_TEST_OPERATOR
        }



    @pytest.mark.smoke
    @pytest.mark.update_status
    def test_update_equipment_status_success(self, api_client: EquipmentAPIClient, valid_status_data):
        """Update equipment status successfully"""
        url = f"{api_client.base_url}{UPDATE_STATUS_ENDPOINT.format(id=TEST_EQUIPMENT_ID)}"
        
        self._log_request("POST", url, dict(api_client.session.headers), valid_status_data)
        
        with allure.step("Send POST request to update equipment status"):
            response, response_data = api_client.update_equipment_status_with_response(TEST_EQUIPMENT_ID, valid_status_data)
            self._log_response(response, response_data)
        
        with allure.step("Validate response structure and data"):
            assert_status_code(response, STATUS_OK)
            assert_response_time(response, MAX_RESPONSE_TIME)
            assert_content_type(response, CONTENT_TYPE_JSON)
            validate_equipment_status_update_response(response_data)

    @pytest.mark.regression
    @pytest.mark.update_status
    def test_update_equipment_status_invalid_id(self, api_client: EquipmentAPIClient, valid_status_data):
        """Invalid equipment ID"""
        url = f"{api_client.base_url}{UPDATE_STATUS_ENDPOINT.format(id=INVALID_EQUIPMENT_ID)}"
        
        self._log_request("POST", url, payload=valid_status_data)
        
        with allure.step("Send POST request with invalid equipment ID"):
            response = api_client._make_request("POST", UPDATE_STATUS_ENDPOINT.format(id=INVALID_EQUIPMENT_ID), data=valid_status_data)
            self._log_response(response)
        
        with allure.step("Validate error response"):
            assert response.status_code in [404, 400], f"Expected 404 or 400, got {response.status_code}"

    @pytest.mark.regression
    @pytest.mark.update_status
    def test_update_equipment_status_invalid_status(self, api_client: EquipmentAPIClient, invalid_status_data):
        """Invalid status value"""
        url = f"{api_client.base_url}{UPDATE_STATUS_ENDPOINT.format(id=TEST_EQUIPMENT_ID)}"
        
        self._log_request("POST", url, payload=invalid_status_data)
        
        with allure.step("Send POST request with invalid status"):
            response = api_client._make_request("POST", UPDATE_STATUS_ENDPOINT.format(id=TEST_EQUIPMENT_ID), data=invalid_status_data)
            self._log_response(response)
        
        with allure.step("Validate error response"):
            assert response.status_code in [400, 422], f"Expected 400 or 422, got {response.status_code}"

    @pytest.mark.regression
    @pytest.mark.update_status
    def test_update_equipment_status_missing_fields(self, api_client: EquipmentAPIClient, incomplete_status_data):
        """Missing required fields - API uses default values"""
        url = f"{api_client.base_url}{UPDATE_STATUS_ENDPOINT.format(id=TEST_EQUIPMENT_ID)}"
        
        self._log_request("POST", url, payload=incomplete_status_data)
        
        with allure.step("Send POST request with missing required fields"):
            response = api_client._make_request("POST", UPDATE_STATUS_ENDPOINT.format(id=TEST_EQUIPMENT_ID), data=incomplete_status_data)
            self._log_response(response)
        
        with allure.step("Validate API behavior with missing fields"):
            # API accepts missing changedBy and uses default value "System"
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            
            if response.status_code == 200:
                response_data = response.json()
                assert response_data["success"] is True, "Success should be True"
                assert "data" in response_data, "Data field should be present"
                assert "historyEntry" in response_data["data"], "History entry should be present"
                assert response_data["data"]["historyEntry"]["changedBy"] == "System", "Default changedBy should be 'System'"

    @pytest.mark.regression
    @pytest.mark.update_status
    def test_update_equipment_status_wrong_method(self, api_client: EquipmentAPIClient):
        """Wrong HTTP method (GET instead of POST)"""
        url = f"{api_client.base_url}{UPDATE_STATUS_ENDPOINT.format(id=TEST_EQUIPMENT_ID)}"
        
        self._log_request("GET", url)
        
        with allure.step("Send GET request instead of POST"):
            response = api_client._make_request("GET", UPDATE_STATUS_ENDPOINT.format(id=TEST_EQUIPMENT_ID))
            self._log_response(response)
        
        with allure.step("Validate error response"):
            assert response.status_code == 405, f"Expected 405, got {response.status_code}"

    @pytest.mark.regression
    @pytest.mark.update_status
    def test_update_equipment_status_invalid_endpoint(self, api_client: EquipmentAPIClient, valid_status_data):
        """Invalid endpoint URL (404 Not Found)"""
        invalid_endpoint = f"/api/equipment/{TEST_EQUIPMENT_ID}/{INVALID_ENDPOINT_SUFFIX}"
        url = f"{api_client.base_url}{invalid_endpoint}"
        
        self._log_request("POST", url, dict(api_client.session.headers), valid_status_data)
        
        with allure.step("Send POST request to invalid endpoint"):
            response = api_client._make_request("POST", invalid_endpoint, data=valid_status_data)
            self._log_response(response)
        
        with allure.step("Validate error response for invalid endpoint"):
            assert response.status_code in [404, 405], f"Expected 404 or 405, got {response.status_code}"

    @pytest.mark.regression
    @pytest.mark.update_status
    def test_update_equipment_status_response_time(self, api_client: EquipmentAPIClient, performance_status_data):
        """Response time validation"""
        url = f"{api_client.base_url}{UPDATE_STATUS_ENDPOINT.format(id=TEST_EQUIPMENT_ID)}"
        
        self._log_request("POST", url)
        
        with allure.step("Send POST request and measure response time"):
            response, response_data = api_client.update_equipment_status_with_response(TEST_EQUIPMENT_ID, performance_status_data)
            self._log_performance_response(response, response_data)
        
        with allure.step("Validate performance"):
            assert_status_code(response, STATUS_OK)
            assert_response_time(response, MAX_RESPONSE_TIME)
            
            response_time = response.elapsed.total_seconds()
            assert response_time < 5.0, f"Response time too slow: {response_time}s"
            
            self._attach_performance_metrics(response, response_data) 