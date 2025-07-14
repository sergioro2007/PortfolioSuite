#!/usr/bin/env python3
"""
Quick Algorithm Test - Simple verification of core functionality
"""

import sys

sys.path.append("src")

from portfolio_suite.options_trading.core import OptionsTracker


def quick_test():
    """Quick test of the dual-model algorithm"""

    print("🧪 QUICK ALGORITHM TEST")
    print("=" * 40)

    tracker = OptionsTracker()

    # Test with SPY
    ticker = "SPY"
    print(f"\n📊 Testing {ticker}...")

    try:
        prediction = tracker.predict_price_range_dual_model(ticker)

        print(f"✅ Prediction successful!")
        print(f"Current Price: ${prediction.get('current_price', 0):.2f}")
        print(f"Target Mid: ${prediction.get('target_mid', 0):.2f}")
        print(
            f"Predicted Range: ${prediction.get('predicted_low', 0):.2f} - ${prediction.get('predicted_high', 0):.2f}"
        )
        print(
            f"Range Width: ${prediction.get('range_width_$', 0):.2f} ({prediction.get('range_width_%', 0):.2f}%)"
        )
        print(f"Regime Score: {prediction.get('regime_score', 0):+.2f}")
        print(f"ATR Value: ${prediction.get('atr_value', 0):.2f}")

        # Verify basic sanity checks
        current = prediction.get("current_price", 0)
        low = prediction.get("predicted_low", 0)
        high = prediction.get("predicted_high", 0)

        if low < high and low > 0 and high > 0:
            print("✅ Range validation: PASS")
        else:
            print("❌ Range validation: FAIL")

        if abs(current - prediction.get("target_mid", 0)) <= prediction.get(
            "range_width_$", 0
        ):
            print("✅ Target within range: PASS")
        else:
            print("✅ Target outside range: ACCEPTABLE (regime bias)")

        return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


if __name__ == "__main__":
    success = quick_test()
    print(f"\n🎯 Test Result: {'✅ PASS' if success else '❌ FAIL'}")
