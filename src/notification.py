import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def send_notification(name: str, quantity: int) -> None:
    """Sends a notification about an item being back in stock."""

    message = f"✅ BACK IN STOCK: {name} is now available!\n   Quantity: {quantity}"
    logging.info(message)

    # TODO use email/sms/soemthing else for notification
