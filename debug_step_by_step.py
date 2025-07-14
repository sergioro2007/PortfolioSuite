#!/usr/bin/env python3
import sys
sys.path.insert(0, 'src')

from portfolio_suite.options_trading.core import OptionsTracker
import yfinance as yf

print("Testing suggestions step by step...")
t = OptionsTracker()

# Test the whole process step by step for SPY
ticker = 'SPY'
print(f"\n1. Testing {ticker}...")

try:
    stock = yf.Ticker(ticker)
    hist_data = stock.history(period="2d")
    print(f"   History data: {not hist_data.empty}")
    
    if not hist_data.empty:
        current_price = hist_data["Close"].iloc[-1]
        print(f"   Current price: {current_price}")
        
        prediction = t.predict_price_range_enhanced(ticker)
        print(f"   Prediction exists: {prediction is not None}")
        print(f"   Target price exists: {prediction.get('target_price') if prediction else 'None'}")
        
        if prediction and prediction.get('target_price') is not None:
            suggestion = t._create_trade_suggestion(ticker, current_price, prediction)
            print(f"   Suggestion created: {suggestion is not None}")
            if suggestion:
                print(f"   Suggestion: {suggestion['strategy']} - ${suggestion['expected_profit']}")
        else:
            print("   Creating fallback prediction...")
            fallback_prediction = {
                'target_price': current_price * 1.01,
                'lower_bound': current_price * 0.97,
                'upper_bound': current_price * 1.05,
                'confidence': 0.6
            }
            suggestion = t._create_trade_suggestion(ticker, current_price, fallback_prediction)
            print(f"   Fallback suggestion: {suggestion is not None}")
            
except Exception as e:
    print(f"   Error: {e}")

print("\n2. Now testing full method...")
suggestions = t.generate_trade_suggestions(1)
print(f"   Full method returned: {len(suggestions)} suggestions")
