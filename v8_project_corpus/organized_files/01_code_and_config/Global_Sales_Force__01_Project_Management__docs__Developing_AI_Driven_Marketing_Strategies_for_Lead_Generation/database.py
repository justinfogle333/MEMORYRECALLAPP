"""
Database Module
===============
SQLite database for tracking customers through the review solicitation flow.
"""

import sqlite3
import logging
from datetime import datetime
from config import DATABASE_PATH

logger = logging.getLogger("review_agent")


def get_connection():
    """Get a database connection with row factory enabled."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    """Create the database tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            brand TEXT NOT NULL,
            location_id TEXT,
            status TEXT NOT NULL DEFAULT 'new',
            reminders_sent INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            survey_sent_at TEXT,
            survey_completed_at TEXT,
            gift_card_sent_at TEXT,
            review_ask_sent_at TEXT,
            gift_card_order_id TEXT,
            notes TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sms_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            direction TEXT NOT NULL,
            message_type TEXT NOT NULL,
            message_body TEXT,
            twilio_sid TEXT,
            sent_at TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gift_card_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            order_id TEXT,
            amount REAL,
            status TEXT,
            sent_at TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
    """)

    # Create indexes for the worker queries
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_customers_status
        ON customers(status)
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_customers_phone
        ON customers(phone)
    """)

    conn.commit()
    conn.close()
    logger.info("Database initialized at %s", DATABASE_PATH)


def add_customer(name, phone, email, brand, location_id):
    """Add a new customer to the database. Returns the customer ID."""
    conn = get_connection()
    cursor = conn.cursor()

    # Check for duplicate (same phone + brand within last 30 days)
    cursor.execute("""
        SELECT id FROM customers
        WHERE phone = ? AND brand = ?
        AND created_at > datetime('now', '-30 days')
    """, (phone, brand))

    existing = cursor.fetchone()
    if existing:
        logger.info("Skipping duplicate: %s (%s) for %s", name, phone, brand)
        conn.close()
        return None

    now = datetime.utcnow().isoformat()
    cursor.execute("""
        INSERT INTO customers (name, phone, email, brand, location_id, status, created_at)
        VALUES (?, ?, ?, ?, ?, 'new', ?)
    """, (name, phone, email, brand, location_id, now))

    customer_id = cursor.lastrowid
    conn.commit()
    conn.close()
    logger.info("Added customer #%d: %s (%s) for %s", customer_id, name, phone, brand)
    return customer_id


def get_customers_by_status(status):
    """Get all customers with a given status."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE status = ?", (status,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_customers_ready_for_review_ask(delay_hours):
    """Get customers who completed the survey at least `delay_hours` ago."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM customers
        WHERE status = 'gift_card_sent'
        AND gift_card_sent_at <= datetime('now', ? || ' hours')
    """, (f"-{delay_hours}",))
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_customers_ready_for_reminder(delay_hours, max_reminders):
    """Get customers who were sent the survey SMS but haven't responded."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM customers
        WHERE status = 'survey_sent'
        AND reminders_sent < ?
        AND survey_sent_at <= datetime('now', ? || ' hours')
    """, (max_reminders, f"-{delay_hours}",))
    rows = cursor.fetchall()
    conn.close()
    return rows


def update_status(customer_id, new_status, **kwargs):
    """Update a customer's status and optional timestamp fields."""
    conn = get_connection()
    cursor = conn.cursor()

    set_clauses = ["status = ?"]
    values = [new_status]

    for field, value in kwargs.items():
        set_clauses.append(f"{field} = ?")
        values.append(value)

    values.append(customer_id)
    query = f"UPDATE customers SET {', '.join(set_clauses)} WHERE id = ?"
    cursor.execute(query, values)
    conn.commit()
    conn.close()
    logger.info("Customer #%d status -> %s", customer_id, new_status)


def increment_reminders(customer_id):
    """Increment the reminders_sent counter for a customer."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE customers SET reminders_sent = reminders_sent + 1 WHERE id = ?
    """, (customer_id,))
    conn.commit()
    conn.close()


def log_sms(customer_id, direction, message_type, message_body, twilio_sid):
    """Log an SMS message to the sms_log table."""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()
    cursor.execute("""
        INSERT INTO sms_log (customer_id, direction, message_type, message_body, twilio_sid, sent_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (customer_id, direction, message_type, message_body, twilio_sid, now))
    conn.commit()
    conn.close()


def log_gift_card(customer_id, order_id, amount, status):
    """Log a gift card order to the gift_card_log table."""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()
    cursor.execute("""
        INSERT INTO gift_card_log (customer_id, order_id, amount, status, sent_at)
        VALUES (?, ?, ?, ?, ?)
    """, (customer_id, order_id, amount, status, now))
    conn.commit()
    conn.close()


def get_customer_by_id(customer_id):
    """Get a single customer by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
    row = cursor.fetchone()
    conn.close()
    return row


def get_customer_by_phone(phone):
    """Get the most recent customer record for a phone number."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM customers WHERE phone = ?
        ORDER BY created_at DESC LIMIT 1
    """, (phone,))
    row = cursor.fetchone()
    conn.close()
    return row


def get_stats():
    """Get summary statistics for the dashboard."""
    conn = get_connection()
    cursor = conn.cursor()

    stats = {}
    for status in ['new', 'survey_sent', 'survey_completed', 'gift_card_sent', 'review_ask_sent']:
        cursor.execute("SELECT COUNT(*) FROM customers WHERE status = ?", (status,))
        stats[status] = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM customers")
    stats['total'] = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(amount) FROM gift_card_log WHERE status = 'sent'")
    result = cursor.fetchone()[0]
    stats['total_gift_card_spend'] = result if result else 0.0

    conn.close()
    return stats
