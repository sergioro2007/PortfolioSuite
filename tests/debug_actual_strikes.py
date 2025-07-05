"""
Test script to debug Iron Condor strike generation and URL creation
"""

from src.options_tracker import OptionsTracker
from src.options_tracker_ui import generate_optionstrat_url

def test_actual_iron_condor_generation():
    """Test actual Iron Condor generation to see strike values"""
    
    tracker = OptionsTracker()
    
    # Add SPY to watchlist to enable trade generation
    ticker = "SPY"
    tracker.watchlist[ticker] = {
        'target_price': 580.0,
        'forecast': 'Bullish',
        'confidence': 75
    }
    
    print(f"Testing Iron Condor generation for {ticker}")
    
    # Get trade suggestions
    suggestions = tracker.generate_trade_suggestions(5)  # Generate more to increase chance of Iron Condor
    
    # Find Iron Condor suggestion
    iron_condor = None
    for suggestion in suggestions:
        if suggestion['strategy'] == 'Iron Condor':
            iron_condor = suggestion
            break
    
    if iron_condor:
        print("\n=== Iron Condor Suggestion ===")
        print(f"Ticker: {iron_condor['ticker']}")
        print(f"Put Long Strike: {iron_condor['put_long_strike']}")
        print(f"Put Short Strike: {iron_condor['put_short_strike']}")
        print(f"Call Short Strike: {iron_condor['call_short_strike']}")
        print(f"Call Long Strike: {iron_condor['call_long_strike']}")
        
        # Generate URL
        url = generate_optionstrat_url(iron_condor)
        print(f"\nGenerated URL: {url}")
        
        # Check strike types
        print("\nStrike types:")
        print(f"Put Long: {type(iron_condor['put_long_strike'])} = {iron_condor['put_long_strike']}")
        print(f"Put Short: {type(iron_condor['put_short_strike'])} = {iron_condor['put_short_strike']}")
        print(f"Call Short: {type(iron_condor['call_short_strike'])} = {iron_condor['call_short_strike']}")
        print(f"Call Long: {type(iron_condor['call_long_strike'])} = {iron_condor['call_long_strike']}")
        
    else:
        print("No Iron Condor suggestion found")
        print(f"Available strategies: {[s['strategy'] for s in suggestions]}")

if __name__ == "__main__":
    test_actual_iron_condor_generation()
