#!/usr/bin/env python3
"""
Simple ATR Analysis - Focus on the core issue
"""

import sys

sys.path.append("src")

from portfolio_suite.options_trading.core import OptionsTracker
import pandas as pd
import numpy as np
import yfinance as yf


def simple_atr_analysis():
    """
    Simple analysis of ATR calculation differences
    """
    print("🔍 SIMPLE ATR ANALYSIS FOR SPY")
    print("=" * 50)

    ticker = "SPY"

    # Method 1: Our algorithm
    print("1️⃣ OUR ALGORITHM RESULTS:")
    tracker = OptionsTracker()
    indicators = tracker.get_technical_indicators(ticker)
    our_atr = indicators["atr_14"]
    our_price = indicators["current_price"]
    hist = indicators["price_history"]

    print(f"Our ATR: ${our_atr:.4f}")
    print(f"Our Price: ${our_price:.2f}")
    print(f"Data points: {len(hist)}")

    # Method 2: Fresh yfinance data
    print("\n2️⃣ FRESH YFINANCE DATA:")
    spy_fresh = yf.download(ticker, period="3mo", interval="1d")

    if spy_fresh is not None and not spy_fresh.empty:
        fresh_price = float(spy_fresh["Close"].iloc[-1])
        print(f"Fresh Price: ${fresh_price:.2f}")
        print(f"Fresh Data points: {len(spy_fresh)}")

        # Calculate ATR manually on fresh data
        high_low = spy_fresh["High"] - spy_fresh["Low"]
        high_close = np.abs(spy_fresh["High"] - spy_fresh["Close"].shift())
        low_close = np.abs(spy_fresh["Low"] - spy_fresh["Close"].shift())
        true_range = np.maximum(high_low, np.maximum(high_close, low_close))
        fresh_atr = float(true_range.rolling(window=14).mean().iloc[-1])

        print(f"Fresh ATR: ${fresh_atr:.4f}")

        # Show recent true range values
        print("\nRecent True Range values:")
        recent_tr = true_range.tail(10)
        for i, (date, tr_val) in enumerate(recent_tr.items()):
            print(f"  {date.strftime('%Y-%m-%d')}: ${float(tr_val):.4f}")

        tr_mean = float(recent_tr.mean())
        print(f"Average TR (last 10 days): ${tr_mean:.4f}")

    else:
        print("❌ Could not get fresh data")
        fresh_atr = 0
        fresh_price = 0

    # Method 3: Different window calculations
    print("\n3️⃣ DIFFERENT ATR WINDOWS:")
    if "price_history" in indicators:
        hist = indicators["price_history"]
        if len(hist) > 20:
            high_low = hist["High"] - hist["Low"]
            high_close = np.abs(hist["High"] - hist["Close"].shift())
            low_close = np.abs(hist["Low"] - hist["Close"].shift())
            true_range = np.maximum(high_low, np.maximum(high_close, low_close))

            for window in [10, 14, 20, 21]:
                if len(true_range) >= window:
                    atr_win = float(true_range.rolling(window=window).mean().iloc[-1])
                    print(f"ATR (window {window}): ${atr_win:.4f}")

    # Method 4: ChatGPT comparison
    print("\n4️⃣ CHATGPT COMPARISON:")
    chatgpt_atr = 11.70
    chatgpt_price = 624.93

    print(f"ChatGPT ATR: ${chatgpt_atr:.2f}")
    print(f"ChatGPT Price: ${chatgpt_price:.2f}")
    print(f"Our ATR: ${our_atr:.4f}")
    print(f"Difference: ${abs(chatgpt_atr - our_atr):.4f}")
    print(f"Ratio: ChatGPT is {chatgpt_atr / our_atr:.2f}x larger")

    # Method 5: Hypothesis testing
    print("\n5️⃣ HYPOTHESIS ANALYSIS:")
    print("Possible explanations for the difference:")

    # Check if ChatGPT might be using different period
    if fresh_atr > 0:
        ratio = chatgpt_atr / fresh_atr
        print(f"• Ratio suggests ChatGPT ATR is {ratio:.1f}x our calculation")

        if ratio > 2:
            print("• This suggests ChatGPT might be using:")
            print("  - Different time period (longer history)")
            print("  - Different ATR calculation method")
            print("  - Different data source with higher volatility")
            print("  - Including overnight gaps or extended hours")

        # What if ChatGPT uses 21-day window instead of 14?
        if len(hist) >= 21:
            high_low = hist["High"] - hist["Low"]
            high_close = np.abs(hist["High"] - hist["Close"].shift())
            low_close = np.abs(hist["Low"] - hist["Close"].shift())
            true_range = np.maximum(high_low, np.maximum(high_close, low_close))
            atr_21 = float(true_range.rolling(window=21).mean().iloc[-1])
            print(
                f"• If ChatGPT uses 21-day window: ${atr_21:.4f} (still {chatgpt_atr/atr_21:.1f}x different)"
            )

    # Method 6: Check our data quality
    print("\n6️⃣ DATA QUALITY CHECK:")
    price_diff = abs(our_price - fresh_price)
    print(f"Price difference (ours vs fresh): ${price_diff:.2f}")

    if price_diff < 2.0:
        print("✅ Our price data is current")
    else:
        print("❌ Our price data might be stale")

    atr_diff = abs(our_atr - fresh_atr) if fresh_atr > 0 else 0
    if atr_diff < 0.1:
        print("✅ Our ATR calculation matches manual calculation")
    else:
        print("❌ Our ATR calculation has issues")

    return {
        "our_atr": our_atr,
        "fresh_atr": fresh_atr,
        "chatgpt_atr": chatgpt_atr,
        "calculation_correct": atr_diff < 0.1,
        "data_current": price_diff < 2.0,
    }


if __name__ == "__main__":
    results = simple_atr_analysis()

    print(f"\n🎯 CONCLUSION:")
    print("=" * 50)

    if results["calculation_correct"]:
        print("✅ Our ATR calculation is mathematically correct")
    else:
        print("❌ Our ATR calculation needs debugging")

    if results["data_current"]:
        print("✅ Our data is reasonably current")
    else:
        print("❌ Our data might be stale")

    if results["chatgpt_atr"] / results["our_atr"] > 2:
        print(
            "🚨 ChatGPT's ATR is suspiciously different - likely using different method"
        )
        print(
            "   Recommendation: Investigate ChatGPT's specific ATR calculation approach"
        )
    else:
        print("✅ ATR difference is within reasonable range")

    print(f"\nOur ATR: ${results['our_atr']:.4f}")
    print(f"ChatGPT ATR: ${results['chatgpt_atr']:.2f}")
    print(f"Difference factor: {results['chatgpt_atr'] / results['our_atr']:.2f}x")
