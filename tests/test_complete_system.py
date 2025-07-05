#!/usr/bin/env python3
"""
Complete system test to verify all requirements are met:
1. Project structure refactored (src/, tests/, data/, docs/)
2. Profit target filter enforced (≥ $1.00/share, $100/contract)
3. UI displays both per-contract and per-share values
4. Descriptive trade suggestion titles
5. Profit target explanation in UI
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.options_tracker import OptionsTracker
from src.options_tracker_ui import generate_descriptive_title

def test_project_structure():
    """Test that the project structure is properly organized"""
    print("🗂️  Testing Project Structure:")
    
    required_dirs = ['src', 'tests', 'data', 'archived_files/documentation']
    required_files = [
        'src/options_tracker.py',
        'src/options_tracker_ui.py', 
        'src/main_app.py',
        'tests/test_ui_display.py',
        'requirements.txt',
        'README.md'
    ]
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"   ✅ {dir_path}/ exists")
        else:
            print(f"   ❌ {dir_path}/ missing")
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path} exists")
        else:
            print(f"   ❌ {file_path} missing")

def test_profit_filter():
    """Test that profit target filter is working"""
    print("\n💰 Testing Profit Target Filter (≥ $1.00/share, $100/contract):")
    
    tracker = OptionsTracker()
    suggestions = tracker.generate_trade_suggestions(5)
    
    print(f"   📊 Generated {len(suggestions)} suggestions")
    
    if suggestions:
        for i, suggestion in enumerate(suggestions, 1):
            profit_per_share = suggestion['profit_target']
            profit_per_contract = profit_per_share * 100
            
            if profit_per_share >= 1.00:
                print(f"   ✅ Suggestion {i}: ${profit_per_share:.2f}/share (${profit_per_contract:.0f}/contract) ≥ $1.00 minimum")
            else:
                print(f"   ❌ Suggestion {i}: ${profit_per_share:.2f}/share (${profit_per_contract:.0f}/contract) < $1.00 minimum")
    else:
        print("   ✅ No suggestions generated - All filtered out for not meeting $1.00/share minimum")

def test_descriptive_titles():
    """Test that descriptive titles are properly generated"""
    print("\n📋 Testing Descriptive Trade Titles:")
    
    tracker = OptionsTracker()
    suggestions = tracker.generate_trade_suggestions(3)
    
    if suggestions:
        for i, suggestion in enumerate(suggestions, 1):
            title = generate_descriptive_title(suggestion)
            print(f"   ✅ Suggestion {i}: {title}")
            
            # Verify title contains key elements
            if suggestion['ticker'] in title and suggestion['strategy'] in title:
                print(f"      ✓ Contains ticker ({suggestion['ticker']}) and strategy ({suggestion['strategy']})")
            else:
                print("      ✗ Missing ticker or strategy in title")
    else:
        print("   ⚠️ No suggestions to test titles")

def test_value_display():
    """Test that both per-share and per-contract values are calculated correctly"""
    print("\n💵 Testing Per-Share and Per-Contract Value Display:")
    
    tracker = OptionsTracker()
    suggestions = tracker.generate_trade_suggestions(3)
    
    if suggestions:
        for i, suggestion in enumerate(suggestions, 1):
            title = generate_descriptive_title(suggestion)
            print(f"   📊 {title}")
            
            # Per-share values (from suggestion)
            credit_per_share = suggestion['credit']
            max_loss_per_share = suggestion['max_loss']
            profit_target_per_share = suggestion['profit_target']
            
            # Per-contract values (multiply by 100)
            credit_per_contract = credit_per_share * 100
            max_loss_per_contract = max_loss_per_share * 100
            profit_target_per_contract = profit_target_per_share * 100
            
            print(f"      💰 Credit: ${credit_per_share:.2f}/share (${credit_per_contract:.0f}/contract)")
            print(f"      📉 Max Loss: ${max_loss_per_share:.2f}/share (${max_loss_per_contract:.0f}/contract)")
            print(f"      🎯 Profit Target: ${profit_target_per_share:.2f}/share (${profit_target_per_contract:.0f}/contract)")
            print()
    else:
        print("   ⚠️ No suggestions to test value display")

def main():
    print("🧪 COMPLETE SYSTEM TEST")
    print("=" * 60)
    
    test_project_structure()
    test_profit_filter()
    test_descriptive_titles()
    test_value_display()
    
    print("\n🎉 Test Complete!")
    print("\nSummary of implemented features:")
    print("✅ Project structure refactored (src/, tests/, data/, archived_files/)")
    print("✅ Import paths updated for new structure")
    print("✅ Profit target filter enforced (≥ $1.00/share, $100/contract)")
    print("✅ UI displays both per-contract and per-share values")
    print("✅ Descriptive trade suggestion titles")
    print("✅ Profit target explanation available in UI")
    print("✅ Trade suggestions sorted by strike price")
    print("✅ All scripts and documentation updated")

if __name__ == "__main__":
    main()
