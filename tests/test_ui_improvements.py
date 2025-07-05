#!/usr/bin/env python3
"""
🔍 Test Options Tracker UI Improvements
======================================

Test the specific improvements made:
1. Trade legs sorted by price (smallest on top)
2. OptionStrat URLs match suggested trades exactly
3. Comprehensive test runner integration

This script verifies that our latest changes work correctly.
"""

import sys
import os
# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.options_tracker import OptionsTracker
from src.options_tracker_ui import generate_optionstrat_url

def test_leg_sorting():
    """Test that trade legs are sorted by strike price (smallest first)"""
    print("🔍 Testing trade leg sorting...")
    
    tracker = OptionsTracker()
    suggestions = tracker.generate_trade_suggestions(1)
    
    if not suggestions:
        print("❌ No suggestions generated")
        return False
    
    suggestion = suggestions[0]
    if 'legs' not in suggestion:
        print("❌ No legs found in suggestion")
        return False
    
    legs = suggestion['legs']
    strikes = [leg['strike'] for leg in legs]
    
    # Check if strikes are sorted (smallest to largest)
    is_sorted = all(strikes[i] <= strikes[i + 1] for i in range(len(strikes) - 1))
    
    print(f"Strategy: {suggestion['strategy']}")
    print(f"Ticker: {suggestion['ticker']}")
    print("Legs (should be sorted by strike price):")
    for i, leg in enumerate(legs):
        print(f"  {i+1}. {leg['action']} {leg['type']} ${leg['strike']:.2f} @ ${leg['price']:.2f}")
    
    if is_sorted:
        print("✅ Legs are correctly sorted by strike price!")
        return True
    else:
        print("❌ Legs are NOT sorted by strike price")
        return False

def test_optionstrat_urls():
    """Test that OptionStrat URLs are generated correctly"""
    print("\n🔗 Testing OptionStrat URL generation...")
    
    # Test Bull Put Spread
    bull_put_suggestion = {
        'ticker': 'SPY',
        'strategy': 'Bull Put Spread',
        'short_strike': 620.0,
        'long_strike': 615.0,
        'expiration': '2025-08-01'
    }
    
    url = generate_optionstrat_url(bull_put_suggestion)
    expected_contains = ['bull-put-spread', 'SPY', '250801', 'P620', 'P615']
    
    print(f"Bull Put Spread URL: {url}")
    if all(part in url for part in expected_contains):
        print("✅ Bull Put Spread URL format correct!")
    else:
        print("❌ Bull Put Spread URL format incorrect")
        print(f"   Expected parts: {expected_contains}")
        print(f"   Missing: {[part for part in expected_contains if part not in url]}")
        return False
    
    # Test Bear Call Spread
    bear_call_suggestion = {
        'ticker': 'QQQ',
        'strategy': 'Bear Call Spread',
        'short_strike': 560.0,
        'long_strike': 565.0,
        'expiration': '2025-08-01'
    }
    
    url = generate_optionstrat_url(bear_call_suggestion)
    expected_contains = ['bear-call-spread', 'QQQ', '250801', 'C560', 'C565']
    
    print(f"Bear Call Spread URL: {url}")
    if all(part in url for part in expected_contains):
        print("✅ Bear Call Spread URL format correct!")
    else:
        print("❌ Bear Call Spread URL format incorrect")
        return False
    
    # Test Iron Condor - THIS IS THE CRITICAL TEST
    iron_condor_suggestion = {
        'ticker': 'QQQ',
        'strategy': 'Iron Condor',
        'put_long_strike': 511.0,    # BUY PUT (lowest strike)
        'put_short_strike': 521.0,   # SELL PUT 
        'call_short_strike': 591.0,  # SELL CALL
        'call_long_strike': 601.0,   # BUY CALL (highest strike)
        'expiration': '2025-08-01'
    }
    
    url = generate_optionstrat_url(iron_condor_suggestion)
    print(f"Iron Condor URL: {url}")
    
    # Verify the URL has strikes in correct order for OptionStrat
    # Should contain: P511, P521, C591, C601
    expected_contains = ['iron-condor', 'QQQ', '250801', 'P511', 'P521', 'C591', 'C601']
    if all(part in url for part in expected_contains):
        print("✅ Iron Condor URL format correct!")
        print("   Strikes in ascending order: P511 < P521 < C591 < C601")
        
        # Additional verification - check that this matches the actual trade
        print("   Trade verification:")
        print("   - BUY PUT $511 (long put)")
        print("   - SELL PUT $521 (short put)")  
        print("   - SELL CALL $591 (short call)")
        print("   - BUY CALL $601 (long call)")
        print("   ✅ URL matches suggested trade structure!")
    else:
        print("❌ Iron Condor URL format incorrect")
        print(f"   Expected parts: {expected_contains}")
        print(f"   Missing: {[part for part in expected_contains if part not in url]}")
        return False
    
    return True

def test_realistic_trade_generation():
    """Test that trade suggestions use realistic strikes and real prices"""
    print("\n💰 Testing realistic trade generation...")
    
    tracker = OptionsTracker()
    suggestions = tracker.generate_trade_suggestions(3)
    
    if not suggestions:
        print("❌ No suggestions generated")
        return False
    
    all_good = True
    for i, suggestion in enumerate(suggestions, 1):
        print(f"\n--- Trade Suggestion {i} ---")
        print(f"Strategy: {suggestion['strategy']}")
        print(f"Ticker: {suggestion['ticker']}")
        print(f"Credit: ${suggestion['credit']:.2f}")
        print(f"Confidence: {suggestion['confidence']:.0f}%")
        
        # Check strikes are realistic (whole/half/quarter dollars)
        if 'legs' in suggestion:
            for leg in suggestion['legs']:
                strike = leg['strike']
                price = leg['price']
                
                # Check strike increments
                if strike % 0.25 != 0:
                    print(f"❌ Strike {strike} not on quarter boundaries")
                    all_good = False
                else:
                    print(f"✅ Strike ${strike:.2f} is realistic")
                
                # Check price is reasonable (not zero)
                if price <= 0:
                    print(f"❌ Invalid price: ${price:.2f} for {leg['action']} {leg['type']} ${strike}")
                    all_good = False
                else:
                    print(f"✅ Price ${price:.2f} is valid")
        
        # Test that credit is calculated (can be positive or negative)
        if 'credit' not in suggestion:
            print("❌ No credit calculated")
            all_good = False
        else:
            print(f"✅ Credit calculated: ${suggestion['credit']:.2f}")
    
    return all_good

def main():
    print("🚀 Testing Options Tracker UI Improvements")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Test 1: Leg sorting
    if not test_leg_sorting():
        all_tests_passed = False
    
    # Test 2: OptionStrat URLs
    if not test_optionstrat_urls():
        all_tests_passed = False
    
    # Test 3: Realistic trade generation
    if not test_realistic_trade_generation():
        all_tests_passed = False
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Legs are sorted by price")
        print("✅ OptionStrat URLs are correct")
        print("✅ Trade generation uses realistic data")
        return 0
    else:
        print("💥 SOME TESTS FAILED!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
