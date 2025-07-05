#!/usr/bin/env python3
"""
Test script to check if yfinance data is consistent
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time

def test_yfinance_consistency():
    """Test if yfinance returns consistent data for the same ticker"""
    print("🔍 Testing yfinance Data Consistency")
    print("=" * 50)
    
    # Test with a popular ticker
    ticker = "AAPL"
    
    print(f"Testing ticker: {ticker}")
    print("Fetching data 3 times with 1-second delay...")
    print()
    
    results = []
    
    for i in range(3):
        print(f"Fetch #{i+1}:")
        
        # Get current price
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1mo")
        
        if not hist.empty:
            current_price = float(hist['Close'].iloc[-1])
            last_date = hist.index[-1].strftime('%Y-%m-%d')
            data_points = len(hist)
            
            print(f"  Current price: ${current_price:.2f}")
            print(f"  Last date: {last_date}")
            print(f"  Data points: {data_points}")
            
            results.append({
                'price': current_price,
                'date': last_date,
                'points': data_points
            })
        else:
            print("  ERROR: No data returned")
            results.append(None)
        
        if i < 2:  # Don't sleep after last iteration
            time.sleep(1)
        print()
    
    # Compare results
    print("🔍 Comparison:")
    print("-" * 30)
    
    if all(r is not None for r in results):
        # Check prices
        prices = [r['price'] for r in results]
        if len(set(prices)) == 1:
            print(f"✅ CONSISTENT: All prices identical (${prices[0]:.2f})")
        else:
            print(f"❌ INCONSISTENT: Prices vary: {prices}")
        
        # Check dates
        dates = [r['date'] for r in results]
        if len(set(dates)) == 1:
            print(f"✅ CONSISTENT: All dates identical ({dates[0]})")
        else:
            print(f"❌ INCONSISTENT: Dates vary: {dates}")
        
        # Check data points
        points = [r['points'] for r in results]
        if len(set(points)) == 1:
            print(f"✅ CONSISTENT: All data points identical ({points[0]})")
        else:
            print(f"❌ INCONSISTENT: Data points vary: {points}")
    else:
        print("❌ ERROR: Some fetches failed")

def test_weekly_returns_consistency():
    """Test if weekly returns calculation is consistent"""
    print("\n" * 2)
    print("🔍 Testing Weekly Returns Consistency")
    print("=" * 50)
    
    ticker = "AAPL"
    print(f"Testing weekly returns for: {ticker}")
    print("Calculating 3 times with 1-second delay...")
    print()
    
    results = []
    
    for i in range(3):
        print(f"Calculation #{i+1}:")
        
        try:
            # Calculate weekly returns using same method as tactical tracker
            end = datetime.today()
            start = end - timedelta(days=5 * 7 + 7)  # 5 weeks + safety
            df = yf.download(ticker, start=start, end=end, interval='1d', auto_adjust=True, progress=False)
            
            if not df.empty:
                # Get the close prices
                close_prices = df['Close']
                
                # Group by ISO calendar week
                close_df = close_prices.to_frame(name='Close')
                close_df['Week'] = close_prices.index.to_series().dt.isocalendar().week
                weekly_close = close_df.groupby('Week')['Close'].last()
                
                # Calculate returns
                returns_series = weekly_close.pct_change().dropna()
                returns = returns_series.tolist()
                last_4_returns = returns[-4:] if len(returns) >= 4 else returns
                
                print(f"  Weekly returns: {[f'{r:.4f}' for r in last_4_returns]}")
                print(f"  Number of weeks: {len(last_4_returns)}")
                
                results.append(last_4_returns)
            else:
                print("  ERROR: No data returned")
                results.append(None)
                
        except Exception as e:
            print(f"  ERROR: {e}")
            results.append(None)
        
        if i < 2:  # Don't sleep after last iteration
            time.sleep(1)
        print()
    
    # Compare results
    print("🔍 Weekly Returns Comparison:")
    print("-" * 30)
    
    if all(r is not None for r in results):
        # Check if all returns are identical
        if all(results[0] == r for r in results[1:]):
            print("✅ CONSISTENT: All weekly returns identical")
        else:
            print("❌ INCONSISTENT: Weekly returns vary")
            for i, r in enumerate(results):
                print(f"  Run {i+1}: {[f'{x:.4f}' for x in r]}")
    else:
        print("❌ ERROR: Some calculations failed")

if __name__ == "__main__":
    test_yfinance_consistency()
    test_weekly_returns_consistency()
