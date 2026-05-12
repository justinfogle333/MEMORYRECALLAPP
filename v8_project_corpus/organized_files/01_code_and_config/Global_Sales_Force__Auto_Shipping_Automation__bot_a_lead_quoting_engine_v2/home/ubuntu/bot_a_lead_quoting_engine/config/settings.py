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
