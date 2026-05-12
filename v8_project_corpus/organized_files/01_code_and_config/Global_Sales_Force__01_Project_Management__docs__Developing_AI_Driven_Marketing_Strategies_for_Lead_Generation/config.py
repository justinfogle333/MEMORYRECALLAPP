"""
Review Agent Configuration
==========================
Fill in your API keys and customize settings below.
All other files import from this single config.
"""

import os

# ============================================================
# TWILIO SETTINGS
# Get these from: https://console.twilio.com
# ============================================================
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "YOUR_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "YOUR_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "+1234567890")

# ============================================================
# TREMENDOUS SETTINGS
# Get these from: https://developers.tremendous.com
# Sandbox URL: https://testflight.tremendous.com/api/v2
# Production URL: https://www.tremendous.com/api/v2
# ============================================================
TREMENDOUS_API_KEY = os.getenv("TREMENDOUS_API_KEY", "YOUR_TREMENDOUS_API_KEY")
TREMENDOUS_BASE_URL = os.getenv(
    "TREMENDOUS_BASE_URL",
    "https://testflight.tremendous.com/api/v2"  # Change to production URL when ready
)
TREMENDOUS_CAMPAIGN_ID = os.getenv("TREMENDOUS_CAMPAIGN_ID", "YOUR_CAMPAIGN_ID")
TREMENDOUS_FUNDING_SOURCE_ID = os.getenv("TREMENDOUS_FUNDING_SOURCE_ID", "YOUR_FUNDING_SOURCE_ID")

# ============================================================
# GIFT CARD SETTINGS
# ============================================================
GIFT_CARD_AMOUNT = 15  # USD
GIFT_CARD_CURRENCY = "USD"

# ============================================================
# TIMING SETTINGS
# ============================================================
SURVEY_DELAY_HOURS = 2      # Hours after move completion to send survey SMS
REVIEW_DELAY_HOURS = 24     # Hours after gift card delivery to send review ask
REMINDER_DELAY_HOURS = 72   # Hours after first SMS to send reminder (if no response)
MAX_REMINDERS = 1            # Maximum number of reminder SMS to send

# ============================================================
# DATABASE
# ============================================================
DATABASE_PATH = os.path.join(os.path.dirname(__file__), "review_agent.db")

# ============================================================
# CSV INBOX
# Drop your daily CRM export CSVs here
# ============================================================
CSV_INBOX_PATH = os.path.join(os.path.dirname(__file__), "csv_inbox")

# ============================================================
# LOGGING
# ============================================================
LOG_PATH = os.path.join(os.path.dirname(__file__), "logs", "review_agent.log")

# ============================================================
# WEBHOOK SERVER
# ============================================================
WEBHOOK_HOST = "0.0.0.0"
WEBHOOK_PORT = 8080
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "change_this_to_a_random_string")

# ============================================================
# GOOGLE BUSINESS PROFILE LINKS
# Map each brand to its Google review URL.
# To get the URL: Search for the business on Google Maps ->
# Click "Write a Review" -> Copy the URL from the browser.
# Format: https://search.google.com/local/writereview?placeid=PLACE_ID
# ============================================================
GBP_REVIEW_LINKS = {
    "Ultimate Movers": "https://search.google.com/local/writereview?placeid=PLACE_ID_HERE",
    "California Seattle Express": "https://search.google.com/local/writereview?placeid=PLACE_ID_HERE",
    "Cross Country Movers": "https://search.google.com/local/writereview?placeid=PLACE_ID_HERE",
    "Cross Country Moving Company": "https://search.google.com/local/writereview?placeid=PLACE_ID_HERE",
    "East Coast West Coast Movers": "https://search.google.com/local/writereview?placeid=PLACE_ID_HERE",
    "Flat Price Auto Transport": "https://search.google.com/local/writereview?placeid=PLACE_ID_HERE",
    "Kerb Moving": "https://search.google.com/local/writereview?placeid=PLACE_ID_HERE",
    "LD Movers": "https://search.google.com/local/writereview?placeid=PLACE_ID_HERE",
    "Long Distance Movers": "https://search.google.com/local/writereview?placeid=PLACE_ID_HERE",
    "Long Distance Moving Experts": "https://search.google.com/local/writereview?placeid=PLACE_ID_HERE",
    "Long Distance USA Movers": "https://search.google.com/local/writereview?placeid=PLACE_ID_HERE",
    "State 2 State Movers": "https://search.google.com/local/writereview?placeid=PLACE_ID_HERE",
    "Trico Long Distance Movers": "https://search.google.com/local/writereview?placeid=PLACE_ID_HERE",
    "USA Auto Transport": "https://search.google.com/local/writereview?placeid=PLACE_ID_HERE",
    "My International Movers": "https://search.google.com/local/writereview?placeid=PLACE_ID_HERE",
    "I Love Moving": "https://search.google.com/local/writereview?placeid=PLACE_ID_HERE",
    "Shepherd International": "https://search.google.com/local/writereview?placeid=PLACE_ID_HERE",
    "Sunset International": "https://search.google.com/local/writereview?placeid=PLACE_ID_HERE",
    "Schmidt International": "https://search.google.com/local/writereview?placeid=PLACE_ID_HERE",
}

# ============================================================
# SURVEY LINK
# Replace with your actual Google Form or Typeform URL.
# Append ?customer_id={id} so the webhook can identify who completed it.
# ============================================================
SURVEY_BASE_URL = "https://forms.gle/YOUR_FORM_ID_HERE"
