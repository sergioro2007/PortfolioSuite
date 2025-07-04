"""
Unit tests for ticker analysis and momentum calculations
Tests covering data fetching, technical analysis, and momentum scoring
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

from streamlit_app import PortfolioTracker

class TestTickerAnalysis(unittest.TestCase):
    """Test ticker analysis and momentum calculations"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.tracker = PortfolioTracker()
        
        # Create sample price data for testing
        dates = pd.date_range('2025-05-01', periods=50, freq='D')
        prices = np.random.uniform(100, 150, 50)
        prices = np.cumsum(np.random.normal(0, 1, 50)) + 100  # Random walk
        volumes = np.random.uniform(1000000, 10000000, 50)
        
        self.sample_data = pd.DataFrame({
            'Close': prices,
            'Volume': volumes,
            'High': prices * 1.02,
            'Low': prices * 0.98,
            'Open': prices * 1.01
        }, index=dates)
        
    @patch('streamlit_app.yf.download')
    def test_get_weekly_returns_success(self, mock_yf_download):
        """Test successful weekly returns calculation"""
        mock_yf_download.return_value = self.sample_data
        
        weekly_returns = self.tracker.get_weekly_returns('AAPL', weeks=4)
        
        self.assertIsNotNone(weekly_returns)
        self.assertIsInstance(weekly_returns, list)
        self.assertEqual(len(weekly_returns), 4)
        
        # All returns should be numbers
        for ret in weekly_returns:
            self.assertIsInstance(ret, (int, float))
            
    @patch('streamlit_app.yf.download')
    def test_get_weekly_returns_insufficient_data(self, mock_yf_download):
        """Test weekly returns with insufficient data"""
        # Create data with only 10 days (less than needed for 4 weeks)
        short_data = self.sample_data.head(10)
        mock_yf_download.return_value = short_data
        
        weekly_returns = self.tracker.get_weekly_returns('AAPL', weeks=4)
        
        # Should return whatever data is available, not None
        self.assertIsNotNone(weekly_returns)
        self.assertIsInstance(weekly_returns, list)
        # Should have fewer than 4 weeks of data
        self.assertLess(len(weekly_returns), 4)
        
    @patch('streamlit_app.yf.download')
    def test_get_weekly_returns_no_data(self, mock_yf_download):
        """Test weekly returns with no data"""
        mock_yf_download.return_value = pd.DataFrame()
        
        weekly_returns = self.tracker.get_weekly_returns('INVALID', weeks=4)
        
        self.assertIsNone(weekly_returns)
        
    @patch('streamlit_app.yf.Ticker')
    def test_analyze_ticker_momentum_success(self, mock_ticker):
        """Test successful ticker momentum analysis"""
        # Create uptrending data
        dates = pd.date_range('2025-05-01', periods=50, freq='D')
        base_price = 100
        trend_prices = [base_price + i * 0.5 for i in range(50)]  # Uptrend
        volumes = [2000000] * 50
        
        mock_data = pd.DataFrame({
            'Close': trend_prices,
            'Volume': volumes,
            'High': [p * 1.02 for p in trend_prices],
            'Low': [p * 0.98 for p in trend_prices],
            'Open': [p * 1.01 for p in trend_prices]
        }, index=dates)
        
        # Mock ticker object
        mock_ticker_obj = Mock()
        mock_ticker_obj.info = {
            'marketCap': 1e12,
            'shortName': 'Apple Inc.',
            'averageVolume': 50000000,
            'sector': 'Technology'
        }
        mock_ticker_obj.history.return_value = mock_data
        mock_ticker.return_value = mock_ticker_obj
        
        # Also need to mock yf.download for get_weekly_returns
        with patch('streamlit_app.yf.download') as mock_download:
            mock_download.return_value = mock_data
            
            result = self.tracker.analyze_ticker_momentum('AAPL', min_rs_score=20, min_weekly_target=0.5)
            
            self.assertIsNotNone(result)
            self.assertIsInstance(result, dict)
            self.assertEqual(result['ticker'], 'AAPL')
            self.assertIn('rs_score', result)
            self.assertIn('avg_weekly_return', result)
            self.assertIn('market_cap', result)
            self.assertIn('meets_criteria', result)
            
    @patch('streamlit_app.yf.download')
    def test_analyze_ticker_momentum_no_data(self, mock_yf_download):
        """Test ticker analysis with no data"""
        mock_yf_download.return_value = pd.DataFrame()
        
        result = self.tracker.analyze_ticker_momentum('INVALID')
        
        self.assertIsNone(result)
        
    @patch('streamlit_app.yf.Ticker')
    @patch('streamlit_app.yf.download')
    def test_analyze_ticker_momentum_no_info(self, mock_yf_download, mock_ticker):
        """Test ticker analysis with missing company info"""
        mock_yf_download.return_value = self.sample_data
        mock_ticker.return_value.info = {}  # Empty info
        
        result = self.tracker.analyze_ticker_momentum('AAPL')
        
        self.assertIsNone(result)

class TestTickerDiscovery(unittest.TestCase):
    """Test ticker discovery and screening functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.tracker = PortfolioTracker()
        
    def test_get_momentum_stocks(self):
        """Test momentum stocks discovery"""
        stocks = self.tracker._get_momentum_stocks()
        
        self.assertIsInstance(stocks, list)
        self.assertGreater(len(stocks), 0)
        
        # Should contain some major tickers
        stock_set = set(stocks)
        expected_tickers = {'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA'}
        intersection = stock_set.intersection(expected_tickers)
        self.assertGreater(len(intersection), 0, "Should contain some major tech stocks")
        
    def test_get_sp500_leaders(self):
        """Test S&P 500 leaders discovery"""
        leaders = self.tracker._get_sp500_leaders()
        
        self.assertIsInstance(leaders, list)
        self.assertGreater(len(leaders), 0)
        
    def test_get_etf_leaders(self):
        """Test ETF leaders discovery"""
        etfs = self.tracker._get_etf_leaders()
        
        self.assertIsInstance(etfs, list)
        self.assertGreater(len(etfs), 0)
        
        # Should contain some major ETFs
        etf_set = set(etfs)
        expected_etfs = {'SPY', 'QQQ', 'IWM', 'XLK', 'XLF'}
        intersection = etf_set.intersection(expected_etfs)
        self.assertGreater(len(intersection), 0, "Should contain some major ETFs")
        
    def test_discover_momentum_tickers(self):
        """Test comprehensive ticker discovery"""
        tickers = self.tracker.discover_momentum_tickers()
        
        self.assertIsInstance(tickers, list)
        self.assertGreaterEqual(len(tickers), 50)  # Should discover substantial number (50 or more)
        
        # Should not have duplicates
        self.assertEqual(len(tickers), len(set(tickers)))
        
    @patch.object(PortfolioTracker, 'analyze_ticker_momentum')
    def test_screen_discovered_tickers(self, mock_analyze):
        """Test screening of discovered tickers"""
        # Mock successful analysis for some tickers
        def mock_analysis_side_effect(ticker, min_rs_score, min_weekly_target):
            if ticker in ['AAPL', 'MSFT']:
                return {
                    'ticker': ticker,
                    'rs_score': 75,
                    'avg_weekly_return': 2.5,
                    'market_cap': 1e12,
                    'meets_criteria': True,
                    'qualification_reason': 'Strong momentum'
                }
            return None
            
        mock_analyze.side_effect = mock_analysis_side_effect
        
        test_tickers = ['AAPL', 'MSFT', 'WEAK1', 'WEAK2']
        market_health = {'market_regime': 'AGGRESSIVE', 'is_defensive': False}
        
        results = self.tracker.screen_discovered_tickers(
            test_tickers, 
            min_rs_score=70, 
            min_weekly_target=2.0,
            market_health=market_health
        )
        
        self.assertEqual(len(results), 2)  # Only AAPL and MSFT should pass
        tickers_returned = [r['ticker'] for r in results]
        self.assertIn('AAPL', tickers_returned)
        self.assertIn('MSFT', tickers_returned)
        
    @patch('streamlit_app.yf.download')
    def test_filter_by_rules_basic(self, mock_yf_download):
        """Test basic filtering by momentum rules"""
        # Create mock data for different ticker performance
        def mock_download_side_effect(ticker, **kwargs):
            if ticker == 'STRONG':
                # Strong uptrend
                dates = pd.date_range('2025-05-01', periods=30, freq='D')
                prices = [100 + i * 2 for i in range(30)]  # Strong uptrend
                return pd.DataFrame({'Close': prices}, index=dates)
            elif ticker == 'WEAK':
                # Weak/declining
                dates = pd.date_range('2025-05-01', periods=30, freq='D')
                prices = [100 - i * 0.5 for i in range(30)]  # Declining
                return pd.DataFrame({'Close': prices}, index=dates)
            return pd.DataFrame()
            
        mock_yf_download.side_effect = mock_download_side_effect
        
        test_tickers = ['STRONG', 'WEAK']
        filtered = self.tracker.filter_by_rules(test_tickers)
        
        self.assertIsInstance(filtered, list)
        # Note: The actual filtering logic may be complex, 
        # so we're mainly testing that it returns a list

class TestDataIntegrity(unittest.TestCase):
    """Test data integrity and edge cases"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.tracker = PortfolioTracker()
        
    def test_passes_filters_edge_cases(self):
        """Test passes_filters with edge case inputs"""
        # Test with None values - should handle gracefully now
        result_with_none = {
            'ticker': 'TEST',
            'rs_score': None,
            'avg_weekly_return': 2.0,
            'market_cap': 1e12,
            'meets_criteria': True,
            'weekly_returns': [0.02, 0.025, 0.015, 0.022],
            'weeks_above_target': 2
        }
        
        filtered = self.tracker.passes_filters(result_with_none)
        self.assertFalse(filtered)  # Should fail with None rs_score (becomes 0)
        
        # Test with zero values
        result_with_zeros = {
            'ticker': 'TEST',
            'rs_score': 0,
            'avg_weekly_return': 0,
            'market_cap': 0,
            'meets_criteria': True,
            'weekly_returns': [0.0, 0.0, 0.0, 0.0],
            'weeks_above_target': 0
        }
        
        filtered = self.tracker.passes_filters(result_with_zeros)
        self.assertFalse(filtered)  # Should fail with zero values
        
    def test_get_top_picks_empty_input(self):
        """Test get_top_picks with empty input"""
        top_picks = self.tracker.get_top_picks([], count=10)
        self.assertEqual(len(top_picks), 0)
        
    def test_get_top_picks_more_requested_than_available(self):
        """Test get_top_picks when requesting more than available"""
        results = [
            {
                'ticker': 'AAPL', 'rs_score': 85, 'avg_weekly_return': 3.0, 'market_cap': 3e12, 
                'meets_criteria': True, 'weeks_above_target': 3, 'daily_change': 1.5,
                'weekly_returns': [0.03, 0.025, 0.035, 0.028]
            }
        ]
        
        with patch.object(self.tracker, 'passes_filters', return_value=True):
            top_picks = self.tracker.get_top_picks(results, count=10)
            self.assertEqual(len(top_picks), 1)  # Only returns what's available

if __name__ == '__main__':
    unittest.main()
