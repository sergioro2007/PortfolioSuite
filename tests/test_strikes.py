#!/usr/bin/env python3
"""
Test script to verify strike price generation
"""

import sys
import os

# Add parent directory to path so we can import the main modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.options_tracker import OptionsTracker

def test_strike_generation():
    tracker = OptionsTracker()
    
    # Test with SPY at ~625
    current_price = 625.0
    
    print(f"🎯 Testing Strike Generation for SPY at ${current_price}")
    print("=" * 50)
    
    # Test different OTM distances
    distances = [0.005, 0.01, 0.015, 0.02, 0.025, 0.03]
    
    for distance in distances:
        put_strike = tracker.find_otm_strikes(current_price, distance, 'put')
        call_strike = tracker.find_otm_strikes(current_price, distance, 'call')
        
        put_distance_actual = (current_price - put_strike) / current_price * 100
        call_distance_actual = (call_strike - current_price) / current_price * 100
        
        print(f"{distance*100:.1f}% OTM:")
        print(f"  PUT:  ${put_strike:.2f} (actual: {put_distance_actual:.2f}% OTM)")
        print(f"  CALL: ${call_strike:.2f} (actual: {call_distance_actual:.2f}% OTM)")
        print()
    
    # Test current strategy strikes
    print("📊 Current Strategy Strikes:")
    print("-" * 30)
    
    # Iron Condor strikes (current settings)
    put_short = tracker.find_otm_strikes(current_price, 0.055, 'put')    # ~5.5% OTM
    put_long = tracker.find_otm_strikes(current_price, 0.08, 'put')      # ~8% OTM
    call_short = tracker.find_otm_strikes(current_price, 0.055, 'call')  # ~5.5% OTM  
    call_long = tracker.find_otm_strikes(current_price, 0.08, 'call')    # ~8% OTM
    
    print(f"Iron Condor (SPY @ ${current_price}):")
    print(f"  SELL PUT:  ${put_short:.2f}")
    print(f"  BUY PUT:   ${put_long:.2f}")
    print(f"  SELL CALL: ${call_short:.2f}")
    print(f"  BUY CALL:  ${call_long:.2f}")
    print()
    
    # Compare with your Webull example
    print("🔍 Comparison with Webull strikes:")
    print("-" * 35)
    print("Your Webull Iron Condor:")
    print("  SELL PUT:  $590.00")
    print("  BUY PUT:   $575.00") 
    print("  SELL CALL: $660.00")
    print("  BUY CALL:  $675.00")
    print()
    
    webull_put_distance = (625 - 590) / 625 * 100
    webull_call_distance = (660 - 625) / 625 * 100
    
    print(f"Webull distances: PUT {webull_put_distance:.1f}% OTM, CALL {webull_call_distance:.1f}% OTM")

if __name__ == "__main__":
    test_strike_generation()
