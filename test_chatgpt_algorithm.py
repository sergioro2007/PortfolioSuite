#!/usr/bin/env python3
"""
Test ChatGPT's actual algorithm based on reverse-engineering their results
"""

import sys
import os

sys.path.append("src")

from portfolio_suite.options_trading.core import OptionsTracker
import pandas as pd


def test_chatgpt_algorithm():
    """
    Test our algorithm using ChatGPT's apparent parameters
    """
    print("🧪 TESTING CHATGPT'S ACTUAL ALGORITHM")
    print("=" * 50)

    # Load ChatGPT results
    chatgpt_df = pd.read_csv("Full_2-Week_Prediction_Table__July_26_.csv", index_col=0)

    tracker = OptionsTracker()

    # Test with the multiplier ChatGPT appears to be using: -0.2
    test_tickers = ["SPY", "QQQ", "MSFT", "NVDA", "GOOGL"]

    print("Testing with regime_multiplier = -0.2 (ChatGPT's apparent value)")
    print("-" * 60)

    for ticker in test_tickers:
        if ticker in chatgpt_df.index:
            print(f"\n📊 {ticker}:")

            # ChatGPT data
            cgpt = chatgpt_df.loc[ticker]
            chatgpt_target = cgpt["Target Mid"]
            chatgpt_current = cgpt["Current Price"]

            # Our algorithm with -0.2 multiplier
            prediction = tracker.predict_price_range(ticker, regime_multiplier=-0.2)
            our_current = prediction.get("current_price", 0)
            our_target = prediction.get("target_price", 0)
            bias_score = prediction.get("bias_score", 0)

            # Calculate expected adjustment
            expected_adjustment = our_current * bias_score * -0.2
            expected_target = our_current + expected_adjustment

            print(
                f"  Current Price - Ours: ${our_current:.2f} | ChatGPT: ${chatgpt_current:.2f}"
            )
            print(f"  Bias Score: {bias_score:.3f}")
            print(f"  Expected Adjustment: ${expected_adjustment:.2f}")
            print(
                f"  Target - Ours (-0.2): ${our_target:.2f} | ChatGPT: ${chatgpt_target:.2f}"
            )
            print(f"  Target Difference: ${abs(our_target - chatgpt_target):.2f}")

            # Test if they match better
            if abs(our_target - chatgpt_target) < 2:
                print("  ✅ MUCH CLOSER MATCH!")
            elif abs(our_target - chatgpt_target) < 5:
                print("  🟡 Better match")
            else:
                print("  ❌ Still different")


def test_multiple_multipliers():
    """
    Test different multipliers to see which one matches ChatGPT best
    """
    print("\n\n🔍 TESTING MULTIPLE MULTIPLIERS")
    print("=" * 40)

    chatgpt_df = pd.read_csv("Full_2-Week_Prediction_Table__July_26_.csv", index_col=0)
    tracker = OptionsTracker()

    # Test different multipliers
    multipliers = [-0.3, -0.25, -0.2, -0.15, -0.1, -0.05, 0.02, 0.05, 0.1, 0.15, 0.2]
    ticker = "SPY"  # Use SPY as test case

    if ticker in chatgpt_df.index:
        cgpt = chatgpt_df.loc[ticker]
        chatgpt_target = cgpt["Target Mid"]
        chatgpt_current = cgpt["Current Price"]

        print(f"Finding best multiplier for {ticker}:")
        print(f"ChatGPT Target: ${chatgpt_target:.2f}")
        print(f"Current Price: ${chatgpt_current:.2f}")
        print(f"Required Bias Adjustment: ${chatgpt_target - chatgpt_current:.2f}")
        print()

        best_diff = float("inf")
        best_multiplier = None

        for mult in multipliers:
            prediction = tracker.predict_price_range(ticker, regime_multiplier=mult)
            our_target = prediction.get("target_price", 0)
            bias_score = prediction.get("bias_score", 0)

            diff = abs(our_target - chatgpt_target)

            print(
                f"  Multiplier {mult:+.2f}: Target=${our_target:.2f}, Diff=${diff:.2f}, Bias={bias_score:.3f}"
            )

            if diff < best_diff:
                best_diff = diff
                best_multiplier = mult

        print(
            f"\n🎯 Best multiplier: {best_multiplier:+.2f} (difference: ${best_diff:.2f})"
        )


if __name__ == "__main__":
    test_chatgpt_algorithm()
    test_multiple_multipliers()
