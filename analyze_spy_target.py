"""
Simple script to analyze SPY technical indicators
"""

import sys
sys.path.append('.')
import yfinance as yf
import numpy as np
import pandas as pd
from datetime import datetime

def analyze_spy_technicals():
    """Analyze SPY technical indicators to understand price target"""
    print("Analyzing SPY technical indicators...")
    
    # Get SPY data
    spy = yf.Ticker("SPY")
    hist = spy.history(period="3mo")
    
    # Calculate last week's performance
    last_week_perf = (hist['Close'].iloc[-1] - hist['Close'].iloc[-6]) / hist['Close'].iloc[-6] * 100
    
    # Calculate indicators
    close = hist['Close']
    
    # Moving averages
    ma_5 = close.rolling(window=5).mean()
    ma_10 = close.rolling(window=10).mean()
    ma_20 = close.rolling(window=20).mean()
    
    # RSI
    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    # MACD
    ema_12 = close.ewm(span=12).mean()
    ema_26 = close.ewm(span=26).mean()
    macd = ema_12 - ema_26
    signal = macd.ewm(span=9).mean()
    
    # Momentum
    momentum = (close.iloc[-1] - close.iloc[-6]) / close.iloc[-6] * 100
    
    # Print results
    print(f"\nSPY Current price: ${close.iloc[-1]:.2f}")
    print(f"Last week's performance: {last_week_perf:.2f}%")
    print("\nTechnical indicators:")
    print(f"RSI: {rsi.iloc[-1]:.2f}")
    print(f"MACD: {macd.iloc[-1]:.4f}")
    print(f"MACD Signal: {signal.iloc[-1]:.4f}")
    print(f"Momentum: {momentum:.2f}%")
    print(f"MA5: ${ma_5.iloc[-1]:.2f}")
    print(f"MA10: ${ma_10.iloc[-1]:.2f}")
    print(f"MA20: ${ma_20.iloc[-1]:.2f}")
    
    # Analyze bias score components
    print("\nBias score components:")
    
    # RSI contribution
    rsi_value = rsi.iloc[-1]
    rsi_bias = 0
    if rsi_value > 70:
        rsi_bias = -0.2  # Overbought, bearish bias
        print(f"RSI {rsi_value:.2f} > 70: Overbought, bearish bias (-0.2)")
    elif rsi_value < 30:
        rsi_bias = 0.2  # Oversold, bullish bias
        print(f"RSI {rsi_value:.2f} < 30: Oversold, bullish bias (0.2)")
    else:
        print(f"RSI {rsi_value:.2f}: Neutral (0.0)")
    
    # MACD contribution
    macd_bias = 0
    if macd.iloc[-1] > signal.iloc[-1]:
        macd_bias = 0.1  # Bullish momentum
        print(f"MACD > Signal: Bullish momentum (0.1)")
    else:
        macd_bias = -0.1  # Bearish momentum
        print(f"MACD < Signal: Bearish momentum (-0.1)")
    
    # MA contribution
    ma_bias = 0
    if close.iloc[-1] > ma_20.iloc[-1]:
        ma_bias = 0.1  # Price above MA20 is bullish
        print(f"Price ${close.iloc[-1]:.2f} > MA20 ${ma_20.iloc[-1]:.2f}: Bullish (0.1)")
    else:
        ma_bias = -0.1  # Price below MA20 is bearish
        print(f"Price ${close.iloc[-1]:.2f} < MA20 ${ma_20.iloc[-1]:.2f}: Bearish (-0.1)")
    
    # Momentum contribution
    mom_bias = 0
    if momentum > 2:
        mom_bias = 0.1
        print(f"Momentum {momentum:.2f}% > 2%: Bullish (0.1)")
    elif momentum < -2:
        mom_bias = -0.1
        print(f"Momentum {momentum:.2f}% < -2%: Bearish (-0.1)")
    else:
        print(f"Momentum {momentum:.2f}%: Neutral (0.0)")
    
    # Calculate total bias score
    total_bias = rsi_bias + macd_bias + ma_bias + mom_bias
    print(f"\nTotal technical bias score: {total_bias:.2f}")
    
    # Calculate target price
    current_price = close.iloc[-1]
    bias_adjustment = current_price * total_bias * 0.01
    target_price = current_price + bias_adjustment
    print(f"\nTarget calculation:")
    print(f"Current price: ${current_price:.2f}")
    print(f"Bias adjustment: {bias_adjustment:.2f} ({total_bias:.2f}% of current price)")
    print(f"Target price: ${target_price:.2f} ({(target_price/current_price - 1) * 100:.2f}% change)")

if __name__ == "__main__":
    analyze_spy_technicals()
