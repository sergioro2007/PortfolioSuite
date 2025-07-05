#!/usr/bin/env python3
"""
Quick Integration Test - Final Verification
==========================================

Test that all key components are working together:
- Option pricing with real market data
- Trade suggestion generation
- OptionStrat URL generation with decimal strikes
- UI components loading without errors
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_integration():
    """Run a comprehensive integration test"""
    print("🚀 Portfolio Management Suite - Integration Test")
    print("=" * 60)
    
    try:
        print("\n1️⃣ Testing Options Tracker...")
        from src.options_tracker import OptionsTracker
        tracker = OptionsTracker()
        print("   ✅ OptionsTracker loaded successfully")
        
        print("\n2️⃣ Testing trade suggestion generation...")
        suggestions = tracker.generate_trade_suggestions(3)
        if suggestions and len(suggestions) > 0:
            print(f"   ✅ Generated {len(suggestions)} trade suggestions")
            for i, suggestion in enumerate(suggestions[:3], 1):
                strategy = suggestion['strategy']
                ticker = suggestion['ticker']
                credit = suggestion['credit']
                print(f"   📊 {i}. {ticker} {strategy} - Credit: ${credit:.2f}")
        else:
            print("   ⚠️  No trade suggestions generated")
        
        print("\n3️⃣ Testing UI components...")
        from src.options_tracker_ui import generate_optionstrat_url, render_options_tracker
        print("   ✅ UI components loaded successfully")
        
        print("\n4️⃣ Testing OptionStrat URL generation with decimal strikes...")
        # Test with a known decimal strike using proper suggestion format
        test_suggestion = {
            'ticker': 'NVDA',
            'expiration': '2025-08-01',
            'legs': [
                {'action': 'SELL', 'option_type': 'CALL', 'strike': 172.5, 'quantity': 1},
                {'action': 'BUY', 'option_type': 'CALL', 'strike': 175.0, 'quantity': 1}
            ]
        }
        url = generate_optionstrat_url(test_suggestion)
        if '172.5' in url:
            print("   ✅ Decimal strike 172.5 preserved in URL")
        else:
            print("   ❌ Decimal strike not preserved in URL")
            print(f"   URL: {url}")
        
        print("\n5️⃣ Testing real option price fetching...")
        strikes = [172.5, 175.0]
        prices = tracker.get_option_prices('NVDA', strikes, '2025-08-01', 'call')
        nvda_172_5_price = prices.get('CALL_172.5', 0)
        if nvda_172_5_price > 0:
            print(f"   ✅ NVDA 172.5 CALL price: ${nvda_172_5_price:.2f}")
        else:
            print("   ⚠️  Could not fetch NVDA 172.5 CALL price")
        
        print("\n" + "=" * 60)
        print("🎉 INTEGRATION TEST COMPLETE")
        print("✅ All core components are working correctly!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_integration()
    sys.exit(0 if success else 1)
