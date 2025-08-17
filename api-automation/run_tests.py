#!/usr/bin/env python3
"""
Simple script to run all 32 tests with minimal output
"""

import subprocess
import sys

def run_all_tests():
    """Run all 32 tests with clean output"""
    print("Running all 32 tests...")
    
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "--tb=no",
        "-q",
        "--no-header",
        "--no-summary",
        "--alluredir=reports/allure-results"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("All tests passed!")
        else:
            print("Some tests failed")
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 