#!/usr/bin/env python3
"""
Final Auto-Discovery Comparison Test
===================================

This script compares auto-discovery results between the original and new apps.
"""

import sys
import os
from typing import Dict, List

# Import both apps
sys.path.append('/Users/soliv112/PersonalProjects/Test')

# Import from original streamlit app
import streamlit_app

# Import from new tactical tracker
from tactical_tracker import PortfolioTracker, discover_momentum_tickers, screen_discovered_tickers

def compare_auto_discovery():
    """Compare auto-discovery between original and new versions"""
    
    print("🔍 Auto-Discovery Comparison Test")
    print("=" * 60)
    
    # Test settings
    min_rs_score = 25
    min_weekly_target = 1.0
    
    print(f"Testing with: RS >= {min_rs_score}, Weekly >= {min_weekly_target}%")
    
    # Initialize trackers
    original_tracker = streamlit_app.PortfolioTracker()
    new_tracker = PortfolioTracker()
    
    print("\n1. Comparing ticker discovery...")
    
    # Test original discovery
    print("   🔸 Original app discovery:")
    try:
        original_tickers = original_tracker.discover_momentum_tickers()
        print(f"      Found {len(original_tickers)} tickers")
        print(f"      Sample: {original_tickers[:5]}")
    except Exception as e:
        print(f"      Error: {e}")
        original_tickers = []
    
    # Test new discovery  
    print("   🔸 New app discovery:")
    try:
        new_tickers = discover_momentum_tickers()
        print(f"      Found {len(new_tickers)} tickers")
        print(f"      Sample: {new_tickers[:5]}")
    except Exception as e:
        print(f"      Error: {e}")
        new_tickers = []
    
    print("\n2. Comparing screening results...")
    
    # Test original screening
    print("   🔸 Original app screening:")
    try:
        market_health = original_tracker.get_market_health()
        original_qualified = original_tracker.screen_discovered_tickers(
            original_tickers, min_rs_score, min_weekly_target, market_health
        )
        print(f"      Qualified: {len(original_qualified)} stocks")
        if original_qualified:
            print(f"      Top 3: {[t['ticker'] for t in original_qualified[:3]]}")
    except Exception as e:
        print(f"      Error: {e}")
        original_qualified = []
    
    # Test new screening
    print("   🔸 New app screening:")
    try:
        market_health = new_tracker.get_market_health()
        new_qualified = screen_discovered_tickers(
            new_tracker, new_tickers, min_rs_score, min_weekly_target, market_health
        )
        print(f"      Qualified: {len(new_qualified)} stocks")
        if new_qualified:
            print(f"      Top 3: {[t['ticker'] for t in new_qualified[:3]]}")
    except Exception as e:
        print(f"      Error: {e}")
        new_qualified = []
    
    print("\n3. Summary:")
    print(f"   Original: {len(original_tickers)} discovered → {len(original_qualified)} qualified")
    print(f"   New:      {len(new_tickers)} discovered → {len(new_qualified)} qualified")
    
    # Check if we have a reasonable number of qualified stocks
    success = len(new_qualified) >= 10  # Should find at least 10 good stocks
    
    if success:
        print(f"\n✅ SUCCESS: New auto-discovery found {len(new_qualified)} qualifying stocks!")
        print("   Auto-discovery issue has been resolved.")
    else:
        print(f"\n❌ ISSUE: New auto-discovery only found {len(new_qualified)} qualifying stocks.")
        print("   This may still be too few for good portfolio selection.")
    
    return success, len(new_qualified)

if __name__ == "__main__":
    print("🎯 Final Auto-Discovery Comparison")
    print("=" * 70)
    
    success, count = compare_auto_discovery()
    
    print(f"\n{'='*70}")
    if success:
        print(f"🎉 AUTO-DISCOVERY FIXED! Found {count} qualifying stocks.")
    else:
        print(f"⚠️  Auto-discovery needs more work. Only {count} stocks found.")
    print("🏁 Test Complete")
