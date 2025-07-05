#!/usr/bin/env python3
"""
Final OptionStrat URL Verification
==================================

Test the fixed OptionStrat URLs with real suggestions
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.options_tracker import OptionsTracker
from src.options_tracker_ui import generate_optionstrat_url

def test_real_suggestions():
    """Test OptionStrat URLs with real trade suggestions"""
    print("🧪 Testing OptionStrat URLs with Real Suggestions")
    print("=" * 50)
    
    tracker = OptionsTracker()
    suggestions = tracker.generate_trade_suggestions(num_suggestions=3)
    
    for i, suggestion in enumerate(suggestions, 1):
        print(f"\n📊 Suggestion {i}: {suggestion['strategy']} - {suggestion['ticker']}")
        
        # Show the trade details
        print("  Trade Details:")
        for leg in suggestion['legs']:
            action = leg['action']
            option_type = leg['type']
            strike = leg['strike']
            price = leg['price']
            print(f"    {action} {option_type} ${strike:g} = ${price:.2f}")
        
        # Generate OptionStrat URL
        url = generate_optionstrat_url(suggestion)
        print(f"  🔗 OptionStrat URL:")
        print(f"    {url}")
        
        # Verify SELL actions have minus signs
        if 'SELL' in [leg['action'] for leg in suggestion['legs']]:
            has_minus = '-.' in url
            if has_minus:
                print(f"    ✅ SELL actions correctly indicated with minus signs")
            else:
                print(f"    ❌ SELL actions missing minus signs")
        
        print()

if __name__ == "__main__":
    test_real_suggestions()
