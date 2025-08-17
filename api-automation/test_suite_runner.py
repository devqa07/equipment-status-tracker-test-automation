#!/usr/bin/env python3
"""
Comprehensive Test Suite Runner
All test suite configurations in one file for easy management
"""

import subprocess
import sys
import os
from typing import List, Dict, Optional

class TestSuiteConfig:
    """Test Suite Configuration"""
    
    def __init__(self, 
                 name: str, 
                 description: str, 
                 markers: List[str] = None,
                 files: List[str] = None,
                 classes: List[str] = None,
                 methods: List[str] = None,
                 parallel: bool = False,
                 thread_count: int = 1):
        self.name = name
        self.description = description
        self.markers = markers or []
        self.files = files or []
        self.classes = classes or []
        self.methods = methods or []
        self.parallel = parallel
        self.thread_count = thread_count

class TestSuiteRunner:
    """Master Test Suite Runner"""
    
    def __init__(self):
        # Define all test suites
        self.test_suites = {
            # Smoke Test Suite - Critical functionality
            "smoke": TestSuiteConfig(
                name="Smoke Test Suite",
                description="Critical functionality tests - must pass for deployment",
                markers=["smoke", "p0"],
                files=["tests/test_add_equipment.py", "tests/test_get_all_equipment.py"],
                parallel=False
            ),

            # Regression Test Suite - Comprehensive testing
            "regression": TestSuiteConfig(
                name="Regression Test Suite",
                description="Comprehensive testing of all features",
                markers=["regression", "api", "equipment"],
                files=["tests/"],
                parallel=True,
                thread_count=4
            ),

            # API Test Suite - All API endpoints
            "api": TestSuiteConfig(
                name="API Test Suite",
                description="All API endpoint tests",
                markers=["add_equipment", "get_equipment", "update_status", "get_history"],
                files=["tests/"],
                parallel=True,
                thread_count=2
            ),

            # Equipment Test Suite - Equipment-specific tests
            "equipment": TestSuiteConfig(
                name="Equipment Test Suite",
                description="All equipment-related tests",
                markers=["add_equipment", "get_equipment", "update_status", "get_history"],
                files=["tests/"],
                parallel=False
            ),

            # Add Equipment Test Suite
            "add_equipment": TestSuiteConfig(
                name="Add Equipment Test Suite",
                description="Add Equipment API tests",
                markers=["add_equipment"],
                files=["tests/test_add_equipment.py"],
                parallel=False
            ),

            # Get Equipment Test Suite
            "get_equipment": TestSuiteConfig(
                name="Get Equipment Test Suite",
                description="Get Equipment API tests",
                markers=["get_equipment"],
                files=["tests/test_get_all_equipment.py"],
                parallel=False
            ),

            # Update Status Test Suite
            "update_status": TestSuiteConfig(
                name="Update Status Test Suite",
                description="Update Equipment Status API tests",
                markers=["update_status"],
                files=["tests/test_update_equipment_status.py"],
                parallel=False
            ),

            # Get History Test Suite
            "get_history": TestSuiteConfig(
                name="Get History Test Suite",
                description="Get Equipment History API tests",
                markers=["get_history"],
                files=["tests/test_get_equipment_history.py"],
                parallel=False
            ),

            # Performance Test Suite
            "performance": TestSuiteConfig(
                name="Performance Test Suite",
                description="Performance and load testing",
                markers=["regression"],
                files=["tests/"],
                parallel=True,
                thread_count=3
            ),

            # Integration Test Suite
            "integration": TestSuiteConfig(
                name="Integration Test Suite",
                description="End-to-end integration tests",
                markers=["smoke", "regression"],
                files=["tests/"],
                parallel=False
            ),

            # All Tests Suite
            "all": TestSuiteConfig(
                name="All Tests Suite",
                description="Run all tests in the project",
                files=["tests/"],
                parallel=True,
                thread_count=4
            )
        }

    def run_suite(self, suite_name: str, generate_report: bool = True, open_report: bool = True) -> bool:
        """Run a specific test suite"""
        if suite_name not in self.test_suites:
            print(f"[ERROR] Test suite '{suite_name}' not found!")
            self.list_available_suites()
            return False

        suite = self.test_suites[suite_name]
        success = self._execute_suite(suite, generate_report, open_report=False)
        
        # Open report only once at the end
        if open_report and success:
            self._open_report()
        
        return success

    def run_multiple_suites(self, suite_names: List[str], generate_report: bool = True, open_report: bool = True) -> Dict[str, bool]:
        """Run multiple test suites"""
        print(f"Running Multiple Test Suites: {', '.join(suite_names)}")
        print("=" * 60)
        
        results = {}
        for suite_name in suite_names:
            if suite_name in self.test_suites:
                results[suite_name] = self.run_suite(suite_name, generate_report=False, open_report=False)
            else:
                print(f"[WARNING] Suite '{suite_name}' not found, skipping...")
                results[suite_name] = False
        
        # Generate final report
        if generate_report:
            self._generate_report()
        
        # Open report only once at the end
        if open_report:
            self._open_report()
        
        # Print summary
        self._print_summary(results)
        
        return results

    def run_all_suites(self, generate_report: bool = True, open_report: bool = True) -> Dict[str, bool]:
        """Run all test suites"""
        print("Running All Test Suites...")
        
        results = {}
        for suite_name, suite in self.test_suites.items():
            if suite_name != "all":  # Skip the "all" suite to avoid duplication
                results[suite_name] = self._execute_suite(suite, generate_report=False, open_report=False)
        
        # Generate final report only once
        if generate_report:
            print("Generating final report...")
            self._generate_report()
        
        # Open report only once at the end
        if open_report:
            self._open_report()
        
        # Print summary
        self._print_summary(results)
        
        return results

    def _execute_suite(self, suite: TestSuiteConfig, generate_report: bool = True, open_report: bool = True) -> bool:
        """Execute a single test suite"""
        print(f"Running: {suite.name}")
        
        # Build pytest command with request/response output
        cmd = [
            sys.executable, "-m", "pytest",
            "--tb=no",
            "-s",
            "--alluredir=reports/allure-results"
        ]
        
        # Add markers
        if suite.markers:
            marker_expr = " or ".join(suite.markers)
            cmd.extend(["-m", marker_expr])
        
        # Add specific files
        if suite.files:
            cmd.extend(suite.files)
        
        # Add parallel execution
        if suite.parallel and suite.thread_count > 1:
            cmd.extend(["-n", str(suite.thread_count)])
        
        try:
            result = subprocess.run(cmd, capture_output=False, text=True)
            
            if result.returncode == 0:
                print(f"{suite.name} completed successfully!")
                return True
            else:
                print(f"{suite.name} had some failures")
                return False
                
        except Exception as e:
            print(f"Error running {suite.name}: {e}")
            return False

    def _generate_report(self):
        """Generate Allure report"""
        try:
            subprocess.run([
                "allure", "generate",
                "reports/allure-results",
                "--clean",
                "-o", "reports/allure-report"
            ], check=True, capture_output=True)
        except Exception as e:
            print(f"Error generating report: {e}")

    def _open_report(self):
        """Open Allure report in browser"""
        try:
            print("Opening report in browser...")
            subprocess.run([
                "allure", "serve",
                "reports/allure-results"
            ], check=True)
        except Exception as e:
            print(f"[WARNING] Could not open report automatically: {e}")
            print("[INFO] Manual: python serve_report.py")

    def _print_summary(self, results: Dict[str, bool]):
        """Print test suite execution summary"""
        passed = sum(1 for success in results.values() if success)
        total = len(results)
        
        print(f"\nSummary: {passed}/{total} test suites passed")
        
        if passed == total:
            print("All test suites completed successfully!")
        else:
            print("Some test suites had failures")

    def list_available_suites(self):
        """List all available test suites"""
        print("\nAvailable Test Suites:")
        print("-" * 40)
        for name, suite in self.test_suites.items():
            print(f"• {name}: {suite.description}")

    def get_suite_info(self, suite_name: str):
        """Get detailed information about a test suite"""
        if suite_name not in self.test_suites:
            print(f"[ERROR] Test suite '{suite_name}' not found!")
            return
        
        suite = self.test_suites[suite_name]
        print(f"\nTest Suite: {suite.name}")
        print(f"Description: {suite.description}")
        print(f"Markers: {', '.join(suite.markers) if suite.markers else 'None'}")
        print(f"Files: {', '.join(suite.files) if suite.files else 'All test files'}")
        print(f"Parallel: {'Yes' if suite.parallel else 'No'}")
        if suite.parallel:
            print(f"Thread Count: {suite.thread_count}")

def main():
    """Main function - Command line interface"""
    runner = TestSuiteRunner()
    
    if len(sys.argv) < 2:
        print("Test Suite Runner")
        print("=" * 40)
        runner.list_available_suites()
        print("\nUsage:")
        print("  python test_suite_runner.py <suite_name>                    # Run specific suite")
        print("  python test_suite_runner.py <suite1> <suite2> <suite3>      # Run multiple suites")
        print("  python test_suite_runner.py all                             # Run all suites")
        print("  python test_suite_runner.py info <suite_name>               # Get suite info")
        print("\nExamples:")
        print("  python test_suite_runner.py smoke")
        print("  python test_suite_runner.py regression")
        print("  python test_suite_runner.py smoke regression")
        print("  python test_suite_runner.py all")
        print("  python test_suite_runner.py info smoke")
        return

    command = sys.argv[1]

    if command == "info" and len(sys.argv) > 2:
        suite_name = sys.argv[2]
        runner.get_suite_info(suite_name)
    elif command == "all":
        runner.run_all_suites()
    elif len(sys.argv) == 2:
        # Single suite
        suite_name = sys.argv[1]
        runner.run_suite(suite_name)
    else:
        # Multiple suites
        suite_names = sys.argv[1:]
        runner.run_multiple_suites(suite_names)

if __name__ == "__main__":
    main() 