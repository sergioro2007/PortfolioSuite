#!/usr/bin/env python3
"""
Test Enhanced Auto-Discovery
============================

This script tests the enhanced auto-discovery with the expanded ticker list.
"""

import sys
import os

# Import tactical tracker
sys.path.append('/Users/soliv112/PersonalProjects/Test')
from tactical_tracker import PortfolioTracker, discover_momentum_tickers, screen_discovered_tickers

def test_enhanced_auto_discovery():
    """Test the enhanced auto-discovery process"""
    
    print("🚀 Testing Enhanced Auto-Discovery")
    print("=" * 50)
    
    # Initialize tracker
    tracker = PortfolioTracker()
    
    # Step 1: Discover tickers
    print("\n1. Discovering tickers with enhanced list...")
    discovered_tickers = discover_momentum_tickers()
    print(f"   Total tickers discovered: {len(discovered_tickers)}")
    print(f"   First 10 tickers: {discovered_tickers[:10]}")
    print(f"   Last 10 tickers: {discovered_tickers[-10:]}")
    
    # Step 2: Test screening with lenient criteria
    print("\n2. Screening with lenient auto-discovery criteria...")
    min_rs_score = 25
    min_weekly_target = 1.0
    
    print(f"   Criteria: RS Score >= {min_rs_score}, Weekly Target >= {min_weekly_target}%")
    
    # Get market health (dummy for now)
    market_health = tracker.get_market_health()
    
    # Screen the tickers
    qualified_results = screen_discovered_tickers(
        tracker, discovered_tickers, min_rs_score, min_weekly_target, market_health
    )
    
    print(f"\n3. Results:")
    print(f"   Total tickers analyzed: {len(discovered_tickers)}")
    print(f"   Qualified tickers: {len(qualified_results)}")
    if len(discovered_tickers) > 0:
        print(f"   Qualification rate: {len(qualified_results)/len(discovered_tickers)*100:.1f}%")
    
    # Step 4: Show top qualified tickers
    if qualified_results:
        print(f"\n4. Top qualified tickers:")
        for i, result in enumerate(qualified_results[:10]):
            print(f"   {i+1}. {result['ticker']}: RS={result['rs_score']:.1f}, "
                  f"Weekly={result['avg_weekly_return']:.1f}%, "
                  f"Reason: {result['qualification_reason']}")
    
    return qualified_results

if __name__ == "__main__":
    print("🎯 Testing Enhanced Auto-Discovery")
    print("=" * 60)
    
    qualified_results = test_enhanced_auto_discovery()
    
    print(f"\n{'='*60}")
    print(f"✅ Enhanced auto-discovery found {len(qualified_results)} qualifying stocks!")
    print("🏁 Test Complete")
