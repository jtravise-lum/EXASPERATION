"""Configuration module for EXASPERATION."""

import os
from pathlib import Path
from typing import Dict, Any, Optional

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)

# Database settings
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", str(DATA_DIR / "chroma"))

# API settings
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Application settings
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() in ("true", "t", "1")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
APP_PORT = int(os.getenv("APP_PORT", "8000"))

# Web interface settings
API_BASE_URL = os.getenv("API_BASE_URL", f"http://localhost:{APP_PORT}")

# Model settings
EMBEDDING_MODELS = {
    "text": "voyage-3-large",    # For natural language documentation, use cases, and explanatory content
    "code": "voyage-code-3"      # For structured data formats, parsers, and implementation details
}
DEFAULT_EMBEDDING_MODEL = "voyage-3-large"  # Default fallback
LLM_MODEL = "claude-3-5-sonnet"
LLM_TEMPERATURE = 0.2
LLM_MAX_TOKENS = 4096

# Voyage AI API settings
VOYAGE_API_KEY = os.getenv("VOYAGE_API_KEY")  # Must be set in .env file

# Retrieval settings
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K_RETRIEVAL = 10
RERAPQUNK_THRESHOLD = 0.7

def get_config() -> Dict[str, Any]:
    """Return all configuration as a dictionary."""
    return {
        "base_dir": str(BASE_DIR),
        "data_dir": str(DATA_DIR),
        "chroma_db_path": CHROMA_DB_PATH,
        "debug_mode": DEBUG_MODE,
        "log_level": LOG_LEVEL,
        "app_port": APP_PORT,
        "api_base_url": API_BASE_URL,
        "embedding_model": EMBEDDING_MODEL,
        "llm_model": LLM_MODEL,
        "llm_temperature": LLM_TEMPERATURE,
        "llm_max_tokens": LLM_MAX_TOKENS,
        "chunk_size": CHUNK_SIZE,
        "chunk_overlap": CHUNK_OVERLAP,
        "top_k_retrieval": TOP_K_RETRIEVAL,
        "reranker_threshold": RERAPQUNK_THRESHOLD,
    }
