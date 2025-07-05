#!/usr/bin/env python3
"""
Test Ranking Order Fix
=====================

This script tests that the new app now produces the same ranking order as the original.
"""

import sys
import os

# Import tactical tracker
sys.path.append('/Users/soliv112/PersonalProjects/Test')
from tactical_tracker import PortfolioTracker, discover_momentum_tickers, screen_discovered_tickers

def test_ranking_fix():
    """Test the ranking order to match original app"""
    
    print("🔍 Testing Ranking Order Fix")
    print("=" * 50)
    
    # Initialize tracker
    tracker = PortfolioTracker()
    
    # Auto-discovery settings (matching what users typically use)
    min_rs_score = 25
    min_weekly_target = 1.0
    
    print(f"Testing with: RS >= {min_rs_score}, Weekly >= {min_weekly_target}%")
    
    # Get market health
    market_health = tracker.get_market_health()
    
    # Discover and screen tickers
    discovered_tickers = discover_momentum_tickers()
    qualified_results = screen_discovered_tickers(
        tracker, discovered_tickers, min_rs_score, min_weekly_target, market_health
    )
    
    # Generate recommendations (this now uses get_top_picks internally)
    recommendations = tracker.generate_portfolio_recommendations(
        qualified_results, 10, min_rs_score, min_weekly_target, market_health
    )
    
    # Get the top picks (should now be sorted by momentum score)
    top_picks = recommendations.get('top_picks', [])
    
    print(f"\n✅ Found {len(top_picks)} top picks")
    
    if top_picks:
        print("\n🏆 New App Ranking (should match original):")
        for i, pick in enumerate(top_picks, 1):
            print(f"#{i}\t{pick['ticker']}\t(Score: {pick['momentum_score']:.1f}, Weekly: {pick['avg_weekly_return']:.1f}%)")
        
        print("\n📊 Expected Original Ranking:")
        expected = ["DDOG", "C", "AXP", "CAT", "FDX", "CMG", "BAC", "CRWD", "BLK", "AMD"]
        for i, ticker in enumerate(expected, 1):
            print(f"#{i}\t{ticker}")
        
        print("\n🔍 Comparison:")
        new_tickers = [pick['ticker'] for pick in top_picks]
        matches = 0
        for i, (new, expected_ticker) in enumerate(zip(new_tickers, expected)):
            match_status = "✅" if new == expected_ticker else "❌"
            print(f"  Position {i+1}: {new} vs {expected_ticker} {match_status}")
            if new == expected_ticker:
                matches += 1
        
        accuracy = (matches / min(len(new_tickers), len(expected))) * 100
        print(f"\n📈 Ranking Accuracy: {matches}/{min(len(new_tickers), len(expected))} ({accuracy:.1f}%)")
        
        if accuracy >= 90:
            print("🎉 SUCCESS: Rankings are very close to original!")
        elif accuracy >= 70:
            print("⚠️  PARTIAL: Rankings are mostly correct but some differences remain")
        else:
            print("❌ ISSUE: Rankings still differ significantly from original")
            
        return accuracy >= 70
    else:
        print("❌ No top picks found!")
        return False

if __name__ == "__main__":
    print("🎯 Testing Ranking Order Fix")
    print("=" * 60)
    
    success = test_ranking_fix()
    
    print(f"\n{'='*60}")
    if success:
        print("🎉 RANKING FIX SUCCESSFUL!")
    else:
        print("⚠️  Ranking fix needs more work")
    print("🏁 Test Complete")
