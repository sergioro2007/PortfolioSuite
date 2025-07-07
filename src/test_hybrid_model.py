"""
Test script for the hybrid target zone model for price predictions.

This script demonstrates how we can combine technical bias with implied volatility
to create a more accurate price range prediction.
"""

import yfinance as yf
import numpy as np
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

def get_technical_indicators(ticker, period="3mo"):
    """Calculate technical indicators for price prediction"""
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        
        if hist.empty:
            return {}
        
        # Calculate indicators
        close = hist['Close']
        volume = hist['Volume']
        
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
        
        # Current values
        current_price = close.iloc[-1]
        
        return {
            'current_price': current_price,
            'ma_5': ma_5.iloc[-1],
            'ma_10': ma_10.iloc[-1],
            'ma_20': ma_20.iloc[-1],
            'rsi': rsi.iloc[-1],
            'macd': macd.iloc[-1],
            'macd_signal': signal.iloc[-1],
            'volatility': close.pct_change().std() * np.sqrt(252),  # Annualized
            'momentum': (current_price - close.iloc[-5]) / close.iloc[-5] * 100
        }
    except Exception as e:
        print(f"Error calculating indicators for {ticker}: {e}")
        return {}

def get_implied_volatility(ticker, current_price=None):
    """Get implied volatility data from options chain"""
    try:
        stock = yf.Ticker(ticker)
        
        # Get current price if not provided
        if current_price is None:
            try:
                info = stock.info
                current_price = info.get('regularMarketPrice', info.get('previousClose', 100))
            except Exception:
                # Fall back to historical data
                hist = stock.history(period="1d")
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                else:
                    current_price = 100
        
        # Try to get options chain
        if hasattr(stock, 'options') and stock.options:
            # Get nearest expiration
            nearest_exp = stock.options[0]
            options = stock.option_chain(nearest_exp)
            
            # Find ATM options (within 5% of current price)
            atm_calls = options.calls[
                (options.calls['strike'] >= current_price * 0.95) & 
                (options.calls['strike'] <= current_price * 1.05)
            ]
            atm_puts = options.puts[
                (options.puts['strike'] >= current_price * 0.95) & 
                (options.puts['strike'] <= current_price * 1.05)
            ]
            
            # Extract implied volatilities
            ivs = []
            
            # From calls
            if 'impliedVolatility' in atm_calls.columns and not atm_calls.empty:
                call_ivs = atm_calls['impliedVolatility'].dropna().tolist()
                ivs.extend(call_ivs)
            
            # From puts
            if 'impliedVolatility' in atm_puts.columns and not atm_puts.empty:
                put_ivs = atm_puts['impliedVolatility'].dropna().tolist()
                ivs.extend(put_ivs)
            
            # If we have IV values, use their average
            if ivs:
                annual_iv = float(sum(ivs) / len(ivs))
                weekly_vol = annual_iv / np.sqrt(52)  # Convert to weekly
                
                return {
                    'valid': True,
                    'annual_iv': annual_iv,
                    'weekly_vol': weekly_vol
                }
        
        # If we get here, return invalid result
        return {'valid': False}
        
    except Exception as e:
        print(f"IV calculation error for {ticker}: {e}")
        return {'valid': False}

def predict_price_range(ticker):
    """Predict 1-week price range using hybrid model: technical bias + IV-based range"""
    try:
        indicators = get_technical_indicators(ticker)
        if not indicators:
            return {}
        
        current_price = indicators['current_price']
        historical_vol = indicators['volatility']
        
        # Step 1: Try to get implied volatility data from options
        iv_data = get_implied_volatility(ticker, current_price)
        
        # Use IV if available, otherwise fall back to historical volatility
        if iv_data and iv_data.get('valid', False):
            weekly_vol = iv_data['weekly_vol']
            print(f"Using implied volatility for {ticker}: {iv_data['annual_iv']:.1%} annual, {weekly_vol:.1%} weekly")
        else:
            # Fall back to historical volatility
            weekly_vol = historical_vol / np.sqrt(52)
            print(f"Using historical volatility for {ticker}: {historical_vol:.1%} annual, {weekly_vol:.1%} weekly")
        
        # Base prediction range (1 standard deviation)
        base_range = current_price * weekly_vol
        
        # Calculate bias based on technical indicators
        rsi = indicators.get('rsi', 50)
        macd = indicators.get('macd', 0)
        macd_signal = indicators.get('macd_signal', 0)
        momentum = indicators.get('momentum', 0)
        
        # Bias calculation
        bias_score = 0
        
        # RSI bias
        if rsi > 70:
            bias_score -= 0.2  # Overbought, bearish bias
        elif rsi < 30:
            bias_score += 0.2  # Oversold, bullish bias
        
        # MACD bias
        if macd > macd_signal:
            bias_score += 0.1  # Bullish momentum
        else:
            bias_score -= 0.1  # Bearish momentum
        
        # Momentum bias
        if momentum > 2:
            bias_score += 0.1
        elif momentum < -2:
            bias_score -= 0.1
        
        # Calculate predicted range
        lower_bound = current_price - base_range
        upper_bound = current_price + base_range
        
        # HYBRID MODEL: Bias-adjusted range center
        bias_adjustment = current_price * bias_score * 0.01
        
        # Shift the entire range based on bias
        lower_bound += bias_adjustment
        upper_bound += bias_adjustment
        
        # Target price is at center of adjusted range
        target_price = current_price + bias_adjustment
        
        # Probability of bullish move
        bullish_prob = 0.5 + (bias_score * 0.5)
        bullish_prob = max(0.1, min(0.9, bullish_prob))
        
        prediction = {
            'current_price': current_price,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'target_price': target_price,
            'bullish_probability': bullish_prob,
            'bias_score': bias_score,
            'weekly_volatility': weekly_vol,
            'iv_based': iv_data.get('valid', False) if iv_data else False
        }
        
        print(f"Price prediction for {ticker}:")
        print(f"Current: ${current_price:.2f}")
        print(f"Target: ${target_price:.2f}")
        print(f"Range: ${lower_bound:.2f} to ${upper_bound:.2f}")
        print(f"Bias score: {bias_score:.2f}")
        print(f"Bullish probability: {bullish_prob:.1%}")
        
        return prediction
        
    except Exception as e:
        print(f"Error predicting price for {ticker}: {e}")
        return {}

# Test the hybrid model with a popular ticker
print("Testing hybrid target zone model with AAPL")
prediction = predict_price_range("AAPL")
