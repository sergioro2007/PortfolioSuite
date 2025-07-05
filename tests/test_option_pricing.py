#!/usr/bin/env python3
"""
Test the new option pricing model to see exact prices
"""

from src.options_tracker import OptionsTracker
from datetime import datetime, timedelta

def test_option_pricing():
    """Test option pricing for SPY to compare with Webull prices"""
    tracker = OptionsTracker()
    
    # Get current SPY price
    prediction = tracker.predict_price_range('SPY')
    current_price = prediction['current_price']
    
    print(f"🎯 Testing Option Pricing for SPY")
    print(f"Current Price: ${current_price:.2f}")
    print("=" * 50)
    
    # Test the exact strikes from Webull example
    expiration = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    test_strikes = [575, 590, 660, 675]
    
    option_prices = tracker.get_option_prices('SPY', test_strikes, expiration, 'both')
    
    print("🔍 Webull Strike Comparison:")
    print("Expected vs Our Estimates:")
    print()
    
    # Puts
    print("PUT OPTIONS:")
    print(f"Available keys: {list(option_prices.keys())}")
    print()
    print(f"$590 PUT - Webull: $1.07, Our estimate: ${option_prices.get('PUT_590', option_prices.get('PUT_590.0', 0)):.2f}")
    print(f"$575 PUT - Webull: $1.01, Our estimate: ${option_prices.get('PUT_575', option_prices.get('PUT_575.0', 0)):.2f}")
    print()
    
    # Calls  
    print("CALL OPTIONS:")
    print(f"$660 CALL - Webull: $1.07, Our estimate: ${option_prices.get('CALL_660', option_prices.get('CALL_660.0', 0)):.2f}")
    print(f"$675 CALL - Webull: $1.01, Our estimate: ${option_prices.get('CALL_675', option_prices.get('CALL_675.0', 0)):.2f}")
    print()
    
    # Calculate distances from current price
    print("📏 Distance Analysis:")
    for strike in test_strikes:
        distance_pct = abs(strike - current_price) / current_price * 100
        otm_type = "PUT" if strike < current_price else "CALL"
        print(f"${strike} {otm_type}: {distance_pct:.1f}% OTM")
    
    print()
    
    # Show Iron Condor suggestion for comparison
    suggestions = tracker.generate_trade_suggestions(1)
    if suggestions:
        suggestion = suggestions[0]
        if suggestion['strategy'] == 'Iron Condor':
            print("🦅 Iron Condor Suggestion:")
            print(f"PUT Spread: SELL ${suggestion['put_short_strike']:.0f} / BUY ${suggestion['put_long_strike']:.0f}")
            print(f"CALL Spread: SELL ${suggestion['call_short_strike']:.0f} / BUY ${suggestion['call_long_strike']:.0f}")
            print(f"Total Credit: ${suggestion['credit']:.2f}")
            print()
            print("Individual Leg Prices:")
            for leg in suggestion['legs']:
                print(f"{leg['action']} {leg['type']} ${leg['strike']:.0f}: ${leg['price']:.2f}")

if __name__ == "__main__":
    test_option_pricing()
