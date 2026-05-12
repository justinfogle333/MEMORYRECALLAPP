"""
Bot A: Lead Quoting Engine — Main Orchestrator

This is the entry point that runs as a 24/7 daemon on the OpenClaw Mini PC.
It ties together all modules:
  1. EmailMonitor — watches inbox for new leads
  2. PricingEngine — calculates competitive quotes
  3. QuoteDelivery — sends quote emails to customers
  4. HumanReviewNotifier — alerts Seneca when human review is needed

Usage:
  python main.py              # Run the bot (daemon mode)
  python main.py --test       # Run a single test cycle then exit
  python main.py --stats      # Print pricing engine stats and exit
  python main.py --quote      # Interactive quote calculator
"""

import argparse
import logging
import signal
import sys
import time
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import (
    BOT_NAME,
    LOG_DIR,
    LOG_LEVEL,
    LOG_FORMAT,
    EMAIL_POLL_INTERVAL,
    DATA_DIR,
)
from modules.pricing_engine import PricingEngine, QuoteRequest, is_golden_route
from modules.lead_ingestion import EmailMonitor
from modules.quote_delivery import QuoteDelivery, HumanReviewNotifier


# ─────────────────────────────────────────────
# LOGGING SETUP
# ─────────────────────────────────────────────

def setup_logging():
    """Configure logging to both console and file."""
    log_file = LOG_DIR / f"bot_a_{datetime.now().strftime('%Y%m%d')}.log"

    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    root_logger.addHandler(console_handler)

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    root_logger.addHandler(file_handler)

    return logging.getLogger(__name__)


# ─────────────────────────────────────────────
# BOT ORCHESTRATOR
# ─────────────────────────────────────────────

class BotA:
    """
    The main orchestrator for Bot A: Lead Quoting Engine.
    Runs as a daemon, continuously monitoring for new leads and sending quotes.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.running = False

        # Initialize modules
        self.logger.info(f"Initializing {BOT_NAME}...")

        # Pricing Engine — load training data
        training_data_path = str(DATA_DIR / "Auto_Shipping_Training_Data_Combined.csv")
        self.pricing_engine = PricingEngine(data_path=training_data_path)

        # Email Monitor
        self.email_monitor = EmailMonitor()

        # Quote Delivery
        self.quote_delivery = QuoteDelivery()

        # Human Review Notifier (Seneca's email — configure in .env)
        import os
        reviewer_email = os.getenv("REVIEWER_EMAIL", "")
        self.review_notifier = HumanReviewNotifier(reviewer_email=reviewer_email)

        # Stats
        self.stats = {
            "started_at": None,
            "cycles": 0,
            "leads_processed": 0,
            "quotes_sent": 0,
            "quotes_flagged_review": 0,
            "errors": 0,
        }

        self.logger.info(f"{BOT_NAME} initialized successfully.")
        stats = self.pricing_engine.get_stats()
        self.logger.info(
            f"Pricing engine loaded: {stats['total_moves']} historical moves "
            f"({stats['booked_count']} booked, {stats['quoted_count']} quoted)"
        )

    def start(self):
        """Start the bot daemon loop."""
        self.running = True
        self.stats["started_at"] = datetime.now().isoformat()

        # Register signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._shutdown_handler)
        signal.signal(signal.SIGTERM, self._shutdown_handler)

        self.logger.info(
            f"{BOT_NAME} started. Polling every {EMAIL_POLL_INTERVAL}s. "
            f"Press Ctrl+C to stop."
        )

        while self.running:
            try:
                self._run_cycle()
            except KeyboardInterrupt:
                break
            except Exception as e:
                self.stats["errors"] += 1
                self.logger.error(f"Error in main loop: {e}", exc_info=True)

            # Wait before next cycle
            if self.running:
                time.sleep(EMAIL_POLL_INTERVAL)

        self._shutdown()

    def _run_cycle(self):
        """Run a single check-and-quote cycle."""
        self.stats["cycles"] += 1

        # Step 1: Check for new leads
        leads = self.email_monitor.check_for_new_leads()

        if not leads:
            return

        self.logger.info(f"Processing {len(leads)} new lead(s)...")

        for lead in leads:
            try:
                self._process_lead(lead)
            except Exception as e:
                self.stats["errors"] += 1
                self.logger.error(
                    f"Failed to process lead {lead.customer_name}: {e}",
                    exc_info=True
                )

    def _process_lead(self, lead: QuoteRequest):
        """Process a single lead through the full pipeline."""
        self.stats["leads_processed"] += 1

        self.logger.info(
            f"Processing lead: {lead.customer_name} — "
            f"{lead.pickup_zip} → {lead.delivery_zip} "
            f"({lead.vehicle_info})"
        )

        # Step 2: Check if it's a Golden Route
        golden = is_golden_route(lead.pickup_zip, lead.delivery_zip)
        if golden:
            self.logger.info(f"  ✓ Golden Route detected — eligible for auto-quoting")
        else:
            self.logger.info(f"  ✗ Non-Golden Route — will flag for human review")

        # Step 3: Calculate the quote
        result = self.pricing_engine.calculate_quote(lead)

        self.logger.info(
            f"  Quote calculated: ${result.customer_quote:.0f} "
            f"(carrier ~${result.carrier_price_estimate:.0f} + "
            f"${result.profit_margin:.0f} margin) — "
            f"confidence: {result.confidence}"
        )

        # Step 4: Send or flag for review
        if result.needs_human_review:
            self.stats["quotes_flagged_review"] += 1
            self.logger.info(
                f"  ⚠ Flagged for human review: {result.review_reason}"
            )
            # Notify Seneca
            self.review_notifier.notify_review_needed(lead, result)
        else:
            # Auto-send the quote
            sent = self.quote_delivery.generate_and_send_quote(lead, result)
            if sent:
                self.stats["quotes_sent"] += 1
                self.logger.info(f"  ✓ Quote sent to {lead.customer_email}")
            else:
                self.stats["errors"] += 1
                self.logger.warning(f"  ✗ Failed to send quote")

    def run_single_cycle(self):
        """Run one cycle and exit (for testing)."""
        self.logger.info("Running single test cycle...")
        self._run_cycle()
        self.logger.info(f"Cycle complete. Stats: {self.stats}")

    def interactive_quote(self):
        """Interactive mode for manual quote calculation."""
        print(f"\n{'='*60}")
        print(f"  {BOT_NAME} — Interactive Quote Calculator")
        print(f"{'='*60}\n")

        while True:
            try:
                pickup_zip = input("  Pickup ZIP code (or 'quit'): ").strip()
                if pickup_zip.lower() in ("quit", "q", "exit"):
                    break

                delivery_zip = input("  Delivery ZIP code: ").strip()

                date_str = input("  Pickup date (YYYY-MM-DD, or Enter for today): ").strip()
                if date_str:
                    pickup_date = datetime.strptime(date_str, "%Y-%m-%d")
                else:
                    pickup_date = datetime.now()

                request = QuoteRequest(
                    pickup_zip=pickup_zip,
                    delivery_zip=delivery_zip,
                    pickup_date=pickup_date,
                )

                result = self.pricing_engine.calculate_quote(request)

                golden = is_golden_route(pickup_zip, delivery_zip)

                print(f"\n  {'─'*50}")
                print(f"  Route:            {pickup_zip} → {delivery_zip}")
                print(f"  Golden Route:     {'YES ✓' if golden else 'NO ✗'}")
                print(f"  Carrier Estimate: ${result.carrier_price_estimate:.0f}")
                print(f"  Profit Margin:    ${result.profit_margin:.0f}")
                print(f"  Customer Quote:   ${result.customer_quote:.0f}")
                print(f"  Confidence:       {result.confidence}")
                print(f"  Comparables:      {result.comparable_moves_count}")
                print(f"  Needs Review:     {result.needs_human_review}")
                if result.review_reason:
                    print(f"  Review Reason:    {result.review_reason}")
                print(f"  Method:           {result.method}")
                print(f"  {'─'*50}\n")

            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"\n  Error: {e}\n")

        print("\nGoodbye!\n")

    def print_stats(self):
        """Print pricing engine statistics."""
        stats = self.pricing_engine.get_stats()
        print(f"\n{'='*60}")
        print(f"  {BOT_NAME} — Pricing Engine Statistics")
        print(f"{'='*60}")
        print(f"  Total historical moves:  {stats['total_moves']}")
        print(f"  Booked records:          {stats['booked_count']}")
        print(f"  Quoted records:          {stats['quoted_count']}")
        print(f"  Avg carrier price:       ${stats['avg_carrier_price']:.2f}")
        print(f"  Price range:             ${stats['min_carrier_price']:.0f} — ${stats['max_carrier_price']:.0f}")
        print(f"  Date range:              {stats['date_range_start']} to {stats['date_range_end']}")
        print(f"{'='*60}\n")

    def _shutdown_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        self.logger.info(f"Received signal {signum}. Shutting down...")
        self.running = False

    def _shutdown(self):
        """Clean shutdown."""
        self.logger.info("Shutting down...")
        self.email_monitor.disconnect()
        self.logger.info(f"Final stats: {self.stats}")
        self.logger.info(f"{BOT_NAME} stopped.")


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description=BOT_NAME)
    parser.add_argument("--test", action="store_true", help="Run a single cycle and exit")
    parser.add_argument("--stats", action="store_true", help="Print pricing engine stats and exit")
    parser.add_argument("--quote", action="store_true", help="Interactive quote calculator")
    args = parser.parse_args()

    logger = setup_logging()

    bot = BotA()

    if args.stats:
        bot.print_stats()
    elif args.quote:
        bot.interactive_quote()
    elif args.test:
        bot.run_single_cycle()
    else:
        bot.start()


if __name__ == "__main__":
    main()
