"""
Test cases for getting all equipment
"""

import pytest
import allure
import json
from api_client.equipment_api import EquipmentAPIClient

from helpers.validations import (
    assert_status_code, 
    assert_response_time, 
    assert_content_type,
    validate_equipment_list_response,
    validate_get_all_equipment_response
)
from helpers.constants import (
    STATUS_OK,
    MAX_RESPONSE_TIME,
    CONTENT_TYPE_JSON,
    GET_ALL_EQUIPMENT_ENDPOINT
)
from tests.base_test import BaseAPITest


class TestGetAllEquipment(BaseAPITest):
    """Test cases for getting all equipment"""

    @pytest.mark.smoke
    @pytest.mark.get_equipment
    def test_get_all_equipment_success(self, api_client: EquipmentAPIClient):
        """Get all equipment successfully"""
        url = f"{api_client.base_url}{GET_ALL_EQUIPMENT_ENDPOINT}"
        self._log_request("GET", url, dict(api_client.session.headers))
        
        with allure.step("Send GET request to retrieve all equipment"):
            response, response_data = api_client.get_all_equipment_with_response()
            self._log_response(response, response_data)
        
        with allure.step("Validate response structure and data"):
            # HTTP Level Assertions
            assert_status_code(response, STATUS_OK)
            assert_response_time(response, MAX_RESPONSE_TIME)
            assert_content_type(response, CONTENT_TYPE_JSON)
            
            # Comprehensive Response Validation
            validate_get_all_equipment_response(response_data)

    @pytest.mark.regression
    @pytest.mark.get_equipment
    def test_get_all_equipment_wrong_http_method(self, api_client: EquipmentAPIClient):
        """Wrong HTTP method (PUT instead of GET)"""
        print(f"\n=== REQUEST (Wrong Method - PUT) ===")
        print(f"Method: PUT {api_client.base_url}{GET_ALL_EQUIPMENT_ENDPOINT}")
        print(f"Payload: {{'test': 'data'}}")
        
        with allure.step("Send PUT request instead of GET"):
            response = api_client._make_request("PUT", GET_ALL_EQUIPMENT_ENDPOINT, data={"test": "data"})
            
            print(f"\n=== RESPONSE ===")
            print(f"Status Code: {response.status_code}")
            print(f"Response Body: {response.text}")
        
        with allure.step("Validate error response"):
            # Should return 405 Method Not Allowed
            assert response.status_code == 405, f"Expected 405, got {response.status_code}"

    @pytest.mark.regression
    @pytest.mark.get_equipment
    def test_get_all_equipment_with_query_params(self, api_client: EquipmentAPIClient):
        """GET request with query parameters"""
        print(f"\n=== REQUEST (With Query Params) ===")
        print(f"URL: GET {api_client.base_url}{GET_ALL_EQUIPMENT_ENDPOINT}?limit=5&offset=0")
        
        with allure.step("Send GET request with query parameters"):
            response = api_client._make_request("GET", GET_ALL_EQUIPMENT_ENDPOINT, params={"limit": 5, "offset": 0})
            
            print(f"\n=== RESPONSE ===")
            print(f"Status Code: {response.status_code}")
            print(f"Response Body: {response.text}")
        
        with allure.step("Validate response"):
            # API might ignore query params or return filtered results
            assert response.status_code in [200, 400], f"Expected 200 or 400, got {response.status_code}"


    @pytest.mark.regression
    @pytest.mark.get_equipment
    def test_get_all_equipment_response_time(self, api_client: EquipmentAPIClient):
        """Response time validation"""
        print(f"\n=== REQUEST (Performance Test) ===")
        print(f"URL: GET {api_client.base_url}{GET_ALL_EQUIPMENT_ENDPOINT}")
        
        with allure.step("Send GET request and measure response time"):
            response, response_data = api_client.get_all_equipment_with_response()
            
            print(f"\n=== RESPONSE ===")
            print(f"Status Code: {response.status_code}")
            print(f"Response Time: {response.elapsed.total_seconds():.3f}s")
            print(f"Equipment Count: {response_data.get('count', 0)}")
        
        with allure.step("Validate performance"):
            assert_status_code(response, STATUS_OK)
            assert_response_time(response, MAX_RESPONSE_TIME)
            
            # Additional performance assertions
            response_time = response.elapsed.total_seconds()
            assert response_time < 5.0, f"Response time too slow: {response_time}s"
            
            # Log performance metrics
            allure.attach(
                f"Response Time: {response_time}s\nEquipment Count: {response_data.get('count', 0)}",
                "Performance Metrics",
                allure.attachment_type.TEXT
            )

    @pytest.mark.regression
    @pytest.mark.get_equipment
    def test_get_all_equipment_invalid_endpoint(self, api_client: EquipmentAPIClient):
        """Invalid endpoint URL (404 Not Found)"""
        invalid_endpoint = "/api/equipmentt"  # Typo in endpoint
        print(f"\n=== REQUEST (Invalid Endpoint) ===")
        print(f"URL: GET {api_client.base_url}{invalid_endpoint}")
        print(f"Headers: {dict(api_client.session.headers)}")
        
        with allure.step("Send GET request to invalid endpoint"):
            response = api_client._make_request("GET", invalid_endpoint)
            
            print(f"\n=== RESPONSE ===")
            print(f"Status Code: {response.status_code}")
            print(f"Response Headers: {dict(response.headers)}")
            print(f"Response Body: {response.text}")
        
        with allure.step("Validate 404 Not Found response"):
            # Should return 404 Not Found
            assert response.status_code == 404, f"Expected 404, got {response.status_code}"
            
            # Additional validations for 404 response
            assert "not found" in response.text.lower() or response.status_code == 404, \
                f"Expected 'not found' in response or 404 status, got: {response.text}"
 