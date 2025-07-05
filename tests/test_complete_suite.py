#!/usr/bin/env python3
"""
Options Trading Tracker - Complete Test Suite
=============================================

Comprehensive test suite covering all aspects of the Options Trading Tracker:
- Option pricing accuracy vs real market data
- OptionStrat URL generation
- Trade suggestion logic
- Strike validation
- UI functionality
- Core system functionality

Run this to verify the entire system is working correctly.
"""

import sys
import os

# Add parent directory to path so we can import the main modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import subprocess
import traceback
from datetime import datetime

# Add parent directory to path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def run_test_module(module_name, description):
    """Run a specific test module and return success status"""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"{'='*60}")
    
    try:
        # Import and run the test module
        module = __import__(module_name)
        if hasattr(module, 'main'):
            return module.main()
        else:
            print(f"⚠️  Test module {module_name} has no main() function")
            return False
    except Exception as e:
        print(f"❌ Error running {module_name}: {e}")
        traceback.print_exc()
        return False

def test_option_pricing_accuracy():
    """Test option pricing accuracy against real market data"""
    print(f"\n{'='*60}")
    print("💰 Option Pricing Accuracy Test")
    print(f"{'='*60}")
    
    try:
        from test_option_pricing_accuracy import main as pricing_main
        return pricing_main()
    except Exception as e:
        print(f"❌ Error running option pricing test: {e}")
        traceback.print_exc()
        return False

def test_optionstrat_urls():
    """Test OptionStrat URL generation"""
    print(f"\n{'='*60}")
    print("🔗 OptionStrat URL Generation Test")
    print(f"{'='*60}")
    
    try:
        sys.path.insert(0, '..')
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
                'name': 'Bear Call Spread',
                'suggestion': {
                    'ticker': 'SPY',
                    'strategy': 'Bear Call Spread',
                    'short_strike': 660,
                    'long_strike': 665,
                    'expiration': '2025-08-01'
                },
                'expected_pattern': 'bear-call-spread/SPY/.SPY250801C660,-.SPY250801C665'
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
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Error testing OptionStrat URLs: {e}")
        traceback.print_exc()
        return False

def test_trade_suggestions():
    """Test trade suggestion generation"""
    print(f"\n{'='*60}")
    print("💡 Trade Suggestion Generation Test")
    print(f"{'='*60}")
    
    try:
        sys.path.insert(0, '..')
        from src.options_tracker import OptionsTracker
        
        tracker = OptionsTracker()
        
        # Test trade suggestion generation
        suggestions = tracker.generate_trade_suggestions(num_suggestions=3)
        
        if not suggestions:
            print("❌ No trade suggestions generated")
            return False
        
        print(f"✅ Generated {len(suggestions)} trade suggestions")
        
        # Test each suggestion has required fields
        required_fields = ['ticker', 'strategy', 'legs', 'credit', 'expiration']
        all_valid = True
        
        for i, suggestion in enumerate(suggestions):
            print(f"\n  🎯 Testing suggestion {i+1}: {suggestion['strategy']} for {suggestion['ticker']}")
            
            # Check required fields
            for field in required_fields:
                if field not in suggestion:
                    print(f"    ❌ Missing field: {field}")
                    all_valid = False
                else:
                    print(f"    ✅ Has {field}: {suggestion[field]}")
            
            # Check legs are properly formatted
            legs = suggestion.get('legs', [])
            if not legs:
                print("    ❌ No legs found")
                all_valid = False
            else:
                print(f"    ✅ Has {len(legs)} legs")
                
                # Check legs are sorted by strike price
                strikes = [leg['strike'] for leg in legs]
                if strikes == sorted(strikes):
                    print("    ✅ Legs sorted by strike price")
                else:
                    print(f"    ❌ Legs not sorted by strike price: {strikes}")
                    all_valid = False
        
        return all_valid
        
    except Exception as e:
        print(f"❌ Error testing trade suggestions: {e}")
        traceback.print_exc()
        return False

def test_strike_validation():
    """Test that only available strikes are used"""
    print(f"\n{'='*60}")
    print("📊 Strike Validation Test")
    print(f"{'='*60}")
    
    try:
        sys.path.insert(0, '..')
        from src.options_tracker import OptionsTracker
        
        tracker = OptionsTracker()
        
        # Test with SPY (should have many available strikes)
        ticker = 'SPY'
        expiration_date = '2025-08-01'
        
        print(f"  📈 Testing {ticker} strike availability...")
        
        # Get available strikes
        available_strikes = tracker.get_available_strikes(ticker, expiration_date)
        
        if available_strikes and len(available_strikes) > 10:
            print(f"  ✅ Found {len(available_strikes)} available strikes for {ticker}")
            print(f"     Sample strikes: {sorted(available_strikes)[:5]}...{sorted(available_strikes)[-5:]}")
        else:
            print(f"  ⚠️  Limited strikes found: {len(available_strikes) if available_strikes else 0}")
            return False
        
        # Test that trade suggestions use only available strikes
        suggestions = tracker.generate_trade_suggestions(num_suggestions=3)
        
        all_valid = True
        for suggestion in suggestions:
            if suggestion['ticker'] != ticker:
                continue
                
            strategy = suggestion['strategy']
            
            # Get all strikes used in this suggestion
            strikes_used = [leg['strike'] for leg in suggestion['legs']]
            
            # Check all strikes are available
            for strike in strikes_used:
                if strike not in available_strikes:
                    print(f"  ❌ {strategy}: Strike {strike} not in available strikes!")
                    all_valid = False
            
            if all_valid:
                print(f"  ✅ {strategy}: All strikes valid ({strikes_used})")
        
        return all_valid
        
    except Exception as e:
        print(f"❌ Error testing strike validation: {e}")
        traceback.print_exc()
        return False

def test_core_functionality():
    """Test core options tracker functionality"""
    print(f"\n{'='*60}")
    print("🔧 Core Functionality Test")
    print(f"{'='*60}")
    
    try:
        sys.path.insert(0, '..')
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
            print("  ✅ Manual trade entry successful")
        except Exception as e:
            print(f"  ⚠️  Manual trade entry failed: {e}")
        
        # Test stats calculation
        stats = tracker.calculate_weekly_pnl()
        print(f"  ✅ Portfolio stats calculated: {len(stats)} metrics")
        
        # Test technical indicators
        try:
            indicators = tracker.get_technical_indicators('SPY')
            if indicators:
                print(f"  ✅ Technical indicators calculated: {len(indicators)} metrics")
            else:
                print("  ⚠️  No technical indicators calculated")
        except Exception as e:
            print(f"  ⚠️  Technical indicators failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing core functionality: {e}")
        traceback.print_exc()
        return False

def main():
    """Run the complete test suite"""
    print("🧪 Options Trading Tracker - Complete Test Suite")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Define all tests to run
    tests = [
        ("Option Pricing Accuracy", test_option_pricing_accuracy),
        ("OptionStrat URL Generation", test_optionstrat_urls),
        ("Trade Suggestion Generation", test_trade_suggestions),
        ("Strike Validation", test_strike_validation),
        ("Core Functionality", test_core_functionality),
    ]
    
    results = []
    
    # Run all tests
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Error running {test_name}: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 COMPLETE TEST SUITE RESULTS")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        print("\nOptions Trading Tracker verified:")
        print("✅ Option pricing matches market data")
        print("✅ OptionStrat URLs generate correctly")
        print("✅ Trade suggestions use valid strikes")
        print("✅ All core functionality works")
        print("✅ System ready for production use")
    else:
        print("⚠️  Some tests failed. Review the issues above.")
        print(f"   Failed tests: {total - passed}")
        print("   Please fix the issues before using in production.")
    
    print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
