"""
Integration test to ensure the trade suggestion workflow functions correctly.

This test verifies that the entire trade suggestion workflow works correctly,
from generating suggestions to displaying them in the UI.
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.options_tracker import OptionsTracker
import pandas as pd

class TestTradeSuggestionWorkflow(unittest.TestCase):
    
    def setUp(self):
        """Set up the test environment"""
        # Create a real instance of OptionsTracker for testing
        self.tracker = OptionsTracker()
        
        # Mock the watchlist with a small subset for testing
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
            }
        }
    
    def test_generate_trade_suggestions_with_profit_target(self):
        """Test generating trade suggestions with different profit targets"""
        # Test with lower profit target ($0.50/share)
        low_target_suggestions = self.tracker.generate_trade_suggestions(
            num_suggestions=2, 
            min_profit_target=0.5
        )
        
        # Should get suggestions with this low target
        self.assertGreaterEqual(len(low_target_suggestions), 1)
        
        # Verify each suggestion meets minimum profit target
        for suggestion in low_target_suggestions:
            self.assertGreaterEqual(suggestion['profit_target'], 0.5)
            
        # Test with high profit target ($5/share = $500/contract)
        high_target_suggestions = self.tracker.generate_trade_suggestions(
            num_suggestions=2, 
            min_profit_target=5.0
        )
        
        # High target may return fewer suggestions
        if high_target_suggestions:
            # Verify each suggestion meets minimum profit target
            for suggestion in high_target_suggestions:
                self.assertGreaterEqual(suggestion['profit_target'], 5.0)
    
    def test_suggestion_structure(self):
        """Test that trade suggestions have the correct structure for UI display"""
        suggestions = self.tracker.generate_trade_suggestions(
            num_suggestions=1, 
            min_profit_target=0.5
        )
        
        # Make sure we got at least one suggestion
        self.assertGreaterEqual(len(suggestions), 1)
        
        suggestion = suggestions[0]
        
        # Check required fields for UI display
        self.assertIn('ticker', suggestion)
        self.assertIn('strategy', suggestion)
        self.assertIn('expiration', suggestion)
        self.assertIn('credit', suggestion)
        self.assertIn('max_loss', suggestion)
        self.assertIn('profit_target', suggestion)
        self.assertIn('confidence', suggestion)
        
        # Strategy-specific fields
        strategy = suggestion['strategy']
        if strategy == 'Bull Put Spread' or strategy == 'Bear Call Spread':
            # Both spread types have short and long strikes
            self.assertIn('short_strike', suggestion)
            self.assertIn('long_strike', suggestion)
        elif strategy == 'Iron Condor':
            self.assertIn('put_short_strike', suggestion)
            self.assertIn('put_long_strike', suggestion)
            self.assertIn('call_short_strike', suggestion)
            self.assertIn('call_long_strike', suggestion)
        
        # Check for detailed reasoning
        self.assertIn('reasoning', suggestion)
        self.assertGreater(len(suggestion['reasoning']), 50)  # Should be substantial
        
        # Check for leg details
        self.assertIn('legs', suggestion)
        self.assertGreaterEqual(len(suggestion['legs']), 2)  # At least two legs
        
        # Check leg structure
        leg = suggestion['legs'][0]
        self.assertIn('action', leg)
        self.assertIn('type', leg)
        self.assertIn('strike', leg)
        self.assertIn('price', leg)

if __name__ == '__main__':
    unittest.main()
