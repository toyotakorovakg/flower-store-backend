"""
Email service placeholder.

In a real implementation, this module would integrate with an SMTP server
or third-party email provider to send transactional emails such as
password resets or order confirmations. For the purposes of this example,
emails are simply logged to standard output.
"""

from __future__ import annotations

import logging


async def send_email(to: str, subject: str, body: str) -> None:
    """Send an email.

    This dummy implementation logs the email parameters. Replace with
    actual email-sending logic in production.
    """
    logging.info("Sending email to %s: %s\n%s", to, subject, body)
