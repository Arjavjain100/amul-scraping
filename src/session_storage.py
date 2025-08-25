import json
import os
from typing import Dict, List, Optional, Any
from logger import default_logger as logger


class SessionStorage:
    """Manages storage and retrieval of cookies and headers for API requests."""

    def __init__(self, storage_dir: str = "data"):
        self.storage_dir = storage_dir
        self.cookies_file = os.path.join(storage_dir, "cookies.json")
        self.headers_file = os.path.join(storage_dir, "headers.json")
        self._ensure_storage_dir()

    def _ensure_storage_dir(self) -> None:
        """Create storage directory if it doesn't exist."""
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)
            logger.info(f"Created storage directory: {self.storage_dir}")

    def save_cookies(self, cookies: List[Dict[str, Any]]) -> bool:
        """Save cookies to storage file.

        Args:
            cookies: List of cookie dictionaries from Playwright

        Returns:
            bool: True if saved successfully, False otherwise
        """
        try:
            with open(self.cookies_file, "w") as f:
                json.dump(cookies, f, indent=2)
            logger.info(f"Saved {len(cookies)} cookies to {self.cookies_file}")
            return True
        except Exception as e:
            logger.error(f"Failed to save cookies: {e}")
            return False

    def load_cookies(self) -> Optional[List[Dict[str, Any]]]:
        """Load cookies from storage file.

        Returns:
            List of cookie dictionaries or None if not found/invalid
        """
        try:
            if not os.path.exists(self.cookies_file):
                return None

            with open(self.cookies_file, "r") as f:
                cookies = json.load(f)

            logger.info(f"Loaded {len(cookies)} cookies from {self.cookies_file}")
            return cookies
        except Exception as e:
            logger.error(f"Failed to load cookies: {e}")
            return None

    def save_headers(self, headers: Dict[str, str]) -> bool:
        """Save headers to storage file.

        Args:
            headers: Dictionary of HTTP headers

        Returns:
            bool: True if saved successfully, False otherwise
        """
        try:
            with open(self.headers_file, "w") as f:
                json.dump(headers, f, indent=2)
            logger.info(f"Saved {len(headers)} headers to {self.headers_file}")
            return True
        except Exception as e:
            logger.error(f"Failed to save headers: {e}")
            return False

    def load_headers(self) -> Optional[Dict[str, str]]:
        """Load headers from storage file.

        Returns:
            Dictionary of headers or None if not found/invalid
        """
        try:
            if not os.path.exists(self.headers_file):
                return None

            with open(self.headers_file, "r") as f:
                headers = json.load(f)

            logger.info(f"Loaded {len(headers)} headers from {self.headers_file}")
            return headers
        except Exception as e:
            logger.error(f"Failed to load headers: {e}")
            return None

    def has_session_data(self) -> bool:
        """Check if both cookies and headers are available.

        Returns:
            bool: True if both cookies and headers files exist
        """
        return os.path.exists(self.cookies_file) and os.path.exists(self.headers_file)

    def clear_session_data(self) -> None:
        """Clear all saved session data."""
        try:
            if os.path.exists(self.cookies_file):
                os.remove(self.cookies_file)
                logger.info("Cleared cookies file")

            if os.path.exists(self.headers_file):
                os.remove(self.headers_file)
                logger.info("Cleared headers file")

        except Exception as e:
            logger.error(f"Failed to clear session data: {e}")


# Global instance
session_storage = SessionStorage()
