"""
Tests for the standalone implied volatility function
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from portfolio_suite.options_trading import OptionsTracker
except ImportError:
    # Fallback to src directory for backward compatibility
    from src.options_tracker import OptionsTracker


class TestImpliedVolatility(unittest.TestCase):
    """Test the implied volatility calculation function"""
    
    def setUp(self):
        """Set up the test environment"""
        self.tracker = OptionsTracker()
    
    @patch('yfinance.Ticker')
    def test_get_implied_volatility_with_calls_and_puts(self, mock_yf_ticker):
        """Test implied volatility calculation with both calls and puts data"""
        # Set up mock options data
        mock_ticker = MagicMock()
        mock_ticker.options = ['2025-08-01']
        
        # Create mock DataFrames for options
        import pandas as pd
        import numpy as np
        
        # Mock calls DataFrame
        calls_data = {
            'strike': [100, 110, 120, 130, 140],
            'impliedVolatility': [0.25, 0.23, 0.22, 0.21, 0.20]
        }
        mock_calls = pd.DataFrame(calls_data)
        
        # Mock puts DataFrame
        puts_data = {
            'strike': [100, 110, 120, 130, 140],
            'impliedVolatility': [0.27, 0.25, 0.24, 0.23, 0.22]
        }
        mock_puts = pd.DataFrame(puts_data)
        
        # Create a mock options chain object
        class MockOptionChain:
            def __init__(self, calls, puts):
                self.calls = calls
                self.puts = puts
        
        mock_option_chain = MockOptionChain(mock_calls, mock_puts)
        
        # Make option_chain return the mock data
        mock_ticker.option_chain.return_value = mock_option_chain
        
        # Mock the stock info
        mock_ticker.info = {'regularMarketPrice': 120.0}
        
        # Set the mock return value for yf.Ticker
        mock_yf_ticker.return_value = mock_ticker
        
        # Call the function - returns a dict with different IV metrics
        iv_result = self.tracker._get_implied_volatility('AAPL')
        
        # Check the result is a dictionary
        self.assertIsInstance(iv_result, dict)
        self.assertIn('valid', iv_result)
        self.assertTrue(iv_result['valid'])
        
        # Check IV values
        self.assertIn('annual_iv', iv_result)
        self.assertIn('weekly_vol', iv_result)
        
        # Check the main IV values
        annual_iv = iv_result['annual_iv']
        weekly_vol = iv_result['weekly_vol']
        
        self.assertIsNotNone(annual_iv)
        self.assertGreater(annual_iv, 0.0)
        self.assertLessEqual(annual_iv, 1.0)
        
        # Should be around 0.23-0.24 based on our mock data (average of ATM options)
        self.assertGreaterEqual(annual_iv, 0.20)
        self.assertLessEqual(annual_iv, 0.30)
        
        # Weekly vol should be annual_iv / sqrt(52)
        self.assertAlmostEqual(weekly_vol, annual_iv / np.sqrt(52), delta=0.01)

    @patch('yfinance.Ticker')
    def test_get_implied_volatility_fallback_to_historical(self, mock_yf_ticker):
        """Test IV calculation fallback to historical volatility"""
        # Set up mock with no options data
        mock_ticker = MagicMock()
        mock_ticker.options = []  # No options available
        
        # Mock the stock info
        mock_ticker.info = {'regularMarketPrice': 120.0}
        
        # Set the mock return value for yf.Ticker
        mock_yf_ticker.return_value = mock_ticker
        
        # Call the function - should return invalid result with no options
        iv_result = self.tracker._get_implied_volatility('AAPL')
        
        # Check the result is a dictionary
        self.assertIsInstance(iv_result, dict)
        
        # Should have 'valid' key set to False
        self.assertIn('valid', iv_result)
        self.assertFalse(iv_result['valid'])


if __name__ == '__main__':
    unittest.main()
