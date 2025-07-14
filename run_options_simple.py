#!/usr/bin/env python3
"""
Simple Options Trading Tracker Launcher
=======================================

Run this script to launch the Options Trading Tracker.
Usage: python run_options_simple.py
"""

import sys
import os

# Add the src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Import and run the options tracker
try:
    from portfolio_suite.options_trading.ui import render_options_tracker

    render_options_tracker()
except ImportError as e:
    print(f"Error: {e}")
    print(
        "Make sure you're in the PortfolioSuite directory and virtual environment is activated."
    )
    print("Try: source .venv/bin/activate && python run_options_simple.py")
