#!/usr/bin/env python3
import sys
sys.path.insert(0, 'src')

from portfolio_suite.options_trading.core import OptionsTracker

print("Testing suggestions...")
t = OptionsTracker()
s = t.generate_trade_suggestions(2)
print(f"Generated {len(s)} suggestions")

for x in s[:3]:
    print(f"- {x['ticker']}: {x['strategy']} (${x['expected_profit']} profit)")
    print(f"  Risk: ${x['risk']}, Confidence: {x['confidence']}")
