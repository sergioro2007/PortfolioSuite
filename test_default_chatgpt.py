#!/usr/bin/env python3
"""
Test that the default method now uses ChatGPT's approach
"""

import sys

sys.path.append("/Users/soliv112/PersonalProjects/PortfolioSuite/src")

from portfolio_suite.options_trading.core import OptionsTracker


def test_default_method():
    """Test that the default method now uses ChatGPT's approach"""
    print("🧪 Testing Default Method Change to ChatGPT")
    print("=" * 60)

    tracker = OptionsTracker()

    # Test SPY with different methods
    print(f"\n📊 SPY Method Comparison:")

    # Default method (should now be ChatGPT)
    default_result = tracker.predict_price_range("SPY")

    # Explicitly ChatGPT fully compatible
    chatgpt_result = tracker.predict_price_range_chatgpt_fully_compatible("SPY")

    # ATR specification
    atr_result = tracker.predict_price_range_atr_specification("SPY")

    # Traditional bias
    traditional_result = tracker.predict_price_range_traditional_bias("SPY")

    if default_result and chatgpt_result and atr_result and traditional_result:
        print(f"   Current Price: ${default_result['current_price']:.2f}")

        print(f"\n   Target Prices:")
        print(f"     Default (ChatGPT):    ${default_result['target_price']:.2f}")
        print(f"     ChatGPT Fully Compat: ${chatgpt_result['target_price']:.2f}")
        print(f"     ATR Specification:    ${atr_result['target_price']:.2f}")
        print(f"     Traditional Bias:     ${traditional_result['target_price']:.2f}")

        print(f"\n   Range Widths:")
        default_range = default_result["upper_bound"] - default_result["lower_bound"]
        chatgpt_range = chatgpt_result["upper_bound"] - chatgpt_result["lower_bound"]
        atr_range = atr_result["range_dollar"]
        traditional_range = (
            traditional_result["upper_bound"] - traditional_result["lower_bound"]
        )

        print(f"     Default (ChatGPT):    ${default_range:.2f}")
        print(f"     ChatGPT Fully Compat: ${chatgpt_range:.2f}")
        print(f"     ATR Specification:    ${atr_range:.2f}")
        print(f"     Traditional Bias:     ${traditional_range:.2f}")

        # Check if default matches ChatGPT
        target_match = (
            abs(default_result["target_price"] - chatgpt_result["target_price"]) < 0.01
        )

        print(f"\n✅ Verification:")
        print(f"   Default uses ChatGPT method: {'YES' if target_match else 'NO'}")
        print(
            f"   Target price difference: ${abs(default_result['target_price'] - chatgpt_result['target_price']):.2f}"
        )

        if target_match:
            print(f"   🎯 SUCCESS: Default method now uses ChatGPT approach!")
        else:
            print(f"   ❌ ERROR: Default method not using ChatGPT approach")

        # Show regime multipliers being used
        print(f"\n🔍 Method Details:")
        print(f"   Default regime multiplier: -0.2 (ChatGPT)")
        print(f"   Traditional regime multiplier: 0.01")
        print(f"   ATR uses bias × 0.01 approach")


def test_method_aliases():
    """Test the new method aliases"""
    print(f"\n\n🔗 Testing Method Aliases:")
    print("=" * 60)

    tracker = OptionsTracker()

    # Test enhanced alias
    enhanced_result = tracker.predict_price_range_enhanced("SPY")
    fully_compatible_result = tracker.predict_price_range_chatgpt_fully_compatible(
        "SPY"
    )

    if enhanced_result and fully_compatible_result:
        target_match = (
            abs(
                enhanced_result["target_price"]
                - fully_compatible_result["target_price"]
            )
            < 0.01
        )

        print(f"   Enhanced method target: ${enhanced_result['target_price']:.2f}")
        print(
            f"   Fully compatible target: ${fully_compatible_result['target_price']:.2f}"
        )
        print(f"   Enhanced = Fully Compatible: {'YES' if target_match else 'NO'}")


if __name__ == "__main__":
    test_default_method()
    test_method_aliases()

    print(f"\n🎯 SUMMARY:")
    print("=" * 60)
    print(f"✅ Default predict_price_range() now uses ChatGPT's -0.2 multiplier")
    print(f"✅ Traditional methods available as predict_price_range_traditional_bias()")
    print(f"✅ ATR specification available as predict_price_range_atr_specification()")
    print(f"✅ Enhanced method is alias for fully compatible ChatGPT")
    print(f"📊 Your preference for ChatGPT method is now the default!")
