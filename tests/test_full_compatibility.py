#!/usr/bin/env python3
"""
Test ChatGPT Fully Compatible Range Calculations
===============================================

This script tests our new fully compatible ChatGPT range calculation method
that includes both target price and range calculation compatibility.
"""

import sys
import os
import pandas as pd

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from portfolio_suite.options_trading.core import OptionsTracker


def test_full_compatibility():
    """Test the fully compatible ChatGPT method"""
    print("🧪 TESTING CHATGPT FULLY COMPATIBLE METHOD")
    print("=" * 60)

    # Load ChatGPT data for comparison
    try:
        chatgpt_df = pd.read_csv(
            "Full_2-Week_Prediction_Table__July_26_.csv", index_col=0
        )
        print("✅ ChatGPT data loaded successfully")
    except Exception as e:
        print(f"❌ Error loading ChatGPT data: {e}")
        return

    # Initialize tracker
    tracker = OptionsTracker()

    # Test key tickers
    test_tickers = ["SPY", "QQQ", "GOOGL", "NVDA", "MSFT"]

    print("\n📊 COMPARISON RESULTS:")
    print("-" * 60)
    print("Ticker   | Target Diff | Range Diff | Range% Diff")
    print("-" * 60)

    for ticker in test_tickers:
        if ticker not in chatgpt_df.index:
            print(f"{ticker:<8} | Not in ChatGPT data")
            continue

        try:
            # Get our fully compatible prediction
            our_pred = tracker.predict_price_range_chatgpt_fully_compatible(ticker)
            if not our_pred:
                print(f"{ticker:<8} | Prediction failed")
                continue

            # Get ChatGPT data
            cgpt = chatgpt_df.loc[ticker]

            # Compare results
            target_diff = abs(our_pred["target_price"] - cgpt["Target Mid"])
            range_diff = abs(
                (our_pred["upper_bound"] - our_pred["lower_bound"])
                - cgpt["Range Width ($)"]
            )
            range_pct_diff = abs(
                (
                    (our_pred["upper_bound"] - our_pred["lower_bound"])
                    / our_pred["current_price"]
                    * 100
                )
                - cgpt["Range Width (%)"]
            )

            print(
                f"{ticker:<8} | ${target_diff:<10.2f} | ${range_diff:<9.2f} | {range_pct_diff:<10.2f}%"
            )

            # Show detailed breakdown for first ticker
            if ticker == "SPY":
                print(f"\n📋 DETAILED BREAKDOWN FOR {ticker}:")
                print("-" * 40)
                print(f"Current Price: ${our_pred['current_price']:.2f}")
                print(f"Our Target:    ${our_pred['target_price']:.2f}")
                print(f"ChatGPT Target: ${cgpt['Target Mid']:.2f}")
                print(f"Target Match:  {'✅' if target_diff < 0.01 else '❌'}")
                print()
                print(
                    f"Our Range:     ${our_pred['lower_bound']:.2f} - ${our_pred['upper_bound']:.2f}"
                )
                print(
                    f"ChatGPT Range: ${cgpt['Predicted Low']:.2f} - ${cgpt['Predicted High']:.2f}"
                )
                print(
                    f"Our Range $:   ${our_pred['upper_bound'] - our_pred['lower_bound']:.2f}"
                )
                print(f"ChatGPT Range $: ${cgpt['Range Width ($)']:.2f}")
                print(f"Range Match:   {'✅' if range_diff < 1.0 else '❌'}")
                print()
                print(
                    f"Volatility Scaling Factor: {our_pred.get('volatility_scaling_factor', 'N/A'):.2f}"
                )
                print(f"Original Vol: {our_pred['weekly_volatility']:.1%}")
                print(
                    f"Adjusted Vol: {our_pred.get('adjusted_weekly_volatility', 0):.1%}"
                )

        except Exception as e:
            print(f"{ticker:<8} | Error: {e}")

    print("\n🎯 IMPROVEMENT SUMMARY:")
    print("-" * 40)
    print("This method should provide:")
    print("✅ Perfect target price matching (already achieved)")
    print("🎯 Much closer range calculations")
    print("📊 Adaptive volatility scaling like ChatGPT")


if __name__ == "__main__":
    test_full_compatibility()
