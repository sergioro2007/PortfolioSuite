#!/usr/bin/env python3
"""
Direct test of ARKK and ARKQ with both apps
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from streamlit_app import PortfolioTracker as OriginalTracker
from tactical_tracker import PortfolioTracker as NewTracker

def test_etf_analysis():
    print("🔍 Testing ETF Analysis")
    print("=" * 40)
    
    original = OriginalTracker()
    new = NewTracker()
    
    etfs = ["ARKK", "ARKQ", "AVGO"]
    
    for ticker in etfs:
        print(f"\n📊 Testing {ticker}:")
        
        # Test original app
        try:
            orig_result = original.analyze_ticker_momentum(ticker)
            if orig_result:
                print(f"  Original: ✅ Analyzed")
                print(f"    Market cap: ${orig_result.get('market_cap', 0)/1e9:.1f}B")
                print(f"    Meets criteria: {orig_result.get('meets_criteria', False)}")
                print(f"    Weekly return: {orig_result.get('avg_weekly_return', 0):.2f}%")
                
                # Check if it passes market cap filter
                passes_market_cap = orig_result.get('market_cap', 0) > 5e9
                print(f"    Passes market cap filter (>$5B): {passes_market_cap}")
            else:
                print(f"  Original: ❌ No result")
        except Exception as e:
            print(f"  Original: ❌ Error - {e}")
        
        # Test new app
        try:
            new_result = new.analyze_ticker_momentum(ticker)
            if new_result:
                print(f"  New: ✅ Analyzed")
                print(f"    Market cap: ${new_result.get('market_cap', 0)/1e9:.1f}B")
                print(f"    Meets criteria: {new_result.get('meets_criteria', False)}")
                print(f"    Weekly return: {new_result.get('avg_weekly_return', 0):.2f}%")
                
                # Check if it passes market cap filter
                passes_market_cap = new_result.get('market_cap', 0) > 5e9
                print(f"    Passes market cap filter (>$5B): {passes_market_cap}")
            else:
                print(f"  New: ❌ No result")
        except Exception as e:
            print(f"  New: ❌ Error - {e}")

if __name__ == "__main__":
    test_etf_analysis()
