"""
📈 Trade Analysis Module
=======================

Comprehensive trade analysis and strategy generation tools for the Portfolio Management Suite.

This module provides:
- Symbol analysis and technical indicators
- Trade suggestion generation
- Performance tracking and reporting
- CLI and UI interfaces for trade analysis

Main Components:
- core.py: Core analysis algorithms and TradeAnalyzer class
- ui.py: Streamlit-based user interface
- cli.py: Command-line interface

Usage:
    # Programmatic usage
    from portfolio_suite.trade_analysis import TradeAnalyzer
    analyzer = TradeAnalyzer()
    analysis = analyzer.analyze_symbol('AAPL')
    
    # UI usage
    from portfolio_suite.trade_analysis.ui import run_analysis_ui
    run_analysis_ui()
    
    # CLI usage
    python -m portfolio_suite.trade_analysis.cli analyze AAPL
"""

from .core import TradeAnalyzer, run_trade_analysis
from .ui import run_analysis_ui

# Create alias for launch function
launch_analysis_ui = run_analysis_ui

__all__ = [
    'TradeAnalyzer',
    'run_trade_analysis', 
    'run_analysis_ui',
    'launch_analysis_ui'
]

__version__ = '1.0.0'
