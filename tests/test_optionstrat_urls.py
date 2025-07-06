#!/usr/bin/env python3
"""
OptionStrat URL Generation Test
==============================

Test to verify that OptionStrat URLs are generated correctly, including proper handling
of half-dollar strikes like 172.50, which should appear as 172.5 in the URL.
"""

import sys
import os
import unittest
# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.options_tracker_ui import generate_optionstrat_url

class TestOptionStratURLs(unittest.TestCase):
    """Test OptionStrat URL generation for all strategies with various strike formats"""
    
    def test_iron_condor_url(self):
        """Test URL generation for Iron Condor with mixed strike formats"""
        # Test with half-dollar strikes (172.5)
        iron_condor = {
            'ticker': 'NVDA',
            'strategy': 'Iron Condor',
            'expiration': '2025-08-01',
            'put_long_strike': 146.0,  # Whole dollar
            'put_short_strike': 150.0,  # Whole dollar
            'call_short_strike': 170.0,  # Whole dollar
            'call_long_strike': 172.5   # Half dollar
        }
        
        url = generate_optionstrat_url(iron_condor)
        expected_url = 'https://optionstrat.com/build/iron-condor/NVDA/.NVDA250801P146,-.NVDA250801P150,-.NVDA250801C170,.NVDA250801C172.5'
        
        # Check that URL is generated correctly
        self.assertEqual(url, expected_url)
        
        # Verify half-dollar strike is preserved as 172.5, not 172.50
        self.assertIn('172.5', url)
        self.assertNotIn('172.50', url)
    
    def test_iron_condor_with_quarter_strikes(self):
        """Test URL generation for Iron Condor with quarter-dollar strikes"""
        iron_condor = {
            'ticker': 'NVDA',
            'strategy': 'Iron Condor',
            'expiration': '2025-08-01',
            'put_long_strike': 146.0,   # Whole dollar
            'put_short_strike': 150.0,  # Whole dollar
            'call_short_strike': 170.25, # Quarter dollar
            'call_long_strike': 172.75  # Quarter dollar
        }
        
        url = generate_optionstrat_url(iron_condor)
        
        # Verify quarter-dollar strikes are preserved correctly
        self.assertIn('170.25', url)
        self.assertIn('172.75', url)
    
    def test_bull_put_spread_url(self):
        """Test URL generation for Bull Put Spread"""
        bull_put = {
            'ticker': 'AAPL',
            'strategy': 'Bull Put Spread',
            'expiration': '2025-08-01',
            'short_strike': 217.5,  # Half dollar
            'long_strike': 215.0    # Whole dollar
        }
        
        url = generate_optionstrat_url(bull_put)
        expected_url = 'https://optionstrat.com/build/bull-put-spread/AAPL/-.AAPL250801P217.5,.AAPL250801P215'
        
        self.assertEqual(url, expected_url)
    
    def test_bear_call_spread_url(self):
        """Test URL generation for Bear Call Spread"""
        bear_call = {
            'ticker': 'QQQ',
            'strategy': 'Bear Call Spread',
            'expiration': '2025-08-01',
            'short_strike': 572.5,  # Half dollar
            'long_strike': 575.0    # Whole dollar
        }
        
        url = generate_optionstrat_url(bear_call)
        expected_url = 'https://optionstrat.com/build/bear-call-spread/QQQ/-.QQQ250801C572.5,.QQQ250801C575'
        
        self.assertEqual(url, expected_url)

if __name__ == "__main__":
    unittest.main()
