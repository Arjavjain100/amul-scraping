import requests
from typing import List, Dict, Any, Optional
import config
from logger import default_logger as logger
from session_storage import session_storage


class AmulApiClient:
    """Client for making direct API calls to Amul using saved session data."""

    def __init__(self):
        self.timeout = 30

    def _prepare_cookies_dict(self, cookies: List[Dict[str, Any]]) -> Dict[str, str]:
        """Convert Playwright cookies to requests-compatible format.

        Args:
            cookies: List of cookie dictionaries from Playwright

        Returns:
            Dictionary of cookie name-value pairs for requests
        """
        cookies_dict = {}
        for cookie in cookies:
            if "name" in cookie and "value" in cookie:
                cookies_dict[cookie["name"]] = cookie["value"]
        return cookies_dict

    def fetch_products(self, pincode: str) -> Optional[List[Dict[str, Any]]]:
        """Fetch products directly from the API using saved session data.

        Args:
            pincode: The pincode to filter products for

        Returns:
            List of product dictionaries or None if failed
        """
        # Load saved session data
        saved_headers = session_storage.load_headers()
        saved_cookies = session_storage.load_cookies()

        if not saved_headers or not saved_cookies:
            logger.warning("No saved session data available for direct API call")
            return None

        try:
            logger.info(f"Making direct API call for pincode: {pincode}")

            # Convert cookies to requests format
            cookies_dict = self._prepare_cookies_dict(saved_cookies)

            # Make the API request using requests
            response = requests.get(
                config.API_URL,
                headers=saved_headers,
                cookies=cookies_dict,
                timeout=self.timeout,
            )
            response.raise_for_status()

            # Parse response
            data = response.json()
            products = data.get("data", [])

            logger.info(
                f"Direct API call successful - retrieved {len(products)} products"
            )
            return products

        except requests.exceptions.RequestException as e:
            logger.error(f"Direct API call failed: {e}")
            return None
        except Exception as e:
            logger.error(f"Error processing API response: {e}")
            return None

    def validate_session(self) -> bool:
        """Validate if the current session data is still working.

        Returns:
            bool: True if session is valid, False otherwise
        """
        # Load saved session data
        saved_headers = session_storage.load_headers()
        saved_cookies = session_storage.load_cookies()

        if not saved_headers or not saved_cookies:
            return False

        try:
            # Convert cookies to requests format
            cookies_dict = self._prepare_cookies_dict(saved_cookies)

            # Make a lightweight test request using requests
            response = requests.get(
                config.API_URL, headers=saved_headers, cookies=cookies_dict, timeout=10
            )

            # Check if we get a valid response
            if response.status_code == 200:
                data = response.json()
                if "data" in data:
                    logger.info("Session validation successful")
                    return True

            logger.warning(
                f"Session validation failed - status: {response.status_code}"
            )
            return False

        except Exception as e:
            logger.warning(f"Session validation failed: {e}")
            return False


# Global instance
api_client = AmulApiClient()
