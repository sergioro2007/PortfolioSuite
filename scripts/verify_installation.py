#!/usr/bin/env python3
"""
End-to-end verification script for Portfolio Management Suite.

This script performs comprehensive checks that cover all troubleshooting
scenarios encountered during setup to ensure the application works properly.
"""

import subprocess
import sys
import time
import requests
from pathlib import Path


def run_check(description, check_func):
    """Run a check function and report results."""
    try:
        result = check_func()
        if result:
            print(f"✅ {description}")
            return True
        else:
            print(f"❌ {description}")
            return False
    except Exception as e:
        print(f"❌ {description}: {e}")
        return False


def check_python_executable():
    """Check Python executable is working."""
    result = subprocess.run([sys.executable, "--version"], 
                          capture_output=True, text=True)
    return result.returncode == 0 and "Python" in result.stdout


def check_package_importable():
    """Check that portfolio_suite can be imported."""
    try:
        result = subprocess.run([
            sys.executable, "-c", 
            "import portfolio_suite; print('Import successful')"
        ], capture_output=True, text=True, timeout=10)
        return result.returncode == 0 and "Import successful" in result.stdout
    except subprocess.TimeoutExpired:
        return False


def check_core_modules():
    """Check that core modules can be imported."""
    test_code = """
import portfolio_suite
from portfolio_suite.options_trading.core import OptionsTracker
from portfolio_suite.tactical_tracker.core import PortfolioTracker  
from portfolio_suite.trade_analysis.core import TradeAnalyzer
print('All core modules imported')
"""
    try:
        result = subprocess.run([
            sys.executable, "-c", test_code
        ], capture_output=True, text=True, timeout=10)
        return result.returncode == 0 and "All core modules imported" in result.stdout
    except subprocess.TimeoutExpired:
        return False


def check_dependencies():
    """Check critical dependencies are available."""
    deps = ["streamlit", "pandas", "numpy", "yfinance", "plotly"]
    for dep in deps:
        try:
            result = subprocess.run([
                sys.executable, "-c", f"import {dep}"
            ], capture_output=True, text=True, timeout=5)
            if result.returncode != 0:
                return False
        except subprocess.TimeoutExpired:
            return False
    return True


def check_module_execution():
    """Check that module can be executed via python -m."""
    try:
        result = subprocess.run([
            sys.executable, "-m", "portfolio_suite", "--help"
        ], capture_output=True, text=True, timeout=10)
        return result.returncode in [0, 2]  # Help might exit with 2
    except subprocess.TimeoutExpired:
        return False


def check_streamlit_startup():
    """Check that Streamlit server can start and respond."""
    process = None
    try:
        # Start server in background
        process = subprocess.Popen([
            sys.executable, "-m", "portfolio_suite", "--component", "web"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for startup
        print("  Starting Streamlit server...")
        time.sleep(15)
        
        # Check if responding
        response = requests.get("http://localhost:8501", timeout=10)
        return response.status_code == 200
        
    except Exception:
        return False
    finally:
        if process:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()


def check_project_structure():
    """Check project structure is correct."""
    project_root = Path(__file__).parent.parent
    
    required_paths = [
        "src/portfolio_suite",
        "src/portfolio_suite/__init__.py",
        "src/portfolio_suite/__main__.py",
        "src/portfolio_suite/options_trading",
        "src/portfolio_suite/tactical_tracker",
        "src/portfolio_suite/trade_analysis",
        "pyproject.toml",
        "requirements.txt"
    ]
    
    for path in required_paths:
        if not (project_root / path).exists():
            return False
    return True


def check_pyproject_config():
    """Check pyproject.toml has correct src layout configuration."""
    project_root = Path(__file__).parent.parent
    pyproject_file = project_root / "pyproject.toml"
    
    if not pyproject_file.exists():
        return False
        
    content = pyproject_file.read_text()
    return ('package-dir = {"" = "src"}' in content and 
            'packages = ["portfolio_suite"]' in content)


def check_basic_functionality():
    """Check basic functionality works without external data."""
    test_code = """
from portfolio_suite.options_trading.core import OptionsTracker
from portfolio_suite.tactical_tracker.core import PortfolioTracker

# Test object creation
options_tracker = OptionsTracker()
portfolio_tracker = PortfolioTracker()

# Test basic attributes exist
assert hasattr(options_tracker, 'watchlist')
assert hasattr(portfolio_tracker, 'portfolio')
print('Basic functionality verified')
"""
    try:
        result = subprocess.run([
            sys.executable, "-c", test_code
        ], capture_output=True, text=True, timeout=10)
        return result.returncode == 0 and "Basic functionality verified" in result.stdout
    except subprocess.TimeoutExpired:
        return False


def main():
    """Run all end-to-end verification checks."""
    print("🔍 Portfolio Management Suite - End-to-End Verification")
    print("=" * 60)
    
    checks = [
        ("Python executable working", check_python_executable),
        ("Project structure correct", check_project_structure), 
        ("pyproject.toml configured for src layout", check_pyproject_config),
        ("Package importable", check_package_importable),
        ("Core modules importable", check_core_modules),
        ("Critical dependencies available", check_dependencies),
        ("Module execution via python -m", check_module_execution),
        ("Basic functionality working", check_basic_functionality),
        ("Streamlit server startup and response", check_streamlit_startup),
    ]
    
    passed = 0
    total = len(checks)
    
    for description, check_func in checks:
        if run_check(description, check_func):
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 VERIFICATION SUMMARY: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 ALL CHECKS PASSED - Portfolio Suite is ready to use!")
        print("\n🚀 To start the application:")
        print("   python3.13 -m portfolio_suite --component web")
        print("   Then open: http://localhost:8501")
        return 0
    else:
        print(f"⚠️  {total - passed} checks failed - see errors above")
        return 1


if __name__ == "__main__":
    sys.exit(main())
