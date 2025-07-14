#!/usr/bin/env python3
"""
Test for Options Trading Trade Suggestions
==========================================

Tests the generate_trade_suggestions method to ensure it works correctly.
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

def test_generate_trade_suggestions():
    """Test the generate_trade_suggestions method"""
    print("🧪 Testing generate_trade_suggestions method...")
    
    try:
        from portfolio_suite.options_trading.core import OptionsTracker
        
        # Initialize tracker
        tracker = OptionsTracker()
        print("✅ OptionsTracker initialized successfully")
        
        # Test method exists
        assert hasattr(tracker, 'generate_trade_suggestions'), "Method generate_trade_suggestions not found"
        print("✅ generate_trade_suggestions method exists")
        
        # Test method call with default parameters
        suggestions = tracker.generate_trade_suggestions()
        print(f"✅ Method called successfully, returned {len(suggestions)} suggestions")
        
        # Test with specific number
        suggestions_3 = tracker.generate_trade_suggestions(3)
        print(f"✅ Method with parameter 3 returned {len(suggestions_3)} suggestions")
        
        # Validate suggestion structure
        if suggestions_3:
            suggestion = suggestions_3[0]
            required_fields = [
                'ticker', 'strategy', 'confidence', 'expected_profit', 
                'risk', 'probability', 'reason', 'entry_price', 
                'target_price', 'stop_loss'
            ]
            
            for field in required_fields:
                assert field in suggestion, f"Missing required field: {field}"
            
            print("✅ Suggestion structure is valid")
            print(f"   Sample suggestion: {suggestion['ticker']} - {suggestion['strategy']}")
            print(f"   Expected profit: ${suggestion['expected_profit']}")
            print(f"   Confidence: {suggestion['confidence']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_helper_method():
    """Test the _create_trade_suggestion helper method"""
    print("🧪 Testing _create_trade_suggestion helper method...")
    
    try:
        from portfolio_suite.options_trading.core import OptionsTracker
        
        tracker = OptionsTracker()
        
        # Test helper method
        prediction = {
            'target_price': 155.0,
            'lower_bound': 150.0,
            'upper_bound': 160.0,
            'confidence': 0.7
        }
        
        suggestion = tracker._create_trade_suggestion('AAPL', 152.0, prediction)
        
        assert suggestion is not None, "Helper method returned None"
        assert suggestion['ticker'] == 'AAPL', "Incorrect ticker"
        assert 'strategy' in suggestion, "Missing strategy"
        
        print("✅ Helper method works correctly")
        print(f"   Generated strategy: {suggestion['strategy']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Helper test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Running Options Trading Trade Suggestions Tests\n")
    
    success1 = test_generate_trade_suggestions()
    print()
    success2 = test_helper_method()
    
    print(f"\n📊 Test Results:")
    print(f"   Main method test: {'✅ PASS' if success1 else '❌ FAIL'}")
    print(f"   Helper method test: {'✅ PASS' if success2 else '❌ FAIL'}")
    
    if success1 and success2:
        print("\n🎉 All tests passed! The generate_trade_suggestions method is working correctly.")
        sys.exit(0)
    else:
        print("\n💥 Some tests failed. Check the implementation.")
        sys.exit(1)
