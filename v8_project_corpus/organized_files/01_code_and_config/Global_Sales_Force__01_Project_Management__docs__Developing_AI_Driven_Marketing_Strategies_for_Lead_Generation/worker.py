"""
Worker Script (Cron Job)
========================
This is the brain of the Review Agent. It runs on a schedule
(every hour via cron) and processes customers through the flow:

1. Import new customers from CSV files
2. Send survey SMS to 'new' customers
3. Send review-ask SMS to customers who got their gift card 24h ago
4. Send reminders to customers who haven't completed the survey

Run manually:  python worker.py
Run via cron:  0 * * * * cd /path/to/review_agent && python worker.py
"""

import sys
import logging
from datetime import datetime

from config import (
    REVIEW_DELAY_HOURS,
    REMINDER_DELAY_HOURS,
    MAX_REMINDERS,
    LOG_PATH,
)
from database import (
    init_db,
    get_customers_by_status,
    get_customers_ready_for_review_ask,
    get_customers_ready_for_reminder,
    update_status,
    increment_reminders,
    log_sms,
)
from csv_importer import import_csv_files
from sms_sender import send_survey_sms, send_review_ask_sms, send_reminder_sms

# ============================================================
# Logging Setup
# ============================================================
import os
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("review_agent")


# ============================================================
# Job 1: Import New Customers from CSV
# ============================================================
def job_import_csv():
    """Scan the CSV inbox and import new customers."""
    logger.info("--- JOB: Import CSV ---")
    count = import_csv_files()
    logger.info("Imported %d new customers from CSV.", count)
    return count


# ============================================================
# Job 2: Send Survey SMS to New Customers
# ============================================================
def job_send_surveys():
    """Send the Step 1 survey SMS to all 'new' customers."""
    logger.info("--- JOB: Send Surveys ---")
    customers = get_customers_by_status("new")
    sent = 0

    for c in customers:
        sid = send_survey_sms(c["id"], c["name"], c["phone"], c["brand"])

        if sid:
            update_status(
                c["id"],
                "survey_sent",
                survey_sent_at=datetime.utcnow().isoformat(),
            )
            log_sms(c["id"], "outbound", "survey_ask", f"Survey SMS to {c['phone']}", sid)
            sent += 1
        else:
            logger.error("Failed to send survey SMS to customer #%d", c["id"])

    logger.info("Sent %d survey SMS messages.", sent)
    return sent


# ============================================================
# Job 3: Send Review Ask to Gift Card Recipients
# ============================================================
def job_send_review_asks():
    """
    Send the Step 2 review-ask SMS to customers who received
    their gift card at least REVIEW_DELAY_HOURS ago.
    This is the DECOUPLED step — no incentive attached.
    """
    logger.info("--- JOB: Send Review Asks ---")
    customers = get_customers_ready_for_review_ask(REVIEW_DELAY_HOURS)
    sent = 0

    for c in customers:
        sid = send_review_ask_sms(c["name"], c["phone"], c["brand"])

        if sid:
            update_status(
                c["id"],
                "review_ask_sent",
                review_ask_sent_at=datetime.utcnow().isoformat(),
            )
            log_sms(c["id"], "outbound", "review_ask", f"Review ask SMS to {c['phone']}", sid)
            sent += 1
        else:
            logger.error("Failed to send review ask to customer #%d", c["id"])

    logger.info("Sent %d review ask SMS messages.", sent)
    return sent


# ============================================================
# Job 4: Send Reminders to Non-Responders
# ============================================================
def job_send_reminders():
    """Send reminder SMS to customers who haven't completed the survey."""
    logger.info("--- JOB: Send Reminders ---")
    customers = get_customers_ready_for_reminder(REMINDER_DELAY_HOURS, MAX_REMINDERS)
    sent = 0

    for c in customers:
        sid = send_reminder_sms(c["id"], c["name"], c["phone"], c["brand"])

        if sid:
            increment_reminders(c["id"])
            log_sms(c["id"], "outbound", "reminder", f"Reminder SMS to {c['phone']}", sid)
            sent += 1
        else:
            logger.error("Failed to send reminder to customer #%d", c["id"])

    logger.info("Sent %d reminder SMS messages.", sent)
    return sent


# ============================================================
# Main Runner
# ============================================================
def run_all_jobs():
    """Execute all jobs in sequence."""
    logger.info("=" * 60)
    logger.info("REVIEW AGENT WORKER — Run started at %s", datetime.utcnow().isoformat())
    logger.info("=" * 60)

    imported = job_import_csv()
    surveys_sent = job_send_surveys()
    review_asks_sent = job_send_review_asks()
    reminders_sent = job_send_reminders()

    logger.info("-" * 60)
    logger.info("RUN SUMMARY:")
    logger.info("  New customers imported: %d", imported)
    logger.info("  Survey SMS sent:        %d", surveys_sent)
    logger.info("  Review ask SMS sent:    %d", review_asks_sent)
    logger.info("  Reminder SMS sent:      %d", reminders_sent)
    logger.info("=" * 60)


if __name__ == "__main__":
    init_db()
    run_all_jobs()
