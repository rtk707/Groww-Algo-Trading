"""
Environment Variables Configuration
Load API credentials from environment variables or .env file
"""
import os

try:
    from dotenv import load_dotenv
    # Load environment variables from .env file if it exists
    load_dotenv()
except ImportError:
    # python-dotenv not installed, will use environment variables only
    pass

# Groww API Credentials
API_KEY = os.getenv("GROWW_API_KEY", "")
API_SECRET = os.getenv("GROWW_API_SECRET", "")

