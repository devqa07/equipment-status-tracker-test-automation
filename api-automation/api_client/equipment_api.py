"""
API client for Equipment Status Tracker API operations
"""

import requests
import json
from typing import Dict, Any, Optional
from config.endpoints import get_config, ENDPOINTS, DEFAULT_HEADERS

class EquipmentAPIClient:
    """Client for Equipment Status Tracker API operations"""
    
    def __init__(self):
        self.config = get_config()
        self.base_url = self.config["base_url"]
        self.timeout = self.config["timeout"]
        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                     params: Optional[Dict] = None) -> requests.Response:
        """
        Make HTTP request with error handling
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint
            data: Request payload
            params: Query parameters
        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=self.timeout
            )
            return response
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
    
    def add_equipment(self, equipment_data: Dict[str, str]) -> Dict[str, Any]:
        """
        Add new equipment
        Args:
            equipment_data: Equipment data (name, status, location)
        Returns:
            Created equipment data with success wrapper
        """
        endpoint = ENDPOINTS["add_equipment"]
        response = self._make_request("POST", endpoint, data=equipment_data)
        
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Failed to add equipment. Status: {response.status_code}, Response: {response.text}")
    
    def add_equipment_with_response(self, equipment_data: Dict[str, str]) -> tuple[requests.Response, Dict[str, Any]]:
        """
        Add new equipment and return both response object and JSON data
        Args:
            equipment_data: Equipment data (name, status, location)
        Returns:
            Tuple of (response_object, json_data)
        """
        endpoint = ENDPOINTS["add_equipment"]
        response = self._make_request("POST", endpoint, data=equipment_data)
        
        if response.status_code == 201:
            return response, response.json()
        else:
            raise Exception(f"Failed to add equipment. Status: {response.status_code}, Response: {response.text}")
    
    def get_all_equipment(self) -> Dict[str, Any]:
        """
        Get all equipment
        Returns:
            Response with success wrapper and list of equipment
        """
        endpoint = ENDPOINTS["get_equipment"]
        response = self._make_request("GET", endpoint)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get equipment. Status: {response.status_code}, Response: {response.text}")
    
    def get_all_equipment_with_response(self) -> tuple[requests.Response, Dict[str, Any]]:
        """
        Get all equipment and return both response object and JSON data
        Returns:
            Tuple of (response_object, json_data)
        """
        endpoint = ENDPOINTS["get_equipment"]
        response = self._make_request("GET", endpoint)
        
        if response.status_code == 200:
            return response, response.json()
        else:
            return response, {}
    
    def update_equipment_status(self, equipment_id: str, status: str) -> Dict[str, Any]:
        """
        Update equipment status
        Args:
            equipment_id: Equipment ID
            status: New status
        Returns:
            Updated equipment data with success wrapper
        """
        endpoint = ENDPOINTS["update_status"].format(id=equipment_id)
        data = {"status": status}
        response = self._make_request("POST", endpoint, data=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to update status. Status: {response.status_code}, Response: {response.text}")
    
    def update_equipment_status_with_response(self, equipment_id: str, status_data: Dict[str, Any]) -> tuple[requests.Response, Dict[str, Any]]:
        """
        Update equipment status and return both response object and JSON data
        Args:
            equipment_id: Equipment ID
            status_data: Status update data (status, changedBy)
        Returns:
            Tuple of (response_object, json_data)
        """
        endpoint = ENDPOINTS["update_status"].format(id=equipment_id)
        response = self._make_request("POST", endpoint, data=status_data)
        
        if response.status_code == 200:
            return response, response.json()
        else:
            return response, {}
    
    def get_equipment_history(self, equipment_id: str) -> Dict[str, Any]:
        """
        Get equipment status history
        Args:
            equipment_id: Equipment ID
        Returns:
            Response with success wrapper and history data
        """
        endpoint = ENDPOINTS["get_history"].format(id=equipment_id)
        response = self._make_request("GET", endpoint)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get history. Status: {response.status_code}, Response: {response.text}")
    
    def get_equipment_history_with_response(self, equipment_id: str, params: Optional[Dict] = None) -> tuple[requests.Response, Dict[str, Any]]:
        """
        Get equipment status history and return both response object and JSON data
        Args:
            equipment_id: Equipment ID
            params: Query parameters (limit, offset)
        Returns:
            Tuple of (response_object, json_data)
        """
        endpoint = ENDPOINTS["get_history"].format(id=equipment_id)
        response = self._make_request("GET", endpoint, params=params)
        
        if response.status_code == 200:
            return response, response.json()
        else:
            return response, {}
    
    def health_check(self) -> bool:
        """
        Check if API is accessible
        Returns:
            True if API is accessible
        """
        try:
            response = self._make_request("GET", "/api/equipment")
            return response.status_code in [200, 404, 500]  # 404 is acceptable for empty list, 500 for server issues
        except:
            return False
