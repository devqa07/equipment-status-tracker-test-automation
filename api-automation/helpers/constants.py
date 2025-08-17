"""
Test constants for API automation framework
"""

# API Endpoints
API_BASE_URL = "https://qa-assignment-omega.vercel.app"
API_VERSION = "v1"
ADD_EQUIPMENT_ENDPOINT = "/api/equipment"
GET_ALL_EQUIPMENT_ENDPOINT = "/api/equipment"

# HTTP Status Codes
STATUS_OK = 200
STATUS_CREATED = 201
STATUS_BAD_REQUEST = 400
STATUS_NOT_FOUND = 404
STATUS_INTERNAL_SERVER_ERROR = 500

# Response Time Limits
MAX_RESPONSE_TIME = 5.0  # seconds

# Content Types
CONTENT_TYPE_JSON = "application/json"

# Equipment Status Options
EQUIPMENT_STATUS_ACTIVE = "Active"
EQUIPMENT_STATUS_IDLE = "Idle"
EQUIPMENT_STATUS_MAINTENANCE = "Under Maintenance"

# Test Data File Paths
EQUIPMENT_DATA_FILE = "test_data/equipment_data.json"

# Allure Severity Levels
SEVERITY_CRITICAL = "critical"
SEVERITY_HIGH = "high"
SEVERITY_NORMAL = "normal"
SEVERITY_LOW = "low"

# Test Categories
TEST_CATEGORY_SMOKE = "smoke"
TEST_CATEGORY_REGRESSION = "regression"
TEST_CATEGORY_ADD_EQUIPMENT = "add_equipment"

# Invalid Test Data
INVALID_STATUS = "InvalidStatus"
INVALID_ENDPOINT_SUFFIX = "invalid"

# Update Equipment Status
UPDATE_STATUS_ENDPOINT = "/api/equipment/{id}/status"
TEST_EQUIPMENT_ID = 7
INVALID_EQUIPMENT_ID = 99999
TEST_OPERATOR = "Operator D"
PERFORMANCE_TEST_OPERATOR = "Performance Operator"

# Get Equipment History
GET_HISTORY_ENDPOINT = "/api/equipment/{id}/history"
TEST_EQUIPMENT_ID_FOR_HISTORY = 1
INVALID_EQUIPMENT_ID_FOR_HISTORY = 99999 