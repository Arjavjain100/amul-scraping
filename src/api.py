from typing import List, Dict, Any, Tuple
import requests
import config
from logger import default_logger as logger


def fetch_api_data() -> List[Dict[str, Any]]:
    """
     Fetches product data from the Amul API.

     Returns:
         A list of dictionaries, where each dictionary represents a product.

     Raises:
         requests.exceptions.RequestException: For connection errors or HTTP error status codes.
         KeyError: If the expected 'data' key is not in the JSON response.
     """

    logger.info("Fetching data from API...")
    response = requests.get(
        url=config.API_URL,
        cookies=config.API_COOKIES,
        headers=config.API_HEADERS,
    )
    # Raise an exception for 4xx or 5xx status codes
    response.raise_for_status()
    return response.json()['data']
