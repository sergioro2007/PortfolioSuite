"""
⚡ Tactical Tracker Module
=========================

Tactical momentum portfolio tracking and analysis tools for the Portfolio Management Suite.

This module provides tactical momentum analysis, market health monitoring,
and defensive cash allocation features.

Main Components:
- core.py: Core tactical tracking algorithms and PortfolioTracker class

Usage:
    # Programmatic usage
    from portfolio_suite.tactical_tracker import run_tactical_tracker
    
    # From main app
    run_tactical_tracker()
"""

# Import the main function from core
try:
    from .core import run_tactical_tracker
    __all__ = ['run_tactical_tracker']
except ImportError:
    # Fallback if core module not properly configured
    def run_tactical_tracker():
        """Placeholder function until core module is properly configured"""
        import streamlit as st
        st.error("Tactical Tracker module not properly configured. Please check the installation.")
    
    __all__ = ['run_tactical_tracker']

__version__ = '1.0.0'
