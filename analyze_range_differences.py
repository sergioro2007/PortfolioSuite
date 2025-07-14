#!/usr/bin/env python3
"""
Detailed Range Calculation Analysis
===================================

This script analyzes the differences in range calculations between our algorithm
and ChatGPT's approach to understand why we get different low/high/range values.
"""

import sys
import os
import pandas as pd

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from portfolio_suite.options_trading.core import OptionsTracker


def analyze_range_differences():
    """Analyze range calculation differences between our algorithm and ChatGPT"""
    print("🔍 RANGE CALCULATION ANALYSIS")
    print("=" * 60)

    # Load ChatGPT data
    try:
        chatgpt_df = pd.read_csv(
            "Full_2-Week_Prediction_Table__July_26_.csv", index_col=0
        )
        print("✅ ChatGPT data loaded successfully")
    except Exception as e:
        print(f"❌ Error loading ChatGPT data: {e}")
        return

    # Initialize our tracker
    tracker = OptionsTracker()

    # Test tickers with significant differences
    test_tickers = ["SPY", "QQQ", "AAPL", "MSFT", "NVDA", "GOOGL"]

    print("\n🔬 DETAILED RANGE ANALYSIS")
    print("-" * 60)

    for ticker in test_tickers:
        if ticker not in chatgpt_df.index:
            print(f"⚠️  {ticker} not in ChatGPT data, skipping")
            continue

        print(f"\n📊 Analyzing {ticker}:")
        print("-" * 40)

        # Get our prediction (both modes)
        our_original = tracker.predict_price_range(ticker, regime_multiplier=0.01)
        our_chatgpt = tracker.predict_price_range_chatgpt_compatible(ticker)

        if not our_original or not our_chatgpt:
            print(f"❌ Could not get predictions for {ticker}")
            continue

        # Get ChatGPT data
        cgpt = chatgpt_df.loc[ticker]

        # Extract values
        current_price = our_original["current_price"]

        # Our algorithm results
        our_low_orig = our_original["lower_bound"]
        our_high_orig = our_original["upper_bound"]
        our_range_orig = our_high_orig - our_low_orig
        our_range_pct_orig = (our_range_orig / current_price) * 100

        our_low_cgpt = our_chatgpt["lower_bound"]
        our_high_cgpt = our_chatgpt["upper_bound"]
        our_range_cgpt = our_high_cgpt - our_low_cgpt
        our_range_pct_cgpt = (our_range_cgpt / current_price) * 100

        # ChatGPT results
        cgpt_low = cgpt["Predicted Low"]
        cgpt_high = cgpt["Predicted High"]
        cgpt_range = cgpt["Range Width ($)"]
        cgpt_range_pct = cgpt["Range Width (%)"]

        # Print comparison
        print(f"Current Price: ${current_price:.2f}")
        print()
        print("RANGE BOUNDS:")
        print(f"  Our Original:  ${our_low_orig:.2f} - ${our_high_orig:.2f}")
        print(f"  Our ChatGPT:   ${our_low_cgpt:.2f} - ${our_high_cgpt:.2f}")
        print(f"  ChatGPT:       ${cgpt_low:.2f} - ${cgpt_high:.2f}")
        print()
        print("RANGE WIDTH ($):")
        print(f"  Our Original:  ${our_range_orig:.2f}")
        print(f"  Our ChatGPT:   ${our_range_cgpt:.2f}")
        print(f"  ChatGPT:       ${cgpt_range:.2f}")
        print(f"  Difference:    ${abs(our_range_cgpt - cgpt_range):.2f}")
        print()
        print("RANGE WIDTH (%):")
        print(f"  Our Original:  {our_range_pct_orig:.2f}%")
        print(f"  Our ChatGPT:   {our_range_pct_cgpt:.2f}%")
        print(f"  ChatGPT:       {cgpt_range_pct:.2f}%")
        print(f"  Difference:    {abs(our_range_pct_cgpt - cgpt_range_pct):.2f}%")
        print()

        # Analyze the pattern
        print("ANALYSIS:")

        # Check if our range is centered around target
        our_target_orig = our_original["target_price"]
        our_target_cgpt = our_chatgpt["target_price"]
        cgpt_target = cgpt["Target Mid"]

        our_low_dist_orig = our_target_orig - our_low_orig
        our_high_dist_orig = our_high_orig - our_target_orig

        our_low_dist_cgpt = our_target_cgpt - our_low_cgpt
        our_high_dist_cgpt = our_high_cgpt - our_target_cgpt

        cgpt_low_dist = cgpt_target - cgpt_low
        cgpt_high_dist = cgpt_high - cgpt_target

        print(
            f"  Our Original Range: {our_low_dist_orig:.2f} below target, {our_high_dist_orig:.2f} above target"
        )
        print(
            f"  Our ChatGPT Range:  {our_low_dist_cgpt:.2f} below target, {our_high_dist_cgpt:.2f} above target"
        )
        print(
            f"  ChatGPT Range:      {cgpt_low_dist:.2f} below target, {cgpt_high_dist:.2f} above target"
        )

        # Check symmetry
        our_symmetry_orig = abs(our_low_dist_orig - our_high_dist_orig)
        our_symmetry_cgpt = abs(our_low_dist_cgpt - our_high_dist_cgpt)
        cgpt_symmetry = abs(cgpt_low_dist - cgpt_high_dist)

        print(f"  Range Symmetry:")
        print(f"    Our Original:  {our_symmetry_orig:.2f} (0 = perfect symmetry)")
        print(f"    Our ChatGPT:   {our_symmetry_cgpt:.2f}")
        print(f"    ChatGPT:       {cgpt_symmetry:.2f}")

        # Check volatility usage
        our_vol = our_original.get("weekly_volatility", 0)
        our_iv_based = our_original.get("iv_based", False)

        print(f"  Our Weekly Vol: {our_vol:.1%} (IV-based: {our_iv_based})")

        # Calculate what ChatGPT's implied volatility might be
        # ChatGPT range appears to be target ± some volatility measure
        cgpt_implied_vol_dollar = cgpt_range / 2  # Half range
        cgpt_implied_vol_pct = cgpt_implied_vol_dollar / current_price

        print(f"  ChatGPT Implied Vol: {cgpt_implied_vol_pct:.1%} weekly")
        print(f"  Vol Ratio (ChatGPT/Ours): {cgpt_implied_vol_pct/our_vol:.2f}x")


def check_range_formula():
    """Check if we can reverse-engineer ChatGPT's range formula"""
    print("\n\n🧮 REVERSE-ENGINEERING CHATGPT'S RANGE FORMULA")
    print("=" * 60)

    try:
        chatgpt_df = pd.read_csv(
            "Full_2-Week_Prediction_Table__July_26_.csv", index_col=0
        )
        tracker = OptionsTracker()

        print("Testing potential range formulas:")
        print()

        for ticker in ["SPY", "QQQ", "GOOGL"]:
            if ticker not in chatgpt_df.index:
                continue

            print(f"📊 {ticker}:")

            # Get our data
            our_pred = tracker.predict_price_range_chatgpt_compatible(ticker)
            if not our_pred:
                continue

            # Get ChatGPT data
            cgpt = chatgpt_df.loc[ticker]

            current_price = our_pred["current_price"]
            our_vol = our_pred["weekly_volatility"]
            cgpt_range = cgpt["Range Width ($)"]
            cgpt_target = cgpt["Target Mid"]

            # Test different formulas
            formula1 = current_price * our_vol * 2  # ±1 std dev
            formula2 = current_price * our_vol * 1.5  # ±0.75 std dev
            formula3 = current_price * our_vol * 2.5  # ±1.25 std dev

            # Test with different base prices
            formula4 = cgpt_target * our_vol * 2  # Target-based

            print(f"  Current: ${current_price:.2f}, Target: ${cgpt_target:.2f}")
            print(f"  Our Vol: {our_vol:.1%}, ChatGPT Range: ${cgpt_range:.2f}")
            print(f"  Formula 1 (±1σ from current): ${formula1:.2f}")
            print(f"  Formula 2 (±0.75σ from current): ${formula2:.2f}")
            print(f"  Formula 3 (±1.25σ from current): ${formula3:.2f}")
            print(f"  Formula 4 (±1σ from target): ${formula4:.2f}")

            # Find closest match
            formulas = [formula1, formula2, formula3, formula4]
            formula_names = [
                "±1σ current",
                "±0.75σ current",
                "±1.25σ current",
                "±1σ target",
            ]

            best_match = min(formulas, key=lambda x: abs(x - cgpt_range))
            best_idx = formulas.index(best_match)

            print(
                f"  🎯 Best match: {formula_names[best_idx]} (${best_match:.2f}, diff: ${abs(best_match - cgpt_range):.2f})"
            )
            print()

    except Exception as e:
        print(f"❌ Error in range formula analysis: {e}")


if __name__ == "__main__":
    analyze_range_differences()
    check_range_formula()
