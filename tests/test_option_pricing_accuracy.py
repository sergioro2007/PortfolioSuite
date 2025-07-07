"""
Tests for option pricing accuracy against theoretical models and market data
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np
import math
from datetime import datetime, timedelta

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.options_tracker import OptionsTracker


class TestOptionPricingAccuracy(unittest.TestCase):
    """Test the accuracy of option pricing against theoretical models"""
    
    def setUp(self):
        """Set up the test environment"""
        self.tracker = OptionsTracker()
        
        # Mock watchlist for testing
        self.tracker.watchlist = {
            'SPY': {'current_price': 500.0},
        }
    
    def black_scholes(self, spot_price, strike_price, time_to_exp, risk_free_rate, sigma, option_type='call'):
        """Black-Scholes option pricing model for comparison"""
        # spot_price: spot price, strike_price: strike price, time_to_exp: time to expiration (in years)
        # risk_free_rate: risk-free interest rate, sigma: volatility
        
        d1 = (math.log(spot_price / strike_price) + (risk_free_rate + sigma**2 / 2) * time_to_exp) / (sigma * math.sqrt(time_to_exp))
        d2 = d1 - sigma * math.sqrt(time_to_exp)
        
        def norm_cdf(x):
            """Normal cumulative distribution function"""
            return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0
        
        if option_type == 'call':
            return spot_price * norm_cdf(d1) - strike_price * math.exp(-risk_free_rate * time_to_exp) * norm_cdf(d2)
        else:  # put
            return strike_price * math.exp(-risk_free_rate * time_to_exp) * norm_cdf(-d2) - spot_price * norm_cdf(-d1)
    
    def test_fallback_pricing_vs_black_scholes(self):
        """Test fallback pricing against Black-Scholes model"""
        # Parameters
        spot_price = 500.0  # SPY spot price
        risk_free_rate = 0.05   # Risk-free rate
        sigma = 0.15  # Volatility for SPY
        
        strikes = [475.0, 485.0, 495.0, 500.0, 505.0, 515.0, 525.0]
        
        # Test for different time horizons
        time_horizons = [7, 30, 60, 90]
        
        for days in time_horizons:
            time_to_exp = days / 365.0  # Convert days to years
            expiration = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
            
            # Get fallback prices
            fallback_prices = self.tracker._fallback_option_prices('SPY', strikes, expiration)
            
            # Calculate Black-Scholes prices
            for strike in strikes:
                strike_key = f"{strike:g}"
                
                # Calculate Black-Scholes call price
                bs_call = self.black_scholes(spot_price, strike, time_to_exp, risk_free_rate, sigma, 'call')
                fb_call = fallback_prices.get(f"CALL_{strike_key}", 0)
                
                # Calculate Black-Scholes put price
                bs_put = self.black_scholes(spot_price, strike, time_to_exp, risk_free_rate, sigma, 'put')
                fb_put = fallback_prices.get(f"PUT_{strike_key}", 0)
                
                # Fallback prices should be within a reasonable range of Black-Scholes
                # We're looking for general direction rather than exact matches
                # since fallback is simplified and may use very different volatility assumptions
                # Only check strikes near ATM for shorter durations
                if days <= 60 and 495.0 <= strike <= 505.0:
                    # Verify call is positive and within reasonable range
                    self.assertGreater(fb_call, 0.0, f"Call price should be positive for {strike_key}, {days}d")
                    self.assertLess(fb_call, bs_call * 2.0, f"Call price unreasonably high: {fb_call} vs {bs_call} for {strike_key}, {days}d")
                    
                    # Verify put is positive and within reasonable range
                    self.assertGreater(fb_put, 0.0, f"Put price should be positive for {strike_key}, {days}d")
                    self.assertLess(fb_put, bs_put * 2.0, f"Put price unreasonably high: {fb_put} vs {bs_put} for {strike_key}, {days}d")
    
    def test_pricing_respects_parity(self):
        """Test that put-call parity roughly holds in the pricing model"""
        # Parameters
        spot_price = 500.0  # SPY spot price
        risk_free_rate = 0.05   # Risk-free rate
        time_to_exp = 30 / 365.0  # 30 days
        expiration = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        
        strikes = [485.0, 495.0, 500.0, 505.0, 515.0]
        
        # Get fallback prices
        fallback_prices = self.tracker._fallback_option_prices('SPY', strikes, expiration)
        
        for strike in strikes:
            strike_key = f"{strike:g}"
            call_price = fallback_prices.get(f"CALL_{strike_key}", 0)
            put_price = fallback_prices.get(f"PUT_{strike_key}", 0)
            
            # Put-Call parity: C + Ke^(-rT) ≈ P + S
            # We'll check if it's reasonably close with our simplified model
            left_side = call_price + strike * math.exp(-risk_free_rate * time_to_exp)
            right_side = put_price + spot_price
            
            # Allow for some difference due to simplifications
            self.assertLess(abs(left_side - right_side), 15.0,
                          f"Put-call parity significantly violated for strike {strike}")
    
    def test_intrinsic_value_constraints(self):
        """Test that option prices respect intrinsic value constraints"""
        spot_price = 500.0  # SPY spot price
        expiration = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        
        strikes = [470.0, 480.0, 490.0, 500.0, 510.0, 520.0, 530.0]
        
        # Get fallback prices
        fallback_prices = self.tracker._fallback_option_prices('SPY', strikes, expiration)
        
        for strike in strikes:
            strike_key = f"{strike:g}"
            call_price = fallback_prices.get(f"CALL_{strike_key}", 0)
            put_price = fallback_prices.get(f"PUT_{strike_key}", 0)
            
            # Call intrinsic value: max(0, S-K)
            call_intrinsic = max(0, spot_price - strike)
            
            # Put intrinsic value: max(0, K-S)
            put_intrinsic = max(0, strike - spot_price)
            
            # Check that prices are never below intrinsic value
            self.assertGreaterEqual(call_price, call_intrinsic,
                                  f"Call price below intrinsic value for strike {strike}")
            self.assertGreaterEqual(put_price, put_intrinsic,
                                  f"Put price below intrinsic value for strike {strike}")


if __name__ == '__main__':
    unittest.main()
