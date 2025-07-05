#!/usr/bin/env python3
"""
Ranking Comparison: Analyze differences in top 10 rankings between apps
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from streamlit_app import PortfolioTracker as OriginalTracker
from tactical_tracker import PortfolioTracker as NewTracker
import pandas as pd

def compare_rankings():
    """Compare the top 10 rankings between both trackers"""
    print("🔍 RANKING COMPARISON ANALYSIS")
    print("=" * 60)
    
    # Initialize both trackers
    original = OriginalTracker()
    new = NewTracker()
    
    # Test parameters
    min_rs_score = 30
    min_weekly_target = 1.5
    
    # Default ticker list (same as both apps use)
    default_tickers = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA", "SPY", "QQQ", "IWM"]
    
    print(f"📋 Analyzing tickers: {default_tickers}")
    print(f"🎯 Parameters: RS Score >= {min_rs_score}, Weekly Target >= {min_weekly_target}")
    print()
    
    # Get results from both trackers
    print("1️⃣ Getting results from ORIGINAL tracker...")
    original_results = []
    for ticker in default_tickers:
        try:
            ticker_data = original.get_ticker_data(ticker)
            if original.passes_filters(ticker_data, min_rs_score, min_weekly_target):
                momentum_score = original.calculate_momentum_score(ticker_data)
                original_results.append({
                    'ticker': ticker,
                    'momentum_score': momentum_score,
                    'weekly_return': ticker_data.get('weekly_return', 0),
                    'rs_score': ticker_data.get('rs_score', 0)
                })
        except Exception as e:
            print(f"   ❌ Error processing {ticker} in original: {e}")
    
    print("2️⃣ Getting results from NEW tracker...")
    new_results = []
    for ticker in default_tickers:
        try:
            ticker_data = new.get_ticker_data(ticker)
            if new.passes_filters(ticker_data, min_rs_score, min_weekly_target):
                momentum_score = new.calculate_momentum_score(ticker_data)
                new_results.append({
                    'ticker': ticker,
                    'momentum_score': momentum_score,
                    'weekly_return': ticker_data.get('weekly_return', 0),
                    'rs_score': ticker_data.get('rs_score', 0)
                })
        except Exception as e:
            print(f"   ❌ Error processing {ticker} in new: {e}")
    
    # Sort by momentum score (descending)
    original_sorted = sorted(original_results, key=lambda x: x['momentum_score'], reverse=True)
    new_sorted = sorted(new_results, key=lambda x: x['momentum_score'], reverse=True)
    
    print("\n3️⃣ RANKING COMPARISON")
    print("-" * 60)
    
    # Show top 10 from each
    print("🥇 ORIGINAL TRACKER - Top 10:")
    for i, result in enumerate(original_sorted[:10], 1):
        print(f"   {i:2d}. {result['ticker']:5s} - Score: {result['momentum_score']:6.2f} | Weekly: {result['weekly_return']:6.2f}% | RS: {result['rs_score']:6.2f}")
    
    print("\n🥈 NEW TRACKER - Top 10:")
    for i, result in enumerate(new_sorted[:10], 1):
        print(f"   {i:2d}. {result['ticker']:5s} - Score: {result['momentum_score']:6.2f} | Weekly: {result['weekly_return']:6.2f}% | RS: {result['rs_score']:6.2f}")
    
    # Check for differences
    print("\n4️⃣ RANKING DIFFERENCES ANALYSIS")
    print("-" * 60)
    
    # Create ranking dictionaries
    original_ranks = {result['ticker']: i+1 for i, result in enumerate(original_sorted)}
    new_ranks = {result['ticker']: i+1 for i, result in enumerate(new_sorted)}
    
    # Find common tickers
    common_tickers = set(original_ranks.keys()) & set(new_ranks.keys())
    
    if not common_tickers:
        print("❌ NO COMMON TICKERS FOUND!")
        return
    
    differences_found = False
    for ticker in sorted(common_tickers):
        orig_rank = original_ranks[ticker]
        new_rank = new_ranks[ticker]
        
        if orig_rank != new_rank:
            differences_found = True
            print(f"📊 {ticker}: Original #{orig_rank} vs New #{new_rank} (diff: {new_rank - orig_rank:+d})")
    
    if not differences_found:
        print("✅ All rankings are IDENTICAL!")
    else:
        print("\n5️⃣ DETAILED SCORE COMPARISON")
        print("-" * 60)
        
        # Compare scores for different rankings
        for ticker in sorted(common_tickers):
            orig_rank = original_ranks[ticker]
            new_rank = new_ranks[ticker]
            
            if orig_rank != new_rank:
                # Find the actual scores
                orig_score = next(r['momentum_score'] for r in original_results if r['ticker'] == ticker)
                new_score = next(r['momentum_score'] for r in new_results if r['ticker'] == ticker)
                
                print(f"🔍 {ticker}:")
                print(f"   Original: Rank #{orig_rank}, Score: {orig_score:.6f}")
                print(f"   New:      Rank #{new_rank}, Score: {new_score:.6f}")
                print(f"   Score diff: {new_score - orig_score:+.6f}")
                print()

if __name__ == "__main__":
    compare_rankings()
