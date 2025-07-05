#!/usr/bin/env python3
"""
Quick test to check if trade suggestions are now generated
"""

import sys
import os
# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.options_tracker import OptionsTracker

def test_suggestions():
    """Test if we get trade suggestions now"""
    print("🧪 Testing Trade Suggestion Generation")
    print("=" * 50)
    
    tracker = OptionsTracker()
    
    # Try to generate suggestions
    print("📊 Generating trade suggestions...")
    suggestions = tracker.generate_trade_suggestions(num_suggestions=5)
    
    print(f"📋 Generated {len(suggestions)} suggestions")
    
    if suggestions:
        print("\n✅ SUCCESS! Suggestions generated:")
        for i, suggestion in enumerate(suggestions, 1):
            ticker = suggestion['ticker']
            strategy = suggestion['strategy']
            confidence = suggestion['confidence']
            credit = suggestion['credit']
            
            print(f"{i}. {ticker} {strategy} - Confidence: {confidence}% - Credit: ${credit:.2f}")
            
            # Check for decimal strikes (especially NVDA 172.5)
            for leg in suggestion['legs']:
                if leg['strike'] == 172.5:
                    print(f"   🎯 Found 172.5 strike! {leg['action']} {leg['type']} ${leg['strike']} = ${leg['price']:.2f}")
        
        return True
    else:
        print("❌ No suggestions generated")
        return False

if __name__ == "__main__":
    test_suggestions()
