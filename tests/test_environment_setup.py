"""
End-to-end environment setup and installation tests.

This module tests all the critical infrastructure components that were
identified during troubleshooting to ensure the application can run properly.
"""

import os
import sys
import subprocess
import importlib
import tempfile
import time
import requests
from pathlib import Path
import pytest


class TestEnvironmentSetup:
    """Test suite for environment setup and installation verification."""

    def test_python_executable_exists(self):
        """Verify Python executable is accessible and working."""
        result = subprocess.run([sys.executable, "--version"], 
                              capture_output=True, text=True)
        assert result.returncode == 0
        assert "Python" in result.stdout
        print(f"✅ Python executable: {sys.executable}")

    def test_virtual_environment_active(self):
        """Verify we're running in a virtual environment."""
        # Check if we're in a venv by looking for specific paths
        in_venv = (
            hasattr(sys, 'real_prefix') or 
            (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) or
            'site-packages' in sys.path[0] if sys.path else False
        )
        assert in_venv, "Tests should run in virtual environment"
        print(f"✅ Virtual environment active: {sys.prefix}")

    def test_package_installation(self):
        """Test that our package is properly installed and importable."""
        try:
            import portfolio_suite
            print("✅ portfolio_suite package imported successfully")
            
            # Test core modules
            from portfolio_suite.options_trading import core as options_core
            from portfolio_suite.tactical_tracker import core as tactical_core
            from portfolio_suite.trade_analysis import core as analysis_core
            print("✅ All core modules imported successfully")
            
        except ImportError as e:
            pytest.fail(f"Package import failed: {e}")

    def test_critical_dependencies(self):
        """Test that all critical dependencies are available."""
        critical_deps = [
            'streamlit',
            'pandas', 
            'numpy',
            'yfinance',
            'plotly',
            'requests'
        ]
        
        for dep in critical_deps:
            try:
                importlib.import_module(dep)
                print(f"✅ {dep} imported successfully")
            except ImportError:
                pytest.fail(f"Critical dependency {dep} not available")

    def test_src_layout_structure(self):
        """Verify the src layout is correctly structured."""
        project_root = Path(__file__).parent.parent
        src_dir = project_root / "src" / "portfolio_suite"
        
        assert src_dir.exists(), "src/portfolio_suite directory should exist"
        assert (src_dir / "__init__.py").exists(), "__init__.py should exist"
        assert (src_dir / "__main__.py").exists(), "__main__.py should exist"
        
        # Check core modules
        core_modules = [
            "options_trading",
            "tactical_tracker", 
            "trade_analysis",
            "ui",
            "utils"
        ]
        
        for module in core_modules:
            module_dir = src_dir / module
            assert module_dir.exists(), f"{module} directory should exist"
            print(f"✅ {module} module structure verified")

    def test_pyproject_toml_configuration(self):
        """Test that pyproject.toml is correctly configured for src layout."""
        project_root = Path(__file__).parent.parent
        pyproject_file = project_root / "pyproject.toml"
        
        assert pyproject_file.exists(), "pyproject.toml should exist"
        
        content = pyproject_file.read_text()
        assert 'package-dir = {"" = "src"}' in content, "Should have src layout config"
        assert 'packages = ["portfolio_suite"]' in content, "Should specify portfolio_suite package"
        print("✅ pyproject.toml correctly configured for src layout")

    def test_module_main_execution(self):
        """Test that the module can be executed via python -m."""
        try:
            # Test help command (should not start server)
            result = subprocess.run([
                sys.executable, "-m", "portfolio_suite", "--help"
            ], capture_output=True, text=True, timeout=10)
            
            # Should exit with 0 or show help (depends on implementation)
            assert result.returncode in [0, 2], f"Module execution failed: {result.stderr}"
            print("✅ Module can be executed via python -m")
            
        except subprocess.TimeoutExpired:
            pytest.fail("Module execution timed out - might be hanging")

    def test_streamlit_integration(self):
        """Test that Streamlit can find and import our modules."""
        try:
            import streamlit as st
            
            # Test that we can import our UI modules
            from portfolio_suite.options_trading.ui import render_options_tracker
            from portfolio_suite.ui.main_app import main
            
            print("✅ Streamlit integration working")
            
        except ImportError as e:
            pytest.fail(f"Streamlit integration failed: {e}")


class TestApplicationStartup:
    """Test application startup and basic functionality."""

    def test_options_tracker_initialization(self):
        """Test that OptionsTracker can be initialized without errors."""
        from portfolio_suite.options_trading.core import OptionsTracker
        
        try:
            tracker = OptionsTracker()
            assert tracker is not None
            print("✅ OptionsTracker initialized successfully")
            
        except Exception as e:
            pytest.fail(f"OptionsTracker initialization failed: {e}")

    def test_portfolio_tracker_initialization(self):
        """Test that PortfolioTracker can be initialized without errors."""
        from portfolio_suite.tactical_tracker.core import PortfolioTracker
        
        try:
            tracker = PortfolioTracker()
            assert tracker is not None
            print("✅ PortfolioTracker initialized successfully")
            
        except Exception as e:
            pytest.fail(f"PortfolioTracker initialization failed: {e}")

    def test_trade_analyzer_initialization(self):
        """Test that TradeAnalyzer can be initialized without errors."""
        from portfolio_suite.trade_analysis.core import TradeAnalyzer
        
        try:
            analyzer = TradeAnalyzer()
            assert analyzer is not None
            print("✅ TradeAnalyzer initialized successfully")
            
        except Exception as e:
            pytest.fail(f"TradeAnalyzer initialization failed: {e}")

    @pytest.mark.slow
    @pytest.mark.integration
    def test_streamlit_server_startup(self):
        """Test that Streamlit server can start (integration test)."""
        import threading
        import time
        
        # Start Streamlit in background
        process = subprocess.Popen([
            sys.executable, "-m", "portfolio_suite", "--component", "web"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        try:
            # Wait for server to start
            time.sleep(10)
            
            # Check if server is responding
            try:
                response = requests.get("http://localhost:8501", timeout=5)
                assert response.status_code == 200
                print("✅ Streamlit server started and responding")
                
            except requests.exceptions.RequestException:
                pytest.fail("Streamlit server not responding")
                
        finally:
            # Clean up - terminate the process
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()


class TestDataAndConfiguration:
    """Test data files and configuration setup."""

    def test_data_directory_exists(self):
        """Test that data directory and required files exist."""
        project_root = Path(__file__).parent.parent
        data_dir = project_root / "data"
        
        assert data_dir.exists(), "data directory should exist"
        
        # Check for required data files
        required_files = [
            "options_trades.pkl",
            "portfolio_results.pkl"
        ]
        
        for file_name in required_files:
            file_path = data_dir / file_name
            if file_path.exists():
                print(f"✅ {file_name} exists")
            else:
                print(f"⚠️  {file_name} missing - will be created on first run")

    def test_vscode_configuration(self):
        """Test VS Code configuration is properly set up."""
        project_root = Path(__file__).parent.parent
        vscode_dir = project_root / ".vscode"
        settings_file = vscode_dir / "settings.json"
        
        if settings_file.exists():
            import json
            settings = json.loads(settings_file.read_text())
            
            # Check critical settings
            assert "python.defaultInterpreterPath" in settings
            assert "streamlit.pythonPath" in settings
            print("✅ VS Code settings configured correctly")
        else:
            print("⚠️  No VS Code settings found")

    def test_requirements_file(self):
        """Test that requirements.txt exists and contains critical packages."""
        project_root = Path(__file__).parent.parent
        req_file = project_root / "requirements.txt"
        
        assert req_file.exists(), "requirements.txt should exist"
        
        content = req_file.read_text()
        critical_packages = ["streamlit", "pandas", "numpy", "yfinance"]
        
        for package in critical_packages:
            assert package in content, f"{package} should be in requirements.txt"
            
        print("✅ requirements.txt contains all critical packages")


class TestEndToEndWorkflow:
    """End-to-end workflow tests that simulate real usage."""

    def test_import_all_modules_workflow(self):
        """Test importing all modules in typical usage order."""
        # Simulate typical import workflow
        modules_to_test = [
            "portfolio_suite",
            "portfolio_suite.options_trading.core",
            "portfolio_suite.options_trading.ui", 
            "portfolio_suite.tactical_tracker.core",
            "portfolio_suite.trade_analysis.core",
            "portfolio_suite.ui.main_app"
        ]
        
        for module_name in modules_to_test:
            try:
                importlib.import_module(module_name)
                print(f"✅ {module_name} imported successfully")
            except ImportError as e:
                pytest.fail(f"Failed to import {module_name}: {e}")

    def test_basic_functionality_workflow(self):
        """Test basic functionality workflow without external dependencies."""
        from portfolio_suite.options_trading.core import OptionsTracker
        from portfolio_suite.tactical_tracker.core import PortfolioTracker
        
        # Test basic object creation and method calls
        options_tracker = OptionsTracker()
        portfolio_tracker = PortfolioTracker()
        
        # Test that objects have expected attributes/methods
        assert hasattr(options_tracker, 'watchlist')
        assert hasattr(portfolio_tracker, 'portfolio')
        
        print("✅ Basic functionality workflow completed")

    def test_installation_verification_complete(self):
        """Comprehensive verification that installation is complete and working."""
        checks = []
        
        # Check 1: Package importable
        try:
            import portfolio_suite
            checks.append("✅ Package import")
        except ImportError:
            checks.append("❌ Package import")
            
        # Check 2: Core modules accessible  
        try:
            from portfolio_suite.options_trading.core import OptionsTracker
            OptionsTracker()
            checks.append("✅ Core functionality")
        except Exception:
            checks.append("❌ Core functionality")
            
        # Check 3: Dependencies available
        try:
            import streamlit, pandas, numpy, yfinance
            checks.append("✅ Dependencies")
        except ImportError:
            checks.append("❌ Dependencies")
            
        # Check 4: Module execution possible
        try:
            result = subprocess.run([
                sys.executable, "-c", "import portfolio_suite; print('OK')"
            ], capture_output=True, text=True, timeout=5)
            if result.returncode == 0 and "OK" in result.stdout:
                checks.append("✅ Module execution")
            else:
                checks.append("❌ Module execution")
        except Exception:
            checks.append("❌ Module execution")
            
        print("\n=== INSTALLATION VERIFICATION SUMMARY ===")
        for check in checks:
            print(check)
            
        # All checks must pass
        failed_checks = [check for check in checks if "❌" in check]
        assert len(failed_checks) == 0, f"Failed checks: {failed_checks}"
        
        print("✅ ALL INSTALLATION VERIFICATION CHECKS PASSED")


if __name__ == "__main__":
    # Allow running this test file directly for quick verification
    pytest.main([__file__, "-v"])
