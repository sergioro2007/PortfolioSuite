#!/usr/bin/env python3
"""
Portfolio Management Suite - Main Entry Point
============================================

Launch the comprehensive portfolio management application.
"""

import sys
import os
import argparse

# Add the src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)


def main():
    """Main entry point for the Portfolio Management Suite"""
    parser = argparse.ArgumentParser(
        description="Portfolio Management Suite - Comprehensive Investment Analysis Platform"
    )
    parser.add_argument(
        "--component",
        choices=["gui", "web", "options", "tactical", "analysis"],
        default="web",  # Default to web since it's most likely to work
        help="Launch specific component (default: web for Streamlit app)",
    )
    parser.add_argument(
        "--port", type=int, default=8501, help="Port for web interface (default: 8501)"
    )
    parser.add_argument(
        "--host",
        default="localhost",
        help="Host for web interface (default: localhost)",
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    args = parser.parse_args()

    if args.component == "gui":
        # Launch desktop GUI application
        try:
            from portfolio_suite.gui.launcher import launch_gui

            launch_gui()
        except ImportError as e:
            print(f"GUI component not available: {e}")
            print("Falling back to web interface...")
            args.component = "web"

    if args.component == "web":
        # Launch web interface
        try:
            from portfolio_suite.ui.main_app import launch_web

            launch_web(host=args.host, port=args.port, debug=args.debug)
        except ImportError as e:
            print(f"Web component error: {e}")
            print("Trying direct Streamlit launch...")
            import streamlit.web.cli as stcli

            sys.argv = [
                "streamlit",
                "run",
                __file__.replace("__main__.py", "ui/main_app.py"),
                "--server.address",
                args.host,
                "--server.port",
                str(args.port),
            ]
            stcli.main()
    elif args.component == "options":
        # Launch options tracker only
        try:
            from portfolio_suite.options_trading.ui import run_options_ui

            run_options_ui()
        except ImportError as e:
            print(f"Options component error: {e}")
    elif args.component == "tactical":
        # Launch tactical tracker only
        try:
            from portfolio_suite.tactical_tracker import run_tactical_tracker

            run_tactical_tracker()
        except ImportError as e:
            print(f"Tactical component error: {e}")
    elif args.component == "analysis":
        # Launch trade analysis tools
        try:
            from portfolio_suite.trade_analysis.ui import launch_analysis_ui

            launch_analysis_ui()
        except ImportError as e:
            print(f"Analysis component error: {e}")


if __name__ == "__main__":
    main()
