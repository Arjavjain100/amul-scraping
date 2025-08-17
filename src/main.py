import requests
from logger import default_logger as logger
import time
import config
from db import update_db_and_notify, init_db
from api import fetch_api_data


def run() -> None:
    """Main execution loop."""
    init_db()
    while True:
        try:
            api_data = fetch_api_data()
            if api_data:
                update_db_and_notify(api_data)
            else:
                logger.warning("API returned no data.")
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
        except KeyError:
            logger.error(
                "Could not find 'data' key in API response. Response format may have changed."
            )
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")

        logger.info(
            f"Waiting for {config.CHECK_INTERVAL_SECONDS} seconds before next check..."
        )
        time.sleep(config.CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    run()
