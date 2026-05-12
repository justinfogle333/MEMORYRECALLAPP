# Review Agent — Automated Review Solicitation System

## What This Does

This agent automates the "Decoupled Two-Step" review solicitation flow for all 19 Global Sales Force brands across 100+ Google Business Profile locations:

1. **Step 1 (Survey + Gift Card):** Texts the customer a $15 Amazon Gift Card offer for completing a 60-second quality survey.
2. **Step 2 (Review Ask):** 24 hours later, sends a separate text asking them to share their experience on Google — with NO incentive attached.

This is FTC-compliant and Google-compliant because the gift card is tied to the survey, not the review.

---

## File Structure

```
review_agent/
├── config.py              # All settings, API keys, brand mappings
├── database.py            # SQLite database (customers, SMS log, gift cards)
├── sms_sender.py          # Twilio SMS sender with FTC-compliant templates
├── gift_card_sender.py    # Tremendous API gift card delivery
├── csv_importer.py        # Imports completed-move CSVs from CRM
├── server.py              # Flask webhook server (survey completion + dashboard)
├── worker.py              # Cron job that processes the queue every hour
├── test_agent.py          # Full test suite (19 tests)
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variable template
├── csv_inbox/             # Drop your CRM export CSVs here
│   └── sample_completed_moves.csv
├── templates/
│   └── google_apps_script.js  # Google Forms webhook script
└── logs/                  # Worker and server logs
```

---

## Quick Start (5 Steps)

### Step 1: Set Up Accounts (30 minutes)

**Twilio (SMS):**
1. Go to [twilio.com](https://www.twilio.com) and create a free trial account
2. Get a phone number from the Twilio console
3. Copy your Account SID, Auth Token, and Phone Number
4. Cost: ~$0.0079 per SMS (less than 1 cent)

**Tremendous (Gift Cards):**
1. Go to [tremendous.com](https://www.tremendous.com) and create an account
2. Go to Settings → API Keys → Create a new key
3. Start with the **Sandbox** (testflight.tremendous.com) for testing
4. Create a Campaign (Settings → Campaigns) and note the Campaign ID
5. Note your Funding Source ID from Settings → Funding Sources
6. Cost: You only pay face value ($15 per card) + no platform fee

### Step 2: Configure the Agent (10 minutes)

```bash
cd review_agent

# Copy the environment template
cp .env.example .env

# Edit .env with your actual API keys
nano .env
```

Fill in all the values in `.env`, then load them:

```bash
export $(cat .env | xargs)
```

**Or** edit `config.py` directly and replace the placeholder values.

### Step 3: Set Up the Google Form Survey (20 minutes)

1. Create a Google Form with 3 questions:
   - "How would you rate your overall moving experience?" (1-5 stars)
   - "What did we do well?" (Short answer)
   - "What could we improve?" (Short answer)
   - Add a hidden field for `customer_id` (Short answer, pre-filled via URL)

2. Open the Form's Script Editor (three dots → Script Editor)
3. Paste the contents of `templates/google_apps_script.js`
4. Replace `YOUR_SERVER_URL` with your actual server URL
5. Set up a trigger: Run → onFormSubmit → On form submit

### Step 4: Install and Test (10 minutes)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the test suite (should show ALL 19 TESTS PASSED)
python test_agent.py

# Test the worker with the sample CSV
python worker.py

# Start the webhook server
python server.py
```

Check the dashboard at: `http://localhost:8080/dashboard`

### Step 5: Set Up the Cron Job (5 minutes)

```bash
# Open crontab
crontab -e

# Add this line to run the worker every hour:
0 * * * * cd /path/to/review_agent && /usr/bin/python3 worker.py >> logs/cron.log 2>&1
```

---

## Daily Usage

### Adding New Customers

**Option A: CSV Drop (Manual)**
1. Export completed moves from `app.ultimatemoving.us`
2. Save as CSV with columns: `customer_name`, `phone`, `email`, `brand`, `location_id`
3. Drop the CSV into the `csv_inbox/` folder
4. The worker will pick it up on the next hourly run

**Option B: Manual Worker Run**
```bash
cd review_agent && python worker.py
```

### Monitoring

- **Dashboard:** `http://your-server:8080/dashboard`
- **Logs:** `logs/review_agent.log`
- **Database:** `review_agent.db` (open with any SQLite viewer)

### Checking Gift Card Budget

```python
from gift_card_sender import check_balance
print(f"Balance: ${check_balance():.2f}")
```

---

## Google Business Profile Links

Before going live, you MUST fill in the GBP review links in `config.py` for each brand. To get the link:

1. Search for the business on Google Maps
2. Click "Write a Review"
3. Copy the URL from the browser bar
4. Paste it into the `GBP_REVIEW_LINKS` dictionary in `config.py`

---

## Cost Breakdown

| Item | Cost | Notes |
|------|------|-------|
| Twilio SMS | ~$0.008/msg | ~$0.016 per customer (2 messages) |
| Tremendous | $0 platform fee | You only pay the $15 gift card face value |
| Gift Cards | $15/customer | Only for customers who complete the survey |
| Server | $5-10/mo | Any VPS (DigitalOcean, Linode, etc.) |
| **Per Customer Total** | **~$15.02** | If they complete the survey |

At 50 surveys/month: ~$750/mo in gift cards + ~$1 in SMS = ~$751/mo total.

---

## Switching to Production

When you're ready to go live with real gift cards:

1. In `config.py` or `.env`, change `TREMENDOUS_BASE_URL` from:
   `https://testflight.tremendous.com/api/v2`
   to:
   `https://www.tremendous.com/api/v2`

2. Fund your Tremendous account with real money

3. Use your production API key instead of the sandbox key

4. Test with ONE real customer first before scaling

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| SMS not sending | Check Twilio console for errors. Verify phone number format (+1XXXXXXXXXX) |
| Gift card not sending | Check Tremendous dashboard. Verify Campaign ID and Funding Source ID |
| CSV not importing | Check column headers match expected names (see csv_importer.py) |
| Survey webhook not firing | Check Google Apps Script execution log. Verify server URL is correct |
| Worker not running | Check cron log: `tail -f logs/cron.log` |
