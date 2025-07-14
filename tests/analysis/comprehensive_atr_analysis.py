#!/usr/bin/env python3
"""
Comprehensive ATR Analysis and External Verification
"""

import sys

sys.path.append("src")

from portfolio_suite.options_trading.core import OptionsTracker
import pandas as pd
import numpy as np
import yfinance as yf


def comprehensive_atr_analysis():
    """
    Compare our ATR with multiple calculation methods and external sources
    """
    print("🔍 COMPREHENSIVE ATR ANALYSIS FOR SPY")
    print("=" * 70)

    ticker = "SPY"

    # Get fresh data from yfinance
    print("📊 DOWNLOADING FRESH DATA...")
    spy_data = yf.download(ticker, period="6mo", interval="1d")
    current_price = spy_data["Close"].iloc[-1]

    print(f"Current Price: ${current_price:.2f}")
    print(f"Data Range: {spy_data.index[0].date()} to {spy_data.index[-1].date()}")
    print(f"Total Days: {len(spy_data)}")

    # Method 1: Our algorithm
    print("\n1️⃣ OUR ALGORITHM:")
    print("-" * 40)
    tracker = OptionsTracker()
    indicators = tracker.get_technical_indicators(ticker)
    our_atr = indicators["atr_14"]
    our_price = indicators["current_price"]

    print(f"Our ATR: ${our_atr:.4f}")
    print(f"Our Price: ${our_price:.2f}")

    # Method 2: Manual calculation on fresh data
    print("\n2️⃣ MANUAL CALCULATION (Fresh YFinance Data):")
    print("-" * 40)

    # Calculate True Range manually
    high_low = spy_data["High"] - spy_data["Low"]
    high_close = np.abs(spy_data["High"] - spy_data["Close"].shift())
    low_close = np.abs(spy_data["Low"] - spy_data["Close"].shift())
    true_range = np.maximum(high_low, np.maximum(high_close, low_close))

    # Different ATR calculation methods
    atr_sma_14 = true_range.rolling(window=14).mean().iloc[-1]
    atr_sma_20 = true_range.rolling(window=20).mean().iloc[-1]
    atr_ema_14 = true_range.ewm(span=14).mean().iloc[-1]

    print(f"ATR SMA-14: ${atr_sma_14:.4f}")
    print(f"ATR SMA-20: ${atr_sma_20:.4f}")
    print(f"ATR EMA-14: ${atr_ema_14:.4f}")

    # Method 3: Different time periods
    print("\n3️⃣ DIFFERENT TIME PERIODS:")
    print("-" * 40)

    for period in ["1mo", "3mo", "6mo", "1y"]:
        try:
            period_data = yf.download(ticker, period=period, interval="1d")
            if len(period_data) >= 20:
                p_high_low = period_data["High"] - period_data["Low"]
                p_high_close = np.abs(
                    period_data["High"] - period_data["Close"].shift()
                )
                p_low_close = np.abs(period_data["Low"] - period_data["Close"].shift())
                p_true_range = np.maximum(
                    p_high_low, np.maximum(p_high_close, p_low_close)
                )
                p_atr = p_true_range.rolling(window=14).mean().iloc[-1]

                print(f"ATR ({period}, {len(period_data)} days): ${p_atr:.4f}")
        except:
            print(f"Error calculating ATR for {period}")

    # Method 4: Check for stock splits or adjustments
    print("\n4️⃣ SPLIT/ADJUSTMENT CHECK:")
    print("-" * 40)

    # Get raw data (non-adjusted)
    spy_raw = yf.download(ticker, period="6mo", auto_adjust=False)
    spy_adj = yf.download(ticker, period="6mo", auto_adjust=True)

    # Calculate ATR on both
    def calc_atr(data):
        high_low = data["High"] - data["Low"]
        high_close = np.abs(data["High"] - data["Close"].shift())
        low_close = np.abs(data["Low"] - data["Close"].shift())
        true_range = np.maximum(high_low, np.maximum(high_close, low_close))
        return true_range.rolling(window=14).mean().iloc[-1]

    atr_raw = calc_atr(spy_raw)
    atr_adj = calc_atr(spy_adj)

    print(f"ATR (Raw prices): ${atr_raw:.4f}")
    print(f"ATR (Adjusted prices): ${atr_adj:.4f}")
    print(f"Raw vs Adj difference: ${abs(atr_raw - atr_adj):.4f}")

    # Method 5: Check recent volatility patterns
    print("\n5️⃣ VOLATILITY PATTERN ANALYSIS:")
    print("-" * 40)

    # Calculate ATR for different recent periods
    recent_30 = spy_data.tail(30)
    recent_60 = spy_data.tail(60)
    recent_90 = spy_data.tail(90)

    for name, data in [
        ("30 days", recent_30),
        ("60 days", recent_60),
        ("90 days", recent_90),
    ]:
        if len(data) >= 14:
            atr_recent = calc_atr(data)
            avg_tr = calc_atr(data)  # This is actually ATR, not just avg TR
            print(f"ATR (Last {name}): ${atr_recent:.4f}")

    # Method 6: Show actual True Range values
    print("\n6️⃣ RECENT TRUE RANGE VALUES:")
    print("-" * 40)

    recent_tr = pd.DataFrame(
        {
            "Date": spy_data.index[-10:],
            "High": spy_data["High"].tail(10),
            "Low": spy_data["Low"].tail(10),
            "Close": spy_data["Close"].tail(10),
            "True_Range": true_range.tail(10),
        }
    ).round(4)

    print(recent_tr.to_string(index=False))

    print(f"\nRecent TR Statistics:")
    print(f"Mean TR (last 10 days): ${true_range.tail(10).mean():.4f}")
    print(f"Mean TR (last 14 days): ${true_range.tail(14).mean():.4f}")
    print(f"Mean TR (last 20 days): ${true_range.tail(20).mean():.4f}")

    # Method 7: Check if ChatGPT might be using different calculation
    print("\n7️⃣ CHATGPT EXPECTATION ANALYSIS:")
    print("-" * 40)

    chatgpt_atr = 11.70
    chatgpt_price = 624.93

    print(f"ChatGPT ATR: ${chatgpt_atr:.2f}")
    print(f"ChatGPT Price: ${chatgpt_price:.2f}")
    print(f"Our best ATR: ${atr_sma_14:.4f}")
    print(f"Difference: ${abs(chatgpt_atr - atr_sma_14):.4f}")
    print(f"Ratio: {chatgpt_atr / atr_sma_14:.2f}x")

    # What would ATR need to be to match ChatGPT?
    print(f"\n🤔 REVERSE ENGINEERING:")
    print(f"If ChatGPT's ATR is correct, recent TR should average ~${chatgpt_atr:.2f}")
    print(f"Our recent TR averages ~${true_range.tail(14).mean():.4f}")
    print(f"Gap suggests different calculation or data source")

    # Method 8: Test different window sizes
    print("\n8️⃣ DIFFERENT WINDOW SIZES:")
    print("-" * 40)

    for window in [10, 14, 20, 21, 30]:
        if len(true_range) >= window:
            atr_window = true_range.rolling(window=window).mean().iloc[-1]
            print(f"ATR (window={window}): ${atr_window:.4f}")

    return {
        "our_atr": our_atr,
        "manual_atr_14": atr_sma_14,
        "chatgpt_atr": chatgpt_atr,
        "fresh_price": current_price,
        "analysis_complete": True,
    }


if __name__ == "__main__":
    print("🚀 Starting comprehensive ATR analysis...")
    results = comprehensive_atr_analysis()

    print(f"\n🏆 FINAL ANALYSIS:")
    print("=" * 70)
    print(f"Our Algorithm ATR: ${results['our_atr']:.4f}")
    print(f"Manual Fresh ATR: ${results['manual_atr_14']:.4f}")
    print(f"ChatGPT Expected: ${results['chatgpt_atr']:.2f}")
    print(f"Fresh Market Price: ${results['fresh_price']:.2f}")

    if abs(results["our_atr"] - results["manual_atr_14"]) < 0.01:
        print("✅ Our algorithm calculation is mathematically correct")
    else:
        print("❌ Our algorithm has calculation issues")

    if results["chatgpt_atr"] / results["manual_atr_14"] > 2:
        print(
            "🚨 ChatGPT's ATR is suspiciously high - possible different method or data"
        )
    else:
        print("✅ ChatGPT's ATR is reasonable")
