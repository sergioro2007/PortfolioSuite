#!/usr/bin/env python3
"""
Portfolio Management Suite - Main Entry Point
============================================

Launch the comprehensive portfolio management application.
"""

import sys
import os
import argparse

def main():
    """Main entry point for the Portfolio Management Suite"""
    parser = argparse.ArgumentParser(
        description="Portfolio Management Suite - Comprehensive Investment Analysis Platform"
    )
    parser.add_argument(
        "--component", 
        choices=["gui", "web", "options", "tactical", "analysis"],
        default="gui",
        help="Launch specific component (default: gui for desktop app)"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=8501,
        help="Port for web interface (default: 8501)"
    )
    parser.add_argument(
        "--host", 
        default="localhost",
        help="Host for web interface (default: localhost)"
    )
    parser.add_argument(
        "--debug", 
        action="store_true",
        help="Enable debug mode"
    )
    
    args = parser.parse_args()
    
    if args.component == "gui":
        # Launch desktop GUI application
        from .gui.launcher import launch_gui
        launch_gui()
    elif args.component == "web":
        # Launch web interface
        from .ui.main_app import launch_web
        launch_web(host=args.host, port=args.port, debug=args.debug)
    elif args.component == "options":
        # Launch options tracker only  
        from .options_trading import run_options_ui
        import streamlit.web.cli as stcli
        import sys
        sys.argv = ["streamlit", "run", "--server.address", args.host, "--server.port", str(args.port)]
        run_options_ui()
    elif args.component == "tactical":
        # Launch tactical tracker only
        from .tactical_tracker import run_tactical_tracker
        import streamlit.web.cli as stcli
        import sys
        sys.argv = ["streamlit", "run", "--server.address", args.host, "--server.port", str(args.port)]
        run_tactical_tracker()
    elif args.component == "analysis":
        # Launch trade analysis tools
        from .trade_analysis.ui import launch_analysis_ui
        launch_analysis_ui()

if __name__ == "__main__":
    main()
