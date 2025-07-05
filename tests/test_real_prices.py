#!/usr/bin/env python3
"""
Test real option price fetching from yfinance
"""

import sys
import os

# Add parent directory to path so we can import the main modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.options_tracker import OptionsTracker

def test_real_option_prices():
    tracker = OptionsTracker()
    
    print("🎯 Testing Real Option Price Fetching")
    print("=" * 50)
    
    # Test SPY with exact strikes from your Webull data
    ticker = "SPY"
    strikes = [575, 590, 660, 675]
    expiration = "2025-08-01"  # August 1st expiration
    
    print(f"Fetching real option prices for {ticker}...")
    print(f"Strikes: {strikes}")
    print(f"Expiration: {expiration}")
    print()
    
    # Get real option prices
    option_prices = tracker.get_option_prices(ticker, strikes, expiration, 'both')
    
    print("📊 Real Option Prices from yfinance:")
    print("-" * 40)
    
    for strike in strikes:
        put_key = f"PUT_{strike}"
        call_key = f"CALL_{strike}"
        
        put_price = option_prices.get(put_key, "N/A")
        call_price = option_prices.get(call_key, "N/A")
        
        print(f"${strike} PUT:  ${put_price}")
        print(f"${strike} CALL: ${call_price}")
        print()
    
    print("🔍 Comparison with your Webull data:")
    print("-" * 40)
    print("Your Webull prices:")
    print("$575 PUT:  $1.23")
    print("$590 PUT:  $2.09") 
    print("$660 CALL: $0.50")
    print("$675 CALL: $0.10")
    print()
    
    # Calculate Iron Condor credit with real prices
    if all(key in option_prices for key in ["PUT_590", "PUT_575", "CALL_660", "CALL_675"]):
        put_spread_credit = option_prices["PUT_590"] - option_prices["PUT_575"]
        call_spread_credit = option_prices["CALL_660"] - option_prices["CALL_675"]
        total_credit = put_spread_credit + call_spread_credit
        
        print(f"💰 Iron Condor Credit Calculation:")
        print(f"Put spread credit: ${put_spread_credit:.2f}")
        print(f"Call spread credit: ${call_spread_credit:.2f}")
        print(f"Total credit: ${total_credit:.2f}")
        print()
        
        # Compare with Webull
        webull_put_credit = 2.09 - 1.23
        webull_call_credit = 0.50 - 0.10
        webull_total = webull_put_credit + webull_call_credit
        
        print(f"Your Webull calculation:")
        print(f"Put spread credit: ${webull_put_credit:.2f}")
        print(f"Call spread credit: ${webull_call_credit:.2f}")
        print(f"Total credit: ${webull_total:.2f}")

if __name__ == "__main__":
    test_real_option_prices()
