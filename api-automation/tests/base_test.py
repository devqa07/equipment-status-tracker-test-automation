"""
Base test class with common functionality for all API tests
"""

import json
import pytest
import allure
from abc import ABC


def print_centered_header(text, width=80):
    """Print a centered header with equals signs"""
    print(f"\n{'=' * width}")
    print(f"{text:^{width}}")
    print(f"{'=' * width}")


class BaseAPITest(ABC):
    """Base class for all API tests with common functionality"""

    def _log_request(self, method, url, headers=None, payload=None, params=None):
        """Helper method to log request details"""
        print_centered_header("REQUEST")
        print(f"Method: {method}")
        print(f"URL: {url}")
        if headers:
            print(f"Headers:")
            for key, value in headers.items():
                print(f"  {key}: {value}")
        if payload:
            print(f"Payload:")
            print(json.dumps(payload, indent=4))
        if params:
            print(f"Query Parameters:")
            for key, value in params.items():
                print(f"  {key}: {value}")
        print()

    def _log_response(self, response, response_data=None):
        """Helper method to log response details"""
        print_centered_header("RESPONSE")
        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {response.elapsed.total_seconds():.3f}s")
        print(f"Headers:")
        for key, value in dict(response.headers).items():
            print(f"  {key}: {value}")
        if response_data:
            print(f"Response Body:")
            print(json.dumps(response_data, indent=4))
        else:
            print(f"Response Body: {response.text}")
        print()

    def _log_performance_response(self, response, response_data=None):
        """Helper method to log performance test response details"""
        print_centered_header("RESPONSE")
        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {response.elapsed.total_seconds():.3f}s")
        print(f"Headers:")
        for key, value in dict(response.headers).items():
            print(f"  {key}: {value}")
        if response_data:
            print(f"Response Body:")
            print(json.dumps(response_data, indent=4))
        else:
            print(f"Response Body: {response.text}")
        print()

    def _validate_basic_response(self, response, expected_status_code, max_response_time=5.0):
        """Helper method to validate basic response properties"""
        assert response.status_code == expected_status_code, \
            f"Expected status code {expected_status_code}, got {response.status_code}"
        
        response_time = response.elapsed.total_seconds()
        assert response_time < max_response_time, \
            f"Response time {response_time}s exceeds maximum {max_response_time}s"

    def _attach_performance_metrics(self, response, response_data, metric_name="Performance Metrics"):
        """Helper method to attach performance metrics to Allure report"""
        response_time = response.elapsed.total_seconds()
        metrics = f"Response Time: {response_time}s"
        
        if response_data and isinstance(response_data, dict):
            if 'count' in response_data:
                metrics += f"\nCount: {response_data['count']}"
            if 'data' in response_data and 'equipment' in response_data['data']:
                equipment_id = response_data['data']['equipment'].get('id', 'N/A')
                metrics += f"\nEquipment ID: {equipment_id}"
        
        allure.attach(metrics, metric_name, allure.attachment_type.TEXT) 