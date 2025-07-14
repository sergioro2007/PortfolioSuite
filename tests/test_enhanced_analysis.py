#!/usr/bin/env python3
"""
Quick test to verify the enhanced detailed technical analysis works correctly
"""

import sys
import os
import pytest

sys.path.append("src")

from portfolio_suite.options_trading.core import OptionsTracker


def test_prediction_detailed_output():
    """Test that prediction returns all necessary fields for detailed analysis"""

    tracker = OptionsTracker()

    # Test with a ticker from the dynamic watchlist
    if not tracker.watchlist:
        print("📋 Refreshing watchlist...")
        tracker.refresh_watchlist()

    if not tracker.watchlist:
        print("⚠️ No tickers available in watchlist, testing with AAPL directly")
        test_ticker = "AAPL"
    else:
        test_ticker = list(tracker.watchlist.keys())[0]
        print(f"🎯 Testing with: {test_ticker}")

    # Get prediction
    prediction = tracker.predict_price_range(test_ticker)

    if not prediction:
        pytest.fail("Failed to get prediction")

    # Check required fields for detailed analysis
    required_fields = [
        "current_price",
        "lower_bound",
        "upper_bound",
        "target_price",
        "bullish_probability",
        "bias_score",
        "weekly_volatility",
        "indicators",
    ]

    print("🔍 Checking prediction output fields:")
    for field in required_fields:
        if field in prediction:
            print(f"✅ {field}: {prediction.get(field)}")
        else:
            print(f"❌ Missing {field}")
            return False

    # Check indicators
    indicators = prediction.get("indicators", {})
    required_indicators = ["rsi", "macd", "macd_signal", "momentum", "current_price"]

    print("\n📊 Checking technical indicators:")
    for indicator in required_indicators:
        if indicator in indicators:
            print(f"✅ {indicator}: {indicators.get(indicator)}")
        else:
            print(f"❌ Missing {indicator}")
            return False

    # Test bias calculation components
    print(f"\n⚖️ Bias Calculation Details:")
    print(f"RSI: {indicators.get('rsi', 0):.1f}")
    print(
        f"MACD: {indicators.get('macd', 0):.3f} vs Signal: {indicators.get('macd_signal', 0):.3f}"
    )
    print(f"Momentum: {indicators.get('momentum', 0):.2f}%")
    print(f"Total Bias Score: {prediction.get('bias_score', 0):.3f}")

    # Test volatility calculation
    print(f"\n📈 Volatility Details:")
    weekly_vol = prediction.get("weekly_volatility", 0)
    annual_vol = weekly_vol * (52**0.5)
    print(f"Weekly Volatility: {weekly_vol:.3f} ({weekly_vol:.1%})")
    print(f"Annualized: {annual_vol:.3f} ({annual_vol:.1%})")

    print("\n✅ All required fields present for enhanced detailed analysis!")
    # Test passed if we reach this point without returning False


def test_dual_model_integration():
    """Test dual-model integration with enhanced analysis"""
    tracker = OptionsTracker()
    # Test dual-model specific fields
    if not tracker.watchlist:
        tracker.refresh_watchlist()
    test_ticker = list(tracker.watchlist.keys())[0] if tracker.watchlist else "AAPL"
    prediction = tracker.predict_price_range(test_ticker)
    enhanced_fields = [
        "atr_value",
        "regime_score",
        "target_mid",
        "predicted_low",
        "predicted_high",
        "range_width_$",
        "range_width_%",
    ]
    for field in enhanced_fields:
        assert field in prediction, f"Enhanced analysis missing field: {field}"
        print(f"✅ {field}: {prediction.get(field)}")
    assert (
        prediction["lower_bound"] == prediction["predicted_low"]
    ), "Range consistency error"
    assert (
        prediction["upper_bound"] == prediction["predicted_high"]
    ), "Range consistency error"
    assert (
        prediction["target_price"] == prediction["target_mid"]
    ), "Target consistency error"
    print("🎯 All dual-model enhanced analysis fields verified!")


if __name__ == "__main__":
    print("🧮 Testing Enhanced Detailed Technical Analysis")
    print("=" * 50)

    success = test_prediction_detailed_output()

    if success:
        print("\n✅ Test passed! Enhanced analysis ready for deployment.")
    else:
        print("\n❌ Test failed! Check implementation.")
