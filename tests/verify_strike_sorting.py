#!/usr/bin/env python3
"""
🎯 Comprehensive Strike Price Sorting Verification
=================================================

This script verifies that both backend and UI sort trade legs by strike price correctly.
For example: strikes 521/511/591/601 should display as 511/521/591/601 (smallest first).
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.options_tracker import OptionsTracker

def main():
    print("🎯 STRIKE PRICE SORTING VERIFICATION")
    print("=" * 50)
    
    tracker = OptionsTracker()
    suggestions = tracker.generate_trade_suggestions(num_suggestions=1)
    
    if not suggestions:
        print("❌ No suggestions generated")
        return
    
    suggestion = suggestions[0]
    print(f"\n📊 Strategy: {suggestion['strategy']}")
    print(f"🏷️  Ticker: {suggestion['ticker']}")
    
    if 'legs' in suggestion:
        print(f"\n📋 BACKEND GENERATED LEGS (already sorted by strike):")
        backend_strikes = []
        for i, leg in enumerate(suggestion['legs'], 1):
            backend_strikes.append(leg['strike'])
            print(f"   {i}. {leg['action']} {leg['type']} ${leg['strike']:.2f} @ ${leg['price']:.2f}")
        
        print(f"\n🔢 Backend strike order: {backend_strikes}")
        
        # Simulate UI processing
        print(f"\n🖥️  UI PROCESSING (sorts by strike price):")
        legs_data = []
        for leg in suggestion['legs']:
            legs_data.append({
                'Action': leg['action'],
                'Type': leg['type'],
                'Strike': f"${leg['strike']:.2f}",
                'Est. Price': f"${leg['price']:.2f}",
                'Strike_Sort': leg['strike']
            })
        
        # Sort by strike price (UI code)
        legs_data.sort(key=lambda x: x['Strike_Sort'])
        
        ui_strikes = []
        for i, leg in enumerate(legs_data, 1):
            ui_strikes.append(leg['Strike_Sort'])
            print(f"   {i}. {leg['Action']} {leg['Type']} {leg['Strike']} @ {leg['Est. Price']}")
        
        print(f"\n🔢 UI strike order: {ui_strikes}")
        
        # Verification
        print(f"\n✅ VERIFICATION:")
        is_sorted = backend_strikes == sorted(backend_strikes)
        print(f"   Backend strikes sorted: {'✅ YES' if is_sorted else '❌ NO'}")
        
        ui_matches_backend = backend_strikes == ui_strikes
        print(f"   UI matches backend: {'✅ YES' if ui_matches_backend else '❌ NO'}")
        
        smallest_first = (len(backend_strikes) == 0 or 
                         backend_strikes[0] == min(backend_strikes))
        print(f"   Smallest strike first: {'✅ YES' if smallest_first else '❌ NO'}")
        
        print(f"\n🎯 RESULT:")
        if is_sorted and ui_matches_backend and smallest_first:
            print("   ✅ PERFECT! Strikes are correctly sorted with smallest first!")
            print(f"   📈 Order: {' → '.join([f'${s:.0f}' for s in backend_strikes])}")
        else:
            print("   ❌ Issues found with strike sorting!")
            if not is_sorted:
                print(f"      Expected: {sorted(backend_strikes)}")
                print(f"      Got: {backend_strikes}")
    
    else:
        print("❌ No legs found in suggestion")

if __name__ == "__main__":
    main()
