"""
Unit tests for OptionsTracker core functionality
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from portfolio_suite.options_trading.core import OptionsTracker


class TestOptionsTracker(unittest.TestCase):
    """Test core functionality of the OptionsTracker class"""
    
    def setUp(self):
        """Set up the test environment"""
        self.tracker = OptionsTracker()
        
        # Mock watchlist for testing
        self.tracker.watchlist = {
            'SPY': {
                'current_price': 625.34,
                'range_68': (601.02, 649.66),
                'target_zone': 625.65,
                'bias_prob': 0.53
            },
            'QQQ': {
                'current_price': 556.22,
                'range_68': (531.61, 580.83),
                'target_zone': 557.33,
                'bias_prob': 0.60
            },
            'AAPL': {
                'current_price': 213.45,
                'range_68': (205.11, 221.79),
                'target_zone': 214.50,
                'bias_prob': 0.57
            }
        }
    
    def test_initialize(self):
        """Test that the OptionsTracker initializes correctly"""
        self.assertIsInstance(self.tracker, OptionsTracker)
        self.assertIsInstance(self.tracker.watchlist, dict)
        self.assertIsInstance(self.tracker.trades, list)
        self.assertIsInstance(self.tracker.strategy_types, list)
        
        # Check that strategy types include the expected strategies
        expected_strategies = ['Bull Put Spread', 'Bear Call Spread', 'Iron Condor']
        for strategy in expected_strategies:
            self.assertIn(strategy, self.tracker.strategy_types)
    
    def test_generate_watchlist(self):
        """Test watchlist generation"""
        # Generate a fresh watchlist
        self.tracker.refresh_watchlist()
        
        # Verify watchlist structure
        self.assertIsInstance(self.tracker.watchlist, dict)
        if len(self.tracker.watchlist) > 0:
            first_ticker = next(iter(self.tracker.watchlist))
            ticker_data = self.tracker.watchlist[first_ticker]
            
            # Check required fields
            self.assertIn('current_price', ticker_data)
            self.assertIn('range_68', ticker_data)
            self.assertIn('target_zone', ticker_data)
            self.assertIn('bias_prob', ticker_data)
    
    def test_add_trade(self):
        """Test adding a new trade"""
        initial_trade_count = len(self.tracker.trades)
        
        # Create a test trade
        new_trade = {
            'ticker': 'SPY',
            'strategy': 'Bull Put Spread',
            'entry_date': '2025-07-01',
            'expiration': '2025-07-11',
            'short_strike': 620,
            'long_strike': 615,
            'contracts': 1,
            'premium': 1.25,
            'max_profit': 125,
            'max_loss': 375,
            'status': 'Open'
        }
        
        # Add the trade
        self.tracker.add_trade(new_trade)
        
        # Verify trade was added
        self.assertEqual(len(self.tracker.trades), initial_trade_count + 1)
        self.assertEqual(self.tracker.trades[-1]['ticker'], 'SPY')
        self.assertEqual(self.tracker.trades[-1]['strategy'], 'Bull Put Spread')

    def test_get_price_prediction(self):
        """Test price prediction functionality"""
        ticker = 'SPY'
        prediction = self.tracker.predict_price_range(ticker)
        
        # Verify prediction structure
        self.assertIsInstance(prediction, dict)
        self.assertIn('current_price', prediction)
        self.assertIn('lower_bound', prediction)
        self.assertIn('upper_bound', prediction)
        self.assertIn('target_price', prediction)
        self.assertIn('bullish_probability', prediction)


if __name__ == '__main__':
    unittest.main()
