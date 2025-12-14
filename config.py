"""
Configuration management for FinGPT.
Loads environment variables and provides application settings.
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

# AI Configuration
AI_API_KEY = os.getenv("AI_API_KEY")
AI_MODEL = os.getenv("AI_MODEL", "gpt-4o-mini")

# Validate API key
if not AI_API_KEY:
    raise ValueError(
        "AI_API_KEY not found in environment variables. "
        "Please create a .env file with your API key. "
        "See .env.example for reference."
    )

# Project Paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
ASSETS_DIR = PROJECT_ROOT / "assets"

# Available Stock Tickers
AVAILABLE_TICKERS = ["AAPL", "AMZN", "META", "MSFT", "NFLX", "TSLA"]

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
