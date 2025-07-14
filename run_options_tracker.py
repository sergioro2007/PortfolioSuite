#!/usr/bin/env python3
"""
Direct launcher for Options Trading Tracker
==========================================

This script directly launches the Options Trading UI without module import complexity.
"""

import sys
import os

# Add the src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)


def main():
    """Launch the Options Trading Tracker directly"""
    try:
        from portfolio_suite.options_trading.ui import render_options_tracker
        import streamlit.web.cli as stcli

        # Set up streamlit to run this script
        sys.argv = ["streamlit", "run", __file__]

        # Call the render function
        render_options_tracker()

    except ImportError as e:
        print(f"Error importing options tracker: {e}")
        print(
            "Make sure you're in the PortfolioSuite directory and the virtual environment is activated."
        )
        sys.exit(1)


if __name__ == "__main__":
    # If running via streamlit, call the render function directly
    if "streamlit" in sys.modules:
        from portfolio_suite.options_trading.ui import render_options_tracker

        render_options_tracker()
    else:
        # If running directly, launch streamlit
        main()
