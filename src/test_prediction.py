"""
Simple test for price prediction functionality
"""
import sys
sys.path.append('.')
from src.options_tracker import OptionsTracker

def test_price_prediction():
    """Test price prediction using hybrid model"""
    print("Testing price prediction with hybrid model...")
    
    # Create tracker and make a prediction
    tracker = OptionsTracker()
    prediction = tracker.predict_price_range('SPY')
    
    # Print results
    if prediction:
        print("Price prediction for SPY:")
        print(f"Current: ${prediction['current_price']:.2f}")
        print(f"Range: ${prediction['lower_bound']:.2f} - ${prediction['upper_bound']:.2f}")
        print(f"Target: ${prediction['target_price']:.2f}")
        print(f"Bias score: {prediction['bias_score']:.2f}")
        print(f"Bullish probability: {prediction['bullish_probability']:.1%}")
        print(f"Using implied volatility: {prediction['iv_based']}")
        print(f"Weekly volatility: {prediction['weekly_volatility']:.1%}")
    else:
        print("Failed to generate prediction")

if __name__ == "__main__":
    test_price_prediction()
