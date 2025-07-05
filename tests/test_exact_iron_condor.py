#!/usr/bin/env python3
"""
Test the exact Iron Condor case that's showing the wrong URL
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.options_tracker_ui import generate_optionstrat_url

def test_exact_case():
    """Test the exact Iron Condor case"""
    print("🧪 Testing exact Iron Condor URL generation...")
    
    # Create a mock suggestion that matches what you're seeing
    suggestion = {
        'strategy': 'Iron Condor',
        'ticker': 'QQQ',
        'put_long_strike': 546,
        'put_short_strike': 551,
        'call_short_strike': 561,
        'call_long_strike': 565,
        'expiration': '2025-08-01'
    }
    
    print(f"📊 Mock suggestion:")
    print(f"  Strategy: {suggestion['strategy']}")
    print(f"  Ticker: {suggestion['ticker']}")
    print(f"  Put Long: {suggestion['put_long_strike']}")
    print(f"  Put Short: {suggestion['put_short_strike']}")
    print(f"  Call Short: {suggestion['call_short_strike']}")
    print(f"  Call Long: {suggestion['call_long_strike']}")
    print(f"  Expiration: {suggestion['expiration']}")
    
    # Generate URL
    url = generate_optionstrat_url(suggestion)
    print(f"\n🔗 Generated URL:")
    print(url)
    
    # Expected URL
    expected = "https://optionstrat.com/build/iron-condor/QQQ/20250801/546p/551p/561c/565c"
    print(f"\n✅ Expected URL:")
    print(expected)
    
    if url == expected:
        print("\n✅ URL matches expected format!")
    else:
        print("\n❌ URL does not match!")
        print("Difference found")

if __name__ == "__main__":
    test_exact_case()
