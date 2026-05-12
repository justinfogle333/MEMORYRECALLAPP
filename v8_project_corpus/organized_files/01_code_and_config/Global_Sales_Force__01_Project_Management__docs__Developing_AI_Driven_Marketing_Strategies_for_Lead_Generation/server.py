"""
Webhook Server
==============
A lightweight Flask server that handles:
1. Survey completion webhooks (from Google Forms / Typeform)
2. Twilio inbound SMS webhooks (for STOP opt-outs)
3. A simple dashboard endpoint to check system status

Run with: python server.py
"""

import logging
import hashlib
import hmac
from datetime import datetime
from flask import Flask, request, jsonify
from config import WEBHOOK_HOST, WEBHOOK_PORT, WEBHOOK_SECRET
from database import (
    init_db,
    update_status,
    get_customer_by_id,
    get_customer_by_phone,
    log_gift_card,
    get_stats,
)
from gift_card_sender import send_gift_card, check_balance

# ============================================================
# Setup
# ============================================================
app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("review_agent")


# ============================================================
# Route 1: Survey Completion Webhook
# ============================================================
@app.route("/webhook/survey-complete", methods=["POST"])
def survey_complete():
    """
    Called when a customer completes the survey.

    Expects JSON body with:
    {
        "customer_id": 123,
        "email": "customer@email.com"  (optional, for gift card delivery)
    }

    If using Google Forms, you'll need a Google Apps Script to
    POST to this endpoint on form submission. See the README.

    If using Typeform, configure a webhook in Typeform settings
    pointing to this URL.
    """
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "No JSON body received"}), 400

    customer_id = data.get("customer_id")
    email = data.get("email", "")

    if not customer_id:
        return jsonify({"error": "customer_id is required"}), 400

    # Look up the customer
    customer = get_customer_by_id(int(customer_id))
    if not customer:
        return jsonify({"error": f"Customer #{customer_id} not found"}), 404

    if customer["status"] not in ("survey_sent", "new"):
        return jsonify({
            "message": f"Customer #{customer_id} already at status: {customer['status']}"
        }), 200

    # Update status to survey_completed
    now = datetime.utcnow().isoformat()
    update_status(
        customer["id"],
        "survey_completed",
        survey_completed_at=now,
    )

    # If we have an email, send the gift card immediately
    gift_card_email = email or customer["email"]
    if gift_card_email:
        result = send_gift_card(customer["name"], gift_card_email, customer["brand"])

        if result["success"]:
            update_status(
                customer["id"],
                "gift_card_sent",
                gift_card_sent_at=datetime.utcnow().isoformat(),
                gift_card_order_id=result["order_id"],
            )
            log_gift_card(customer["id"], result["order_id"], 15.0, "sent")
            logger.info("Gift card sent to customer #%d", customer["id"])
        else:
            log_gift_card(customer["id"], None, 15.0, f"failed: {result['error']}")
            logger.error("Gift card failed for customer #%d: %s", customer["id"], result["error"])

        return jsonify({
            "message": "Survey recorded and gift card sent",
            "customer_id": customer["id"],
            "gift_card_status": "sent" if result["success"] else "failed",
        }), 200
    else:
        logger.warning("No email for customer #%d — gift card not sent", customer["id"])
        return jsonify({
            "message": "Survey recorded but no email — gift card pending",
            "customer_id": customer["id"],
        }), 200


# ============================================================
# Route 2: Twilio Inbound SMS (Opt-Out Handling)
# ============================================================
@app.route("/webhook/twilio-inbound", methods=["POST"])
def twilio_inbound():
    """
    Handles inbound SMS from Twilio.
    Primarily used to process STOP opt-out requests.
    Twilio handles STOP automatically, but we log it here too.
    """
    from_number = request.form.get("From", "")
    body = request.form.get("Body", "").strip().upper()

    logger.info("Inbound SMS from %s: %s", from_number, body)

    if body in ("STOP", "UNSUBSCRIBE", "CANCEL", "QUIT"):
        customer = get_customer_by_phone(from_number)
        if customer:
            update_status(customer["id"], "opted_out")
            logger.info("Customer #%d opted out", customer["id"])

    # Twilio expects a 200 response (or TwiML)
    return "<Response></Response>", 200, {"Content-Type": "text/xml"}


# ============================================================
# Route 3: Dashboard (Status Check)
# ============================================================
@app.route("/dashboard", methods=["GET"])
def dashboard():
    """
    Simple JSON dashboard showing system stats.
    Access at: http://your-server:8080/dashboard
    """
    stats = get_stats()
    balance = check_balance()

    return jsonify({
        "review_agent_status": "running",
        "customers": stats,
        "tremendous_balance": f"${balance:.2f}" if balance is not None else "unavailable",
        "timestamp": datetime.utcnow().isoformat(),
    })


# ============================================================
# Route 4: Health Check
# ============================================================
@app.route("/health", methods=["GET"])
def health():
    """Simple health check endpoint."""
    return jsonify({"status": "ok"}), 200


# ============================================================
# Run
# ============================================================
if __name__ == "__main__":
    init_db()
    logger.info("Starting Review Agent webhook server on %s:%d", WEBHOOK_HOST, WEBHOOK_PORT)
    app.run(host=WEBHOOK_HOST, port=WEBHOOK_PORT, debug=False)
