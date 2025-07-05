#!/usr/bin/env python3
"""
Debug NVDA 172.50 Call Option Pricing
====================================

Investigate why our system shows $0.32 for NVDA 172.50 CALL when Webull shows $1.78
"""

import yfinance as yf
from datetime import datetime

def debug_nvda_172_5_call():
    """Debug the specific NVDA 172.50 call option pricing"""
    
    print("🔍 Debugging NVDA 172.50 CALL Option Pricing")
    print("=" * 60)
    
    ticker = "NVDA"
    strike = 172.5
    expiration = "2025-08-01"
    
    try:
        # Get current stock price
        stock = yf.Ticker(ticker)
        info = stock.info
        current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
        print(f"📊 {ticker} Current Price: ${current_price:.2f}")
        print(f"🎯 Target Strike: ${strike:.2f}")
        print(f"📅 Expiration: {expiration}")
        print(f"💰 Moneyness: ${current_price - strike:.2f} ({'ITM' if current_price > strike else 'OTM'})")
        
        # Get option chain
        print(f"\n🔗 Fetching option chain for {expiration}...")
        option_chain = stock.option_chain(expiration)
        calls = option_chain.calls
        
        print(f"📋 Available call strikes: {sorted(calls['strike'].unique())}")
        
        # Look for our specific strike
        strike_data = calls[calls['strike'] == strike]
        
        if not strike_data.empty:
            row = strike_data.iloc[0]
            bid = row['bid']
            ask = row['ask']
            last = row['lastPrice']
            volume = row['volume']
            open_interest = row['openInterest']
            
            print(f"\n💰 NVDA {strike} CALL {expiration} - Real Market Data:")
            print(f"  📊 Bid: ${bid:.2f}")
            print(f"  📊 Ask: ${ask:.2f}")
            print(f"  📊 Last: ${last:.2f}")
            print(f"  📊 Volume: {volume}")
            print(f"  📊 Open Interest: {open_interest}")
            
            if bid > 0 and ask > 0:
                midpoint = (bid + ask) / 2
                print(f"  📊 Midpoint: ${midpoint:.2f}")
                
                print(f"\n🎯 Comparison:")
                print(f"  Our System: $0.32")
                print(f"  Webull: $1.78")
                print(f"  yfinance Midpoint: ${midpoint:.2f}")
                print(f"  yfinance Last: ${last:.2f}")
                
                # Check which is closer to real data
                our_diff = abs(0.32 - midpoint)
                webull_diff = abs(1.78 - midpoint)
                
                print(f"\n📏 Accuracy Check:")
                print(f"  Our system vs yfinance: ${our_diff:.2f} difference")
                print(f"  Webull vs yfinance: ${webull_diff:.2f} difference")
                
                if our_diff < webull_diff:
                    print("  ✅ Our system is closer to yfinance data")
                else:
                    print("  ⚠️ Webull is closer to yfinance data")
                    
        else:
            print(f"\n❌ No data found for strike ${strike}")
            print("Available strikes near target:")
            nearby_strikes = calls[
                (calls['strike'] >= strike - 5) & 
                (calls['strike'] <= strike + 5)
            ]['strike'].sort_values()
            for s in nearby_strikes:
                print(f"  ${s:.2f}")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def check_our_pricing_model():
    """Check how our system calculates this price"""
    
    print(f"\n🔧 Checking Our Pricing Model")
    print("=" * 40)
    
    try:
        from src.options_tracker import OptionsTracker
        
        tracker = OptionsTracker()
        
        # Get our price for this specific option
        strikes = [172.5]
        prices = tracker.get_option_prices("NVDA", strikes, "2025-08-01", "call")
        
        call_price = prices.get("CALL_172.5", 0)
        print(f"📊 Our System Price for NVDA 172.5 CALL: ${call_price:.2f}")
        
        # Check if we're using fallback pricing
        real_prices = tracker.get_option_prices("NVDA", strikes, "2025-08-01", "call")
        print(f"📊 Real price fetch result: {real_prices}")
        
        # Test fallback pricing
        fallback_prices = tracker._fallback_option_prices("NVDA", strikes, "2025-08-01", "call")
        fallback_call_price = fallback_prices.get("CALL_172.5", 0)
        print(f"📊 Fallback Price: ${fallback_call_price:.2f}")
        
        if call_price == fallback_call_price:
            print("⚠️ Using fallback pricing (not real market data)")
        else:
            print("✅ Using real market data")
            
    except Exception as e:
        print(f"❌ Error checking our pricing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_nvda_172_5_call()
    check_our_pricing_model()
