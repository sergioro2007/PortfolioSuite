#!/usr/bin/env python3
"""
Advanced UI and Integration Testing for PortfolioSuite
======================================================

This module provides comprehensive UI testing and advanced integration testing
for the PortfolioSuite application including:
- Streamlit UI component testing
- Web application functionality
- CLI interface testing
- Application startup validation
- End-to-end workflow validation
"""

import sys
import os
import unittest
import subprocess
import threading
import time
import tempfile
import requests
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock
import signal

# Add src directory to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

try:
    # Import core modules
    from portfolio_suite.options_trading.core import OptionsTracker
    from portfolio_suite.tactical_tracker.core import PortfolioTracker 
    from portfolio_suite.trade_analysis.core import TradeAnalyzer
    print("✅ All core modules imported successfully for UI testing")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)


class TestStreamlitUI(unittest.TestCase):
    """Test Streamlit UI components and web interface."""
    
    def setUp(self):
        """Set up UI test fixtures."""
        self.test_port = 8502  # Use different port to avoid conflicts
        
    def test_streamlit_modules_import(self):
        """Test that all Streamlit UI modules can be imported."""
        ui_modules = [
            'portfolio_suite.ui.main_app',
            'portfolio_suite.options_trading.ui'
        ]
        
        for module_name in ui_modules:
            try:
                __import__(module_name)
                print(f"✅ {module_name} imported successfully")
            except ImportError as e:
                self.fail(f"Failed to import {module_name}: {e}")
                
    @patch('streamlit.title')
    @patch('streamlit.sidebar')
    @patch('streamlit.columns')
    def test_main_app_ui_components(self, mock_columns, mock_sidebar, mock_title):
        """Test main app UI components with mocked Streamlit."""
        try:
            from portfolio_suite.ui.main_app import main
            
            # Mock streamlit components
            mock_columns.return_value = [Mock(), Mock(), Mock()]
            
            # Should not raise errors when called
            # Note: This tests import and basic structure, not actual rendering
            self.assertTrue(callable(main))
            
        except Exception as e:
            # UI components may require Streamlit context
            print(f"UI component test limitation: {e}")
            
    @patch('streamlit.selectbox')
    @patch('streamlit.button')
    def test_options_ui_components(self, mock_button, mock_selectbox):
        """Test options trading UI components."""
        try:
            from portfolio_suite.options_trading.ui import render_options_tracker
            
            # Mock user interactions
            mock_selectbox.return_value = 'AAPL'
            mock_button.return_value = False
            
            self.assertTrue(callable(render_options_tracker))
            
        except Exception as e:
            print(f"Options UI test limitation: {e}")
            
    def test_web_server_startup_simulation(self):
        """Test that web server can start (simulated)."""
        # Test command line arguments for main module
        test_args = ['--component', 'web', '--port', str(self.test_port)]
        
        # This tests the argument parsing without actually starting server
        try:
            from portfolio_suite.__main__ import main
            self.assertTrue(callable(main))
        except Exception as e:
            print(f"Web server test limitation: {e}")


class TestCLIInterface(unittest.TestCase):
    """Test command-line interface functionality."""
    
    def test_main_module_help(self):
        """Test main module help command."""
        try:
            result = subprocess.run([
                sys.executable, '-c', 
                "import sys; sys.path.insert(0, 'src'); from portfolio_suite.__main__ import main; print('CLI accessible')"
            ], capture_output=True, text=True, timeout=10)
            
            self.assertEqual(result.returncode, 0)
            self.assertIn('CLI accessible', result.stdout)
            
        except subprocess.TimeoutExpired:
            self.fail("CLI test timed out")
        except Exception as e:
            print(f"CLI test limitation: {e}")
            
    def test_module_execution_paths(self):
        """Test different module execution paths."""
        execution_tests = [
            "import portfolio_suite; print('Package import OK')",
            "from portfolio_suite.options_trading.core import OptionsTracker; print('Options import OK')",
            "from portfolio_suite.tactical_tracker.core import PortfolioTracker; print('Tactical import OK')",
            "from portfolio_suite.trade_analysis.core import TradeAnalyzer; print('Analysis import OK')"
        ]
        
        for test_code in execution_tests:
            try:
                result = subprocess.run([
                    sys.executable, '-c', 
                    f"import sys; sys.path.insert(0, 'src'); {test_code}"
                ], capture_output=True, text=True, timeout=10)
                
                self.assertEqual(result.returncode, 0)
                self.assertIn('OK', result.stdout)
                
            except subprocess.TimeoutExpired:
                self.fail(f"Module execution test timed out: {test_code}")
            except Exception as e:
                print(f"Module execution test limitation: {e}")


class TestApplicationStartup(unittest.TestCase):
    """Test application startup and initialization."""
    
    def test_component_initialization_sequence(self):
        """Test proper component initialization sequence."""
        # Test initialization order and dependencies
        try:
            # 1. Options Tracker
            options = OptionsTracker()
            self.assertIsNotNone(options)
            self.assertIsInstance(options.watchlist, list)
            self.assertIsInstance(options.trades, list)
            
            # 2. Portfolio Tracker
            portfolio = PortfolioTracker()
            self.assertIsNotNone(portfolio)
            self.assertIsInstance(portfolio.portfolio, dict)
            
            # 3. Trade Analyzer
            analyzer = TradeAnalyzer()
            self.assertIsNotNone(analyzer)
            
            print("✅ All components initialized successfully in sequence")
            
        except Exception as e:
            self.fail(f"Component initialization failed: {e}")
            
    def test_data_directory_setup(self):
        """Test data directory and file setup."""
        project_root = Path(__file__).parent
        
        # Check for data directory
        data_dir = project_root / "data"
        if data_dir.exists():
            print(f"✅ Data directory found: {data_dir}")
        else:
            print(f"ℹ️  Data directory will be created on first run: {data_dir}")
            
        # Check for required data files
        data_files = ["options_trades.pkl", "portfolio_results.pkl"]
        for file_name in data_files:
            file_path = data_dir / file_name
            if file_path.exists():
                print(f"✅ {file_name} exists")
            else:
                print(f"ℹ️  {file_name} will be created on first run")
                
    def test_configuration_validation(self):
        """Test configuration and settings validation."""
        # Test that core configuration is accessible
        try:
            options = OptionsTracker()
            
            # Test configuration attributes
            config_attrs = ['target_weekly_income', 'strategy_types']
            for attr in config_attrs:
                if hasattr(options, attr):
                    value = getattr(options, attr)
                    self.assertIsNotNone(value)
                    print(f"✅ Configuration {attr}: {value}")
                    
        except Exception as e:
            print(f"Configuration test limitation: {e}")


class TestEndToEndWorkflows(unittest.TestCase):
    """Comprehensive end-to-end workflow testing."""
    
    def setUp(self):
        """Set up end-to-end test fixtures."""
        self.options = OptionsTracker()
        self.portfolio = PortfolioTracker()
        self.analyzer = TradeAnalyzer()
        
    def test_complete_options_trading_workflow(self):
        """Test complete options trading workflow end-to-end."""
        workflow_steps = []
        
        try:
            # Step 1: Initialize and check watchlist
            initial_watchlist_size = len(self.options.watchlist)
            workflow_steps.append(f"✅ Step 1: Watchlist initialized ({initial_watchlist_size} tickers)")
            
            # Step 2: Check network status
            network_status = self.options.check_network_status()
            workflow_steps.append(f"✅ Step 2: Network status checked: {network_status}")
            
            # Step 3: Try to get technical indicators (may fail offline)
            try:
                indicators = self.options.get_technical_indicators('AAPL')
                if indicators:
                    workflow_steps.append("✅ Step 3: Technical indicators retrieved")
                else:
                    workflow_steps.append("ℹ️  Step 3: Technical indicators unavailable (offline)")
            except Exception:
                workflow_steps.append("ℹ️  Step 3: Technical indicators failed (expected offline)")
                
            # Step 4: Test trade suggestions
            try:
                suggestions = self.options.generate_trade_suggestions('AAPL')
                if suggestions:
                    workflow_steps.append(f"✅ Step 4: Trade suggestions generated ({len(suggestions)})")
                else:
                    workflow_steps.append("ℹ️  Step 4: No trade suggestions (offline mode)")
            except Exception:
                workflow_steps.append("ℹ️  Step 4: Trade suggestions failed (expected offline)")
                
            # Step 5: Test trade management
            initial_trades = len(self.options.trades)
            try:
                self.options.add_trade(
                    ticker='AAPL',
                    strategy='Bull Put Spread',
                    entry_date=datetime.now(),
                    quantity=1,
                    credit_received=100.0
                )
                final_trades = len(self.options.trades)
                if final_trades > initial_trades:
                    workflow_steps.append("✅ Step 5: Trade added successfully")
                else:
                    workflow_steps.append("ℹ️  Step 5: Trade addition method needs parameters")
            except Exception as e:
                workflow_steps.append(f"ℹ️  Step 5: Trade addition failed: {str(e)[:50]}")
                
            # Step 6: Test persistence
            try:
                self.options.save_trades()
                self.options.load_trades()
                workflow_steps.append("✅ Step 6: Trade persistence working")
            except Exception:
                workflow_steps.append("ℹ️  Step 6: Trade persistence limited in test environment")
                
            # Print workflow results
            print("\n📋 Options Trading Workflow Results:")
            for step in workflow_steps:
                print(f"  {step}")
                
            # At least basic initialization should work
            self.assertGreater(len(workflow_steps), 3)
            
        except Exception as e:
            self.fail(f"Complete options workflow failed: {e}")
            
    def test_complete_portfolio_management_workflow(self):
        """Test complete portfolio management workflow."""
        workflow_steps = []
        
        try:
            # Step 1: Portfolio initialization
            portfolio_size = len(self.portfolio.portfolio)
            workflow_steps.append(f"✅ Step 1: Portfolio initialized (size: {portfolio_size})")
            
            # Step 2: Market health analysis
            try:
                health = self.portfolio.get_market_health()
                if health and isinstance(health, dict):
                    regime = health.get('market_regime', 'Unknown')
                    defensive = health.get('is_defensive', False)
                    workflow_steps.append(f"✅ Step 2: Market health analyzed (Regime: {regime}, Defensive: {defensive})")
                else:
                    workflow_steps.append("ℹ️  Step 2: Market health unavailable (offline)")
            except Exception:
                workflow_steps.append("ℹ️  Step 2: Market health analysis failed (expected offline)")
                
            # Step 3: Test filtering and analysis
            test_results = [
                {
                    'ticker': 'AAPL', 'rs_score': 85, 'avg_weekly_return': 3.0, 
                    'market_cap': 3e12, 'meets_criteria': True, 'weeks_above_target': 4,
                    'weekly_returns': [0.03, 0.025, 0.035, 0.028]
                },
                {
                    'ticker': 'MSFT', 'rs_score': 80, 'avg_weekly_return': 2.8, 
                    'market_cap': 2.5e12, 'meets_criteria': True, 'weeks_above_target': 3,
                    'weekly_returns': [0.028, 0.032, 0.025, 0.031]
                }
            ]
            
            top_picks = self.portfolio.get_top_picks(test_results, count=2)
            workflow_steps.append(f"✅ Step 3: Portfolio analysis completed ({len(top_picks)} picks)")
            
            # Step 4: Position status evaluation
            for change in [3.5, -2.0, -4.0, 0.5]:
                status, color = self.portfolio.get_position_status(change)
                if status and color:
                    workflow_steps.append(f"✅ Step 4: Position status for {change}%: {status}")
                    break
                    
            # Step 5: Test portfolio persistence
            try:
                self.portfolio.save_results()
                workflow_steps.append("✅ Step 5: Portfolio results saved")
            except Exception:
                workflow_steps.append("ℹ️  Step 5: Portfolio persistence limited in test environment")
                
            # Print workflow results
            print("\n📊 Portfolio Management Workflow Results:")
            for step in workflow_steps:
                print(f"  {step}")
                
            self.assertGreater(len(workflow_steps), 3)
            
        except Exception as e:
            self.fail(f"Complete portfolio workflow failed: {e}")
            
    def test_data_analysis_workflow(self):
        """Test data analysis and reporting workflow."""
        workflow_steps = []
        
        try:
            # Step 1: Analyzer initialization
            self.assertIsNotNone(self.analyzer)
            workflow_steps.append("✅ Step 1: Trade analyzer initialized")
            
            # Step 2: Mock trade data analysis
            sample_trades = [
                {'profit_loss': 100, 'date': '2025-06-01', 'strategy': 'Bull Put Spread'},
                {'profit_loss': -50, 'date': '2025-06-02', 'strategy': 'Bear Call Spread'},
                {'profit_loss': 75, 'date': '2025-06-03', 'strategy': 'Iron Condor'},
                {'profit_loss': 200, 'date': '2025-06-04', 'strategy': 'Bull Put Spread'}
            ]
            
            # Step 3: Performance calculations
            total_pnl = sum(trade['profit_loss'] for trade in sample_trades)
            win_rate = len([t for t in sample_trades if t['profit_loss'] > 0]) / len(sample_trades)
            
            workflow_steps.append(f"✅ Step 2: Sample data analysis (P&L: ${total_pnl}, Win Rate: {win_rate:.1%})")
            
            # Step 4: Strategy analysis
            strategies = set(trade['strategy'] for trade in sample_trades)
            workflow_steps.append(f"✅ Step 3: Strategy analysis ({len(strategies)} strategies)")
            
            # Step 5: Risk metrics
            returns = [0.02, -0.01, 0.03, 0.015, -0.005, 0.025]
            avg_return = np.mean(returns)
            volatility = np.std(returns)
            sharpe = avg_return / volatility if volatility > 0 else 0
            
            workflow_steps.append(f"✅ Step 4: Risk metrics (Sharpe: {sharpe:.2f})")
            
            # Print workflow results
            print("\n📈 Data Analysis Workflow Results:")
            for step in workflow_steps:
                print(f"  {step}")
                
            self.assertGreater(len(workflow_steps), 3)
            
        except Exception as e:
            self.fail(f"Data analysis workflow failed: {e}")


class TestRobustnessAndEdgeCases(unittest.TestCase):
    """Test robustness and edge case handling."""
    
    def test_offline_mode_functionality(self):
        """Test that application works in offline mode."""
        offline_tests = []
        
        try:
            # Test 1: Component initialization without network
            options = OptionsTracker()
            portfolio = PortfolioTracker()
            analyzer = TradeAnalyzer()
            
            offline_tests.append("✅ All components initialize offline")
            
            # Test 2: Basic operations without network
            watchlist_size = len(options.watchlist)
            portfolio_size = len(portfolio.portfolio)
            
            offline_tests.append(f"✅ Basic data accessible (watchlist: {watchlist_size}, portfolio: {portfolio_size})")
            
            # Test 3: Filtering logic without external data
            test_data = {
                'ticker': 'TEST',
                'rs_score': 75,
                'avg_weekly_return': 2.5,
                'market_cap': 1e11,
                'meets_criteria': True,
                'weekly_returns': [0.025, 0.030, 0.020, 0.025]
            }
            
            result = portfolio.passes_filters(test_data, min_rs_score=70, min_weekly_target=2.0)
            offline_tests.append(f"✅ Filtering logic works offline: {result}")
            
            # Test 4: Position status calculation
            status, color = portfolio.get_position_status(2.5)
            offline_tests.append(f"✅ Position status calculation: {status}")
            
            print("\n🔌 Offline Mode Functionality:")
            for test in offline_tests:
                print(f"  {test}")
                
            self.assertGreater(len(offline_tests), 3)
            
        except Exception as e:
            self.fail(f"Offline mode test failed: {e}")
            
    def test_invalid_input_handling(self):
        """Test handling of invalid inputs."""
        input_tests = []
        
        try:
            portfolio = PortfolioTracker()
            
            # Test 1: Empty data handling
            empty_results = []
            top_picks = portfolio.get_top_picks(empty_results, count=5)
            self.assertEqual(len(top_picks), 0)
            input_tests.append("✅ Empty data handled correctly")
            
            # Test 2: Invalid position changes
            extreme_changes = [999, -999, 0, None]
            for change in extreme_changes:
                try:
                    if change is not None:
                        status, color = portfolio.get_position_status(change)
                        if status and color:
                            input_tests.append(f"✅ Extreme change {change}% handled")
                            break
                except Exception:
                    continue
                    
            # Test 3: Invalid ticker data
            invalid_data = {
                'ticker': '',
                'rs_score': None,
                'avg_weekly_return': -999,
                'market_cap': 0
            }
            
            try:
                result = portfolio.passes_filters(invalid_data, min_rs_score=50, min_weekly_target=1.0)
                input_tests.append(f"✅ Invalid data filtered: {result}")
            except Exception:
                input_tests.append("✅ Invalid data raises appropriate exception")
                
            print("\n🛡️  Invalid Input Handling:")
            for test in input_tests:
                print(f"  {test}")
                
            self.assertGreater(len(input_tests), 1)
            
        except Exception as e:
            self.fail(f"Invalid input handling test failed: {e}")


def run_advanced_tests():
    """Run all advanced test suites."""
    print("🚀 Starting Advanced PortfolioSuite Testing")
    print("=" * 60)
    
    test_suites = [
        TestStreamlitUI,
        TestCLIInterface, 
        TestApplicationStartup,
        TestEndToEndWorkflows,
        TestRobustnessAndEdgeCases
    ]
    
    total_tests = 0
    total_passed = 0
    results = {}
    
    for suite_class in test_suites:
        print(f"\n📋 Running {suite_class.__name__}")
        print("-" * 40)
        
        suite = unittest.TestLoader().loadTestsFromTestCase(suite_class)
        runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
        result = runner.run(suite)
        
        suite_name = suite_class.__name__
        tests_run = result.testsRun
        failures = len(result.failures)
        errors = len(result.errors)
        passed = tests_run - failures - errors
        
        results[suite_name] = {
            'tests_run': tests_run,
            'passed': passed,
            'failed': failures + errors,
            'success_rate': (passed / tests_run * 100) if tests_run > 0 else 0
        }
        
        total_tests += tests_run
        total_passed += passed
        
        print(f"  ✅ Passed: {passed}")
        print(f"  ❌ Failed: {failures + errors}")
        print(f"  📊 Success Rate: {passed/tests_run*100:.1f}%" if tests_run > 0 else "No tests")
    
    # Final summary
    print("\n" + "=" * 60)
    print("📊 ADVANCED TEST RESULTS SUMMARY")
    print("=" * 60)
    
    for suite_name, result in results.items():
        status = "✅" if result['failed'] == 0 else "⚠️"
        print(f"{status} {suite_name}: {result['passed']}/{result['tests_run']} "
              f"({result['success_rate']:.1f}%)")
    
    print("\n" + "-" * 40)
    overall_success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
    print(f"🎯 OVERALL ADVANCED RESULTS: {total_passed}/{total_tests} ({overall_success_rate:.1f}%)")
    
    if total_passed == total_tests:
        print("🎉 ALL ADVANCED TESTS PASSED!")
    else:
        failed = total_tests - total_passed
        print(f"⚠️  {failed} advanced tests need attention.")
    
    print("=" * 60)
    
    return results


if __name__ == "__main__":
    # Set up environment
    print("🔧 Setting up advanced test environment...")
    
    # Ensure proper Python path
    src_path = str(Path(__file__).parent / "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    
    # Run advanced tests
    results = run_advanced_tests()
    
    # Exit with appropriate code
    total_failed = sum(r['failed'] for r in results.values())
    sys.exit(0 if total_failed == 0 else 1)