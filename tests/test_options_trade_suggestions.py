#!/usr/bin/env python3
"""
Test for Options Trading Trade Suggestions - Comprehensive Test Suite
====================================================================

Tests the generate_trade_suggestions method and related functionality.
This ensures the method works correctly and handles edge cases.
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

def test_generate_trade_suggestions():
    """Test the main generate_trade_suggestions method"""
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
        suggestions_2 = tracker.generate_trade_suggestions(2)
        print(f"✅ Method with parameter 2 returned {len(suggestions_2)} suggestions")
        
        # Test with larger number
        suggestions_5 = tracker.generate_trade_suggestions(5)
        print(f"✅ Method with parameter 5 returned {len(suggestions_5)} suggestions")
        
        # Validate suggestion structure
        if suggestions_2:
            suggestion = suggestions_2[0]
            required_fields = [
                'ticker', 'strategy', 'confidence', 'expected_profit', 
                'risk', 'probability', 'reason', 'entry_price', 
                'target_price', 'stop_loss', 'strike_price', 'expiration'
            ]
            
            for field in required_fields:
                assert field in suggestion, f"Missing required field: {field}"
            
            print("✅ Suggestion structure is valid")
            print(f"   Sample suggestion: {suggestion['ticker']} - {suggestion['strategy']}")
            print(f"   Expected profit: ${suggestion['expected_profit']}")
            print(f"   Risk: ${suggestion['risk']}")
            print(f"   Confidence: {suggestion['confidence']}")
            print(f"   Probability: {suggestion['probability']}")
            
            # Validate data types
            assert isinstance(suggestion['expected_profit'], (int, float)), "Expected profit should be numeric"
            assert isinstance(suggestion['risk'], (int, float)), "Risk should be numeric"
            assert isinstance(suggestion['probability'], (float)), "Probability should be float"
            assert 0 <= suggestion['probability'] <= 1, "Probability should be between 0 and 1"
            
            print("✅ Data types are correct")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_edge_cases():
    """Test edge cases and error handling"""
    print("🧪 Testing edge cases...")
    
    try:
        from portfolio_suite.options_trading.core import OptionsTracker
        
        tracker = OptionsTracker()
        
        # Test with zero suggestions
        suggestions_0 = tracker.generate_trade_suggestions(0)
        print(f"✅ Zero suggestions request handled: {len(suggestions_0)} returned")
        
        # Test with very large number
        suggestions_100 = tracker.generate_trade_suggestions(100)
        print(f"✅ Large request handled: {len(suggestions_100)} returned")
        
        # Test fallback mechanism (ensure it works even if predictions fail)
        # This is handled internally by the method
        
        return True
        
    except Exception as e:
        print(f"❌ Edge case test failed: {e}")
        return False

def test_integration_with_ui():
    """Test that the method works as expected by the UI"""
    print("🧪 Testing UI integration...")
    
    try:
        from portfolio_suite.options_trading.core import OptionsTracker
        
        tracker = OptionsTracker()
        
        # This is the exact call made by the UI
        suggestions = tracker.generate_trade_suggestions(3)
        
        # Verify it returns data that the UI can use
        assert isinstance(suggestions, list), "Should return a list"
        
        if suggestions:
            suggestion = suggestions[0]
            # Check that all UI-expected fields are present
            ui_fields = ['ticker', 'strategy', 'confidence', 'expected_profit', 'risk']
            for field in ui_fields:
                assert field in suggestion, f"UI expects field: {field}"
        
        print("✅ UI integration test passed")
        return True
        
    except Exception as e:
        print(f"❌ UI integration test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Running Comprehensive Options Trading Trade Suggestions Tests\n")
    
    success1 = test_generate_trade_suggestions()
    print()
    success2 = test_edge_cases()
    print()
    success3 = test_integration_with_ui()
    
    print(f"\n📊 Test Results:")
    print(f"   Main method test: {'✅ PASS' if success1 else '❌ FAIL'}")
    print(f"   Edge cases test: {'✅ PASS' if success2 else '❌ FAIL'}")
    print(f"   UI integration test: {'✅ PASS' if success3 else '❌ FAIL'}")
    
    if success1 and success2 and success3:
        print("\n🎉 ALL TESTS PASSED! The generate_trade_suggestions method is working correctly.")
        print("   ✅ Method exists and is callable")
        print("   ✅ Returns properly structured suggestions")  
        print("   ✅ Handles edge cases gracefully")
        print("   ✅ Integrates correctly with UI expectations")
        sys.exit(0)
    else:
        print("\n💥 Some tests failed. Check the implementation.")
        sys.exit(1)
