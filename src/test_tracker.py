"""
Test module version of options_tracker.py that doesn't rely on streamlit
This allows us to test the functionality in isolation.
"""

import sys
import os
sys.path.append('.')

# Patch streamlit to avoid dependency issues
import builtins
original_import = builtins.__import__

def patched_import(name, *args, **kwargs):
    if name == 'streamlit':
        # Create a mock streamlit module
        class MockStreamlit:
            def error(self, msg):
                print(f"ERROR: {msg}")
                
            def warning(self, msg):
                print(f"WARNING: {msg}")
                
            def info(self, msg):
                print(f"INFO: {msg}")
        
        return MockStreamlit()
    return original_import(name, *args, **kwargs)

# Apply the patch
builtins.__import__ = patched_import

# Now import from options_tracker
from src.options_tracker import OptionsTracker

class TestOptionsTracker(BaseOptionsTracker):
    """Test-friendly version of OptionsTracker"""
    
    def __init__(self):
        """Override init to avoid streamlit dependencies"""
        self.trades_file = "data/options_trades.pkl"
        self.predictions_file = "price_predictions.pkl"
        self.target_weekly_income = 500
        
        # Load existing trades (simplified)
        self.trades = []
        self.predictions = {}
        
        # Strategy types
        self.strategy_types = [
            "Bull Put Spread",
            "Bear Call Spread", 
            "Broken Wing Butterfly",
            "Iron Condor",
            "Cash Secured Put",
            "Covered Call",
            "Protective Put"
        ]
        
        # Generate a dynamic watchlist with popular options-active tickers
        self.watchlist = self.generate_dynamic_watchlist()
    
    # Override methods that use streamlit to use print instead
    def error(self, message):
        """Override st.error to use print"""
        print(f"ERROR: {message}")
    
    def warning(self, message):
        """Override st.warning to use print"""
        print(f"WARNING: {message}")

if __name__ == "__main__":
    # Simple test
    tracker = TestOptionsTracker()
    prediction = tracker.predict_price_range('SPY')
    
    if prediction:
        print("\nPrice prediction for SPY:")
        print(f"Current: ${prediction['current_price']:.2f}")
        print(f"Range: ${prediction['lower_bound']:.2f} - ${prediction['upper_bound']:.2f}")
        print(f"Target: ${prediction['target_price']:.2f}")
        print(f"Bias score: {prediction['bias_score']:.2f}")
        print(f"Bullish probability: {prediction['bullish_probability']:.1%}")
        print(f"Using implied volatility: {prediction['iv_based']}")
        print(f"Weekly volatility: {prediction['weekly_volatility']:.1%}")
    else:
        print("Failed to generate prediction")
