"""
📈 Trade Analysis UI Module
==========================

Streamlit-based user interface for trade analysis and strategy generation.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any

try:
    from .core import TradeAnalyzer
except ImportError:
    from core import TradeAnalyzer


def run_analysis_ui():
    """Main function to run the trade analysis UI"""
    st.markdown("## 📈 Trade Analysis Tools")
    st.markdown("*Advanced tools for trade analysis and strategy generation*")
    
    st.info("Trade Analysis module is working! This is a simplified version.")
    st.write("### Available Features:")
    st.write("- Symbol Analysis")
    st.write("- Trade Suggestions")
    st.write("- Performance Tracking")


def launch_analysis_ui():
    """Launch the analysis UI - for compatibility with main launcher"""
    run_analysis_ui()


if __name__ == "__main__":
    run_analysis_ui()
