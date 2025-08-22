from playwright.sync_api import sync_playwright
from typing import List, Dict, Any
import config
from logger import default_logger as logger


def scrape_amul_data(pincode: str) -> List[Dict[str, Any]]:
    """Scrape Amul product data and return the response data.

    Args:
        pincode (str): The pincode to use for location-based filtering

    Returns:
        dict: The API response data containing product information
    """
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
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36",
            extra_http_headers={
                "Accept-Language": "en-US,en;q=0.9",
            },
        )
        page = context.new_page()

        def handle_response(response):
            nonlocal response_data
            if config.API_URL == response.url:
                try:
                    response_data = response.json()["data"]
                    logger.info(
                        f"Successfully captured API response with {len(response_data) if response_data else 0} items"
                    )
                except Exception as e:
                    logger.error(f"Error parsing API response: {e}")

        page.on("response", handle_response)

        page.goto(
            "https://shop.amul.com/en/browse/protein", wait_until="domcontentloaded"
        )

        # Fill inputs
        page.get_by_placeholder("Enter Your Pincode").fill(pincode)

        # Click submit button
        page.get_by_role("button", name=pincode).click()

        # Wait until navigation completes
        page.wait_for_load_state("networkidle")

        logger.info(f"Successfully loaded page: {page.title()}")
        browser.close()

    if response_data:
        logger.info(f"Scraping completed successfully for pincode {pincode}")
    else:
        logger.warning(f"No data captured during scraping for pincode {pincode}")

    return response_data
