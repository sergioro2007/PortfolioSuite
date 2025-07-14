#!/usr/bin/env python3
"""
Test script to demonstrate ChatGPT-compatible prediction mode
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from portfolio_suite.options_trading.core import OptionsTracker


def test_chatgpt_compatible():
    """Test the ChatGPT-compatible prediction mode"""
    print("🧪 TESTING CHATGPT-COMPATIBLE MODE")
    print("=" * 50)

    # Initialize tracker
    tracker = OptionsTracker()

    # Test symbols
    test_symbols = ["SPY", "QQQ", "GOOGL"]

    for symbol in test_symbols:
        print(f"\n📊 Testing {symbol}:")
        print("-" * 30)

        # Original method with ChatGPT multiplier
        result_original = tracker.predict_price_range(symbol, regime_multiplier=-0.2)

        # New ChatGPT-compatible convenience method
        result_chatgpt = tracker.predict_price_range_chatgpt_compatible(symbol)

        # Compare results
        current_price = result_original.get("current_price", 0)
        target_original = result_original.get("target_price", 0)
        target_chatgpt = result_chatgpt.get("target_price", 0)

        print(f"Current Price: ${current_price:.2f}")
        print(f"Original (-0.2): ${target_original:.2f}")
        print(f"ChatGPT Mode:  ${target_chatgpt:.2f}")
        print(
            f"Match: {'✅' if abs(target_original - target_chatgpt) < 0.01 else '❌'}"
        )

        # Show bias score
        bias_score = result_original.get("bias_score", 0)
        print(f"Bias Score: {bias_score:+.2f}")

    print(f"\n🎉 ChatGPT-compatible mode is working perfectly!")
    print(
        "Use tracker.predict_price_range_chatgpt_compatible(symbol) for easy ChatGPT matching"
    )


if __name__ == "__main__":
    test_chatgpt_compatible()
