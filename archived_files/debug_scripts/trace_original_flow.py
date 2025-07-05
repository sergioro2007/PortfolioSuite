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

def trace_original_flow():
    """Trace the exact flow in the original app to identify the ETF issue."""
    
    print("=== TRACING ORIGINAL APP FLOW ===")
    
    # Initialize the original tracker
    tracker = PortfolioTracker()
    
    print("\n1. Getting discovered tickers...")
    # Get the discovered tickers (this should match what auto-discovery does)
    discovered_tickers = tracker.get_discovered_tickers()
    print(f"Discovered tickers count: {len(discovered_tickers)}")
    print(f"First 20 discovered tickers: {discovered_tickers[:20]}")
    
    # Check if ARKK and ARKQ are in the discovered list
    etfs_to_check = ['ARKK', 'ARKQ']
    for etf in etfs_to_check:
        if etf in discovered_tickers:
            print(f"✓ {etf} found in discovered tickers at position {discovered_tickers.index(etf)}")
        else:
            print(f"✗ {etf} NOT found in discovered tickers")
    
    print("\n2. Analyzing all discovered tickers...")
    
    # Track which tickers pass each filter
    filter_results = {}
    
    for ticker in discovered_tickers:
        print(f"\nAnalyzing {ticker}:")
        
        try:
            # Get ticker data
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Check market cap
            market_cap = info.get('marketCap')
            if market_cap is None:
                market_cap = 0
                print(f"  Market cap: None -> defaulting to 0")
            else:
                print(f"  Market cap: ${market_cap:,.0f} (${market_cap/1e9:.1f}B)")
            
            # Check if it passes the market cap filter
            market_cap_pass = market_cap >= 5e9
            print(f"  Market cap filter (>= $5B): {'PASS' if market_cap_pass else 'FAIL'}")
            
            # Get historical data for momentum analysis
            try:
                hist = stock.history(period="1y")
                if len(hist) < 50:  # Need enough data
                    print(f"  Historical data: INSUFFICIENT ({len(hist)} days)")
                    continue
                
                # Check if it passes the basic filters using the original logic
                passes = tracker.passes_filters(ticker, info, hist)
                print(f"  passes_filters(): {'PASS' if passes else 'FAIL'}")
                
                if passes:
                    # Calculate momentum score
                    momentum_data = tracker.analyze_ticker_momentum(ticker, hist)
                    if momentum_data:
                        momentum_score = momentum_data.get('momentum_score', 0)
                        print(f"  Momentum score: {momentum_score:.2f}")
                        
                        filter_results[ticker] = {
                            'market_cap': market_cap,
                            'market_cap_pass': market_cap_pass,
                            'passes_filters': passes,
                            'momentum_score': momentum_score,
                            'momentum_data': momentum_data
                        }
                    else:
                        print(f"  Momentum analysis: FAILED")
                else:
                    print(f"  Skipping momentum analysis (failed filters)")
                    
            except Exception as e:
                print(f"  Error getting historical data: {e}")
                
        except Exception as e:
            print(f"  Error analyzing {ticker}: {e}")
            
        # Only analyze first 50 tickers to avoid too much output
        if len(filter_results) >= 50:
            print(f"\n... stopping after analyzing first 50 tickers with valid data")
            break
    
    print(f"\n3. Summary of qualified tickers:")
    print(f"Total qualified tickers: {len(filter_results)}")
    
    # Check specifically for ETFs
    etf_results = {}
    for ticker in etfs_to_check:
        if ticker in filter_results:
            etf_results[ticker] = filter_results[ticker]
            print(f"\n{ticker} qualification:")
            print(f"  Market cap: ${filter_results[ticker]['market_cap']:,.0f}")
            print(f"  Market cap filter: {'PASS' if filter_results[ticker]['market_cap_pass'] else 'FAIL'}")
            print(f"  passes_filters(): {'PASS' if filter_results[ticker]['passes_filters'] else 'FAIL'}")
            print(f"  Momentum score: {filter_results[ticker]['momentum_score']:.2f}")
    
    # Get top 10 by momentum score
    qualified_tickers = [(ticker, data) for ticker, data in filter_results.items()]
    qualified_tickers.sort(key=lambda x: x[1]['momentum_score'], reverse=True)
    
    print(f"\n4. Top 10 by momentum score:")
    for i, (ticker, data) in enumerate(qualified_tickers[:10]):
        market_cap_status = "PASS" if data['market_cap_pass'] else "FAIL"
        print(f"{i+1:2d}. {ticker:6s} - Score: {data['momentum_score']:6.2f} - MarketCap: {market_cap_status}")
    
    # Now run the actual original app logic to see what it produces
    print(f"\n5. Running original app's get_top_picks()...")
    try:
        top_picks = tracker.get_top_picks(discovered_tickers)
        print(f"Original app top picks count: {len(top_picks) if top_picks else 0}")
        
        if top_picks:
            print("Original app top 10:")
            for i, pick in enumerate(top_picks[:10]):
                ticker = pick.get('ticker', 'Unknown')
                score = pick.get('momentum_score', 0)
                print(f"{i+1:2d}. {ticker:6s} - Score: {score:6.2f}")
                
                # Check if this ticker should have been filtered out
                if ticker in filter_results:
                    if not filter_results[ticker]['market_cap_pass']:
                        print(f"    ⚠️  WARNING: {ticker} has market cap < $5B but appears in top 10!")
        
    except Exception as e:
        print(f"Error running original app logic: {e}")
    
    return filter_results, etf_results

if __name__ == "__main__":
    results, etf_results = trace_original_flow()
    
    print(f"\n=== FINAL ANALYSIS ===")
    print(f"Total tickers analyzed: {len(results)}")
    print(f"ETFs found in results: {len(etf_results)}")
    
    for ticker, data in etf_results.items():
        print(f"\n{ticker}:")
        print(f"  Market cap: ${data['market_cap']:,.0f} ({'PASS' if data['market_cap_pass'] else 'FAIL'} $5B filter)")
        print(f"  passes_filters(): {'PASS' if data['passes_filters'] else 'FAIL'}")
        print(f"  Momentum score: {data['momentum_score']:.2f}")
        
        if not data['market_cap_pass'] and data['passes_filters']:
            print(f"  🔍 INVESTIGATION NEEDED: {ticker} failed market cap but passed filters!")
