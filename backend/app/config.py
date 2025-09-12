"""
Configuration module for managing API keys and settings.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Global variable to store the dynamic API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

def set_api_key(api_key: str):
    """Set the Gemini API key dynamically."""
    global GEMINI_API_KEY
    GEMINI_API_KEY = api_key

def get_api_key() -> str:
    """Get the current Gemini API key."""
    return GEMINI_API_KEY