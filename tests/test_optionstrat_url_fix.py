#!/usr/bin/env python3
"""
Test the updated OptionStrat URL generation
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.options_tracker_ui import generate_optionstrat_url

def test_updated_url_generation():
    """Test the updated URL format"""
    print("🧪 Testing updated OptionStrat URL generation...")
    
    # Test Iron Condor with SPY strikes matching your working example
    suggestion = {
        'strategy': 'Iron Condor',
        'ticker': 'SPY',
        'put_long_strike': 575,
        'put_short_strike': 590,
        'call_short_strike': 660,
        'call_long_strike': 680,
        'expiration': '2025-08-01'
    }
    
    print(f"📊 Mock suggestion:")
    print(f"  Strategy: {suggestion['strategy']}")
    print(f"  Ticker: {suggestion['ticker']}")
    print(f"  Strikes: {suggestion['put_long_strike']}/{suggestion['put_short_strike']}/{suggestion['call_short_strike']}/{suggestion['call_long_strike']}")
    print(f"  Expiration: {suggestion['expiration']}")
    
    # Generate URL
    url = generate_optionstrat_url(suggestion)
    print(f"\n🔗 Generated URL:")
    print(url)
    
    # Your working example
    expected = "https://optionstrat.com/build/iron-condor/SPY/.SPY250801P575,-.SPY250801P590,-.SPY250801C660,.SPY250801C680"
    print(f"\n✅ Your working URL:")
    print(expected)
    
    if url == expected:
        print("\n✅ URL matches perfectly!")
    else:
        print("\n❌ URLs don't match!")
        print("Checking differences...")
        
        # Compare parts
        if url.split('/')[:-1] == expected.split('/')[:-1]:
            print("   Base URL parts match, checking symbols...")
            url_symbols = url.split('/')[-1]
            expected_symbols = expected.split('/')[-1]
            print(f"   Generated symbols: {url_symbols}")
            print(f"   Expected symbols:  {expected_symbols}")
        else:
            print("   Base URL structure differs")

if __name__ == "__main__":
    test_updated_url_generation()
