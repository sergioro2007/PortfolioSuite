#!/usr/bin/env python3
"""
Options Trading Tracker - Direct Launch
======================================

Direct launcher for the Options Trading interface without module complications.
"""

import streamlit as st
import sys
import os

# Configure Streamlit page first
st.set_page_config(page_title="Options Trading Tracker", page_icon="🎯", layout="wide")

# Add paths for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "src")
options_dir = os.path.join(src_dir, "portfolio_suite", "options_trading")

for path in [src_dir, options_dir]:
    if path not in sys.path:
        sys.path.insert(0, path)


def main():
    """Main entry point for direct options tracker"""
    try:
        # Try multiple import paths
        try:
            from portfolio_suite.options_trading.ui import render_options_tracker
        except ImportError:
            sys.path.insert(
                0,
                os.path.join(current_dir, "src", "portfolio_suite", "options_trading"),
            )
            from ui import render_options_tracker

        # Render the application
        render_options_tracker()

    except ImportError as e:
        st.error(f"❌ Import Error: {e}")
        st.info("**Troubleshooting:**")
        st.write("1. Make sure you're in the PortfolioSuite directory")
        st.write("2. Activate the virtual environment: `source .venv/bin/activate`")
        st.write("3. Install dependencies: `pip install -r requirements.txt`")

        st.write("**Current Python path:**")
        for i, path in enumerate(sys.path[:10]):  # Show first 10 paths
            st.write(f"{i+1}. {path}")

    except Exception as e:
        st.error(f"❌ Unexpected Error: {e}")
        st.info("Please check the logs for more details.")


if __name__ == "__main__":
    main()
