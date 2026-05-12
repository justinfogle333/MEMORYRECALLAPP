"""
Test Suite for the Review Agent
================================
Tests all components locally without requiring real API keys.
Uses mocking for Twilio and Tremendous API calls.

Run with: python test_agent.py
"""

import os
import sys
import json
import sqlite3
import tempfile
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Ensure we're in the right directory
sys.path.insert(0, os.path.dirname(__file__))

# Override config before importing modules
import config
config.DATABASE_PATH = os.path.join(tempfile.gettempdir(), "test_review_agent.db")
config.CSV_INBOX_PATH = os.path.join(tempfile.gettempdir(), "test_csv_inbox")
config.LOG_PATH = os.path.join(tempfile.gettempdir(), "test_review_agent.log")

import database
import csv_importer
import sms_sender
import gift_card_sender


class TestDatabase(unittest.TestCase):
    """Test the database module."""

    def setUp(self):
        """Create a fresh database for each test."""
        if os.path.exists(config.DATABASE_PATH):
            os.remove(config.DATABASE_PATH)
        database.init_db()

    def tearDown(self):
        if os.path.exists(config.DATABASE_PATH):
            os.remove(config.DATABASE_PATH)

    def test_init_db_creates_tables(self):
        """Verify that init_db creates the required tables."""
        conn = sqlite3.connect(config.DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()

        self.assertIn("customers", tables)
        self.assertIn("sms_log", tables)
        self.assertIn("gift_card_log", tables)
        print("  [PASS] Database tables created correctly")

    def test_add_customer(self):
        """Verify that adding a customer works."""
        cid = database.add_customer(
            "John Test", "+15551234567", "john@test.com", "Cross Country Movers", "NYC-001"
        )
        self.assertIsNotNone(cid)
        self.assertGreater(cid, 0)

        customer = database.get_customer_by_id(cid)
        self.assertEqual(customer["name"], "John Test")
        self.assertEqual(customer["phone"], "+15551234567")
        self.assertEqual(customer["status"], "new")
        print("  [PASS] Customer added and retrieved correctly")

    def test_duplicate_prevention(self):
        """Verify that duplicate customers (same phone + brand) are skipped."""
        cid1 = database.add_customer(
            "John Test", "+15551234567", "john@test.com", "Cross Country Movers", "NYC-001"
        )
        cid2 = database.add_customer(
            "John Test", "+15551234567", "john@test.com", "Cross Country Movers", "NYC-001"
        )
        self.assertIsNotNone(cid1)
        self.assertIsNone(cid2)
        print("  [PASS] Duplicate prevention working")

    def test_status_update(self):
        """Verify that status updates work correctly."""
        cid = database.add_customer(
            "Jane Demo", "+15559876543", "jane@test.com", "State 2 State Movers", "LA-002"
        )
        database.update_status(cid, "survey_sent", survey_sent_at=datetime.utcnow().isoformat())

        customer = database.get_customer_by_id(cid)
        self.assertEqual(customer["status"], "survey_sent")
        self.assertIsNotNone(customer["survey_sent_at"])
        print("  [PASS] Status update working")

    def test_get_customers_by_status(self):
        """Verify filtering by status."""
        database.add_customer("A", "+15551111111", "a@test.com", "Brand A", "")
        database.add_customer("B", "+15552222222", "b@test.com", "Brand B", "")
        cid3 = database.add_customer("C", "+15553333333", "c@test.com", "Brand C", "")
        database.update_status(cid3, "survey_sent")

        new_customers = database.get_customers_by_status("new")
        self.assertEqual(len(new_customers), 2)

        sent_customers = database.get_customers_by_status("survey_sent")
        self.assertEqual(len(sent_customers), 1)
        print("  [PASS] Status filtering working")

    def test_get_stats(self):
        """Verify the stats function."""
        database.add_customer("A", "+15551111111", "a@test.com", "Brand A", "")
        database.add_customer("B", "+15552222222", "b@test.com", "Brand B", "")

        stats = database.get_stats()
        self.assertEqual(stats["total"], 2)
        self.assertEqual(stats["new"], 2)
        print("  [PASS] Stats function working")

    def test_sms_logging(self):
        """Verify SMS logging."""
        cid = database.add_customer("A", "+15551111111", "a@test.com", "Brand A", "")
        database.log_sms(cid, "outbound", "survey_ask", "Test message", "SM123")

        conn = sqlite3.connect(config.DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sms_log WHERE customer_id = ?", (cid,))
        log = cursor.fetchone()
        conn.close()

        self.assertIsNotNone(log)
        self.assertEqual(log["twilio_sid"], "SM123")
        print("  [PASS] SMS logging working")


class TestCSVImporter(unittest.TestCase):
    """Test the CSV importer module."""

    def setUp(self):
        if os.path.exists(config.DATABASE_PATH):
            os.remove(config.DATABASE_PATH)
        database.init_db()

        os.makedirs(config.CSV_INBOX_PATH, exist_ok=True)

    def tearDown(self):
        if os.path.exists(config.DATABASE_PATH):
            os.remove(config.DATABASE_PATH)
        import shutil
        if os.path.exists(config.CSV_INBOX_PATH):
            shutil.rmtree(config.CSV_INBOX_PATH)

    def test_import_csv(self):
        """Verify that CSV import works with the expected format."""
        csv_path = os.path.join(config.CSV_INBOX_PATH, "test.csv")
        with open(csv_path, "w") as f:
            f.write("customer_name,phone,email,brand,location_id\n")
            f.write("John Test,5551234567,john@test.com,Cross Country Movers,NYC-001\n")
            f.write("Jane Demo,5559876543,jane@test.com,State 2 State Movers,LA-002\n")

        count = csv_importer.import_csv_files()
        self.assertEqual(count, 2)

        customers = database.get_customers_by_status("new")
        self.assertEqual(len(customers), 2)
        print("  [PASS] CSV import working (2 customers imported)")

    def test_phone_normalization(self):
        """Verify phone number normalization."""
        self.assertEqual(csv_importer._normalize_phone("5551234567"), "+15551234567")
        self.assertEqual(csv_importer._normalize_phone("15551234567"), "+15551234567")
        self.assertEqual(csv_importer._normalize_phone("(555) 123-4567"), "+15551234567")
        self.assertEqual(csv_importer._normalize_phone("+15551234567"), "+15551234567")
        print("  [PASS] Phone normalization working")

    def test_csv_moved_to_processed(self):
        """Verify that processed CSVs are moved to the processed folder."""
        csv_path = os.path.join(config.CSV_INBOX_PATH, "test.csv")
        with open(csv_path, "w") as f:
            f.write("customer_name,phone,email,brand\n")
            f.write("John Test,5551234567,john@test.com,Brand A\n")

        csv_importer.import_csv_files()

        # Original file should be gone
        self.assertFalse(os.path.exists(csv_path))

        # Should be in processed folder
        processed_dir = os.path.join(config.CSV_INBOX_PATH, "processed")
        processed_files = os.listdir(processed_dir)
        self.assertEqual(len(processed_files), 1)
        print("  [PASS] Processed CSV moved correctly")


class TestSMSSender(unittest.TestCase):
    """Test the SMS sender module (with mocked Twilio)."""

    @patch("sms_sender._get_client")
    def test_send_survey_sms(self, mock_get_client):
        """Verify survey SMS sends correctly."""
        mock_client = MagicMock()
        mock_message = MagicMock()
        mock_message.sid = "SM_TEST_123"
        mock_client.messages.create.return_value = mock_message
        mock_get_client.return_value = mock_client

        sid = sms_sender.send_survey_sms(1, "John Test", "+15551234567", "Cross Country Movers")

        self.assertEqual(sid, "SM_TEST_123")
        mock_client.messages.create.assert_called_once()

        call_kwargs = mock_client.messages.create.call_args
        body = call_kwargs.kwargs.get("body") or call_kwargs[1].get("body")
        self.assertIn("John", body)
        self.assertIn("$15 Amazon Gift Card", body)
        self.assertIn("STOP", body)
        print("  [PASS] Survey SMS template correct and FTC-compliant")

    @patch("sms_sender._get_client")
    def test_send_review_ask_sms(self, mock_get_client):
        """Verify review ask SMS sends correctly with NO incentive mention."""
        mock_client = MagicMock()
        mock_message = MagicMock()
        mock_message.sid = "SM_TEST_456"
        mock_client.messages.create.return_value = mock_message
        mock_get_client.return_value = mock_client

        sid = sms_sender.send_review_ask_sms("John Test", "+15551234567", "Cross Country Movers")

        self.assertEqual(sid, "SM_TEST_456")

        call_kwargs = mock_client.messages.create.call_args
        body = call_kwargs.kwargs.get("body") or call_kwargs[1].get("body")
        self.assertNotIn("gift card", body.lower())
        self.assertNotIn("$15", body)
        self.assertIn("Google", body)
        self.assertIn("STOP", body)
        print("  [PASS] Review ask SMS has NO incentive (Google-compliant)")

    @patch("sms_sender._get_client")
    def test_send_failure_returns_none(self, mock_get_client):
        """Verify that SMS failures return None instead of crashing."""
        mock_client = MagicMock()
        mock_client.messages.create.side_effect = Exception("Twilio error")
        mock_get_client.return_value = mock_client

        sid = sms_sender.send_survey_sms(1, "John Test", "+15551234567", "Brand A")
        self.assertIsNone(sid)
        print("  [PASS] SMS failure handled gracefully")


class TestGiftCardSender(unittest.TestCase):
    """Test the gift card sender module (with mocked Tremendous API)."""

    @patch("gift_card_sender.requests.post")
    def test_send_gift_card_success(self, mock_post):
        """Verify gift card sends correctly."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"order": {"id": "ORDER_123"}}
        mock_post.return_value = mock_response

        result = gift_card_sender.send_gift_card("John Test", "john@test.com", "Brand A")

        self.assertTrue(result["success"])
        self.assertEqual(result["order_id"], "ORDER_123")
        self.assertIsNone(result["error"])
        print("  [PASS] Gift card sent successfully")

    @patch("gift_card_sender.requests.post")
    def test_send_gift_card_failure(self, mock_post):
        """Verify gift card failure is handled gracefully."""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Bad request"
        mock_post.return_value = mock_response

        result = gift_card_sender.send_gift_card("John Test", "john@test.com", "Brand A")

        self.assertFalse(result["success"])
        self.assertIsNone(result["order_id"])
        self.assertIsNotNone(result["error"])
        print("  [PASS] Gift card failure handled gracefully")


class TestWebhookServer(unittest.TestCase):
    """Test the Flask webhook server."""

    def setUp(self):
        if os.path.exists(config.DATABASE_PATH):
            os.remove(config.DATABASE_PATH)
        database.init_db()

        from server import app
        app.config["TESTING"] = True
        self.client = app.test_client()

    def tearDown(self):
        if os.path.exists(config.DATABASE_PATH):
            os.remove(config.DATABASE_PATH)

    def test_health_check(self):
        """Verify health endpoint works."""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "ok")
        print("  [PASS] Health check endpoint working")

    def test_dashboard(self):
        """Verify dashboard endpoint works."""
        with patch("server.check_balance", return_value=100.0):
            response = self.client.get("/dashboard")
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertEqual(data["review_agent_status"], "running")
            self.assertIn("customers", data)
            print("  [PASS] Dashboard endpoint working")

    def test_survey_complete_webhook(self):
        """Verify survey completion webhook processes correctly."""
        # Add a customer first
        cid = database.add_customer(
            "John Test", "+15551234567", "john@test.com", "Cross Country Movers", "NYC-001"
        )
        database.update_status(cid, "survey_sent")

        # Mock the gift card sender
        with patch("server.send_gift_card") as mock_gc:
            mock_gc.return_value = {"success": True, "order_id": "ORD_123", "error": None}

            response = self.client.post(
                "/webhook/survey-complete",
                json={"customer_id": cid, "email": "john@test.com"},
                content_type="application/json",
            )

            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIn("gift card sent", data["message"].lower())

            # Verify customer status was updated
            customer = database.get_customer_by_id(cid)
            self.assertEqual(customer["status"], "gift_card_sent")
            print("  [PASS] Survey webhook -> gift card flow working")

    def test_survey_webhook_missing_customer_id(self):
        """Verify webhook rejects requests without customer_id."""
        response = self.client.post(
            "/webhook/survey-complete",
            json={"email": "test@test.com"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        print("  [PASS] Webhook validation working")


# ============================================================
# Run All Tests
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("REVIEW AGENT — TEST SUITE")
    print("=" * 60)
    print()

    # Run tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test classes in order
    for test_class in [TestDatabase, TestCSVImporter, TestSMSSender, TestGiftCardSender, TestWebhookServer]:
        print(f"\n--- {test_class.__name__} ---")
        suite.addTests(loader.loadTestsFromTestCase(test_class))

    runner = unittest.TextTestRunner(verbosity=0)
    result = runner.run(suite)

    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("ALL TESTS PASSED")
    else:
        print(f"FAILURES: {len(result.failures)}, ERRORS: {len(result.errors)}")
    print("=" * 60)
