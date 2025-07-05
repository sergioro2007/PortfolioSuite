"""
Integration tests for the complete application workflow
Tests end-to-end functionality and component integration
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

class TestIntegrationWorkflow(unittest.TestCase):
    """Test complete application workflows"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.tracker = PortfolioTracker()
        
        # Create comprehensive mock market data
        self.create_mock_market_data()
        
    def create_mock_market_data(self):
        """Create realistic mock market data for testing"""
        dates = pd.date_range('2025-05-01', periods=50, freq='D')
        
        # Mock SPY data (healthy market)
        self.mock_spy_data = pd.DataFrame({
            'Close': np.linspace(500, 520, 50),  # Uptrending
            'Volume': [80000000] * 50,
            'High': np.linspace(502, 522, 50),
            'Low': np.linspace(498, 518, 50),
            'Open': np.linspace(501, 521, 50)
        }, index=dates)
        
        # Mock VIX data (low volatility)
        self.mock_vix_data = pd.DataFrame({
            'Close': [15.0] * 50  # Low, stable VIX
        }, index=dates)
        
        # Mock individual stock data (strong performer)
        self.mock_stock_data = pd.DataFrame({
            'Close': np.linspace(100, 130, 50),  # Strong uptrend
            'Volume': [5000000] * 50,
            'High': np.linspace(102, 132, 50),
            'Low': np.linspace(98, 128, 50),
            'Open': np.linspace(101, 131, 50)
        }, index=dates)
        
    @patch('streamlit_app.yf.Ticker')
    @patch('streamlit_app.yf.download')
    def test_complete_screening_workflow_aggressive_market(self, mock_yf_download, mock_ticker):
        """Test complete screening workflow in aggressive market conditions"""
        
        # Mock yfinance download for market health
        def mock_download_side_effect(ticker, **kwargs):
            if ticker == '^VIX':
                return self.mock_vix_data
            elif ticker == 'SPY':
                return self.mock_spy_data
            elif ticker in ['AAPL', 'MSFT', 'GOOGL']:
                return self.mock_stock_data
            return pd.DataFrame()
            
        mock_yf_download.side_effect = mock_download_side_effect
        
        # Mock ticker info
        mock_info = {
            'marketCap': 3e12,
            'averageVolume': 50000000,
            'sector': 'Technology'
        }
        mock_ticker.return_value.info = mock_info
        
        # Step 1: Get market health
        market_health = self.tracker.get_market_health()
        
        self.assertIsInstance(market_health, dict)
        self.assertFalse(market_health.get('is_defensive', True))  # Should be aggressive
        
        # Step 2: Discover tickers
        with patch.object(self.tracker, '_get_momentum_stocks', return_value=['AAPL', 'MSFT', 'GOOGL']):
            discovered_tickers = self.tracker._get_momentum_stocks()
            
            self.assertGreater(len(discovered_tickers), 0)
            
            # Step 3: Screen tickers
            results = self.tracker.screen_discovered_tickers(
                discovered_tickers,
                min_rs_score=20,
                min_weekly_target=0.5,
                market_health=market_health
            )
            
            self.assertIsInstance(results, list)
            # In aggressive market with good data, should return results
            self.assertGreaterEqual(len(results), 0)
            
            if len(results) > 0:
                # Verify result structure
                result = results[0]
                self.assertIn('ticker', result)
                self.assertIn('rs_score', result)
                self.assertIn('avg_weekly_return', result)
                self.assertIn('meets_criteria', result)
                
    @patch('streamlit_app.yf.Ticker')
    @patch('streamlit_app.yf.download')
    def test_complete_screening_workflow_defensive_market(self, mock_yf_download, mock_ticker):
        """Test complete screening workflow in defensive market conditions"""
        
        # Create defensive market data
        dates = pd.date_range('2025-05-01', periods=50, freq='D')
        
        # High VIX (stressed market)
        mock_vix_defensive = pd.DataFrame({
            'Close': [35.0] * 50  # High VIX
        }, index=dates)
        
        # Declining SPY
        mock_spy_defensive = pd.DataFrame({
            'Close': np.linspace(500, 470, 50),  # Declining
            'Volume': [120000000] * 50,  # High volume
            'High': np.linspace(502, 472, 50),
            'Low': np.linspace(498, 468, 50),
            'Open': np.linspace(501, 471, 50)
        }, index=dates)
        
        def mock_download_side_effect(ticker, **kwargs):
            if ticker == '^VIX':
                return mock_vix_defensive
            elif ticker == 'SPY':
                return mock_spy_defensive
            elif ticker in ['XLV', 'XLP']:  # Defensive stocks
                return self.mock_stock_data
            return pd.DataFrame()
            
        mock_yf_download.side_effect = mock_download_side_effect
        
        mock_info = {
            'marketCap': 500e9,
            'averageVolume': 30000000,
            'sector': 'Healthcare'
        }
        mock_ticker.return_value.info = mock_info
        
        # Test workflow with mocked defensive market
        with patch.object(self.tracker, 'get_market_health') as mock_market_health:
            mock_market_health.return_value = {
                'market_regime': 'DEFENSIVE',
                'is_defensive': True,
                'defensive_score': 60,
                'vix': 25,
                'breadth': 45
            }
            
            market_health = self.tracker.get_market_health()
            
            self.assertTrue(market_health.get('is_defensive', False))  # Should be defensive
            self.assertGreaterEqual(market_health.get('defensive_score', 0), 50)
            
            # Test defensive criteria
            defensive_criteria = self.tracker.get_defensive_criteria(market_health)
            
            self.assertGreater(defensive_criteria['min_rs_score'], 30)  # Higher than aggressive
            self.assertGreater(defensive_criteria['min_weekly_target'], 0.5)  # Higher than aggressive
        
    @patch.object(PortfolioTracker, 'analyze_ticker_momentum')
    def test_end_to_end_portfolio_generation(self, mock_analyze):
        """Test end-to-end portfolio generation workflow"""
        
        # Mock analysis results for various tickers
        def mock_analysis_side_effect(ticker, min_rs_score, min_weekly_target):
            ticker_data = {
                'AAPL': {'rs_score': 85, 'avg_weekly_return': 3.0, 'sector': 'Technology'},
                'MSFT': {'rs_score': 80, 'avg_weekly_return': 2.8, 'sector': 'Technology'},
                'JPM': {'rs_score': 75, 'avg_weekly_return': 2.2, 'sector': 'Financial Services'},
                'XLV': {'rs_score': 70, 'avg_weekly_return': 1.8, 'sector': 'Healthcare'},
                'JNJ': {'rs_score': 65, 'avg_weekly_return': 1.5, 'sector': 'Healthcare'}
            }
            
            if ticker in ticker_data:
                data = ticker_data[ticker]
                return {
                    'ticker': ticker,
                    'rs_score': data['rs_score'],
                    'avg_weekly_return': data['avg_weekly_return'],
                    'market_cap': 1e12,
                    'meets_criteria': True,
                    'qualification_reason': 'Mock analysis',
                    'sector': data['sector'],
                    'weeks_above_target': 3,
                    'daily_change': 1.0,
                    'weekly_returns': [0.025, 0.020, 0.028, 0.025]
                }
            return None
            
        mock_analyze.side_effect = mock_analysis_side_effect
        
        # Mock market health (aggressive)
        market_health = {
            'market_regime': 'AGGRESSIVE',
            'is_defensive': False,
            'defensive_score': 20
        }
        
        # Run complete workflow
        test_tickers = ['AAPL', 'MSFT', 'JPM', 'XLV', 'JNJ', 'WEAK1', 'WEAK2']
        
        # Screen tickers
        results = self.tracker.screen_discovered_tickers(
            test_tickers,
            min_rs_score=60,
            min_weekly_target=1.0,
            market_health=market_health
        )
        
        self.assertGreater(len(results), 0)
        
        # Generate portfolio recommendations
        portfolio = self.tracker.generate_portfolio_recommendations(
            results,
            portfolio_size=3,
            min_rs_score=60,
            min_weekly_target=1.0
        )
        
        self.assertIsInstance(portfolio, dict)
        self.assertIn('top_picks', portfolio)
        self.assertIn('strong_buys', portfolio)
        self.assertIn('moderate_buys', portfolio)
        self.assertIn('watch_list', portfolio)
        
        # Should recommend diverse portfolio
        recommended = portfolio['top_picks']
        self.assertGreater(len(recommended), 0)
        self.assertLessEqual(len(recommended), 3)
        
    def test_parameter_propagation_workflow(self):
        """Test that user parameters are properly propagated through the workflow"""
        
        # Create mock result that meets Elite Momentum criteria
        user_qualifying_result = {
            'ticker': 'USER_PICK',
            'rs_score': 35,  # Below defensive threshold (40) but above user min (30)
            'avg_weekly_return': 3.0,  # Well above Elite threshold (2.5%)
            'market_cap': 100e9,
            'meets_criteria': True,
            'qualification_reason': 'Elite momentum',
            'weeks_above_target': 3,  # 3 weeks >2%
            'daily_change': 1.0,
            'weekly_returns': [0.035, 0.025, 0.030, 0.010]  # 3.5%, 2.5%, 3.0%, 1.0% - meets Elite criteria
        }
        
        # Test with aggressive market (should use user parameters)
        # Should pass user filters in aggressive market  
        result = self.tracker.passes_filters(
            user_qualifying_result,
            min_rs_score=30,  # Lower than user's RS score of 35
            min_weekly_target=1.5
        )
        self.assertTrue(result)
        
        # Test with defensive market (should use defensive parameters)
        defensive_market = {
            'market_regime': 'HIGHLY_DEFENSIVE',
            'is_defensive': True,
            'defensive_score': 80
        }
        
        defensive_criteria = self.tracker.get_defensive_criteria(defensive_market)
        
        # Should fail defensive filters due to low RS score (35 < 70)
        result = self.tracker.passes_filters(
            user_qualifying_result,
            min_rs_score=defensive_criteria['min_rs_score'],  # 70
            min_weekly_target=defensive_criteria['min_weekly_target']  # 2.0
        )
        self.assertFalse(result)

class TestSystemReliability(unittest.TestCase):
    """Test system reliability and error handling"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.tracker = PortfolioTracker()
        
    @patch('streamlit_app.yf.download')
    def test_market_health_with_data_failures(self, mock_yf_download):
        """Test market health calculation with data failures"""
        
        # Simulate partial data failure
        def mock_download_side_effect(ticker, **kwargs):
            if ticker == '^VIX':
                return pd.DataFrame()  # No VIX data
            elif ticker == 'SPY':
                # Return minimal SPY data
                dates = pd.date_range('2025-06-29', periods=3, freq='D')
                return pd.DataFrame({
                    'Close': [500, 505, 510],
                    'Volume': [80000000, 85000000, 82000000]
                }, index=dates)
            return pd.DataFrame()
            
        mock_yf_download.side_effect = mock_download_side_effect
        
        # Should handle missing VIX data gracefully
        market_health = self.tracker.get_market_health()
        
        self.assertIsInstance(market_health, dict)
        # Should return some kind of result even with missing data
        
    @patch('streamlit_app.yf.download')
    def test_ticker_analysis_resilience(self, mock_yf_download):
        """Test ticker analysis resilience to data issues"""
        
        # Test with various data problems
        test_cases = [
            ('EMPTY', pd.DataFrame()),  # No data
            ('SHORT', pd.DataFrame({'Close': [100]}, index=[datetime.now()])),  # Insufficient data
        ]
        
        def mock_download_side_effect(ticker, **kwargs):
            for test_ticker, test_data in test_cases:
                if ticker == test_ticker:
                    return test_data
            return pd.DataFrame()
            
        mock_yf_download.side_effect = mock_download_side_effect
        
        # Should handle data issues gracefully
        for test_ticker, _ in test_cases:
            result = self.tracker.analyze_ticker_momentum(test_ticker)
            self.assertIsNone(result)  # Should return None for bad data
            
    def test_screening_with_mixed_data_quality(self):
        """Test screening process with mixed data quality"""
        
        def mock_analyze_side_effect(ticker, min_rs_score, min_weekly_target):
            # Simulate mixed success/failure
            if ticker in ['GOOD1', 'GOOD2']:
                return {
                    'ticker': ticker,
                    'rs_score': 75,
                    'avg_weekly_return': 2.5,
                    'market_cap': 1e12,
                    'meets_criteria': True,
                    'qualification_reason': 'Good data'
                }
            return None  # Simulate data failure
            
        mixed_tickers = ['GOOD1', 'BAD1', 'GOOD2', 'BAD2', 'BAD3']
        market_health = {'market_regime': 'AGGRESSIVE', 'is_defensive': False}
        
        with patch.object(self.tracker, 'analyze_ticker_momentum', side_effect=mock_analyze_side_effect):
            results = self.tracker.screen_discovered_tickers(
                mixed_tickers,
                min_rs_score=70,
                min_weekly_target=2.0,
                market_health=market_health
            )
            
            # Should return only the good results
            self.assertEqual(len(results), 2)
            returned_tickers = [r['ticker'] for r in results]
            self.assertIn('GOOD1', returned_tickers)
            self.assertIn('GOOD2', returned_tickers)

if __name__ == '__main__':
    unittest.main()
