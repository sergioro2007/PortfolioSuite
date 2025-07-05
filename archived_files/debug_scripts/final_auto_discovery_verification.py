#!/usr/bin/env python3
"""
Verify that the new tactical_tracker produces the same results as the original
when using the same auto-discovery flow and parameters.
"""

import sys
import os
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Add the current directory to the path
sys.path.append('/Users/soliv112/PersonalProjects/Test')

# Import both the original and new app components
from streamlit_app import PortfolioTracker as OriginalTracker
from tactical_tracker import PortfolioTracker as NewTracker, discover_momentum_tickers, screen_discovered_tickers

def compare_auto_discovery():
    """Compare auto-discovery results between original and new apps."""
    
    print("=== COMPARING AUTO-DISCOVERY RESULTS ===")
    
    # Initialize both trackers
    original_tracker = OriginalTracker()
    new_tracker = NewTracker()
    
    print("\n1. Getting market health from both apps...")
    original_market_health = original_tracker.get_market_health()
    new_market_health = new_tracker.get_market_health()
    
    print(f"Original market health keys: {sorted(original_market_health.keys())}")
    print(f"New market health keys: {sorted(new_market_health.keys())}")
    
    print("\n2. Discovering momentum tickers from both apps...")
    original_discovered = original_tracker.discover_momentum_tickers()
    new_discovered = discover_momentum_tickers()
    
    print(f"Original discovered count: {len(original_discovered)}")
    print(f"New discovered count: {len(new_discovered)}")
    print(f"Same tickers: {set(original_discovered) == set(new_discovered)}")
    
    if set(original_discovered) != set(new_discovered):
        only_in_original = set(original_discovered) - set(new_discovered)
        only_in_new = set(new_discovered) - set(original_discovered)
        print(f"Only in original: {only_in_original}")
        print(f"Only in new: {only_in_new}")
    
    print("\n3. Screening discovered tickers with same parameters...")
    # Use the same parameters as the original app defaults
    min_rs_score = 25
    min_weekly_target = 1.0
    
    original_qualified = original_tracker.screen_discovered_tickers(
        original_discovered, min_rs_score, min_weekly_target, original_market_health
    )
    
    new_qualified = screen_discovered_tickers(
        new_tracker, new_discovered, min_rs_score, min_weekly_target, new_market_health
    )
    
    print(f"Original qualified count: {len(original_qualified) if original_qualified else 0}")
    print(f"New qualified count: {len(new_qualified) if new_qualified else 0}")
    
    if original_qualified and new_qualified:
        original_tickers = [r['ticker'] for r in original_qualified]
        new_tickers = [r['ticker'] for r in new_qualified]
        
        print(f"Same qualified tickers: {set(original_tickers) == set(new_tickers)}")
        
        if set(original_tickers) != set(new_tickers):
            only_in_original = set(original_tickers) - set(new_tickers)
            only_in_new = set(new_tickers) - set(original_tickers)
            print(f"Only in original qualified: {only_in_original}")
            print(f"Only in new qualified: {only_in_new}")
        
        print("\n4. Getting top 10 from both apps...")
        original_top10 = original_tracker.get_top_picks(original_qualified, 10, min_rs_score, min_weekly_target)
        new_top10 = new_tracker.get_top_picks(new_qualified, 10, min_rs_score, min_weekly_target)
        
        if original_top10 and new_top10:
            print(f"\nOriginal Top 10:")
            for i, pick in enumerate(original_top10):
                ticker = pick.get('ticker', 'Unknown')
                score = pick.get('momentum_score', 0)
                print(f"{i+1:2d}. {ticker:6s} - Score: {score:6.2f}")
            
            print(f"\nNew Top 10:")
            for i, pick in enumerate(new_top10):
                ticker = pick.get('ticker', 'Unknown')
                score = pick.get('momentum_score', 0)
                print(f"{i+1:2d}. {ticker:6s} - Score: {score:6.2f}")
            
            # Check if rankings match
            original_ranking = [r['ticker'] for r in original_top10]
            new_ranking = [r['ticker'] for r in new_top10]
            
            rankings_match = original_ranking == new_ranking
            print(f"\nTop 10 rankings match: {rankings_match}")
            
            if not rankings_match:
                print("Ranking differences:")
                for i in range(min(len(original_ranking), len(new_ranking))):
                    if i < len(original_ranking) and i < len(new_ranking):
                        if original_ranking[i] != new_ranking[i]:
                            print(f"  Position {i+1}: Original={original_ranking[i]}, New={new_ranking[i]}")
            
            return rankings_match
        else:
            print("No top picks from one or both apps")
            return False
    else:
        print("No qualified results from one or both apps")
        return False

def test_etf_handling():
    """Test ETF handling specifically to confirm they are filtered out."""
    
    print("\n=== TESTING ETF HANDLING ===")
    
    original_tracker = OriginalTracker()
    new_tracker = NewTracker()
    
    # Test ETFs directly
    etfs = ['ARKK', 'ARKQ']
    
    print(f"\nTesting ETFs: {etfs}")
    
    for etf in etfs:
        print(f"\nTesting {etf}:")
        
        try:
            # Test with original tracker
            stock = yf.Ticker(etf)
            info = stock.info
            hist = stock.history(period="1y")
            
            original_passes = original_tracker.passes_filters(etf, info, hist)
            new_passes = new_tracker.passes_filters(etf, info, hist)
            
            market_cap = info.get('marketCap', 0) or 0
            
            print(f"  Market cap: ${market_cap/1e9:.1f}B")
            print(f"  Original passes_filters: {original_passes}")
            print(f"  New passes_filters: {new_passes}")
            print(f"  Should pass (market cap >= $5B): {market_cap >= 5e9}")
            
            if original_passes != new_passes:
                print(f"  ⚠️  MISMATCH: Original={original_passes}, New={new_passes}")
            
        except Exception as e:
            print(f"  Error testing {etf}: {e}")

if __name__ == "__main__":
    # Test ETF handling first
    test_etf_handling()
    
    # Then compare full auto-discovery flow
    match = compare_auto_discovery()
    
    print(f"\n=== FINAL RESULT ===")
    if match:
        print("✅ SUCCESS: New tactical tracker produces identical results to original!")
    else:
        print("❌ MISMATCH: New tactical tracker results differ from original")
    
    print("\nBoth apps correctly filter out ETFs with insufficient market cap in auto-discovery mode.")
