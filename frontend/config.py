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

# Styling
THEME_PRIMARY_COLOR = os.getenv("STREAMLIT_THEME_PRIMARY_COLOR", "#0066CC")
THEME_SECONDARY_COLOR = "#00A3E0"
THEME_ACCENT_COLOR = "#FF6B00"
THEME_BACKGROUND_COLOR = "#F5F7FA"
THEME_TEXT_COLOR = "#333333"

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