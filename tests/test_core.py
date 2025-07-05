"""
Unit tests for the PortfolioTracker class - Core Methods
Tests covering filtering, parameter validation, and core logic
"""

import unittest
from unittest.mock import patch, Mock, MagicMock
import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Add parent directory to path to import the main module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.streamlit_app import PortfolioTracker

class TestPortfolioTrackerCore(unittest.TestCase):
    """Test core functionality of PortfolioTracker"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.tracker = PortfolioTracker()
        
        # Sample ticker result for testing - meets Elite Momentum criteria
        self.sample_result = {
            'ticker': 'AAPL',
            'rs_score': 75.0,
            'avg_weekly_return': 2.8,  # Avg 2.8% to meet Elite threshold
            'market_cap': 3e12,
            'meets_criteria': True,
            'qualification_reason': 'Elite momentum',
            'weekly_returns': [0.035, 0.025, 0.030, 0.020],  # 3.5%, 2.5%, 3.0%, 2.0%
            'weeks_above_target': 3,  # 3 weeks >2%
            'daily_change': 1.5,
            'price': 150.0,
            'volume': 50000000
        }
        
        # Non-qualifying example
        self.weak_result = {
            'ticker': 'WEAK',
            'rs_score': 45.0,
            'avg_weekly_return': 0.25,  # Low avg return
            'market_cap': 1e10,
            'meets_criteria': False,
            'qualification_reason': 'Weak momentum',
            'weekly_returns': [0.015, 0.010, 0.005, -0.020],  # 1.5%, 1.0%, 0.5%, -2.0%
            'weeks_above_target': 0,  # 0 weeks >2%
            'daily_change': -0.5,
            'price': 50.0,
            'volume': 10000000
        }
        
    def test_passes_filters_valid_ticker(self):
        """Test passes_filters with valid ticker data that meets Elite Momentum criteria"""
        result = self.tracker.passes_filters(
            self.sample_result, 
            min_rs_score=70, 
            min_weekly_target=2.5  # Raised to match Elite criteria
        )
        self.assertTrue(result)
        
    def test_passes_filters_low_rs_score(self):
        """Test passes_filters rejects low RS score"""
        result = self.tracker.passes_filters(
            self.weak_result,  # Use weak example with RS score 45
            min_rs_score=70, 
            min_weekly_target=1.5
        )
        self.assertFalse(result)
        self.assertIn('RS Score too low', self.weak_result['qualification_reason'])
        
    def test_passes_filters_low_weekly_return(self):
        """Test passes_filters rejects low weekly return"""
        result = self.tracker.passes_filters(
            self.weak_result,  # Use weak example with 0.25% avg return
            min_rs_score=30,  # Lower than weak_result's 45
            min_weekly_target=1.5
        )
        self.assertFalse(result)
        self.assertIn('Weekly return too low', self.weak_result['qualification_reason'])
        
    def test_passes_filters_small_market_cap(self):
        """Test passes_filters - market cap is not checked in this method"""
        small_cap_result = self.sample_result.copy()
        small_cap_result['market_cap'] = 3e9  # $3B < $5B threshold
        
        # passes_filters doesn't check market cap, only tactical criteria
        result = self.tracker.passes_filters(
            small_cap_result, 
            min_rs_score=70, 
            min_weekly_target=2.0
        )
        self.assertTrue(result)  # Should pass since market cap isn't checked here
        
    def test_passes_filters_doesnt_meet_criteria(self):
        """Test passes_filters rejects ticker that doesn't meet tactical criteria"""
        no_criteria_result = self.sample_result.copy()
        no_criteria_result['meets_criteria'] = False
        no_criteria_result['weekly_returns'] = [0.005, 0.003, 0.002, 0.001]  # Very low returns: 0.5%, 0.3%, 0.2%, 0.1%
        no_criteria_result['avg_weekly_return'] = 0.275  # 0.275% average 
        no_criteria_result['weeks_above_target'] = 0
        
        result = self.tracker.passes_filters(
            no_criteria_result, 
            min_rs_score=70, 
            min_weekly_target=2.0
        )
        # Should fail because avg_weekly_return 0.275% < min_weekly_target 2.0%
        self.assertFalse(result)
        self.assertIn('Weekly return too low', no_criteria_result['qualification_reason'])
        
    def test_get_top_picks_basic(self):
        """Test get_top_picks returns correct number of results"""
        results = [
            {
                'ticker': 'AAPL', 'rs_score': 85, 'avg_weekly_return': 3.0, 'market_cap': 3e12, 
                'meets_criteria': True, 'weeks_above_target': 4, 'daily_change': 1.5,
                'weekly_returns': [0.03, 0.025, 0.035, 0.028]
            },
            {
                'ticker': 'MSFT', 'rs_score': 80, 'avg_weekly_return': 2.8, 'market_cap': 2.5e12, 
                'meets_criteria': True, 'weeks_above_target': 3, 'daily_change': 1.2,
                'weekly_returns': [0.028, 0.032, 0.025, 0.031]
            },
            {
                'ticker': 'GOOGL', 'rs_score': 75, 'avg_weekly_return': 2.5, 'market_cap': 1.8e12, 
                'meets_criteria': True, 'weeks_above_target': 3, 'daily_change': 0.8,
                'weekly_returns': [0.025, 0.022, 0.028, 0.025]
            },
        ]
        
        with patch.object(self.tracker, 'passes_filters', return_value=True):
            top_picks = self.tracker.get_top_picks(results, count=2)
            self.assertEqual(len(top_picks), 2)
            self.assertEqual(top_picks[0]['ticker'], 'AAPL')  # Highest momentum score
            
    def test_get_top_picks_filtering(self):
        """Test get_top_picks properly filters results"""
        results = [
            {
                'ticker': 'AAPL', 'rs_score': 85, 'avg_weekly_return': 3.0, 'market_cap': 3e12, 
                'meets_criteria': True, 'weeks_above_target': 4, 'daily_change': 1.5,
                'weekly_returns': [0.03, 0.025, 0.035, 0.028]
            },
            {
                'ticker': 'WEAK', 'rs_score': 25, 'avg_weekly_return': 0.5, 'market_cap': 1e11, 
                'meets_criteria': False, 'weeks_above_target': 0, 'daily_change': -0.5,
                'weekly_returns': [0.005, -0.002, 0.001, 0.003]
            },
        ]
        
        # Mock passes_filters to return True only for AAPL
        def mock_passes_filters(result, min_rs_score, min_weekly_target):
            return result['ticker'] == 'AAPL'
            
        with patch.object(self.tracker, 'passes_filters', side_effect=mock_passes_filters):
            top_picks = self.tracker.get_top_picks(results, count=5, min_rs_score=70, min_weekly_target=2.0)
            self.assertEqual(len(top_picks), 1)
            self.assertEqual(top_picks[0]['ticker'], 'AAPL')
            
    def test_get_position_status_strong_gain(self):
        """Test position status for strong gains"""
        status, color = self.tracker.get_position_status(3.5)
        self.assertEqual(status, "🚀 STRONG")
        self.assertEqual(color, "success")
        
    def test_get_position_status_watch_drop(self):
        """Test position status for watch-level drops"""
        status, color = self.tracker.get_position_status(-2.0)
        self.assertEqual(status, "⚠️ WATCH")
        self.assertEqual(color, "warning")
        
    def test_get_position_status_exit_drop(self):
        """Test position status for exit-level drops"""
        status, color = self.tracker.get_position_status(-4.0)
        self.assertEqual(status, "🚨 EXIT")
        self.assertEqual(color, "danger")
        
    def test_get_position_status_normal(self):
        """Test position status for normal movement"""
        status, color = self.tracker.get_position_status(0.5)
        self.assertEqual(status, "✅ HOLD")
        self.assertEqual(color, "info")

class TestMarketHealthAnalysis(unittest.TestCase):
    """Test market health analysis functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.tracker = PortfolioTracker()
        
    @patch('streamlit_app.yf.download')
    def test_get_market_health_aggressive(self, mock_yf_download):
        """Test market health analysis for aggressive market conditions"""
        # Mock market data indicating healthy conditions
        mock_vix_data = pd.DataFrame({
            'Close': [15.0, 14.5, 16.0]  # Low VIX
        }, index=pd.date_range('2025-06-28', periods=3))
        
        mock_spy_data = pd.DataFrame({
            'Close': [500, 505, 510],  # Uptrending SPY
            'Volume': [100000, 110000, 105000]
        }, index=pd.date_range('2025-06-28', periods=3))
        
        def mock_download_side_effect(ticker, **kwargs):
            if ticker == '^VIX':
                return mock_vix_data
            elif ticker == 'SPY':
                return mock_spy_data
            return pd.DataFrame()
            
        mock_yf_download.side_effect = mock_download_side_effect
        
        market_health = self.tracker.get_market_health()
        
        self.assertIsInstance(market_health, dict)
        self.assertIn('market_regime', market_health)
        self.assertIn('is_defensive', market_health)
        self.assertIn('defensive_score', market_health)
        
    @patch('streamlit_app.yf.Ticker')
    def test_get_market_health_defensive(self, mock_ticker):
        """Test market health analysis returns proper structure"""
        # Mock YFinance Ticker to return defensive data
        mock_vix_ticker = Mock()
        mock_spy_ticker = Mock()
        mock_sector_ticker = Mock()
        
        # VIX data showing high fear
        vix_dates = pd.date_range('2025-06-20', periods=10)
        vix_data = pd.DataFrame({
            'Close': [35, 38, 40, 37, 35, 38, 41, 39, 36, 40]  # High VIX values
        }, index=vix_dates)
        
        # SPY data showing decline below moving averages  
        spy_dates = pd.date_range('2025-04-01', periods=100)
        spy_prices = [500 - i * 1.0 for i in range(100)]  # Strong decline
        spy_data = pd.DataFrame({
            'Close': spy_prices
        }, index=spy_dates)
        
        # Sector data showing weakness
        sector_dates = pd.date_range('2025-06-10', periods=20)
        sector_data = pd.DataFrame({
            'Close': [100 - i * 0.5 for i in range(20)]  # Declining sectors
        }, index=sector_dates)
        
        def ticker_side_effect(symbol):
            if symbol == '^VIX':
                mock_vix_ticker.history.return_value = vix_data
                return mock_vix_ticker
            elif symbol == 'SPY':
                mock_spy_ticker.history.return_value = spy_data
                return mock_spy_ticker
            else:  # Sector ETFs
                mock_sector_ticker.history.return_value = sector_data
                return mock_sector_ticker
                
        mock_ticker.side_effect = ticker_side_effect
        
        market_health = self.tracker.get_market_health()
        
        # Just verify it returns the expected structure
        self.assertIsInstance(market_health, dict)
        self.assertIn('is_defensive', market_health)
        self.assertIn('defensive_score', market_health)
        self.assertIn('market_regime', market_health)
        
        # With the mocked data, should be defensive (high VIX, declining SPY, weak sectors)
        self.assertTrue(market_health.get('is_defensive', False))
        
    def test_get_defensive_criteria_aggressive(self):
        """Test defensive criteria for aggressive market"""
        market_health = {
            'market_regime': 'AGGRESSIVE',
            'is_defensive': False,
            'defensive_score': 20
        }
        
        criteria = self.tracker.get_defensive_criteria(market_health)
        
        self.assertEqual(criteria['max_results'], 25)
        self.assertEqual(criteria['min_rs_score'], 20)
        self.assertEqual(criteria['min_weekly_target'], 1.2)
        
    def test_get_defensive_criteria_defensive(self):
        """Test defensive criteria for defensive market"""
        market_health = {
            'market_regime': 'DEFENSIVE',
            'is_defensive': True,
            'defensive_score': 60
        }
        
        criteria = self.tracker.get_defensive_criteria(market_health)
        
        self.assertEqual(criteria['max_results'], 8)
        self.assertEqual(criteria['min_rs_score'], 35)
        self.assertEqual(criteria['min_weekly_target'], 0.8)
        
    def test_get_defensive_criteria_highly_defensive(self):
        """Test defensive criteria for highly defensive market"""
        market_health = {
            'market_regime': 'HIGHLY_DEFENSIVE',
            'is_defensive': True,
            'defensive_score': 80
        }
        
        criteria = self.tracker.get_defensive_criteria(market_health)
        
        self.assertEqual(criteria['max_results'], 5)
        self.assertEqual(criteria['min_rs_score'], 40)
        self.assertEqual(criteria['min_weekly_target'], 0.5)

if __name__ == '__main__':
    unittest.main()
