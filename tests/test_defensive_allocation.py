"""
Tests for defensive cash allocation functionality.
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to sys.path to import streamlit_app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from streamlit_app import PortfolioTracker


class TestDefensiveCashAllocation(unittest.TestCase):
    """Test defensive cash allocation in different market conditions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tracker = PortfolioTracker()
        
        # Mock stock data
        self.strong_buys = [
            {
                'ticker': 'AAPL',
                'momentum_score': 16.5,
                'avg_weekly_return': 2.5
            },
            {
                'ticker': 'MSFT', 
                'momentum_score': 17.2,
                'avg_weekly_return': 2.8
            }
        ]
        
        self.moderate_buys = [
            {
                'ticker': 'GOOGL',
                'momentum_score': 12.1,
                'avg_weekly_return': 1.8
            },
            {
                'ticker': 'NVDA',
                'momentum_score': 13.4,
                'avg_weekly_return': 2.1
            }
        ]
    
    def test_aggressive_market_no_cash(self):
        """Test that aggressive market allocates 100% to stocks."""
        market_health = {
            'market_regime': 'AGGRESSIVE',
            'defensive_score': 0
        }
        
        allocation = self.tracker.calculate_simple_allocation(
            self.strong_buys, self.moderate_buys,
            strong_buy_weight=12, moderate_buy_weight=6,
            market_health=market_health, allow_cash=True
        )
        
        self.assertEqual(allocation['defensive_cash'], 0)
        self.assertEqual(allocation['total_allocated'], 100)
        self.assertEqual(allocation['market_regime'], 'AGGRESSIVE')
        self.assertEqual(len(allocation['allocations']), 4)
    
    def test_cautious_market_small_cash(self):
        """Test that cautious market holds 5% cash."""
        market_health = {
            'market_regime': 'CAUTIOUS',
            'defensive_score': 25
        }
        
        allocation = self.tracker.calculate_simple_allocation(
            self.strong_buys, self.moderate_buys,
            strong_buy_weight=12, moderate_buy_weight=6,
            market_health=market_health, allow_cash=True
        )
        
        self.assertEqual(allocation['defensive_cash'], 5)
        self.assertEqual(allocation['total_allocated'], 95)
        self.assertEqual(allocation['market_regime'], 'CAUTIOUS')
        self.assertEqual(allocation['target_stock_allocation'], 95)
    
    def test_defensive_market_moderate_cash(self):
        """Test that defensive market holds 15% cash."""
        market_health = {
            'market_regime': 'DEFENSIVE',
            'defensive_score': 50
        }
        
        allocation = self.tracker.calculate_simple_allocation(
            self.strong_buys, self.moderate_buys,
            strong_buy_weight=12, moderate_buy_weight=6,
            market_health=market_health, allow_cash=True
        )
        
        self.assertEqual(allocation['defensive_cash'], 15)
        self.assertEqual(allocation['total_allocated'], 85)
        self.assertEqual(allocation['market_regime'], 'DEFENSIVE')
        self.assertEqual(allocation['target_stock_allocation'], 85)
    
    def test_highly_defensive_market_high_cash(self):
        """Test that highly defensive market holds 30% cash."""
        market_health = {
            'market_regime': 'HIGHLY_DEFENSIVE',
            'defensive_score': 75
        }
        
        allocation = self.tracker.calculate_simple_allocation(
            self.strong_buys, self.moderate_buys,
            strong_buy_weight=12, moderate_buy_weight=6,
            market_health=market_health, allow_cash=True
        )
        
        self.assertEqual(allocation['defensive_cash'], 30)
        self.assertEqual(allocation['total_allocated'], 70)
        self.assertEqual(allocation['market_regime'], 'HIGHLY_DEFENSIVE')
        self.assertEqual(allocation['target_stock_allocation'], 70)
    
    def test_disable_cash_allocation(self):
        """Test that cash allocation can be disabled."""
        market_health = {
            'market_regime': 'HIGHLY_DEFENSIVE',
            'defensive_score': 75
        }
        
        allocation = self.tracker.calculate_simple_allocation(
            self.strong_buys, self.moderate_buys,
            strong_buy_weight=12, moderate_buy_weight=6,
            market_health=market_health, allow_cash=False
        )
        
        self.assertEqual(allocation['defensive_cash'], 0)
        self.assertEqual(allocation['total_allocated'], 100)
        self.assertEqual(allocation['market_regime'], 'HIGHLY_DEFENSIVE')
    
    def test_no_market_health_data(self):
        """Test behavior when no market health data is provided."""
        allocation = self.tracker.calculate_simple_allocation(
            self.strong_buys, self.moderate_buys,
            strong_buy_weight=12, moderate_buy_weight=6,
            market_health=None, allow_cash=True
        )
        
        self.assertEqual(allocation['defensive_cash'], 0)
        self.assertEqual(allocation['total_allocated'], 100)
        self.assertEqual(allocation['market_regime'], 'AGGRESSIVE')
    
    def test_allocation_sums_to_100_percent(self):
        """Test that stock allocation + defensive cash always equals 100%."""
        market_conditions = [
            {'market_regime': 'AGGRESSIVE', 'defensive_score': 0},
            {'market_regime': 'CAUTIOUS', 'defensive_score': 25},
            {'market_regime': 'DEFENSIVE', 'defensive_score': 50},
            {'market_regime': 'HIGHLY_DEFENSIVE', 'defensive_score': 75}
        ]
        
        for market_health in market_conditions:
            allocation = self.tracker.calculate_simple_allocation(
                self.strong_buys, self.moderate_buys,
                strong_buy_weight=12, moderate_buy_weight=6,
                market_health=market_health, allow_cash=True
            )
            
            total = allocation['total_allocated'] + allocation['defensive_cash']
            self.assertEqual(total, 100, 
                           f"Total allocation should be 100% for {market_health['market_regime']}")
    
    def test_empty_portfolios_with_defensive_cash(self):
        """Test defensive cash allocation with empty portfolios."""
        market_health = {
            'market_regime': 'HIGHLY_DEFENSIVE',
            'defensive_score': 75
        }
        
        allocation = self.tracker.calculate_simple_allocation(
            [], [],  # Empty portfolios
            strong_buy_weight=12, moderate_buy_weight=6,
            market_health=market_health, allow_cash=True
        )
        
        self.assertEqual(allocation['defensive_cash'], 100)
        self.assertEqual(allocation['total_allocated'], 0)
        self.assertEqual(allocation['num_positions'], 0)
        self.assertEqual(len(allocation['allocations']), 0)
    
    def test_generate_recommendations_with_market_health(self):
        """Test that generate_portfolio_recommendations properly uses market health."""
        mock_results = [
            {
                'ticker': 'AAPL',
                'momentum_score': 16.5,
                'avg_weekly_return': 2.5,
                'rs_score': 85,
                'current_price': 150.0,
                'name': 'Apple Inc.',
                'daily_change': 1.2,
                'market_cap': 2000000000000,
                'weeks_data': [2.1, 2.3, 2.8, 2.2, 2.6]
            },
            {
                'ticker': 'MSFT',
                'momentum_score': 17.2,
                'avg_weekly_return': 2.8,
                'rs_score': 88,
                'current_price': 300.0,
                'name': 'Microsoft Corporation',
                'daily_change': 0.8,
                'market_cap': 2200000000000,
                'weeks_data': [2.5, 2.9, 3.1, 2.7, 2.8]
            }
        ]
        
        market_health = {
            'market_regime': 'DEFENSIVE',
            'defensive_score': 50
        }
        
        # Mock the historical data loading to avoid file system dependency
        with patch.object(self.tracker, 'load_historical_results', return_value=[]):
            recommendations = self.tracker.generate_portfolio_recommendations(
                mock_results, portfolio_size=10, 
                min_rs_score=30, min_weekly_target=1.5,
                market_health=market_health
            )
        
        allocation = recommendations['allocation']
        
        # Check the allocation regardless of qualifying positions
        self.assertEqual(allocation['market_regime'], 'DEFENSIVE')
        
        # If we have qualifying positions, expect specific allocation
        if len(recommendations['strong_buys']) + len(recommendations['moderate_buys']) > 0:
            self.assertEqual(allocation['defensive_cash'], 15)
            self.assertLess(allocation['total_allocated'], 100)
        else:
            # If no qualifying positions, all goes to defensive cash
            self.assertEqual(allocation['defensive_cash'], 100)
            self.assertEqual(allocation['total_allocated'], 0)


if __name__ == '__main__':
    unittest.main()
