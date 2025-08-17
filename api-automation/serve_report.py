#!/usr/bin/env python3
"""
Simple HTTP server to serve Allure HTML report
"""

import http.server
import socketserver
import webbrowser
import os
import sys

def serve_report():
    """Serve the Allure HTML report on localhost"""
    
    # Check if report exists
    report_dir = "reports/allure-report"
    if not os.path.exists(report_dir):
        print("Report directory not found!")
        print("Please run tests first: python run_tests_and_generate_report.py")
        sys.exit(1)
    
    # Change to report directory
    os.chdir(report_dir)
    
    # Set up server
    PORT = 8080
    
    try:
        # Create a custom handler that doesn't log requests
        class QuietHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
            def log_message(self, format, *args):
                pass  # Don't log anything
        
        with socketserver.TCPServer(("", PORT), QuietHTTPRequestHandler) as httpd:
            print(f"Report opened at: http://localhost:{PORT}")
            print("Press Ctrl+C to stop")
            
            # Open browser
            webbrowser.open(f"http://localhost:{PORT}")
            
            # Start server
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\nServer stopped")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"Port {PORT} is already in use")
            print("Try a different port or stop the existing server")
        else:
            print(f"Error: {e}")

if __name__ == "__main__":
    serve_report() 