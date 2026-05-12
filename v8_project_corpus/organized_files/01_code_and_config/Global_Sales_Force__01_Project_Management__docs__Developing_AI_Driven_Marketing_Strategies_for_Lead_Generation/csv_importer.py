"""
CSV Importer Module
===================
Reads completed-move CSVs from the inbox folder and imports
new customers into the database.

Expected CSV columns:
    - customer_name (or name)
    - phone (or phone_number)
    - email (optional)
    - brand (or brand_name)
    - location_id (optional)
"""

import os
import csv
import shutil
import logging
from datetime import datetime
from config import CSV_INBOX_PATH
from database import add_customer

logger = logging.getLogger("review_agent")

# Column name mappings (flexible to handle different CRM export formats)
NAME_COLUMNS = ["customer_name", "name", "customer", "full_name", "client_name"]
PHONE_COLUMNS = ["phone", "phone_number", "mobile", "cell", "telephone"]
EMAIL_COLUMNS = ["email", "email_address", "customer_email"]
BRAND_COLUMNS = ["brand", "brand_name", "company", "company_name"]
LOCATION_COLUMNS = ["location_id", "location", "office", "branch"]


def _find_column(headers, candidates):
    """Find the first matching column name from a list of candidates."""
    headers_lower = [h.strip().lower().replace(" ", "_") for h in headers]
    for candidate in candidates:
        if candidate in headers_lower:
            return headers_lower.index(candidate)
    return None


def _normalize_phone(phone):
    """Normalize phone number to +1XXXXXXXXXX format."""
    digits = "".join(c for c in phone if c.isdigit())
    if len(digits) == 10:
        return f"+1{digits}"
    elif len(digits) == 11 and digits.startswith("1"):
        return f"+{digits}"
    elif len(digits) > 11:
        return f"+{digits}"
    return phone  # Return as-is if we can't normalize


def import_csv_files():
    """
    Scan the CSV inbox folder, import all CSV files, and move
    processed files to a 'processed' subfolder.

    Returns the number of new customers imported.
    """
    if not os.path.exists(CSV_INBOX_PATH):
        os.makedirs(CSV_INBOX_PATH)
        logger.info("Created CSV inbox folder: %s", CSV_INBOX_PATH)
        return 0

    processed_dir = os.path.join(CSV_INBOX_PATH, "processed")
    os.makedirs(processed_dir, exist_ok=True)

    csv_files = [f for f in os.listdir(CSV_INBOX_PATH) if f.endswith(".csv")]

    if not csv_files:
        logger.info("No CSV files found in inbox.")
        return 0

    total_imported = 0

    for filename in csv_files:
        filepath = os.path.join(CSV_INBOX_PATH, filename)
        logger.info("Processing CSV: %s", filename)

        try:
            imported = _process_csv(filepath)
            total_imported += imported

            # Move to processed folder with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_name = f"{timestamp}_{filename}"
            shutil.move(filepath, os.path.join(processed_dir, new_name))
            logger.info("Imported %d customers from %s", imported, filename)

        except Exception as e:
            logger.error("Failed to process %s: %s", filename, str(e))
            # Move to an error folder instead
            error_dir = os.path.join(CSV_INBOX_PATH, "errors")
            os.makedirs(error_dir, exist_ok=True)
            shutil.move(filepath, os.path.join(error_dir, filename))

    return total_imported


def _process_csv(filepath):
    """Process a single CSV file and import customers."""
    imported = 0

    with open(filepath, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        headers = next(reader)

        # Find column indexes
        name_idx = _find_column(headers, NAME_COLUMNS)
        phone_idx = _find_column(headers, PHONE_COLUMNS)
        email_idx = _find_column(headers, EMAIL_COLUMNS)
        brand_idx = _find_column(headers, BRAND_COLUMNS)
        location_idx = _find_column(headers, LOCATION_COLUMNS)

        if name_idx is None or phone_idx is None:
            raise ValueError(
                f"CSV must have at least 'customer_name' and 'phone' columns. "
                f"Found headers: {headers}"
            )

        for row_num, row in enumerate(reader, start=2):
            try:
                name = row[name_idx].strip()
                phone = _normalize_phone(row[phone_idx].strip())
                email = row[email_idx].strip() if email_idx is not None and email_idx < len(row) else ""
                brand = row[brand_idx].strip() if brand_idx is not None and brand_idx < len(row) else "Unknown"
                location_id = row[location_idx].strip() if location_idx is not None and location_idx < len(row) else ""

                if not name or not phone:
                    logger.warning("Skipping row %d: missing name or phone", row_num)
                    continue

                result = add_customer(name, phone, email, brand, location_id)
                if result is not None:
                    imported += 1

            except (IndexError, ValueError) as e:
                logger.warning("Skipping row %d: %s", row_num, str(e))

    return imported
