# Email Notification Setup

This guide will help you set up email notifications for the Amul scraping system.

## Quick Setup

1. **Copy the environment template:**
   ```bash
   cp .env.example .env
   ```

2. **Edit the `.env` file with your email credentials:**
   ```env
   EMAIL_FROM=your-email@gmail.com
   EMAIL_PASSWORD=your-app-password
   EMAIL_TO=recipient1@email.com,recipient2@email.com
   ```

3. **For Gmail users (recommended):**
   - Enable 2-Factor Authentication on your Google account
   - Generate an App Password: https://support.google.com/accounts/answer/185833
   - Use the App Password in the `EMAIL_PASSWORD` field (not your regular password)

## Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `EMAIL_ENABLED` | Enable/disable email notifications | `True` |
| `SMTP_SERVER` | SMTP server address | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP server port | `587` |
| `EMAIL_FROM` | Your email address | Required |
| `EMAIL_PASSWORD` | Your email password/app password | Required |
| `EMAIL_TO` | Recipient emails (comma-separated) | Required |
| `EMAIL_SUBJECT` | Email subject line | `Amul Product Back in Stock Alert` |


## Testing Email Notifications

You can test the email functionality by running a simple test:

```python
from src.notification import send_notification

# Test email notification
send_notification("Test Product", 5)
```

## Troubleshooting

### Common Issues

1. **Authentication Error:**
   - For Gmail: Make sure you're using an App Password, not your regular password
   - Enable 2FA and generate an App Password from your Google Account settings

2. **Connection Refused:**
   - Check if the SMTP server and port are correct
   - Some networks block outgoing SMTP connections

3. **No Recipients:**
   - Make sure `EMAIL_TO` contains valid email addresses
   - Multiple recipients should be comma-separated

4. **Email Not Received:**
   - Check spam/junk folders
   - Verify recipient email addresses are correct
   - Check the logs for any error messages

## Disabling Email Notifications

To disable email notifications without removing the configuration:

```env
EMAIL_ENABLED=False
```

Or set `EMAIL_ENABLED = False` directly in `src/config.py`.
