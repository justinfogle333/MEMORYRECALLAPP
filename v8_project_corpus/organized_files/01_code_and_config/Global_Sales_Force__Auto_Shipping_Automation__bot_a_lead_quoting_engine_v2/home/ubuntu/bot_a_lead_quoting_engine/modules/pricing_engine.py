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
