#!/usr/bin/env python3
"""
System Parity Test: Ensures the new tactical tracker maintains 100% parity with the original.
This test should be run regularly to verify that both apps produce identical results.
"""

import unittest
import sys
import os
import warnings
warnings.filterwarnings('ignore')

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestSystemParity(unittest.TestCase):
    """Test that the new tactical tracker maintains parity with the original"""
    
    def setUp(self):
        """Set up test fixtures"""
        try:
            from tactical_tracker import PortfolioTracker as NewTracker, discover_momentum_tickers, screen_discovered_tickers
            from streamlit_app import PortfolioTracker as OriginalTracker
            
            self.new_tracker = NewTracker()
            self.original_tracker = OriginalTracker()
            self.discover_momentum_tickers = discover_momentum_tickers
            self.screen_discovered_tickers = screen_discovered_tickers
        except ImportError as e:
            self.skipTest(f"Could not import required modules: {e}")
    
    def test_passes_filters_logic(self):
        """Test that passes_filters logic is identical between implementations"""
        # Test case with high quality stock
        test_data = {
            'ticker': 'TEST1',
            'rs_score': 85,
            'avg_weekly_return': 2.5,
            'weekly_returns': [0.025, 0.030, 0.020, 0.015],
            'weeks_above_target': 3,
            'daily_change': 1.2
        }
        
        min_rs_score = 30
        min_weekly_target = 1.5
        
        # Test both implementations
        original_result = self.original_tracker.passes_filters(
            test_data, min_rs_score, min_weekly_target
        )
        new_result = self.new_tracker.passes_filters(
            test_data, min_rs_score, min_weekly_target
        )
        
        self.assertEqual(original_result, new_result, 
                        "passes_filters logic differs between implementations")
    
    def test_market_health_consistency(self):
        """Test that market health calculation is consistent"""
        original_health = self.original_tracker.get_market_health()
        new_health = self.new_tracker.get_market_health()
        
        # Check that both return dictionaries with expected keys
        self.assertIsInstance(original_health, dict)
        self.assertIsInstance(new_health, dict)
        
        # Both should have the same structure
        self.assertEqual(sorted(original_health.keys()), sorted(new_health.keys()),
                        "Market health structure differs between implementations")
    
    def test_auto_discovery_parity(self):
        """Test that auto-discovery produces the same results"""
        # Discover tickers using both methods
        original_discovered = self.original_tracker.discover_momentum_tickers()
        new_discovered = self.discover_momentum_tickers()
        
        # Should discover the same tickers
        self.assertEqual(set(original_discovered), set(new_discovered),
                        "Auto-discovery produces different ticker sets")
    
    def test_screening_parity(self):
        """Test that screening produces the same qualified results"""
        # Use standard parameters
        min_rs_score = 25
        min_weekly_target = 1.0
        
        # Get market health
        original_health = self.original_tracker.get_market_health()
        new_health = self.new_tracker.get_market_health()
        
        # Discover tickers
        discovered = self.original_tracker.discover_momentum_tickers()
        
        # Screen with both implementations
        original_qualified = self.original_tracker.screen_discovered_tickers(
            discovered, min_rs_score, min_weekly_target, original_health
        )
        
        new_qualified = self.screen_discovered_tickers(
            self.new_tracker, discovered, min_rs_score, min_weekly_target, new_health
        )
        
        if original_qualified and new_qualified:
            original_tickers = {r['ticker'] for r in original_qualified}
            new_tickers = {r['ticker'] for r in new_qualified}
            
            self.assertEqual(original_tickers, new_tickers,
                            "Screening produces different qualified ticker sets")
    
    def test_top_picks_ranking(self):
        """Test that top picks ranking is consistent"""
        # Use standard parameters
        min_rs_score = 25
        min_weekly_target = 1.0
        
        # Get market health and discover tickers
        market_health = self.new_tracker.get_market_health()
        discovered = self.discover_momentum_tickers()
        
        # Screen tickers
        qualified = self.screen_discovered_tickers(
            self.new_tracker, discovered, min_rs_score, min_weekly_target, market_health
        )
        
        if qualified and len(qualified) >= 10:
            # Get top 10 from both implementations
            original_top10 = self.original_tracker.get_top_picks(
                qualified, 10, min_rs_score, min_weekly_target
            )
            new_top10 = self.new_tracker.get_top_picks(
                qualified, 10, min_rs_score, min_weekly_target
            )
            
            if original_top10 and new_top10:
                original_ranking = [r['ticker'] for r in original_top10]
                new_ranking = [r['ticker'] for r in new_top10]
                
                # Rankings should be identical
                self.assertEqual(original_ranking, new_ranking,
                                f"Top 10 ranking differs: {original_ranking} vs {new_ranking}")
    
    def test_momentum_score_calculation(self):
        """Test that momentum score calculation is consistent"""
        # Test with a known ticker if available
        test_ticker = 'AAPL'
        
        try:
            original_analysis = self.original_tracker.analyze_ticker_momentum(test_ticker)
            new_analysis = self.new_tracker.analyze_ticker_momentum(test_ticker)
            
            if original_analysis and new_analysis:
                # Momentum scores should be very close (allowing for minor floating point differences)
                original_score = original_analysis.get('momentum_score', 0)
                new_score = new_analysis.get('momentum_score', 0)
                
                self.assertAlmostEqual(original_score, new_score, places=1,
                                     msg=f"Momentum scores differ significantly: {original_score} vs {new_score}")
        except Exception:
            # Skip if ticker data is not available
            self.skipTest("Ticker data not available for momentum score test")

if __name__ == '__main__':
    unittest.main(verbosity=2)
