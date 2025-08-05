import logging
import requests
import time
import config
from db import update_db_and_notify, init_db
from api import fetch_api_data

# Setup basic logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def run() -> None:
    """Main execution loop."""
    init_db()
    while True:
        try:
            api_data = fetch_api_data()
            if api_data:
                update_db_and_notify(api_data)
            else:
                logging.warning("API returned no data.")
        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed: {e}")
        except KeyError:
            logging.error(
                "Could not find 'data' key in API response. Response format may have changed.")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")

        logging.info(
            f"Waiting for {config.CHECK_INTERVAL_SECONDS} seconds before next check...")
        time.sleep(config.CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    run()
