#!/usr/bin/env python3
"""
Test script to verify that trade legs are sorted by strike price
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.options_tracker import OptionsTracker

def test_strike_sorting():
    """Test that trade legs are sorted by strike price (smallest first)"""
    print("🧪 Testing strike price sorting...")
    
    tracker = OptionsTracker()
    
    # Test trade suggestions
    suggestions = tracker.generate_trade_suggestions(num_suggestions=3)
    
    if not suggestions:
        print("❌ No suggestions generated")
        return False
    
    all_sorted = True
    
    for i, suggestion in enumerate(suggestions):
        print(f"\n📊 Suggestion {i+1}: {suggestion['strategy']}")
        
        if 'legs' in suggestion:
            legs = suggestion['legs']
            strikes = [leg['strike'] for leg in legs]
            print(f"Strike order: {strikes}")
            
            # Check if strikes are sorted (smallest first)
            is_sorted = strikes == sorted(strikes)
            print(f"Correctly sorted: {'✅' if is_sorted else '❌'}")
            
            if not is_sorted:
                print(f"Expected: {sorted(strikes)}")
                print(f"Actual: {strikes}")
                all_sorted = False
            
            # Show leg details
            for j, leg in enumerate(legs):
                print(f"  Leg {j+1}: {leg['action']} {leg['type']} ${leg['strike']:.2f} @ ${leg['price']:.2f}")
        else:
            print("No legs data found")
    
    return all_sorted

if __name__ == "__main__":
    success = test_strike_sorting()
    if success:
        print("\n✅ All trade legs are correctly sorted by strike price!")
    else:
        print("\n❌ Strike price sorting needs to be fixed!")
    
    sys.exit(0 if success else 1)
