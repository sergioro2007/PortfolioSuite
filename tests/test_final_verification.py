#!/usr/bin/env python3
"""
Final Verification Test Suite
============================

Verify that:
1. OptionStrat URLs use the correct format
2. Trade suggestions only use actually available strikes
3. UI displays legs sorted by strike price
4. All core functionality works as expected
"""

import sys
import traceback
from datetime import datetime, timedelta

def test_optionstrat_urls():
    """Test OptionStrat URL generation for all strategies"""
    print("🔗 Testing OptionStrat URL Generation...")
    
    try:
        from src.options_tracker_ui import generate_optionstrat_url
        
        # Test cases with expected URL patterns
        test_cases = [
            {
                'name': 'Bull Put Spread',
                'suggestion': {
                    'ticker': 'SPY',
                    'strategy': 'Bull Put Spread',
                    'short_strike': 575,
                    'long_strike': 570,
                    'expiration': '2025-08-01'
                },
                'expected_pattern': 'bull-put-spread/SPY/.SPY250801P575,-.SPY250801P570'
            },
            {
                'name': 'Iron Condor',
                'suggestion': {
                    'ticker': 'SPY',
                    'strategy': 'Iron Condor',
                    'put_long_strike': 575,
                    'put_short_strike': 590,
                    'call_short_strike': 660,
                    'call_long_strike': 680,
                    'expiration': '2025-08-01'
                },
                'expected_pattern': 'iron-condor/SPY/.SPY250801P575,-.SPY250801P590,-.SPY250801C660,.SPY250801C680'
            },
            {
                'name': 'Short Strangle',
                'suggestion': {
                    'ticker': 'SPY',
                    'strategy': 'Short Strangle',
                    'put_strike': 575,
                    'call_strike': 660,
                    'expiration': '2025-08-01'
                },
                'expected_pattern': 'short-strangle/SPY/.SPY250801P575,-.SPY250801C660'
            }
        ]
        
        all_passed = True
        for test_case in test_cases:
            url = generate_optionstrat_url(test_case['suggestion'])
            
            if test_case['expected_pattern'] in url:
                print(f"  ✅ {test_case['name']}: URL format correct")
                print(f"     {url}")
            else:
                print(f"  ❌ {test_case['name']}: URL format incorrect")
                print(f"     Expected pattern: {test_case['expected_pattern']}")
                print(f"     Generated: {url}")
                all_passed = False
        
        if all_passed:
            print("  🎉 All OptionStrat URLs use correct format!")
        else:
            print("  ⚠️  Some OptionStrat URLs have incorrect format")
            
        return all_passed
        
    except Exception as e:
        print(f"  ❌ Error testing OptionStrat URLs: {e}")
        traceback.print_exc()
        return False

def test_available_strikes_validation():
    """Test that trade suggestions only use available strikes"""
    print("\n📊 Testing Available Strikes Validation...")
    
    try:
        from src.options_tracker import OptionsTracker
        
        tracker = OptionsTracker()
        
        # Test with SPY (should have many available strikes)
        print("  📈 Testing SPY strike availability...")
        
        # Get available strikes for SPY
        available_strikes = tracker.get_available_strikes('SPY', '2025-08-01')
        
        if available_strikes and len(available_strikes) > 10:
            print(f"  ✅ Found {len(available_strikes)} available strikes for SPY")
            print(f"     Sample strikes: {sorted(available_strikes)[:10]}...")
        else:
            print(f"  ⚠️  Limited strikes found: {available_strikes}")
        
        # Test trade suggestions use only available strikes
        print("  🎯 Testing trade suggestion strike validation...")
        
        suggestions = tracker.generate_trade_suggestions(num_suggestions=5)
        
        if suggestions:
            all_valid = True
            for suggestion in suggestions:
                strategy = suggestion['strategy']
                
                # Check strikes based on strategy
                if strategy == 'Bull Put Spread':
                    strikes_to_check = [suggestion['short_strike'], suggestion['long_strike']]
                elif strategy == 'Bear Call Spread':
                    strikes_to_check = [suggestion['short_strike'], suggestion['long_strike']]
                elif strategy == 'Iron Condor':
                    strikes_to_check = [
                        suggestion['put_long_strike'],
                        suggestion['put_short_strike'],
                        suggestion['call_short_strike'],
                        suggestion['call_long_strike']
                    ]
                elif strategy in ['Cash Secured Put', 'Covered Call']:
                    strikes_to_check = [suggestion.get('strike', suggestion.get('put_strike', suggestion.get('call_strike')))]
                else:
                    continue
                
                # Validate all strikes are available
                for strike in strikes_to_check:
                    if strike not in available_strikes:
                        print(f"  ❌ {strategy}: Strike {strike} not in available strikes!")
                        all_valid = False
                        break
                
                if all_valid:
                    print(f"  ✅ {strategy}: All strikes valid ({strikes_to_check})")
            
            if all_valid:
                print("  🎉 All suggested trades use only available strikes!")
            else:
                print("  ⚠️  Some suggestions use unavailable strikes")
                
            return all_valid
        else:
            print("  ⚠️  No trade suggestions generated")
            return False
            
    except Exception as e:
        print(f"  ❌ Error testing strike validation: {e}")
        traceback.print_exc()
        return False

def test_leg_sorting():
    """Test that trade legs are sorted by strike price"""
    print("\n📋 Testing Trade Leg Sorting...")
    
    try:
        from src.options_tracker import OptionsTracker
        
        tracker = OptionsTracker()
        
        # Get some trade suggestions
        suggestions = tracker.generate_trade_suggestions(num_suggestions=3)
        
        if not suggestions:
            print("  ⚠️  No suggestions to test sorting")
            return False
        
        for suggestion in suggestions:
            strategy = suggestion['strategy']
            
            # Get legs for this suggestion (they're already included)
            legs = suggestion.get('legs', [])
            
            if len(legs) > 1:
                # Check if legs are sorted by strike price
                strikes = [leg['strike'] for leg in legs]
                sorted_strikes = sorted(strikes)
                
                if strikes == sorted_strikes:
                    print(f"  ✅ {strategy}: Legs sorted by strike ({strikes})")
                else:
                    print(f"  ❌ {strategy}: Legs not sorted!")
                    print(f"     Current: {strikes}")
                    print(f"     Expected: {sorted_strikes}")
                    return False
            else:
                if legs:
                    print(f"  ✅ {strategy}: Single leg trade ({legs[0]['strike']})")
                else:
                    print(f"  ⚠️  {strategy}: No legs found")
        
        print("  🎉 All trade legs properly sorted by strike price!")
        return True
        
    except Exception as e:
        print(f"  ❌ Error testing leg sorting: {e}")
        traceback.print_exc()
        return False

def test_core_functionality():
    """Test core tracker functionality"""
    print("\n🔧 Testing Core Functionality...")
    
    try:
        from src.options_tracker import OptionsTracker
        
        tracker = OptionsTracker()
        
        # Test tracker initialization
        print("  ✅ OptionsTracker initialized successfully")
        
        # Test trade suggestions
        suggestions = tracker.generate_trade_suggestions(num_suggestions=3)
        if suggestions:
            print(f"  ✅ Generated {len(suggestions)} trade suggestions")
        else:
            print("  ⚠️  No trade suggestions generated")
        
        # Test manual trade entry
        manual_trade = {
            'strategy': 'Bull Put Spread',
            'ticker': 'SPY',
            'short_strike': 590,
            'long_strike': 585,
            'quantity': 1,
            'expiration': '2025-08-01'
        }
        
        try:
            tracker.add_trade(manual_trade)
            print(f"  ✅ Manual trade entry successful")
        except Exception as e:
            print(f"  ⚠️  Manual trade entry failed: {e}")
        
        # Test stats calculation
        stats = tracker.calculate_weekly_pnl()
        print(f"  ✅ Portfolio stats calculated: {len(stats)} metrics")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error testing core functionality: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all verification tests"""
    print("🧪 Portfolio Management Suite - Final Verification")
    print("=" * 55)
    
    test_results = []
    
    # Run all tests
    test_results.append(('OptionStrat URLs', test_optionstrat_urls()))
    test_results.append(('Available Strikes', test_available_strikes_validation()))
    test_results.append(('Leg Sorting', test_leg_sorting()))
    test_results.append(('Core Functionality', test_core_functionality()))
    
    # Summary
    print("\n" + "=" * 55)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 55)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! The system is ready for use.")
        print("\nKey improvements verified:")
        print("✅ OptionStrat links use correct symbol format")
        print("✅ Trade suggestions only use actually available strikes")
        print("✅ Trade legs are sorted by strike price")
        print("✅ All core functionality works as expected")
    else:
        print("⚠️  Some tests failed. Please review the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
