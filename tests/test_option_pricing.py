"""
Unit tests for option pricing functionality
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.options_tracker import OptionsTracker


class TestOptionPricing(unittest.TestCase):
    """Test the option pricing functions in OptionsTracker"""
    
    def setUp(self):
        """Set up the test environment"""
        self.tracker = OptionsTracker()
        
        # Mock watchlist for testing
        self.tracker.watchlist = {
            'SPY': {'current_price': 500.0},
            'AAPL': {'current_price': 200.0},
            'NVDA': {'current_price': 120.0},
        }
    
    @patch('yfinance.Ticker')
    def test_get_option_prices(self, mock_yf_ticker):
        """Test getting option prices from yfinance"""
        # Set up mock options data
        mock_ticker = MagicMock()
        mock_ticker.options = ['2025-08-15', '2025-09-19']
        
        # Create mock DataFrames for options chains
        calls_data = {
            'strike': [495.0, 500.0, 505.0],
            'bid': [12.50, 9.75, 7.25],
            'ask': [13.00, 10.25, 7.75],
            'lastPrice': [12.75, 10.0, 7.50]
        }
        puts_data = {
            'strike': [495.0, 500.0, 505.0],
            'bid': [7.50, 9.80, 12.30],
            'ask': [8.00, 10.30, 12.80],
            'lastPrice': [7.75, 10.05, 12.55]
        }
        
        mock_calls = pd.DataFrame(calls_data)
        mock_puts = pd.DataFrame(puts_data)
        
        mock_option_chain = MagicMock()
        mock_option_chain.calls = mock_calls
        mock_option_chain.puts = mock_puts
        
        mock_ticker.option_chain.return_value = mock_option_chain
        mock_yf_ticker.return_value = mock_ticker
        
        # Test the function
        strikes = [495.0, 500.0, 505.0]
        expiration = '2025-08-15'
        result = self.tracker.get_option_prices('SPY', strikes, expiration)
        
        # Verify results
        self.assertEqual(len(result), 6)  # 3 calls + 3 puts
        self.assertAlmostEqual(result['CALL_495'], 12.75, places=2)
        self.assertAlmostEqual(result['CALL_500'], 10.00, places=2)
        self.assertAlmostEqual(result['CALL_505'], 7.50, places=2)
        self.assertAlmostEqual(result['PUT_495'], 7.75, places=2)
        self.assertAlmostEqual(result['PUT_500'], 10.05, places=2)
        self.assertAlmostEqual(result['PUT_505'], 12.55, places=2)
    
    @patch('yfinance.Ticker')
    def test_get_option_prices_empty_chain(self, mock_yf_ticker):
        """Test fallback to estimated prices when options chain is empty"""
        # Mock an empty options chain
        mock_ticker = MagicMock()
        mock_ticker.options = []
        mock_yf_ticker.return_value = mock_ticker
        
        # Test with fallback
        strikes = [495.0, 500.0, 505.0]
        expiration = '2025-08-15'
        result = self.tracker.get_option_prices('SPY', strikes, expiration)
        
        # Verify fallback prices were generated
        self.assertEqual(len(result), 6)  # 3 calls + 3 puts
        self.assertTrue(all(price > 0 for price in result.values()))
    
    def test_fallback_option_prices(self):
        """Test the fallback price estimation logic"""
        # Test ATM, ITM, and OTM options
        strikes = [490.0, 500.0, 510.0]
        expiration = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        result = self.tracker._fallback_option_prices('SPY', strikes, expiration)
        
        # Verify basics of fallback pricing
        self.assertEqual(len(result), 6)  # 3 calls + 3 puts
        
        # Check that ITM options have higher intrinsic value than OTM
        # Note: We're not testing the full pricing order since the fallback
        # algorithm may include time value that affects the ordering
        self.assertGreater(result['CALL_490'], result['CALL_510'])  # ITM call > OTM call
        self.assertGreater(result['PUT_510'], result['PUT_490'])    # ITM put > OTM put
        
        # Intrinsic value checks
        self.assertGreaterEqual(result['CALL_490'], 10.0)  # At least intrinsic value (500-490)
        self.assertGreaterEqual(result['PUT_510'], 10.0)   # At least intrinsic value (510-500)
    
    def test_different_volatility_levels(self):
        """Test that higher volatility tickers have higher option prices"""
        strikes = [195.0, 200.0, 205.0]
        expiration = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        
        # AAPL (moderate volatility)
        aapl_prices = self.tracker._fallback_option_prices('AAPL', strikes, expiration)
        
        # NVDA (higher volatility)
        # Adjust price to match AAPL for comparison
        old_price = self.tracker.watchlist['NVDA']['current_price']
        self.tracker.watchlist['NVDA']['current_price'] = 200.0
        nvda_prices = self.tracker._fallback_option_prices('NVDA', strikes, expiration)
        self.tracker.watchlist['NVDA']['current_price'] = old_price
        
        # Higher volatility should result in higher option prices for ATM options
        self.assertGreater(nvda_prices['CALL_200'], aapl_prices['CALL_200'])
        self.assertGreater(nvda_prices['PUT_200'], aapl_prices['PUT_200'])


if __name__ == '__main__':
    unittest.main()
