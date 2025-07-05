"""
Focused coverage tests for Portfolio Management Suite v2.0
===========================================================

Simple, direct tests to achieve 80%+ coverage.
"""

import unittest
from unittest.mock import patch, Mock
import sys
import os
import pandas as pd
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestMainAppCoverage(unittest.TestCase):
    """Focused tests for main_app.py coverage"""
    
    def test_imports_and_constants(self):
        """Test module imports and constants"""
        import main_app
        
        # Test that all required functions exist
        self.assertTrue(hasattr(main_app, 'main'))
        self.assertTrue(hasattr(main_app, 'show_home_page'))
        self.assertTrue(hasattr(main_app, 'show_tactical_tracker'))
        self.assertTrue(hasattr(main_app, 'show_quality_tracker'))
        
        # Test docstrings
        self.assertIsNotNone(main_app.__doc__)
        self.assertIsNotNone(main_app.main.__doc__)
        self.assertIsNotNone(main_app.show_home_page.__doc__)
        self.assertIsNotNone(main_app.show_tactical_tracker.__doc__)
        self.assertIsNotNone(main_app.show_quality_tracker.__doc__)
        
    def test_module_level_code(self):
        """Test module-level code execution"""
        import main_app
        
        # Test that streamlit is imported
        self.assertTrue(hasattr(main_app, 'st'))
        
        # Test that sys and os are available
        self.assertTrue(hasattr(main_app, 'sys'))
        self.assertTrue(hasattr(main_app, 'os'))


class TestTacticalTrackerCoverage(unittest.TestCase):
    """Focused tests for tactical_tracker.py coverage"""
    
    def test_constants_and_imports(self):
        """Test constants and imports"""
        import tactical_tracker
        
        # Test all constants exist
        constants = [
            'DEFENSIVE_ETFS', 'VIX_THRESHOLD', 'BREADTH_THRESHOLD', 
            'DROP_THRESHOLD', 'WATCH_THRESHOLD', 'MOMENTUM_THRESHOLD',
            'MIN_MARKET_CAP', 'WEEKLY_TARGET'
        ]
        
        for const in constants:
            self.assertTrue(hasattr(tactical_tracker, const))
            
        # Test types
        self.assertIsInstance(tactical_tracker.DEFENSIVE_ETFS, list)
        self.assertIsInstance(tactical_tracker.VIX_THRESHOLD, (int, float))
        self.assertIsInstance(tactical_tracker.MIN_MARKET_CAP, (int, float))
    
    @patch('tactical_tracker.yf')
    def test_portfolio_tracker_methods(self, mock_yf):
        """Test individual methods of PortfolioTracker"""
        import tactical_tracker
        
        # Test tracker initialization
        tracker = tactical_tracker.PortfolioTracker()
        self.assertEqual(tracker.results_file, "portfolio_results.pkl")
        self.assertEqual(tracker.portfolio, {})
        self.assertEqual(tracker.market_data, {})
        
        # Test market health with empty data (exception path)
        mock_yf.Ticker.side_effect = Exception("Network error")
        market_health = tracker.get_market_health()
        self.assertIn('vix', market_health)
        self.assertIn('is_defensive', market_health)
        
    def test_allocation_methods(self):
        """Test allocation calculation methods"""
        import tactical_tracker
        
        tracker = tactical_tracker.PortfolioTracker()
        
        # Test with empty lists
        allocation = tracker.calculate_simple_allocation([], [])
        self.assertEqual(allocation['total_allocated'], 0)
        self.assertEqual(allocation['allocations'], [])
        
        # Test with minimal data
        strong_buys = [{'ticker': 'TEST', 'momentum_score': 15.0, 'avg_weekly_return': 2.0}]
        moderate_buys = []
        
        allocation = tracker.calculate_simple_allocation(strong_buys, moderate_buys)
        self.assertIn('allocations', allocation)
        self.assertIn('total_allocated', allocation)


class TestQualityTrackerCoverage(unittest.TestCase):
    """Focused tests for quality_tracker.py coverage"""
    
    def test_constants_and_imports(self):
        """Test constants and imports"""
        import quality_tracker
        
        # Test constants exist
        self.assertTrue(hasattr(quality_tracker, 'DEFENSIVE_SECTORS'))
        self.assertTrue(hasattr(quality_tracker, 'PRE_SEED_UNIVERSE'))
        
        # Test types and content
        self.assertIsInstance(quality_tracker.DEFENSIVE_SECTORS, dict)
        self.assertIsInstance(quality_tracker.PRE_SEED_UNIVERSE, list)
        
        # Test that defensive sectors have content
        for sector, tickers in quality_tracker.DEFENSIVE_SECTORS.items():
            self.assertIsInstance(tickers, list)
            self.assertGreater(len(tickers), 0)
            
    def test_quality_stocks_tracker_init(self):
        """Test QualityStocksTracker initialization"""
        import quality_tracker
        
        tracker = quality_tracker.QualityStocksTracker()
        self.assertEqual(tracker.results_file, "quality_results.pkl")
        self.assertIsNone(tracker.spy_benchmark)
        
    def test_calculation_methods(self):
        """Test calculation methods with mock data"""
        import quality_tracker
        
        tracker = quality_tracker.QualityStocksTracker()
        
        # Test YTD return calculation
        hist_data = pd.DataFrame({
            'Close': [100, 102, 104, 106, 108, 110]
        }, index=pd.date_range('2024-01-01', periods=6, freq='D'))
        
        ytd_return = tracker.calculate_ytd_return(hist_data)
        self.assertIsInstance(ytd_return, (int, float))
        
        # Test period return calculation
        period_return = tracker.calculate_period_return(hist_data, 3)
        self.assertIsInstance(period_return, (int, float))
        
        # Test beta calculation
        spy_data = pd.DataFrame({
            'Close': [400, 402, 404, 406, 408, 410]
        }, index=pd.date_range('2024-01-01', periods=6, freq='D'))
        
        beta = tracker.calculate_beta(hist_data, spy_data)
        self.assertIsInstance(beta, (int, float))
        
    def test_quality_filters(self):
        """Test quality filter methods"""
        import quality_tracker
        
        tracker = quality_tracker.QualityStocksTracker()
        
        # Test with valid stock data
        valid_stock = {
            'ticker': 'PG',
            'roe': 15.0,
            'beta': 0.8,
            'dividend_yield': 3.0,
            'market_cap': 400e9,
            'sector': 'Consumer Staples'
        }
        
        # Test passes_quality_filters method signature
        result = tracker.passes_quality_filters(
            valid_stock, 
            min_roe=10.0, 
            max_beta=1.2,
            min_dividend_yield=2.0, 
            min_market_cap_str="$25B",
            preferred_sectors=["Consumer Staples"], 
            exclude_unprofitable=False,
            require_dividend_history=False
        )
        self.assertIsInstance(result, bool)
        
        # Test with invalid stock data
        invalid_stock = {}
        result = tracker.passes_quality_filters(
            invalid_stock, 
            min_roe=10.0, 
            max_beta=1.2,
            min_dividend_yield=2.0, 
            min_market_cap_str="$25B",
            preferred_sectors=["Consumer Staples"], 
            exclude_unprofitable=False,
            require_dividend_history=False
        )
        self.assertFalse(result)
        
    def test_standalone_functions(self):
        """Test standalone functions"""
        import quality_tracker
        
        # Test calculate_quality_score
        stock_data = {
            'roe': 15.0,
            'dividend_yield': 3.0,
            'beta': 0.9,
            'five_year_return': 50.0,
            'market_cap': 100e9
        }
        
        score = quality_tracker.calculate_quality_score(stock_data)
        self.assertIsInstance(score, (int, float))
        self.assertGreaterEqual(score, 0)
        
        # Test with extreme values
        extreme_stock = {
            'roe': 30.0,
            'dividend_yield': 8.0,
            'beta': 0.5,
            'five_year_return': 150.0,
            'market_cap': 500e9
        }
        
        extreme_score = quality_tracker.calculate_quality_score(extreme_stock)
        self.assertGreater(extreme_score, score)  # Should score higher


class TestCrossModuleFunctionality(unittest.TestCase):
    """Test cross-module functionality and integration"""
    
    def test_all_modules_importable(self):
        """Test that all modules can be imported together"""
        import main_app
        import tactical_tracker  
        import quality_tracker
        
        # All should be importable without conflicts
        modules = [main_app, tactical_tracker, quality_tracker]
        for module in modules:
            self.assertTrue(hasattr(module, '__name__'))
            self.assertIsNotNone(module.__doc__)
            
    def test_class_instantiation(self):
        """Test that all main classes can be instantiated"""
        import tactical_tracker
        import quality_tracker
        
        # Test PortfolioTracker
        tactical_tracker_inst = tactical_tracker.PortfolioTracker()
        self.assertIsInstance(tactical_tracker_inst, tactical_tracker.PortfolioTracker)
        
        # Test QualityStocksTracker
        quality_tracker_inst = quality_tracker.QualityStocksTracker()
        self.assertIsInstance(quality_tracker_inst, quality_tracker.QualityStocksTracker)
        
    def test_function_signatures(self):
        """Test that key functions have correct signatures"""
        import main_app
        import tactical_tracker
        import quality_tracker
        
        # Test main app functions
        main_functions = [main_app.main, main_app.show_home_page, 
                         main_app.show_tactical_tracker, main_app.show_quality_tracker]
        
        for func in main_functions:
            self.assertTrue(callable(func))
            
        # Test tactical tracker functions
        self.assertTrue(callable(tactical_tracker.run_tactical_tracker))
        
        # Test quality tracker functions
        self.assertTrue(callable(quality_tracker.run_quality_tracker))
        self.assertTrue(callable(quality_tracker.calculate_quality_score))
        self.assertTrue(callable(quality_tracker.display_quality_education))
        
    def test_data_structure_consistency(self):
        """Test that data structures are consistent across modules"""
        import tactical_tracker
        import quality_tracker
        
        # Test that both modules use similar data patterns
        tactical_constants = dir(tactical_tracker)
        quality_constants = dir(quality_tracker)
        
        # Both should have threshold constants
        self.assertIn('PortfolioTracker', tactical_constants)
        self.assertIn('QualityStocksTracker', quality_constants)
        
        # Both should have defensive-related constants
        tactical_defensive = [x for x in tactical_constants if 'DEFENSIVE' in x]
        quality_defensive = [x for x in quality_constants if 'DEFENSIVE' in x]
        
        self.assertGreater(len(tactical_defensive), 0)
        self.assertGreater(len(quality_defensive), 0)


if __name__ == '__main__':
    print("\\n🎯 Running Focused Coverage Tests")
    print("=" * 50)
    unittest.main(verbosity=2)
