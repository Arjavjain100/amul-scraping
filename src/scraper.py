from playwright.sync_api import sync_playwright
from typing import List, Dict, Any
import config
import random
import time
from logger import default_logger as logger
from session_storage import session_storage
from api_client import api_client


def scrape_amul_data(pincode: str) -> List[Dict[str, Any]]:
    """Scrape Amul product data and return the response data."""

    logger.info(f"Starting scrape for pincode: {pincode}")
    response_data = None

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ],
        )

        context = browser.new_context(
            user_agent=random.choice(
                [
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
                ]
            ),
            locale="en-US",
            timezone_id="Asia/Kolkata",
            viewport={"width": 1366, "height": 768},
            extra_http_headers={"Accept-Language": "en-US,en;q=0.9"},
        )
        page = context.new_page()

        def handle_response(response):
            nonlocal response_data
            if config.API_URL in response.url:
                try:
                    response_data = response.json().get("data", [])
                    logger.info(
                        f"Captured API response with {len(response_data)} items"
                    )
                    # Save session data (headers) for future API calls
                    if len(response_data) > 0:
                        try:
                            # Get headers from the last successful request
                            headers = response.headers

                            # Save headers data
                            session_storage.save_headers(headers)
                            logger.info(
                                "Session header data saved successfully for future API calls"
                            )

                        except Exception as e:
                            logger.error(
                                f"Failed to save session header data: {e}")

                except Exception as e:
                    logger.error(f"Error parsing API response: {e}")

        page.on("response", handle_response)

        # Go to products page
        page.goto(
            "https://shop.amul.com/en/browse/protein", wait_until="domcontentloaded"
        )

        # Fill pincode and submit
        page.get_by_placeholder("Enter Your Pincode").fill(pincode)
        time.sleep(random.uniform(1.5, 3.0))
        page.get_by_role("button", name=pincode).click()

        # Explicitly wait for API response
        try:
            page.wait_for_response(
                lambda r: config.API_URL in r.url, timeout=15000)
        except Exception:
            logger.warning("Did not receive API response in time")

        try:
            # Get cookies from the browser context
            cookies = context.cookies()
            # Save cookies
            session_storage.save_cookies(cookies)
            logger.info(
                "Session cookies saved successfully for future API calls")

        except Exception as e:
            logger.error(f"Failed to save cookies session data: {e}")

        # Add short delay for late responses
        time.sleep(random.uniform(2, 4))

        logger.info(f"Page loaded: {page.title()}")
        page.close()
        context.close()
        browser.close()

    if response_data:
        logger.info(f"Scraping completed successfully for {pincode}")
    else:
        logger.warning(f"No data captured for {pincode}")

    return response_data


def get_amul_data(pincode: str) -> List[Dict[str, Any]]:
    """Enhanced function that tries API call first, falls back to full scraping.

    Args:
        pincode: The pincode to filter products for

    Returns:
        List of product dictionaries
    """
    logger.info(f"Getting Amul data for pincode: {pincode}")

    # First, try to use saved session data for direct API call
    if session_storage.has_session_data():
        logger.info("Attempting direct API call with saved session data")

        # Validate session before using it
        if api_client.validate_session():
            # Try direct API call
            api_data = api_client.fetch_products(pincode)
            if api_data:
                return api_data
            else:
                logger.warning("Direct API call failed, clearing session data")
                session_storage.clear_session_data()
        else:
            logger.warning("Session validation failed, clearing session data")
            session_storage.clear_session_data()
    else:
        logger.info("No saved session data available")

    # If API call failed or no session data, fall back to full scraping
    logger.info("Falling back to full website scraping")
    scraped_data = scrape_amul_data(pincode)

    if scraped_data:
        logger.info(
            f"Full scraping successful - retrieved {len(scraped_data)} products"
        )
        return scraped_data
    else:
        logger.error("Both API call and full scraping failed")
        return []
