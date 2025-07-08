"""
Portfolio Management Suite
==========================

A comprehensive investment analysis platform with multiple portfolio management tools:

- **Tactical Momentum Portfolio Tracker**: Short-term momentum and market health analysis
- **Options Trading Tracker**: Weekly income options trading strategies
- **Trade Analysis Tools**: Automated trade analysis and reporting
- **Long-Term Quality Stocks**: Conservative, defensive, high-quality stock screening

Features:
- Real-time market data analysis
- Options trading strategy recommendations
- Portfolio performance tracking
- Technical analysis and predictions
- Risk management tools
- Automated reporting

Version: 2.0.0
"""

__version__ = "2.0.0"
__author__ = "Portfolio Manager"
__email__ = "manager@example.com"

# Import core components - use lazy imports to avoid issues
try:
    from .options_trading import OptionsTracker
except ImportError:
    OptionsTracker = None

try:
    from .trade_analysis import TradeAnalyzer
except ImportError:
    TradeAnalyzer = None

__all__ = ['OptionsTracker', 'TradeAnalyzer']
