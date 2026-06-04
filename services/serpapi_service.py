import os
import requests
from dotenv import load_dotenv


load_dotenv()


def test_serpapi_connection() -> dict:
    """
    Test whether the SerpAPI key is valid by making a simple Google search request.
    """

    api_key = os.getenv("SERPAPI_API_KEY")
    base_url = os.getenv("SERPAPI_BASE_URL", "https://serpapi.com/search")

    if not api_key:
        raise ValueError("Missing SERPAPI_API_KEY in .env")

    params = {
        "engine": "google",
        "q": "Miami travel guide",
        "api_key": api_key
    }

    response = requests.get(base_url, params=params, timeout=30)

    if response.status_code != 200:
        raise Exception(
            f"SerpAPI connection failed. "
            f"Status code: {response.status_code}. "
            f"Response: {response.text}"
        )

    return response.json()