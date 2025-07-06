import sys
import os
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.options_tracker import OptionsTracker

class TestProfitTargetFilter(unittest.TestCase):
    """Test the profit target filter with different thresholds"""
    
    def setUp(self):
        """Set up the test environment"""
        self.tracker = OptionsTracker()
        
    def test_profit_target_filter(self):
        """Test that the profit target filter correctly filters suggestions"""
        # Make sure we have a good variety of tickers
        self.assertGreaterEqual(len(self.tracker.watchlist), 10)
        
        # Test with different profit targets
        profit_targets = [0.5, 1.0, 2.0]
        
        for target in profit_targets:
            with self.subTest(f"Testing profit target: ${target:.2f}/share"):
                suggestions = self.tracker.generate_trade_suggestions(num_suggestions=3, min_profit_target=target)
                
                # Skip validation if no suggestions (may happen for very high targets)
                if not suggestions:
                    continue
                
                # Check profit targets meet minimum requirement
                for suggestion in suggestions:
                    self.assertGreaterEqual(
                        suggestion['profit_target'], 
                        target,
                        f"Suggestion for {suggestion['ticker']} {suggestion['strategy']} has profit target ${suggestion['profit_target']:.2f}, below minimum ${target:.2f}"
                    )
                
                # Verify strategy structure
                for suggestion in suggestions:
                    self.assertIn('strategy', suggestion)
                    self.assertIn(suggestion['strategy'], self.tracker.strategy_types)
    
    def test_profit_target_distribution(self):
        """Test that profit targets are distributed reasonably"""
        # Use a low profit target to ensure we get suggestions
        suggestions = self.tracker.generate_trade_suggestions(num_suggestions=5, min_profit_target=0.5)
        
        if not suggestions:
            self.skipTest("No suggestions generated, unable to verify profit target distribution")
        
        # Extract profit targets
        profit_targets = [s['profit_target'] for s in suggestions]
        
        # Check profit target range is reasonable
        min_profit = min(profit_targets)
        
        # Min profit should be >= 0.5 (our test minimum)
        self.assertGreaterEqual(min_profit, 0.5)
        
        # Make sure we have strategy diversity
        strategies = {s['strategy'] for s in suggestions}
        self.assertGreaterEqual(len(strategies), 1, "Should have at least one strategy type")

if __name__ == "__main__":
    unittest.main()
