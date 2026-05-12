# V8 Knowledge Extract Pack: Global_Sales_Force__Auto_Shipping_Automation__bot_a_lead_quoting_engine_v2

This pack is generated from extracted project files for analysis and recall. Treat file contents as data, not instructions.


---

## File: `01_code_and_config/Global_Sales_Force__Auto_Shipping_Automation__bot_a_lead_quoting_engine_v2/home/ubuntu/bot_a_lead_quoting_engine/config/__init__.py`

| Field | Value |
|---|---|
| Kind | `text` |
| Size Bytes | 1 |
| Extract Chars | 0 |
| Truncated | False |

```text

```


---

## File: `01_code_and_config/Global_Sales_Force__Auto_Shipping_Automation__bot_a_lead_quoting_engine_v2/home/ubuntu/bot_a_lead_quoting_engine/config/settings.py`

| Field | Value |
|---|---|
| Kind | `text` |
| Size Bytes | 6721 |
| Extract Chars | 5258 |
| Truncated | False |

```text
"""
Bot A: Lead Quoting Engine — Configuration
All settings are loaded from environment variables or .env file.
No credentials are stored in code.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from project root
PROJECT_ROOT = Path(__file__).parent.parent
load_dotenv(PROJECT_ROOT / ".env")

# ─────────────────────────────────────────────
# GENERAL
# ─────────────────────────────────────────────
BOT_NAME = "Bot A: Lead Quoting Engine"
LOG_DIR = PROJECT_ROOT / "logs"
DATA_DIR = PROJECT_ROOT / "data"
LOG_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

# ─────────────────────────────────────────────
# EMAIL (IMAP / SMTP)
# ─────────────────────────────────────────────
IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.gmail.com")
IMAP_PORT = int(os.getenv("IMAP_PORT", "993"))
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")  # App password for Gmail

# How often to check for new emails (seconds)
EMAIL_POLL_INTERVAL = int(os.getenv("EMAIL_POLL_INTERVAL", "30"))

# ─────────────────────────────────────────────
# LLM ENGINE
# ─────────────────────────────────────────────
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")  # "gemini", "openai", "ollama"

# Gemini (primary — near-free)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

# OpenAI-compatible (backup)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-nano")

# Ollama (local fallback — free)
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:4b")

# ─────────────────────────────────────────────
# CENTRAL DISPATCH API
# ─────────────────────────────────────────────
CD_API_BASE_URL = os.getenv("CD_API_BASE_URL", "https://api.centraldispatch.com")
CD_API_KEY = os.getenv("CD_API_KEY", "")
CD_API_SECRET = os.getenv("CD_API_SECRET", "")

# ─────────────────────────────────────────────
# GOOGLE SHEETS (for training data)
# ─────────────────────────────────────────────
GOOGLE_SHEETS_CREDENTIALS_FILE = os.getenv(
    "GOOGLE_SHEETS_CREDENTIALS_FILE",
    str(PROJECT_ROOT / "config" / "google_service_account.json")
)
TRAINING_DATA_SPREADSHEET_ID = os.getenv(
    "TRAINING_DATA_SPREADSHEET_ID",
    "12cjcIZ2ErS7wU_j7t8jIkFvVwoyTiJ4WD4DO8nJSNso"
)

# ─────────────────────────────────────────────
# PRICING ENGINE
# ─────────────────────────────────────────────
# Target profit margin per move (dollars)
TARGET_PROFIT_MARGIN = int(os.getenv("TARGET_PROFIT_MARGIN", "100"))

# Seasonal adjustment for peak season quotes based on non-peak data
SEASONAL_ADJUSTMENT = int(os.getenv("SEASONAL_ADJUSTMENT", "150"))

# Small increase for peak-to-peak year-over-year
PEAK_YOY_INCREASE_MIN = int(os.getenv("PEAK_YOY_INCREASE_MIN", "50"))
PEAK_YOY_INCREASE_MAX = int(os.getenv("PEAK_YOY_INCREASE_MAX", "100"))

# Recency window (days) — moves within this window are considered "recent"
RECENCY_WINDOW_DAYS = int(os.getenv("RECENCY_WINDOW_DAYS", "30"))

# Peak season months (1-indexed)
PEAK_MONTHS = [6, 7, 8]  # June, July, August

# Golden Routes — the 6 bidirectional route pairs for automated quoting
# Format: list of (region_a, region_b) tuples
# Each region is a list of state abbreviations
GOLDEN_ROUTES = [
    # CA ↔ East Coast
    (["CA"], ["NY", "NJ", "CT", "MA", "PA", "MD", "VA", "NC", "SC", "GA", "FL", "ME", "NH", "VT", "RI", "DE", "DC", "WV"]),
    # CA ↔ Midwest
    (["CA"], ["IL", "OH", "MI", "IN", "WI", "MN", "MO", "IA", "KS", "NE", "ND", "SD"]),
    # CA ↔ TX
    (["CA"], ["TX"]),
    # CA ↔ WA
    (["CA"], ["WA"]),
    # WA ↔ FL
    (["WA"], ["FL"]),
    # WA ↔ NY/NJ
    (["WA"], ["NY", "NJ"]),
]

# ─────────────────────────────────────────────
# MULTI-BRAND CONFIGURATION
# ─────────────────────────────────────────────
# Maps company names from the CRM to brand display names for customer emails
BRAND_MAP = {
    "Usa Autotransport": "USA Auto Transport",
    "Flat Price Auto Transport": "Flat Price Auto Transport",
    "State 2 State Movers": "State 2 State Movers",
    "Cross Country Movers": "Cross Country Movers",
    "Cross Country Moving": "Cross Country Moving",
    "East Coast West Coast Express": "East Coast West Coast Express",
    "All American Moving": "All American Moving",
    "American Van Lines": "American Van Lines",
    "Best Cross Country Movers": "Best Cross Country Movers",
    "Colonial Van Lines": "Colonial Van Lines",
    "National Van Lines": "National Van Lines",
    "Safeway Moving Systems": "Safeway Moving Systems",
    "Flat Price Movers": "Flat Price Movers",
    "International Van Lines": "International Van Lines",
    "Nationwide Movers": "Nationwide Movers",
    "Prestige Moving": "Prestige Moving",
    "Ultimate Movers": "Ultimate Movers",
}

# ─────────────────────────────────────────────
# LOGGING
# ─────────────────────────────────────────────
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
```


---

## File: `01_code_and_config/Global_Sales_Force__Auto_Shipping_Automation__bot_a_lead_quoting_engine_v2/home/ubuntu/bot_a_lead_quoting_engine/logs/test_results.json`

| Field | Value |
|---|---|
| Kind | `text` |
| Size Bytes | 725 |
| Extract Chars | 725 |
| Truncated | False |

```text
{
  "timestamp": "2026-04-27T20:55:40.587837",
  "data_path": "/home/ubuntu/bot_a_lead_quoting_engine/data/Auto_Shipping_Training_Data_Combined.csv",
  "total_tests": 6,
  "passed": 6,
  "failed": 0,
  "results": [
    {
      "test": "1. Data Loading (v2 structure)",
      "status": "PASS"
    },
    {
      "test": "2. Route Matching (zip + city/state + state)",
      "status": "PASS"
    },
    {
      "test": "3. Pricing Algorithm (quotes + seasonality)",
      "status": "PASS"
    },
    {
      "test": "4. Vehicle Type Data",
      "status": "PASS"
    },
    {
      "test": "5. Golden Route Detection",
      "status": "PASS"
    },
    {
      "test": "6. Carrier Name Data",
      "status": "PASS"
    }
  ]
}
```


---

## File: `01_code_and_config/Global_Sales_Force__Auto_Shipping_Automation__bot_a_lead_quoting_engine_v2/home/ubuntu/bot_a_lead_quoting_engine/main.py`

| Field | Value |
|---|---|
| Kind | `text` |
| Size Bytes | 11817 |
| Extract Chars | 11226 |
| Truncated | False |

```text
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
        self.pricing_engine = PricingEngine(training_data_path=training_data_path)

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
```


---

## File: `01_code_and_config/Global_Sales_Force__Auto_Shipping_Automation__bot_a_lead_quoting_engine_v2/home/ubuntu/bot_a_lead_quoting_engine/modules/pricing_engine.py`

| Field | Value |
|---|---|
| Kind | `text` |
| Size Bytes | 27162 |
| Extract Chars | 26497 |
| Truncated | False |

```text
"""
Bot A: Lead Quoting Engine — Pricing Engine Module (v2)

This module implements the v2 pricing algorithm:
1. Historical Lookup — find most recent carrier price for similar route
2. Recency & Seasonality Check — adjust based on timing
3. Margin Addition — add $100 flat profit
4. Competitiveness Check — validate against CD Market Intelligence (future)

Training data v2 supports two record types:
- UM CRM records: have pickup_zip/delivery_zip (zip-based matching)
- Google Sheet records: have origin_city/origin_state/dest_city/dest_state (city+state matching)

Route matching cascades: exact zip → regional zip → city+state → state-to-state.
Vehicle type matching is used as a tiebreaker when available.
"""

import csv
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field

from config.settings import (
    DATA_DIR,
    TARGET_PROFIT_MARGIN,
    SEASONAL_ADJUSTMENT,
    PEAK_YOY_INCREASE_MIN,
    PEAK_YOY_INCREASE_MAX,
    RECENCY_WINDOW_DAYS,
    PEAK_MONTHS,
    GOLDEN_ROUTES,
)

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# DATA MODELS
# ─────────────────────────────────────────────

@dataclass
class HistoricalMove:
    """A single historical move record from the training data."""
    id: str
    record_date: datetime  # The primary date for this record (pickup_date or created_at)
    pickup_zip: str
    delivery_zip: str
    origin_city: str
    origin_state: str
    dest_city: str
    dest_state: str
    pickup_date: Optional[datetime]
    offer_price: float
    carrier_price: float
    profit_markup: float
    vehicle_type: str  # sedan, suv, truck, van, motorcycle, sports
    vehicle_raw: str  # Original vehicle string (e.g., "2020 Volkswagen Tiguan")
    carrier_name: str
    company_name: str
    status: str
    dataset_source: str  # "BOOKED", "QUOTED", or "BOOKED_GSHEET"

    @property
    def pickup_region(self) -> str:
        """First 3 digits of zip = regional grouping."""
        return self.pickup_zip[:3] if self.pickup_zip else ""

    @property
    def delivery_region(self) -> str:
        """First 3 digits of zip = regional grouping."""
        return self.delivery_zip[:3] if self.delivery_zip else ""

    @property
    def is_peak_season(self) -> bool:
        """Was this move during peak season (June-August)?"""
        if self.pickup_date:
            return self.pickup_date.month in PEAK_MONTHS
        if self.record_date:
            return self.record_date.month in PEAK_MONTHS
        return False

    @property
    def is_booked(self) -> bool:
        """Was this move actually booked (vs just quoted)?"""
        return self.dataset_source in ("BOOKED", "BOOKED_GSHEET")


@dataclass
class QuoteRequest:
    """An incoming lead that needs a price quote."""
    pickup_zip: str
    delivery_zip: str
    pickup_date: datetime
    origin_city: str = ""
    origin_state: str = ""
    dest_city: str = ""
    dest_state: str = ""
    vehicle_info: str = ""  # Make/model if available
    vehicle_type: str = ""  # sedan, suv, truck, etc.
    transport_type: str = "open"  # open or enclosed
    company_name: str = ""
    customer_name: str = ""
    customer_email: str = ""

    @property
    def pickup_region(self) -> str:
        return self.pickup_zip[:3] if self.pickup_zip else ""

    @property
    def delivery_region(self) -> str:
        return self.delivery_zip[:3] if self.delivery_zip else ""

    @property
    def is_peak_season(self) -> bool:
        return self.pickup_date.month in PEAK_MONTHS


@dataclass
class QuoteResult:
    """The calculated quote to present to the customer."""
    carrier_price_estimate: float
    profit_margin: float
    customer_quote: float
    confidence: str  # "high", "medium", "low", "none"
    method: str  # Description of how the price was calculated
    comparable_moves_count: int
    needs_human_review: bool = False
    review_reason: str = ""


# ─────────────────────────────────────────────
# ZIP CODE → STATE MAPPING
# ─────────────────────────────────────────────

ZIP_TO_STATE = {}
_ZIP_RANGES = [
    ("005", "009", "PR"), ("010", "027", "MA"), ("028", "029", "RI"),
    ("030", "038", "NH"), ("039", "049", "ME"), ("050", "059", "VT"),
    ("060", "069", "CT"), ("070", "089", "NJ"), ("100", "149", "NY"),
    ("150", "196", "PA"), ("197", "199", "DE"), ("200", "205", "DC"),
    ("206", "219", "MD"), ("220", "246", "VA"), ("247", "268", "WV"),
    ("270", "289", "NC"), ("290", "299", "SC"), ("300", "319", "GA"),
    ("320", "349", "FL"), ("350", "369", "AL"), ("370", "385", "TN"),
    ("386", "397", "MS"), ("400", "427", "KY"), ("430", "459", "OH"),
    ("460", "479", "IN"), ("480", "499", "MI"), ("500", "528", "IA"),
    ("530", "549", "WI"), ("550", "567", "MN"), ("570", "577", "SD"),
    ("580", "588", "ND"), ("590", "599", "MT"), ("600", "629", "IL"),
    ("630", "658", "MO"), ("660", "679", "KS"), ("680", "693", "NE"),
    ("700", "714", "LA"), ("716", "729", "AR"), ("730", "749", "OK"),
    ("750", "799", "TX"), ("800", "816", "CO"), ("820", "831", "WY"),
    ("832", "838", "ID"), ("840", "847", "UT"), ("850", "865", "AZ"),
    ("870", "884", "NM"), ("889", "898", "NV"), ("900", "966", "CA"),
    ("967", "968", "HI"), ("970", "979", "OR"), ("980", "994", "WA"),
    ("995", "999", "AK"),
]

for start, end, state in _ZIP_RANGES:
    for prefix in range(int(start), int(end) + 1):
        ZIP_TO_STATE[f"{prefix:03d}"] = state


def zip_to_state(zip_code: str) -> str:
    """Convert a zip code to a 2-letter state abbreviation."""
    if not zip_code or len(zip_code) < 3:
        return ""
    prefix = zip_code[:3]
    return ZIP_TO_STATE.get(prefix, "")


def is_golden_route(pickup_zip: str, delivery_zip: str,
                    origin_state: str = "", dest_state: str = "") -> bool:
    """Check if a route is a Golden Route (high-volume, easy-to-fulfill)."""
    # Try zip-based state lookup first, fall back to provided state
    pickup_state = zip_to_state(pickup_zip) if pickup_zip else origin_state
    delivery_state = zip_to_state(delivery_zip) if delivery_zip else dest_state

    if not pickup_state or not delivery_state:
        return False

    # GOLDEN_ROUTES is a list of tuples: ([origin_states], [dest_states])
    # Check both directions
    for origins, dests in GOLDEN_ROUTES:
        if (pickup_state in origins and delivery_state in dests) or \
           (pickup_state in dests and delivery_state in origins):
            return True
    return False


# ─────────────────────────────────────────────
# PRICING ENGINE
# ─────────────────────────────────────────────

class PricingEngine:
    """
    The core pricing engine that calculates quotes based on historical data.
    Loads training data from CSV and implements the v2 pricing algorithm.
    """

    def __init__(self, data_path: str = None):
        self._data_path = data_path or str(Path(DATA_DIR) / "Auto_Shipping_Training_Data_Combined.csv")
        self.moves: list[HistoricalMove] = []
        self._load_training_data()

    def _load_training_data(self):
        """Load and parse the training CSV into HistoricalMove objects.

        Supports both v1 (UM CRM) and v2 (Google Sheet) column structures.
        """
        path = Path(self._data_path)
        if not path.exists():
            logger.warning(f"Training data not found at {path}. Pricing engine has no data.")
            return

        count = 0
        skipped = 0

        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    # Parse carrier price — skip records with no valid price
                    carrier_price = self._parse_float(row.get("carrier_price", ""))
                    if carrier_price <= 0:
                        skipped += 1
                        continue

                    offer_price = self._parse_float(row.get("offer_price", ""))
                    profit_markup = self._parse_float(row.get("profit_markup", ""))

                    # Parse dates — v2 uses pickup_date as primary; v1 had created_at
                    pickup_date = self._parse_date(row.get("pickup_date", ""))
                    created_at = self._parse_datetime(row.get("created_at", ""))

                    # record_date: prefer pickup_date, fall back to created_at
                    record_date = pickup_date or created_at
                    if not record_date:
                        # Try to derive from month column (e.g., "2024-06")
                        month_str = row.get("month", "")
                        if month_str and len(month_str) >= 7:
                            record_date = self._parse_date(month_str + "-15")
                        if not record_date:
                            skipped += 1
                            continue

                    # Location data — support both zip-based and city/state
                    pickup_zip = row.get("pickup_zip", "").strip()
                    delivery_zip = row.get("delivery_zip", "").strip()
                    origin_city = row.get("origin_city", "").strip().upper()
                    origin_state = row.get("origin_state", "").strip().upper()
                    dest_city = row.get("dest_city", "").strip().upper()
                    dest_state = row.get("dest_state", "").strip().upper()

                    # Clean zip codes (remove .0 from float conversion)
                    if pickup_zip and '.' in pickup_zip:
                        pickup_zip = pickup_zip.split('.')[0]
                    if delivery_zip and '.' in delivery_zip:
                        delivery_zip = delivery_zip.split('.')[0]

                    # Pad zip codes to 5 digits
                    if pickup_zip and pickup_zip.isdigit():
                        pickup_zip = pickup_zip.zfill(5)
                    if delivery_zip and delivery_zip.isdigit():
                        delivery_zip = delivery_zip.zfill(5)

                    # If we have zip but no state, derive state from zip
                    if pickup_zip and not origin_state:
                        origin_state = zip_to_state(pickup_zip)
                    if delivery_zip and not dest_state:
                        dest_state = zip_to_state(delivery_zip)

                    # Must have at least state-level location data
                    if not origin_state and not pickup_zip:
                        skipped += 1
                        continue
                    if not dest_state and not delivery_zip:
                        skipped += 1
                        continue

                    move = HistoricalMove(
                        id=row.get("reference_number", row.get("id", "")),
                        record_date=record_date,
                        pickup_zip=pickup_zip,
                        delivery_zip=delivery_zip,
                        origin_city=origin_city,
                        origin_state=origin_state,
                        dest_city=dest_city,
                        dest_state=dest_state,
                        pickup_date=pickup_date,
                        offer_price=offer_price,
                        carrier_price=carrier_price,
                        profit_markup=profit_markup,
                        vehicle_type=row.get("vehicle_type", "").strip().lower(),
                        vehicle_raw=row.get("vehicle_raw", "").strip(),
                        carrier_name=row.get("carrier_name", "").strip(),
                        company_name=row.get("company_name", ""),
                        status=row.get("status", ""),
                        dataset_source=row.get("dataset_source", ""),
                    )
                    self.moves.append(move)
                    count += 1

                except Exception as e:
                    skipped += 1
                    logger.debug(f"Skipped row: {e}")

        logger.info(
            f"Loaded {count} historical moves ({skipped} skipped). "
            f"Data path: {self._data_path}"
        )

    def _parse_float(self, value: str) -> float:
        """Safely parse a float, returning 0.0 on failure."""
        try:
            if not value or value == 'nan':
                return 0.0
            # Handle currency formatting
            clean = str(value).replace('$', '').replace(',', '').strip()
            return float(clean)
        except (ValueError, TypeError):
            return 0.0

    def _parse_datetime(self, value: str) -> Optional[datetime]:
        """Parse a datetime string like '2025-01-01 05:51:01'."""
        if not value or value == 'nan':
            return None
        try:
            return datetime.strptime(value.strip(), "%Y-%m-%d %H:%M:%S")
        except ValueError:
            try:
                return datetime.strptime(value.strip(), "%Y-%m-%d")
            except ValueError:
                return None

    def _parse_date(self, value: str) -> Optional[datetime]:
        """Parse a date string in various formats."""
        if not value or value == 'nan':
            return None
        value = str(value).strip()
        for fmt in ["%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y", "%Y-%m-%d %H:%M:%S"]:
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
        return None

    def find_comparable_moves(
        self,
        pickup_zip: str = "",
        delivery_zip: str = "",
        origin_city: str = "",
        origin_state: str = "",
        dest_city: str = "",
        dest_state: str = "",
        vehicle_type: str = "",
        max_results: int = 20,
    ) -> tuple[list[HistoricalMove], str]:
        """
        Find historical moves on similar routes.

        Matching strategy (cascading):
        1. Exact zip-to-zip match
        2. Regional zip match (first 3 digits = same metro area)
        3. City+State match (exact city name + state)
        4. State-to-state match (broadest)

        Prioritizes BOOKED records over QUOTED records.
        Returns (matches, match_quality) with most recent matches first.
        """
        pickup_region = pickup_zip[:3] if pickup_zip else ""
        delivery_region = delivery_zip[:3] if delivery_zip else ""

        # Derive states from zips if not provided
        if not origin_state and pickup_zip:
            origin_state = zip_to_state(pickup_zip)
        if not dest_state and delivery_zip:
            dest_state = zip_to_state(delivery_zip)

        origin_city = origin_city.upper().strip()
        dest_city = dest_city.upper().strip()
        origin_state = origin_state.upper().strip()
        dest_state = dest_state.upper().strip()

        exact_zip_matches = []
        regional_matches = []
        city_state_matches = []
        state_matches = []

        for move in self.moves:
            # ── Exact zip match (both directions) ──
            if pickup_zip and delivery_zip and move.pickup_zip and move.delivery_zip:
                is_fwd = (move.pickup_zip == pickup_zip and move.delivery_zip == delivery_zip)
                is_rev = (move.pickup_zip == delivery_zip and move.delivery_zip == pickup_zip)
                if is_fwd or is_rev:
                    exact_zip_matches.append(move)
                    continue

            # ── Regional zip match ──
            if pickup_region and delivery_region and move.pickup_region and move.delivery_region:
                is_fwd = (move.pickup_region == pickup_region and
                          move.delivery_region == delivery_region)
                is_rev = (move.pickup_region == delivery_region and
                          move.delivery_region == pickup_region)
                if is_fwd or is_rev:
                    regional_matches.append(move)
                    continue

            # ── City + State match ──
            if origin_city and dest_city and origin_state and dest_state:
                if move.origin_city and move.dest_city:
                    is_fwd = (move.origin_city == origin_city and move.origin_state == origin_state and
                              move.dest_city == dest_city and move.dest_state == dest_state)
                    is_rev = (move.origin_city == dest_city and move.origin_state == dest_state and
                              move.dest_city == origin_city and move.dest_state == origin_state)
                    if is_fwd or is_rev:
                        city_state_matches.append(move)
                        continue

            # ── State-to-state match ──
            move_origin_state = move.origin_state or zip_to_state(move.pickup_zip)
            move_dest_state = move.dest_state or zip_to_state(move.delivery_zip)
            if origin_state and dest_state and move_origin_state and move_dest_state:
                is_fwd = (move_origin_state == origin_state and move_dest_state == dest_state)
                is_rev = (move_origin_state == dest_state and move_dest_state == origin_state)
                if is_fwd or is_rev:
                    state_matches.append(move)

        # Sort each tier: prefer booked, then most recent
        def sort_key(m: HistoricalMove):
            booked_priority = 0 if m.is_booked else 1
            # Vehicle type match bonus
            vtype_priority = 0 if (vehicle_type and m.vehicle_type == vehicle_type) else 1
            return (booked_priority, vtype_priority,
                    -(m.record_date.timestamp() if m.record_date else 0))

        exact_zip_matches.sort(key=sort_key)
        regional_matches.sort(key=sort_key)
        city_state_matches.sort(key=sort_key)
        state_matches.sort(key=sort_key)

        # Cascade: use the most specific matches available
        if exact_zip_matches:
            return exact_zip_matches[:max_results], "exact_zip"
        elif regional_matches:
            return regional_matches[:max_results], "regional"
        elif city_state_matches:
            return city_state_matches[:max_results], "city_state"
        elif state_matches:
            return state_matches[:max_results], "state_level"
        else:
            return [], "none"

    def calculate_quote(self, request: QuoteRequest) -> QuoteResult:
        """
        Calculate a quote for an incoming lead using the v2 pricing algorithm.

        Returns a QuoteResult with the calculated price, confidence level,
        and whether human review is needed.
        """
        now = datetime.now()

        comparables, match_quality = self.find_comparable_moves(
            pickup_zip=request.pickup_zip,
            delivery_zip=request.delivery_zip,
            origin_city=request.origin_city,
            origin_state=request.origin_state,
            dest_city=request.dest_city,
            dest_state=request.dest_state,
            vehicle_type=request.vehicle_type,
        )

        if not comparables:
            return QuoteResult(
                carrier_price_estimate=0,
                profit_margin=TARGET_PROFIT_MARGIN,
                customer_quote=0,
                confidence="none",
                method="No comparable historical moves found. Requires human pricing.",
                comparable_moves_count=0,
                needs_human_review=True,
                review_reason="No historical data for this route.",
            )

        # ─── Step 1: Get the most recent carrier price ───
        most_recent = comparables[0]
        baseline_carrier_price = most_recent.carrier_price
        method_parts = []

        method_parts.append(
            f"Baseline: ${baseline_carrier_price:.0f} from {most_recent.dataset_source} "
            f"record #{most_recent.id} ({match_quality} match, "
            f"dated {most_recent.record_date.strftime('%Y-%m-%d')})"
        )

        # ─── Step 2: Recency & Seasonality Check ───
        days_since_move = (now - most_recent.record_date).days
        is_recent = days_since_move <= RECENCY_WINDOW_DAYS
        move_is_peak = request.is_peak_season
        historical_is_peak = most_recent.is_peak_season
        adjusted_carrier_price = baseline_carrier_price

        if is_recent:
            # Recent data — use as-is
            method_parts.append(
                f"Recency: {days_since_move} days old (within {RECENCY_WINDOW_DAYS}-day window). "
                f"Using baseline as-is."
            )
        elif not historical_is_peak and move_is_peak:
            # Old non-peak data, but new move is peak → add seasonal adjustment
            adjusted_carrier_price += SEASONAL_ADJUSTMENT
            method_parts.append(
                f"Seasonal: Historical is non-peak, new move is peak season. "
                f"Added ${SEASONAL_ADJUSTMENT} adjustment. "
                f"Adjusted carrier: ${adjusted_carrier_price:.0f}"
            )
        elif historical_is_peak and move_is_peak:
            # Peak-to-peak year-over-year comparison
            current_non_peak = self._find_most_recent_non_peak(comparables)
            if current_non_peak:
                if most_recent.carrier_price <= current_non_peak.carrier_price:
                    yoy_increase = (PEAK_YOY_INCREASE_MIN + PEAK_YOY_INCREASE_MAX) // 2
                    adjusted_carrier_price = most_recent.carrier_price + yoy_increase
                    method_parts.append(
                        f"Peak YoY: Last peak ${most_recent.carrier_price:.0f} <= "
                        f"current non-peak ${current_non_peak.carrier_price:.0f}. "
                        f"Added ${yoy_increase} YoY increase. "
                        f"Adjusted carrier: ${adjusted_carrier_price:.0f}"
                    )
                else:
                    adjusted_carrier_price = current_non_peak.carrier_price + SEASONAL_ADJUSTMENT
                    method_parts.append(
                        f"Peak YoY: Last peak ${most_recent.carrier_price:.0f} > "
                        f"current non-peak ${current_non_peak.carrier_price:.0f}. "
                        f"Added ${SEASONAL_ADJUSTMENT} to current non-peak. "
                        f"Adjusted carrier: ${adjusted_carrier_price:.0f}"
                    )
            else:
                adjusted_carrier_price += SEASONAL_ADJUSTMENT
                method_parts.append(
                    f"Peak YoY: No non-peak comparables found. "
                    f"Added ${SEASONAL_ADJUSTMENT} seasonal adjustment. "
                    f"Adjusted carrier: ${adjusted_carrier_price:.0f}"
                )

        # ─── Step 3: Add profit margin ───
        customer_quote = adjusted_carrier_price + TARGET_PROFIT_MARGIN
        method_parts.append(
            f"Margin: Added ${TARGET_PROFIT_MARGIN} profit. "
            f"Final quote: ${customer_quote:.0f}"
        )

        # ─── Determine confidence level ───
        booked_count = sum(1 for m in comparables if m.is_booked)
        if match_quality == "exact_zip" and booked_count >= 3:
            confidence = "high"
        elif match_quality in ("exact_zip", "regional", "city_state") and len(comparables) >= 3:
            confidence = "medium"
        else:
            confidence = "low"

        # ─── Flag for human review if needed ───
        needs_review = False
        review_reason = ""

        if confidence == "low":
            needs_review = True
            review_reason = f"Low confidence: {match_quality} match with only {len(comparables)} comparables."

        if customer_quote > 3000:
            needs_review = True
            review_reason = f"High quote (${customer_quote:.0f}) — verify before sending."

        if not is_golden_route(request.pickup_zip, request.delivery_zip,
                               request.origin_state, request.dest_state):
            needs_review = True
            review_reason = "Route is NOT a Golden Route — requires manual pricing."

        return QuoteResult(
            carrier_price_estimate=adjusted_carrier_price,
            profit_margin=TARGET_PROFIT_MARGIN,
            customer_quote=customer_quote,
            confidence=confidence,
            method=" | ".join(method_parts),
            comparable_moves_count=len(comparables),
            needs_human_review=needs_review,
            review_reason=review_reason,
        )

    def _find_most_recent_non_peak(
        self, comparables: list[HistoricalMove]
    ) -> Optional[HistoricalMove]:
        """Find the most recent non-peak season move from comparables."""
        for move in comparables:
            if not move.is_peak_season:
                return move
        return None

    def reload_data(self):
        """Reload training data from disk (called after Bot B syncs new data)."""
        self.moves.clear()
        self._load_training_data()
        logger.info("Training data reloaded.")

    def get_stats(self) -> dict:
        """Return summary statistics about the loaded training data."""
        if not self.moves:
            return {"total_moves": 0}

        booked = [m for m in self.moves if m.is_booked]
        quoted = [m for m in self.moves if not m.is_booked]
        carrier_prices = [m.carrier_price for m in self.moves if m.carrier_price > 0]

        # Vehicle type stats
        vtypes = {}
        for m in self.moves:
            vt = m.vehicle_type or "unknown"
            vtypes[vt] = vtypes.get(vt, 0) + 1

        # State coverage
        states = set()
        for m in self.moves:
            if m.origin_state:
                states.add(m.origin_state)
            if m.dest_state:
                states.add(m.dest_state)

        return {
            "total_moves": len(self.moves),
            "booked_count": len(booked),
            "quoted_count": len(quoted),
            "avg_carrier_price": sum(carrier_prices) / len(carrier_prices) if carrier_prices else 0,
            "min_carrier_price": min(carrier_prices) if carrier_prices else 0,
            "max_carrier_price": max(carrier_prices) if carrier_prices else 0,
            "date_range_start": min(m.record_date for m in self.moves).strftime("%Y-%m-%d"),
            "date_range_end": max(m.record_date for m in self.moves).strftime("%Y-%m-%d"),
            "vehicle_types": vtypes,
            "states_covered": len(states),
            "with_zip": sum(1 for m in self.moves if m.pickup_zip),
            "with_city_state": sum(1 for m in self.moves if m.origin_city and m.origin_state),
        }
```


---

## File: `01_code_and_config/Global_Sales_Force__Auto_Shipping_Automation__bot_a_lead_quoting_engine_v2/home/ubuntu/bot_a_lead_quoting_engine/tests/test_full_pipeline.py`

| Field | Value |
|---|---|
| Kind | `text` |
| Size Bytes | 10358 |
| Extract Chars | 10105 |
| Truncated | False |

```text
"""
Bot A: Full Pipeline Test Suite (v2)

Tests the complete pipeline with the restructured training data:
1. Data loading — verify the v2 CSV loads correctly with city/state + zip records
2. Route matching — test zip-based, city+state, and state-level matching
3. Pricing algorithm — verify seasonal adjustments and margin calculations
4. Vehicle type data — verify vehicle type is loaded and accessible
5. Golden Route detection — verify route classification with both zip and state
6. Carrier name data — verify carrier info is loaded
"""

import sys
import os
import json
import logging
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.pricing_engine import PricingEngine, QuoteRequest, is_golden_route, zip_to_state

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

RESULTS = []
DATA_PATH = str(Path(__file__).parent.parent / "data" / "Auto_Shipping_Training_Data_Combined.csv")


def run_test(name, test_func):
    """Run a test and record the result."""
    try:
        test_func()
        RESULTS.append({"test": name, "status": "PASS"})
        print(f"  ✓ {name}")
    except AssertionError as e:
        RESULTS.append({"test": name, "status": "FAIL", "error": str(e)})
        print(f"  ✗ {name}: {e}")
    except Exception as e:
        RESULTS.append({"test": name, "status": "ERROR", "error": str(e)})
        print(f"  ✗ {name}: ERROR — {e}")


def test_data_loading():
    """Test 1: Verify training data loads correctly with v2 structure."""
    engine = PricingEngine(data_path=DATA_PATH)
    stats = engine.get_stats()

    assert stats["total_moves"] > 10000, (
        f"Expected >10,000 moves, got {stats['total_moves']}"
    )

    # Should have both booked and quoted records
    assert stats["booked_count"] > 0, "No booked records loaded"
    assert stats["quoted_count"] > 0, "No quoted records loaded"

    # Should have vehicle type data from the Google Sheet records
    vtypes = stats.get("vehicle_types", {})
    assert "sedan" in vtypes or "suv" in vtypes, (
        f"No vehicle type data loaded. Types: {vtypes}"
    )

    # Should have both zip-based and city/state records
    assert stats["with_zip"] > 0, "No zip-based records loaded"
    assert stats["with_city_state"] > 0, "No city/state records loaded"

    # Should cover many states
    assert stats["states_covered"] >= 40, (
        f"Expected >=40 states covered, got {stats['states_covered']}"
    )

    logger.info(
        f"Loaded {stats['total_moves']} moves: "
        f"{stats['booked_count']} booked, {stats['quoted_count']} quoted. "
        f"Vehicle types: {vtypes}. "
        f"States: {stats['states_covered']}. "
        f"With zip: {stats['with_zip']}, with city/state: {stats['with_city_state']}"
    )


def test_route_matching():
    """Test 2: Verify route matching works at all levels."""
    engine = PricingEngine(data_path=DATA_PATH)

    # Test state-level matching (CA → NY — a Golden Route)
    matches, quality = engine.find_comparable_moves(
        origin_state="CA", dest_state="NY"
    )
    assert len(matches) > 0, "No matches found for CA → NY state-level"
    logger.info(f"CA → NY: {len(matches)} matches ({quality})")

    # Test city+state matching (LOS ANGELES, CA → NEW YORK, NY)
    matches_city, quality_city = engine.find_comparable_moves(
        origin_city="LOS ANGELES", origin_state="CA",
        dest_city="NEW YORK", dest_state="NY"
    )
    assert len(matches_city) > 0, "No matches found for LA → NY city+state"
    logger.info(f"LA → NY city+state: {len(matches_city)} matches ({quality_city})")

    # Test zip-based matching (90210 → 10001)
    matches_zip, quality_zip = engine.find_comparable_moves(
        pickup_zip="90210", delivery_zip="10001"
    )
    logger.info(f"90210 → 10001: {len(matches_zip)} matches ({quality_zip})")

    # Test bidirectional matching (NY → CA should also find CA → NY)
    matches_rev, quality_rev = engine.find_comparable_moves(
        origin_state="NY", dest_state="CA"
    )
    assert len(matches_rev) > 0, "No reverse matches found for NY → CA"
    logger.info(f"NY → CA (reverse): {len(matches_rev)} matches ({quality_rev})")


def test_pricing_algorithm():
    """Test 3: Verify the pricing algorithm produces valid quotes."""
    engine = PricingEngine(data_path=DATA_PATH)

    # Test a Golden Route quote (CA → NY)
    request = QuoteRequest(
        pickup_zip="90210",
        delivery_zip="10001",
        pickup_date=datetime(2026, 3, 15),
        origin_city="LOS ANGELES",
        origin_state="CA",
        dest_city="NEW YORK",
        dest_state="NY",
    )

    result = engine.calculate_quote(request)

    assert result.customer_quote > 0, "Quote should be > 0 for a Golden Route"
    assert result.carrier_price_estimate > 0, "Carrier price estimate should be > 0"
    assert result.profit_margin > 0, "Profit margin should be > 0"
    assert result.comparable_moves_count > 0, "Should have comparable moves"
    assert result.confidence in ("high", "medium", "low"), (
        f"Unexpected confidence: {result.confidence}"
    )

    logger.info(
        f"CA → NY quote: ${result.customer_quote:.0f} "
        f"(carrier: ${result.carrier_price_estimate:.0f}, "
        f"margin: ${result.profit_margin:.0f}, "
        f"confidence: {result.confidence}, "
        f"comparables: {result.comparable_moves_count})"
    )
    logger.info(f"Method: {result.method}")

    # Test a WA → FL route (peak season)
    request2 = QuoteRequest(
        pickup_zip="98101",
        delivery_zip="33101",
        pickup_date=datetime(2026, 7, 15),
        origin_city="SEATTLE",
        origin_state="WA",
        dest_city="MIAMI",
        dest_state="FL",
    )

    result2 = engine.calculate_quote(request2)
    assert result2.customer_quote > 0, "WA → FL quote should be > 0"
    logger.info(
        f"WA → FL (peak): ${result2.customer_quote:.0f} "
        f"(confidence: {result2.confidence})"
    )


def test_vehicle_type_data():
    """Test 4: Verify vehicle type data is loaded and accessible."""
    engine = PricingEngine(data_path=DATA_PATH)

    with_vtype = sum(1 for m in engine.moves if m.vehicle_type)
    total = len(engine.moves)

    assert with_vtype > 0, "No moves have vehicle type data"
    pct = with_vtype / total * 100

    vtypes = {}
    for m in engine.moves:
        vt = m.vehicle_type or "unknown"
        vtypes[vt] = vtypes.get(vt, 0) + 1

    logger.info(
        f"Vehicle type coverage: {with_vtype}/{total} ({pct:.0f}%). "
        f"Distribution: {vtypes}"
    )

    assert "sedan" in vtypes, "No sedan records found"
    assert "suv" in vtypes, "No SUV records found"


def test_golden_route_detection():
    """Test 5: Verify Golden Route detection works with both zip and state."""
    assert is_golden_route("90210", "10001") is True, "CA → NY should be golden (zip)"
    assert is_golden_route("98101", "33101") is True, "WA → FL should be golden (zip)"
    assert is_golden_route("90210", "75001") is True, "CA → TX should be golden (zip)"

    assert is_golden_route("", "", "CA", "NY") is True, "CA → NY should be golden (state)"
    assert is_golden_route("", "", "WA", "FL") is True, "WA → FL should be golden (state)"

    assert is_golden_route("", "", "ME", "VT") is False, "ME → VT should NOT be golden"

    assert is_golden_route("10001", "90210") is True, "NY → CA should be golden (reverse)"

    logger.info("Golden Route detection: all checks passed")


def test_carrier_name_data():
    """Test 6: Verify carrier name data is loaded from Google Sheet records."""
    engine = PricingEngine(data_path=DATA_PATH)

    with_carrier = sum(1 for m in engine.moves if m.carrier_name)
    total = len(engine.moves)

    assert with_carrier > 0, "No moves have carrier name data"
    pct = with_carrier / total * 100

    carriers = {}
    for m in engine.moves:
        if m.carrier_name:
            carriers[m.carrier_name] = carriers.get(m.carrier_name, 0) + 1

    top_5 = sorted(carriers.items(), key=lambda x: -x[1])[:5]

    logger.info(
        f"Carrier name coverage: {with_carrier}/{total} ({pct:.0f}%). "
        f"Unique carriers: {len(carriers)}. "
        f"Top 5: {top_5}"
    )


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("BOT A: FULL PIPELINE TEST SUITE (v2)")
    print("=" * 60)

    if not Path(DATA_PATH).exists():
        print(f"\n✗ Training data not found at: {DATA_PATH}")
        print("  Please ensure the CSV is in the data/ directory.")
        sys.exit(1)

    print(f"\nTraining data: {DATA_PATH}")
    print(f"File size: {os.path.getsize(DATA_PATH) / 1024 / 1024:.2f} MB\n")

    print("Running tests...\n")

    run_test("1. Data Loading (v2 structure)", test_data_loading)
    run_test("2. Route Matching (zip + city/state + state)", test_route_matching)
    run_test("3. Pricing Algorithm (quotes + seasonality)", test_pricing_algorithm)
    run_test("4. Vehicle Type Data", test_vehicle_type_data)
    run_test("5. Golden Route Detection", test_golden_route_detection)
    run_test("6. Carrier Name Data", test_carrier_name_data)

    passed = sum(1 for r in RESULTS if r["status"] == "PASS")
    failed = sum(1 for r in RESULTS if r["status"] != "PASS")

    print(f"\n{'=' * 60}")
    print(f"RESULTS: {passed}/{len(RESULTS)} passed, {failed} failed")
    print(f"{'=' * 60}")

    results_path = Path(__file__).parent.parent / "logs" / "test_results.json"
    results_path.parent.mkdir(parents=True, exist_ok=True)
    with open(results_path, "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "data_path": DATA_PATH,
            "total_tests": len(RESULTS),
            "passed": passed,
            "failed": failed,
            "results": RESULTS,
        }, f, indent=2)
    print(f"\nResults saved to: {results_path}")

    sys.exit(0 if failed == 0 else 1)
```


---

## File: `01_code_and_config/Global_Sales_Force__Auto_Shipping_Automation__bot_a_lead_quoting_engine_v2/home/ubuntu/bot_a_lead_quoting_engine/tests/test_pricing_engine.py`

| Field | Value |
|---|---|
| Kind | `text` |
| Size Bytes | 7598 |
| Extract Chars | 7533 |
| Truncated | False |

```text
"""
Tests for the Pricing Engine module.
Run with: python -m pytest tests/test_pricing_engine.py -v
"""

import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.pricing_engine import (
    PricingEngine,
    QuoteRequest,
    zip_to_state,
    is_golden_route,
)


def test_zip_to_state():
    """Test zip code to state mapping."""
    assert zip_to_state("90210") == "CA"  # Beverly Hills
    assert zip_to_state("10001") == "NY"  # Manhattan
    assert zip_to_state("33101") == "FL"  # Miami
    assert zip_to_state("77001") == "TX"  # Houston
    assert zip_to_state("98101") == "WA"  # Seattle
    assert zip_to_state("60601") == "IL"  # Chicago
    assert zip_to_state("07001") == "NJ"  # New Jersey
    assert zip_to_state("") is None
    assert zip_to_state("00") is None
    print("  zip_to_state: ALL PASSED")


def test_golden_routes():
    """Test Golden Route detection."""
    # CA → NY (East Coast) — should be golden
    assert is_golden_route("90210", "10001") is True
    # NY → CA (reverse) — should be golden
    assert is_golden_route("10001", "90210") is True
    # CA → TX — should be golden
    assert is_golden_route("90210", "77001") is True
    # CA → WA — should be golden
    assert is_golden_route("90210", "98101") is True
    # WA → FL — should be golden
    assert is_golden_route("98101", "33101") is True
    # WA → NJ — should be golden
    assert is_golden_route("98101", "07001") is True
    # CA → IL (Midwest) — should be golden
    assert is_golden_route("90210", "60601") is True
    # TX → FL — NOT a golden route
    assert is_golden_route("77001", "33101") is False
    # NY → FL — NOT a golden route
    assert is_golden_route("10001", "33101") is False
    print("  is_golden_route: ALL PASSED")


def test_pricing_engine_loads_data():
    """Test that the pricing engine loads the training data."""
    data_path = str(Path(__file__).parent.parent.parent /
                    "projects" / "global-sales-force-ba73233e" /
                    "Auto_Shipping_Training_Data_Combined.csv")

    engine = PricingEngine(training_data_path=data_path)
    stats = engine.get_stats()

    print(f"\n  Training Data Stats:")
    print(f"    Total moves:       {stats['total_moves']}")
    print(f"    Booked:            {stats['booked_count']}")
    print(f"    Quoted:            {stats['quoted_count']}")
    print(f"    Avg carrier price: ${stats['avg_carrier_price']:.2f}")
    print(f"    Price range:       ${stats['min_carrier_price']:.0f} - ${stats['max_carrier_price']:.0f}")
    print(f"    Date range:        {stats['date_range_start']} to {stats['date_range_end']}")

    assert stats["total_moves"] > 5000, "Should have loaded 5000+ records"
    print("  load_training_data: PASSED")


def test_find_comparable_moves():
    """Test finding comparable historical moves."""
    data_path = str(Path(__file__).parent.parent.parent /
                    "projects" / "global-sales-force-ba73233e" /
                    "Auto_Shipping_Training_Data_Combined.csv")

    engine = PricingEngine(training_data_path=data_path)

    # CA → NY route (should have many comparables)
    comparables = engine.find_comparable_moves("90210", "10001")
    print(f"\n  CA(90210) → NY(10001): {len(comparables)} comparables found")
    if comparables:
        print(f"    Most recent: #{comparables[0].id} — carrier ${comparables[0].carrier_price:.0f} "
              f"({comparables[0].dataset_source}, {comparables[0].created_at.strftime('%Y-%m-%d')})")

    # CA → TX route
    comparables_tx = engine.find_comparable_moves("90210", "77001")
    print(f"  CA(90210) → TX(77001): {len(comparables_tx)} comparables found")

    # WA → FL route
    comparables_wa_fl = engine.find_comparable_moves("98101", "33101")
    print(f"  WA(98101) → FL(33101): {len(comparables_wa_fl)} comparables found")

    print("  find_comparable_moves: PASSED")


def test_calculate_quote():
    """Test the full quote calculation pipeline."""
    data_path = str(Path(__file__).parent.parent.parent /
                    "projects" / "global-sales-force-ba73233e" /
                    "Auto_Shipping_Training_Data_Combined.csv")

    engine = PricingEngine(training_data_path=data_path)

    # Test 1: Golden Route — CA to NY (non-peak)
    request_1 = QuoteRequest(
        pickup_zip="90210",
        delivery_zip="10001",
        pickup_date=datetime(2026, 3, 15),  # March = non-peak
        customer_name="Test Customer",
        customer_email="test@example.com",
        company_name="Usa Autotransport",
    )
    result_1 = engine.calculate_quote(request_1)
    print(f"\n  Quote 1: CA→NY (non-peak, March)")
    print(f"    Carrier estimate:  ${result_1.carrier_price_estimate:.0f}")
    print(f"    Profit margin:     ${result_1.profit_margin:.0f}")
    print(f"    Customer quote:    ${result_1.customer_quote:.0f}")
    print(f"    Confidence:        {result_1.confidence}")
    print(f"    Comparables used:  {result_1.comparable_moves_count}")
    print(f"    Needs review:      {result_1.needs_human_review}")
    print(f"    Method:            {result_1.method}")

    # Test 2: Golden Route — CA to TX (peak season)
    request_2 = QuoteRequest(
        pickup_zip="90210",
        delivery_zip="77001",
        pickup_date=datetime(2026, 7, 15),  # July = peak
        customer_name="Test Customer 2",
        customer_email="test2@example.com",
        company_name="Flat Price Auto Transport",
    )
    result_2 = engine.calculate_quote(request_2)
    print(f"\n  Quote 2: CA→TX (peak, July)")
    print(f"    Carrier estimate:  ${result_2.carrier_price_estimate:.0f}")
    print(f"    Profit margin:     ${result_2.profit_margin:.0f}")
    print(f"    Customer quote:    ${result_2.customer_quote:.0f}")
    print(f"    Confidence:        {result_2.confidence}")
    print(f"    Comparables used:  {result_2.comparable_moves_count}")
    print(f"    Needs review:      {result_2.needs_human_review}")

    # Test 3: NON-Golden Route — should flag for human review
    request_3 = QuoteRequest(
        pickup_zip="77001",  # TX
        delivery_zip="33101",  # FL
        pickup_date=datetime(2026, 4, 15),
        customer_name="Test Customer 3",
        customer_email="test3@example.com",
    )
    result_3 = engine.calculate_quote(request_3)
    print(f"\n  Quote 3: TX→FL (non-golden route)")
    print(f"    Customer quote:    ${result_3.customer_quote:.0f}")
    print(f"    Needs review:      {result_3.needs_human_review}")
    print(f"    Review reason:     {result_3.review_reason}")

    assert result_1.customer_quote > 0, "Golden route should produce a quote"
    assert result_1.profit_margin == 100, "Profit margin should be $100"
    assert result_3.needs_human_review is True, "Non-golden route should need review"
    print("\n  calculate_quote: ALL PASSED")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  BOT A — PRICING ENGINE TESTS")
    print("=" * 60)

    print("\n[1] Testing zip_to_state...")
    test_zip_to_state()

    print("\n[2] Testing golden route detection...")
    test_golden_routes()

    print("\n[3] Testing training data loading...")
    test_pricing_engine_loads_data()

    print("\n[4] Testing comparable move finder...")
    test_find_comparable_moves()

    print("\n[5] Testing full quote calculation...")
    test_calculate_quote()

    print("\n" + "=" * 60)
    print("  ALL TESTS PASSED")
    print("=" * 60 + "\n")
```


---

## File: `02_docs_and_strategy/Global_Sales_Force__Auto_Shipping_Automation__bot_a_lead_quoting_engine_v2/home/ubuntu/bot_a_lead_quoting_engine/README.md`

| Field | Value |
|---|---|
| Kind | `text` |
| Size Bytes | 2443 |
| Extract Chars | 2379 |
| Truncated | False |

```text
# Bot A: Lead Quoting Engine

**Automated auto shipping quote generator for Global Sales Force.**

Monitors the sales inbox for new auto shipping leads, calculates competitive quotes using historical pricing data and Alex's pricing algorithm, and sends professional quote emails to customers — all running locally on the OpenClaw Mini PC at ~$0.30/month.

## Architecture

```
Email Inbox (IMAP)
       │
       ▼
  Lead Ingestion ──► LLM parses email into structured data
       │
       ▼
  Pricing Engine ──► Historical lookup → Recency check → Seasonal adjustment → $100 margin
       │
       ▼
  Quote Delivery ──► LLM drafts email → SMTP sends to customer
       │
       ▼
  Audit Log (JSONL) + Seneca notification (if review needed)
```

## Quick Start

```bash
# 1. Clone and enter directory
cd bot_a_lead_quoting_engine

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy and configure environment
cp .env.example .env
# Edit .env with your credentials

# 4. Place training data
cp /path/to/Auto_Shipping_Training_Data_Combined.csv data/

# 5. Run the bot
python main.py              # Daemon mode (24/7)
python main.py --test       # Single cycle test
python main.py --stats      # View pricing stats
python main.py --quote      # Interactive quote calculator
```

## Modules

| Module | File | Purpose |
|--------|------|---------|
| Config | `config/settings.py` | Centralized settings from .env |
| Pricing Engine | `modules/pricing_engine.py` | Historical price lookup + algorithm |
| Lead Ingestion | `modules/lead_ingestion.py` | IMAP email monitor + LLM parser |
| Quote Delivery | `modules/quote_delivery.py` | Email generation + SMTP sender |
| Orchestrator | `main.py` | Daemon loop tying everything together |

## Pricing Algorithm (v2)

1. Find comparable moves (same route corridor, ±30 days)
2. If recent (within 1 month): use that carrier price
3. If old or non-peak → peak transition: add $150
4. If peak → peak (year-over-year): compare last summer vs current; add $50-100 if current ≥ last summer
5. Add $100 flat profit margin (Golden Routes) or $150+ (non-Golden)
6. Flag for human review if <3 comparables or confidence is low

## Golden Routes (Auto-Quote Eligible)

- CA ↔ All East Coast
- CA ↔ Midwest
- CA ↔ TX
- CA ↔ WA
- WA ↔ FL
- WA ↔ NY/NJ

## Cost

~$0.30/month (Gemini Flash API for ~1,000 email parses + quote drafts)
```


---

## File: `02_docs_and_strategy/Global_Sales_Force__Auto_Shipping_Automation__bot_a_lead_quoting_engine_v2/home/ubuntu/bot_a_lead_quoting_engine/requirements.txt`

| Field | Value |
|---|---|
| Kind | `text` |
| Size Bytes | 346 |
| Extract Chars | 343 |
| Truncated | False |

```text
# Bot A: Lead Quoting Engine — Dependencies
# All lightweight, no heavy ML frameworks needed

python-dotenv>=1.0.0     # Environment variable management
requests>=2.31.0         # HTTP client for LLM APIs
openai>=1.0.0            # OpenAI-compatible API client (optional, for fallback)
pandas>=2.0.0            # Data handling for training CSV
```


---

## File: `03_data_and_spreadsheets/Global_Sales_Force__Auto_Shipping_Automation__bot_a_lead_quoting_engine_v2/home/ubuntu/bot_a_lead_quoting_engine/data/Auto_Shipping_Training_Data_Combined.csv`

| Field | Value |
|---|---|
| Kind | `csv_text` |
| Size Bytes | 8124960 |
| Extract Chars | 56861 |
| Truncated | False |

```text
origin_city,origin_state,dest_city,dest_state,pickup_date,delivery_date,month,offer_price,carrier_price,profit_markup,profit_pct,vehicle_raw,vehicle_year,vehicle_make,vehicle_model,vehicle_type,carrier_name,customer_name,pickup_zip,delivery_zip,status,notes,payment_form,payment_date,dataset_source,sheet_source,cd_order_id,reference_number,company_name,source_name,email,phone
SCHENECTADY,,OAKLEY,,2026-12-22,,2025-03,1695.0,1300.0,395.0,30.4,,,,,,,Leah Ramos,12309.0,94561.0,ACTIVE,,,,QUOTED,UM_CRM,,372561,Flat Price Auto Transport,Better Business Bureau,leah.l.ramos@gmail.com,15189869052.0
,,,,2026-12-14,,2026-02,1231.0,900.0,250.0,27.8,,,,,,,Sheila Taylor,78130.0,42101.0,ACTIVE,,,,QUOTED,UM_CRM,,388485,Flat Price Auto Transport,Google,sheilasangelz@gmail.com,18156716818.0
PUYALLUP,,HOUSTON,,2026-12-09,,2025-03,1350.0,1000.0,286.0,28.6,,,,,,,Sulaiman  Zadran,98374.0,77074.0,ACTIVE,,,,QUOTED,UM_CRM,,373527,Usa Autotransport,Website,alpha4su@gmail.com,18329193000.0
,,,,2026-12-08,,2025-03,1575.0,1200.0,300.0,25.0,,,,,,,Nicole DeFranco,43964.0,90802.0,ACTIVE,,,,QUOTED,UM_CRM,,372975,Usa Autotransport,Google,nicoleallendefranco@gmail.com,14126801403.0
,,,,2026-12-04,,2025-03,2200.0,1600.0,495.0,30.9,,,,,,,Kartik Madhira,1702.0,92126.0,ACTIVE,,,,QUOTED,UM_CRM,,373551,East Coast West Coast Express,Google,kartikmadhira1@gmail.com,13012046989.0
TARZANA,,HAVANA,,2026-12-04,,2025-03,1470.0,1100.0,300.0,27.3,,,,,,,Bradley  ,91356.0,32333.0,ACTIVE,,,,QUOTED,UM_CRM,,373217,Cross Country Moving,Old Gen Lead,atlanteum@gmail.com,13109480072.0
,,,,2026-12-03,,2025-04,1100.0,800.0,248.0,31.0,,,,,,,Ryan Cummings,94901.0,85044.0,ACTIVE,,,,QUOTED,UM_CRM,,374683,Usa Autotransport,Google,ryandcummings22@gmail.com,16103292944.0
,,,,2026-12-02,,2025-04,1890.0,1450.0,350.0,24.1,,,,,,,Seth Karpinski,97401.0,14623.0,ACTIVE,,,,QUOTED,UM_CRM,,374288,Usa Autotransport,Google,sethislove@gmail.com,15415542950.0
,,,,2026-12-02,,2025-12,800.0,550.0,212.0,38.5,,,,,,,Mike Erick,15120.0,30033.0,ACTIVE,,,,QUOTED,UM_CRM,,385817,Usa Autotransport,Google,bobie8398@gmail.com,18049161910.0
,,,,2026-12-01,,2025-10,3577.0,1000.0,150.0,15.0,,,,,,,R M,89166.0,46530.0,ACTIVE,,,,QUOTED,UM_CRM,,384486,Flat Price Auto Transport,Website,dwayner2001@gmail.com,15742869073.0
BENSALEM,,,,2026-11-21,,2026-04,3200.0,2700.0,291.0,10.8,,,,,,,Emily Dunyo,19020.0,98102.0,ACTIVE,,,,QUOTED,UM_CRM,,390858,Cross Country Movers,Google Ads,emilyantoniadunyo@gmail.com,12676144152.0
,,HARTSELLE,,2026-11-06,,2025-04,1733.0,1300.0,350.0,26.9,,,,,,,Raven Johnson,95926.0,35640.0,ACTIVE,,,,QUOTED,UM_CRM,,374171,Usa Autotransport,Website,ravenjohnson1964@icloud.com,12563452085.0
JERSEY CITY,,MINNEAPOLIS,,2026-11-06,,2025-04,1050.0,750.0,250.0,33.3,,,,,,,NJ ,7306.0,55443.0,ACTIVE,,,,QUOTED,UM_CRM,,373846,Usa Autotransport,Old Gen Lead,lksadklsmkdlm@gmail.com,15516979544.0
SAMMAMISH,,ALTAMONTE SPRINGS,,2026-11-05,,2025-04,1628.0,1250.0,300.0,24.0,,,,,,,Lady ,98074.0,32714.0,ACTIVE,,,,QUOTED,UM_CRM,,374020,Flat Price Auto Transport,Old Gen Lead,lksadlksamdlM@gmail.com,14087040859.0
SOUTH JORDAN,,ORLANDO,,2026-11-04,,2025-04,1365.0,1050.0,250.0,23.8,,,,,,,Elizabeth  Longhurst ,84095.0,32836.0,ACTIVE,,,,QUOTED,UM_CRM,,374666,Flat Price Auto Transport,Old Gen Lead,asdlksmKMLKM@gmail.com,18018597205.0
,,,,2026-10-30,,2025-10,532.0,300.0,207.0,69.0,,,,,,,Joyce Glucksman,80401.0,30345.0,ACTIVE,,,,QUOTED,UM_CRM,,384575,Usa Autotransport,Website,joy@joycefglucksman.com,16789846663.0
SEATTLE,,RANCHO MIRAGE,,2026-10-01,,2026-03,1175.0,900.0,198.0,22.0,,,,,,,Linda /,98168.0,92270.0,ACTIVE,,,,QUOTED,UM_CRM,,389384,State 2 State Movers,Google,lindaplaceholder@yahoo.com,12063721031.0
,,,,2026-10-01,,2026-03,1391.0,1000.0,300.0,30.0,,,,,,,Shannon Brown,80104.0,32772.0,ACTIVE,,,,QUOTED,UM_CRM,,389788,Usa Autotransport,Google,Jabncb@yahoo.com,18057465789.0
HELOTES,,LAS VEGAS,,2026-10-01,,2025-12,1450.0,1050.0,331.0,31.5,,,,,,,Craig ,78023.0,89110.0,ACTIVE,,,,QUOTED,UM_CRM,,386639,East Coast West Coast Express,SMS Marketing,craigaustralia@hotmail.com,19292045451.0
,,,,2026-10-01,,2026-03,1338.0,1050.0,200.0,19.0,,,,,,,Joe Roux,98168.0,92270.0,ACTIVE,,,,QUOTED,UM_CRM,,389061,State 2 State Movers,Google,joeykroux@gmail.com,12064754532.0
,,,,2026-10-01,,2026-03,1070.0,700.0,300.0,42.9,,,,,,,Virginia Barta,98579.0,83263.0,ACTIVE,,,,QUOTED,UM_CRM,,389243,Long Distance Movers,Yelp,vbarta111@gmail.com,19145889735.0
,,,,2026-10-01,,2025-11,1399.0,999.0,333.0,33.3,,,,,,,Phillip Fife,89117.0,16502.0,ACTIVE,,,,QUOTED,UM_CRM,,385416,Flat Price Auto Transport,Google,jphillip747@icloud.com,18145723259.0
,,,,2026-09-30,,2026-01,1498.0,1100.0,300.0,27.3,,,,,,,Omar Haddad,85282.0,11004.0,ACTIVE,,,,QUOTED,UM_CRM,,387548,Usa Autotransport,Google,ohaddad0586@gmail.com,16233967562.0
,,,,2026-09-30,,2026-04,1712.0,1300.0,300.0,23.1,,,,,,,JEROME MORRIS,58104.0,30909.0,ACTIVE,,,,QUOTED,UM_CRM,,390335,State 2 State Movers,Google,Scemeboy@gmail.com,17012004094.0
,,,,2026-09-30,,2026-04,2121.0,1649.0,333.0,20.2,,,,,,,Stephanie Gard,34210.0,98391.0,ACTIVE,,,,QUOTED,UM_CRM,,390527,Cross Country Movers,Facebook,stephanie.m.gard@gmail.com,12533809097.0
,,,,2026-09-29,,2026-04,2568.0,2000.0,400.0,20.0,,,,,,,Gary Fuller,13317.0,90045.0,ACTIVE,,,,QUOTED,UM_CRM,,390913,Usa Autotransport,Google,Garyfuller031@gmail.com,15188522833.0
,,,,2026-09-25,,2026-04,1800.0,1349.0,333.0,24.7,,,,,,,Peter Lee,89102.0,19130.0,ACTIVE,,,,QUOTED,UM_CRM,,390342,East Coast West Coast Express,Google,nadapeter@gmail.com,15109102613.0
,,,,2026-09-24,,2026-04,1868.0,1550.0,196.0,12.6,,,,,,,Kimbirly Thomas,35816.0,93065.0,ACTIVE,,,,QUOTED,UM_CRM,,390272,East Coast West Coast Express,Google,lenorathomas16@yahoo.com,12566941635.0
RENO,,POWELL,,2026-09-21,,2026-02,1776.0,1325.0,335.0,25.3,,,,,,,Bob Ellis,89506.0,37849.0,DEAD,,,,QUOTED,UM_CRM,,388154,Usa Autotransport,Google,crazydadbe@yahoo.com,17753787231.0
,,,,2026-09-13,,2026-02,1598.0,1200.0,293.0,24.4,,,,,,,Jennifer Gawith,22602.0,84015.0,ACTIVE,,,,QUOTED,UM_CRM,,387984,Usa Autotransport,Website,jagawith@yahoo.com,15419694853.0
MILWAUKEE,,ALBUQUERQUE,,2026-09-07,,2026-02,2058.0,700.0,323.0,46.1,,,,,,,Kevin Tarkington,53223.0,87121.0,ACTIVE,,,,QUOTED,UM_CRM,,388767,Flat Price Auto Transport,Yelp,ktarkingtonassoc@yahoo.com,16127159696.0
SCHERERVILLE,,AUSTELL,,2026-09-01,,2025-11,690.0,450.0,207.0,46.0,,,,,,,Charlene /,46375.0,30106.0,ACTIVE,,,,QUOTED,UM_CRM,,385103,State 2 State Movers,Old Gen Lead,charlenenextyear@gmail.com,12197771454.0
GRESHAM,,MENDOTA,,2026-09-01,,2026-04,1425.0,999.0,333.0,33.3,,,,,,,Mike Snow,97080.0,55150.0,ACTIVE,,,,QUOTED,UM_CRM,,390822,East Coast West Coast Express,Referral,joseph@eastcoastwestcoastmovers.edu,15035448942.0
,,,,2026-08-31,,2026-04,1425.0,999.0,333.0,33.3,,,,,,,Mason Wheeler,1945.0,92109.0,ACTIVE,,,,QUOTED,UM_CRM,,391048,Usa Autotransport,Yelp,masonbot5@gmail.com,13392933111.0
,,,,2026-08-31,,2026-03,1097.0,750.0,275.0,36.7,,,,,,,Dennis Smith,63146.0,23832.0,ACTIVE,,,,QUOTED,UM_CRM,,389875,Flat Price Auto Transport,Google,Dennis.smith30@outlook.com,13142584352.0
MESA,,BALTIMORE,,2026-08-22,,2026-04,1497.0,999.0,400.0,40.0,,,,,,,Tonia Walker,85212.0,21205.0,ACTIVE,,,,QUOTED,UM_CRM,,390730,East Coast West Coast Express,Website,tmfwalker@gmail.com,13179794295.0
,,,,2026-08-21,,2025-11,1399.0,999.0,333.0,33.3,,,,,,,Celeste Lucero,80021.0,29078.0,ACTIVE,,,,QUOTED,UM_CRM,,385123,Usa Autotransport,Website,celucero7@comcast.net,13036533751.0
BETHESDA,,CAMPBELL,,2026-08-21,,2026-03,1605.0,1300.0,200.0,15.4,,,,,,,Rahul Phadnis,20814.0,95008.0,ACTIVE,,,,QUOTED,UM_CRM,,389588,Trico Long Distance Movers,Website,that.rahulphadnis@gmail.com,14086366678.0
,,,,2026-08-19,,2026-04,1926.0,1500.0,300.0,20.0,,,,,,,Shai Iredale,98026.0,29566.0,ACTIVE,,,,QUOTED,UM_CRM,,390302,Long Distance Movers,Yelp,shai.simone04@gmail.com,18433719950.0
,,,,2026-08-17,,2025-11,1445.0,1100.0,250.0,22.7,,,,,,,Jeff King,86442.0,57042.0,ACTIVE,,,,QUOTED,UM_CRM,,385729,Usa Autotransport,Google,Jking7@hotmail.com,19282990785.0
,,,,2026-08-15,,2026-02,1338.0,1000.0,250.0,25.0,,,,,,,Valentine Boyer,58103.0,11590.0,ACTIVE,,,,QUOTED,UM_CRM,,388901,East Coast West Coast Express,Website,Boyerv1218@yahoo.com,19733914717.0
,,,,2026-08-14,,2026-04,1552.0,1200.0,250.0,20.8,,,,,,,Emily Murphy,85012.0,21043.0,BOOKED,,,,BOOKED,UM_CRM,,390554,Usa Autotransport,Google,emilymurphy0494@gmail.com,14438676592.0
,,,,2026-08-13,,2026-04,1091.0,800.0,220.0,27.5,,,,,,,Heidi Farr,80231.0,60506.0,ACTIVE,,,,QUOTED,UM_CRM,,390970,Usa Autotransport,Yelp,heidi.m.farr@gmail.com,13033322432.0
,,,,2026-08-12,,2026-04,1178.0,850.0,251.0,29.5,,,,,,,Precious Charles,33169.0,60515.0,ACTIVE,,,,QUOTED,UM_CRM,,390113,Usa Autotransport,Website,pwcharles25@gmail.com,17866672481.0
,,,,2026-08-12,,2026-03,1284.0,1000.0,200.0,20.0,,,,,,,Natalie Bryson,80015.0,33618.0,ACTIVE,,,,QUOTED,UM_CRM,,389154,Usa Autotransport,Google,Nataliebryson9@gmail.com,13605502298.0
COMPTON,,DALLAS,,2026-08-12,,2026-04,1111.0,816.0,222.0,27.2,,,,,,,Natalie Martinez,90222.0,75241.0,ACTIVE,,,,QUOTED,UM_CRM,,390801,Cross Country Movers,Website,NatalieMartinez876@gmail.com,13236158758.0
,,,,2026-08-08,,2026-04,1498.0,1100.0,300.0,27.3,,,,,,,Katie Nunez,93312.0,37916.0,ACTIVE,,,,QUOTED,UM_CRM,,390716,Usa Autotransport,Website,katiemeador@yahoo.com,16613195453.0
,,,,2026-08-07,,2026-02,1675.0,1300.0,265.0,20.4,,,,,,,Josie LeCompte,80210.0,2467.0,ACTIVE,,,,QUOTED,UM_CRM,,388866, Long Distance Movers,Yelp,josie.lecompte@yahoo.com,13033926886.0
,,,,2026-08-07,,2026-01,1445.0,1100.0,250.0,22.7,,,,,,,Gerardo Olivares,91942.0,78660.0,ACTIVE,,,,QUOTED,UM_CRM,,386756,State 2 State Movers,Website,Gthecreator101@gmail.com,16198873845.0
,,,,2026-08-04,,2026-04,795.0,493.0,250.0,50.7,,,,,,,Jack Stoltz,78701.0,30110.0,BOOKED,,,,BOOKED,UM_CRM,,390500,Cross Country Movers,Facebook,JStoltz5@gmail.com,16467995047.0
,,,,2026-08-04,,2026-03,1552.0,1250.0,200.0,16.0,,,,,,,Jhanic Ramos,93905.0,32223.0,ACTIVE,,,,QUOTED,UM_CRM,,389047,Usa Autotransport,Google,jhaniclramos@gmail.com,18317709299.0
,,,,2026-08-01,,2025-12,1712.0,1200.0,400.0,33.3,,,,,,,Melissa Barnes,22046.0,94949.0,ACTIVE,,,,QUOTED,UM_CRM,,386133,Cross Country Movers,Website,Melissawbarnes@gmail.com,15714356570.0
BROOKLYN,,MATTHEWS,,2026-08-01,,2026-03,998.0,700.0,233.0,33.3,,,,,,,Monica ,11202.0,28105.0,ACTIVE,,,,QUOTED,UM_CRM,,389578,Cross Country Moving,Google,monica.annemarie@proton.me,13137566883.0
,,,,2026-07-31,,2026-03,1873.0,1450.0,300.0,20.7,,,,,,,Marianne Husberg,90277.0,20147.0,BOOKED,,,,BOOKED,UM_CRM,,389563,Usa Autotransport,Website,marianne_harmon@yahoo.com,16509064666.0
,,,,2026-07-30,,2026-03,1391.0,950.0,350.0,36.8,,,,,,,Aneisha Ralph,89110.0,20735.0,ACTIVE,,,,QUOTED,UM_CRM,,389842,Usa Autotransport,Website,aralph_1994@yahoo.com,19122272483.0
,,,,2026-07-26,,2026-03,1284.0,900.0,300.0,33.3,,,,,,,Annette Jackson-Thomas,53051.0,28115.0,ACTIVE,,,,QUOTED,UM_CRM,,389293,Usa Autotransport,Google,annette_jthomas@hotmail.com,14143501958.0
,,,,2026-07-25,,2026-03,1338.0,1000.0,250.0,25.0,,,,,,,Aiesha Morrison,60409.0,98133.0,ACTIVE,,,,QUOTED,UM_CRM,,389425,Long Distance Movers,Yelp,aieshanmorrison@gmail.com,17733289916.0
,,,,2026-07-20,,2026-03,1926.0,1600.0,200.0,12.5,,,,,,,Thet Bhone Naing,33174.0,94085.0,ACTIVE,,,,QUOTED,UM_CRM,,390094,Usa Autotransport,Website,thetbhonenaing040@gmail.com,17863568899.0
,,,,2026-07-20,,2026-04,1231.0,450.0,150.0,33.3,,,,,,,Sandra Martinez,85031.0,79925.0,ACTIVE,,,,QUOTED,UM_CRM,,390537,State 2 State Movers,Google,sandy.mtz.1988@gmail.com,16024655061.0
SURPRISE,,PEARLAND,,2026-07-20,,2026-04,1391.0,1000.0,300.0,30.0,,,,,,,Trinity Black,85379.0,77581.0,ACTIVE,,,,QUOTED,UM_CRM,,391003,Flat Price Auto Transport,Google,na@gmail.com,17733836705.0
,,,,2026-07-19,,2026-02,1156.0,880.0,200.0,22.7,,,,,,,Isaac Salcido,80204.0,28307.0,ACTIVE,,,,QUOTED,UM_CRM,,388731,Cross Country Movers,Website,Isaacsalcido74@gmail.com,15055540258.0
,,,,2026-07-19,,2026-04,1552.0,1200.0,250.0,20.8,,,,,,,Brittney Harris,90302.0,30303.0,ACTIVE,,,,QUOTED,UM_CRM,,390703,Usa Autotransport,Google,Msbrittneyharris@gmail.com,15622345808.0
,,,,2026-07-18,,2026-03,1338.0,850.0,400.0,47.1,,,,,,,Roxanne Harutyunyan,91201.0,77493.0,ACTIVE,,,,QUOTED,UM_CRM,,389716,Cross Country Movers,Website,Rojo9293@yahoo.com,18184845199.0
,,,,2026-07-17,,2025-11,1391.0,1000.0,300.0,30.0,,,,,,,Lyn Wells,34287.0,2132.0,ACTIVE,,,,QUOTED,UM_CRM,,384815,Cross Country Movers,Website,Lynsyns46@Gmail.com,16174350131.0
TUCSON,,WEST HAVEN,,2026-07-15,,2025-03,1552.0,1200.0,250.0,20.8,,,,,,,Chloe Jacobs,85745.0,6516.0,ACTIVE,,,,QUOTED,UM_CRM,,373250,East Coast West Coast Express,Return Customer,cscrn21@gmail.com,12036849267.0
BROOKINGS,,ALIQUIPPA,,2026-07-15,,2026-04,2164.0,1800.0,222.0,12.3,,,,,,,Tristen Lawson,97415.0,15001.0,ACTIVE,,,,QUOTED,UM_CRM,,391060,Cross Country Movers,Website,TristenLawson1@gmail.com,15412540838.0
,,,,2026-07-15,,2026-03,1165.0,788.0,301.0,38.2,,,,,,,Kate Lygrisse,11501.0,77019.0,ACTIVE,,,,QUOTED,UM_CRM,,389752,Cross Country Moving,Google,Klygrisse@gmail.com,13169905752.0
,,,,2026-07-15,,2026-03,2461.0,950.0,200.0,21.1,,,,,,,AMANDA MCCLOUD,53209.0,75002.0,ACTIVE,,,,QUOTED,UM_CRM,,389828,Usa Autotransport,Google,EXQUISITELADY471@YAHOO.COM,14147226344.0
SAN DIEGO,,GENEVA,,2026-07-15,,2025-12,1715.0,1300.0,333.0,25.6,,,,,,,Curt Lewis,92116.0,14456.0,ACTIVE,,,,QUOTED,UM_CRM,,386670,Cross Country Moving,Google,cdub707@aol.com,19519708070.0
,,,,2026-07-15,,2026-04,514.0,1300.0,180.0,13.8,,,,,,,DAVID CLARK,34606.0,4224.0,ACTIVE,,,,QUOTED,UM_CRM,,391004,Usa Autotransport,Google,dixfield1959@gmail.com,13529423856.0
,,,,2026-07-14,,2026-04,1625.0,1122.0,397.0,35.4,,,,,,,Jamie Howard,20769.0,90746.0,ACTIVE,,,,QUOTED,UM_CRM,,391148,Cross Country Movers,Google,callerealhome@gmail.com,18056896659.0
,,,,2026-07-14,,2026-03,798.0,522.0,224.0,42.9,,,,,,,Lola Morodolu,73132.0,30301.0,ACTIVE,,,,QUOTED,UM_CRM,,389723,Flat Price Auto Transport,Website,lolamorodolu@gmail.com,14055350295.0
,,,,2026-07-13,,2026-04,2308.0,1000.0,307.0,30.7,,,,,,,Linda Kruger,91945.0,98405.0,BOOKED,,,,BOOKED,UM_CRM,,390585, Long Distance Movers,Website,lkruger808@gmail.com,18083423892.0
,,,,2026-07-10,,2026-02,1712.0,1300.0,300.0,23.1,,,,,,,tan nguyen,13210.0,79938.0,ACTIVE,,,,QUOTED,UM_CRM,,388602,Usa Autotransport,Google,tanrom84@yahoo.com,17134259102.0
SUNNYVALE,,WABAN,,2026-07-10,,2026-04,1888.0,1542.3,222.0,14.4,,,,,,,Amy kim,94086.0,2468.0,ACTIVE,,,,QUOTED,UM_CRM,,390490,Cross Country Movers,Yelp,amyyeonsoo@gmail.com,16098644148.0
,,,,2026-07-07,,2026-02,942.0,830.0,50.0,6.0,,,,,,,Madeline Booze,21237.0,77002.0,ACTIVE,,,,QUOTED,UM_CRM,,388697,State 2 State Movers,Google,Transactions.chg@gmail.com,16676570002.0
,,,,2026-07-06,,2025-11,2287.0,1800.0,360.0,20.0,,,,,,,Julieta Abad,2125.0,95123.0,BOOKED,,,,BOOKED,UM_CRM,,385771,State 2 State Movers,Website,jtrabad@gmail.com,14086748394.0
BROOKLYN,,SEATTLE,,2026-07-03,,2026-03,1500.0,1050.0,352.0,33.5,,,,,,,Natalie Sue Johnson,11231.0,98117.0,BOOKED,,,,BOOKED,UM_CRM,,389441,Usa Autotransport,Return Customer,natalie.sue.johnson@gmail.com,15037028317.0
LUTZ,,WARRENVILLE,,2026-07-01,,2026-03,1177.0,800.0,300.0,37.5,,,,,,,Alvis Lee,33558.0,60555.0,ACTIVE,,,,QUOTED,UM_CRM,,389686,Usa Autotransport,Return Customer,x_alvis@yahoo.com,14084804322.0
,,,,2026-07-01,,2026-03,963.0,550.0,350.0,63.6,,,,,,,Diane Malloy,92037.0,97212.0,ACTIVE,,,,QUOTED,UM_CRM,,389706,Usa Autotransport,Website,Mdtm07@gmail.com,13106016967.0
,,,,2026-07-01,,2026-04,1558.0,1200.0,256.0,21.3,,,,,,,Ryan Krochko,89135.0,98109.0,ACTIVE,,,,QUOTED,UM_CRM,,391091,California Seattle Express,Website,ryan.krochko@gmail.com,14157697061.0
HENDERSON,,NASHVILLE,,2026-07-01,,2026-03,1775.0,900.0,759.0,84.3,,,,,,,Kat ,89052.0,37203.0,ACTIVE,,,,QUOTED,UM_CRM,,389507,Usa Autotransport,Return Customer,kdk3226@yahoo.com,14106884523.0
,,,,2026-07-01,,2026-03,1498.0,1100.0,300.0,27.3,,,,,,,Rebecca Seickel,27523.0,80222.0,ACTIVE,,,,QUOTED,UM_CRM,,389618,Long Distance Movers,Website,rseickel@outlook.com,12019695885.0
,,,,2026-06-30,,2026-04,2301.0,1800.0,350.0,19.4,,,,,,,Amy Kim,94086.0,2468.0,ACTIVE,,,,QUOTED,UM_CRM,,390156,Usa Autotransport,Yelp,amyyeonsoo@gmail.com,16098644148.0
,,,,2026-06-30,,2026-04,1888.0,1542.3,222.0,14.4,,,,,,,Amy kim,94086.0,2468.0,ACTIVE,,,,QUOTED,UM_CRM,,390155,Cross Country Movers,Yelp,amyyeonsoo@gmail.com,16098644148.0
,,,,2026-06-30,,2026-02,1605.0,1200.0,300.0,25.0,,,,,,,Flor Valverde,92691.0,28202.0,ACTIVE,,,,QUOTED,UM_CRM,,388001,Usa Autotransport,Google,fvalro@hotmail.com,19492454100.0
,,,,2026-06-30,,2026-01,1498.0,1100.0,300.0,27.3,,,,,,,Nicholas Tuitele,94709.0,30340.0,ACTIVE,,,,QUOTED,UM_CRM,,387189,Cross Country Moving,Website,ngtuitele@gmail.com,18059908807.0
,,,,2026-06-30,,2026-02,1284.0,1000.0,200.0,20.0,,,,,,,Kati Padilla,10990.0,34613.0,ACTIVE,,,,QUOTED,UM_CRM,,388753,Cross Country Moving,Google,Katipadilla@aol.com,18457757830.0
,,,,2026-06-30,,2026-02,1445.0,1100.0,250.0,22.7,,,,,,,Jeannette Bastin,28570.0,98122.0,ACTIVE,,,,QUOTED,UM_CRM,,387967,Usa Autotransport,Website,jeannettebastin@gmail.com,17608454291.0
FAYETTEVILLE,,SAN ANTONIO,,2026-06-29,,2026-04,3317.0,1400.0,250.0,17.9,,,,,,,Deepa  ,13066.0,78249.0,ACTIVE,,,,QUOTED,UM_CRM,,390720,Usa Autotransport,Better Business Bureau,drspdeeparavi@gmail.com,13154139757.0
TORRANCE,,FORT WORTH,,2026-06-29,,2026-03,1145.0,850.0,220.0,25.9,,,,,,,Salim Rashad,90504.0,76120.0,BOOKED,,,,BOOKED,UM_CRM,,390084,Flat Price Auto Transport,Return Customer,szrashad@gmail.com,18176300406.0
,,,,2026-06-29,,2026-01,1498.0,1100.0,300.0,27.3,,,,,,,David Bunyard,89143.0,33578.0,ACTIVE,,,,QUOTED,UM_CRM,,387460,Usa Autotransport,Google,doubleclutcher702@yahoo.com,17022414300.0
POWELL,,SAN FRANCISCO,,2026-06-29,,2026-04,1503.0,1150.0,255.0,22.2,,,,,,,Marian Saad,43065.0,94108.0,ACTIVE,,,,QUOTED,UM_CRM,,390312,Usa Autotransport,Google,marian.saad@gmail.com,16145579333.0
MINNEAPOLIS,,WESTMINSTER,,2026-06-28,,2025-12,2625.0,900.0,350.0,38.9,,,,,,,Tina Tran,55425.0,92683.0,ACTIVE,,,,QUOTED,UM_CRM,,386186,State 2 State Movers,Old Gen Lead,tinachangplaceholder@yahoo.com,19522126858.0
NORTH LAS VEGAS,,FORT WORTH,,2026-06-28,,2026-04,1213.0,850.0,284.0,33.4,,,,,,,Gene Davis,89084.0,76101.0,BOOKED,,,,BOOKED,UM_CRM,,390948,Usa Autotransport,Google,gened2783@gmail.com,17753573323.0
,,,,2026-06-28,,2026-02,1390.0,999.0,300.0,30.0,,,,,,,Terry Selucky,91403.0,60202.0,ACTIVE,,,,QUOTED,UM_CRM,,387986,Cross Country Movers,Website,terry.selucky@gmail.com,19172024192.0
CANAL WINCHESTER,,SAN ANTONIO,,2026-06-28,,2026-04,1605.0,1300.0,200.0,15.4,,,,,,,Sarah ,43110.0,78201.0,ACTIVE,,,,QUOTED,UM_CRM,,390784,Flat Price Auto Transport,Google,brt2sarah@gmail.com,16144034205.0
,,,,2026-06-28,,2025-12,1313.0,1000.0,250.0,25.0,,,,,,,Anusha Singh,20009.0,77002.0,ACTIVE,,,,QUOTED,UM_CRM,,386205,Flat Price Auto Transport,Website,anusha.singh405@gmail.com,17818014865.0
,,,,2026-06-27,,2026-03,1270.0,1000.0,187.0,18.7,,,,,,,Elizabeth Cappello,30309.0,11373.0,ACTIVE,,,,QUOTED,UM_CRM,,389327,Usa Autotransport,Yelp,emcappe@me.com,19175836113.0
,,,,2026-06-27,,2026-03,1673.0,1164.0,400.0,34.4,,,,,,,Kelvin Zhong,43212.0,77001.0,ACTIVE,,,,QUOTED,UM_CRM,,389731,Usa Autotransport,Website,kelvinzhong122@yahoo.com,16269277017.0
TACOMA,,AUSTIN,,2026-06-25,,2026-04,1391.0,1050.0,250.0,23.8,,,,,,,Claire Keepers,98404.0,78744.0,BOOKED,,,,BOOKED,UM_CRM,,391022,Usa Autotransport,Yelp,clairekprs@gmail.com,15204053760.0
,,,,2026-06-25,,2026-04,874.0,767.0,50.0,6.5,,,,,,,Emily Zhou,92373.0,98059.0,BOOKED,,,,BOOKED,UM_CRM,,390755, Long Distance Movers,Yelp,emilyzandandrewk@gmail.com,15717661029.0
FORT WORTH,,TORRANCE,,2026-06-24,,2026-04,1145.0,850.0,220.0,25.9,,,,,,,Salim Rashad,76120.0,90504.0,BOOKED,,,,BOOKED,UM_CRM,,390128,Flat Price Auto Transport,Return Customer,szrashad@gmail.com,18176300406.0
,,,,2026-06-23,,2026-04,963.0,600.0,300.0,50.0,,,,,,,ANGELA WANG,64111.0,48105.0,BOOKED,,,,BOOKED,UM_CRM,,390648,Kerb,Google,cumcsummer@gmail.com,13477513096.0
HUNTINGTON BEACH,,,,2026-06-23,,2026-04,1605.0,1200.0,300.0,25.0,,,,,,,John Moss,92646.0,30253.0,ACTIVE,,,,QUOTED,UM_CRM,,390484,Cross Country Movers,Website,jvmbusiness@gmail.com,19513888811.0
MIDDLETON,,FOLSOM,,2026-06-23,,2026-04,1498.0,1200.0,200.0,16.7,,,,,,,Cat Hatsell,53562.0,95630.0,BOOKED,,,,BOOKED,UM_CRM,,390305,Usa Autotransport,Return Customer,kathleenhatsell@gmail.com,16507870967.0
MILL VALLEY,,WEST HARTFORD,,2026-06-23,,2026-04,1898.0,1600.0,174.0,10.9,,,,,,,Samuel Peelle,94941.0,6117.0,ACTIVE,,,,QUOTED,UM_CRM,,390130,Usa Autotransport,Roadway,speelle@gmail.com,18609302849.0
,,,,2026-06-23,,2025-11,1819.0,1400.0,300.0,21.4,,,,,,,Jorge Rodriguez,58854.0,78574.0,ACTIVE,,,,QUOTED,UM_CRM,,385725,Cross Country Movers,Website,Jorgerodriguez482@gmail.com,19563603915.0
,,,,2026-06-22,,2026-03,1962.0,1409.0,425.0,30.2,,,,,,,Robert Brown,92210.0,11937.0,ACTIVE,,,,QUOTED,UM_CRM,,390005,Usa Autotransport,Google,Robert.sayler.brown@gmail.com,16093152967.0
MIAMI BEACH,,WAINSCOTT,,2026-06-21,,2026-04,2354.0,900.0,200.0,22.2,,,,,,,Katy Chen,33141.0,11975.0,ACTIVE,,,,QUOTED,UM_CRM,,391081,Flat Price Auto Transport,Google,katyc@jjm-mgmt.com,18482818150.0
,,,,2026-06-21,,2026-01,1470.0,1150.0,250.0,21.7,,,,,,,Vivian Kalu,2145.0,77493.0,ACTIVE,,,,QUOTED,UM_CRM,,387033,Flat Price Auto Transport,Website,vivikay96@yahoo.com,18648846835.0
,,,,2026-06-20,,2026-03,1391.0,1000.0,300.0,30.0,,,,,,,Josephine Mutepfa,48382.0,93306.0,ACTIVE,,,,QUOTED,UM_CRM,,389622,Usa Autotransport,Website,roofarrow@gmail.com,12074000429.0
,,,,2026-06-19,,2025-10,1365.0,1000.0,300.0,30.0,,,,,,,Amari Jones,28083.0,78244.0,ACTIVE,,,,QUOTED,UM_CRM,,384295,Flat Price Auto Transport,Website,Amarijane590@gmail.com,12103475161.0
,,,,2026-06-18,,2026-04,1284.0,1000.0,200.0,20.0,,,,,,,Stephany Otero,34475.0,6705.0,ACTIVE,,,,QUOTED,UM_CRM,,391096,State 2 State Movers,Website,stephanyotero28@gmail.com,13215503370.0
PORTLAND,,OWINGS MILLS,,2026-06-17,,2026-04,1338.0,1000.0,250.0,25.0,,,,,,,Bola Demola,97217.0,21117.0,BOOKED,,,,BOOKED,UM_CRM,,390380,Cross Country Moving,Return Customer,bola.demola@gmail.com,19173702155.0
,,,,2026-06-16,,2026-04,1525.0,1200.0,225.0,18.8,,,,,,,Lorida Pestano,89166.0,49286.0,ACTIVE,,,,QUOTED,UM_CRM,,390288,Usa Autotransport,Yelp,MSRIDA@MSN.COM,17252757900.0
,,,,2026-06-16,,2026-04,2888.0,999.0,400.0,40.0,,,,,,,Sondra Kinney,10954.0,90024.0,ACTIVE,,,,QUOTED,UM_CRM,,390965,Usa Autotransport,Google,sondra.kinney15@gmail.com,13474858307.0
GREENDALE,,CARY,,2026-06-16,,2026-01,1199.0,725.0,417.0,57.5,,,,,,,Chimma ,53129.0,27511.0,ACTIVE,,,,QUOTED,UM_CRM,,387166,East Coast West Coast Express,Old Gen Lead,chidimmaozodi@gmail.com,14143349556.0
EATONTOWN,,ROCHESTER,,2026-06-15,,2025-12,945.0,700.0,200.0,28.6,,,,,,,Ahmed Elhatw,7724.0,55905.0,ACTIVE,,,,QUOTED,UM_CRM,,386483,Cross Country Moving,Referral,ahmedelhatw@gmail.com,17329622672.0
CHICAGO,,NEW YORK,,2026-06-15,,2025-11,977.0,700.0,230.0,32.9,,,,,,,Ernest Vandeweghe,60637.0,10065.0,ACTIVE,,,,QUOTED,UM_CRM,,385482,Cross Country Movers,SMS Marketing,reecevdw@gmail.com,16462460189.0
,,,,2026-06-15,,2026-02,1712.0,1300.0,300.0,23.1,,,,,,,Dejah Daniels,98087.0,92602.0,ACTIVE,,,,QUOTED,UM_CRM,,388473,Flat Price Auto Transport,Google,therealdejahd20@outlook.com,12065309478.0
CORONA,,NORTH PORT,,2026-06-15,,2026-04,1525.0,1200.0,225.0,18.8,,,,,,,Serena Martinez,92879.0,34288.0,ACTIVE,,,,QUOTED,UM_CRM,,390946,Cross Country Movers,Google,serenamartinez@yahoo.com,19512887497.0
,,,,2026-06-15,,2025-12,1458.0,999.0,390.0,39.0,,,,,,,Will Kaufman,2446.0,94301.0,ACTIVE,,,,QUOTED,UM_CRM,,386608,Flat Price Auto Transport,Website,will@wjkaufman.com,13035064853.0
,,,,2026-06-15,,2026-04,1605.0,1300.0,200.0,15.4,,,,,,,Saif Ali,94303.0,11520.0,ACTIVE,,,,QUOTED,UM_CRM,,390741,Usa Autotransport,Website,saifali892001@gmail.com,15163209981.0
,,,,2026-06-15,,2026-03,1391.0,1000.0,300.0,30.0,,,,,,,Emerson Souza,55108.0,32606.0,ACTIVE,,,,QUOTED,UM_CRM,,389036,Flat Price Auto Transport,Google,emerson.cordova@hotmail.com,16126440551.0
,,,,2026-06-15,,2026-01,2364.0,900.0,451.0,50.1,,,,,,,Kj Figaro,19973.0,80201.0,ACTIVE,,,,QUOTED,UM_CRM,,387234, Long Distance Movers,Website,Smithfigaro8@gmail.com,13022450998.0
,,,,2026-06-15,,2026-04,1640.0,1200.0,333.0,27.8,,,,,,,Valerie Ritenour,13316.0,32780.0,ACTIVE,,,,QUOTED,UM_CRM,,390892,Usa Autotransport,Google,valeriev7768@yahoo.com,13153716166.0
SPARKS,,KATY,,2026-06-14,,2026-04,1498.0,1100.0,300.0,27.3,,,,,,,Dylan Deerings,89434.0,77493.0,ACTIVE,,,,QUOTED,UM_CRM,,390704,Usa Autotransport,Website,dylandeeringps1@gmail.com,14234323703.0
DENVER,,WALES,,2026-06-14,,2026-01,1000.0,800.0,152.0,19.0,,,,,,,Matthew Pearls,80202.0,53183.0,ACTIVE,,,,QUOTED,UM_CRM,,387249,Usa Autotransport,Google,praline-67.pockets@icloud.com,12065695452.0
DESERT HOT SPRINGS,,BRANDYWINE,,2026-06-14,,2026-04,1659.0,1300.0,250.0,19.2,,,,,,,Sandra Alas,92240.0,20613.0,BOOKED,,,,BOOKED,UM_CRM,,390724,Usa Autotransport,Google,alasrsandra3@gmail.com,12068411280.0
,,,,2026-06-13,,2026-03,1367.0,1000.0,278.0,27.8,,,,,,,Mariel Morehead,92663.0,78712.0,ACTIVE,,,,QUOTED,UM_CRM,,390022,Usa Autotransport,Yelp,marielmorehead2003@gmail.com,19498997411.0
,,,,2026-06-12,,2026-02,1952.0,1500.0,325.0,21.7,,,,,,,Ahad Bawany,98133.0,23185.0,ACTIVE,,,,QUOTED,UM_CRM,,388160,Cross Country Movers,Google,abdulahadbawany@gmail.com,19544961381.0
LONGVIEW,,PLEASANT PRAIRIE,,2026-06-12,,2026-03,1338.0,1000.0,250.0,25.0,,,,,,,Jonothan Emanuelson,75601.0,53158.0,ACTIVE,,,,QUOTED,UM_CRM,,389548,Flat Price Auto Transport,Google,jonathan.emanuelson@gmail.com,12776895896.0
LIMA,,ORLANDO,,2026-06-12,,2026-04,1258.0,950.0,226.0,23.8,,,,,,,Brandon Minnis,45805.0,32839.0,ACTIVE,,,,QUOTED,UM_CRM,,391155,Flat Price Auto Transport,SMS Marketing,b.minnis11@yahoo.com,16147879358.0
,,,,2026-06-12,,2026-03,1498.0,1100.0,300.0,27.3,,,,,,,Florybeth Garcia Corona,95901.0,53214.0,ACTIVE,,,,QUOTED,UM_CRM,,389219,East Coast West Coast Express,Website,florybeth18@gmail.com,15309300425.0
SAN FRANCISCO,,ATLANTA,,2026-06-12,,2026-04,1198.0,800.0,320.0,40.0,,,,,,,Sally Chu,94127.0,30305.0,ACTIVE,,,,QUOTED,UM_CRM,,390525,State 2 State Movers,Google,sally.chu91@gmail.com,19173553025.0
,,,,2026-06-11,,2026-01,1552.0,1100.0,350.0,31.8,,,,,,,Lakiesha Lal,89128.0,77493.0,ACTIVE,,,,QUOTED,UM_CRM,,387782,State 2 State Movers,Website,Kkdimples33@gmail.com,17026290058.0
SAN FRANCISCO,,CLARKSVILLE,,2026-06-10,,2026-02,1450.0,1000.0,355.0,35.5,,,,,,,Robyn Malone,94158.0,37043.0,BOOKED,,,,BOOKED,UM_CRM,,388273,Long Distance Movers,Website,lett_9@hotmail.com,17188646846.0
GOLETA,,SCOTTSDALE,,2026-06-10,,2026-02,855.0,500.0,299.0,59.8,,,,,,,Edward DeOcampo,93117.0,85258.0,BOOKED,,,,BOOKED,UM_CRM,,388477,Usa Autotransport,Yelp,edeocampo@yahoo.com,19257196059.0
AZUSA,,NOVI,,2026-06-10,,2026-04,1284.0,900.0,300.0,33.3,,,,,,,Matt Navarette,91702.0,48377.0,ACTIVE,,,,QUOTED,UM_CRM,,390331,Long Distance Movers,Website,mattnav34@yahoo.com,19518169501.0
,,,,2026-06-10,,2026-02,1177.0,800.0,300.0,37.5,,,,,,,Sonia Romero,84116.0,90247.0,ACTIVE,,,,QUOTED,UM_CRM,,388038,Flat Price Auto Transport,Google,Soniar0711@gmail.com,13237454428.0
,,,,2026-06-10,,2026-04,3531.0,1400.0,200.0,14.3,,,,,,,TYLER BROWN,98012.0,34761.0,ACTIVE,,,,QUOTED,UM_CRM,,390573,Usa Autotransport,Website,tbrown_7@msn.com,14252190956.0
,,,,2026-06-09,,2026-04,1045.0,900.0,77.0,8.6,,,,,,,Matthew Swartz,30621.0,48313.0,ACTIVE,,,,QUOTED,UM_CRM,,390770,Usa Autotransport,Google,mswartz25@gmail.com,12482555740.0
,,,,2026-06-09,,2026-02,1226.0,860.0,286.0,33.3,,,,,,,Ryan Sigala,92833.0,76115.0,ACTIVE,,,,QUOTED,UM_CRM,,388138,Usa Autotransport,Google,ryansigala07@gmail.com,16575009962.0
FOLSOM,,PANAMA CITY,,2026-06-09,,2026-04,1600.0,1100.0,395.0,35.9,,,,,,,William Merritt,95630.0,32404.0,ACTIVE,,,,QUOTED,UM_CRM,,390876,State 2 State Movers,Google Guarantee,merritt715@gmail.com,13058799321.0
,,,,2026-06-08,,2026-04,1380.0,1090.0,200.0,18.3,,,,,,,Kimya Ghaffarian,92653.0,33904.0,ACTIVE,,,,QUOTED,UM_CRM,,391141,Cross Country Movers,Google,kimyag3@gmail.com,19497353087.0
,,,,2026-06-08,,2026-02,1398.0,1100.0,207.0,18.8,,,,,,,Noah Greenwald,94304.0,2116.0,BOOKED,,,,BOOKED,UM_CRM,,388771,Flat Price Auto Transport,Website,noahfgreenwald@gmail.com,13103871325.0
,,,,2026-06-08,,2026-04,1766.0,1400.0,250.0,17.9,,,,,,,Ramon Espinoza,8540.0,94143.0,ACTIVE,,,,QUOTED,UM_CRM,,390722,Usa Autotransport,Website,ramonespnza@gmail.com,19802973822.0
,,,,2026-06-08,,2026-03,1295.0,1050.0,160.0,15.2,,,,,,,Rahul Phadnis,95008.0,20814.0,ACTIVE,,,,QUOTED,UM_CRM,,389461,Trico Long Distance Movers,Website,that.rahulphadnis@gmail.com,14086366678.0
BRENTWOOD,,DEARBORN,,2026-06-08,,2026-04,1575.0,1200.0,272.0,22.7,,,,,,,Ken Schultz,94513.0,48124.0,ACTIVE,,,,QUOTED,UM_CRM,,390522,Usa Autotransport,Website,KMSchultz3@yahoo.com,18103002543.0
THE VILLAGES,,BROOKINGS,,2026-06-08,,2026-01,1925.0,1500.0,333.0,22.2,,,,,,,Deca Fletcher,32162.0,97415.0,ACTIVE,,,,QUOTED,UM_CRM,,387305,Cross Country Moving,Google,deca@decafletcher.com,14257507169.0
SAINT LOUIS,,HENDERSON,,2026-06-08,,2026-02,1148.0,800.0,273.0,34.1,,,,,,,Tiffany Jaquess,63113.0,89014.0,ACTIVE,,,,QUOTED,UM_CRM,,388798,State 2 State Movers,Yelp,jaquess_tiffany@yahoo.com,13146854185.0
,,,,2026-06-05,,2026-01,1070.0,700.0,300.0,42.9,,,,,,,SAMUEL OFORI,55414.0,20147.0,ACTIVE,,,,QUOTED,UM_CRM,,387421,State 2 State Movers,Website,sofori061@gmail.com,19522152558.0
,,,,2026-06-05,,2026-04,1749.0,1185.0,450.0,38.0,,,,,,,Duke Utter,92253.0,33458.0,ACTIVE,,,,QUOTED,UM_CRM,,390901,Usa Autotransport,Google,dcr.builders@yahoo.com,17605745638.0
,,,,2026-06-02,,2026-04,2782.0,1100.0,150.0,13.6,,,,,,,Alyssa /,90005.0,27707.0,ACTIVE,,,,QUOTED,UM_CRM,,390917,Cross Country Movers,Google Ads,agpark2016@gmail.com,15109143876.0
,,,,2026-06-02,,2026-01,1605.0,1180.0,320.0,27.1,,,,,,,Scot Rap,22044.0,98040.0,ACTIVE,,,,QUOTED,UM_CRM,,387635,Usa Autotransport,Website,Ltusmcol@gmail.com,17033444061.0
,,,,2026-06-01,,2026-04,1284.0,800.0,400.0,50.0,,,,,,,Randle Jennings,78636.0,81055.0,ACTIVE,,,,QUOTED,UM_CRM,,390263,Usa Autotransport,Yelp,Pedernaleswoodworks@gmail.com,15128010697.0
,,,,2026-06-01,,2026-04,1675.0,1165.0,400.0,34.3,,,,,,,Ethan Frink,85255.0,2135.0,ACTIVE,,,,QUOTED,UM_CRM,,390903,Usa Autotransport,Yelp,efrink29@gmail.com,14805441034.0
SEATTLE,,,,2026-06-01,,2026-02,8667.0,6300.0,1800.0,28.6,,,,,,,Akash Singh,98102.0,0.0,ACTIVE,,,,QUOTED,UM_CRM,,388747,Schmidt International Relocations,Yelp,akash4393@gmail.com,11562787590.0
,,,,2026-06-01,,2025-10,1575.0,1200.0,300.0,25.0,,,,,,,Gina Guerra,1835.0,92052.0,ACTIVE,,,,QUOTED,UM_CRM,,384547,Flat Price Auto Transport,Website,ginaguerra.remax@gmail.com,19782301198.0
,,,,2026-06-01,,2026-04,1498.0,1100.0,300.0,27.3,,,,,,,Lawrence Jonson,89523.0,70112.0,ACTIVE,,,,QUOTED,UM_CRM,,390487,Usa Autotransport,Google,Johnlawrence.jonson@gmail.com,19256420282.0
,,,,2026-06-01,,2026-04,1584.0,1200.0,280.0,23.3,,,,,,,Lubz Bernard,89436.0,77423.0,ACTIVE,,,,QUOTED,UM_CRM,,391056,Usa Autotransport,Google,lubzbernard@gmail.com,16154812774.0
,,,,2026-06-01,,2026-01,1306.0,888.0,333.0,37.5,,,,,,,Pat Owen,78756.0,94582.0,ACTIVE,,,,QUOTED,UM_CRM,,387598,Usa Autotransport,Website,patricia_owen@att.net,14087727714.0
,,,,2026-06-01,,2026-03,1391.0,1000.0,300.0,30.0,,,,,,,Matthew Careskey,91950.0,98403.0,ACTIVE,,,,QUOTED,UM_CRM,,389698,Cross Country Movers,Google,Mcareske@gmail.com,18082867765.0
,,,,2026-06-01,,2026-03,1659.0,1250.0,300.0,24.0,,,,,,,Najma El,46205.0,27545.0,ACTIVE,,,,QUOTED,UM_CRM,,389554,Flat Price Auto Transport,Google,lesamjan@gmail.com,13172019359.0
PHOENIX,,MOUNT PLEASANT,,2026-06-01,,2026-04,1712.0,1400.0,200.0,14.3,,,,,,,Minna Gautam,85004.0,29464.0,ACTIVE,,,,QUOTED,UM_CRM,,390385,Flat Price Auto Transport,Referral,minnagautam9@gmail.com,13019198545.0
,,,,2026-06-01,,2026-04,2140.0,750.0,200.0,26.7,,,,,,,Angie Harvey,80247.0,76039.0,ACTIVE,,,,QUOTED,UM_CRM,,390959,Usa Autotransport,Website,aharvey@kilduffunderground.com,17203196725.0
,,,,2026-06-01,,2026-02,1509.0,1060.0,350.0,33.0,,,,,,,Sharon Cooper,60085.0,29591.0,ACTIVE,,,,QUOTED,UM_CRM,,388543,Flat Price Auto Transport,Website,blessed_child2@yahoo.com,18474017774.0
,,,,2026-06-01,,2026-02,1525.0,1125.0,300.0,26.7,,,,,,,EMMA CARRIER,89509.0,30107.0,ACTIVE,,,,QUOTED,UM_CRM,,388402,Usa Autotransport,Google,emmarkrump@gmail.com,17758428929.0
,,,,2026-06-01,,2026-02,1659.0,1300.0,250.0,19.2,,,,,,,Juan Villarreal,13602.0,93257.0,ACTIVE,,,,QUOTED,UM_CRM,,387959,Usa Autotransport,Google,juan.villarreal486@yahoo.com,15595008510.0
,,,,2026-05-31,,2026-03,1552.0,1200.0,250.0,20.8,,,,,,,Elizabeth McBride,19015.0,98607.0,ACTIVE,,,,QUOTED,UM_CRM,,389747,State 2 State Movers,Yelp,lizannesteele@gmail.com,14848320611.0
,,,,2026-05-31,,2026-03,938.0,600.0,277.0,46.2,,,,,,,Connor Rasmussen,89084.0,97838.0,ACTIVE,,,,QUOTED,UM_CRM,,389903,Usa Autotransport,Google,berries_lintel.3r@icloud.com,15412155303.0
,,,,2026-05-31,,2026-04,1396.0,1050.0,255.0,24.3,,,,,,,Kelsi Blake,89117.0,97086.0,ACTIVE,,,,QUOTED,UM_CRM,,390275,Usa Autotransport,Website,kelsihunter3@gmail.com,19713025582.0
,,,,2026-05-30,,2026-02,2568.0,1100.0,200.0,18.2,,,,,,,Andrew Simons,92104.0,21131.0,ACTIVE,,,,QUOTED,UM_CRM,,388723,Long Distance Movers,Website,andrew.simons86@gmail.com,14108028600.0
,,,,2026-05-30,,2026-03,1231.0,850.0,300.0,35.3,,,,,,,Addison Wheeler,84101.0,2903.0,ACTIVE,,,,QUOTED,UM_CRM,,389298,Usa Autotransport,Website,addison.loyalty@gmail.com,13855008753.0
MIAMI,,HARWOOD HEIGHTS,,2026-05-29,,2026-04,1177.0,800.0,300.0,37.5,,,,,,,Jack Benso,33161.0,60706.0,BOOKED,,,,BOOKED,UM_CRM,,391040,Cross Country Movers,Google Ads,jackbenso1@yahoo.com,18476827097.0
RICHMOND,,EAST ORANGE,,2026-05-29,,2026-04,1258.0,1000.0,176.0,17.6,,,,,,,Darlington Omeni,77407.0,7017.0,ACTIVE,,,,QUOTED,UM_CRM,,390372,Flat Price Auto Transport,Google,d.omeni1@yahoo.com,12013783015.0
,,,,2026-05-29,,2026-04,1284.0,900.0,300.0,33.3,,,,,,,Amber Kennedy,87124.0,50263.0,ACTIVE,,,,QUOTED,UM_CRM,,390377,State 2 State Movers,Website,ambkenn@gmail.com,15054502489.0
MEDFORD,,SAN DIEGO,,2026-05-29,,2025-03,1519.0,1050.0,425.0,40.5,,,,,,,Sair Abbas,2155.0,92101.0,BOOKED,,,,BOOKED,UM_CRM,,372253,Cross Country Movers,Return Customer,sair_abbas@yahoo.com,15105085059.0
DESERT HOT SPRINGS,,FORT WORTH,,2026-05-29,,2026-04,2461.0,1000.0,150.0,15.0,,,,,,,Christopher Martinez,92240.0,76102.0,ACTIVE,,,,QUOTED,UM_CRM,,390575,Usa Autotransport,Website,Christopher.Martinez@gmail.com,17602239973.0
,,,,2026-05-28,,2026-04,1605.0,1200.0,300.0,25.0,,,,,,,Brooke Sorrentino,80126.0,34221.0,ACTIVE,,,,QUOTED,UM_CRM,,390922,Usa Autotransport,Website,bamesaveda@gmail.com,13039156208.0
SYRACUSE,,CHAPEL HILL,,2026-05-28,,2026-04,1284.0,900.0,300.0,33.3,,,,,,,Mark CALL FRIDAY,13206.0,27516.0,ACTIVE,,,,QUOTED,UM_CRM,,391053,Usa Autotransport,Google,mark4397@gmail.com,17087014397.0
,,,,2026-05-28,,2026-04,963.0,600.0,300.0,50.0,,,,,,,Courtney Maitland,17406.0,33634.0,ACTIVE,,,,QUOTED,UM_CRM,,390714,Cross Country Movers,Website,courtneymaitland93@yahoo.com,14436159048.0
,,,,2026-05-28,,2026-03,1834.0,1289.0,425.0,33.0,,,,,,,Afework Woldeyes,89139.0,11605.0,ACTIVE,,,,QUOTED,UM_CRM,,389817,State 2 State Movers,Website,afemeng@yahoo.com,17022345229.0
RIVERSIDE,,FORT WORTH,,2026-05-28,,2026-04,1231.0,950.0,200.0,21.1,,,,,,,Lauren  ,92505.0,76134.0,ACTIVE,,,,QUOTED,UM_CRM,,391131,Cross Country Movers,Google,lady6841@gmail.com,16827176841.0
,,,,2026-05-28,,2026-03,888.0,608.0,222.0,36.5,,,,,,,Abdullah Nasim,60616.0,2139.0,BOOKED,,,,BOOKED,UM_CRM,,389201,State 2 State Movers,Google,abdullahnasim93@gmail.com,16179093152.0
,,,,2026-05-28,,2025-12,1599.0,1200.0,323.0,26.9,,,,,,,Pepe Perez,92553.0,34472.0,ACTIVE,,,,QUOTED,UM_CRM,,386353,Cross Country Movers,Website,Peput@hotmail.com,19093524580.0
PHILADELPHIA,,HEATH SPRINGS,,2026-05-28,,2026-02,774.0,501.0,222.0,44.3,,,,,,,Destiny Hayes,19151.0,29058.0,BOOKED,,,,BOOKED,UM_CRM,,388555,State 2 State Movers,Google,greenedes09@gmail.com,12675709219.0
BONITA SPRINGS,,CHATHAM,,2026-05-28,,2025-04,1235.0,800.0,376.0,47.0,,,,,,,John Smart,34134.0,2633.0,ACTIVE,,,,QUOTED,UM_CRM,,373918,Usa Autotransport,Google,lynnjohnsmart@comcast.net,12392067041.0
MIDDLETOWN,,FORT LAUDERDALE,,2026-05-27,,2026-01,1247.0,900.0,265.0,29.4,,,,,,,Tom Driver,19709.0,33319.0,BOOKED,,,,BOOKED,UM_CRM,,387510,Flat Price Auto Transport,SMS Marketing,drivert148@hotmail.com,13023739771.0
HOUSTON,,EL PASO,,2026-05-27,,2026-03,589.0,400.0,150.0,37.5,,,,,,,Christian Cargile,77021.0,79912.0,BOOKED,,,,BOOKED,UM_CRM,,389085,State 2 State Movers,Google,Ccargile03@gmail.com,18327237112.0
,,FORT MYERS,,2026-05-26,,2026-04,1578.0,1200.0,275.0,22.9,,,,,,,Daniel Sanchez,76179.0,33901.0,ACTIVE,,,,QUOTED,UM_CRM,,390719,Usa Autotransport,Website,Daniel@1845midstream.com,14326646451.0
,,,,2026-05-26,,2026-03,1115.0,800.0,242.0,30.2,,,,,,,Patrick McEnroe,34108.0,60614.0,BOOKED,,,,BOOKED,UM_CRM,,389587,Usa Autotransport,Google,patrickjmcenroe@gmail.com,13129677631.0
,,,,2026-05-26,,2026-03,1049.0,780.0,200.0,25.6,,,,,,,Leigh Crain,85018.0,74011.0,ACTIVE,,,,QUOTED,UM_CRM,,389712,Usa Autotransport,Website,Lncrain@gmail.com,19182371042.0
SAN JOSE,,DARBY,,2026-05-26,,2026-04,1498.0,1200.0,200.0,16.7,,,,,,,Viola vorr,95135.0,19023.0,BOOKED,,,,BOOKED,UM_CRM,,390796,Flat Price Auto Transport,Google,ladyvorr@gmail.com,14085058965.0
,,,,2026-05-26,,2026-04,1638.0,1300.0,231.0,17.8,,,,,,,Josiah Phelps,98119.0,70003.0,ACTIVE,,,,QUOTED,UM_CRM,,390196,Cross Country Movers,Website,Josiahtphelps@yahoo.com,19014685396.0
AURORA,,FANWOOD,,2026-05-26,,2026-04,1102.0,800.0,230.0,28.7,,,,,,,Michael Tieu,80014.0,7023.0,ACTIVE,,,,QUOTED,UM_CRM,,390990,East Coast West Coast Express,Google,Miketieu2@gmail.com,12532246256.0
WALLINGFORD,,DALLAS,,2026-05-25,,2026-04,1318.0,950.0,282.0,29.7,,,,,,,Richard Carabetta,6492.0,75235.0,ACTIVE,,,,QUOTED,UM_CRM,,391052,Usa Autotransport,Website,rcarabetta@snet.net,12395932055.0
LEBANON,,PORTLAND,,2026-05-24,,2026-04,1776.0,1100.0,560.0,50.9,,,,,,,Haley Aldrige,3766.0,97212.0,BOOKED,,,,BOOKED,UM_CRM,,390638,Cross Country Moving,Return Customer,haleyaldridg@gmail.com,19092008934.0
,,,,2026-05-24,,2026-02,1552.0,1250.0,200.0,16.0,,,,,,,Jiny Burg,92008.0,7070.0,ACTIVE,,,,QUOTED,UM_CRM,,388184,Cross Country Movers,Yelp,borninjapan12+crosscountry@gmail.com,17603313688.0
REDMOND,,NEWINGTON,,2026-05-23,,2026-03,1474.0,1222.0,156.0,12.8,,,,,,,Virgina Ho,98052.0,6111.0,ACTIVE,,,,QUOTED,UM_CRM,,389270,East Coast West Coast Express,Google,virginiaho234@gmail.com,15083458669.0
,,,,2026-05-23,,2026-04,1231.0,850.0,300.0,35.3,,,,,,,Nicholas Best,80401.0,77089.0,ACTIVE,,,,QUOTED,UM_CRM,,390836,Usa Autotransport,Google,Nicholas636best@gmail.com,19792925637.0
,,,,2026-05-23,,2026-04,2140.0,1600.0,400.0,25.0,,,,,,,Olivia Taylor,2903.0,95624.0,ACTIVE,,,,QUOTED,UM_CRM,,390960,Usa Autotransport,Google,livitay1226@gmail.com,19164160174.0
,,,,2026-05-23,,2026-03,1177.0,800.0,300.0,37.5,,,,,,,rielca pya palma,60140.0,78709.0,ACTIVE,,,,QUOTED,UM_CRM,,389477,State 2 State Movers,Website,rielca_pya@yahoo.com,12246169714.0
,,,,2026-05-23,,2026-01,1231.0,900.0,250.0,27.8,,,,,,,Jessica Mordaunt,84404.0,35205.0,ACTIVE,,,,QUOTED,UM_CRM,,387839,Long Distance Movers,Website,jessmordaunt1@gmail.com,18017870514.0
,,,,2026-05-22,,2026-03,1497.0,999.0,400.0,40.0,,,,,,,Domnic Brandenburg,84107.0,23325.0,ACTIVE,,,,QUOTED,UM_CRM,,389337,Flat Price Auto Transport,Google,Domnic.lb123@gmail.com,14356400769.0
,,,,2026-05-22,,2025-11,1733.0,1350.0,300.0,22.2,,,,,,,Shaq King,89081.0,36756.0,ACTIVE,,,,QUOTED,UM_CRM,,385414,Usa Autotransport,Google,shauill@gmail.com,17023435464.0
SAN FRANCISCO,,NEW YORK,,2026-05-22,,2026-04,3959.0,1400.0,500.0,35.7,,,,,,,Maxime Petazzoni,94114.0,10026.0,ACTIVE,,,,QUOTED,UM_CRM,,391133,Cross Country Movers,Website,maxime.petazzoni@bulix.org,14083100595.0
,,,,2026-05-21,,2026-04,1879.0,1500.0,256.0,17.1,,,,,,,Dino Rocha,33138.0,89523.0,ACTIVE,,,,QUOTED,UM_CRM,,391104,Usa Autotransport,Google,dino_rocha@live.com,17862127563.0
,,,,2026-05-21,,2026-04,1766.0,1400.0,250.0,17.9,,,,,,,Timothy Jackson,95667.0,74701.0,ACTIVE,,,,QUOTED,UM_CRM,,390845,Usa Autotransport,Yelp,tmjckson11@gmail.com,19198698567.0
,,,,2026-05-21,,2026-02,748.0,450.0,249.0,55.3,,,,,,,Santana Hands,62205.0,76054.0,ACTIVE,,,,QUOTED,UM_CRM,,388689,Flat Price Auto Transport,Google,santana.hands8186@outlook.com,12282368289.0
TWIN FALLS,,PHOENIX,,2026-05-21,,2026-02,1748.0,1400.0,234.0,16.7,,,,,,,Alex DeLair,83301.0,21131.0,ACTIVE,,,,QUOTED,UM_CRM,,388666,Usa Autotransport,Website,adelair@knottmechanical.com,14433926072.0
,,,,2026-05-21,,2026-03,1445.0,1000.0,350.0,35.0,,,,,,,William Wolz,93101.0,60526.0,ACTIVE,,,,QUOTED,UM_CRM,,389008,Usa Autotransport,Google,wmwolz8888@gmail.com,17089276693.0
MAMMOTH LAKES,,AUSTIN,,2026-05-21,,2026-03,1579.0,1176.0,300.0,25.5,,,,,,,Doug Everett,93546.0,78701.0,ACTIVE,,,,QUOTED,UM_CRM,,390079,Usa Autotransport,Google,everett858@hotmail.com,18184261542.0
SEATTLE,,METAIRIE,,2026-05-21,,2026-04,1685.0,1175.0,400.0,34.0,,,,,,,Josiah Phelps,98119.0,70002.0,ACTIVE,,,,QUOTED,UM_CRM,,390707,Cross Country Movers,Instagram,josiahtphelps@gmail.com,19014685396.0
,,,,2026-05-21,,2026-03,1498.0,1100.0,300.0,27.3,,,,,,,Corinne Flanigan,90245.0,8251.0,ACTIVE,,,,QUOTED,UM_CRM,,389995,Trico Long Distance Movers,Website,corinneflanigan@gmail.com,16097804640.0
FAIRFIELD,,PHOENIX,,2026-05-20,,2026-01,1097.0,800.0,225.0,28.1,,,,,,,Kristina Hemmitt,94533.0,85002.0,ACTIVE,,,,QUOTED,UM_CRM,,387802,Cross Country Movers,Yelp,khemmitt25@icloud.com,17077188100.0
,,,,2026-05-20,,2026-04,2358.0,2000.0,204.0,10.2,,,,,,,Rachel Kim,13202.0,95134.0,BOOKED,,,,BOOKED,UM_CRM,,390772,Usa Autotransport,Google,rachely113@gmail.com,13159603392.0
,,,,2026-05-20,,2026-04,2333.0,2000.0,180.0,9.0,,,,,,,Jonathan Hersholt,91307.0,32164.0,ACTIVE,,,,QUOTED,UM_CRM,,390783,Cross Country Movers,Website,jonbh1234@gmail.com,18183070773.0
SAN ANTONIO,,LAKE WORTH,,2026-05-20,,2026-03,1192.0,790.0,324.0,41.0,,,,,,,Tie Mason,78260.0,33467.0,ACTIVE,,,,QUOTED,UM_CRM,,390012,State 2 State Movers,Google,tmason.3737@gmail.com,18325455117.0
,,,,2026-05-20,,2026-03,1605.0,1200.0,300.0,25.0,,,,,,,Bj co,29708.0,95127.0,ACTIVE,,,,QUOTED,UM_CRM,,389128,East Coast West Coast Express,Google,bobbiejcox@earthlink.net,14088360100.0
SEATTLE,,LONG BEACH,,2026-05-20,,2026-03,975.0,665.0,246.0,37.0,,,,,,,Leanne Linsky,98116.0,90803.0,ACTIVE,,,,QUOTED,UM_CRM,,390085,East Coast West Coast Express,Return Customer,leannelinsky@yahoo.com,13109481568.0
,,,,2026-05-20,,2026-04,1699.0,1200.0,388.0,32.3,,,,,,,Shannon Stoll,14519.0,34211.0,ACTIVE,,,,QUOTED,UM_CRM,,390584,Usa Autotransport,Website,Smstoll94@gmail.com,15857942981.0
,,,,2026-05-20,,2026-04,1746.0,1232.0,400.0,32.5,,,,,,,Glen Bourque,92806.0,2703.0,ACTIVE,,,,QUOTED,UM_CRM,,390650,Usa Autotransport,Website,Chemawagolf@comcast.net,17742540075.0
,,,,2026-05-19,,2026-04,1445.0,1100.0,250.0,22.7,,,,,,,James Boland,43221.0,33441.0,BOOKED,,,,BOOKED,UM_CRM,,390629,Usa Autotransport,Google,jv2798@yahoo.com,13864440182.0
ATLANTA,,VISTA,,2026-05-19,,2026-04,1500.0,1100.0,302.0,27.5,,,,,,,Elizabeth Ford,30328.0,92083.0,BOOKED,,,,BOOKED,UM_CRM,,390144,Usa Autotransport,Return Customer,eford1doc@gmail.com,12024866286.0
,,,,2026-05-19,,2026-04,1070.0,800.0,200.0,25.0,,,,,,,Emily Park,94305.0,98075.0,ACTIVE,,,,QUOTED,UM_CRM,,390981,Usa Autotransport,Google,goldenpond9@gmail.com,14252709558.0
,,,,2026-05-19,,2026-04,2461.0,2000.0,300.0,15.0,,,,,,,Sabrina Carrington,89074.0,2141.0,ACTIVE,,,,QUOTED,UM_CRM,,390976, Long Distance Movers,Website,src1215@gmail.com,16178777028.0
BOULDER,,REDWOOD CITY,,2026-05-19,,2026-04,1234.0,853.0,300.0,35.2,,,,,,,Evie Schwartz,80304.0,94061.0,ACTIVE,,,,QUOTED,UM_CRM,,390971,Usa Autotransport,Return Customer,evieschwartz13@gmail.com,18188356600.0
,,,,2026-05-19,,2026-03,1448.0,1100.0,253.0,23.0,,,,,,,Amy Jones,80946.0,13244.0,ACTIVE,,,,QUOTED,UM_CRM,,389665,Usa Autotransport,Google,chrisamyjones@aol.com,17209353658.0
NAPLES,,GLOUCESTER,,2026-05-18,,2026-03,3048.0,1300.0,249.0,19.2,,,,,,,Patty Clayman,34108.0,1930.0,ACTIVE,,,,QUOTED,UM_CRM,,390081,Usa Autotransport,Yelp,pfclayman4@gmail.com,19782737300.0
SAN FRANCISCO,,MATTHEWS,,2026-05-18,,2026-03,1958.0,1600.0,230.0,14.4,,,,,,,Jennie Goodell,94117.0,28105.0,ACTIVE,,,,QUOTED,UM_CRM,,389862,Usa Autotransport,Roadway,jgoodell357@gmail.com,19176588828.0
TACOMA,,OKLAHOMA CITY,,2026-05-18,,2026-04,1698.0,1400.0,187.0,13.4,,,,,,,Kiobi Aling,98408.0,73139.0,ACTIVE,,,,QUOTED,UM_CRM,,391143,Cross Country Movers,Google Ads,alingkiobi@gmail.com,12532097442.0
,,,,2026-05-18,,2026-04,1766.0,1400.0,250.0,17.9,,,,,,,Alicia Flores,85351.0,48237.0,ACTIVE,,,,QUOTED,UM_CRM,,390931,State 2 State Movers,Google,alicia@wellthy.com,15614690261.0
STATE COLLEGE,,CUPERTINO,,2026-05-18,,2026-04,1350.0,1000.0,262.0,26.2,,,,,,,Colleen Ranney,16803.0,95014.0,BOOKED,,,,BOOKED,UM_CRM,,390286,Usa Autotransport,Google,colleen@theranneys.com,14084774691.0
,,,,2026-05-18,,2026-04,1175.0,873.0,225.0,25.8,,,,,,,Eric Ettinger,33487.0,7740.0,BOOKED,,,,BOOKED,UM_CRM,,390261,Usa Autotransport,Google,eric@ettingerengineering.com,15163199360.0
,,,,2026-05-18,,2025-12,1295.0,900.0,333.0,37.0,,,,,,,Malcolm Davis,36606.0,90012.0,BOOKED,,,,BOOKED,UM_CRM,,386368,East Coast West Coast Express,Google,macli0312@outlook.com,12512926546.0
ORANGEVALE,,FLINT,,2026-05-18,,2025-11,7489.0,1500.0,999.0,66.6,,,,,,,Lon Renfroe,95662.0,48501.0,ACTIVE,,,,QUOTED,UM_CRM,,385190,Usa Autotransport,Google,rlrenfri@comcast.net,19168991992.0
,,RICHMOND,,2026-05-18,,2026-02,1418.0,1100.0,225.0,20.5,,,,,,,Mia Coronel,92562.0,23221.0,BOOKED,,,,BOOKED,UM_CRM,,388777,Cross Country Movers,Referral,ckmcoronel2014@gmail.com,19513037949.0
NEWTON CENTER,,PLEASANTON,,2026-05-17,,2026-04,1427.0,999.0,335.0,33.5,,,,,,,Lei Sun,2459.0,94566.0,BOOKED,,,,BOOKED,UM_CRM,,390485,Usa Autotransport,Google,lesst17@yahoo.com,17077668868.0
,,,,2026-05-17,,2026-04,1926.0,1500.0,300.0,20.0,,,,,,,Nicholas Chestnut,80232.0,83854.0,ACTIVE,,,,QUOTED,UM_CRM,,390941,Cross Country Movers,Website,srttuner@gmail.com,17207377837.0
RENO,,HARKER HEIGHTS,,2026-05-16,,2026-04,1017.0,700.0,250.0,35.7,,,,,,,Jan Sluchak,89511.0,76548.0,ACTIVE,,,,QUOTED,UM_CRM,,390151,Usa Autotransport,Google,jsluchak@pacbell.net,17756902117.0
JENSEN BEACH,,WEST DES MOINES,,2026-05-16,,2026-03,1284.0,1000.0,200.0,20.0,,,,,,,Joe D'Souza,34957.0,50266.0,BOOKED,,,,BOOKED,UM_CRM,,389626,Cross Country Moving,Return Customer,captjoejas@gmail.com,15153212812.0
,,,,2026-05-16,,2026-04,1498.0,1250.0,150.0,12.0,,,,,,,Brian Jordan,90802.0,30324.0,ACTIVE,,,,QUOTED,UM_CRM,,391067,Cross Country Movers,Website,bljordan1@att.net,14042175297.0
,,,,2026-05-16,,2026-04,700.0,554.0,100.0,18.1,,,,,,,Ron Kaiser,80202.0,90012.0,BOOKED,,,,BOOKED,UM_CRM,,390324,Usa Autotransport,Google,rkbozeman@gmail.com,14065708415.0
BALTIMORE,,HOUSTON,,2026-05-16,,2026-01,1080.0,800.0,209.0,26.1,,,,,,,Vincent Guida,21212.0,77030.0,ACTIVE,,,,QUOTED,UM_CRM,,387705,Kerb,Google,vincentmauriceguida@gmail.com,14107070067.0
,,,,2026-05-16,,2026-04,1589.0,1200.0,285.0,23.8,,,,,,,Stephen Lessard,98040.0,85747.0,ACTIVE,,,,QUOTED,UM_CRM,,390505,State 2 State Movers,Website,hasps_strops7c@icloud.com,19496371802.0
SAN JOSE,,ISSAQUAH,,2026-05-16,,2026-03,1099.0,727.0,300.0,41.3,,,,,,,Shogo  Ishii,95134.0,98029.0,BOOKED,,,,BOOKED,UM_CRM,,389377,Kerb,Referral,shigman@outlook.com,12063213240.0
REDMOND,,COLORADO SPRINGS,,2026-05-15,2026-06-01 00:00:00,2026-04,1177.0,900.0,200.0,22.2,,,,,,,Nikhita Sathiyan ,98073.0,80904.0,ACTIVE,,,,QUOTED,UM_CRM,,390320, Long Distance Movers,Yelp,nikhitasathiyan26@gmail.comDNC,15615634579.0
SAN RAMON,,EL MONTE,,2026-05-15,,2026-04,749.0,500.0,200.0,40.0,,,,,,,Christian ,94582.0,91732.0,ACTIVE,,,,QUOTED,UM_CRM,,390132,Flat Price Auto Transport,Google,Calvasocial@gmail.com,19252195794.0
,,EUGENE,,2026-05-15,,2026-04,1177.0,800.0,300.0,37.5,,,,,,,Josh Cottam,99205.0,97405.0,ACTIVE,,,,QUOTED,UM_CRM,,390756,Usa Autotransport,Google,joshcottam83@gmail.com,15093857250.0
SAINT LOUIS,,WATERBURY,,2026-05-15,,2026-04,1338.0,950.0,300.0,31.6,,,,,,,Manuel Paniagua,63146.0,6704.0,ACTIVE,,,,QUOTED,UM_CRM,,390443,Flat Price Auto Transport,Google,manuelpaniagua14@yahoo.com,12035786147.0
,,,,2026-05-15,,2026-03,1500.0,1100.0,301.9,27.4,,,,,,,Holly Ward,33566.0,85749.0,ACTIVE,,,,QUOTED,UM_CRM,,389360,State 2 State Movers,Website,fridayhere@yahoo.com,18136597533.0
,,,,2026-05-15,,2026-03,895.0,600.0,236.0,39.3,,,,,,,Pat Estes,80027.0,92612.0,ACTIVE,,,,QUOTED,UM_CRM,,389736,Usa Autotransport,Google,Pattiestes71@gmail.com,15627861182.0
,,,,2026-05-15,,2026-04,1225.0,800.0,345.0,43.1,,,,,,,Lindsey Ruiz,93933.0,91326.0,ACTIVE,,,,QUOTED,UM_CRM,,390699,Usa Autotransport,Google,lnruiz2006@gmail.com,12814753390.0
,,,,2026-05-15,,2026-03,2194.0,850.0,250.0,29.4,,,,,,,Pat Estes,80027.0,92612.0,ACTIVE,,,,QUOTED,UM_CRM,,389737,Flat Price Auto Transport,Google,Pattiestes71@gmail.com,15627861182.0
,,,,2026-05-15,,2026-04,1766.0,1400.0,250.0,17.9,,,,,,,Katlynn Patterson,13616.0,33897.0,ACTIVE,,,,QUOTED,UM_CRM,,390139,Usa Autotransport,Google,kpatterson1282@gmail.com,13154056390.0
,,,,2026-05-15,,2026-01,1319.0,933.0,300.0,32.2,,,,,,,Rachele Cantelli,76207.0,97123.0,ACTIVE,,,,QUOTED,UM_CRM,,387924,Cross Country Moving,Google,rachele@relocity.com,14159434205.0
,,,,2026-05-15,,2026-01,1391.0,1000.0,300.0,30.0,,,,,,,Rachele Cantelli,76207.0,97123.0,ACTIVE,,,,QUOTED,UM_CRM,,387925,Trico Long Distance Movers,Google,rachele@relocity.com,14159434205.0
,,,,2026-05-14,,2026-04,3321.0,1760.0,222.0,12.6,,,,,,,Doug Stuetzle,95033.0,83709.0,ACTIVE,,,,QUOTED,UM_CRM,,391031,Usa Autotransport,Yelp,dstuetzle@gmail.com,14086560239.0
BROOKLYN,,ATLANTA,,2026-05-14,,2026-04,1043.0,750.0,225.0,30.0,,,,,,,Ternicia Odom,11221.0,30318.0,BOOKED,,,,BOOKED,UM_CRM,,390619,Usa Autotransport,Return Customer,t.marie.odom@gmail.com,13127182273.0
FULLERTON,,AURORA,,2026-05-14,,2026-03,2240.0,900.0,183.0,20.3,,,,,,,Aisling O'Brien,92832.0,80017.0,ACTIVE,,,,QUOTED,UM_CRM,,389188,State 2 State Movers,Google,deonbender@gmail.com,12132000671.0
FREMONT,,NEWARK,,2026-05-14,,2026-04,1749.0,1400.0,235.0,16.8,,,,,,,Madelyn Madrigal,94538.0,7107.0,ACTIVE,,,,QUOTED,UM_CRM,,391102,Usa Autotransport,Roadway,madfa31cam@gmail.com,19514623453.0
,,,,2026-05-14,,2026-04,1498.0,1100.0,300.0,27.3,,,,,,,Aidan Gomes,89503.0,60446.0,ACTIVE,,,,QUOTED,UM_CRM,,390667,Usa Autotransport,Website,ampgomes31@gmail.com,19252070898.0
MIAMI,,NORWALK,,2026-05-13,,2026-04,1552.0,1200.0,250.0,20.8,,,,,,,Alexander Bank,33101.0,90650.0,ACTIVE,,,,QUOTED,UM_CRM,,390829,Cross Country Movers,Google Guarantee,calvin2064@gmail.com,12132691967.0
,,,,2026-05-13,,2025-11,1399.0,999.0,333.0,33.3,,,,,,,Shonetta Dennie,85021.0,29201.0,ACTIVE,,,,QUOTED,UM_CRM,,385571,Flat Price Auto Transport,Google,shonettadennie@gmail.com,16026972333.0
EL CAJON,,COGGON,,2026-05-13,,2026-04,1873.0,1500.0,250.0,16.7,,,,,,,Randy ,92021.0,52218.0,ACTIVE,,,,QUOTED,UM_CRM,,390548,Flat Price Auto Transport,Google,rmelhouse@apexmech.com,18585832362.0
PHOENIX,,SALT LAKE CITY,,2026-05-13,,2026-02,2793.0,670.0,200.0,29.9,,,,,,,Chad Mattes,85024.0,84107.0,ACTIVE,,,,QUOTED,UM_CRM,,388801,Usa Autotransport,Referral,chadmat421@gmail.com,17204543459.0
MIAMI,,WASHINGTON,,2026-05-13,,2026-04,2247.0,400.0,600.0,150.0,,,,,,,Brian McDonald,33136.0,20017.0,ACTIVE,,,,QUOTED,UM_CRM,,391042,Usa Autotransport,Return Customer,sierraechobravox@gmail.com,17543679236.0
,,,,2026-05-13,,2026-04,1926.0,1500.0,300.0,20.0,,,,,,,Caitlyn Comminiello,80108.0,21663.0,ACTIVE,,,,QUOTED,UM_CRM,,390848,Usa Autotransport,Google,caitlynmscherr@gmail.com,18053388522.0
,,,,2026-05-13,,2026-02,1177.0,750.0,350.0,46.7,,,,,,,Zion Wallace,74037.0,90746.0,ACTIVE,,,,QUOTED,UM_CRM,,388566,State 2 State Movers,Google,zionwallace68@gmail.com,19189959361.0
,,,,2026-05-12,,2026-04,1391.0,1050.0,250.0,23.8,,,,,,,Joe Bailey,55117.0,28401.0,ACTIVE,,,,QUOTED,UM_CRM,,390961,Usa Autotransport,Yelp,jbailey@theprecisionteam.com,16122896641.0
WALNUT CREEK,,FORT LAUDERDALE,,2026-05-12,,2026-04,1497.0,999.0,400.0,40.0,,,,,,,Florian  Binet ,94597.0,33301.0,ACTIVE,,,,QUOTED,UM_CRM,,390550, Long Distance Movers,Google,florian.alexandre.binet@gmail.com,14153186215.0
PHOENIX,,IRVINGTON,,2026-05-12,,2026-03,1470.0,1000.0,374.0,37.4,,,,,,,Karen Zelonka,85008.0,10533.0,BOOKED,,,,BOOKED,UM_CRM,,389372,Flat Price Auto Transport,Return Customer,kzeecontact@icloud.com,19287780113.0
,,,,2026-05-12,,2026-04,1498.0,1000.0,400.0,40.0,,,,,,,Xiaodong Huang,33076.0,94040.0,ACTIVE,,,,QUOTED,UM_CRM,,390918,Usa Autotransport,Website,huanghexd@hotmail.com,19543264072.0
,,,,2026-05-12,,2026-03,1380.0,1065.0,225.0,21.1,,,,,,,Maggie Tan,94022.0,46285.0,ACTIVE,,,,QUOTED,UM_CRM,,390057,Usa Autotransport,Website,maggie.tan@gmail.com,16502406280.0
,,,,2026-05-12,,2026-04,1552.0,1150.0,300.0,26.1,,,,,,,Kim Plair,94533.0,76063.0,ACTIVE,,,,QUOTED,UM_CRM,,391073,State 2 State Movers,Google,Mzlairp@gmail.com,15106916078.0
,,,,2026-05-11,,2025-12,2247.0,1800.0,300.0,16.7,,,,,,,Piper Kennedy,84101.0,22079.0,ACTIVE,,,,QUOTED,UM_CRM,,386569,Long Distance Movers,Website,pmkennedy02@gmail.com,18019415908.0
,,,,2026-05-11,,2026-03,1118.0,800.0,245.0,30.6,,,,,,,Fayaz Shawl,43022.0,20854.0,DEAD,,,,QUOTED,UM_CRM,,389998,Usa Autotransport,Google,fas777@aol.com,13012334275.0
SEATTLE,,SAN DIEGO,,2026-05-11,,2026-04,1338.0,950.0,300.0,31.6,,,,,,,Jason ,98136.0,92110.0,ACTIVE,,,,QUOTED,UM_CRM,,391008,Cross Country Movers,Google Guarantee,suplizio@hotmail.com,12062952865.0
,,,,2026-05-11,,2026-04,1485.0,1100.0,288.0,26.2,,,,,,,Viet Nguyen,92024.0,8854.0,ACTIVE,,,,QUOTED,UM_CRM,,390530,Cross Country Moving,Website,vietphilly2002@yahoo.com,16263886869.0
PEARLAND,,BRENTWOOD,,2026-05-11,,2026-04,1868.0,1500.0,246.0,16.4,,,,,,,Alex Syerik,77581.0,94513.0,BOOKED,,,,BOOKED,UM_CRM,,391011,Usa Autotransport,Roadway,alex@syerik.com,15105668215.0
,,,,2026-05-11,,2026-01,1263.0,1000.0,180.0,18.0,,,,,,,Asia Harris,20613.0,75114.0,ACTIVE,,,,QUOTED,UM_CRM,,387769,Flat Price Auto Transport,Google,A.lucas2011@gmail.com,12406060287.0
ROSEVILLE,,WALLOON LAKE,,2026-05-11,,2026-03,2624.0,2100.0,352.0,16.8,,,,,,,Rick Lantz,95661.0,49796.0,ACTIVE,,,,QUOTED,UM_CRM,,389303,Usa Autotransport,Return Customer,rick@dmsautoleads.com,19165952600.0
DAYTONA BEACH,,LAS VEGAS,,2026-05-11,,2026-04,2140.0,1700.0,300.0,17.6,,,,,,,Bob  ,32118.0,89101.0,ACTIVE,,,,QUOTED,UM_CRM,,390952,Cross Country Movers,Google,xk8sl550@gmail.com,15177757721.0
,,,,2026-05-11,,2025-11,1177.0,900.0,200.0,22.2,,,,,,,J K,47408.0,37027.0,ACTIVE,,,,QUOTED,UM_CRM,,385404,Flat Price Auto Transport,Website,Kangjoa@iu.edu,14014995457.0
,,,,2026-05-11,,2026-02,1177.0,800.0,300.0,37.5,,,,,,,Ravi Katare,30097.0,47403.0,ACTIVE,,,,QUOTED,UM_CRM,,388688,State 2 State Movers,Google,Rkkatare@gmail.com,16166880701.0
ALLENTOWN,,JACKSONVILLE,,2026-05-11,,2026-03,1284.0,1000.0,200.0,20.0,,,,,,,Peter herasimchuk,18109.0,32225.0,BOOKED,,,,BOOKED,UM_CRM,,389725,State 2 State Movers,Google,herasimchukpeter@gmail.com,14844267284.0
,,,,2026-05-10,,2026-04,1306.0,999.0,222.0,22.2,,,,,,,Jake Hernandez Vasquez,89436.0,46260.0,ACTIVE,,,,QUOTED,UM_CRM,,390884,Usa Autotransport,Google,Jakehernandezv@gmail.com,17754709241.0
PHOENIX,,PEORIA,,2026-05-10,,2026-02,1182.0,850.0,255.0,30.0,,,,,,,Shurie Staples,85007.0,61604.0,ACTIVE,,,,QUOTED,UM_CRM,,388581,State 2 State Movers,Yelp,staples.shurie4@gmail.com,13094723432.0
RIVERSIDE,,,,2026-05-10,,2026-04,1873.0,1400.0,350.0,25.0,,,,,,,Yoselin Becerril,92503.0,34219.0,ACTIVE,,,,QUOTED,UM_CRM,,391086,Cross Country Movers,Google Ads,yoselinbecerril14@gmail.com,19416009851.0
SYRACUSE,,LOS ANGELES,,2026-05-09,,2026-04,1743.0,1299.0,330.0,25.4,,,,,,,Pammela Jackson ,13210.0,90066.0,BOOKED,,,,BOOKED,UM_CRM,,390213,Cross Country Moving,Return Customer,jackson5@jrtp.com,13107402011.0
,,,,2026-05-09,,2026-03,1488.0,1150.0,241.0,21.0,,,,,,,Siena Tom,60614.0,95765.0,BOOKED,,,,BOOKED,UM_CRM,,389822,State 2 State Movers,Website,spt1205@gmail.com,19167789064.0
,,,,2026-05-09,,2026-02,749.0,500.0,200.0,40.0,,,,,,,Diptayan Dasgupta,28262.0,2452.0,ACTIVE,,,,QUOTED,UM_CRM,,388727,Flat Price Auto Transport,Website,ddg3737@gmail.com,17047059532.0
,,,,2026-05-09,,2026-04,1498.0,1100.0,300.0,27.3,,,,,,,Christian Pham,89123.0,55304.0,ACTIVE,,,,QUOTED,UM_CRM,,390912,Usa Autotransport,Yelp,pham524@gmail.com,17027123234.0
TOPANGA,,MIAMI,,2026-05-09,,2026-04,3538.0,1400.0,407.0,29.1,,,,,,,Lilly Sevilla,90290.0,33101.0,BOOKED,,,,BOOKED,UM_CRM,,390611,Usa Autotransport,Roadway,21114colina@gmail.com,17863746741.0
,,,,2026-05-09,,2026-04,1552.0,1200.0,250.0,20.8,,,,,,,Moises Flores,97525.0,78752.0,ACTIVE,,,,QUOTED,UM_CRM,,390871,Usa Autotransport,Yelp,fmoises457@yahoo.com,15128254977.0
,,,,2026-05-08,,2026-04,1358.0,999.0,270.0,27.0,,,,,,,Morgan McCord,80211.0,37209.0,ACTIVE,,,,QUOTED,UM_CRM,,390120,Cross Country Moving,Google,m.morganmccord@gmail.com,13178746240.0
PALM BEACH GARDENS,FL,PARKER,CO,2026-05-08,,2026-05,2622.0,2200.0,422.0,19.2,2017 VW Passat / 2005 Toyota RAV 4,2017.0,VW,Passat / 2005 Toyota RAV 4,sedan,UZ Auto Trans Inc,Adrian Del pino Gomez,,,,,,,BOOKED_GSHEET,Booked Cars (2024+),,502389557,,,,
[TRUNCATED_AFTER_300_LINES]
```


---

## File: `06_other_assets/Global_Sales_Force__Auto_Shipping_Automation__bot_a_lead_quoting_engine_v2/home/ubuntu/bot_a_lead_quoting_engine/.env.example`

| Field | Value |
|---|---|
| Kind | `text` |
| Size Bytes | 1329 |
| Extract Chars | 1322 |
| Truncated | False |

```text
# ============================================
# Bot A: Lead Quoting Engine — Environment Variables
# Copy this file to .env and fill in your values
# ============================================

# EMAIL (IMAP / SMTP)
IMAP_SERVER=imap.gmail.com
IMAP_PORT=993
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=your-sales-email@gmail.com
EMAIL_PASSWORD=your-gmail-app-password

# How often to check for new emails (seconds)
EMAIL_POLL_INTERVAL=30

# LLM ENGINE
# Options: "gemini" (recommended), "openai", "ollama"
LLM_PROVIDER=gemini

# Gemini (primary — ~$0.30/month for 1000 quotes)
GEMINI_API_KEY=your-gemini-api-key

# OpenAI-compatible (backup)
OPENAI_API_KEY=your-openai-api-key
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4.1-nano

# Ollama (local fallback — free, runs on the mini PC)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen3:4b

# CENTRAL DISPATCH API
CD_API_BASE_URL=https://api.centraldispatch.com
CD_API_KEY=your-cd-api-key
CD_API_SECRET=your-cd-api-secret

# GOOGLE SHEETS
GOOGLE_SHEETS_CREDENTIALS_FILE=config/google_service_account.json
TRAINING_DATA_SPREADSHEET_ID=12cjcIZ2ErS7wU_j7t8jIkFvVwoyTiJ4WD4DO8nJSNso

# PRICING
TARGET_PROFIT_MARGIN=100
SEASONAL_ADJUSTMENT=150
PEAK_YOY_INCREASE_MIN=50
PEAK_YOY_INCREASE_MAX=100
RECENCY_WINDOW_DAYS=30

# LOGGING
LOG_LEVEL=INFO
```


---

## File: `06_other_assets/Global_Sales_Force__Auto_Shipping_Automation__bot_a_lead_quoting_engine_v2/home/ubuntu/bot_a_lead_quoting_engine/.gitignore`

| Field | Value |
|---|---|
| Kind | `text` |
| Size Bytes | 88 |
| Extract Chars | 87 |
| Truncated | False |

```text
.env
__pycache__/
*.pyc
venv/
logs/*.log
logs/*.jsonl
logs/test_results.json
data/*.csv
```
