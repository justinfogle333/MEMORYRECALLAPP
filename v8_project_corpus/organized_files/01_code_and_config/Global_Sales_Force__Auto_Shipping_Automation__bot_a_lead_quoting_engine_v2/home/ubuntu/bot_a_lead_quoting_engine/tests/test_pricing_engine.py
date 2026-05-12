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
