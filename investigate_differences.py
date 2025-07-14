#!/usr/bin/env python3
"""
Investigation script to understand the differences between our algorithm and ChatGPT's results
"""

import sys
import os
import pandas as pd
import numpy as np

sys.path.append("src")

from portfolio_suite.options_trading.core import OptionsTracker


def investigate_differences():
    """
    Detailed investigation of why our results differ from ChatGPT's
    """
    print("🔍 INVESTIGATING ALGORITHM DIFFERENCES")
    print("=" * 60)

    # Load ChatGPT results
    try:
        chatgpt_df = pd.read_csv(
            "Full_2-Week_Prediction_Table__July_26_.csv", index_col=0
        )
        print("📋 ChatGPT Results Loaded")
    except Exception as e:
        print(f"❌ Could not load ChatGPT results: {e}")
        return

    tracker = OptionsTracker()

    print("\n🎯 KEY DIFFERENCES ANALYSIS")
    print("-" * 40)

    # Test with both multipliers to see the impact
    test_tickers = ["SPY", "QQQ", "AAPL", "MSFT", "NVDA"]

    for ticker in test_tickers:
        if ticker in chatgpt_df.index:
            print(f"\n📊 ANALYZING {ticker}")
            print("-" * 30)

            # Get ChatGPT data
            cgpt = chatgpt_df.loc[ticker]
            chatgpt_current = cgpt["Current Price"]
            chatgpt_target = cgpt["Target Mid"]
            chatgpt_range_width = cgpt["Range Width ($)"]

            # Our algorithm with default (0.001) multiplier
            prediction_default = tracker.predict_price_range(ticker)
            our_current_default = prediction_default.get("current_price", 0)
            our_target_default = prediction_default.get("target_price", 0)
            our_range_default = prediction_default.get(
                "upper_bound", 0
            ) - prediction_default.get("lower_bound", 0)

            # Our algorithm with 0.01 multiplier (original)
            prediction_strong = tracker.predict_price_range(
                ticker, regime_multiplier=0.01
            )
            our_target_strong = prediction_strong.get("target_price", 0)

            print(f"Current Price:")
            print(f"  ChatGPT:     ${chatgpt_current:.2f}")
            print(f"  Our Algo:    ${our_current_default:.2f}")
            print(f"  Difference:  ${abs(chatgpt_current - our_current_default):.2f}")

            if abs(chatgpt_current - our_current_default) > 1:
                print(f"  ⚠️  MAJOR PRICE DISCREPANCY!")

            print(f"\nTarget Price (0.001 multiplier):")
            print(f"  ChatGPT:     ${chatgpt_target:.2f}")
            print(f"  Our Algo:    ${our_target_default:.2f}")
            print(f"  Difference:  ${abs(chatgpt_target - our_target_default):.2f}")

            print(f"\nTarget Price (0.01 multiplier):")
            print(f"  Our Algo:    ${our_target_strong:.2f}")
            print(f"  vs ChatGPT:  ${abs(chatgpt_target - our_target_strong):.2f} diff")

            print(f"\nRange Width:")
            print(f"  ChatGPT:     ${chatgpt_range_width:.2f}")
            print(f"  Our Algo:    ${our_range_default:.2f}")
            print(f"  Difference:  ${abs(chatgpt_range_width - our_range_default):.2f}")

            # Calculate what multiplier ChatGPT might be using
            if our_current_default > 0 and chatgpt_current > 0:
                bias_score = prediction_default.get("bias_score", 0)
                if bias_score != 0:
                    chatgpt_bias_adjustment = chatgpt_target - chatgpt_current
                    implied_multiplier = chatgpt_bias_adjustment / (
                        chatgpt_current * bias_score
                    )
                    print(f"\nChatGPT's Implied Multiplier:")
                    print(f"  Bias Score:       {bias_score:.3f}")
                    print(f"  Bias Adjustment:  ${chatgpt_bias_adjustment:.4f}")
                    print(f"  Implied Mult:     {implied_multiplier:.6f}")


def compare_technical_indicators():
    """
    Compare the technical indicators we're calculating vs what ChatGPT might be using
    """
    print("\n\n🔬 TECHNICAL INDICATORS COMPARISON")
    print("=" * 50)

    tracker = OptionsTracker()
    test_ticker = "SPY"

    indicators = tracker.get_technical_indicators(test_ticker)

    print(f"Technical Indicators for {test_ticker}:")
    print(f"  Current Price: ${indicators.get('current_price', 0):.2f}")
    print(f"  RSI:          {indicators.get('rsi', 0):.2f}")
    print(f"  MACD:         {indicators.get('macd', 0):.4f}")
    print(f"  MACD Signal:  {indicators.get('macd_signal', 0):.4f}")
    print(f"  Momentum:     {indicators.get('momentum', 0):.2f}%")
    print(f"  Volatility:   {indicators.get('volatility', 0):.2%}")

    # Manual regime score
    rsi = indicators.get("rsi", 50)
    macd = indicators.get("macd", 0)
    macd_signal = indicators.get("macd_signal", 0)
    momentum = indicators.get("momentum", 0)

    # RSI bias
    if rsi > 70:
        rsi_bias = -0.2
    elif rsi < 30:
        rsi_bias = 0.2
    else:
        rsi_bias = 0.0

    # MACD bias
    macd_bias = 0.1 if macd > macd_signal else -0.1

    # Momentum bias
    if momentum > 2:
        momentum_bias = 0.1
    elif momentum < -2:
        momentum_bias = -0.1
    else:
        momentum_bias = 0.0

    regime_score = rsi_bias + macd_bias + momentum_bias

    print(f"\nRegime Score Components:")
    print(f"  RSI Bias:       {rsi_bias:+.1f}")
    print(f"  MACD Bias:      {macd_bias:+.1f}")
    print(f"  Momentum Bias:  {momentum_bias:+.1f}")
    print(f"  Total Score:    {regime_score:+.2f}")


def test_date_sensitivity():
    """
    Test if the date difference is causing the price discrepancies
    """
    print("\n\n📅 DATE SENSITIVITY ANALYSIS")
    print("=" * 40)

    import yfinance as yf

    # Check AAPL specifically since it has the biggest discrepancy
    ticker = "AAPL"
    stock = yf.Ticker(ticker)

    # Get recent price history
    hist = stock.history(period="1mo")

    print(f"Recent {ticker} prices:")
    print(hist[["Close"]].tail(10))

    print(f"\nChatGPT date: 2025-07-11")
    print(f"Current date: 2025-07-13")
    print(f"Latest price: ${hist['Close'].iloc[-1]:.2f}")


if __name__ == "__main__":
    investigate_differences()
    compare_technical_indicators()
    test_date_sensitivity()
