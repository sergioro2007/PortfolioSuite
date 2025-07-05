#!/usr/bin/env python3
"""
🧪 Comprehensive Test Suite for Options Trading Tracker
======================================================

This test runner consolidates all functionality tests to verify:
- Strike price generation
- Real option price fetching
- Trade suggestion logic
- Strategy reasoning
- UI components

Run this to verify all functionality is working correctly.
"""

import sys
import os

# Add parent directory to path so we can import the main modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datetime import datetime
from src.options_tracker import OptionsTracker

class TestRunner:
    def __init__(self):
        self.passed_tests = 0
        self.failed_tests = 0
        self.tracker = OptionsTracker()
    
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"    {details}")
        
        if success:
            self.passed_tests += 1
        else:
            self.failed_tests += 1
    
    def test_strike_generation(self):
        """Test realistic strike price generation"""
        print("\n🎯 Testing Strike Generation")
        print("-" * 40)
        
        # Test SPY strikes at ~625
        current_price = 625.0
        
        # Test different OTM distances
        try:
            put_590 = self.tracker.find_otm_strikes(current_price, 0.055, 'put')
            put_575 = self.tracker.find_otm_strikes(current_price, 0.08, 'put')
            call_660 = self.tracker.find_otm_strikes(current_price, 0.055, 'call')
            call_675 = self.tracker.find_otm_strikes(current_price, 0.08, 'call')
            
            # Verify strikes match expected values
            strikes_correct = (put_590 == 590 and put_575 == 575 and 
                             call_660 == 660 and call_675 == 675)
            
            self.log_test("Strike Generation", strikes_correct, 
                         f"Generated: PUT {put_590}/{put_575}, CALL {call_660}/{call_675}")
            
            return strikes_correct
            
        except Exception as e:
            self.log_test("Strike Generation", False, f"Error: {e}")
            return False
    
    def test_option_pricing(self):
        """Test real option price fetching"""
        print("\n💰 Testing Option Price Fetching")
        print("-" * 40)
        
        try:
            ticker = "SPY"
            strikes = [575, 590, 660, 675]
            expiration = "2025-08-01"
            
            option_prices = self.tracker.get_option_prices(ticker, strikes, expiration, 'both')
            
            # Check if we got prices for all strikes
            expected_keys = ["PUT_590", "PUT_575", "CALL_660", "CALL_675"]
            prices_found = all(key in option_prices for key in expected_keys)
            
            if prices_found:
                put_590_price = option_prices["PUT_590"]
                put_575_price = option_prices["PUT_575"]
                call_660_price = option_prices["CALL_660"]
                call_675_price = option_prices["CALL_675"]
                
                # Verify prices are reasonable (based on Webull data)
                reasonable_prices = (1.5 < put_590_price < 3.0 and 
                                   1.0 < put_575_price < 2.0 and
                                   0.3 < call_660_price < 0.8 and
                                   0.05 < call_675_price < 0.2)
                
                self.log_test("Option Price Fetching", reasonable_prices,
                             f"PUT 590: ${put_590_price}, PUT 575: ${put_575_price}, CALL 660: ${call_660_price}, CALL 675: ${call_675_price}")
                
                return reasonable_prices
            else:
                self.log_test("Option Price Fetching", False, "Missing price data")
                return False
                
        except Exception as e:
            self.log_test("Option Price Fetching", False, f"Error: {e}")
            return False
    
    def test_trade_suggestions(self):
        """Test trade suggestion generation"""
        print("\n💡 Testing Trade Suggestions")
        print("-" * 40)
        
        try:
            suggestions = self.tracker.generate_trade_suggestions(3)
            
            has_suggestions = len(suggestions) > 0
            self.log_test("Trade Suggestion Generation", has_suggestions,
                         f"Generated {len(suggestions)} suggestions")
            
            if has_suggestions:
                # Test first suggestion details
                suggestion = suggestions[0]
                required_fields = ['ticker', 'strategy', 'credit', 'legs', 'reasoning']
                has_required_fields = all(field in suggestion for field in required_fields)
                
                self.log_test("Suggestion Structure", has_required_fields,
                             f"Strategy: {suggestion.get('strategy', 'N/A')}, Credit: ${suggestion.get('credit', 0):.2f}")
                
                # Test if legs have prices
                legs = suggestion.get('legs', [])
                legs_have_prices = all('price' in leg and leg['price'] > 0 for leg in legs)
                
                self.log_test("Leg Pricing", legs_have_prices,
                             f"All {len(legs)} legs have valid prices")
                
                # Test reasoning exists
                has_reasoning = 'reasoning' in suggestion and len(suggestion['reasoning']) > 100
                
                self.log_test("Strategy Reasoning", has_reasoning,
                             "Detailed reasoning provided" if has_reasoning else "Missing reasoning")
                
                return has_suggestions and has_required_fields and legs_have_prices and has_reasoning
            
            return has_suggestions
            
        except Exception as e:
            self.log_test("Trade Suggestion Generation", False, f"Error: {e}")
            return False
    
    def test_iron_condor_credit(self):
        """Test Iron Condor credit calculation specifically"""
        print("\n🦅 Testing Iron Condor Credit Calculation")
        print("-" * 40)
        
        try:
            # Generate suggestions and look for Iron Condor
            suggestions = self.tracker.generate_trade_suggestions(5)
            
            iron_condor = None
            for suggestion in suggestions:
                if suggestion['strategy'] == 'Iron Condor':
                    iron_condor = suggestion
                    break
            
            if iron_condor:
                credit = iron_condor['credit']
                legs = iron_condor['legs']
                
                # Verify credit calculation
                if len(legs) == 4:
                    put_spread_credit = legs[0]['price'] - legs[1]['price']  # SELL PUT - BUY PUT
                    call_spread_credit = legs[2]['price'] - legs[3]['price']  # SELL CALL - BUY CALL
                    calculated_credit = put_spread_credit + call_spread_credit
                    
                    credit_matches = abs(credit - calculated_credit) < 0.05
                    
                    self.log_test("Iron Condor Credit", credit_matches,
                                 f"Expected: ${calculated_credit:.2f}, Got: ${credit:.2f}")
                    
                    # Check if credit is reasonable (should be around $1.20-$1.30 for SPY)
                    reasonable_credit = 1.0 < credit < 2.0
                    
                    self.log_test("Iron Condor Credit Range", reasonable_credit,
                                 f"Credit: ${credit:.2f} (should be $1.00-$2.00)")
                    
                    return credit_matches and reasonable_credit
                else:
                    self.log_test("Iron Condor Credit", False, "Wrong number of legs")
                    return False
            else:
                self.log_test("Iron Condor Credit", False, "No Iron Condor suggestion found")
                return False
                
        except Exception as e:
            self.log_test("Iron Condor Credit", False, f"Error: {e}")
            return False
    
    def test_technical_indicators(self):
        """Test technical indicator calculations"""
        print("\n📊 Testing Technical Indicators")
        print("-" * 40)
        
        try:
            indicators = self.tracker.get_technical_indicators("SPY")
            
            required_indicators = ['current_price', 'rsi', 'macd', 'volatility']
            has_indicators = all(ind in indicators for ind in required_indicators)
            
            self.log_test("Technical Indicators", has_indicators,
                         f"RSI: {indicators.get('rsi', 'N/A'):.1f}, Volatility: {indicators.get('volatility', 'N/A'):.3f}")
            
            # Test reasonable values
            if has_indicators:
                rsi = indicators['rsi']
                volatility = indicators['volatility']
                
                reasonable_values = (0 <= rsi <= 100 and 0.1 <= volatility <= 1.0)
                
                self.log_test("Indicator Values", reasonable_values,
                             "Values within expected ranges")
                
                return has_indicators and reasonable_values
            
            return has_indicators
            
        except Exception as e:
            self.log_test("Technical Indicators", False, f"Error: {e}")
            return False
    
    def test_fallback_pricing(self):
        """Test fallback pricing mechanism"""
        print("\n🔄 Testing Fallback Pricing")
        print("-" * 40)
        
        try:
            # Test with non-existent expiration to trigger fallback
            strikes = [590, 575, 660, 675]
            fallback_prices = self.tracker._fallback_option_prices("SPY", strikes, "2025-12-31", "both")
            
            # Should have Webull prices for SPY strikes
            expected_prices = {
                "PUT_590": 2.09,
                "PUT_575": 1.23,
                "CALL_660": 0.50,
                "CALL_675": 0.10
            }
            
            prices_match = all(fallback_prices.get(key) == expected_prices[key] 
                             for key in expected_prices.keys())
            
            self.log_test("Fallback Pricing", prices_match,
                         "Webull prices used as fallback")
            
            return prices_match
            
        except Exception as e:
            self.log_test("Fallback Pricing", False, f"Error: {e}")
            return False
    
    def run_all_tests(self):
        """Run all tests and provide summary"""
        print("🧪 Options Trading Tracker - Comprehensive Test Suite")
        print("=" * 60)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Run all test methods
        tests = [
            self.test_strike_generation,
            self.test_option_pricing,
            self.test_trade_suggestions,
            self.test_iron_condor_credit,
            self.test_technical_indicators,
            self.test_fallback_pricing
        ]
        
        for test_method in tests:
            try:
                test_method()
            except Exception as e:
                print(f"❌ FAIL {test_method.__name__}: Unexpected error: {e}")
                self.failed_tests += 1
        
        # Summary
        print("\n" + "=" * 60)
        print("📋 TEST SUMMARY")
        print("-" * 20)
        print(f"✅ Passed: {self.passed_tests}")
        print(f"❌ Failed: {self.failed_tests}")
        print(f"📊 Success Rate: {(self.passed_tests / (self.passed_tests + self.failed_tests) * 100):.1f}%")
        
        if self.failed_tests == 0:
            print("\n🎉 ALL TESTS PASSED! Options tracker is working correctly.")
            return True
        else:
            print(f"\n⚠️  {self.failed_tests} test(s) failed. Please review the issues above.")
            return False

if __name__ == "__main__":
    runner = TestRunner()
    success = runner.run_all_tests()
    sys.exit(0 if success else 1)
