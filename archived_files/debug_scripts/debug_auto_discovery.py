#!/usr/bin/env python3
"""
Debug Auto-Discovery Issue
==========================

This script debugs why auto-discovery is only returning one stock.
It mimics the auto-discovery process and shows detailed filtering results.
"""

import sys
import os
import logging
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
import numpy as np

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import tactical tracker
sys.path.append('/Users/soliv112/PersonalProjects/Test')
from tactical_tracker import PortfolioTracker

def debug_auto_discovery():
    """Debug the auto-discovery process step by step"""
    
    print("🔍 DEBUG: Auto-Discovery Process")
    print("=" * 50)
    
    # Initialize tracker
    tracker = PortfolioTracker()
    
    # Step 1: Discover tickers
    print("\n1. Discovering tickers...")
    discovered_tickers = discover_test_tickers()
    print(f"   Found {len(discovered_tickers)} tickers: {discovered_tickers}")
    
    # Step 2: Test with lenient criteria (auto-discovery defaults)
    print("\n2. Testing with lenient criteria (auto-discovery defaults)...")
    min_rs_score = 25
    min_weekly_target = 1.0
    
    print(f"   Criteria: RS Score >= {min_rs_score}, Weekly Target >= {min_weekly_target}%")
    
    qualified_results = []
    detailed_results = []
    
    for i, ticker in enumerate(discovered_tickers):
        print(f"\n   [{i+1}/{len(discovered_tickers)}] Analyzing {ticker}...")
        
        try:
            # Analyze the ticker
            result = tracker.analyze_ticker_momentum(ticker, min_rs_score, min_weekly_target)
            
            if result:
                meets_criteria = result.get('meets_criteria', False)
                reason = result.get('qualification_reason', 'Unknown')
                
                detailed_results.append({
                    'ticker': ticker,
                    'meets_criteria': meets_criteria,
                    'rs_score': result.get('rs_score', 0),
                    'avg_weekly_return': result.get('avg_weekly_return', 0),
                    'weekly_returns': result.get('weekly_returns', []),
                    'reason': reason
                })
                
                if meets_criteria:
                    qualified_results.append(result)
                    print(f"       ✅ QUALIFIED: {reason}")
                else:
                    print(f"       ❌ REJECTED: {reason}")
            else:
                print(f"       ⚠️  NO DATA: Could not analyze {ticker}")
                detailed_results.append({
                    'ticker': ticker,
                    'meets_criteria': False,
                    'reason': 'No data available'
                })
                
        except Exception as e:
            print(f"       💥 ERROR: {str(e)}")
            detailed_results.append({
                'ticker': ticker,
                'meets_criteria': False,
                'reason': f'Error: {str(e)}'
            })
    
    # Step 3: Summary
    print(f"\n3. Summary:")
    print(f"   Total tickers analyzed: {len(discovered_tickers)}")
    print(f"   Qualified tickers: {len(qualified_results)}")
    print(f"   Qualification rate: {len(qualified_results)/len(discovered_tickers)*100:.1f}%")
    
    # Step 4: Detailed breakdown
    print(f"\n4. Detailed breakdown:")
    qualified_count = 0
    rejected_count = 0
    error_count = 0
    
    for result in detailed_results:
        if result['meets_criteria']:
            qualified_count += 1
        elif 'Error' in result['reason'] or 'No data' in result['reason']:
            error_count += 1
        else:
            rejected_count += 1
    
    print(f"   ✅ Qualified: {qualified_count}")
    print(f"   ❌ Rejected: {rejected_count}")
    print(f"   💥 Errors: {error_count}")
    
    # Step 5: Show top qualified tickers
    if qualified_results:
        print(f"\n5. Top qualified tickers:")
        for i, result in enumerate(qualified_results[:5]):
            print(f"   {i+1}. {result['ticker']}: RS={result['rs_score']:.1f}, "
                  f"Weekly={result['avg_weekly_return']:.1f}%, "
                  f"Reason: {result['qualification_reason']}")
    
    # Step 6: Show rejection reasons
    print(f"\n6. Common rejection reasons:")
    rejection_reasons = {}
    for result in detailed_results:
        if not result['meets_criteria']:
            reason = result['reason']
            if reason not in rejection_reasons:
                rejection_reasons[reason] = 0
            rejection_reasons[reason] += 1
    
    for reason, count in sorted(rejection_reasons.items(), key=lambda x: x[1], reverse=True):
        print(f"   {reason}: {count} tickers")
    
    return qualified_results, detailed_results

def discover_test_tickers():
    """Get a test set of tickers for discovery"""
    # Use the same logic as tactical_tracker but with a smaller set for testing
    test_tickers = [
        # Major tech stocks
        'AAPL', 'MSFT', 'NVDA', 'GOOGL', 'AMZN', 'META', 'TSLA',
        # Major indices  
        'SPY', 'QQQ', 'IWM',
        # Sector ETFs
        'XLK', 'XLF', 'XLV', 'XLE', 'XLI',
        # Some momentum candidates
        'CRM', 'SNOW', 'DDOG', 'COIN', 'UBER'
    ]
    
    return test_tickers

def test_specific_ticker(ticker: str):
    """Test a specific ticker in detail"""
    
    print(f"\n🔬 DETAILED ANALYSIS: {ticker}")
    print("=" * 50)
    
    tracker = PortfolioTracker()
    
    # Test with both lenient and strict criteria
    test_cases = [
        {"name": "Lenient (Auto-Discovery)", "rs": 25, "weekly": 1.0},
        {"name": "Moderate", "rs": 30, "weekly": 1.5},
        {"name": "Strict", "rs": 40, "weekly": 2.0}
    ]
    
    for test_case in test_cases:
        print(f"\n{test_case['name']} (RS>={test_case['rs']}, Weekly>={test_case['weekly']}%):")
        
        result = tracker.analyze_ticker_momentum(ticker, test_case['rs'], test_case['weekly'])
        
        if result:
            meets_criteria = result.get('meets_criteria', False)
            reason = result.get('qualification_reason', 'Unknown')
            
            print(f"   RS Score: {result.get('rs_score', 0):.1f}")
            print(f"   Avg Weekly Return: {result.get('avg_weekly_return', 0):.1f}%")
            print(f"   Weekly Returns: {[f'{r*100:.1f}%' for r in result.get('weekly_returns', [])]}")
            print(f"   Meets Criteria: {'✅' if meets_criteria else '❌'}")
            print(f"   Reason: {reason}")
        else:
            print(f"   ⚠️  No data available")

if __name__ == "__main__":
    print("🚀 Starting Auto-Discovery Debug Session")
    print("=" * 60)
    
    # Run the full debug
    qualified_results, detailed_results = debug_auto_discovery()
    
    # Test a few specific tickers in detail
    test_tickers = ['AAPL', 'NVDA', 'SPY', 'QQQ']
    
    for ticker in test_tickers:
        test_specific_ticker(ticker)
    
    print("\n" + "=" * 60)
    print("🏁 Debug Session Complete")
