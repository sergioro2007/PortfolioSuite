#!/usr/bin/env python3
import sys
sys.path.insert(0, 'src')

from portfolio_suite.options_trading.core import OptionsTracker

print("Testing enhanced prediction...")
t = OptionsTracker()

# Test prediction directly
print("Testing prediction for SPY...")
prediction = t.predict_price_range_enhanced('SPY')
print(f"Prediction result: {prediction}")

print("\nTesting _create_trade_suggestion...")
suggestion = t._create_trade_suggestion('SPY', 623.62, {
    'target_price': 630.0,
    'lower_bound': 615.0,
    'upper_bound': 635.0,
    'confidence': 0.7
})
print(f"Suggestion result: {suggestion}")
