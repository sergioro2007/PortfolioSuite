#!/usr/bin/env python3

import sys
import os
# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.options_tracker import OptionsTracker

# Test what gets displayed in the UI
tracker = OptionsTracker()
suggestions = tracker.generate_trade_suggestions(1)

if suggestions:
    suggestion = suggestions[0]
    print(f"🎯 Trade Suggestion: {suggestion['strategy']} on {suggestion['ticker']}")
    
    if 'legs' in suggestion:
        print("\n📋 Raw legs from suggestion (already sorted by backend):")
        for i, leg in enumerate(suggestion['legs'], 1):
            print(f"  {i}. {leg['action']} {leg['type']} ${leg['strike']:.2f} @ ${leg['price']:.2f}")
        
        print(f"\n💰 Strike prices in order: {[leg['strike'] for leg in suggestion['legs']]}")
        
        # Simulate what the UI does
        print("\n🖥️  What UI should display (after UI sorting by strike price):")
        legs_data = []
        for leg in suggestion['legs']:
            legs_data.append({
                'Action': leg['action'],
                'Type': leg['type'],
                'Strike': f"${leg['strike']:.2f}",
                'Est. Price': f"${leg['price']:.2f}",
                'Strike_Sort': leg['strike']  # Sort by strike price, not option price
            })
        
        # Sort legs by strike price (smallest on top) - this is what UI does
        legs_data.sort(key=lambda x: x['Strike_Sort'])
        
        for i, leg in enumerate(legs_data, 1):
            print(f"  {i}. {leg['Action']} {leg['Type']} {leg['Strike']} @ {leg['Est. Price']}")
        
        ui_strikes = [leg['Strike_Sort'] for leg in legs_data]
        print(f"\n💰 UI strike prices in order: {ui_strikes}")
        print(f"✅ Smallest strike price on top: {ui_strikes[0] <= min(ui_strikes)}")
        
        # Check if there's any difference
        backend_strikes = [leg['strike'] for leg in suggestion['legs']]
        if backend_strikes == ui_strikes:
            print("✅ Backend and UI sorting match perfectly!")
        else:
            print("❌ Backend and UI sorting differ!")
            print(f"   Backend strikes: {backend_strikes}")
            print(f"   UI strikes: {ui_strikes}")
    
    else:
        print("❌ No legs found in suggestion")
else:
    print("❌ No suggestions generated")
