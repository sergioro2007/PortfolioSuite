"""
📊 Trade Repository Module
=========================

This module provides comprehensive trade management functionality including:
- Trade data storage and management
- Trade analysis and reporting
- Memory-based trade tracking
- Performance analytics

Modules:
- core: Core trade management functionality
- memory: Trade memory and historical data management
- reporting: Trade analysis reporting
- templates: Templates for trade analysis
"""

from .core import TradeRepository, TradeManager
from .memory import TradeMemory
from .reporting import TradeReporter

__all__ = [
    'TradeRepository',
    'TradeManager', 
    'TradeMemory',
    'TradeReporter'
]

__version__ = "1.0.0"