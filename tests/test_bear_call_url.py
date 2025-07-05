#!/usr/bin/env python3
"""
Test Bear Call Spread URL Generation Fix
========================================

Test the specific Bear Call Spread example from the user
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.options_tracker_ui import generate_optionstrat_url

def test_bear_call_spread():
    """Test the specific Bear Call Spread example"""
    print("🧪 Testing Bear Call Spread URL Generation Fix...")
    
    # User's example:
    # SELL CALL $660.00 $0.50
    # BUY  CALL $680.00 $0.08
    bear_call = {
        'strategy': 'Bear Call Spread',
        'ticker': 'SPY',
        'short_strike': 660.0,  # SELL
        'long_strike': 680.0,   # BUY
        'expiration': '2025-08-01'
    }
    
    print(f"📊 Bear Call Spread:")
    print(f"  SELL CALL ${bear_call['short_strike']:.2f}")
    print(f"  BUY  CALL ${bear_call['long_strike']:.2f}")
    
    # Generate URL
    url = generate_optionstrat_url(bear_call)
    print(f"\n🔗 Generated URL:")
    print(url)
    
    # User said the corrected URL should be:
    expected = "https://optionstrat.com/build/bear-call-spread/SPY/-.SPY250801C660,.SPY250801C680"
    print(f"\n✅ Expected URL (with SELL indicated by minus):")
    print(expected)
    
    if url == expected:
        print("\n🎉 URL generation fixed! SELL action correctly indicated with minus sign.")
        return True
    else:
        print("\n❌ URLs don't match!")
        print("Generated:", url)
        print("Expected: ", expected)
        return False

if __name__ == "__main__":
    success = test_bear_call_spread()
    if success:
        print("\n✅ Bear Call Spread URL fix verified!")
    else:
        print("\n❌ Fix not working properly")
    sys.exit(0 if success else 1)
