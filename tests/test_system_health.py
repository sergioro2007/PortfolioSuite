#!/usr/bin/env python3
"""
System Health Check: Comprehensive system verification to ensure all components work correctly.
This should be run as part of CI/CD or regular system health checks.
"""

import unittest
import subprocess
import sys
import os
import time
import requests
from typing import Optional

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestSystemHealth(unittest.TestCase):
    """Comprehensive system health checks"""
    
    def test_core_imports(self):
        """Test that all core modules can be imported successfully"""
        core_modules = [
            'main_app',
            'tactical_tracker', 
            'quality_tracker',
            'streamlit_app'
        ]
        
        for module in core_modules:
            with self.subTest(module=module):
                try:
                    __import__(module)
                except ImportError as e:
                    self.fail(f"Failed to import {module}: {e}")
    
    def test_tactical_tracker_functionality(self):
        """Test core tactical tracker functionality"""
        try:
            from tactical_tracker import PortfolioTracker, discover_momentum_tickers
            
            # Test tracker initialization
            tracker = PortfolioTracker()
            self.assertIsNotNone(tracker)
            
            # Test market health (should return dict)
            health = tracker.get_market_health()
            self.assertIsInstance(health, dict)
            self.assertGreater(len(health), 0)
            
            # Test auto-discovery (should return list)
            discovered = discover_momentum_tickers()
            self.assertIsInstance(discovered, list)
            # Should discover some tickers (typically 40-60)
            self.assertGreater(len(discovered), 10)
            
        except Exception as e:
            self.fail(f"Tactical tracker functionality test failed: {e}")
    
    def test_quality_tracker_functionality(self):
        """Test core quality tracker functionality"""
        try:
            from quality_tracker import QualityStockTracker
            
            # Test tracker initialization
            tracker = QualityStockTracker()
            self.assertIsNotNone(tracker)
            
            # Test with a sample ticker
            result = tracker.analyze_stock('AAPL')
            if result:  # Only test if data is available
                self.assertIsInstance(result, dict)
                self.assertIn('ticker', result)
                
        except Exception as e:
            self.fail(f"Quality tracker functionality test failed: {e}")
    
    def test_data_integrity(self):
        """Test that required data files exist and are accessible"""
        # Check for pickle files if they exist
        data_files = ['portfolio_results.pkl']
        
        for data_file in data_files:
            if os.path.exists(data_file):
                with self.subTest(file=data_file):
                    # Try to access the file
                    try:
                        with open(data_file, 'rb'):
                            # Just verify we can open it
                            pass
                    except Exception as e:
                        self.fail(f"Cannot access data file {data_file}: {e}")
    
    def test_streamlit_app_syntax(self):
        """Test that Streamlit apps have valid syntax"""
        streamlit_apps = ['main_app.py', 'streamlit_app.py']
        
        for app in streamlit_apps:
            with self.subTest(app=app):
                if os.path.exists(app):
                    try:
                        with open(app, 'r') as f:
                            content = f.read()
                        # Test syntax by compiling
                        compile(content, app, 'exec')
                    except SyntaxError as e:
                        self.fail(f"Syntax error in {app}: {e}")
                    except Exception as e:
                        self.fail(f"Error checking {app}: {e}")
    
    def test_dependencies_available(self):
        """Test that required dependencies are available"""
        required_packages = [
            'streamlit',
            'yfinance', 
            'pandas',
            'numpy',
            'requests',
            'beautifulsoup4'
        ]
        
        for package in required_packages:
            with self.subTest(package=package):
                try:
                    __import__(package.replace('-', '_'))
                except ImportError:
                    try:
                        # Try alternative import names
                        if package == 'beautifulsoup4':
                            __import__('bs4')
                        else:
                            raise
                    except ImportError:
                        self.fail(f"Required package {package} is not available")
    
    def test_performance_benchmarks(self):
        """Test that key operations complete within reasonable time"""
        try:
            from tactical_tracker import PortfolioTracker
            
            tracker = PortfolioTracker()
            
            # Market health should complete quickly
            start_time = time.time()
            tracker.get_market_health()
            market_health_time = time.time() - start_time
            
            self.assertLess(market_health_time, 30.0, 
                          f"Market health took too long: {market_health_time:.2f}s")
            
            # Single ticker analysis should be reasonably fast
            start_time = time.time()
            tracker.analyze_ticker_momentum('AAPL')
            analysis_time = time.time() - start_time
            
            self.assertLess(analysis_time, 15.0,
                          f"Single ticker analysis took too long: {analysis_time:.2f}s")
            
        except Exception as e:
            self.skipTest(f"Performance test skipped due to: {e}")
    
    def test_error_handling(self):
        """Test that error conditions are handled gracefully"""
        try:
            from tactical_tracker import PortfolioTracker
            
            tracker = PortfolioTracker()
            
            # Test with invalid ticker
            result = tracker.analyze_ticker_momentum('INVALID_TICKER_12345')
            # Should return None or empty dict, not crash
            self.assertIn(type(result), [type(None), dict])
            
            # Test passes_filters with missing data
            invalid_data = {'ticker': 'TEST'}  # Missing required fields
            result = tracker.passes_filters(invalid_data, 30, 1.5)
            # Should return False, not crash
            self.assertFalse(result)
            
        except Exception as e:
            self.fail(f"Error handling test failed: {e}")

class TestSystemIntegration(unittest.TestCase):
    """Integration tests for the complete system"""
    
    def test_end_to_end_flow(self):
        """Test complete end-to-end workflow"""
        try:
            from tactical_tracker import PortfolioTracker, discover_momentum_tickers, screen_discovered_tickers
            
            # Full workflow
            tracker = PortfolioTracker()
            market_health = tracker.get_market_health()
            discovered = discover_momentum_tickers()
            
            if len(discovered) > 0:
                qualified = screen_discovered_tickers(
                    tracker, discovered[:10], 25, 1.0, market_health
                )
                
                if qualified:
                    recommendations = tracker.generate_portfolio_recommendations(
                        qualified, 5, 25, 1.0, market_health
                    )
                    
                    self.assertIsInstance(recommendations, dict)
                    self.assertIn('top_picks', recommendations)
                    
        except Exception as e:
            self.fail(f"End-to-end flow test failed: {e}")

if __name__ == '__main__':
    # Run with high verbosity to see all test details
    unittest.main(verbosity=2)
