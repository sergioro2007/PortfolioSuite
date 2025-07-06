"""
Helper function for implied volatility calculation.
This will be imported into options_tracker.py
"""

def _get_implied_volatility(self, ticker, current_price=None):
    """Helper method to get implied volatility from options data"""
    try:
        import yfinance as yf
        import numpy as np
        
        stock = yf.Ticker(ticker)
        
        # Get current price if not provided
        if current_price is None:
            try:
                info = stock.info
                current_price = info.get('regularMarketPrice', info.get('previousClose', 100))
            except:
                # Fall back to historical data
                hist = stock.history(period="1d")
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                else:
                    current_price = 100
        
        # Try to get options chain
        if hasattr(stock, 'options') and stock.options:
            # Get nearest expiration
            nearest_exp = stock.options[0]
            options = stock.option_chain(nearest_exp)
            
            # Find ATM options (within 5% of current price)
            atm_calls = options.calls[
                (options.calls['strike'] >= current_price * 0.95) & 
                (options.calls['strike'] <= current_price * 1.05)
            ]
            atm_puts = options.puts[
                (options.puts['strike'] >= current_price * 0.95) & 
                (options.puts['strike'] <= current_price * 1.05)
            ]
            
            # Extract implied volatilities
            ivs = []
            
            # From calls
            if 'impliedVolatility' in atm_calls.columns and not atm_calls.empty:
                call_ivs = atm_calls['impliedVolatility'].dropna().tolist()
                ivs.extend(call_ivs)
            
            # From puts
            if 'impliedVolatility' in atm_puts.columns and not atm_puts.empty:
                put_ivs = atm_puts['impliedVolatility'].dropna().tolist()
                ivs.extend(put_ivs)
            
            # If we have IV values, use their average
            if ivs:
                annual_iv = float(sum(ivs) / len(ivs))
                weekly_vol = annual_iv / np.sqrt(52)  # Convert to weekly
                
                return {
                    'valid': True,
                    'annual_iv': annual_iv,
                    'weekly_vol': weekly_vol
                }
        
        # If we get here, return invalid result
        return {'valid': False}
        
    except Exception as e:
        print(f"  ⚠️ IV calculation error for {ticker}: {e}")
        return {'valid': False}
