#!/usr/bin/env python3
import sys
sys.path.insert(0, 'src')

from portfolio_suite.options_trading.core import OptionsTracker

print("Testing watchlist structure...")
t = OptionsTracker()

print(f"Watchlist type: {type(t.watchlist)}")
print(f"Watchlist keys: {list(t.watchlist.keys())}")

if 'tickers' in t.watchlist:
    tickers_dict = t.watchlist['tickers']
    print(f"Tickers dict type: {type(tickers_dict)}")
    print(f"Tickers dict keys: {list(tickers_dict.keys())[:5]}...")
    
    # Test the list creation logic
    watchlist_tickers = list(t.watchlist.get("tickers", {}).keys())[:10]
    print(f"Watchlist tickers length: {len(watchlist_tickers)}")
    print(f"First 5 tickers: {watchlist_tickers[:5]}")
    
    # Test the slice
    num_suggestions = 2
    sliced_tickers = watchlist_tickers[: num_suggestions * 2]
    print(f"Sliced tickers: {sliced_tickers}")
else:
    print("No 'tickers' key in watchlist!")
