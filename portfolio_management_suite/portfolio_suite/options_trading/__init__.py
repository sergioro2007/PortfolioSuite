"""
🎯 Options Trading Module
========================

Options trading tracking and analysis tools for the Portfolio Management Suite.

This module provides options strategy analysis, implied volatility tracking,
and options trading recommendations.

Main Components:
- core.py: Core options tracking algorithms and OptionsTracker class
- ui.py: Options trading user interface

Usage:
    # Programmatic usage
    from portfolio_suite.options_trading import OptionsTracker
    
    # UI usage
    from portfolio_suite.options_trading import run_options_ui
"""

# Import the main components from core and ui
try:
    from .core import OptionsTracker
    import sys; print("✅ OptionsTracker imported successfully from core module", file=sys.stderr)
except ImportError as e:
    import sys; print(f"Warning: Could not import OptionsTracker from core: {e}", file=sys.stderr)
    # Fallback placeholder
    class OptionsTracker:
        """Placeholder class until core module is properly configured"""
        def __init__(self):
            # Placeholder until actual implementation is loaded
            import sys; print("Warning: Using placeholder OptionsTracker. Real implementation not available.", file=sys.stderr)

try:
    from .ui import run_options_tracker_ui, run_options_ui
    import sys; print("✅ UI functions imported successfully", file=sys.stderr)
except ImportError as e:
    import sys; print(f"Warning: Could not import UI functions: {e}", file=sys.stderr)
    # Fallback functions
    def run_options_tracker_ui():
        """Placeholder function until modules are properly configured"""
        import streamlit as st
        st.error("Options Trading UI not properly configured. Please check the installation.")
    
    def run_options_ui():
        """Placeholder function until modules are properly configured"""
        return run_options_tracker_ui()

__all__ = ['OptionsTracker', 'run_options_ui', 'run_options_tracker_ui']

__version__ = '1.0.0'
