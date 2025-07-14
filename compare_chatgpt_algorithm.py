#!/usr/bin/env python3
"""
ChatGPT Algorithm Comparison for SPY
Compare our implementation with ChatGPT's step-by-step process
"""

import sys

sys.path.append("src")

from portfolio_suite.options_trading.core import OptionsTracker
import numpy as np


def compare_chatgpt_algorithm():
    """
    Compare our algorithm with ChatGPT's exact process for SPY
    """
    print("🔍 CHATGPT ALGORITHM COMPARISON FOR SPY")
    print("=" * 60)

    ticker = "SPY"
    tracker = OptionsTracker()

    # Get our algorithm's results
    print("📊 OUR ALGORITHM RESULTS:")
    print("-" * 40)

    indicators = tracker.get_technical_indicators(ticker)
    prediction = tracker.predict_price_range_dual_model(ticker)

    our_current = indicators["current_price"]
    our_atr = indicators["atr_14"]
    our_rsi = indicators.get("rsi", 50)
    our_macd = indicators.get("macd", 0)
    our_macd_signal = indicators.get("macd_signal", 0)
    our_momentum = indicators.get("momentum", 0)
    our_regime_score = prediction.get("regime_score", 0)
    our_target_mid = prediction.get("target_mid", 0)
    our_predicted_low = prediction.get("predicted_low", 0)
    our_predicted_high = prediction.get("predicted_high", 0)
    our_range_width_pct = prediction.get("range_width_%", 0)

    print(f"Current Price: ${our_current:.2f}")
    print(f"ATR (14-day): ${our_atr:.2f}")
    print(f"RSI: {our_rsi:.1f}")
    print(f"MACD: {our_macd:.3f}")
    print(f"MACD Signal: {our_macd_signal:.3f}")
    print(f"MACD Bullish: {our_macd > our_macd_signal}")
    print(f"Momentum: {our_momentum:.1f}%")
    print(f"Regime Score: {our_regime_score:+.1f}")
    print(f"Target Mid: ${our_target_mid:.2f}")
    print(f"Predicted Low: ${our_predicted_low:.2f}")
    print(f"Predicted High: ${our_predicted_high:.2f}")
    print(f"Range Width %: {our_range_width_pct:.2f}%")

    # ChatGPT's stated values
    print("\n📋 CHATGPT'S STATED VALUES:")
    print("-" * 40)
    chatgpt_current = 624.93
    chatgpt_atr = 11.70
    chatgpt_rsi = 67.3
    chatgpt_macd_bullish = True
    chatgpt_momentum = 0.7
    chatgpt_regime_score = 0.1
    chatgpt_target_mid = 625.55
    chatgpt_predicted_low = 613.85
    chatgpt_predicted_high = 637.25
    chatgpt_range_width_pct = 3.78

    print(f"Current Price: ${chatgpt_current:.2f}")
    print(f"ATR (14-day): ${chatgpt_atr:.2f}")
    print(f"RSI: {chatgpt_rsi:.1f}")
    print(f"MACD: Bullish = {chatgpt_macd_bullish}")
    print(f"Momentum: {chatgpt_momentum:.1f}%")
    print(f"Regime Score: {chatgpt_regime_score:+.1f}")
    print(f"Target Mid: ${chatgpt_target_mid:.2f}")
    print(f"Predicted Low: ${chatgpt_predicted_low:.2f}")
    print(f"Predicted High: ${chatgpt_predicted_high:.2f}")
    print(f"Range Width %: {chatgpt_range_width_pct:.2f}%")

    # Step-by-step comparison
    print("\n🔍 STEP-BY-STEP ALGORITHM COMPARISON:")
    print("=" * 60)

    # Step 1: Current Price
    print("1️⃣ CURRENT PRICE COMPARISON:")
    price_diff = abs(our_current - chatgpt_current)
    print(f"   Our Price: ${our_current:.2f}")
    print(f"   ChatGPT:   ${chatgpt_current:.2f}")
    print(
        f"   Difference: ${price_diff:.2f} ({'✅ MATCH' if price_diff < 1.0 else '❌ DIFFERENT'})"
    )

    # Step 2: ATR Comparison
    print("\n2️⃣ ATR CALCULATION COMPARISON:")
    atr_diff = abs(our_atr - chatgpt_atr)
    print(f"   Our ATR:   ${our_atr:.2f}")
    print(f"   ChatGPT:   ${chatgpt_atr:.2f}")
    print(
        f"   Difference: ${atr_diff:.2f} ({'✅ CLOSE' if atr_diff < 2.0 else '❌ VERY DIFFERENT'})"
    )

    # Step 3: Regime Bias Analysis
    print("\n3️⃣ REGIME BIAS COMPARISON:")

    # Our regime calculation (detailed)
    print("   OUR REGIME CALCULATION:")
    if our_rsi > 70:
        our_rsi_bias = -0.2
        our_rsi_label = "Overbought"
    elif our_rsi < 30:
        our_rsi_bias = 0.2
        our_rsi_label = "Oversold"
    else:
        our_rsi_bias = 0.0
        our_rsi_label = "Neutral"

    our_macd_bias = 0.1 if our_macd > our_macd_signal else -0.1
    our_macd_label = "Bullish" if our_macd > our_macd_signal else "Bearish"

    if our_momentum > 2:
        our_momentum_bias = 0.1
    elif our_momentum < -2:
        our_momentum_bias = -0.1
    else:
        our_momentum_bias = 0.0

    our_calculated_regime = our_rsi_bias + our_macd_bias + our_momentum_bias

    print(f"     RSI {our_rsi:.1f} → Bias: {our_rsi_bias:+.1f} ({our_rsi_label})")
    print(f"     MACD {our_macd_label} → Bias: {our_macd_bias:+.1f}")
    print(f"     Momentum {our_momentum:.1f}% → Bias: {our_momentum_bias:+.1f}")
    print(f"     Total Regime Score: {our_calculated_regime:+.1f}")

    # ChatGPT's regime calculation
    print("   CHATGPT'S REGIME CALCULATION:")
    chatgpt_rsi_bias = 0.0  # RSI 67.3 = Neutral
    chatgpt_macd_bias = 0.1  # Bullish
    chatgpt_momentum_bias = 0.0  # 0.7% = Neutral

    print(f"     RSI {chatgpt_rsi:.1f} → Bias: {chatgpt_rsi_bias:+.1f} (Neutral)")
    print(f"     MACD Bullish → Bias: {chatgpt_macd_bias:+.1f}")
    print(f"     Momentum {chatgpt_momentum:.1f}% → Bias: {chatgpt_momentum_bias:+.1f}")
    print(f"     Total Regime Score: {chatgpt_regime_score:+.1f}")

    regime_match = abs(our_calculated_regime - chatgpt_regime_score) < 0.01
    print(f"   Regime Logic Match: {'✅ SAME' if regime_match else '❌ DIFFERENT'}")

    # Step 4: Target Mid Calculation
    print("\n4️⃣ TARGET MID CALCULATION:")

    # Our calculation
    our_bias_pct = our_calculated_regime * 0.01
    our_calc_target = our_current * (1 + our_bias_pct)

    print(f"   OUR CALCULATION:")
    print(f"     Bias % = {our_calculated_regime:+.1f} × 0.01 = {our_bias_pct:+.5f}")
    print(
        f"     Target = {our_current:.2f} × (1 + {our_bias_pct:+.5f}) = ${our_calc_target:.2f}"
    )

    # ChatGPT's calculation
    chatgpt_bias_pct = chatgpt_regime_score * 0.001  # Note: ChatGPT uses 0.001!
    chatgpt_calc_target = chatgpt_current + (chatgpt_current * chatgpt_bias_pct)

    print(f"   CHATGPT'S CALCULATION:")
    print(
        f"     Bias Adjustment = {chatgpt_current:.2f} × {chatgpt_bias_pct:.3f} = {chatgpt_current * chatgpt_bias_pct:.2f}"
    )
    print(
        f"     Target = {chatgpt_current:.2f} + {chatgpt_current * chatgpt_bias_pct:.2f} = ${chatgpt_calc_target:.2f}"
    )

    target_formula_match = abs(chatgpt_bias_pct - our_bias_pct) < 0.001
    print(
        f"   Target Formula Match: {'✅ SAME' if target_formula_match else '❌ DIFFERENT MULTIPLIER!'}"
    )

    # Step 5: Range Calculation
    print("\n5️⃣ RANGE CALCULATION:")

    print(f"   OUR RANGE:")
    print(
        f"     Low  = {our_target_mid:.2f} - {our_atr:.2f} = ${our_predicted_low:.2f}"
    )
    print(
        f"     High = {our_target_mid:.2f} + {our_atr:.2f} = ${our_predicted_high:.2f}"
    )

    print(f"   CHATGPT'S RANGE:")
    print(
        f"     Low  = {chatgpt_target_mid:.2f} - {chatgpt_atr:.2f} = ${chatgpt_predicted_low:.2f}"
    )
    print(
        f"     High = {chatgpt_target_mid:.2f} + {chatgpt_atr:.2f} = ${chatgpt_predicted_high:.2f}"
    )

    range_logic_match = True  # Same ATR ± logic
    print(f"   Range Logic Match: {'✅ SAME' if range_logic_match else '❌ DIFFERENT'}")

    # Final Analysis
    print("\n🏆 ALGORITHM DIFFERENCES IDENTIFIED:")
    print("=" * 60)

    differences = []

    if price_diff >= 1.0:
        differences.append(
            f"📊 Current Price: Ours ${our_current:.2f} vs ChatGPT ${chatgpt_current:.2f}"
        )

    if atr_diff >= 2.0:
        differences.append(
            f"📈 ATR Calculation: Ours ${our_atr:.2f} vs ChatGPT ${chatgpt_atr:.2f}"
        )

    if not regime_match:
        differences.append(
            f"⚖️ Regime Scoring: Ours {our_calculated_regime:+.1f} vs ChatGPT {chatgpt_regime_score:+.1f}"
        )

    if not target_formula_match:
        differences.append(f"🎯 Target Formula: We use ×0.01, ChatGPT uses ×0.001")

    if differences:
        print("❌ KEY DIFFERENCES FOUND:")
        for i, diff in enumerate(differences, 1):
            print(f"   {i}. {diff}")
    else:
        print("✅ ALGORITHMS ARE IDENTICAL!")

    return len(differences) == 0


if __name__ == "__main__":
    algorithms_match = compare_chatgpt_algorithm()
    print(
        f"\n🎯 FINAL RESULT: {'✅ SAME ALGORITHM' if algorithms_match else '❌ DIFFERENT ALGORITHMS'}"
    )
