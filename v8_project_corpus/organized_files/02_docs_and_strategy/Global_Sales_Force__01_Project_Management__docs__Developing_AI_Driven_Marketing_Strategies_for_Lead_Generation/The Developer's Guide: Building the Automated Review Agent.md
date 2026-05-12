# The Developer's Guide: Building the Automated Review Agent

**For:** Justin (Lead Developer)**Goal:** Build the Automated Review Solicitation Agent for Global Sales Force**Constraint:** Maximize cost efficiency and minimize token usage.

This guide is written specifically for you to build the agent yourself. Because you want to keep costs and token usage as low as possible, we are going to bypass expensive orchestration tools like Zapier ($30-$100/mo) and Make.com, and we are **not** going to use an LLM for this. This is a rules-based workflow, so a simple Python script running on a cheap VPS (or even a local machine) is the most cost-effective solution.

---

## The Tech Stack (Cost-Optimized)

| Component | Tool | Cost |
| --- | --- | --- |
| **Logic & Orchestration** | Python 3.11 | Free |
| **Database** | SQLite (Local file) | Free |
| **SMS Delivery** | Twilio API | ~$0.008 per message |
| **Gift Card Fulfillment** | Tremendous API | Free API (pay only for the $15 gift cards) |
| **CRM Integration** | CSV Export / Selenium | Free |

**Total Monthly Software Cost:** ~$0.016 per customer (for 2 SMS messages).

---

## Step 1: The CRM Integration Challenge

I investigated `app.ultimatemoving.us`. This is a proprietary CRM ("UM - Ultimate Moving") and it does not have public API documentation or standard webhook integrations available out-of-the-box.

Since you are building this yourself, you have two options to get the "Completed Moves" data out of the CRM and into your Python script:

**Option A: The CSV Export Method (Easiest)**

1. Every day, export a CSV from the CRM of all moves marked "Completed" that day.

1. The CSV needs 4 columns: `Customer Name`, `Phone Number`, `Brand Name`, `Location ID`.

1. Drop this CSV into a specific folder on your computer.

1. Your Python script runs daily, reads the CSV, and triggers the workflow.

**Option B: The Browser Automation Method (Fully Automated)**

1. Write a Python script using `Selenium` or `Playwright`.

1. The script logs into `app.ultimatemoving.us` using your credentials.

1. It navigates to the "Completed Jobs" view, scrapes the customer data, and saves it to your local SQLite database.

*Recommendation: Start with Option A to get the system working and generating ROI immediately. Once it's proving its value, build Option B.*

---

## Step 2: Setting Up the Infrastructure

### 1. Twilio Setup

1. Create a Twilio account at twilio.com.

1. Buy a phone number (approx $1/month). If you want to be perfect, buy one number for each of the 19 brands so the area codes match, but to start, one number is fine.

1. Get your `Account SID` and `Auth Token` from the Twilio console.

1. Install the Python library: `pip install twilio`

### 2. Tremendous Setup

1. Create a free developer account at developers.tremendous.com.

1. Generate a Sandbox API Key.

1. Create a "Campaign" in Tremendous. This campaign will hold the email template that delivers the $15 Amazon Gift Card.

1. Note your `Campaign ID`.

1. Install the Python library: `pip install tremendous`

---

## Step 3: The Python Architecture

You will need to build a Python application with three main components.

### Component 1: The Database (`database.py`)

Use SQLite to track where each customer is in the flow. You need one table: `customers`.Columns: `id`, `name`, `phone`, `brand`, `location_id`, `status` (values: 'new', 'survey_sent', 'survey_completed', 'review_ask_sent'), `timestamp`.

### Component 2: The Webhook Listener (`server.py`)

You need a simple web server to catch the webhook when a customer finishes the survey. Use `FastAPI` or `Flask`.

1. Customer clicks the link in the first SMS and goes to a Typeform or Google Form.

1. They fill out the 3-question survey.

1. The form sends a webhook to your `server.py`.

1. `server.py` updates the database status to `survey_completed` and immediately calls the Tremendous API to send the gift card.

### Component 3: The Cron Job (`worker.py`)

This script runs every hour (using Linux `cron` or Windows Task Scheduler).

1. **Check for 'new' customers:** If a customer is 'new', send SMS Template 1 (The Survey Ask) via Twilio. Update status to `survey_sent`.

1. **Check for 'survey_completed' customers:** If a customer completed the survey exactly 24 hours ago, send SMS Template 3 (The Google Review Ask) via Twilio. Update status to `review_ask_sent`.

---

## Step 4: The Code Snippets

Here is the core logic you need to write.

### Sending the Twilio SMS (Python)

```python
from twilio.rest import Client

def send_sms(phone_number, message_body):
    account_sid = 'your_account_sid'
    auth_token = 'your_auth_token'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=message_body,
        from_='+1234567890', # Your Twilio number
        to=phone_number
    )
    return message.sid
```

### Sending the Tremendous Gift Card (Python)

```python
import requests

def send_gift_card(customer_name, customer_email, campaign_id):
    url = "https://testflight.tremendous.com/api/v2/orders"
    headers = {
        "Authorization": "Bearer YOUR_SANDBOX_API_KEY",
        "Content-Type": "application/json"
    }
    payload = {
        "payment": {"funding_source_id": "YOUR_FUNDING_SOURCE_ID"},
        "reward": {
            "campaign_id": campaign_id,
            "delivery": {"method": "EMAIL"},
            "recipient": {
                "name": customer_name,
                "email": customer_email
            },
            "value": {"denomination": 15, "currency_code": "USD"}
        }
    }
    response = requests.post(url, json=payload, headers=headers )
    return response.json()
```

---

## Step 5: The Execution Plan for This Week

1. **Today:** Set up Twilio and Tremendous sandbox accounts. Get your API keys.

1. **Tomorrow:** Write the SQLite database schema and the `worker.py` script to send the Twilio SMS. Test it on your own phone number.

1. **Day 3:** Set up a free Google Form or Typeform for the survey. Connect its webhook to a simple Python Flask server (`server.py`).

1. **Day 4:** Write the Tremendous API integration inside `server.py` so it fires when the webhook is received.

1. **Day 5:** Export a CSV of 5 real (but friendly) past customers from `app.ultimatemoving.us` and run them through the system live.

By building this in Python yourself, you avoid all monthly SaaS fees (Zapier/Make) and you don't use any LLM tokens because the logic is entirely rules-based. It is the ultimate cost-effective solution.

