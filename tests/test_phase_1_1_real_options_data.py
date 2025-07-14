#!/usr/bin/env python3
"""
Test Phase 1.1: Real Options Data Integration
"""

import pandas as pd

# Add the src directory to the path for imports
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from portfolio_suite.options_trading.core import OptionsTracker

class TestPhase11RealOptionsData:
    """Test real options data integration functionality."""
    
    def setup_method(self):
        """Setup test environment."""
        self.tracker = OptionsTracker()
    
    def test_get_tradable_options_chain_real_data(self):
        """Test getting tradable options with real SPY data."""
        print("\n🧪 Testing Phase 1.1: Real Options Data Integration")
        
        # Test with SPY as it always has high liquidity
        result = self.tracker.get_tradable_options_chain("SPY", min_volume=100, max_bid_ask_spread_pct=0.03)
        
        print(f"  📊 Current SPY price: ${result.get('current_price', 'N/A'):.2f}")
        print(f"  📅 Expiration dates available: {len(result.get('expiration_dates', []))}")
        print(f"  📈 Liquid puts available: {result.get('summary', {}).get('liquid_puts_available', 0)}")
        print(f"  📉 Liquid calls available: {result.get('summary', {}).get('liquid_calls_available', 0)}")
        
        # Basic validation
        assert "error" not in result, f"Error getting options data: {result.get('error')}"
        assert "current_price" in result
        assert "expiration_dates" in result
        assert "puts" in result
        assert "calls" in result
        assert "summary" in result
        
        # Validate we have some liquid options
        assert result["summary"]["liquid_puts_available"] > 0, "Should have some liquid puts"
        assert result["summary"]["liquid_calls_available"] > 0, "Should have some liquid calls"
        
        # Check that we have reasonable current price
        current_price = result["current_price"]
        assert 300 < current_price < 800, f"SPY price {current_price} seems unrealistic"
        
        print("  ✅ Real options data integration working correctly")
    
    def test_filter_liquid_options(self):
        """Test the liquidity filtering logic."""
        print("\n🧪 Testing options liquidity filtering")
        
        # Create mock options data
        mock_options = pd.DataFrame({
            "strike": [500, 510, 520, 530, 540],
            "bid": [1.0, 0.5, 0.0, 2.0, 1.5],
            "ask": [1.1, 0.6, 0.1, 2.2, 1.7],
            "volume": [1000, 50, 0, 200, 150],
            "openInterest": [500, 100, 0, 300, 250],
            "impliedVolatility": [0.2, 0.25, 0.3, 0.22, 0.24]
        })
        
        # Filter with strict criteria
        filtered = self.tracker._filter_liquid_options(mock_options, min_volume=100, max_bid_ask_spread_pct=0.15)
        
        print(f"  📊 Original options: {len(mock_options)}")
        print(f"  📊 Liquid options: {len(filtered)}")
        
        # Should have 3 options that meet criteria (strikes 500, 530, 540)
        assert len(filtered) == 3, f"Expected 3 liquid options, got {len(filtered)}"
        
        # Check liquidity scores are calculated
        assert "liquidity_score" in filtered.columns
        assert all(filtered["liquidity_score"] > 0)
        
        print("  ✅ Liquidity filtering working correctly")
    
    def test_liquidity_score_calculation(self):
        """Test the liquidity scoring algorithm."""
        print("\n🧪 Testing liquidity score calculation")
        
        # Create options with different liquidity characteristics
        mock_options = pd.DataFrame({
            "volume": [1000, 100, 50],
            "openInterest": [500, 200, 100],
            "spread_pct": [0.01, 0.05, 0.10]  # 1%, 5%, 10%
        })
        
        scores = self.tracker._calculate_liquidity_score(mock_options)
        
        print(f"  📊 Liquidity scores: {scores.tolist()}")
        
        # High volume/OI, tight spread should score highest
        assert scores.iloc[0] > scores.iloc[1] > scores.iloc[2], "Scores should decrease with liquidity"
        
        # All scores should be between 0 and 100
        assert all(0 <= score <= 100 for score in scores)
        
        print("  ✅ Liquidity scoring working correctly")
    
    def test_options_summary_generation(self):
        """Test the options summary generation."""
        print("\n🧪 Testing options summary generation")
        
        # Create mock tradable options data
        mock_puts = pd.DataFrame({
            "liquidity_score": [80, 75, 70]
        })
        
        mock_calls = pd.DataFrame({
            "liquidity_score": [85, 90, 65]
        })
        
        tradable_options = {
            "expiration_dates": ["2024-01-19", "2024-01-26"],
            "puts": {"2024-01-19": mock_puts},
            "calls": {"2024-01-19": mock_calls}
        }
        
        summary = self.tracker._generate_options_summary(tradable_options)
        
        print(f"  📊 Summary: {summary}")
        
        assert summary["total_expiration_dates"] == 2
        assert summary["liquid_puts_available"] == 3
        assert summary["liquid_calls_available"] == 3
        assert abs(summary["avg_put_liquidity_score"] - 75.0) < 0.1
        assert abs(summary["avg_call_liquidity_score"] - 80.0) < 0.1
        
        print("  ✅ Options summary generation working correctly")
    
    def test_error_handling(self):
        """Test error handling for invalid tickers."""
        print("\n🧪 Testing error handling")
        
        # Test with invalid ticker
        result = self.tracker.get_tradable_options_chain("INVALID_TICKER_XYZ")
        
        # Should handle gracefully
        assert "error" in result or len(result.get("puts", {})) == 0
        
        print("  ✅ Error handling working correctly")

def main():
    """Run the Phase 1.1 tests."""
    print("🚀 Running Phase 1.1: Real Options Data Integration Tests")
    print("=" * 60)
    
    # Create test instance
    test_instance = TestPhase11RealOptionsData()
    test_instance.setup_method()
    
    try:
        # Run each test
        test_instance.test_get_tradable_options_chain_real_data()
        test_instance.test_filter_liquid_options()
        test_instance.test_liquidity_score_calculation() 
        test_instance.test_options_summary_generation()
        test_instance.test_error_handling()
        
        print("\n" + "=" * 60)
        print("✅ All Phase 1.1 tests passed! Real options data integration working correctly.")
        print("📋 Phase 1.1 Complete - Ready to commit")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Phase 1.1 test failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
