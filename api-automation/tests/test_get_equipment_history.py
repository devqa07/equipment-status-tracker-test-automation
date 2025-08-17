"""
Test cases for getting equipment status history
"""

import pytest
import json
import allure
from api_client.equipment_api import EquipmentAPIClient

from helpers.validations import (
    assert_status_code, 
    assert_response_time, 
    assert_content_type,
    validate_equipment_history_response
)
from helpers.constants import (
    STATUS_OK,
    MAX_RESPONSE_TIME,
    CONTENT_TYPE_JSON,
    GET_HISTORY_ENDPOINT,
    TEST_EQUIPMENT_ID_FOR_HISTORY,
    INVALID_EQUIPMENT_ID_FOR_HISTORY,
    INVALID_ENDPOINT_SUFFIX
)
from tests.base_test import BaseAPITest


class TestGetEquipmentHistory(BaseAPITest):
    """Test cases for getting equipment status history"""

    @pytest.fixture
    def default_params(self):
        """Fixture for default query parameters"""
        return {"limit": 10, "offset": 1}

    @pytest.fixture
    def custom_params(self):
        """Fixture for custom query parameters"""
        return {"limit": 5, "offset": 2}

    @pytest.fixture
    def large_limit_params(self):
        """Fixture for large limit parameter"""
        return {"limit": 50, "offset": 0}

    @pytest.mark.smoke
    @pytest.mark.get_history
    def test_get_equipment_history_success(self, api_client: EquipmentAPIClient, default_params):
        """Get equipment history successfully"""
        url = f"{api_client.base_url}{GET_HISTORY_ENDPOINT.format(id=TEST_EQUIPMENT_ID_FOR_HISTORY)}"
        self._log_request("GET", url, dict(api_client.session.headers), params=default_params)
        
        with allure.step("Send GET request to retrieve equipment history"):
            response, response_data = api_client.get_equipment_history_with_response(TEST_EQUIPMENT_ID_FOR_HISTORY, default_params)
            self._log_response(response, response_data)
        
        with allure.step("Validate response structure and data"):
            assert_status_code(response, STATUS_OK)
            assert_response_time(response, MAX_RESPONSE_TIME)
            assert_content_type(response, CONTENT_TYPE_JSON)
            validate_equipment_history_response(response_data)

    @pytest.mark.regression
    @pytest.mark.get_history
    def test_get_equipment_history_with_custom_params(self, api_client: EquipmentAPIClient, custom_params):
        """Get equipment history with custom limit and offset"""
        url = f"{api_client.base_url}{GET_HISTORY_ENDPOINT.format(id=TEST_EQUIPMENT_ID_FOR_HISTORY)}"
        self._log_request("GET", url, dict(api_client.session.headers), params=custom_params)
        
        with allure.step("Send GET request with custom parameters"):
            response, response_data = api_client.get_equipment_history_with_response(TEST_EQUIPMENT_ID_FOR_HISTORY, custom_params)
            self._log_response(response, response_data)
        
        with allure.step("Validate response with custom parameters"):
            assert_status_code(response, STATUS_OK)
            assert_response_time(response, MAX_RESPONSE_TIME)
            assert_content_type(response, CONTENT_TYPE_JSON)
            validate_equipment_history_response(response_data)
            
            # Validate pagination parameters
            data = response_data["data"]
            assert data["limit"] == custom_params["limit"], f"Expected limit {custom_params['limit']}, got {data['limit']}"
            assert data["offset"] == custom_params["offset"], f"Expected offset {custom_params['offset']}, got {data['offset']}"

    @pytest.mark.regression
    @pytest.mark.get_history
    def test_get_equipment_history_without_params(self, api_client: EquipmentAPIClient):
        """Get equipment history without query parameters (default behavior)"""
        url = f"{api_client.base_url}{GET_HISTORY_ENDPOINT.format(id=TEST_EQUIPMENT_ID_FOR_HISTORY)}"
        self._log_request("GET", url, dict(api_client.session.headers))
        
        with allure.step("Send GET request without parameters"):
            response, response_data = api_client.get_equipment_history_with_response(TEST_EQUIPMENT_ID_FOR_HISTORY)
            self._log_response(response, response_data)
        
        with allure.step("Validate response without parameters"):
            assert_status_code(response, STATUS_OK)
            assert_response_time(response, MAX_RESPONSE_TIME)
            assert_content_type(response, CONTENT_TYPE_JSON)
            validate_equipment_history_response(response_data)

    @pytest.mark.regression
    @pytest.mark.get_history
    def test_get_equipment_history_invalid_id(self, api_client: EquipmentAPIClient, default_params):
        """Invalid equipment ID - API returns empty history"""
        url = f"{api_client.base_url}{GET_HISTORY_ENDPOINT.format(id=INVALID_EQUIPMENT_ID_FOR_HISTORY)}"
        self._log_request("GET", url, dict(api_client.session.headers), params=default_params)
        
        with allure.step("Send GET request with invalid equipment ID"):
            response = api_client._make_request("GET", GET_HISTORY_ENDPOINT.format(id=INVALID_EQUIPMENT_ID_FOR_HISTORY), params=default_params)
            self._log_response(response)
        
        with allure.step("Validate API behavior with invalid ID"):
            # API returns 200 with empty history for non-existent equipment
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            
            if response.status_code == 200:
                response_data = response.json()
                assert response_data["success"] is True, "Success should be True"
                assert "data" in response_data, "Data field should be present"
                assert response_data["data"]["equipmentId"] == INVALID_EQUIPMENT_ID_FOR_HISTORY, "Equipment ID should match"
                assert response_data["data"]["history"] == [], "History should be empty"
                assert response_data["data"]["total"] == 0, "Total should be 0"
                assert response_data["data"]["hasMore"] is False, "HasMore should be False"

    @pytest.mark.regression
    @pytest.mark.get_history
    def test_get_equipment_history_wrong_method(self, api_client: EquipmentAPIClient):
        """Wrong HTTP method (POST instead of GET)"""
        url = f"{api_client.base_url}{GET_HISTORY_ENDPOINT.format(id=TEST_EQUIPMENT_ID_FOR_HISTORY)}"
        self._log_request("POST", url, dict(api_client.session.headers))
        
        with allure.step("Send POST request instead of GET"):
            response = api_client._make_request("POST", GET_HISTORY_ENDPOINT.format(id=TEST_EQUIPMENT_ID_FOR_HISTORY))
            self._log_response(response)
        
        with allure.step("Validate error response"):
            assert response.status_code == 405, f"Expected 405, got {response.status_code}"

    @pytest.mark.regression
    @pytest.mark.get_history
    def test_get_equipment_history_invalid_endpoint(self, api_client: EquipmentAPIClient, default_params):
        """Invalid endpoint URL (404 Not Found)"""
        invalid_endpoint = f"/api/equipment/{TEST_EQUIPMENT_ID_FOR_HISTORY}/histories"
        url = f"{api_client.base_url}{invalid_endpoint}"
        self._log_request("GET", url, dict(api_client.session.headers), params=default_params)
        
        with allure.step("Send GET request to invalid endpoint"):
            response = api_client._make_request("GET", invalid_endpoint, params=default_params)
            self._log_response(response)
        
        with allure.step("Validate error response for invalid endpoint"):
            assert response.status_code in [404, 405], f"Expected 404 or 405, got {response.status_code}"

    @pytest.mark.regression
    @pytest.mark.get_history
    def test_get_equipment_history_invalid_params(self, api_client: EquipmentAPIClient):
        """Invalid query parameters - API uses null values"""
        invalid_params = {"limit": "invalid", "offset": "invalid"}
        url = f"{api_client.base_url}{GET_HISTORY_ENDPOINT.format(id=TEST_EQUIPMENT_ID_FOR_HISTORY)}"
        self._log_request("GET", url, dict(api_client.session.headers), params=invalid_params)
        
        with allure.step("Send GET request with invalid parameters"):
            response = api_client._make_request("GET", GET_HISTORY_ENDPOINT.format(id=TEST_EQUIPMENT_ID_FOR_HISTORY), params=invalid_params)
            self._log_response(response)
        
        with allure.step("Validate API behavior with invalid parameters"):
            # API returns 200 with null values for invalid parameters
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            
            if response.status_code == 200:
                response_data = response.json()
                assert response_data["success"] is True, "Success should be True"
                assert "data" in response_data, "Data field should be present"
                assert response_data["data"]["limit"] is None, "Limit should be null for invalid input"
                assert response_data["data"]["offset"] is None, "Offset should be null for invalid input"

    @pytest.mark.regression
    @pytest.mark.get_history
    def test_get_equipment_history_large_limit(self, api_client: EquipmentAPIClient, large_limit_params):
        """Large limit parameter"""
        url = f"{api_client.base_url}{GET_HISTORY_ENDPOINT.format(id=TEST_EQUIPMENT_ID_FOR_HISTORY)}"
        self._log_request("GET", url, dict(api_client.session.headers), params=large_limit_params)
        
        with allure.step("Send GET request with large limit"):
            response, response_data = api_client.get_equipment_history_with_response(TEST_EQUIPMENT_ID_FOR_HISTORY, large_limit_params)
            self._log_response(response, response_data)
        
        with allure.step("Validate response with large limit"):
            assert_status_code(response, STATUS_OK)
            assert_response_time(response, MAX_RESPONSE_TIME)
            assert_content_type(response, CONTENT_TYPE_JSON)
            validate_equipment_history_response(response_data)

    @pytest.mark.regression
    @pytest.mark.get_history
    def test_get_equipment_history_response_time(self, api_client: EquipmentAPIClient, default_params):
        """Response time validation"""
        url = f"{api_client.base_url}{GET_HISTORY_ENDPOINT.format(id=TEST_EQUIPMENT_ID_FOR_HISTORY)}"
        self._log_request("GET", url)
        
        with allure.step("Send GET request and measure response time"):
            response, response_data = api_client.get_equipment_history_with_response(TEST_EQUIPMENT_ID_FOR_HISTORY, default_params)
            self._log_performance_response(response, response_data)
        
        with allure.step("Validate performance"):
            assert_status_code(response, STATUS_OK)
            assert_response_time(response, MAX_RESPONSE_TIME)
            
            response_time = response.elapsed.total_seconds()
            assert response_time < 5.0, f"Response time too slow: {response_time}s"
            
            self._attach_performance_metrics(response, response_data, "History Performance Metrics") 