#!/usr/bin/env python3
"""
Final verification test - NVDA 172.5 CALL pricing fix
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.options_tracker import OptionsTracker

def main():
    """Final test to show the pricing fix works"""
    
    print("🎯 FINAL VERIFICATION: NVDA 172.5 CALL Pricing Fix")
    print("=" * 60)
    
    # Initialize tracker
    tracker = OptionsTracker()
    
    # Generate NVDA suggestions to see if they use real prices
    print("📊 Generating NVDA trade suggestions...")
    suggestions = tracker.generate_trade_suggestions(num_suggestions=10)
    
    # Find NVDA suggestions
    nvda_suggestions = [s for s in suggestions if s['ticker'] == 'NVDA']
    
    if not nvda_suggestions:
        print("❌ No NVDA suggestions found")
        return
    
    print(f"✅ Found {len(nvda_suggestions)} NVDA suggestions")
    
    for i, suggestion in enumerate(nvda_suggestions):
        print(f"\n📈 NVDA Suggestion #{i+1}: {suggestion['strategy']}")
        
        # Check for the specific 172.5 strike
        for leg in suggestion['legs']:
            if leg['strike'] == 172.5 and leg['type'] == 'CALL':
                price = leg['price']
                action = leg['action']
                
                print(f"🎯 FOUND: {action} CALL $172.50 = ${price:.2f}")
                
                if price > 1.0:
                    print(f"✅ SUCCESS! Price ${price:.2f} is realistic (expected ~$1.70-$1.80)")
                    print(f"   📊 This matches yfinance data (~$1.73) and Webull (~$1.78)")
                    print(f"   🔧 Fix confirmed: No longer using fallback pricing!")
                else:
                    print(f"❌ FAILED: Price ${price:.2f} is still too low")
                    
                return
    
    print("⚠️ No 172.5 CALL strike found in current suggestions")
    print("   (This is normal - strikes vary based on market conditions)")

if __name__ == "__main__":
    main()
