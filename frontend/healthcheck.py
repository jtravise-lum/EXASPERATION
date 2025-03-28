#!/usr/bin/env python3
"""
Health check script for the EXASPERATION frontend container.
This is used by Docker to check if the frontend is running properly.
"""

import http.client
import sys
import os
import time

def check_streamlit_health():
    """
    Check if the Streamlit server is responding.
    """
    try:
        # Define connection parameters
        host = "localhost"
        port = int(os.environ.get("STREAMLIT_SERVER_PORT", 8501))
        
        # Connect and make a request
        conn = http.client.HTTPConnection(host, port, timeout=5)
        conn.request("GET", "/_stcore/health")
        response = conn.getresponse()
        
        # Check if response is successful
        if response.status == 200:
            return True
        return False
    except Exception as e:
        print(f"Health check failed: {str(e)}")
        return False

if __name__ == "__main__":
    # Allow the server some time to start up
    retry_count = 3
    retry_delay = 1
    
    for _ in range(retry_count):
        if check_streamlit_health():
            print("Streamlit server is healthy")
            sys.exit(0)
        time.sleep(retry_delay)
    
    print("Streamlit server is not responding")
    sys.exit(1)