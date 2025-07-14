#!/usr/bin/env python3
"""
ATR Investigation Script
Deep dive into why our ATR calculation differs so much from ChatGPT's
"""

import sys

sys.path.append("src")

from portfolio_suite.options_trading.core import OptionsTracker
import pandas as pd
import numpy as np
import yfinance as yf


def investigate_atr_calculation():
    """
    Investigate ATR calculation differences
    """
    print("🔍 ATR CALCULATION INVESTIGATION")
    print("=" * 60)

    ticker = "SPY"
    tracker = OptionsTracker()

    # Get our data
    print("📊 OUR DATA SOURCE:")
    print("-" * 40)

    indicators = tracker.get_technical_indicators(ticker)
    our_atr = indicators["atr_14"]
    our_current = indicators["current_price"]
    hist = indicators["price_history"]

    print(f"Our ATR: ${our_atr:.4f}")
    print(f"Our Current Price: ${our_current:.2f}")
    print(f"Data Period: {len(hist)} days")
    print(f"Date Range: {hist.index[0]} to {hist.index[-1]}")

    # Show recent price data
    print("\n📈 RECENT PRICE DATA (Last 10 days):")
    recent = hist.tail(10)[["High", "Low", "Close"]].round(2)
    print(recent)

    # Manual ATR calculation step by step
    print("\n🧮 MANUAL ATR CALCULATION:")
    print("-" * 40)

    # Calculate True Range manually
    high_low = hist["High"] - hist["Low"]
    high_close = np.abs(hist["High"] - hist["Close"].shift())
    low_close = np.abs(hist["Low"] - hist["Close"].shift())
    true_range = np.maximum(high_low, np.maximum(high_close, low_close))

    # Show last 15 days of TR calculation
    print("TRUE RANGE CALCULATION (Last 15 days):")
    tr_data = (
        pd.DataFrame(
            {
                "High": hist["High"],
                "Low": hist["Low"],
                "Close": hist["Close"],
                "Prev_Close": hist["Close"].shift(),
                "H-L": high_low,
                "H-PC": high_close,
                "L-PC": low_close,
                "True_Range": true_range,
            }
        )
        .tail(15)
        .round(4)
    )

    print(tr_data)

    # Calculate ATR different ways
    atr_sma = true_range.rolling(window=14).mean().iloc[-1]
    atr_ema = true_range.ewm(span=14).mean().iloc[-1]

    print(f"\nATR Calculations:")
    print(f"ATR (14-day SMA): ${atr_sma:.4f}")
    print(f"ATR (14-day EMA): ${atr_ema:.4f}")
    print(f"Our Algorithm:    ${our_atr:.4f}")

    # Compare with yfinance directly
    print("\n📊 DIRECT YFINANCE COMPARISON:")
    print("-" * 40)

    try:
        # Get data with different periods
        spy_3mo = yf.download(ticker, period="3mo", interval="1d")
        spy_6mo = yf.download(ticker, period="6mo", interval="1d")
        spy_1yr = yf.download(ticker, period="1y", interval="1d")

        print(f"YFinance 3mo data: {len(spy_3mo)} days")
        print(f"YFinance 6mo data: {len(spy_6mo)} days")
        print(f"YFinance 1yr data: {len(spy_1yr)} days")

        # Calculate ATR for each period
        for period_name, data in [("3mo", spy_3mo), ("6mo", spy_6mo), ("1yr", spy_1yr)]:
            if len(data) > 20:
                data_high_low = data["High"] - data["Low"]
                data_high_close = np.abs(data["High"] - data["Close"].shift())
                data_low_close = np.abs(data["Low"] - data["Close"].shift())
                data_true_range = np.maximum(
                    data_high_low, np.maximum(data_high_close, data_low_close)
                )
                data_atr = data_true_range.rolling(window=14).mean().iloc[-1]

                print(f"ATR ({period_name}): ${data_atr:.4f}")
                print(f"Current Price ({period_name}): ${data['Close'].iloc[-1]:.2f}")
                print(f"Latest Date ({period_name}): {data.index[-1].date()}")

    except Exception as e:
        print(f"Error with direct yfinance: {e}")

    # Check if we're using adjusted vs non-adjusted prices
    print("\n💡 PRICE ADJUSTMENT INVESTIGATION:")
    print("-" * 40)

    try:
        # Get both adjusted and non-adjusted
        spy_raw = yf.download(ticker, period="3mo", auto_adjust=False)
        spy_adj = yf.download(ticker, period="3mo", auto_adjust=True)

        print("Raw vs Adjusted Prices (Last 5 days):")
        comparison = pd.DataFrame(
            {
                "Raw_High": spy_raw["High"].tail(5),
                "Adj_High": spy_adj["High"].tail(5),
                "Raw_Low": spy_raw["Low"].tail(5),
                "Adj_Low": spy_adj["Low"].tail(5),
                "Raw_Close": spy_raw["Close"].tail(5),
                "Adj_Close": spy_adj["Close"].tail(5),
            }
        ).round(2)
        print(comparison)

        # Calculate ATR on both
        for adj_type, data in [("Raw", spy_raw), ("Adjusted", spy_adj)]:
            data_high_low = data["High"] - data["Low"]
            data_high_close = np.abs(data["High"] - data["Close"].shift())
            data_low_close = np.abs(data["Low"] - data["Close"].shift())
            data_true_range = np.maximum(
                data_high_low, np.maximum(data_high_close, data_low_close)
            )
            data_atr = data_true_range.rolling(window=14).mean().iloc[-1]
            print(f"ATR ({adj_type}): ${data_atr:.4f}")

    except Exception as e:
        print(f"Error with price adjustment check: {e}")

    # Check our implementation source
    print("\n🔍 OUR IMPLEMENTATION CHECK:")
    print("-" * 40)

    # Let's look at the actual function
    try:
        # Check what period we're using
        indicators_1mo = tracker.get_technical_indicators(ticker, period="1mo")
        indicators_3mo = tracker.get_technical_indicators(ticker, period="3mo")
        indicators_6mo = tracker.get_technical_indicators(ticker, period="6mo")

        print(f"Our ATR (1mo):  ${indicators_1mo.get('atr_14', 0):.4f}")
        print(f"Our ATR (3mo):  ${indicators_3mo.get('atr_14', 0):.4f}")
        print(f"Our ATR (6mo):  ${indicators_6mo.get('atr_14', 0):.4f}")

        print(f"Data points (1mo): {len(indicators_1mo.get('price_history', []))}")
        print(f"Data points (3mo): {len(indicators_3mo.get('price_history', []))}")
        print(f"Data points (6mo): {len(indicators_6mo.get('price_history', []))}")

    except Exception as e:
        print(f"Error checking different periods: {e}")

    print("\n🎯 CHATGPT'S EXPECTED VALUES:")
    print("-" * 40)
    print(f"ChatGPT Current Price: $624.93")
    print(f"ChatGPT ATR: $11.70")
    print(f"Our Current Price: ${our_current:.2f}")
    print(f"Our ATR: ${our_atr:.4f}")
    print(f"ATR Ratio: {11.70 / our_atr:.2f}x larger")

    # Hypothesis testing
    print("\n🧪 HYPOTHESIS TESTING:")
    print("-" * 40)
    print("Possible causes for ATR difference:")
    print("1. Different time periods (we might be using shorter period)")
    print("2. Different data sources (splits/adjustments)")
    print("3. Different ATR calculation method (SMA vs EMA)")
    print("4. Data freshness (we might have older data)")
    print("5. Calculation bug in our implementation")

    return {
        "our_atr": our_atr,
        "chatgpt_atr": 11.70,
        "difference": abs(our_atr - 11.70),
        "ratio": 11.70 / our_atr if our_atr > 0 else 0,
    }


if __name__ == "__main__":
    results = investigate_atr_calculation()
    print(f"\n🏆 INVESTIGATION COMPLETE")
    print(f"ATR Difference: ${results['difference']:.4f}")
    print(f"ChatGPT ATR is {results['ratio']:.1f}x larger than ours")
