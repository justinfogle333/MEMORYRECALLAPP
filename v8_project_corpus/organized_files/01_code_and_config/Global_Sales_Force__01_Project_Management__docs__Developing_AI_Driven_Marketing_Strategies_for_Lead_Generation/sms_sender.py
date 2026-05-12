"""
SMS Sender Module
=================
Handles all outbound SMS via Twilio.
Includes the FTC-compliant message templates for all 3 SMS types.
"""

import logging
from twilio.rest import Client
from config import (
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_PHONE_NUMBER,
    SURVEY_BASE_URL,
    GBP_REVIEW_LINKS,
)

logger = logging.getLogger("review_agent")

# ============================================================
# Initialize Twilio Client
# ============================================================
_client = None


def _get_client():
    """Lazy-initialize the Twilio client."""
    global _client
    if _client is None:
        _client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    return _client


# ============================================================
# SMS TEMPLATES (FTC-Compliant)
# ============================================================

def _survey_message(customer_name, customer_id, brand):
    """
    Step 1: The Survey Ask.
    Incentive is tied to the SURVEY, not the review.
    This is FTC-compliant because the gift card is compensation
    for the customer's time completing the survey.
    """
    first_name = customer_name.split()[0] if customer_name else "there"
    survey_url = f"{SURVEY_BASE_URL}?cid={customer_id}&brand={brand.replace(' ', '+')}"

    return (
        f"Hi {first_name}! This is {brand}. "
        f"Thank you for choosing us for your move! "
        f"We'd love your feedback on a quick 60-second quality check "
        f"(3 questions). As a thank you, we'll send you a $15 Amazon Gift Card.\n\n"
        f"Take the survey here: {survey_url}\n\n"
        f"Reply STOP to opt out."
    )


def _review_ask_message(customer_name, brand):
    """
    Step 2: The Review Ask.
    Sent 24 hours AFTER the gift card was delivered.
    NO incentive is attached to this message — it's a separate,
    standalone request. This is the 'Decoupled Two-Step' that
    keeps us compliant with Google's review gating policy.
    """
    first_name = customer_name.split()[0] if customer_name else "there"
    review_link = GBP_REVIEW_LINKS.get(brand, "")

    return (
        f"Hi {first_name}, thanks again for your feedback! "
        f"If you have a moment, we'd really appreciate it if you "
        f"shared your experience on Google. It helps other families "
        f"find reliable movers.\n\n"
        f"{review_link}\n\n"
        f"Reply STOP to opt out."
    )


def _reminder_message(customer_name, customer_id, brand):
    """
    Reminder: Sent if the customer hasn't completed the survey
    after the configured reminder delay.
    """
    first_name = customer_name.split()[0] if customer_name else "there"
    survey_url = f"{SURVEY_BASE_URL}?cid={customer_id}&brand={brand.replace(' ', '+')}"

    return (
        f"Hi {first_name}, just a friendly reminder from {brand}! "
        f"Your $15 Amazon Gift Card is still waiting — just takes "
        f"60 seconds to complete our quick quality check.\n\n"
        f"Survey: {survey_url}\n\n"
        f"Reply STOP to opt out."
    )


# ============================================================
# SEND FUNCTIONS
# ============================================================

def send_survey_sms(customer_id, customer_name, phone, brand):
    """Send the Step 1 survey request SMS."""
    body = _survey_message(customer_name, customer_id, brand)
    return _send(phone, body, "survey_ask")


def send_review_ask_sms(customer_name, phone, brand):
    """Send the Step 2 review request SMS (no incentive)."""
    body = _review_ask_message(customer_name, brand)
    return _send(phone, body, "review_ask")


def send_reminder_sms(customer_id, customer_name, phone, brand):
    """Send a reminder SMS for the survey."""
    body = _reminder_message(customer_name, customer_id, brand)
    return _send(phone, body, "reminder")


def _send(to_phone, body, msg_type):
    """
    Send an SMS via Twilio. Returns the Twilio message SID on success,
    or None on failure.
    """
    try:
        client = _get_client()
        message = client.messages.create(
            body=body,
            from_=TWILIO_PHONE_NUMBER,
            to=to_phone,
        )
        logger.info("SMS sent [%s] to %s | SID: %s", msg_type, to_phone, message.sid)
        return message.sid
    except Exception as e:
        logger.error("SMS failed [%s] to %s | Error: %s", msg_type, to_phone, str(e))
        return None
