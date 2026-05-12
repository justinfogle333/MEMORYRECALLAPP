# SAVED TASK: 5-Day Review Agent Build Plan

**Project:** Global Sales Force — Automated Review Solicitation Agent
**Priority:** #1 (Alex's top priority from meeting)
**Status:** Code complete, ready for deployment
**Application Location:** `/home/ubuntu/review_agent/` (also packaged as `review_agent.zip`)

---

## Day 1: Account Setup & Verification

- [ ] Download and unzip `review_agent.zip`
- [ ] Sign up at [twilio.com](https://www.twilio.com)
  - [ ] Get a phone number from the Twilio console
  - [ ] Copy your Account SID
  - [ ] Copy your Auth Token
  - [ ] Note the phone number (format: +1XXXXXXXXXX)
- [ ] Sign up at [tremendous.com](https://www.tremendous.com)
  - [ ] Get an API key (Settings → API Keys)
  - [ ] Create a Campaign (Settings → Campaigns) — note the Campaign ID
  - [ ] Note your Funding Source ID (Settings → Funding Sources)
  - [ ] Start with Sandbox mode (testflight.tremendous.com) for testing
- [ ] Copy `.env.example` to `.env` and fill in all API keys
- [ ] Run `python test_agent.py` — confirm **ALL 19 TESTS PASSED**

**Day 1 Outcome:** All accounts created, API keys configured, tests passing.

---

## Day 2: Google Form Survey Setup

- [ ] Create a Google Form with 3 questions:
  - [ ] "How would you rate your overall moving experience?" (1-5 stars)
  - [ ] "What did we do well?" (Short answer)
  - [ ] "What could we improve?" (Short answer)
  - [ ] Add a hidden field for `customer_id` (Short answer, pre-filled via URL)
- [ ] Open the Form's Script Editor (three dots → Script Editor)
- [ ] Paste the contents of `templates/google_apps_script.js`
- [ ] Replace `YOUR_SERVER_URL` with your actual server URL
- [ ] Set up a trigger: Run → onFormSubmit → On form submit
- [ ] Test the webhook by submitting the form yourself
- [ ] Verify the webhook hits your server (check logs)

**Day 2 Outcome:** Survey form live, webhook connected to the agent.

---

## Day 3: GBP Links & Server Launch

- [ ] Fill in the GBP review links in `config.py` for each brand:
  - [ ] Search each business on Google Maps
  - [ ] Click "Write a Review"
  - [ ] Copy the URL from the browser bar
  - [ ] Paste into the `GBP_REVIEW_LINKS` dictionary in `config.py`
  - [ ] Repeat for all 19 brands (prioritize the top 5-6 brands first)
- [ ] Start the Flask server: `python server.py`
- [ ] Run the worker with the sample CSV: `python worker.py`
- [ ] Check the dashboard at `http://localhost:8080/dashboard`
- [ ] Verify sample data flows through correctly in the database

**Day 3 Outcome:** Server running, GBP links mapped, dashboard live.

---

## Day 4: Live Test with Real Customers

- [ ] Export 5 real past customers from `app.ultimatemoving.us`
  - [ ] Save as CSV with columns: `customer_name`, `phone`, `email`, `brand`, `location_id`
- [ ] Drop the CSV into the `csv_inbox/` folder
- [ ] Run `python worker.py`
- [ ] Watch the SMS go out (use Twilio sandbox first if testing)
- [ ] Verify the full flow:
  - [ ] Customer receives survey SMS
  - [ ] Customer completes the Google Form
  - [ ] Webhook fires → gift card auto-sends
  - [ ] 24 hours later → review ask SMS sends (can manually trigger for testing)
- [ ] Check Twilio console for delivery confirmations
- [ ] Check Tremendous dashboard for gift card delivery

**Day 4 Outcome:** End-to-end flow verified with real customers.

---

## Day 5: Go Live

- [ ] Switch Tremendous from sandbox to production:
  - [ ] Change `TREMENDOUS_BASE_URL` in `.env` from `testflight.tremendous.com` to `www.tremendous.com`
  - [ ] Use production API key
  - [ ] Fund your Tremendous account with real money
- [ ] Set up the cron job for automated hourly runs:
  ```
  crontab -e
  0 * * * * cd /path/to/review_agent && /usr/bin/python3 worker.py >> logs/cron.log 2>&1
  ```
- [ ] Deploy server to a VPS (DigitalOcean, Linode, etc.) — $5-10/mo
- [ ] Run first live batch with 10-20 real customers
- [ ] Monitor dashboard and logs for 24 hours

**Day 5 Outcome:** Agent is live and running autonomously.

---

## Post-Launch Checklist (Week 2)

- [ ] Review first batch results — how many surveys completed? How many reviews posted?
- [ ] Adjust SMS timing if needed (currently 2 hours post-move for survey, 24 hours for review ask)
- [ ] Scale to additional brands
- [ ] Report results to Alex
- [ ] Begin planning Phase 2: Browser automation for CRM (eliminate manual CSV export)

---

## Cost Summary

| Item | Cost |
|------|------|
| Twilio SMS | ~$0.016 per customer (2 messages) |
| Tremendous | $0 platform fee |
| Gift Cards | $15 per customer who completes survey |
| VPS Hosting | $5-10/month |
| **Monthly estimate (50 customers)** | **~$751/month** |

---

## Key Files Reference

| File | Purpose |
|------|---------|
| `config.py` | All settings — API keys, timing, brand mappings |
| `database.py` | SQLite database — customer tracking |
| `sms_sender.py` | Twilio SMS — 3 FTC-compliant templates |
| `gift_card_sender.py` | Tremendous API — $15 Amazon gift cards |
| `csv_importer.py` | CRM export CSV importer |
| `server.py` | Flask webhook server + dashboard |
| `worker.py` | Hourly cron job — the brain |
| `test_agent.py` | 19 unit tests |
| `README.md` | Full deployment documentation |
