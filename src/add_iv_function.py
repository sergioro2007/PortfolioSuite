import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from _get_implied_volatility import _get_implied_volatility

# Add the function to OptionsTracker
import types
from src.options_tracker import OptionsTracker

# Add the method to the class instance
OptionsTracker._get_implied_volatility = _get_implied_volatility

print("Successfully added implied volatility function to OptionsTracker class")
