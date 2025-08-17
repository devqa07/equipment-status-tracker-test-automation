"""
Pytest configuration and fixtures for Equipment Status Tracker API tests
"""

import pytest
import allure
from api_client.equipment_api import EquipmentAPIClient
from helpers.test_data import create_equipment_payload, get_sample_equipment

@pytest.fixture(scope="session")
def api_client():
    """
    Fixture to provide API client instance
    Returns:
        EquipmentAPIClient instance
    """
    client = EquipmentAPIClient()
    
    # Verify API is accessible
    if not client.health_check():
        pytest.skip("API is not accessible")
    
    return client

@pytest.fixture
def sample_equipment_data():
    """
    Fixture to provide sample equipment data
    Returns:
        Sample equipment dictionary
    """
    return get_sample_equipment()

@pytest.fixture
def dynamic_equipment_data():
    """
    Fixture to provide dynamically generated equipment data
    Returns:
        Dynamically generated equipment dictionary
    """
    return create_equipment_payload()

@pytest.fixture
def multiple_equipment_data():
    """
    Fixture to provide multiple equipment data for batch testing
    Returns:
        List of equipment dictionaries
    """
    from helpers.test_data import create_multiple_equipment_payloads
    return create_multiple_equipment_payloads(3)

# Allure reporting hooks
def pytest_runtest_setup(item):
    """Setup hook for Allure reporting"""
    allure.dynamic.description(f"Test: {item.name}")

def pytest_runtest_teardown(item, nextitem):
    """Teardown hook for Allure reporting"""
    pass

def pytest_configure(config):
    """Register custom markers"""
    config.addinivalue_line("markers", "smoke: Smoke tests")
    config.addinivalue_line("markers", "regression: Regression tests")
    config.addinivalue_line("markers", "api: API tests")
    config.addinivalue_line("markers", "equipment: Equipment related tests")
    config.addinivalue_line("markers", "add_equipment: Add equipment tests")
    config.addinivalue_line("markers", "get_equipment: Get equipment tests")
    config.addinivalue_line("markers", "update_status: Update status tests")
    config.addinivalue_line("markers", "get_history: Get history tests")
    config.addinivalue_line("markers", "performance: Performance tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "p0: Priority 0 tests")
    config.addinivalue_line("markers", "p1: Priority 1 tests")
    config.addinivalue_line("markers", "p2: Priority 2 tests")
    config.addinivalue_line("markers", "p3: Priority 3 tests")

def pytest_sessionfinish(session, exitstatus):
    """Generate HTML report after all tests complete"""
    import subprocess
    import os
    
    # Check if allure-results exists
    results_dir = "reports/allure-results"
    if os.path.exists(results_dir) and os.listdir(results_dir):
        print("\nGenerating HTML report...")
        try:
            # Generate HTML report
            cmd = [
                "allure", "generate", 
                results_dir, 
                "--clean", 
                "-o", "reports/allure-report"
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Report generated")
            else:
                print(f"❌ Failed to generate report: {result.stderr}")
        except Exception as e:
            print(f"❌ Error generating HTML report: {e}")
    else:
        print("No Allure results found to generate report from.")
