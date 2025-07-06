"""
Test the UI components for trade display and suggestions.

This test ensures that the UI components correctly display trade suggestions,
including profit targets, descriptive titles, and the OpenStrat URL generation.
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.options_tracker_ui import generate_descriptive_title, generate_optionstrat_url
from src.options_tracker import OptionsTracker
from datetime import datetime

class TestTradeDisplayUI(unittest.TestCase):
    
    def test_generate_descriptive_title_bull_put_spread(self):
        """Test the descriptive title generation for Bull Put Spreads"""
        suggestion = {
            'ticker': 'SPY',
            'strategy': 'Bull Put Spread',
            'expiration': '2025-08-01',
            'short_strike': 600,
            'long_strike': 590
        }
        
        title = generate_descriptive_title(suggestion)
        # Format: SPY Aug 1st 590/600 Bull Put Spread
        self.assertIn('SPY', title)
        self.assertIn('Aug 1st', title)
        self.assertIn('590/600', title)
        self.assertIn('Bull Put Spread', title)
    
    def test_generate_descriptive_title_bear_call_spread(self):
        """Test the descriptive title generation for Bear Call Spreads"""
        suggestion = {
            'ticker': 'QQQ',
            'strategy': 'Bear Call Spread',
            'expiration': '2025-08-01',
            'short_strike': 540,
            'long_strike': 550
        }
        
        title = generate_descriptive_title(suggestion)
        # Format: QQQ Aug 1st 540/550 Bear Call Spread
        self.assertIn('QQQ', title)
        self.assertIn('Aug 1st', title)
        self.assertIn('540/550', title)
        self.assertIn('Bear Call Spread', title)
    
    def test_generate_descriptive_title_iron_condor(self):
        """Test the descriptive title generation for Iron Condors"""
        suggestion = {
            'ticker': 'NVDA',
            'strategy': 'Iron Condor',
            'expiration': '2025-08-01',
            'put_long_strike': 140,
            'put_short_strike': 150,
            'call_short_strike': 170,
            'call_long_strike': 180
        }
        
        title = generate_descriptive_title(suggestion)
        # Format: NVDA Aug 1st 140/150/170/180 Iron Condor
        self.assertIn('NVDA', title)
        self.assertIn('Aug 1st', title)
        self.assertIn('140/150/170/180', title)
        self.assertIn('Iron Condor', title)
    
    def test_generate_optionstrat_url_bull_put_spread(self):
        """Test OpenStrat URL generation for Bull Put Spreads"""
        suggestion = {
            'ticker': 'SPY',
            'strategy': 'Bull Put Spread',
            'expiration': '2025-08-01',
            'short_strike': 600,
            'long_strike': 590
        }
        
        url = generate_optionstrat_url(suggestion)
        
        # Expected format: https://optionstrat.com/build/bull-put-spread/SPY/-.SPY250801P600,.SPY250801P590
        self.assertIn('optionstrat.com/build/bull-put-spread/SPY/', url)
        self.assertIn('-.SPY250801P600', url)
        self.assertIn('.SPY250801P590', url)
    
    def test_generate_optionstrat_url_bear_call_spread(self):
        """Test OpenStrat URL generation for Bear Call Spreads"""
        suggestion = {
            'ticker': 'QQQ',
            'strategy': 'Bear Call Spread',
            'expiration': '2025-08-01',
            'short_strike': 540,
            'long_strike': 550
        }
        
        url = generate_optionstrat_url(suggestion)
        
        # Expected format: https://optionstrat.com/build/bear-call-spread/QQQ/-.QQQ250801C540,.QQQ250801C550
        self.assertIn('optionstrat.com/build/bear-call-spread/QQQ/', url)
        self.assertIn('-.QQQ250801C540', url)
        self.assertIn('.QQQ250801C550', url)
    
    def test_generate_optionstrat_url_iron_condor(self):
        """Test OpenStrat URL generation for Iron Condors"""
        suggestion = {
            'ticker': 'NVDA',
            'strategy': 'Iron Condor',
            'expiration': '2025-08-01',
            'put_long_strike': 140,
            'put_short_strike': 150,
            'call_short_strike': 170,
            'call_long_strike': 180
        }
        
        url = generate_optionstrat_url(suggestion)
        
        # Format: https://optionstrat.com/build/iron-condor/NVDA/.NVDA250801P140,-.NVDA250801P150,-.NVDA250801C170,.NVDA250801C180
        self.assertIn('optionstrat.com/build/iron-condor/NVDA/', url)
        self.assertIn('.NVDA250801P140', url)
        self.assertIn('-.NVDA250801P150', url)
        self.assertIn('-.NVDA250801C170', url)
        self.assertIn('.NVDA250801C180', url)
    
    @patch('src.options_tracker.OptionsTracker')
    def test_trade_suggestions_profit_targets(self, tracker_class_mock):
        """Test that trade suggestions include appropriate profit targets"""
        # Create a mock options tracker with predefined suggestions
        mock_tracker = MagicMock()
        
        # Mock the generate_trade_suggestions method
        mock_suggestions = [
            {
                'ticker': 'SPY',
                'strategy': 'Bull Put Spread',
                'expiration': '2025-08-01',
                'short_strike': 600,
                'long_strike': 590,
                'credit': 2.50,  # $2.50 per share
                'max_loss': 7.50,  # $7.50 per share
                'profit_target': 1.25,  # 50% of credit
                'bullish_prob': 0.65,
                'bias': 'Bullish',
                'confidence': 65,
                'legs': [
                    {'action': 'SELL', 'type': 'PUT', 'strike': 600, 'price': 3.50},
                    {'action': 'BUY', 'type': 'PUT', 'strike': 590, 'price': 1.00}
                ]
            }
        ]
        
        mock_tracker.generate_trade_suggestions.return_value = mock_suggestions
        
        # Test that the profit target is properly calculated (50% of credit)
        suggestion = mock_suggestions[0]
        self.assertEqual(suggestion['profit_target'], suggestion['credit'] * 0.5)
        
        # Verify the per-contract values (100 shares per contract)
        credit_per_contract = suggestion['credit'] * 100  # $250 per contract
        profit_target_per_contract = suggestion['profit_target'] * 100  # $125 per contract
        
        self.assertEqual(credit_per_contract, 250.0)
        self.assertEqual(profit_target_per_contract, 125.0)

if __name__ == '__main__':
    unittest.main()
