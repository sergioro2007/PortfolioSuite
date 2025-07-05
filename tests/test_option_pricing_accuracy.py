#!/usr/bin/env python3
"""
Option Pricing Accuracy Test
============================

Test to verify that the suggested leg prices of spreads match real online values from yfinance.
This ensures our pricing model is accurate and reliable for trade suggestions.
"""

import sys
import os
import traceback
from datetime import datetime
import yfinance as yf

# Add parent directory to path so we can import the main modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_option_pricing_accuracy():
    """Test that our option pricing matches real market data"""
    print("💰 Testing Option Pricing Accuracy...")
    
    try:
        from src.options_tracker import OptionsTracker
        
        tracker = OptionsTracker()
        
        # Test with liquid tickers that should have good option data
        test_tickers = ['SPY', 'QQQ', 'AAPL']
        expiration_date = '2025-08-01'
        
        all_accurate = True
        
        for ticker in test_tickers:
            print(f"\n📊 Testing {ticker} option pricing...")
            
            # Get trade suggestions for this ticker
            suggestions = tracker.generate_trade_suggestions(num_suggestions=5)
            ticker_suggestions = [s for s in suggestions if s['ticker'] == ticker]
            
            if not ticker_suggestions:
                print(f"  ⚠️  No suggestions found for {ticker}")
                continue
            
            suggestion = ticker_suggestions[0]  # Test the first suggestion
            strategy = suggestion['strategy']
            
            print(f"  🎯 Testing {strategy} pricing...")
            
            # Get the strikes from the suggestion
            if strategy == 'Bull Put Spread':
                strikes_to_test = [
                    ('PUT', suggestion['short_strike']),
                    ('PUT', suggestion['long_strike'])
                ]
            elif strategy == 'Bear Call Spread':
                strikes_to_test = [
                    ('CALL', suggestion['short_strike']),
                    ('CALL', suggestion['long_strike'])
                ]
            elif strategy == 'Iron Condor':
                strikes_to_test = [
                    ('PUT', suggestion['put_long_strike']),
                    ('PUT', suggestion['put_short_strike']),
                    ('CALL', suggestion['call_short_strike']),
                    ('CALL', suggestion['call_long_strike'])
                ]
            else:
                print(f"  ⚠️  Strategy {strategy} not implemented in test")
                continue
            
            # Get real market prices from yfinance
            try:
                stock = yf.Ticker(ticker)
                option_chain = stock.option_chain(expiration_date)
                
                # Test each leg
                for option_type, strike in strikes_to_test:
                    strike_int = int(strike)
                    
                    # Get our suggested price
                    suggested_price = None
                    for leg in suggestion['legs']:
                        if leg['type'] == option_type and leg['strike'] == strike:
                            suggested_price = leg['price']
                            break
                    
                    if suggested_price is None:
                        print(f"    ❌ Could not find suggested price for {option_type} {strike}")
                        all_accurate = False
                        continue
                    
                    # Get real market price
                    if option_type == 'PUT':
                        market_data = option_chain.puts
                    else:
                        market_data = option_chain.calls
                    
                    strike_data = market_data[market_data['strike'] == strike_int]
                    
                    if strike_data.empty:
                        print(f"    ⚠️  No market data for {option_type} {strike}")
                        continue
                    
                    # Calculate real market price (midpoint of bid/ask)
                    bid = strike_data['bid'].iloc[0]
                    ask = strike_data['ask'].iloc[0]
                    last = strike_data['lastPrice'].iloc[0]
                    
                    if bid > 0 and ask > 0:
                        market_price = (bid + ask) / 2
                        source = "bid/ask midpoint"
                    else:
                        market_price = last
                        source = "last price"
                    
                    # Calculate accuracy
                    if market_price > 0:
                        price_diff = abs(suggested_price - market_price)
                        price_diff_pct = (price_diff / market_price) * 100
                        
                        # Consider accurate if within 15% (options can have wide spreads)
                        is_accurate = price_diff_pct <= 15.0
                        
                        status = "✅" if is_accurate else "⚠️"
                        print(f"    {status} {option_type} ${strike}: Suggested=${suggested_price:.2f}, Market=${market_price:.2f} ({source}), Diff={price_diff_pct:.1f}%")
                        
                        if not is_accurate:
                            all_accurate = False
                    else:
                        print(f"    ⚠️  {option_type} ${strike}: No valid market price available")
                
            except Exception as e:
                print(f"    ❌ Error fetching market data for {ticker}: {e}")
                all_accurate = False
        
        return all_accurate
        
    except Exception as e:
        print(f"  ❌ Error testing option pricing: {e}")
        traceback.print_exc()
        return False

def test_spread_credit_accuracy():
    """Test that spread credits are calculated correctly"""
    print("\n💸 Testing Spread Credit Calculation...")
    
    try:
        from src.options_tracker import OptionsTracker
        
        tracker = OptionsTracker()
        
        # Get some spread suggestions
        suggestions = tracker.generate_trade_suggestions(num_suggestions=3)
        
        for suggestion in suggestions:
            strategy = suggestion['strategy']
            ticker = suggestion['ticker']
            
            print(f"\n  🎯 Testing {strategy} for {ticker}...")
            
            # Calculate credit manually from legs
            legs = suggestion['legs']
            calculated_credit = 0
            
            for leg in legs:
                if leg['action'] == 'SELL':
                    calculated_credit += leg['price']
                elif leg['action'] == 'BUY':
                    calculated_credit -= leg['price']
            
            # Compare with suggested credit
            suggested_credit = suggestion['credit']
            credit_diff = abs(calculated_credit - suggested_credit)
            
            if credit_diff < 0.01:  # Allow for small rounding differences
                print(f"    ✅ Credit calculation correct: ${suggested_credit:.2f}")
            else:
                print(f"    ❌ Credit mismatch: Suggested=${suggested_credit:.2f}, Calculated=${calculated_credit:.2f}")
                return False
        
        print("  🎉 All spread credits calculated correctly!")
        return True
        
    except Exception as e:
        print(f"  ❌ Error testing spread credits: {e}")
        traceback.print_exc()
        return False

def test_price_consistency():
    """Test that option prices are consistent across multiple calls"""
    print("\n🔄 Testing Price Consistency...")
    
    try:
        from src.options_tracker import OptionsTracker
        
        tracker = OptionsTracker()
        
        # Test same strikes multiple times to ensure consistency
        ticker = 'SPY'
        strikes = [600, 610, 620]
        expiration = '2025-08-01'
        
        print(f"  📊 Testing {ticker} price consistency...")
        
        # Get prices multiple times
        prices_1 = tracker.get_option_prices(ticker, strikes, expiration, 'both')
        prices_2 = tracker.get_option_prices(ticker, strikes, expiration, 'both')
        
        consistent = True
        for strike in strikes:
            for option_type in ['PUT', 'CALL']:
                key = f"{option_type}_{strike}"
                
                price_1 = prices_1.get(key, 0)
                price_2 = prices_2.get(key, 0)
                
                if price_1 != price_2:
                    print(f"    ❌ Inconsistent pricing for {key}: {price_1} vs {price_2}")
                    consistent = False
                else:
                    print(f"    ✅ {key}: ${price_1:.2f} (consistent)")
        
        if consistent:
            print("  🎉 All prices are consistent across calls!")
        
        return consistent
        
    except Exception as e:
        print(f"  ❌ Error testing price consistency: {e}")
        traceback.print_exc()
        return False

def test_fallback_pricing():
    """Test that fallback pricing works when market data is unavailable"""
    print("\n🔧 Testing Fallback Pricing...")
    
    try:
        from src.options_tracker import OptionsTracker
        
        tracker = OptionsTracker()
        
        # Test with a ticker that might not have option data
        test_ticker = 'INVALID_TICKER'
        strikes = [100, 110, 120]
        expiration = '2025-08-01'
        
        print(f"  📊 Testing fallback pricing for invalid ticker...")
        
        # This should trigger fallback pricing
        fallback_prices = tracker._fallback_option_prices(test_ticker, strikes, expiration, 'both')
        
        if fallback_prices:
            print(f"    ✅ Fallback pricing generated {len(fallback_prices)} prices")
            
            # Check that all expected prices are there
            for strike in strikes:
                put_key = f"PUT_{strike}"
                call_key = f"CALL_{strike}"
                
                if put_key in fallback_prices and call_key in fallback_prices:
                    put_price = fallback_prices[put_key]
                    call_price = fallback_prices[call_key]
                    print(f"    ✅ ${strike}: PUT=${put_price:.2f}, CALL=${call_price:.2f}")
                else:
                    print(f"    ❌ Missing fallback prices for strike ${strike}")
                    return False
            
            print("  🎉 Fallback pricing works correctly!")
            return True
        else:
            print("    ❌ No fallback prices generated")
            return False
        
    except Exception as e:
        print(f"  ❌ Error testing fallback pricing: {e}")
        traceback.print_exc()
        return False

def test_optionstrat_url_decimal_strikes():
    """Test that OptionStrat URLs preserve decimal strikes like 172.5"""
    print("\n🔗 Testing OptionStrat URL Decimal Strike Preservation...")
    
    try:
        from src.options_tracker_ui import generate_optionstrat_url
        
        # Test the exact NVDA Iron Condor example from user
        nvda_suggestion = {
            'ticker': 'NVDA',
            'strategy': 'Iron Condor',
            'put_long_strike': 146.0,
            'put_short_strike': 150.0,
            'call_short_strike': 170.0,
            'call_long_strike': 172.5,  # Half-dollar strike
            'expiration': '2025-08-01'
        }
        
        expected_url = 'https://optionstrat.com/build/iron-condor/NVDA/.NVDA250801P146,-.NVDA250801P150,-.NVDA250801C170,.NVDA250801C172.5'
        generated_url = generate_optionstrat_url(nvda_suggestion)
        
        print(f"  🎯 Testing NVDA Iron Condor (146/150/170/172.5)...")
        print(f"     Expected: {expected_url}")
        print(f"     Generated: {generated_url}")
        
        if generated_url == expected_url:
            print(f"    ✅ URL correct - decimal strike 172.5 preserved!")
            return True
        else:
            print(f"    ❌ URL mismatch!")
            return False
        
    except Exception as e:
        print(f"  ❌ Error testing OptionStrat URL: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all pricing accuracy tests"""
    print("💰 Option Pricing Accuracy Test Suite")
    print("=" * 50)
    
    test_results = []
    
    # Run all tests
    test_results.append(('Option Pricing Accuracy', test_option_pricing_accuracy()))
    test_results.append(('Spread Credit Calculation', test_spread_credit_accuracy()))
    test_results.append(('Price Consistency', test_price_consistency()))
    test_results.append(('Fallback Pricing', test_fallback_pricing()))
    test_results.append(('OptionStrat URL Decimal Strikes', test_optionstrat_url_decimal_strikes()))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 PRICING TEST RESULTS")
    print("=" * 50)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} pricing tests passed")
    
    if passed == total:
        print("🎉 ALL PRICING TESTS PASSED!")
        print("\nPricing accuracy verified:")
        print("✅ Option prices match market data within acceptable range")
        print("✅ Spread credits are calculated correctly")
        print("✅ Pricing is consistent across multiple calls")
        print("✅ Fallback pricing works when market data unavailable")
    else:
        print("⚠️  Some pricing tests failed. Review the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
