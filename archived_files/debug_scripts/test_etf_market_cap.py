#!/usr/bin/env python3
"""
Quick test to check market cap data for ETFs
"""
import yfinance as yf

# Test ETFs that are missing from new app but present in original
etfs = ["ARKK", "ARKQ", "AVGO"]

for ticker in etfs:
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        market_cap = info.get('marketCap', 0)
        print(f"{ticker}: Market cap = {market_cap:,}")
        if market_cap == 0:
            print(f"  Trying other fields...")
            # Check alternative fields
            net_assets = info.get('totalAssets', 0)
            aum = info.get('aum', 0) 
            print(f"  Total assets: {net_assets:,}")
            print(f"  AUM: {aum:,}")
        print()
    except Exception as e:
        print(f"{ticker}: Error - {e}")
        print()
