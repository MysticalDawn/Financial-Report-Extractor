"""
Helper Utilities

Common utility functions used throughout the application.
"""

import os
from dotenv import load_dotenv


def load_environment() -> str:
    """Load environment variables and return API key.

    Returns:
        OpenAI API key

    Raises:
        ValueError: If API key is not found
    """
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Please set the OPENAI_API_KEY environment variable.")
    return api_key


def setup_environment():
    """Set up environment variables and configurations."""
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    load_dotenv()
