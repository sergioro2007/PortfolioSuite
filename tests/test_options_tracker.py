#!/usr/bin/env python3
"""
Test script for Options Trading Tracker
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.options_tracker import OptionsTracker

def test_options_tracker():
    """Test basic functionality of the options tracker"""
    print("🎯 Testing Options Trading Tracker")
    print("=" * 50)
    
    # Initialize tracker
    tracker = OptionsTracker()
    print("✅ Tracker initialized successfully")
    
    # Test price prediction
    print("\n📊 Testing price predictions...")
    for ticker in ['SPY', 'QQQ', 'AAPL']:
        prediction = tracker.predict_price_range(ticker)
        if prediction:
            print(f"  {ticker}: ${prediction['current_price']:.2f} (Target: ${prediction['target_price']:.2f}, Prob: {prediction['bullish_probability']:.1%})")
        else:
            print(f"  {ticker}: Failed to get prediction")
    
    # Test trade suggestions
    print("\n💡 Testing trade suggestions...")
    suggestions = tracker.generate_trade_suggestions(2)
    
    if suggestions:
        for i, suggestion in enumerate(suggestions):
            print(f"  Suggestion #{i+1}: {suggestion['ticker']} {suggestion['strategy']}")
            print(f"    Bias: {suggestion['bias']} ({suggestion['confidence']:.0f}% confidence)")
            print(f"    Credit: ${suggestion['credit']:.2f}, Max Loss: ${suggestion['max_loss']:.2f}")
    else:
        print("  No suggestions generated")
    
    # Test trade management
    print("\n📋 Testing trade management...")
    open_trades = tracker.get_open_trades()
    closed_trades = tracker.get_closed_trades()
    print(f"  Open trades: {len(open_trades)}")
    print(f"  Closed trades: {len(closed_trades)}")
    
    # Test P&L calculation
    stats = tracker.calculate_weekly_pnl()
    print(f"  Total P&L: ${stats['total_pnl']:.2f}")
    print(f"  Win rate: {stats['win_rate']:.1%}")
    
    print("\n✅ Options Tracker test completed successfully!")

if __name__ == "__main__":
    try:
        test_options_tracker()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
