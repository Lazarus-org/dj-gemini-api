import requests
import logging
from typing import Dict, Any, Optional
from django.conf import settings
from requests.exceptions import RequestException

# Set up logging
logger = logging.getLogger(__name__)

# Validate required settings
if not hasattr(settings, "GEMINI_API_URL") or not hasattr(settings, "GEMINI_API_KEY"):
    raise ValueError("GEMINI_API_URL and GEMINI_API_KEY must be set in Django settings.")

GEMINI_API_URL = settings.GEMINI_API_URL
GEMINI_API_KEY = settings.GEMINI_API_KEY

# Constants
TIMEOUT = 10  # Timeout in seconds
MAX_RETRIES = 3  # Maximum number of retries for transient failures

def send_prompt_to_gemini(prompt: str, retries: int = MAX_RETRIES) -> Optional[Dict[str, Any]]:
    """
    Sends a prompt to the Gemini API and returns the response.

    Args:
        prompt (str): The prompt to send to the Gemini API.
        retries (int): Number of retries for transient failures.

    Returns:
        Optional[Dict[str, Any]]: The JSON response from the Gemini API, or None if all retries fail.

    Raises:
        ValueError: If the prompt is empty or invalid.
        Exception: If the API request fails after all retries.
    """
    if not prompt or not isinstance(prompt, str):
        raise ValueError("Prompt must be a non-empty string.")

    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "prompt": prompt,
    }

    for attempt in range(retries):
        try:
            response = requests.post(
                GEMINI_API_URL,
                json=data,
                headers=headers,
                timeout=TIMEOUT,
            )
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
            return response.json()  # Return the JSON response if successful

        except RequestException as e:
            logger.warning(f"Attempt {attempt + 1} failed: {e}")
            if attempt == retries - 1:  # If this was the last attempt
                logger.error(f"All {retries} attempts failed. Last error: {e}")
                raise Exception(f"Failed to get a valid response from Gemini API after {retries} attempts: {e}")
            continue  # Retry on transient failures

    return None  # This line is only reached if all retries fail