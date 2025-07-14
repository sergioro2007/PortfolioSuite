#!/usr/bin/env python3
"""
Test script to verify the adjustable regime multiplier functionality
"""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from portfolio_suite.options_trading.core import OptionsTracker


def test_adjustable_multiplier():
    """Test the adjustable regime multiplier feature"""
    print("🧪 Testing Adjustable Regime Multiplier Feature")
    print("=" * 60)

    # Initialize tracker
    tracker = OptionsTracker()
    ticker = "AAPL"

    print(f"\n📊 Testing with ticker: {ticker}")

    # Test 1: Default behavior (ChatGPT's 0.001 multiplier)
    print("\n1️⃣ Testing default behavior (0.001 multiplier - ChatGPT's approach):")
    try:
        prediction_default = tracker.predict_price_range(ticker)
        if prediction_default:
            bias_score = prediction_default.get("bias_score", 0)
            current_price = prediction_default.get("current_price", 0)
            target_price = prediction_default.get("target_price", 0)
            bias_adjustment = target_price - current_price
            implied_multiplier = (
                bias_adjustment / (current_price * bias_score) if bias_score != 0 else 0
            )

            print(f"   Current Price: ${current_price:.2f}")
            print(f"   Bias Score: {bias_score:.3f}")
            print(f"   Target Price: ${target_price:.2f}")
            print(f"   Bias Adjustment: ${bias_adjustment:.4f}")
            print(f"   Implied Multiplier: {implied_multiplier:.6f} (should be ~0.001)")
        else:
            print("   ❌ Failed to get prediction")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    # Test 2: Strong bias (original 0.01 multiplier)
    print("\n2️⃣ Testing strong bias (0.01 multiplier - original approach):")
    try:
        prediction_strong = tracker.predict_price_range(ticker, regime_multiplier=0.01)
        if prediction_strong:
            bias_score = prediction_strong.get("bias_score", 0)
            current_price = prediction_strong.get("current_price", 0)
            target_price = prediction_strong.get("target_price", 0)
            bias_adjustment = target_price - current_price
            implied_multiplier = (
                bias_adjustment / (current_price * bias_score) if bias_score != 0 else 0
            )

            print(f"   Current Price: ${current_price:.2f}")
            print(f"   Bias Score: {bias_score:.3f}")
            print(f"   Target Price: ${target_price:.2f}")
            print(f"   Bias Adjustment: ${bias_adjustment:.4f}")
            print(f"   Implied Multiplier: {implied_multiplier:.6f} (should be ~0.01)")
        else:
            print("   ❌ Failed to get prediction")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    # Test 3: Convenience methods
    print("\n3️⃣ Testing convenience methods:")
    try:
        # ChatGPT bias method
        prediction_chatgpt = tracker.predict_price_range_chatgpt_bias(ticker)
        if prediction_chatgpt:
            bias_adjustment_chatgpt = prediction_chatgpt.get(
                "target_price", 0
            ) - prediction_chatgpt.get("current_price", 0)
            print(f"   ChatGPT bias adjustment: ${bias_adjustment_chatgpt:.4f}")

        # Strong bias method
        prediction_strong_method = tracker.predict_price_range_strong_bias(ticker)
        if prediction_strong_method:
            bias_adjustment_strong = prediction_strong_method.get(
                "target_price", 0
            ) - prediction_strong_method.get("current_price", 0)
            print(f"   Strong bias adjustment: ${bias_adjustment_strong:.4f}")

        # Verify difference
        if prediction_chatgpt and prediction_strong_method:
            ratio = (
                abs(bias_adjustment_strong / bias_adjustment_chatgpt)
                if bias_adjustment_chatgpt != 0
                else 0
            )
            print(f"   Ratio (Strong/ChatGPT): {ratio:.1f}x (should be ~10x)")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    # Test 4: Custom multiplier
    print("\n4️⃣ Testing custom multiplier (0.005 - middle ground):")
    try:
        prediction_custom = tracker.predict_price_range(ticker, regime_multiplier=0.005)
        if prediction_custom:
            bias_score = prediction_custom.get("bias_score", 0)
            current_price = prediction_custom.get("current_price", 0)
            target_price = prediction_custom.get("target_price", 0)
            bias_adjustment = target_price - current_price
            implied_multiplier = (
                bias_adjustment / (current_price * bias_score) if bias_score != 0 else 0
            )

            print(f"   Current Price: ${current_price:.2f}")
            print(f"   Bias Score: {bias_score:.3f}")
            print(f"   Target Price: ${target_price:.2f}")
            print(f"   Bias Adjustment: ${bias_adjustment:.4f}")
            print(f"   Implied Multiplier: {implied_multiplier:.6f} (should be ~0.005)")
        else:
            print("   ❌ Failed to get prediction")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    print("\n" + "=" * 60)
    print("✅ Test completed! The regime multiplier is now adjustable.")
    print("💡 Default value (0.001) matches ChatGPT's gentler approach.")
    print("💡 Use 0.01 for the original stronger bias effects.")


if __name__ == "__main__":
    test_adjustable_multiplier()
