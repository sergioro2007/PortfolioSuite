#!/usr/bin/env python3
"""
Test script to check for non-deterministic behavior in tactical tracker
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.tactical_tracker import PortfolioTracker, discover_momentum_tickers, screen_discovered_tickers

def test_deterministic_behavior():
    """Test if the tactical tracker produces consistent results"""
    print("🔍 Testing Tactical Tracker Deterministic Behavior")
    print("=" * 60)
    
    # Create tracker
    tracker = PortfolioTracker()
    
    # Test parameters
    min_rs_score = 30.0
    min_weekly_target = 1.5
    market_health = {'defensive_score': 0}  # No defensive mode
    
    print("🎯 Running 3 consecutive screenings with same parameters...")
    print(f"Parameters: RS Score >= {min_rs_score}, Weekly Return >= {min_weekly_target}%")
    print()
    
    results_list = []
    
    for run in range(3):
        print(f"Run #{run + 1}:")
        
        # Discover tickers
        discovered_tickers = discover_momentum_tickers()
        print(f"  📊 Discovered {len(discovered_tickers)} tickers")
        
        # Screen tickers
        results = screen_discovered_tickers(tracker, discovered_tickers, min_rs_score, min_weekly_target, market_health)
        print(f"  ✅ {len(results)} qualified tickers")
        
        # Get top picks
        top_picks = tracker.get_top_picks(results, 10, min_rs_score, min_weekly_target)
        print(f"  🎯 Top {len(top_picks)} picks:")
        
        # Show top 5 tickers
        for i, pick in enumerate(top_picks[:5]):
            print(f"    #{i+1}: {pick['ticker']} (Score: {pick['momentum_score']:.1f}, Avg: {pick['avg_weekly_return']:.2f}%)")
        
        results_list.append(top_picks)
        print()
    
    # Compare results
    print("🔍 Comparison Analysis:")
    print("-" * 40)
    
    # Check if top 5 are the same
    if len(results_list) >= 2:
        run1_top5 = [r['ticker'] for r in results_list[0][:5]]
        run2_top5 = [r['ticker'] for r in results_list[1][:5]]
        
        print(f"Run 1 Top 5: {run1_top5}")
        print(f"Run 2 Top 5: {run2_top5}")
        
        if run1_top5 == run2_top5:
            print("✅ CONSISTENT: Top 5 tickers are identical")
        else:
            print("❌ INCONSISTENT: Top 5 tickers differ!")
            print(f"   Different tickers: {set(run1_top5) ^ set(run2_top5)}")
        
        # Check if orders match
        if len(results_list) >= 3:
            run3_top5 = [r['ticker'] for r in results_list[2][:5]]
            print(f"Run 3 Top 5: {run3_top5}")
            
            if run1_top5 == run2_top5 == run3_top5:
                print("✅ ALL CONSISTENT: All 3 runs produced identical results")
            else:
                print("❌ INCONSISTENT: Results vary between runs")
    
    print()
    print("🔍 Detailed Analysis:")
    print("-" * 40)
    
    # Check for any differences in scores or ordering
    if len(results_list) >= 2:
        for i in range(min(5, len(results_list[0]), len(results_list[1]))):
            r1 = results_list[0][i]
            r2 = results_list[1][i]
            
            if r1['ticker'] != r2['ticker']:
                print(f"  Position #{i+1}: {r1['ticker']} vs {r2['ticker']} - DIFFERENT!")
            elif abs(r1['momentum_score'] - r2['momentum_score']) > 0.01:
                print(f"  {r1['ticker']}: Score {r1['momentum_score']:.2f} vs {r2['momentum_score']:.2f} - SCORE CHANGED!")
            else:
                print(f"  {r1['ticker']}: ✅ Consistent")

if __name__ == "__main__":
    test_deterministic_behavior()
