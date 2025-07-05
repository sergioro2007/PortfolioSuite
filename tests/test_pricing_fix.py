#!/usr/bin/env python3
"""
Test if the option pricing fix works for NVDA 172.5 call
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.options_tracker import OptionsTracker

def test_nvda_172_5_pricing():
    """Test that NVDA 172.5 call pricing now works correctly"""
    
    print("🧪 Testing NVDA 172.5 CALL Option Pricing Fix")
    print("=" * 50)
    
    # Initialize tracker
    tracker = OptionsTracker()
    
    # Test the specific case
    ticker = "NVDA"
    strikes = [172.5]
    expiration = "2025-08-01"
    option_type = "call"
    
    print(f"📊 Testing {ticker} {strikes[0]} {option_type.upper()} for {expiration}")
    
    # Get option prices using our fixed function
    result = tracker.get_option_prices(ticker, strikes, expiration, option_type)
    
    print(f"🔍 Raw result: {result}")
    
    # Check if we got real data (not fallback)
    expected_key = f"CALL_{strikes[0]:g}"  # Should be "CALL_172.5"
    
    if expected_key in result:
        price = result[expected_key]
        print(f"✅ Found price for {expected_key}: ${price:.2f}")
        
        if price > 1.0:
            print(f"🎯 SUCCESS! Price ${price:.2f} is realistic (expected ~$1.70-$1.80)")
            return True
        else:
            print(f"⚠️ Price ${price:.2f} seems low (expected ~$1.70-$1.80)")
            return False
    else:
        print(f"❌ Key '{expected_key}' not found in result")
        print(f"Available keys: {list(result.keys())}")
        return False

if __name__ == "__main__":
    test_nvda_172_5_pricing()
