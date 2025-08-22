from playwright.sync_api import sync_playwright
from typing import List, Dict, Any
import config
import random
import time
from logger import default_logger as logger


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

        # Add short delay for late responses
        time.sleep(random.uniform(2, 4))

        logger.info(f"Page loaded: {page.title()}")
        browser.close()

    if response_data:
        logger.info(f"Scraping completed successfully for {pincode}")
    else:
        logger.warning(f"No data captured for {pincode}")

    return response_data
