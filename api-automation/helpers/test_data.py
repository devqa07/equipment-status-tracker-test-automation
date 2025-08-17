"""
Test data generation utilities for Equipment Status Tracker API tests
"""

import json
import random
import time
from typing import Dict, Any, List

def load_test_data(file_path: str = None) -> Dict[str, Any]:
    """Load test data from JSON file"""
    if file_path is None:
        file_path = "test_data/equipment_data.json"
        
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Warning: Test data file {file_path} not found")
        return {}

def generate_equipment_name() -> str:
    """
    Generate a unique equipment name with random 6 digits
    Returns: "Test_equipment_XXXXXX" where XXXXXX is 6 random digits
    """
    # Generate 6 random digits
    random_digits = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    return f"Test_equipment_{random_digits}"

def generate_location() -> str:
    """
    Generate a unique location with random 6 digits
    Returns: "Test_location_XXXXXX" where XXXXXX is 6 random digits
    """
    # Generate 6 random digits
    random_digits = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    return f"Test_location_{random_digits}"

def get_random_status() -> str:
    """
    Get a random status from test data
    Returns: Random status from available options
    """
    test_data = load_test_data()
    status_options = test_data.get("status_options", ["Active", "Idle", "Under Maintenance"])
    
    return random.choice(status_options)



def create_equipment_payload(name: str = None, status: str = None, location: str = None) -> Dict[str, str]:
    """
    Create equipment payload with dynamic data
    Args:
        name: Equipment name (generated if not provided)
        status: Equipment status (from test data)
        location: Equipment location (generated if not provided)
    Returns:
        Dictionary with equipment data
    """
    # Get status from test data if not provided
    if status is None:
        status = get_random_status()
    
    payload = {
        "name": name or generate_equipment_name(),
        "status": status,
        "location": location or generate_location()
    }
    
    return payload

def create_multiple_equipment_payloads(count: int = 3) -> List[Dict[str, str]]:
    """
    Create multiple equipment payloads for batch testing
    Args:
        count: Number of equipment payloads to create
    Returns:
        List of equipment payload dictionaries
    """
    payloads = []
    for _ in range(count):
        payloads.append(create_equipment_payload())
        # Small delay to ensure unique timestamps
        time.sleep(0.1)
    
    return payloads

def get_sample_equipment() -> Dict[str, str]:
    """
    Get sample equipment data from test file
    Returns:
        Sample equipment dictionary
    """
    test_data = load_test_data()
    return test_data.get("sample_equipment", {
        "name": "Test Equipment",
        "status": "Active", 
        "location": "Test Site"
    })
