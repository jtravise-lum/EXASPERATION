"""Configuration management for the EXASPERATION frontend application."""

import os
from dotenv import load_dotenv

# Load environment variables from .env.frontend file
load_dotenv(".env.frontend")

# API Configuration
API_URL = os.getenv("EXASPERATION_API_URL", "http://localhost:8888/v1")
API_KEY = os.getenv("EXASPERATION_API_KEY", "")
API_TIMEOUT = int(os.getenv("EXASPERATION_API_TIMEOUT", "30"))

# Feature Flags
ENABLE_ANALYTICS = os.getenv("ENABLE_ANALYTICS", "false").lower() == "true"
ENABLE_AUTHENTICATION = os.getenv("ENABLE_AUTHENTICATION", "false").lower() == "true"
ENABLE_ADVANCED_FILTERS = os.getenv("ENABLE_ADVANCED_FILTERS", "true").lower() == "true"
ENABLE_SUGGESTIONS = os.getenv("ENABLE_SUGGESTIONS", "true").lower() == "true"

# Error Handling
ENABLE_MOCK_FALLBACKS = os.getenv("ENABLE_MOCK_FALLBACKS", "false").lower() == "true"
SHOW_API_ERRORS = os.getenv("SHOW_API_ERRORS", "true").lower() == "true"

# Color Scheme
COLORS = {
    "primary": "#1E2639",  # Deep dark blue
    "secondary": "#29344F",  # Lighter dark blue
    "accent": "#00B3E6",  # Vibrant cyan
    "text": "#E0E0E0",  # Very light gray
    "error": "#FF4136",
    "success": "#2ECC40",
}

# Typography
TEXT = {
    "family": "Roboto",
    "headings_weight": "bold",
    "body_weight": "regular",
    "headings_size": {
        "h1": "24px",
        "h2": "20px",
        "h3": "18px",
    },
    "body_size": "16px",
    "small_size": "14px",
}

# Default Parameters
DEFAULT_MAX_RESULTS = 10
DEFAULT_THRESHOLD = 0.7
DEFAULT_INCLUDE_METADATA = True
DEFAULT_RERANK = True

# Example queries for the search interface - focused on CIM content
EXAMPLE_QUERIES = [
    "What fields are available for the endpoint-login activity type?", 
    "How is lateral movement detection implemented in the Exabeam Common Information Model?",
    "What are the supported data sources for detecting privilege escalation?",
    "Explain the structure of the Exabeam Common Information Model",
    "What activity types are related to user authentication events?",
    "How does Cisco ASA integration work with Exabeam?",
    "What MITRE ATT&CK techniques are covered by the Exabeam Content Library?"
]