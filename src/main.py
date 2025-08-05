import requests
import sqlite3
import time
import config
from typing import List, Dict, Any, Tuple
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def init_db() -> None:
    """Initializes the database and creates the items table if it doesn't exist."""
    try:
        with sqlite3.connect(config.DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS items (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    quantity INTEGER,
                    available INTEGER -- 0 for false, 1 for true
                )
            ''')
            conn.commit()
            logging.info("Database initialized successfully.")
    except sqlite3.Error as e:
        logging.error(f"Database initialization failed: {e}")
        raise


def fetch_api_data() -> List[Dict[str, Any]]:
    """
     Fetches product data from the Amul API.

     Returns:
         A list of dictionaries, where each dictionary represents a product.

     Raises:
         requests.exceptions.RequestException: For connection errors or HTTP error status codes.
         KeyError: If the expected 'data' key is not in the JSON response.
     """

    logging.info("Fetching data from API...")
    response = requests.get(
        url=config.API_URL,
        cookies=config.API_COOKIES,
        headers=config.API_HEADERS,
    )
    # Raise an exception for 4xx or 5xx status codes
    response.raise_for_status()
    return response.json()['data']


def get_current_stock_status() -> Dict[str, int]:
    """
    Retrieves the current availability status of all items from the database.

    Returns:
        A dictionary mapping item ID to its availability status (1 for available, 0 for not).
    """
    try:
        with sqlite3.connect(config.DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, available FROM items")
            # Create a dictionary of {id: available_status}
            return {row[0]: row[1] for row in cur.fetchall()}
    except sqlite3.Error as e:
        logging.error(f"Failed to get current stock status from DB: {e}")
        return {}


def update_db_and_notify(new_items: List[Dict[str, Any]]) -> None:
    """
    Updates the database with new item data and sends notifications for state changes.
    Only notifies if an item changes from unavailable to available.
    """
    old_stock_status = get_current_stock_status()

    items_to_update: List[Tuple] = []

    for item in new_items:
        item_id = item['_id']
        name = item['name']
        quantity = item.get('inventory_quantity', 0)
        is_available = 1 if item.get('available', False) else 0

        items_to_update.append((item_id, name, quantity, is_available))

        # Check for notification condition
        # Item is newly available if its new status is 1 and old status was 0 or not present
        # Default to 0 (unavailable) if not in DB
        old_status = old_stock_status.get(item_id, 0)
        if is_available and not old_status:
            send_notification(name, quantity)

    # Batch update the database
    try:
        with sqlite3.connect(config.DB_PATH) as conn:
            cur = conn.cursor()
            cur.executemany('''
                INSERT INTO items (id, name, quantity, available)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    name=excluded.name,
                    quantity=excluded.quantity,
                    available=excluded.available
            ''', items_to_update)
            conn.commit()
            logging.info(
                f"Database updated with {len(items_to_update)} items.")
    except sqlite3.Error as e:
        logging.error(f"Database update failed: {e}")


def send_notification(name: str, quantity: int) -> None:
    """Sends a notification about an item being back in stock."""

    message = f"✅ BACK IN STOCK: {name} is now available!\n   Quantity: {quantity}"
    logging.info(message)

    # TODO use email/sms/soemthing else for notification
    print(message)


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
