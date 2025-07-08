"""
🛠️ Utilities Module
===================

Common utilities and helper functions for the Portfolio Management Suite.

This module provides shared utilities, configuration management,
and common helper functions used across all modules.

Main Components:
- Configuration management
- Data validation utilities
- Common financial calculations
- Logging and error handling utilities

Usage:
    from portfolio_suite.utils import validate_symbol, format_currency
"""

import re
from typing import Any, Dict, List, Optional


def validate_symbol(symbol: str) -> bool:
    """
    Validate if a string is a valid stock ticker symbol
    
    Args:
        symbol: Stock ticker symbol to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not symbol or not isinstance(symbol, str):
        return False
    
    # Basic validation: 1-5 letters, possibly with dots for special shares
    pattern = r'^[A-Z]{1,5}(\.[A-Z]{1,2})?$'
    return bool(re.match(pattern, symbol.upper().strip()))


def format_currency(amount: float, include_sign: bool = True) -> str:
    """
    Format a number as currency
    
    Args:
        amount: Amount to format
        include_sign: Whether to include + sign for positive amounts
        
    Returns:
        Formatted currency string
    """
    if amount >= 0 and include_sign:
        return f"+${amount:,.2f}"
    else:
        return f"${amount:,.2f}"


def format_percentage(value: float, decimals: int = 1) -> str:
    """
    Format a decimal as percentage
    
    Args:
        value: Decimal value (e.g., 0.05 for 5%)
        decimals: Number of decimal places
        
    Returns:
        Formatted percentage string
    """
    return f"{value * 100:.{decimals}f}%"


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename for safe filesystem usage
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove extra spaces and dots
    sanitized = re.sub(r'\s+', '_', sanitized)
    sanitized = re.sub(r'\.+', '.', sanitized)
    
    # Limit length
    if len(sanitized) > 100:
        name, ext = sanitized.rsplit('.', 1) if '.' in sanitized else (sanitized, '')
        sanitized = name[:95] + ('.' + ext if ext else '')
    
    return sanitized


def validate_price(price: Any) -> Optional[float]:
    """
    Validate and convert price to float
    
    Args:
        price: Price value to validate
        
    Returns:
        Valid price as float or None if invalid
    """
    try:
        price_float = float(price)
        if price_float < 0:
            return None
        return price_float
    except (ValueError, TypeError):
        return None


def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """
    Calculate percentage change between two values
    
    Args:
        old_value: Original value
        new_value: New value
        
    Returns:
        Percentage change as decimal (e.g., 0.05 for 5% increase)
    """
    if old_value == 0:
        return 0.0
    
    return (new_value - old_value) / old_value


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divide two numbers, returning default if division by zero
    
    Args:
        numerator: Numerator
        denominator: Denominator  
        default: Default value if division by zero
        
    Returns:
        Division result or default value
    """
    if denominator == 0:
        return default
    
    return numerator / denominator


def get_config_defaults() -> Dict[str, Any]:
    """
    Get default configuration values for the application
    
    Returns:
        Dictionary of default configuration values
    """
    return {
        'data_refresh_interval': 300,  # 5 minutes
        'max_symbols_per_request': 10,
        'default_risk_tolerance': 'moderate',
        'cache_timeout': 3600,  # 1 hour
        'max_trade_history': 1000,
        'default_watchlist': ['SPY', 'QQQ', 'AAPL', 'MSFT'],
        'volatility_threshold': 0.25,
        'confidence_threshold': 0.6,
        'enable_notifications': True,
        'theme': 'light'
    }


__all__ = [
    'validate_symbol',
    'format_currency', 
    'format_percentage',
    'sanitize_filename',
    'validate_price',
    'calculate_percentage_change',
    'safe_divide',
    'get_config_defaults'
]

__version__ = '1.0.0'
