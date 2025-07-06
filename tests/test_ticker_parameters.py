import sys
sys.path.append('.')
from src.options_tracker import OptionsTracker
import yfinance as yf

def test_calculate_ticker_parameters():
    """Test the _calculate_ticker_parameters method"""
    print('=== TESTING TICKER PARAMETER CALCULATION ===')
    tracker = OptionsTracker()
    
    # Test with a few different types of tickers
    test_tickers = [
        'AAPL',    # Large cap tech
        'SPY',     # ETF
        'XLE',     # Sector ETF
        'SQ',      # Fintech
        'INVALID'  # Non-existent ticker
    ]
    
    for ticker in test_tickers:
        print(f"\nTesting ticker: {ticker}")
        try:
            params = tracker._calculate_ticker_parameters(ticker)
            
            if params is None:
                print(f"❌ No parameters returned for {ticker}")
                continue
                
            print(f"✅ Parameters successfully calculated:")
            print(f"  - Current price: ${params['current_price']:.2f}")
            print(f"  - Range: ${params['range_68'][0]:.2f} to ${params['range_68'][1]:.2f}")
            print(f"  - Target zone: ${params['target_zone']:.2f}")
            print(f"  - Bias probability: {params['bias_prob']:.2f}")
            
            # Verify parameter relationships
            price = params['current_price']
            range_low, range_high = params['range_68']
            bias = params['bias_prob']
            target = params['target_zone']
            
            # Check that range makes sense (price in the middle, roughly)
            if not (range_low < price < range_high):
                print(f"⚠️ Price (${price:.2f}) not within calculated range (${range_low:.2f} to ${range_high:.2f})")
            
            # Check that bias and target are correlated
            if bias > 0.5 and target < price:
                print(f"⚠️ Bullish bias ({bias:.2f}) but target (${target:.2f}) below current price (${price:.2f})")
            elif bias < 0.5 and target > price:
                print(f"⚠️ Bearish bias ({bias:.2f}) but target (${target:.2f}) above current price (${price:.2f})")
                
            # Calculate actual weekly volatility from returned values
            weekly_vol = (range_high - range_low) / (2 * price)
            print(f"  - Implied weekly volatility: {weekly_vol:.2%}")
            
            # Get real data to compare
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1mo")
            if not hist.empty:
                actual_weekly_return = hist['Close'].pct_change().std() * (5/252)**0.5
                print(f"  - Actual recent weekly volatility: {actual_weekly_return:.2%}")
                
                # Compare implied vs actual
                ratio = weekly_vol / actual_weekly_return if actual_weekly_return > 0 else 0
                print(f"  - Volatility estimation ratio: {ratio:.2f}x")
                
                if ratio < 0.5 or ratio > 2:
                    print(f"⚠️ Volatility estimate differs significantly from actual recent volatility")
            
        except Exception as e:
            print(f"❌ Error testing {ticker}: {e}")
    
    # Test error handling for API failures
    print("\nTesting error handling:")
    try:
        # Force an error by using a non-existent ticker symbol
        params = tracker._calculate_ticker_parameters('THISISNOTAREALTICKER')
        if params is None:
            print("✅ Properly handled invalid ticker")
        else:
            print("❌ Failed to handle invalid ticker properly")
    except Exception as e:
        print(f"❌ Uncaught exception for invalid ticker: {e}")

if __name__ == "__main__":
    test_calculate_ticker_parameters()
