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
