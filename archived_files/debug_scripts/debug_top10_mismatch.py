#!/usr/bin/env python3
"""
Debug Top 10 Mismatch: Find exactly why the new app returns different stocks
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Import both applications' classes and functions
from streamlit_app import PortfolioTracker as OriginalTracker
from tactical_tracker import PortfolioTracker as NewTracker, discover_momentum_tickers

def compare_ticker_universes():
    """Compare the ticker universes used by both apps"""
    print("🔍 Comparing Ticker Universes...")
    
    # Original app universe
    original = OriginalTracker()
    original_tickers = original.discover_momentum_tickers()
    
    # New app universe  
    new_tickers = discover_momentum_tickers()
    
    print(f"Original app tickers: {len(original_tickers)}")
    print(f"New app tickers: {len(new_tickers)}")
    
    # Find differences
    only_in_original = set(original_tickers) - set(new_tickers)
    only_in_new = set(new_tickers) - set(original_tickers)
    
    if only_in_original:
        print(f"❌ Tickers only in original: {sorted(only_in_original)}")
    if only_in_new:
        print(f"❌ Tickers only in new: {sorted(only_in_new)}")
    
    # Check specific tickers that are different
    missing_tickers = ['ADSK', 'CSCO']
    extra_tickers = ['AXP', 'CMG']
    
    print("\n🎯 Checking specific problem tickers:")
    for ticker in missing_tickers:
        in_orig = ticker in original_tickers
        in_new = ticker in new_tickers
        print(f"  {ticker}: Original={in_orig}, New={in_new}")
    
    for ticker in extra_tickers:
        in_orig = ticker in original_tickers
        in_new = ticker in new_tickers
        print(f"  {ticker}: Original={in_orig}, New={in_new}")
    
    return original_tickers, new_tickers

def compare_screening_logic():
    """Compare the screening logic for specific tickers"""
    print("\n🔍 Comparing Screening Logic...")
    
    original = OriginalTracker()
    new = NewTracker()
    
    # Test specific tickers that show differences
    test_tickers = ['ADSK', 'CSCO', 'AXP', 'CMG']
    
    for ticker in test_tickers:
        print(f"\n📊 Testing {ticker}:")
        
        try:
            # Use analyze_ticker_momentum to get the full result
            orig_result = original.analyze_ticker_momentum(ticker)
            new_result = new.analyze_ticker_momentum(ticker)
            
            if orig_result is None:
                print(f"  ❌ Original app: No result for {ticker}")
            else:
                orig_passes = original.passes_filters(orig_result)
                print(f"  Original passes: {orig_passes}, momentum: {orig_result.get('avg_weekly_return', 'N/A'):.2f}%")
            
            if new_result is None:
                print(f"  ❌ New app: No result for {ticker}")
            else:
                new_passes = new.passes_filters(new_result)
                print(f"  New passes: {new_passes}, momentum: {new_result.get('avg_weekly_return', 'N/A'):.2f}%")
            
            # Compare results if both exist
            if orig_result and new_result:
                if orig_passes != new_passes:
                    print(f"  ⚠️  FILTER MISMATCH for {ticker}!")
                elif abs(orig_result.get('avg_weekly_return', 0) - new_result.get('avg_weekly_return', 0)) > 0.01:
                    print(f"  ⚠️  MOMENTUM SCORE MISMATCH for {ticker}!")
                else:
                    print(f"  ✅ {ticker} matches between apps")
                    
        except Exception as e:
            print(f"  ❌ Error testing {ticker}: {e}")
                    
        except Exception as e:
            print(f"  ❌ Error testing {ticker}: {e}")

def compare_momentum_scoring():
    """Compare momentum scoring for specific tickers"""
    print("\n🔍 Comparing Momentum Scoring...")
    
    original = OriginalTracker()
    new = NewTracker()
    
    # Test tickers that should be in top 10
    test_tickers = ['ADSK', 'CSCO', 'AXP', 'CMG', 'DDOG', 'C', 'CAT', 'FDX', 'BAC', 'CRWD', 'BLK', 'AMD']
    
    results = []
    
    for ticker in test_tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1y")
            
            if hist.empty:
                continue
                
            # Check if passes filters in both
            orig_passes = original.passes_filters(ticker, hist)
            new_passes = new.passes_filters(ticker, hist)
            
            if not (orig_passes and new_passes):
                print(f"  ⚠️  {ticker} filter mismatch: orig={orig_passes}, new={new_passes}")
                continue
            
            # Get momentum scores
            orig_score = original.calculate_momentum_score(hist)
            new_score = new.calculate_momentum_score(hist)
            
            results.append({
                'ticker': ticker,
                'orig_score': orig_score,
                'new_score': new_score,
                'diff': abs(orig_score - new_score)
            })
            
        except Exception as e:
            print(f"  ❌ Error scoring {ticker}: {e}")
    
    # Sort by original score
    results.sort(key=lambda x: x['orig_score'], reverse=True)
    
    print("\n📊 Momentum Score Comparison (sorted by original):")
    print("Ticker | Original | New      | Diff")
    print("-" * 40)
    for r in results:
        diff_str = f"{r['diff']:.4f}" if r['diff'] > 0.001 else "✅"
        print(f"{r['ticker']:6} | {r['orig_score']:8.4f} | {r['new_score']:8.4f} | {diff_str}")

def run_full_screening_comparison():
    """Run full screening on both apps and compare results"""
    print("\n🔍 Running Full Screening Comparison...")
    
    original = OriginalTracker()
    new = NewTracker()
    
    print("Running original app screening...")
    orig_qualified = original.run_screening()
    
    print("Running new app screening...")
    new_qualified = new.run_screening()
    
    print(f"\nOriginal app qualified: {len(orig_qualified)} tickers")
    print(f"New app qualified: {len(new_qualified)} tickers")
    
    # Find differences
    orig_set = set(orig_qualified)
    new_set = set(new_qualified)
    
    only_in_orig = orig_set - new_set
    only_in_new = new_set - orig_set
    
    if only_in_orig:
        print(f"\n❌ Only in original: {sorted(only_in_orig)}")
    if only_in_new:
        print(f"❌ Only in new: {sorted(only_in_new)}")
    
    common = orig_set & new_set
    print(f"\n✅ Common qualified tickers: {len(common)}")
    
    return orig_qualified, new_qualified

def compare_final_rankings():
    """Compare the final top 10 rankings"""
    print("\n🔍 Comparing Final Rankings...")
    
    original = OriginalTracker()
    new = NewTracker()
    
    # Get qualified tickers
    orig_qualified = original.run_screening()
    new_qualified = new.run_screening()
    
    # Get momentum scores and rankings
    print("Getting original rankings...")
    orig_rankings = []
    for ticker in orig_qualified:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1y")
            score = original.calculate_momentum_score(hist)
            orig_rankings.append((ticker, score))
        except:
            continue
    
    print("Getting new rankings...")
    new_rankings = []
    for ticker in new_qualified:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1y")
            score = new.calculate_momentum_score(hist)
            new_rankings.append((ticker, score))
        except:
            continue
    
    # Sort by score
    orig_rankings.sort(key=lambda x: x[1], reverse=True)
    new_rankings.sort(key=lambda x: x[1], reverse=True)
    
    print("\n📊 Top 10 Comparison:")
    print("Rank | Original      | New")
    print("-" * 35)
    for i in range(min(10, len(orig_rankings), len(new_rankings))):
        orig_ticker, orig_score = orig_rankings[i]
        new_ticker, new_score = new_rankings[i]
        match = "✅" if orig_ticker == new_ticker else "❌"
        print(f"{i+1:4} | {orig_ticker:6} ({orig_score:.4f}) | {new_ticker:6} ({new_score:.4f}) {match}")

def main():
    print("🎯 Debug Top 10 Mismatch Analysis")
    print("=" * 60)
    
    # Step 1: Compare ticker universes
    compare_ticker_universes()
    
    # Step 2: Compare screening logic for specific tickers
    compare_screening_logic()
    
    # Step 3: Compare momentum scoring
    compare_momentum_scoring()
    
    # Step 4: Run full screening comparison
    run_full_screening_comparison()
    
    # Step 5: Compare final rankings
    compare_final_rankings()
    
    print("\n✅ Analysis complete!")

if __name__ == "__main__":
    main()
