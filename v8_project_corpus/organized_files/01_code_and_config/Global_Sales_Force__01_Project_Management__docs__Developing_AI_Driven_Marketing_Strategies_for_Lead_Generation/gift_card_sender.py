"""
Gift Card Sender Module
=======================
Handles automated $15 Amazon Gift Card delivery via the Tremendous API.
"""

import logging
import requests
from config import (
    TREMENDOUS_API_KEY,
    TREMENDOUS_BASE_URL,
    TREMENDOUS_CAMPAIGN_ID,
    TREMENDOUS_FUNDING_SOURCE_ID,
    GIFT_CARD_AMOUNT,
    GIFT_CARD_CURRENCY,
)

logger = logging.getLogger("review_agent")


def send_gift_card(customer_name, customer_email, brand):
    """
    Send a $15 Amazon Gift Card via the Tremendous API.

    Returns a dict with 'success' (bool), 'order_id' (str or None),
    and 'error' (str or None).
    """
    url = f"{TREMENDOUS_BASE_URL}/orders"
    headers = {
        "Authorization": f"Bearer {TREMENDOUS_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "payment": {
            "funding_source_id": TREMENDOUS_FUNDING_SOURCE_ID,
        },
        "rewards": [
            {
                "campaign_id": TREMENDOUS_CAMPAIGN_ID,
                "delivery": {
                    "method": "EMAIL",
                },
                "recipient": {
                    "name": customer_name,
                    "email": customer_email,
                },
                "value": {
                    "denomination": GIFT_CARD_AMOUNT,
                    "currency_code": GIFT_CARD_CURRENCY,
                },
            }
        ],
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)

        if response.status_code in (200, 201):
            data = response.json()
            order_id = data.get("order", {}).get("id", "unknown")
            logger.info(
                "Gift card sent to %s (%s) for %s | Order: %s",
                customer_name, customer_email, brand, order_id,
            )
            return {"success": True, "order_id": order_id, "error": None}
        else:
            error_msg = f"HTTP {response.status_code}: {response.text}"
            logger.error(
                "Gift card FAILED for %s (%s) | %s",
                customer_name, customer_email, error_msg,
            )
            return {"success": False, "order_id": None, "error": error_msg}

    except requests.exceptions.RequestException as e:
        error_msg = str(e)
        logger.error(
            "Gift card REQUEST FAILED for %s (%s) | %s",
            customer_name, customer_email, error_msg,
        )
        return {"success": False, "order_id": None, "error": error_msg}


def check_balance():
    """
    Check the current Tremendous account balance.
    Useful for monitoring gift card budget.
    """
    url = f"{TREMENDOUS_BASE_URL}/funding_sources"
    headers = {
        "Authorization": f"Bearer {TREMENDOUS_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            sources = data.get("funding_sources", [])
            for source in sources:
                meta = source.get("meta", {})
                balance = meta.get("available_cents", 0) / 100
                logger.info("Tremendous balance: $%.2f", balance)
                return balance
        return None
    except requests.exceptions.RequestException as e:
        logger.error("Balance check failed: %s", str(e))
        return None
