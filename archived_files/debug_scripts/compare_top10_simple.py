#!/usr/bin/env python3
"""
Simple comparison script to find the exact cause of top 10 mismatch
"""
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from streamlit_app import PortfolioTracker as OriginalTracker
from tactical_tracker import PortfolioTracker as NewTracker, discover_momentum_tickers, screen_discovered_tickers

def compare_full_process():
    """Compare the complete auto-discovery process between both apps"""
    print("🔍 Running Full Auto-Discovery Comparison")
    print("=" * 60)
    
    # Initialize trackers
    original = OriginalTracker()
    new = NewTracker()
    
    # Step 1: Get discovered tickers
    print("Step 1: Getting discovered tickers...")
    original_tickers = original.discover_momentum_tickers()
    new_tickers = discover_momentum_tickers()
    
    print(f"Original discovered: {len(original_tickers)} tickers")
    print(f"New discovered: {len(new_tickers)} tickers")
    
    # Check if ticker lists are the same
    if set(original_tickers) != set(new_tickers):
        print("❌ Ticker lists differ!")
        only_orig = set(original_tickers) - set(new_tickers)
        only_new = set(new_tickers) - set(original_tickers)
        if only_orig:
            print(f"  Only in original: {only_orig}")
        if only_new:
            print(f"  Only in new: {only_new}")
    else:
        print("✅ Ticker universes match")
    
    # Step 2: Screen tickers 
    print("\nStep 2: Screening tickers...")
    try:
        # For original app - let's get the qualified results directly
        original_results = []
        for ticker in original_tickers:
            result = original.analyze_ticker_momentum(ticker)
            if result and original.passes_filters(result):
                original_results.append(result)
        
        print(f"Original qualified: {len(original_results)} tickers")
        
        # For new app - use screen_discovered_tickers with proper parameters
        market_health = new.get_market_health()
        new_results = screen_discovered_tickers(new, new_tickers, 30.0, 1.5, market_health)
        print(f"New qualified: {len(new_results)} tickers")
        
        # Step 3: Get top picks
        print("\nStep 3: Getting top picks...")
        
        # Sort original results by momentum score
        original_sorted = sorted(original_results, key=lambda x: x.get('avg_weekly_return', 0), reverse=True)
        original_top10 = original_sorted[:10]
        
        # Get top picks from new app
        new_top10 = new.get_top_picks(new_results)[:10]
        
        print("\nTop 10 comparison:")
        print("Rank | Original              | New")
        print("-" * 45)
        
        for i in range(10):
            orig_ticker = original_top10[i]['ticker'] if i < len(original_top10) else "N/A"
            orig_score = original_top10[i].get('avg_weekly_return', 0) if i < len(original_top10) else 0
            
            new_ticker = new_top10[i]['ticker'] if i < len(new_top10) else "N/A"
            new_score = new_top10[i].get('avg_weekly_return', 0) if i < len(new_top10) else 0
            
            match = "✅" if orig_ticker == new_ticker else "❌"
            
            print(f"{i+1:4d} | {orig_ticker:8s} ({orig_score:5.2f}%)  | {new_ticker:8s} ({new_score:5.2f}%) {match}")
        
        # Check if any tickers appear in only one list
        orig_tickers = {r['ticker'] for r in original_top10}
        new_tickers_set = {r['ticker'] for r in new_top10}
        
        only_in_orig = orig_tickers - new_tickers_set
        only_in_new = new_tickers_set - orig_tickers
        
        if only_in_orig:
            print(f"\n❌ Only in original top 10: {only_in_orig}")
        if only_in_new:
            print(f"❌ Only in new top 10: {only_in_new}")
        
        if not only_in_orig and not only_in_new:
            print("\n✅ Same tickers in both top 10 lists")
        
    except Exception as e:
        print(f"❌ Error in screening comparison: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    compare_full_process()
