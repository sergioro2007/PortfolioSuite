#!/usr/bin/env python3
"""
Debug the OptionStrat URL generation to see what's happening
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.options_tracker import OptionsTracker
from src.options_tracker_ui import generate_optionstrat_url

def debug_url_generation():
    """Debug URL generation for Iron Condor"""
    print("🔍 Debugging OptionStrat URL generation...")
    
    tracker = OptionsTracker()
    suggestions = tracker.generate_trade_suggestions(1)
    
    if suggestions:
        suggestion = suggestions[0]
        print(f"📊 Strategy: {suggestion['strategy']}")
        print(f"📈 Ticker: {suggestion['ticker']}")
        
        if suggestion['strategy'] == 'Iron Condor':
            print(f"\n🎯 Iron Condor strikes:")
            print(f"  Put Long: {suggestion.get('put_long_strike', 'MISSING')}")
            print(f"  Put Short: {suggestion.get('put_short_strike', 'MISSING')}")
            print(f"  Call Short: {suggestion.get('call_short_strike', 'MISSING')}")
            print(f"  Call Long: {suggestion.get('call_long_strike', 'MISSING')}")
            print(f"  Expiration: {suggestion.get('expiration', 'MISSING')}")
            
            # Generate URL
            url = generate_optionstrat_url(suggestion)
            print(f"\n🔗 Generated URL:")
            print(url)
            
            # Check if it matches expected format
            expected_format = "iron-condor/{ticker}/{exp}/{put_long}p/{put_short}p/{call_short}c/{call_long}c"
            print(f"\n✅ Expected format: {expected_format}")
            
            # Check legs
            if 'legs' in suggestion:
                print(f"\n📋 Legs data:")
                for leg in suggestion['legs']:
                    print(f"  {leg['action']} {leg['type']} ${leg['strike']:.2f}")
        else:
            print(f"⚠️  Strategy is {suggestion['strategy']}, not Iron Condor")
            
            # Still generate URL to see what happens
            url = generate_optionstrat_url(suggestion)
            print(f"\n🔗 Generated URL: {url}")
    else:
        print("❌ No suggestions generated")

if __name__ == "__main__":
    debug_url_generation()
