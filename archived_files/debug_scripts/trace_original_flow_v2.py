#!/usr/bin/env python3
"""
Trace the exact flow in the original streamlit_app.py to understand
why ETFs like ARKK and ARKQ appear in the top 10 despite having $0B market cap.
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

# Import the original app components
from streamlit_app import PortfolioTracker

def trace_original_auto_discovery():
    """Trace the exact auto-discovery flow in the original app."""
    
    print("=== TRACING ORIGINAL AUTO-DISCOVERY FLOW ===")
    
    # Initialize the original tracker
    tracker = PortfolioTracker()
    
    print("\n1. Getting market health...")
    market_health = tracker.get_market_health()
    print(f"Market health: {market_health}")
    
    print("\n2. Discovering momentum tickers...")
    # This is what the original app calls
    discovered_tickers = tracker.discover_momentum_tickers()
    print(f"Discovered tickers count: {len(discovered_tickers)}")
    print(f"First 20 discovered tickers: {discovered_tickers[:20]}")
    
    # Check if ARKK and ARKQ are in the discovered list
    etfs_to_check = ['ARKK', 'ARKQ']
    for etf in etfs_to_check:
        if etf in discovered_tickers:
            print(f"✓ {etf} found in discovered tickers at position {discovered_tickers.index(etf)}")
        else:
            print(f"✗ {etf} NOT found in discovered tickers")
    
    print("\n3. Screening discovered tickers...")
    # Use the same parameters as the original app defaults
    min_rs_score = 25  # Default from original app
    min_weekly_target = 1.0  # Default from original app
    
    # This is the key method that does the screening
    qualified_results = tracker.screen_discovered_tickers(
        discovered_tickers, 
        min_rs_score, 
        min_weekly_target, 
        market_health
    )
    
    print(f"Qualified results count: {len(qualified_results) if qualified_results else 0}")
    
    if qualified_results:
        print(f"\nQualified tickers:")
        for i, result in enumerate(qualified_results[:20]):  # Show first 20
            ticker = result.get('ticker', 'Unknown')
            score = result.get('momentum_score', 0)
            rs_score = result.get('rs_score', 0)
            weekly_return = result.get('weekly_return', 0)
            market_cap = result.get('market_cap', 0)
            print(f"{i+1:2d}. {ticker:6s} - Score: {score:6.2f} - RS: {rs_score:4.1f} - Weekly: {weekly_return:5.2f}% - Cap: ${market_cap/1e9:.1f}B")
            
            # Flag ETFs
            if ticker in etfs_to_check:
                print(f"    🎯 ETF {ticker} QUALIFIED! Market cap: ${market_cap/1e9:.1f}B")
        
        print(f"\n4. Getting top picks...")
        # This is what get_top_picks does - it sorts by momentum_score
        top_picks = tracker.get_top_picks(qualified_results, 10, min_rs_score, min_weekly_target)
        
        if top_picks:
            print(f"Top 10 picks from original app:")
            for i, pick in enumerate(top_picks):
                ticker = pick.get('ticker', 'Unknown')
                score = pick.get('momentum_score', 0)
                market_cap = pick.get('market_cap', 0)
                print(f"{i+1:2d}. {ticker:6s} - Score: {score:6.2f} - Cap: ${market_cap/1e9:.1f}B")
                
                # Flag ETFs in top 10
                if ticker in etfs_to_check:
                    print(f"    🚨 ETF {ticker} IN TOP 10! Market cap: ${market_cap/1e9:.1f}B")
        
        # Check specifically for ETFs
        etf_in_qualified = [r for r in qualified_results if r.get('ticker') in etfs_to_check]
        if etf_in_qualified:
            print(f"\n5. ETF Analysis:")
            for etf in etf_in_qualified:
                ticker = etf.get('ticker')
                market_cap = etf.get('market_cap', 0)
                print(f"\n{ticker} details:")
                print(f"  Market cap: ${market_cap:,.0f} (${market_cap/1e9:.1f}B)")
                print(f"  RS Score: {etf.get('rs_score', 0):.2f}")
                print(f"  Weekly Return: {etf.get('weekly_return', 0):.2f}%")
                print(f"  Momentum Score: {etf.get('momentum_score', 0):.2f}")
                print(f"  Volume: {etf.get('avg_volume', 0):,.0f}")
                
                # Check if this should have been filtered out by market cap
                min_market_cap = 5e9  # $5B threshold
                if market_cap < min_market_cap:
                    print(f"  ⚠️  WARNING: Market cap ${market_cap/1e9:.1f}B < ${min_market_cap/1e9:.0f}B threshold!")
                    print(f"      But {ticker} still qualified - investigating why...")
                    
                    # Let's check what the screening logic actually does
                    print(f"      Let's trace the screening logic for {ticker}...")
    
    return qualified_results

def check_etf_directly():
    """Check ETF data directly to understand the market cap issue."""
    
    print("\n=== DIRECT ETF CHECK ===")
    
    etfs = ['ARKK', 'ARKQ']
    
    for ticker in etfs:
        print(f"\nChecking {ticker} directly:")
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Check various market cap fields
            market_cap = info.get('marketCap')
            total_assets = info.get('totalAssets')
            nav = info.get('navPrice')
            shares_outstanding = info.get('sharesOutstanding')
            float_shares = info.get('floatShares')
            
            print(f"  marketCap: {market_cap}")
            print(f"  totalAssets: {total_assets}")
            print(f"  navPrice: {nav}")
            print(f"  sharesOutstanding: {shares_outstanding}")
            print(f"  floatShares: {float_shares}")
            
            # What would the original app see?
            if market_cap is None:
                effective_market_cap = 0
                print(f"  Original app would see: ${effective_market_cap} (None -> 0)")
            else:
                effective_market_cap = market_cap
                print(f"  Original app would see: ${effective_market_cap:,.0f}")
                
            # Check if it's above the threshold
            threshold = 5e9  # $5B
            passes_market_cap = effective_market_cap >= threshold
            print(f"  Passes $5B threshold: {passes_market_cap}")
            
        except Exception as e:
            print(f"  Error: {e}")

if __name__ == "__main__":
    # Check ETFs directly first
    check_etf_directly()
    
    # Then trace the full flow
    results = trace_original_auto_discovery()
    
    print(f"\n=== SUMMARY ===")
    if results:
        etf_results = [r for r in results if r.get('ticker') in ['ARKK', 'ARKQ']]
        if etf_results:
            print(f"ETFs found in qualified results: {len(etf_results)}")
            for etf in etf_results:
                ticker = etf.get('ticker')
                market_cap = etf.get('market_cap', 0)
                print(f"  {ticker}: ${market_cap/1e9:.1f}B market cap")
        else:
            print("No ETFs found in qualified results")
    else:
        print("No qualified results found")
