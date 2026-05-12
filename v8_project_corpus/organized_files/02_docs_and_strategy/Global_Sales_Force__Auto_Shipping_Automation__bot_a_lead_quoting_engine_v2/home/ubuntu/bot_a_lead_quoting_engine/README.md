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
