import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from logger import default_logger as logger
from config import (
    EMAIL_ENABLED,
    SMTP_SERVER,
    SMTP_PORT,
    EMAIL_FROM,
    EMAIL_PASSWORD,
    EMAIL_TO,
    EMAIL_SUBJECT,
)


def send_email(subject: str, body: str, to_emails: list[str]) -> bool:
    """Sends an email notification.

    Args:
        subject: Email subject
        body: Email body content
        to_emails: List of recipient email addresses

    Returns:
        bool: True if email sent successfully, False otherwise
    """
    if not EMAIL_FROM or not EMAIL_PASSWORD:
        logger.warning(
            "Email credentials not configured. Please set EMAIL_FROM and EMAIL_PASSWORD in config.py"
        )
        return False

    if not to_emails:
        logger.warning(
            "No recipient email addresses configured. Please set EMAIL_TO in config.py"
        )
        return False

    try:
        # Create message
        msg = MIMEMultipart()
        msg["From"] = EMAIL_FROM
        msg["To"] = ", ".join(to_emails)
        msg["Subject"] = subject

        # Add body to email
        msg.attach(MIMEText(body, "plain"))

        # Create SMTP session
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Enable security
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.send_message(msg)

        logger.info(f"Email notification sent successfully to {', '.join(to_emails)}")
        return True

    except Exception as e:
        logger.error(f"Failed to send email notification: {str(e)}")
        return False


def send_notification(name: str, quantity: int) -> None:
    """Sends a notification about an item being back in stock.

    Args:
        name: Product name
        quantity: Available quantity
    """
    message = f"✅ BACK IN STOCK: {name} is now available!\n   Quantity: {quantity}"
    logger.info(message)

    # Send email notification if enabled
    if EMAIL_ENABLED:
        email_body = f"""Good news!

The product "{name}" is now back in stock on Amul's website.

Details:
• Product: {name}
• Available Quantity: {quantity}

Don't miss out - get it while it's available!

This is an automated notification from your Amul stock monitoring system.
        """

        success = send_email(
            subject=f"{name} {EMAIL_SUBJECT}", body=email_body, to_emails=EMAIL_TO
        )

        if not success:
            logger.warning("Email notification failed - check email configuration")
    else:
        logger.info("Email notifications are disabled")


def send_consolidated_notification(items: list[dict]) -> None:
    """Sends a consolidated notification about multiple items being back in stock.

    Args:
        items: List of dictionaries with 'name' and 'quantity' keys for each item
    """
    if not items:
        return

    # Log all items individually
    for item in items:
        message = f"✅ BACK IN STOCK: {item['name']} is now available!\n   Quantity: {item['quantity']}"
        logger.info(message)

    # Send consolidated email notification if enabled
    if EMAIL_ENABLED:
        if len(items) == 1:
            # If only one item, use the original single-item format
            item = items[0]
            email_body = f"""Good news!

The product "{item["name"]}" is now back in stock on Amul's website.

Details:
• Product: {item["name"]}
• Available Quantity: {item["quantity"]}

Don't miss out - get it while it's available!

This is an automated notification from your Amul stock monitoring system.
            """
            subject = f"{item['name']} {EMAIL_SUBJECT}"
        else:
            # Multiple items - create consolidated notification
            item_list = "\n".join(
                [f"• {item['name']} (Quantity: {item['quantity']})" for item in items]
            )
            total_items = len(items)

            email_body = f"""Great news!

{total_items} products are now back in stock on Amul's website:

{item_list}

Don't miss out - get them while they're available!

This is an automated notification from your Amul stock monitoring system.
            """
            subject = f"{total_items} Products {EMAIL_SUBJECT}"

        success = send_email(subject=subject, body=email_body, to_emails=EMAIL_TO)

        if not success:
            logger.warning(
                "Consolidated email notification failed - check email configuration"
            )
    else:
        logger.info("Email notifications are disabled")
