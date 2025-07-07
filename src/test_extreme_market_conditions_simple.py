"""
Test script to demonstrate the prediction model behavior under extreme market conditions.

This script shows what the hybrid target zone model would predict in:
1. Very bearish market conditions
2. Very bullish market conditions

The script manipulates the technical indicators to simulate these extreme conditions.
(Simple version that doesn't use matplotlib for visualization)
"""

import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime

# Add parent directory to path to import local modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.options_tracker import OptionsTracker

# Create a test class that inherits from OptionsTracker to mock extreme conditions
class ExtremeConditionTester(OptionsTracker):
    def __init__(self):
        # Initialize without calling parent constructor to avoid loading real data
        self.trades_file = "data/options_trades.pkl"
        self.predictions_file = "price_predictions.pkl"
        self.target_weekly_income = 500
        
    def get_technical_indicators_with_override(self, ticker, period="3mo", override_values=None):
        """Get technical indicators with the ability to override values for testing"""
        # Get normal indicators
        indicators = self.get_technical_indicators(ticker, period)
        
        # Override with test values if provided
        if override_values and isinstance(override_values, dict):
            for key, value in override_values.items():
                if key in indicators:
                    indicators[key] = value
        
        return indicators
    
    def predict_price_range_extreme(self, ticker, scenario="neutral", iv_override=None):
        """Predict price range under extreme market conditions"""
        try:
            # Get base indicators
            indicators = self.get_technical_indicators(ticker)
            if not indicators:
                return {}
            
            current_price = indicators['current_price']
            historical_vol = indicators['volatility']
            
            # Override indicators based on scenario
            if scenario == "very_bearish":
                # Very bearish scenario: high RSI (overbought), negative MACD, negative momentum
                indicators['rsi'] = 85.0  # Extremely overbought (bearish signal)
                indicators['macd'] = -2.0  # Strong bearish momentum
                indicators['macd_signal'] = 1.0  # MACD below signal line (bearish)
                indicators['momentum'] = -5.0  # Strong downward price momentum
                print(f"🐻 VERY BEARISH SCENARIO for {ticker}: Overbought RSI, Bearish MACD, Negative Momentum")
                
            elif scenario == "very_bullish":
                # Very bullish scenario: low RSI (oversold), positive MACD, positive momentum
                indicators['rsi'] = 15.0  # Extremely oversold (bullish signal)
                indicators['macd'] = 2.0  # Strong bullish momentum
                indicators['macd_signal'] = -1.0  # MACD above signal line (bullish)
                indicators['momentum'] = 5.0  # Strong upward price momentum
                print(f"🐂 VERY BULLISH SCENARIO for {ticker}: Oversold RSI, Bullish MACD, Positive Momentum")
            
            # Use IV if available, otherwise fall back to historical volatility
            if iv_override:
                weekly_vol = iv_override
                print(f"  📈 Using override implied volatility for {ticker}: {weekly_vol * np.sqrt(52):.1%} annual, {weekly_vol:.1%} weekly")
            else:
                # For this test, just use historical volatility
                weekly_vol = historical_vol / np.sqrt(52)
                print(f"  📊 Using historical volatility for {ticker}: {historical_vol:.1%} annual, {weekly_vol:.1%} weekly")
            
            # Base prediction range (1 standard deviation)
            base_range = current_price * weekly_vol
            
            # Extract the indicator values for bias calculation
            rsi = indicators.get('rsi', 50)
            macd = indicators.get('macd', 0)
            macd_signal = indicators.get('macd_signal', 0)
            momentum = indicators.get('momentum', 0)
            
            # Bias calculation
            bias_score = 0
            
            # RSI bias
            if rsi > 70:
                bias_score -= 0.2  # Overbought, bearish bias
                print(f"  📉 RSI overbought ({rsi:.1f}): {bias_score:.2f} bias adjustment")
            elif rsi < 30:
                bias_score += 0.2  # Oversold, bullish bias
                print(f"  📈 RSI oversold ({rsi:.1f}): {bias_score:.2f} bias adjustment")
            else:
                print(f"  ↔️ RSI neutral ({rsi:.1f}): No bias adjustment")
            
            # MACD bias
            if macd > macd_signal:
                bias_score += 0.1  # Bullish momentum
                print(f"  📈 MACD bullish ({macd:.2f} > {macd_signal:.2f}): +0.10 bias adjustment")
            else:
                bias_score -= 0.1  # Bearish momentum
                print(f"  📉 MACD bearish ({macd:.2f} <= {macd_signal:.2f}): -0.10 bias adjustment")
            
            # Momentum bias
            if momentum > 2:
                bias_score += 0.1
                print(f"  📈 Strong positive momentum ({momentum:.2f}): +0.10 bias adjustment")
            elif momentum < -2:
                bias_score -= 0.1
                print(f"  📉 Strong negative momentum ({momentum:.2f}): -0.10 bias adjustment")
            else:
                print(f"  ↔️ Neutral momentum ({momentum:.2f}): No bias adjustment")
                
            print(f"  🎯 Final bias score: {bias_score:.2f}")
            
            # Calculate predicted range - use implied volatility for the range width
            lower_bound = current_price - base_range
            upper_bound = current_price + base_range
            
            # HYBRID MODEL: Bias-adjusted range center
            bias_adjustment = current_price * bias_score * 0.01
            print(f"  📊 Price bias adjustment: ${bias_adjustment:.2f} ({bias_score:.2f}% of ${current_price:.2f})")
            
            # Shift the entire range based on bias
            lower_bound += bias_adjustment
            upper_bound += bias_adjustment
            
            # Target price is at center of adjusted range
            target_price = current_price + bias_adjustment
            
            # Probability of bullish move
            bullish_prob = 0.5 + (bias_score * 0.5)
            bullish_prob = max(0.1, min(0.9, bullish_prob))
            
            print(f"  🎯 Prediction: ${lower_bound:.2f} to ${upper_bound:.2f} (target: ${target_price:.2f})")
            print(f"  📊 Bullish probability: {bullish_prob:.1%}")
            
            return {
                'current_price': current_price,
                'lower_bound': lower_bound,
                'upper_bound': upper_bound,
                'target_price': target_price,
                'bullish_probability': bullish_prob,
                'bias_score': bias_score,
                'weekly_volatility': weekly_vol,
                'bias_adjustment': bias_adjustment,
                'indicators': {
                    'rsi': rsi,
                    'macd': macd,
                    'macd_signal': macd_signal,
                    'momentum': momentum
                }
            }
        
        except Exception as e:
            print(f"Error in predict_price_range_extreme: {str(e)}")
            return {}

def run_test():
    """Run the test for extreme market conditions"""
    print("=" * 80)
    print("TESTING EXTREME MARKET CONDITIONS")
    print("=" * 80)
    
    # Initialize the tester
    tester = ExtremeConditionTester()
    
    # Test with SPY (S&P 500 ETF)
    ticker = "SPY"
    print(f"\n🔍 ANALYZING {ticker} UNDER DIFFERENT MARKET CONDITIONS\n")
    
    # Run predictions for different scenarios
    predictions = {}
    
    # 1. Neutral (actual market conditions)
    print("\n" + "=" * 50)
    print("SCENARIO: NEUTRAL (BASELINE)")
    print("=" * 50)
    neutral_pred = tester.predict_price_range_extreme(ticker, "neutral")
    if neutral_pred:
        predictions['neutral'] = neutral_pred
    
    # 2. Very Bearish
    print("\n" + "=" * 50)
    print("SCENARIO: VERY BEARISH")
    print("=" * 50)
    bearish_pred = tester.predict_price_range_extreme(ticker, "very_bearish")
    if bearish_pred:
        predictions['very_bearish'] = bearish_pred
    
    # 3. Very Bullish
    print("\n" + "=" * 50)
    print("SCENARIO: VERY BULLISH")
    print("=" * 50)
    bullish_pred = tester.predict_price_range_extreme(ticker, "very_bullish")
    if bullish_pred:
        predictions['very_bullish'] = bullish_pred
    
    # Print detailed comparison
    print("\n" + "=" * 80)
    print("DETAILED COMPARISON OF PREDICTIONS")
    print("=" * 80)
    
    if 'neutral' in predictions and 'very_bearish' in predictions and 'very_bullish' in predictions:
        neutral = predictions['neutral']
        bearish = predictions['very_bearish']
        bullish = predictions['very_bullish']
        
        current_price = neutral['current_price']
        
        print(f"Current Price: ${current_price:.2f}")
        print("\nNeutral Scenario:")
        print(f"  • Target Price: ${neutral['target_price']:.2f} ({(neutral['target_price']/current_price - 1)*100:.1f}% change)")
        print(f"  • Price Range: ${neutral['lower_bound']:.2f} to ${neutral['upper_bound']:.2f}")
        print(f"  • Range Width: ${neutral['upper_bound'] - neutral['lower_bound']:.2f}")
        print(f"  • Bias Score: {neutral['bias_score']:.2f}")
        print(f"  • Bullish Probability: {neutral['bullish_probability']:.1%}")
        
        print("\nVery Bearish Scenario:")
        print(f"  • Target Price: ${bearish['target_price']:.2f} ({(bearish['target_price']/current_price - 1)*100:.1f}% change)")
        print(f"  • Price Range: ${bearish['lower_bound']:.2f} to ${bearish['upper_bound']:.2f}")
        print(f"  • Range Width: ${bearish['upper_bound'] - bearish['lower_bound']:.2f}")
        print(f"  • Bias Score: {bearish['bias_score']:.2f}")
        print(f"  • Bullish Probability: {bearish['bullish_probability']:.1%}")
        
        print("\nVery Bullish Scenario:")
        print(f"  • Target Price: ${bullish['target_price']:.2f} ({(bullish['target_price']/current_price - 1)*100:.1f}% change)")
        print(f"  • Price Range: ${bullish['lower_bound']:.2f} to ${bullish['upper_bound']:.2f}")
        print(f"  • Range Width: ${bullish['upper_bound'] - bullish['lower_bound']:.2f}")
        print(f"  • Bias Score: {bullish['bias_score']:.2f}")
        print(f"  • Bullish Probability: {bullish['bullish_probability']:.1%}")
        
        # Show percentage differences
        bearish_diff = (bearish['target_price'] / neutral['target_price'] - 1) * 100
        bullish_diff = (bullish['target_price'] / neutral['target_price'] - 1) * 100
        
        print("\nDifference from Neutral:")
        print(f"  • Bearish Target: {bearish_diff:.1f}% lower")
        print(f"  • Bullish Target: {bullish_diff:.1f}% higher")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    run_test()
