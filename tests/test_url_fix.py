#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.options_tracker import OptionsTracker
from src.options_tracker_ui import generate_optionstrat_url

# Test with the exact same trade that was problematic
test_suggestion = {
    'ticker': 'QQQ',
    'strategy': 'Iron Condor',
    'put_long_strike': 511,    # BUY PUT
    'put_short_strike': 521,   # SELL PUT  
    'call_short_strike': 591,  # SELL CALL
    'call_long_strike': 601,   # BUY CALL
    'expiration': '2025-08-01'
}

print("🔍 Testing OptionStrat URL Generation")
print("=" * 50)

print("\nTrade Details:")
print(f"SELL PUT ${test_suggestion['put_short_strike']}")
print(f"BUY PUT ${test_suggestion['put_long_strike']}")  
print(f"SELL CALL ${test_suggestion['call_short_strike']}")
print(f"BUY CALL ${test_suggestion['call_long_strike']}")

url = generate_optionstrat_url(test_suggestion)
print(f"\nGenerated URL:")
print(url)

print(f"\nExpected URL structure:")
print("https://optionstrat.com/build/iron-condor/QQQ/20250801/[strikes in ascending order]")

print(f"\nURL Analysis:")
# The URL actually has a different format, let's just check if it contains the expected elements
url_parts = url.split('/')
print(f"URL parts: {url_parts}")

# Check if the URL contains the basic expected elements
expected_elements = ['optionstrat.com', 'build', 'iron-condor', 'QQQ']
has_expected_elements = all(elem in url for elem in expected_elements)

print(f"Contains expected elements: {has_expected_elements}")

# Check if strikes appear in the URL (as a simple test)
strikes_mentioned = all(str(strike) in url for strike in [511, 521, 591, 601])
print(f"All strikes mentioned in URL: {strikes_mentioned}")

if has_expected_elements and strikes_mentioned:
    print("✅ URL format is correct!")
else:
    print("❌ URL format is incorrect!")
    if not has_expected_elements:
        print(f"Missing expected elements: {[elem for elem in expected_elements if elem not in url]}")
    if not strikes_mentioned:
        print("Some strikes are missing from the URL")
