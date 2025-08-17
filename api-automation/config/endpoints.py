"""
API endpoints configuration for Equipment Status Tracker API automation
"""

import os
from typing import Dict, Any

# API Configuration
BASE_URL = "https://qa-assignment-omega.vercel.app"
API_VERSION = "v1"

# Endpoints
ENDPOINTS = {
    "add_equipment": "/api/equipment",
    "get_equipment": "/api/equipment", 
    "update_status": "/api/equipment/{id}/status",
    "get_history": "/api/equipment/{id}/history"
}

# Headers
DEFAULT_HEADERS = {
    "accept": "application/json",
    "Content-Type": "application/json"
}

# Test Configuration
TIMEOUT = 30
RETRY_ATTEMPTS = 3

# Environment variables
def get_config() -> Dict[str, Any]:
    """Get configuration with environment variable support"""
    return {
        "base_url": os.getenv("API_BASE_URL", BASE_URL),
        "timeout": int(os.getenv("API_TIMEOUT", TIMEOUT)),
        "retry_attempts": int(os.getenv("API_RETRY_ATTEMPTS", RETRY_ATTEMPTS))
    }
