#!/usr/bin/env python3
"""
Demo of Enhanced Detailed Technical Analysis
============================================

This script demonstrates the new mathematical calculation breakdown
that shows users exactly how price predictions are calculated.
"""

import sys
import os
sys.path.append('src')

from portfolio_suite.options_trading.core import OptionsTracker

def demo_enhanced_analysis():
    """Demonstrate the enhanced detailed technical analysis features"""
    
    print("🎯 Enhanced Detailed Technical Analysis Demo")
    print("=" * 50)
    
    # Initialize tracker
    tracker = OptionsTracker()
    
    # Get a test ticker
    if not tracker.watchlist:
        print("📋 Refreshing watchlist...")
        tracker.refresh_watchlist()
    
    if not tracker.watchlist:
        print("⚠️ No tickers available, using AAPL for demo")
        test_ticker = "AAPL"
    else:
        test_ticker = list(tracker.watchlist.keys())[0]
    
    print(f"🔍 Analyzing: {test_ticker}")
    print("-" * 30)
    
    # Get prediction with all detailed fields
    prediction = tracker.predict_price_range(test_ticker)
    
    if not prediction:
        print("❌ Failed to get prediction")
        return
    
    # Display the same calculations that will appear in the UI
    current_price = prediction['current_price']
    weekly_vol = prediction['weekly_volatility']
    indicators = prediction['indicators']
    bias_score = prediction.get('bias_score', 0)
    
    print(f"📊 Current Price: ${current_price:.2f}")
    print(f"📈 Weekly Volatility: {weekly_vol:.3f} ({weekly_vol:.1%})")
    print(f"⚖️ Bias Score: {bias_score:+.3f}")
    
    print("\n🧮 Mathematical Breakdown (as shown in UI):")
    print("-" * 40)
    
    # Step 1: Volatility Analysis
    print("📊 Step 1: Volatility Analysis")
    annual_vol = weekly_vol * (52 ** 0.5)
    base_range = current_price * weekly_vol
    print(f"   Annual Volatility: {annual_vol:.1%}")
    print(f"   Base Range: ${current_price:.2f} × {weekly_vol:.3f} = ${base_range:.2f}")
    
    # Step 2: Technical Bias
    print("\n⚖️ Step 2: Technical Bias Calculation")
    rsi = indicators.get('rsi', 50)
    macd = indicators.get('macd', 0)
    macd_signal = indicators.get('macd_signal', 0)
    momentum = indicators.get('momentum', 0)
    
    # Calculate individual bias components (same logic as in core)
    rsi_bias = 0
    if rsi > 70:
        rsi_bias = -0.2
        print(f"   RSI: {rsi:.1f} > 70 (Overbought) → -0.2")
    elif rsi < 30:
        rsi_bias = 0.2
        print(f"   RSI: {rsi:.1f} < 30 (Oversold) → +0.2")
    else:
        print(f"   RSI: {rsi:.1f} (Neutral) → 0.0")
    
    macd_bias = 0.1 if macd > macd_signal else -0.1
    macd_direction = "Bullish" if macd > macd_signal else "Bearish"
    print(f"   MACD: {macd:.3f} vs {macd_signal:.3f} ({macd_direction}) → {macd_bias:+.1f}")
    
    momentum_bias = 0
    if momentum > 2:
        momentum_bias = 0.1
        print(f"   Momentum: {momentum:.2f}% > 2% (Strong Up) → +0.1")
    elif momentum < -2:
        momentum_bias = -0.1
        print(f"   Momentum: {momentum:.2f}% < -2% (Strong Down) → -0.1")
    else:
        print(f"   Momentum: {momentum:.2f}% (Neutral) → 0.0")
    
    print(f"   Total: {rsi_bias:+.1f} + {macd_bias:+.1f} + {momentum_bias:+.1f} = {bias_score:+.2f}")
    
    # Step 3: Final Range
    print("\n🎯 Step 3: Final Price Range")
    bias_adjustment = current_price * bias_score * 0.01
    lower_bound = prediction['lower_bound']
    upper_bound = prediction['upper_bound']
    
    print(f"   Bias Adjustment: ${current_price:.2f} × {bias_score:.3f} × 0.01 = ${bias_adjustment:.2f}")
    print(f"   Final Range: ${lower_bound:.2f} - ${upper_bound:.2f}")
    print(f"   Target Price: ${prediction['target_price']:.2f}")
    
    # Step 4: Probability
    print("\n📊 Step 4: Bullish Probability")
    bullish_prob = prediction['bullish_probability']
    print(f"   Formula: 50% + ({bias_score:.3f} × 50%) = {bullish_prob:.1%}")
    
    # Trading Implications
    print("\n💡 Trading Implications:")
    range_width = upper_bound - lower_bound
    range_pct = range_width / current_price
    
    if range_pct > 0.08:
        print("   🌪️ High Volatility (>8%) - Consider selling premium")
    elif range_pct < 0.03:
        print("   😴 Low Volatility (<3%) - Consider buying options")
    else:
        print("   ⚖️ Moderate Volatility (3-8%) - Balanced approach")
    
    if bias_score > 0.15:
        print("   📈 Strong Bullish Bias - Bull put spreads")
    elif bias_score < -0.15:
        print("   📉 Strong Bearish Bias - Bear call spreads")
    else:
        print("   ⚖️ Neutral Bias - Iron condors/straddles")
    
    print(f"\n✨ Enhanced Analysis Complete!")
    print(f"🎯 This detailed breakdown is now available in the UI under:")
    print(f"   📈 Market Analysis → 🔍 Detailed Technical Analysis")
    print(f"   Select '{test_ticker}' and expand the calculation sections!")

if __name__ == "__main__":
    demo_enhanced_analysis()
