#!/usr/bin/env python3
"""
Test script to verify all Portfolio Suite components load correctly
"""

import sys
import os
import traceback

def test_component_imports():
    """Test importing all major components"""
    
    print("🧪 Testing Portfolio Suite Component Imports")
    print("=" * 50)
    
    # Test 1: Options Trading
    print("\n1. Testing Options Trading Module...")
    try:
        from portfolio_suite.options_trading import OptionsTracker, run_options_ui
        print("   ✅ OptionsTracker imported successfully")
        print("   ✅ run_options_ui imported successfully")
        
        # Test creating an instance
        tracker = OptionsTracker()
        print("   ✅ OptionsTracker instance created successfully")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        traceback.print_exc()
    
    # Test 2: Tactical Tracker  
    print("\n2. Testing Tactical Tracker Module...")
    try:
        from portfolio_suite.tactical_tracker import run_tactical_tracker
        print("   ✅ run_tactical_tracker imported successfully")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        traceback.print_exc()
    
    # Test 3: Trade Analysis
    print("\n3. Testing Trade Analysis Module...")
    try:
        from portfolio_suite.trade_analysis import run_trade_analysis
        from portfolio_suite.trade_analysis.ui import run_analysis_ui
        print("   ✅ run_trade_analysis imported successfully")
        print("   ✅ run_analysis_ui imported successfully")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        traceback.print_exc()
    
    # Test 4: Main UI
    print("\n4. Testing Main UI Module...")
    try:
        from portfolio_suite.ui.main_app import show_options_trading, show_tactical_tracker, show_trade_analysis
        print("   ✅ show_options_trading imported successfully")
        print("   ✅ show_tactical_tracker imported successfully")
        print("   ✅ show_trade_analysis imported successfully")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        traceback.print_exc()
    
    print("\n" + "=" * 50)
    print("🎉 Import test completed!")

if __name__ == "__main__":
    test_component_imports()
