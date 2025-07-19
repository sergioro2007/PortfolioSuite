"""
📈 Trade Analysis Module - Enhanced
===================================

Comprehensive trade analysis toolkit with enhanced trading capabilities.
Provides both traditional analysis tools and advanced trade management.

Main Components:
- TradeAnalyzer: Core analysis engine (legacy compatibility)
- TradeRepository: New trade data management
- TradeManager: Enhanced trade execution and management
- TradeMemory: Historical trade data and memory management
- TradeReporter: Advanced reporting and analytics

Integration with new trade module provides:
- Persistent trade storage
- Advanced portfolio tracking
- Comprehensive reporting
- Historical analysis
"""

# Legacy imports for compatibility
from .core import TradeAnalyzer, run_trade_analysis
from .ui import run_analysis_ui

# Create alias for launch function
launch_analysis_ui = run_analysis_ui

# New enhanced trade functionality
try:
    from ..trade import TradeRepository, TradeManager, TradeMemory, TradeReporter
    ENHANCED_FEATURES_AVAILABLE = True
except ImportError:
    ENHANCED_FEATURES_AVAILABLE = False
    TradeRepository = None
    TradeManager = None
    TradeMemory = None
    TradeReporter = None

__all__ = [
    # Legacy components
    'TradeAnalyzer',
    'run_trade_analysis', 
    'run_analysis_ui',
    'launch_analysis_ui',
    
    # Enhanced components (if available)
    'TradeRepository',
    'TradeManager', 
    'TradeMemory',
    'TradeReporter',
    'ENHANCED_FEATURES_AVAILABLE'
]

__version__ = '2.0.0'
