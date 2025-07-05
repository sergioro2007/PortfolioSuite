#!/usr/bin/env python3
"""
OptionStrat URL Generation Test
==============================

Test to verify that OptionStrat URLs are generated correctly, including proper handling
of half-dollar strikes like 172.50, which should appear as 172.5 in the URL.
"""

import sys
import os
import traceback
# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_optionstrat_url_generation():
    """Test OptionStrat URL generation for all strategies with various strike formats"""
    print("🔗 Testing OptionStrat URL Generation...")
    
    try:
        from src.options_tracker_ui import generate_optionstrat_url
        
        # Test cases with different strike formats including half-dollars
        test_cases = [
            {
                'name': 'NVDA Iron Condor - User Example (146/150/170/172.5)',
                'suggestion': {
                    'ticker': 'NVDA',
                    'strategy': 'Iron Condor',
                    'put_long_strike': 146.0,
                    'put_short_strike': 150.0,
                    'call_short_strike': 170.0,
                    'call_long_strike': 172.5,  # Half-dollar strike from user example
                    'expiration': '2025-08-01'
                },
                'expected_url': 'https://optionstrat.com/build/iron-condor/NVDA/.NVDA250801P146,-.NVDA250801P150,-.NVDA250801C170,.NVDA250801C172.5'
            },
            {
                'name': 'Iron Condor with Half-Dollar Strike',
                'suggestion': {
                    'ticker': 'NVDA',
                    'strategy': 'Iron Condor',
                    'put_long_strike': 146.0,
                    'put_short_strike': 150.0,
                    'call_short_strike': 170.0,
                    'call_long_strike': 172.5,  # Half-dollar strike
                    'expiration': '2025-08-01'
                },
                'expected_url': 'https://optionstrat.com/build/iron-condor/NVDA/.NVDA250801P146,-.NVDA250801P150,-.NVDA250801C170,.NVDA250801C172.5'
            },
            {
                'name': 'Bull Put Spread with Half-Dollar Strike',
                'suggestion': {
                    'ticker': 'AAPL',
                    'strategy': 'Bull Put Spread',
                    'short_strike': 217.5,  # Half-dollar strike (SELL - gets minus)
                    'long_strike': 215.0,   # BUY - no minus
                    'expiration': '2025-08-01'
                },
                'expected_url': 'https://optionstrat.com/build/bull-put-spread/AAPL/-.AAPL250801P217.5,.AAPL250801P215'
            },
            {
                'name': 'Bear Call Spread with Half-Dollar Strike',
                'suggestion': {
                    'ticker': 'QQQ',
                    'strategy': 'Bear Call Spread',
                    'short_strike': 572.5,  # Half-dollar strike (SELL - gets minus)
                    'long_strike': 575.0,   # BUY - no minus
                    'expiration': '2025-08-01'
                },
                'expected_url': 'https://optionstrat.com/build/bear-call-spread/QQQ/-.QQQ250801C572.5,.QQQ250801C575'
            },
            {
                'name': 'Short Strangle with Half-Dollar Strikes',
                'suggestion': {
                    'ticker': 'SPY',
                    'strategy': 'Short Strangle',
                    'put_strike': 617.5,  # Half-dollar strike
                    'call_strike': 632.5,  # Half-dollar strike
                    'expiration': '2025-08-01'
                },
                'expected_url': 'https://optionstrat.com/build/short-strangle/SPY/.SPY250801P617.5,-.SPY250801C632.5'
            },
            {
                'name': 'Cash Secured Put with Quarter-Dollar Strike',
                'suggestion': {
                    'ticker': 'NVDA',
                    'strategy': 'Cash Secured Put',
                    'strike': 157.25,  # Quarter-dollar strike
                    'expiration': '2025-08-01'
                },
                'expected_url': 'https://optionstrat.com/build/cash-secured-put/NVDA/.NVDA250801P157.25'
            },
            {
                'name': 'Covered Call with Quarter-Dollar Strike',
                'suggestion': {
                    'ticker': 'NVDA',
                    'strategy': 'Covered Call',
                    'strike': 172.75,  # Quarter-dollar strike
                    'expiration': '2025-08-01'
                },
                'expected_url': 'https://optionstrat.com/build/covered-call/NVDA/-.NVDA250801C172.75'
            }
        ]
        
        all_passed = True
        for test_case in test_cases:
            generated_url = generate_optionstrat_url(test_case['suggestion'])
            expected_url = test_case['expected_url']
            
            if generated_url == expected_url:
                print(f"  ✅ {test_case['name']}: URL correct")
                print(f"     {generated_url}")
            else:
                print(f"  ❌ {test_case['name']}: URL incorrect")
                print(f"     Expected: {expected_url}")
                print(f"     Generated: {generated_url}")
                all_passed = False
            print()
        
        if all_passed:
            print("  🎉 All OptionStrat URLs generated correctly!")
        else:
            print("  ⚠️  Some OptionStrat URLs have incorrect format")
            
        return all_passed
        
    except Exception as e:
        print(f"  ❌ Error testing OptionStrat URLs: {e}")
        traceback.print_exc()
        return False

def test_real_nvda_suggestion():
    """Test the specific NVDA suggestion that was failing"""
    print("\n🎯 Testing Real NVDA Suggestion...")
    
    try:
        from src.options_tracker_ui import generate_optionstrat_url
        
        # The exact suggestion that was failing
        nvda_suggestion = {
            'ticker': 'NVDA',
            'strategy': 'Iron Condor',
            'put_long_strike': 146.0,
            'put_short_strike': 150.0,
            'call_short_strike': 170.0,
            'call_long_strike': 172.5,  # This was becoming 172 instead of 172.5
            'expiration': '2025-08-01'
        }
        
        generated_url = generate_optionstrat_url(nvda_suggestion)
        expected_url = 'https://optionstrat.com/build/iron-condor/NVDA/.NVDA250801P146,-.NVDA250801P150,-.NVDA250801C170,.NVDA250801C172.5'
        
        print(f"  Legs: BUY PUT $146, SELL PUT $150, SELL CALL $170, BUY CALL $172.5")
        print(f"  Generated: {generated_url}")
        print(f"  Expected:  {expected_url}")
        
        if generated_url == expected_url:
            print("  ✅ NVDA Iron Condor URL is now correct!")
            return True
        else:
            print("  ❌ NVDA Iron Condor URL is still incorrect")
            
            # Show the specific differences
            if '172.5' not in generated_url:
                print("  🔍 Issue: 172.5 strike not preserved in URL")
            if '.NVDA250801C172.5' not in generated_url:
                print("  🔍 Issue: Call leg symbol incorrect")
                
            return False
        
    except Exception as e:
        print(f"  ❌ Error testing NVDA suggestion: {e}")
        traceback.print_exc()
        return False

def test_strike_formatting():
    """Test various strike price formatting scenarios"""
    print("\n📊 Testing Strike Price Formatting...")
    
    try:
        # Test the formatting directly
        test_strikes = [
            (146.0, "146"),
            (150.0, "150"), 
            (170.0, "170"),
            (172.5, "172.5"),
            (157.25, "157.25"),
            (100.75, "100.75"),
            (50.5, "50.5"),
            (1000.0, "1000")
        ]
        
        all_correct = True
        for strike, expected in test_strikes:
            formatted = f"{strike:g}"
            if formatted == expected:
                print(f"  ✅ {strike} → {formatted}")
            else:
                print(f"  ❌ {strike} → {formatted} (expected {expected})")
                all_correct = False
        
        if all_correct:
            print("  🎉 All strike price formatting correct!")
        else:
            print("  ⚠️  Some strike price formatting incorrect")
            
        return all_correct
        
    except Exception as e:
        print(f"  ❌ Error testing strike formatting: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all OptionStrat URL generation tests"""
    print("🔗 OptionStrat URL Generation Test Suite")
    print("=" * 55)
    
    test_results = []
    
    # Run all tests
    test_results.append(('Strike Formatting', test_strike_formatting()))
    test_results.append(('OptionStrat URL Generation', test_optionstrat_url_generation()))
    test_results.append(('Real NVDA Suggestion', test_real_nvda_suggestion()))
    
    # Summary
    print("\n" + "=" * 55)
    print("📊 URL GENERATION TEST RESULTS")
    print("=" * 55)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} URL generation tests passed")
    
    if passed == total:
        print("🎉 ALL URL GENERATION TESTS PASSED!")
        print("\nURL generation verified:")
        print("✅ Half-dollar strikes (172.5) preserved correctly")
        print("✅ Quarter-dollar strikes (157.25) preserved correctly")
        print("✅ Whole-dollar strikes (170) formatted correctly")
        print("✅ All strategy types generate correct URLs")
    else:
        print("⚠️  Some URL generation tests failed. Review the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
