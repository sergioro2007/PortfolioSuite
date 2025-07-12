"""
Test configuration and utilities for Tactical Portfolio Tracker tests
"""

import unittest
from unittest.mock import Mock, MagicMock
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class TestConfig:
    """Test configuration and common test data"""
    
    # Test constants
    MIN_MARKET_CAP = 5e9
    MIN_RS_SCORE = 20
    MIN_WEEKLY_TARGET = 0.5
    
    # Sample tickers for testing
    SAMPLE_TICKERS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
    SAMPLE_ETFS = ['SPY', 'QQQ', 'IWM', 'XLK', 'XLF']
    
    @staticmethod
    def create_sample_ticker_result(ticker='TEST', rs_score=75, weekly_return=2.5, market_cap=1e12):
        """Create a sample ticker analysis result for testing"""
        return {
            'ticker': ticker,
            'rs_score': rs_score,
            'avg_weekly_return': weekly_return,
            'market_cap': market_cap,
            'meets_criteria': True,
            'qualification_reason': 'Test result',
            'weekly_returns': [2.1, 2.8, 2.3, 2.7],
            'price': 150.0,
            'volume': 50000000,
            'sector': 'Technology'
        }
    
    @staticmethod
    def create_sample_market_data(days=50, trend='up'):
        """Create sample market data for testing"""
        dates = pd.date_range('2025-05-01', periods=days, freq='D')
        
        if trend == 'up':
            prices = np.linspace(100, 130, days)
        elif trend == 'down':
            prices = np.linspace(130, 100, days)
        else:  # flat
            prices = [115 + np.random.normal(0, 2) for _ in range(days)]
            
        return pd.DataFrame({
            'Close': prices,
            'Volume': [5000000] * days,
            'High': [p * 1.02 for p in prices],
            'Low': [p * 0.98 for p in prices],
            'Open': [p * 1.01 for p in prices]
        }, index=dates)
    
    @staticmethod
    def create_aggressive_market_health():
        """Create aggressive market health conditions"""
        return {
            'market_regime': 'AGGRESSIVE',
            'is_defensive': False,
            'defensive_score': 20,
            'vix': 15.0,
            'breadth': 80,
            'spy_above_ma': True
        }
    
    @staticmethod
    def create_defensive_market_health():
        """Create defensive market health conditions"""
        return {
            'market_regime': 'DEFENSIVE',
            'is_defensive': True,
            'defensive_score': 60,
            'vix': 25.0,
            'breadth': 45,
            'spy_above_ma': False
        }

class MockYFinance:
    """Mock yfinance for consistent testing"""
    
    @staticmethod
    def mock_ticker_info(ticker='TEST', market_cap=1e12, sector='Technology'):
        """Create mock ticker info"""
        return {
            'marketCap': market_cap,
            'averageVolume': 50000000,
            'sector': sector,
            'industry': 'Software',
            'country': 'US'
        }
    
    @staticmethod
    def mock_download_aggressive_market(ticker, **kwargs):
        """Mock download for aggressive market conditions"""
        if ticker == '^VIX':
            dates = pd.date_range('2025-06-25', periods=10, freq='D')
            return pd.DataFrame({'Close': [15.0] * 10}, index=dates)
        elif ticker == 'SPY':
            return TestConfig.create_sample_market_data(10, 'up')
        elif ticker in TestConfig.SAMPLE_TICKERS:
            return TestConfig.create_sample_market_data(50, 'up')
        return pd.DataFrame()
    
    @staticmethod
    def mock_download_defensive_market(ticker, **kwargs):
        """Mock download for defensive market conditions"""
        if ticker == '^VIX':
            dates = pd.date_range('2025-06-25', periods=10, freq='D')
            return pd.DataFrame({'Close': [35.0] * 10}, index=dates)
        elif ticker == 'SPY':
            return TestConfig.create_sample_market_data(10, 'down')
        elif ticker in TestConfig.SAMPLE_TICKERS:
            return TestConfig.create_sample_market_data(50, 'down')
        return pd.DataFrame()

def skip_if_no_internet(test_func):
    """Decorator to skip tests that require internet connection"""
    def wrapper(*args, **kwargs):
        try:
            import requests
            requests.get('https://finance.yahoo.com', timeout=5)
            return test_func(*args, **kwargs)
        except:
            import unittest
            raise unittest.SkipTest("Internet connection required")
    return wrapper

class BaseTestCase(unittest.TestCase):
    """Base test case with common setup and utilities"""
    
    def setUp(self):
        """Common setup for all tests"""
        self.config = TestConfig()
        self.mock_yf = MockYFinance()
        
    def assertValidTickerResult(self, result):
        """Assert that a ticker result has valid structure"""
        required_keys = ['ticker', 'rs_score', 'avg_weekly_return', 'market_cap', 'meets_criteria']
        
        self.assertIsInstance(result, dict)
        for key in required_keys:
            self.assertIn(key, result, f"Missing required key: {key}")
            
        # Validate data types
        self.assertIsInstance(result['ticker'], str)
        self.assertIsInstance(result['rs_score'], (int, float))
        self.assertIsInstance(result['avg_weekly_return'], (int, float))
        self.assertIsInstance(result['market_cap'], (int, float))
        self.assertIsInstance(result['meets_criteria'], bool)
        
    def assertValidMarketHealth(self, market_health):
        """Assert that market health has valid structure"""
        required_keys = ['market_regime', 'is_defensive', 'defensive_score']
        
        self.assertIsInstance(market_health, dict)
        for key in required_keys:
            self.assertIn(key, market_health, f"Missing required key: {key}")
            
        # Validate values
        self.assertIn(market_health['market_regime'], ['AGGRESSIVE', 'DEFENSIVE', 'HIGHLY_DEFENSIVE'])
        self.assertIsInstance(market_health['is_defensive'], bool)
        self.assertIsInstance(market_health['defensive_score'], (int, float))
        self.assertGreaterEqual(market_health['defensive_score'], 0)
        self.assertLessEqual(market_health['defensive_score'], 100)
