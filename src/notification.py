from logger import default_logger as logger


def send_notification(name: str, quantity: int) -> None:
    """Sends a notification about an item being back in stock."""

    message = f"✅ BACK IN STOCK: {name} is now available!\n   Quantity: {quantity}"
    logger.info(message)

    # TODO use email/sms/soemthing else for notification
