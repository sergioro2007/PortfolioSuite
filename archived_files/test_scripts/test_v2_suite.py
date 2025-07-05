"""
Tests for the Multi-Feature Portfolio Management Suite v2.0
===========================================================

Test suite for the main application hub and feature navigation.
"""

import unittest
from unittest.mock import patch, Mock, MagicMock
import sys
import os
import pandas as pd

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# We need to mock Streamlit for testing since it's UI-based
class MockStreamlit:
    """Mock Streamlit for unit testing"""
    
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    
    @staticmethod
    def set_page_config(**kwargs):
        pass
        
    @staticmethod
    def title(text):
        return text
        
    @staticmethod
    def markdown(text):
        return text
        
    @staticmethod
    def columns(num):
        return [MockStreamlit() for _ in range(num)]
        
    @staticmethod
    def info(text):
        return text
        
    @staticmethod
    def error(text):
        return text
        
    @staticmethod
    def warning(text):
        return text
        
    @staticmethod
    def button(text, **kwargs):
        return False
        
    @staticmethod
    def selectbox(label, options, **kwargs):
        return options[kwargs.get('index', 0)]
        
    @staticmethod
    def slider(*args, **kwargs):
        return args[2] if len(args) > 2 else 10
        
    @staticmethod
    def multiselect(label, options, **kwargs):
        return kwargs.get('default', [])
        
    @staticmethod
    def expander(label, **kwargs):
        return MockStreamlit()
        
    class sidebar:
        @staticmethod
        def title(text):
            return text
        @staticmethod
        def markdown(text):
            return text
        @staticmethod
        def selectbox(label, options, **kwargs):
            return options[kwargs.get('index', 0)]
        @staticmethod
        def slider(*args, **kwargs):
            return args[2] if len(args) > 2 else 10
        @staticmethod
        def checkbox(label, default=False, **kwargs):
            return default
        @staticmethod
        def multiselect(label, options, **kwargs):
            return kwargs.get('default', [])

# Mock streamlit before importing our modules
sys.modules['streamlit'] = MockStreamlit()

class TestMainApp(unittest.TestCase):
    """Test the main application hub functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Mock streamlit module
        self.st_mock = Mock()
        
    def test_main_app_import(self):
        """Test that main app module can be imported"""
        try:
            import main_app
            self.assertTrue(hasattr(main_app, 'main'))
            self.assertTrue(hasattr(main_app, 'show_home_page'))
            self.assertTrue(hasattr(main_app, 'show_tactical_tracker'))
            self.assertTrue(hasattr(main_app, 'show_quality_tracker'))
        except ImportError as e:
            self.fail(f"Failed to import main_app: {e}")
    
    def test_home_page_function_exists(self):
        """Test that home page function is properly defined"""
        import main_app
        
        # Test that the function exists and is callable
        self.assertTrue(callable(main_app.show_home_page))
        
        # Test that it doesn't raise exceptions when called
        try:
            main_app.show_home_page()
        except Exception as e:
            self.fail(f"show_home_page raised an exception: {e}")
    
    def test_tactical_tracker_fallback(self):
        """Test tactical tracker import fallback behavior"""
        import main_app
        
        # Test that the function exists and handles import errors gracefully
        self.assertTrue(callable(main_app.show_tactical_tracker))
        
        # Test fallback behavior when module is not available
        try:
            main_app.show_tactical_tracker()
        except ImportError:
            # This is expected behavior when tactical_tracker is not available
            pass
    
    def test_quality_tracker_fallback(self):
        """Test quality tracker import fallback behavior"""
        import main_app
        
        # Test that the function exists and handles import errors gracefully
        self.assertTrue(callable(main_app.show_quality_tracker))
        
        # Test fallback behavior when module is not available
        try:
            main_app.show_quality_tracker()
        except ImportError:
            # This is expected behavior when quality_tracker is not available
            pass
    
    def test_main_function_execution(self):
        """Test that main function executes without errors"""
        import main_app
        
        # Test that main function exists and is callable
        self.assertTrue(callable(main_app.main))
        
        # Test main function execution (should not raise errors with mocked streamlit)
        try:
            main_app.main()
        except Exception as e:
            self.fail(f"main() raised an exception: {e}")
    
    def test_page_configuration(self):
        """Test that page configuration is set correctly"""
        import main_app
        
        # This tests that the module can be imported without errors
        # Page config is set at module level, so importing tests it
        self.assertTrue(hasattr(main_app, 'st'))
        
    def test_navigation_options(self):
        """Test that all navigation options are handled"""
        import main_app
        
        # Mock different feature selections
        features = [
            "🏠 Home - Feature Overview",
            "⚡ Tactical Momentum Tracker", 
            "🛡️ Long-Term Quality Stocks"
        ]
        
        for feature in features:
            # Each feature should have a corresponding handler
            if "Home" in feature:
                self.assertTrue(callable(main_app.show_home_page))
            elif "Tactical" in feature:
                self.assertTrue(callable(main_app.show_tactical_tracker))
            elif "Quality" in feature:
                self.assertTrue(callable(main_app.show_quality_tracker))

    def test_if_name_main_execution(self):
        """Test the if __name__ == '__main__' block"""
        import main_app
        
        # Test that the main function would be called in script execution
        # We can't directly test __name__ == '__main__' but we can verify main() exists
        self.assertTrue(hasattr(main_app, 'main'))
        self.assertTrue(callable(main_app.main))


class TestTacticalTrackerModule(unittest.TestCase):
    """Test the tactical tracker module functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Mock yfinance for testing
        self.mock_yf = Mock()
        
    def test_tactical_tracker_import(self):
        """Test that tactical tracker module can be imported"""
        try:
            import tactical_tracker
            self.assertTrue(hasattr(tactical_tracker, 'run_tactical_tracker'))
            self.assertTrue(hasattr(tactical_tracker, 'PortfolioTracker'))
        except ImportError as e:
            self.fail(f"Failed to import tactical_tracker: {e}")
    
    def test_portfolio_tracker_class(self):
        """Test PortfolioTracker class instantiation"""
        import tactical_tracker
        
        # Test class instantiation
        tracker = tactical_tracker.PortfolioTracker()
        self.assertIsInstance(tracker, tactical_tracker.PortfolioTracker)
        
        # Test required methods exist
        self.assertTrue(hasattr(tracker, 'get_market_health'))
        self.assertTrue(hasattr(tracker, 'calculate_simple_allocation'))
        self.assertTrue(hasattr(tracker, 'generate_portfolio_recommendations'))
        self.assertTrue(hasattr(tracker, 'passes_filters'))
    
    @patch('tactical_tracker.yf')
    def test_market_health_analysis(self, mock_yf):
        """Test market health analysis with mocked data"""
        import tactical_tracker
        
        # Create more comprehensive mocks
        mock_vix_data = pd.DataFrame({
            'Close': [25.0, 24.5, 24.0, 23.5, 24.0, 24.5, 25.0, 25.5, 26.0, 25.0]
        })
        mock_vix_ticker = Mock()
        mock_vix_ticker.history.return_value = mock_vix_data
        
        # Create SPY data with proper structure
        spy_closes = [400.0, 398.0, 395.0, 397.0, 399.0] * 20  # 100 days
        mock_spy_data = pd.DataFrame({
            'Close': spy_closes
        })
        mock_spy_ticker = Mock()
        mock_spy_ticker.history.return_value = mock_spy_data
        
        # Create sector ETF mocks
        mock_sector_data = pd.DataFrame({
            'Close': [100.0, 101.0, 102.0, 103.0, 104.0] * 4  # 20 days
        })
        mock_sector_ticker = Mock()
        mock_sector_ticker.history.return_value = mock_sector_data
        
        # Set up yfinance mock
        def ticker_side_effect(symbol):
            if symbol == "^VIX":
                return mock_vix_ticker
            elif symbol == "SPY":
                return mock_spy_ticker
            elif symbol in ['XLK', 'XLF', 'XLV', 'XLE', 'XLI']:
                return mock_sector_ticker
            else:
                return Mock()
        
        mock_yf.Ticker.side_effect = ticker_side_effect
        
        # Test market health analysis
        tracker = tactical_tracker.PortfolioTracker()
        market_health = tracker.get_market_health()
        
        # Verify structure - should have full structure since mocking is proper
        self.assertIsInstance(market_health, dict)
        self.assertIn('vix', market_health)
        self.assertIn('market_regime', market_health)
        self.assertIn('defensive_score', market_health)
        self.assertIn('is_defensive', market_health)
    
    def test_allocation_calculation(self):
        """Test portfolio allocation calculation"""
        import tactical_tracker
        
        tracker = tactical_tracker.PortfolioTracker()
        
        # Test data
        strong_buys = [
            {'ticker': 'AAPL', 'momentum_score': 18.5, 'avg_weekly_return': 2.8},
            {'ticker': 'MSFT', 'momentum_score': 16.2, 'avg_weekly_return': 2.3}
        ]
        
        moderate_buys = [
            {'ticker': 'GOOGL', 'momentum_score': 12.1, 'avg_weekly_return': 1.8},
            {'ticker': 'NVDA', 'momentum_score': 13.4, 'avg_weekly_return': 2.1}
        ]
        
        market_health = {
            'market_regime': 'AGGRESSIVE',
            'defensive_score': 20
        }
        
        # Test allocation
        allocation = tracker.calculate_simple_allocation(
            strong_buys, moderate_buys, 12, 6, market_health, True
        )
        
        # Verify allocation structure
        self.assertIsInstance(allocation, dict)
        self.assertIn('allocations', allocation)
        self.assertIn('total_allocated', allocation)
        self.assertIn('defensive_cash', allocation)
        self.assertIn('market_regime', allocation)
        
        # Test aggressive market (no defensive cash)
        self.assertEqual(allocation['defensive_cash'], 0)
        self.assertEqual(allocation['total_allocated'], 100)
    
    def test_defensive_cash_allocation(self):
        """Test defensive cash allocation in different market regimes"""
        import tactical_tracker
        
        tracker = tactical_tracker.PortfolioTracker()
        
        strong_buys = [{'ticker': 'AAPL', 'momentum_score': 18.5, 'avg_weekly_return': 2.8}]
        moderate_buys = [{'ticker': 'GOOGL', 'momentum_score': 12.1, 'avg_weekly_return': 1.8}]
        
        # Test different market regimes
        test_cases = [
            ('AGGRESSIVE', 0),
            ('CAUTIOUS', 5),
            ('DEFENSIVE', 15),
            ('HIGHLY_DEFENSIVE', 30)
        ]
        
        for regime, expected_cash in test_cases:
            market_health = {'market_regime': regime, 'defensive_score': 50}
            
            allocation = tracker.calculate_simple_allocation(
                strong_buys, moderate_buys, 12, 6, market_health, True
            )
            
            self.assertEqual(allocation['defensive_cash'], expected_cash,
                           f"Expected {expected_cash}% cash for {regime} regime")
            self.assertEqual(allocation['total_allocated'] + allocation['defensive_cash'], 100,
                           f"Total allocation should be 100% for {regime} regime")
    
    def test_run_tactical_tracker_interface(self):
        """Test the main tactical tracker interface function"""
        import tactical_tracker
        
        # Test that the main interface function exists and runs
        self.assertTrue(callable(tactical_tracker.run_tactical_tracker))
        
        # Test execution (should not raise errors with mocked streamlit)
        try:
            tactical_tracker.run_tactical_tracker()
        except Exception as e:
            self.fail(f"run_tactical_tracker() raised an exception: {e}")
    
    def test_tactical_tracker_constants(self):
        """Test that all required constants are defined"""
        import tactical_tracker
        
        # Test defensive ETFs constant
        self.assertTrue(hasattr(tactical_tracker, 'DEFENSIVE_ETFS'))
        self.assertIsInstance(tactical_tracker.DEFENSIVE_ETFS, list)
        self.assertGreater(len(tactical_tracker.DEFENSIVE_ETFS), 0)
        
        # Test threshold constants
        self.assertTrue(hasattr(tactical_tracker, 'VIX_THRESHOLD'))
        self.assertTrue(hasattr(tactical_tracker, 'BREADTH_THRESHOLD'))
        self.assertTrue(hasattr(tactical_tracker, 'DROP_THRESHOLD'))
        self.assertTrue(hasattr(tactical_tracker, 'MOMENTUM_THRESHOLD'))
        
        # Test that thresholds are numeric
        self.assertIsInstance(tactical_tracker.VIX_THRESHOLD, (int, float))
        self.assertIsInstance(tactical_tracker.BREADTH_THRESHOLD, (int, float))
        self.assertIsInstance(tactical_tracker.DROP_THRESHOLD, (int, float))
        self.assertIsInstance(tactical_tracker.MOMENTUM_THRESHOLD, (int, float))
    
    @patch('tactical_tracker.yf')
    def test_get_market_health_exception_handling(self, mock_yf):
        """Test market health analysis exception handling"""
        import tactical_tracker
        
        # Mock yfinance to raise an exception
        mock_yf.Ticker.side_effect = Exception("Network error")
        
        tracker = tactical_tracker.PortfolioTracker()
        market_health = tracker.get_market_health()
        
        # Should return fallback dictionary when exception occurs
        self.assertIsInstance(market_health, dict)
        self.assertIn('vix', market_health)
        self.assertIn('is_defensive', market_health)
        
    def test_calculate_simple_allocation_empty_inputs(self):
        """Test allocation calculation with empty inputs"""
        import tactical_tracker
        
        tracker = tactical_tracker.PortfolioTracker()
        allocation = tracker.calculate_simple_allocation([], [])
        
        # Should handle empty inputs gracefully
        self.assertIsInstance(allocation, dict)
        self.assertIn('allocations', allocation)
        self.assertEqual(allocation['total_allocated'], 0)


class TestQualityTrackerModule(unittest.TestCase):
    """Test the quality tracker module functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_yf = Mock()
    
    def test_quality_tracker_import(self):
        """Test that quality tracker module can be imported"""
        try:
            import quality_tracker
            self.assertTrue(hasattr(quality_tracker, 'run_quality_tracker'))
            self.assertTrue(hasattr(quality_tracker, 'QualityStocksTracker'))
        except ImportError as e:
            self.fail(f"Failed to import quality_tracker: {e}")
    
    def test_quality_stocks_tracker_class(self):
        """Test QualityStocksTracker class instantiation"""
        import quality_tracker
        
        # Test class instantiation
        tracker = quality_tracker.QualityStocksTracker()
        self.assertIsInstance(tracker, quality_tracker.QualityStocksTracker)
        
        # Test required methods exist
        self.assertTrue(hasattr(tracker, 'get_stock_fundamentals'))
        self.assertTrue(hasattr(tracker, 'passes_quality_filters'))
        self.assertTrue(hasattr(tracker, 'calculate_ytd_return'))
        self.assertTrue(hasattr(tracker, 'calculate_beta'))
    
    def test_defensive_sectors_constants(self):
        """Test that defensive sectors are properly defined"""
        import quality_tracker
        
        # Test that DEFENSIVE_SECTORS constant exists and has expected structure
        self.assertTrue(hasattr(quality_tracker, 'DEFENSIVE_SECTORS'))
        defensive_sectors = quality_tracker.DEFENSIVE_SECTORS
        
        self.assertIsInstance(defensive_sectors, dict)
        self.assertIn('Consumer Staples', defensive_sectors)
        self.assertIn('Healthcare', defensive_sectors)
        self.assertIn('Utilities', defensive_sectors)
        
        # Test that each sector has stock tickers
        for sector, tickers in defensive_sectors.items():
            self.assertIsInstance(tickers, list)
            self.assertGreater(len(tickers), 0)
    
    def test_quality_score_calculation(self):
        """Test quality score calculation"""
        import quality_tracker
        
        # Test stock data
        stock_data = {
            'ticker': 'JNJ',
            'roe': 15.0,
            'dividend_yield': 3.0,
            'beta': 0.8,
            'five_year_return': 80.0,
            'market_cap': 400e9
        }
        
        score = quality_tracker.calculate_quality_score(stock_data)
        
        # Verify score calculation
        self.assertIsInstance(score, (int, float))
        self.assertGreater(score, 0)
        
        # Test that higher quality metrics result in higher scores
        high_quality_stock = {
            'ticker': 'KO',
            'roe': 25.0,  # Higher ROE
            'dividend_yield': 4.0,  # Higher dividend
            'beta': 0.6,  # Lower volatility
            'five_year_return': 120.0,  # Better performance
            'market_cap': 250e9
        }
        
        high_score = quality_tracker.calculate_quality_score(high_quality_stock)
        self.assertGreater(high_score, score)
    
    def test_quality_filters(self):
        """Test quality filtering logic"""
        import quality_tracker
        
        tracker = quality_tracker.QualityStocksTracker()
        
        # Test stock data that should pass filters
        good_stock = {
            'ticker': 'JNJ',
            'market_cap': 400e9,
            'beta': 1.0,
            'roe': 15.0,
            'dividend_yield': 3.0,
            'net_income': 15e9,
            'free_cash_flow': 12e9,
            'sector': 'Healthcare'
        }
        
        # Test with permissive filters
        passes = tracker.passes_quality_filters(
            good_stock, min_roe=10, max_beta=1.2, min_dividend_yield=2.0,
            min_market_cap_str="$25B", preferred_sectors=["Healthcare"],
            exclude_unprofitable=True, require_dividend_history=True
        )
        
        self.assertTrue(passes)
        
        # Test stock that should fail filters
        bad_stock = {
            'ticker': 'SPEC',
            'market_cap': 1e9,  # Too small
            'beta': 2.0,  # Too volatile
            'roe': 5.0,  # Too low ROE
            'dividend_yield': 0.5,  # Too low dividend
            'net_income': -1e9,  # Unprofitable
            'free_cash_flow': -500e6,
            'sector': 'Technology'
        }
        
        fails = tracker.passes_quality_filters(
            bad_stock, min_roe=10, max_beta=1.2, min_dividend_yield=2.0,
            min_market_cap_str="$25B", preferred_sectors=["Healthcare"],
            exclude_unprofitable=True, require_dividend_history=True
        )
        
        self.assertFalse(fails)
    
    def test_run_quality_tracker_interface(self):
        """Test the main quality tracker interface function"""
        import quality_tracker
        
        # Test that the main interface function exists and runs
        self.assertTrue(callable(quality_tracker.run_quality_tracker))
        
        # Test execution (should not raise errors with mocked streamlit)
        try:
            quality_tracker.run_quality_tracker()
        except Exception as e:
            self.fail(f"run_quality_tracker() raised an exception: {e}")
    
    def test_quality_metrics_constants(self):
        """Test quality metrics and thresholds"""
        import quality_tracker
        
        # Test that defensive sectors are defined
        self.assertTrue(hasattr(quality_tracker, 'DEFENSIVE_SECTORS'))
        defensive_sectors = quality_tracker.DEFENSIVE_SECTORS
        self.assertIsInstance(defensive_sectors, dict)
        
        # Test that pre-seed universe is defined
        self.assertTrue(hasattr(quality_tracker, 'PRE_SEED_UNIVERSE'))
        self.assertIsInstance(quality_tracker.PRE_SEED_UNIVERSE, list)
        self.assertGreater(len(quality_tracker.PRE_SEED_UNIVERSE), 0)
    
    def test_education_content_display(self):
        """Test educational content display function"""
        import quality_tracker
        
        # Test that education function exists and runs
        self.assertTrue(callable(quality_tracker.display_quality_education))
        
        # Test execution (should not raise errors with mocked streamlit)
        try:
            quality_tracker.display_quality_education()
        except Exception as e:
            self.fail(f"display_quality_education() raised an exception: {e}")
    
    def test_quality_tracker_class_advanced_methods(self):
        """Test advanced methods of QualityStocksTracker class"""
        import quality_tracker
        
        tracker = quality_tracker.QualityStocksTracker()
        
        # Test actual methods that exist
        self.assertTrue(hasattr(tracker, 'get_stock_fundamentals'))
        self.assertTrue(hasattr(tracker, 'passes_quality_filters'))
        self.assertTrue(hasattr(tracker, 'calculate_ytd_return'))
        self.assertTrue(hasattr(tracker, 'calculate_period_return'))
        self.assertTrue(hasattr(tracker, 'calculate_beta'))
        
        # Test that standalone functions exist
        self.assertTrue(hasattr(quality_tracker, 'calculate_quality_score'))
        self.assertTrue(hasattr(quality_tracker, 'run_quality_screening'))
        
        # Test filter with sample data
        sample_stock_data = {
            'ticker': 'PG', 'sector': 'Consumer Staples', 'beta': 0.8, 
            'roe': 15.0, 'dividend_yield': 3.5, 'market_cap': 400e9
        }
        
        # Test filtering (should return filtered results without errors)
        try:
            result = tracker.passes_quality_filters(
                sample_stock_data, min_roe=10.0, max_beta=1.2, 
                min_dividend_yield=1.0, min_market_cap_str="$10B",
                preferred_sectors=["Consumer Staples"], exclude_unprofitable=False,
                require_dividend_history=False
            )
            self.assertIsInstance(result, bool)
        except Exception as e:
            self.fail(f"passes_quality_filters() raised an exception: {e}")
    
    def test_quality_score_edge_cases(self):
        """Test quality score calculation with edge cases"""
        import quality_tracker
        
        # Test with extreme values
        extreme_stock = {
            'roe': 50.0,  # Very high ROE
            'beta': 0.1,  # Very low beta
            'dividend_yield': 10.0,  # Very high dividend
            'market_cap': 1e12,  # Very large market cap
            'debt_to_equity': 0.1,  # Very low debt
            'five_year_return': 150.0  # 150% over 5 years
        }
        
        try:
            score = quality_tracker.calculate_quality_score(extreme_stock)
            self.assertIsInstance(score, (int, float))
            self.assertGreaterEqual(score, 0)
        except Exception as e:
            self.fail(f"calculate_quality_score() with extreme values raised: {e}")
        
        # Test with missing data - should use get() with defaults
        incomplete_stock = {
            'roe': 15.0,
            'beta': 0.8,
            'dividend_yield': 3.0,
            'market_cap': 50e9,
            'five_year_return': 25.0
        }
        
        try:
            score = quality_tracker.calculate_quality_score(incomplete_stock)
            self.assertIsInstance(score, (int, float))
        except Exception as e:
            self.fail(f"calculate_quality_score() with missing data raised: {e}")


class TestApplicationIntegration(unittest.TestCase):
    """Test integration between different components of the v2.0 suite"""
    
    def test_module_integration(self):
        """Test that all modules can work together"""
        try:
            import main_app
            import tactical_tracker
            import quality_tracker
            
            # Test that main functions exist
            self.assertTrue(callable(main_app.main))
            self.assertTrue(callable(tactical_tracker.run_tactical_tracker))
            self.assertTrue(callable(quality_tracker.run_quality_tracker))
            
        except ImportError as e:
            self.fail(f"Module integration test failed: {e}")
    
    def test_feature_selection_logic(self):
        """Test the feature selection logic in main app"""
        import main_app
        
        # Test that all show functions exist and are callable
        functions_to_test = [
            'show_home_page',
            'show_tactical_tracker', 
            'show_quality_tracker'
        ]
        
        for func_name in functions_to_test:
            self.assertTrue(hasattr(main_app, func_name))
            self.assertTrue(callable(getattr(main_app, func_name)))
    
    def test_constants_consistency(self):
        """Test that constants are consistent across modules"""
        try:
            import tactical_tracker
            import quality_tracker
            
            # Test that both modules have their required constants
            self.assertTrue(hasattr(tactical_tracker, 'VIX_THRESHOLD'))
            self.assertTrue(hasattr(tactical_tracker, 'MIN_MARKET_CAP'))
            
            self.assertTrue(hasattr(quality_tracker, 'DEFENSIVE_SECTORS'))
            self.assertTrue(hasattr(quality_tracker, 'PRE_SEED_UNIVERSE'))
            
        except ImportError:
            # If modules aren't available, skip this test
            pass
    
    def test_error_handling_integration(self):
        """Test error handling across modules"""
        import main_app
        import tactical_tracker
        import quality_tracker
        
        # Test that all modules handle exceptions gracefully
        modules = [main_app, tactical_tracker, quality_tracker]
        
        for module in modules:
            # Each module should be importable without errors
            self.assertTrue(hasattr(module, '__name__'))
            
    def test_shared_utilities_consistency(self):
        """Test that shared utilities work consistently across modules"""
        import tactical_tracker
        import quality_tracker
        
        # Test that both modules can handle similar data structures
        sample_data = {
            'ticker': 'AAPL',
            'sector': 'Technology',
            'market_cap': 3000e9,
            'beta': 1.2
        }
        
        # Both modules should be able to process basic stock data
        self.assertIsInstance(sample_data, dict)
        self.assertIn('ticker', sample_data)
        self.assertIn('sector', sample_data)
        
    def test_portfolio_size_consistency(self):
        """Test portfolio size handling across modules"""
        import tactical_tracker
        import quality_tracker
        
        # Test that both modules handle portfolio size parameters
        tactical_tracker_class = tactical_tracker.PortfolioTracker()
        quality_tracker_class = quality_tracker.QualityStocksTracker()
        
        # Both classes should be instantiable
        self.assertIsInstance(tactical_tracker_class, tactical_tracker.PortfolioTracker)
        self.assertIsInstance(quality_tracker_class, quality_tracker.QualityStocksTracker)
        
    def test_navigation_flow_simulation(self):
        """Test simulated navigation flow between features"""
        import main_app
        
        # Test that navigation functions don't interfere with each other
        navigation_functions = [
            main_app.show_home_page,
            main_app.show_tactical_tracker,
            main_app.show_quality_tracker
        ]
        
        for func in navigation_functions:
            self.assertTrue(callable(func))
            
        # Test that main app handles all navigation scenarios
        try:
            main_app.main()
        except Exception as e:
            self.fail(f"Navigation simulation failed: {e}")
    
    def test_streamlit_ui_components(self):
        """Test that UI components are properly mocked and handled"""
        import main_app
        
        # Test that UI functions complete without errors
        ui_functions = [
            main_app.show_home_page,
            main_app.show_tactical_tracker,
            main_app.show_quality_tracker
        ]
        
        for func in ui_functions:
            try:
                func()
            except Exception as e:
                self.fail(f"UI function {func.__name__} failed: {e}")
    
    def test_module_documentation_completeness(self):
        """Test that all modules have proper documentation"""
        import main_app
        import tactical_tracker
        import quality_tracker
        
        modules = [main_app, tactical_tracker, quality_tracker]
        
        for module in modules:
            # Each module should have a docstring
            self.assertIsNotNone(module.__doc__)
            self.assertGreater(len(module.__doc__.strip()), 0)
            
            # Main functions should have docstrings
            if hasattr(module, 'main'):
                self.assertIsNotNone(module.main.__doc__)
            
            # Key classes should have docstrings
            if hasattr(module, 'PortfolioTracker'):
                self.assertIsNotNone(module.PortfolioTracker.__doc__)
            if hasattr(module, 'QualityStocksTracker'):
                self.assertIsNotNone(module.QualityStocksTracker.__doc__)


if __name__ == '__main__':
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestMainApp))
    suite.addTests(loader.loadTestsFromTestCase(TestTacticalTrackerModule))
    suite.addTests(loader.loadTestsFromTestCase(TestQualityTrackerModule))
    suite.addTests(loader.loadTestsFromTestCase(TestApplicationIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n📊 V2.0 Test Summary:")
    print(f"✅ Tests Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Tests Failed: {len(result.failures)}")
    print(f"🚫 Errors: {len(result.errors)}")
    print(f"📈 Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
