#!/usr/bin/env python3
"""
Verify if our implementation follows the ATR-based specification
"""

import sys

sys.path.append("/Users/soliv112/PersonalProjects/PortfolioSuite/src")

from portfolio_suite.options_trading.core import OptionsTracker
import yfinance as yf
import numpy as np
import pandas as pd


def calculate_atr_manual(ticker, period=14):
    """Calculate ATR manually according to specification"""
    stock = yf.Ticker(ticker)
    hist = stock.history(period="3mo")

    if hist.empty:
        return None

    high = hist["High"]
    low = hist["Low"]
    close = hist["Close"]
    prev_close = close.shift(1)

    # True Range calculation
    tr1 = high - low
    tr2 = abs(high - prev_close)
    tr3 = abs(low - prev_close)

    true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    # ATR is 14-day rolling average of True Range
    atr = true_range.rolling(window=period).mean()

    return {"current_price": close.iloc[-1], "atr": atr.iloc[-1], "data": hist}


def test_specification_example():
    """Test the exact example from specification"""
    print("🔍 Testing SPY Example from Specification")
    print("=" * 50)

    # Get SPY data
    spy_data = calculate_atr_manual("SPY")
    if not spy_data:
        print("❌ Could not get SPY data")
        return

    current_price = spy_data["current_price"]
    atr = spy_data["atr"]

    print(f"📊 SPY Current Data:")
    print(f"   Current Price: ${current_price:.2f}")
    print(f"   ATR (14-day): ${atr:.2f}")

    # Specification example values
    spec_price = 624.93
    spec_atr = 11.70
    spec_bias = 0.1

    print(f"\n📋 Specification Example:")
    print(f"   Current Price: ${spec_price:.2f}")
    print(f"   ATR (14-day): ${spec_atr:.2f}")
    print(f"   Bias Score: {spec_bias}")

    # Calculate according to specification
    print(f"\n🧮 Specification Calculations:")
    bias_pct = spec_bias * 0.01  # 0.1 × 0.01 = 0.001
    bias_adjustment = spec_price * bias_pct  # 624.93 × 0.001 = $0.62
    target_mid = spec_price + bias_adjustment  # 624.93 + 0.62 = $625.55
    predicted_low = target_mid - spec_atr  # 625.55 - 11.70 = $613.85
    predicted_high = target_mid + spec_atr  # 625.55 + 11.70 = $637.25
    range_dollar = predicted_high - predicted_low  # 637.25 - 613.85 = $23.40
    range_percent = (range_dollar / spec_price) * 100  # (23.40 / 624.93) × 100 = 3.74%

    print(f"   Bias (%) = {spec_bias} × 0.01 = {bias_pct:.3f}")
    print(
        f"   Bias Adjustment = ${spec_price:.2f} × {bias_pct:.3f} = ${bias_adjustment:.2f}"
    )
    print(
        f"   Target Mid = ${spec_price:.2f} + ${bias_adjustment:.2f} = ${target_mid:.2f}"
    )
    print(
        f"   Predicted Low = ${target_mid:.2f} - ${spec_atr:.2f} = ${predicted_low:.2f}"
    )
    print(
        f"   Predicted High = ${target_mid:.2f} + ${spec_atr:.2f} = ${predicted_high:.2f}"
    )
    print(
        f"   Range ($) = ${predicted_high:.2f} - ${predicted_low:.2f} = ${range_dollar:.2f}"
    )
    print(
        f"   Range (%) = (${range_dollar:.2f} / ${spec_price:.2f}) × 100 = {range_percent:.2f}%"
    )


def test_current_implementation():
    """Test our current implementation"""
    print(f"\n🔍 Testing Current Implementation")
    print("=" * 50)

    tracker = OptionsTracker()

    # Test with different regime multipliers
    print(f"\n📊 SPY Current Implementation (regime_multiplier=0.01):")
    result = tracker.predict_price_range("SPY", regime_multiplier=0.01)

    if result:
        current_price = result["current_price"]
        target_price = result["target_price"]
        lower_bound = result["lower_bound"]
        upper_bound = result["upper_bound"]
        bias_score = result["bias_score"]

        range_dollar = upper_bound - lower_bound
        range_percent = (range_dollar / current_price) * 100
        bias_adjustment = target_price - current_price

        print(f"   Current Price: ${current_price:.2f}")
        print(f"   Bias Score: {bias_score:.3f}")
        print(f"   Bias Adjustment: ${bias_adjustment:.2f}")
        print(f"   Target Price: ${target_price:.2f}")
        print(f"   Lower Bound: ${lower_bound:.2f}")
        print(f"   Upper Bound: ${upper_bound:.2f}")
        print(f"   Range ($): ${range_dollar:.2f}")
        print(f"   Range (%): {range_percent:.2f}%")

        print(f"\n🔍 Analysis:")
        print(f"   Uses ATR? ❌ No - uses implied/historical volatility")
        print(f"   Range calculation: volatility-based, not ATR-based")
        print(f"   Formula: base_range = current_price * weekly_vol")
    else:
        print("❌ Could not get prediction from current implementation")


if __name__ == "__main__":
    print("🧪 ATR Specification Verification")
    print("=" * 60)

    test_specification_example()
    test_current_implementation()

    print(f"\n💡 CONCLUSION:")
    print(f"   ❌ Current implementation does NOT follow ATR specification")
    print(f"   ❌ Missing ATR calculation entirely")
    print(f"   ❌ Using volatility-based range instead of ATR-based")
    print(f"   ❌ Wrong default regime multiplier (0.001 vs 0.01)")
