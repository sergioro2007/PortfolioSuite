#!/usr/bin/env python3
"""
Test the new ATR-based specification implementation
"""

import sys

sys.path.append("/Users/soliv112/PersonalProjects/PortfolioSuite/src")

from portfolio_suite.options_trading.core import OptionsTracker


def test_atr_specification():
    """Test the ATR specification implementation"""
    print("🧪 Testing ATR Specification Implementation")
    print("=" * 60)

    tracker = OptionsTracker()

    # Test SPY with ATR specification
    print(f"\n📊 SPY ATR Specification Test:")
    result = tracker.predict_price_range_atr_specification("SPY")

    if result:
        print(f"   Current Price: ${result['current_price']:.2f}")
        print(f"   ATR (14-day): ${result['atr']:.2f}")
        print(f"   Bias Score: {result['bias_score']:.3f}")
        print(f"   Bias (%): {result['bias_percent']:.3f}")
        print(f"   Bias Adjustment: ${result['bias_adjustment']:.2f}")
        print(f"   Target Mid: ${result['target_mid']:.2f}")
        print(f"   Predicted Low: ${result['lower_bound']:.2f}")
        print(f"   Predicted High: ${result['upper_bound']:.2f}")
        print(f"   Range ($): ${result['range_dollar']:.2f}")
        print(f"   Range (%): {result['range_percent']:.2f}%")

        # Manual verification of calculations
        print(f"\n🔍 Verification:")
        expected_bias_adj = result["current_price"] * result["bias_score"] * 0.01
        expected_target = result["current_price"] + expected_bias_adj
        expected_low = expected_target - result["atr"]
        expected_high = expected_target + result["atr"]
        expected_range_dollar = expected_high - expected_low
        expected_range_percent = (expected_range_dollar / result["current_price"]) * 100

        print(
            f"   ✓ Bias Adj: ${expected_bias_adj:.2f} == ${result['bias_adjustment']:.2f}"
        )
        print(f"   ✓ Target: ${expected_target:.2f} == ${result['target_mid']:.2f}")
        print(f"   ✓ Low: ${expected_low:.2f} == ${result['lower_bound']:.2f}")
        print(f"   ✓ High: ${expected_high:.2f} == ${result['upper_bound']:.2f}")
        print(
            f"   ✓ Range $: ${expected_range_dollar:.2f} == ${result['range_dollar']:.2f}"
        )
        print(
            f"   ✓ Range %: {expected_range_percent:.2f}% == {result['range_percent']:.2f}%"
        )

        # Check if calculations match
        calculations_correct = (
            abs(expected_bias_adj - result["bias_adjustment"]) < 0.01
            and abs(expected_target - result["target_mid"]) < 0.01
            and abs(expected_low - result["lower_bound"]) < 0.01
            and abs(expected_high - result["upper_bound"]) < 0.01
            and abs(expected_range_dollar - result["range_dollar"]) < 0.01
            and abs(expected_range_percent - result["range_percent"]) < 0.01
        )

        if calculations_correct:
            print(f"\n✅ ATR Specification Implementation: CORRECT")
        else:
            print(f"\n❌ ATR Specification Implementation: INCORRECT")

    else:
        print("❌ Could not get ATR specification prediction")


def compare_old_vs_new():
    """Compare old volatility-based vs new ATR-based"""
    print(f"\n🔍 Comparing Old vs New Implementation")
    print("=" * 60)

    tracker = OptionsTracker()

    tickers = ["SPY", "QQQ", "AAPL"]

    for ticker in tickers:
        print(f"\n📊 {ticker}:")

        # Old volatility-based method
        old_result = tracker.predict_price_range(ticker, regime_multiplier=0.01)

        # New ATR-based method
        new_result = tracker.predict_price_range_atr_specification(ticker)

        if old_result and new_result:
            print(f"   Current Price: ${old_result['current_price']:.2f}")
            print(
                f"   OLD (Volatility): Range ${old_result['lower_bound']:.2f} - ${old_result['upper_bound']:.2f}"
            )
            print(
                f"   NEW (ATR):        Range ${new_result['lower_bound']:.2f} - ${new_result['upper_bound']:.2f}"
            )

            old_range = old_result["upper_bound"] - old_result["lower_bound"]
            new_range = new_result["range_dollar"]

            print(f"   OLD Range: ${old_range:.2f}")
            print(f"   NEW Range: ${new_range:.2f}")
            print(f"   Difference: ${abs(old_range - new_range):.2f}")


def demonstrate_specification_example():
    """Demonstrate with specification example values"""
    print(f"\n📋 Specification Example Demonstration")
    print("=" * 60)

    # Using specification example:
    # Current Price = $624.93, ATR = $11.70, Bias = +0.1
    print(f"Specification Example:")
    print(f"   Current Price: $624.93")
    print(f"   ATR (14-day): $11.70")
    print(f"   Bias Score: +0.1")

    # Manual calculation
    current_price = 624.93
    atr = 11.70
    bias_score = 0.1

    bias_percent = bias_score * 0.01  # 0.1 × 0.01 = 0.001
    bias_adjustment = current_price * bias_percent  # 624.93 × 0.001 = $0.62
    target_mid = current_price + bias_adjustment  # 624.93 + 0.62 = $625.55
    predicted_low = target_mid - atr  # 625.55 - 11.70 = $613.85
    predicted_high = target_mid + atr  # 625.55 + 11.70 = $637.25
    range_dollar = predicted_high - predicted_low  # 637.25 - 613.85 = $23.40
    range_percent = (
        range_dollar / current_price
    ) * 100  # (23.40 / 624.93) × 100 = 3.74%

    print(f"\n🧮 Manual Calculation:")
    print(f"   Bias (%) = {bias_score} × 0.01 = {bias_percent:.3f}")
    print(
        f"   Bias Adjustment = ${current_price:.2f} × {bias_percent:.3f} = ${bias_adjustment:.2f}"
    )
    print(
        f"   Target Mid = ${current_price:.2f} + ${bias_adjustment:.2f} = ${target_mid:.2f}"
    )
    print(f"   Predicted Low = ${target_mid:.2f} - ${atr:.2f} = ${predicted_low:.2f}")
    print(f"   Predicted High = ${target_mid:.2f} + ${atr:.2f} = ${predicted_high:.2f}")
    print(
        f"   Range ($) = ${predicted_high:.2f} - ${predicted_low:.2f} = ${range_dollar:.2f}"
    )
    print(
        f"   Range (%) = (${range_dollar:.2f} / ${current_price:.2f}) × 100 = {range_percent:.2f}%"
    )

    print(f"\n✅ Expected Results:")
    print(f"   Target Midpoint: $625.55")
    print(f"   Predicted Low: $613.85")
    print(f"   Predicted High: $637.25")
    print(f"   Range ($): $23.40")
    print(f"   Range (%): 3.74%")


if __name__ == "__main__":
    demonstrate_specification_example()
    test_atr_specification()
    compare_old_vs_new()
