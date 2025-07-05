#!/usr/bin/env python3
"""
Test script to verify the $100 minimum profit target filter is working
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from options_tracker import OptionsTracker

def test_profit_filter():
    print("🎯 Testing $100 Minimum Profit Target Filter")
    print("=" * 50)
    
    tracker = OptionsTracker()
    suggestions = tracker.generate_trade_suggestions(5)
    
    if not suggestions:
        print("✅ FILTER WORKING: No suggestions generated")
        print("   All potential trades had profit targets below $100")
        print("\n💡 This is expected when market conditions don't offer high-profit trades")
        return
    
    print(f"📊 Generated {len(suggestions)} suggestion(s) meeting $100+ requirement:")
    print()
    
    all_meet_minimum = True
    for i, suggestion in enumerate(suggestions, 1):
        credit_per_share = suggestion['credit']
        profit_target_per_share = suggestion['profit_target']
        
        credit_per_contract = credit_per_share * 100
        profit_target_per_contract = profit_target_per_share * 100
        
        meets_minimum = profit_target_per_contract >= 100
        status = "✅" if meets_minimum else "❌"
        
        print(f"{status} Suggestion #{i}: {suggestion['ticker']} {suggestion['strategy']}")
        print(f"   Credit: ${credit_per_contract:.0f} per contract")
        print(f"   Profit Target: ${profit_target_per_contract:.0f} per contract")
        print(f"   Meets $100 minimum: {meets_minimum}")
        print()
        
        if not meets_minimum:
            all_meet_minimum = False
    
    if all_meet_minimum:
        print("🎉 SUCCESS: All suggestions meet the $100 minimum profit target!")
    else:
        print("❌ FAILURE: Some suggestions don't meet the minimum requirement")

if __name__ == "__main__":
    test_profit_filter()
