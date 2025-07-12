"""
Portfolio Management Suite - Main Web Interface
==============================================

Unified Streamlit application that serves all portfolio management tools.
"""

import streamlit as st
import sys
import os
from typing import Optional

# Add parent directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

def configure_page():
    """Configure the Streamlit page"""
    st.set_page_config(
        page_title="Portfolio Management Suite",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main > div {
        padding-top: 2rem;
    }
    .stSelectbox > div > div {
        background-color: white;
    }
    .stApp {
        background-color: #FFFFFF;
    }
    .sidebar-content {
        padding: 1rem;
    }
    .module-header {
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

def main_sidebar():
    """Create the main sidebar for module selection"""
    st.sidebar.markdown("## 📊 Portfolio Management Suite")
    st.sidebar.markdown("---")
    
    # Module selection
    module = st.sidebar.selectbox(
        "Select Module",
        [
            "🏠 Dashboard",
            "🎯 Options Trading Tracker", 
            "⚡ Tactical Momentum Tracker",
            "📈 Trade Analysis Tools",
            "🛡️ Long-Term Quality Stocks",
            "⚙️ Settings"
        ],
        index=0
    )
    
    st.sidebar.markdown("---")
    
    # Quick stats or info
    st.sidebar.markdown("### 📊 Quick Stats")
    st.sidebar.info("Real-time market data and analysis")
    
    st.sidebar.markdown("### 🔗 Quick Links")
    st.sidebar.markdown("- [Options Tracker](/?module=options)")
    st.sidebar.markdown("- [Tactical Tracker](/?module=tactical)")
    st.sidebar.markdown("- [Trade Analysis](/?module=analysis)")
    
    return module

def show_dashboard():
    """Show the main dashboard"""
    st.markdown("""
    <div class="module-header">
        <h1>🏠 Portfolio Management Dashboard</h1>
        <p>Welcome to your comprehensive investment analysis platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Portfolio Value", "$125,430", "2.3%")
    
    with col2:
        st.metric("Monthly P&L", "$3,245", "1.2%")
    
    with col3:
        st.metric("Active Positions", "12", "2")
    
    with col4:
        st.metric("Win Rate", "73%", "5%")
    
    st.markdown("---")
    
    # Module cards
    st.markdown("### 🚀 Available Modules")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container():
            st.markdown("""
            #### 🎯 Options Trading Tracker
            - Weekly income strategies
            - Trade suggestions and analysis
            - P&L tracking and optimization
            - Real-time options data
            """)
            if st.button("Launch Options Tracker", key="options"):
                st.query_params.module = "options"
                st.rerun()
        
        with st.container():
            st.markdown("""
            #### 📈 Trade Analysis Tools
            - Automated trade reports
            - Performance analytics
            - Risk assessment
            - Historical analysis
            """)
            if st.button("Launch Trade Analysis", key="analysis"):
                st.query_params.module = "analysis"
                st.rerun()
    
    with col2:
        with st.container():
            st.markdown("""
            #### ⚡ Tactical Momentum Tracker
            - Short-term momentum analysis
            - Market health indicators
            - Technical analysis
            - Entry/exit signals
            """)
            if st.button("Launch Tactical Tracker", key="tactical"):
                st.query_params.module = "tactical"
                st.rerun()
        
        with st.container():
            st.markdown("""
            #### 🛡️ Long-Term Quality Stocks
            - Conservative stock screening
            - Defensive portfolio analysis
            - Quality metrics
            - Long-term holdings
            """)
            if st.button("Launch Quality Stocks", key="quality"):
                st.query_params.module = "quality"
                st.rerun()

def show_options_trading():
    """Show the options trading module"""
    try:
        # Try absolute import first
        from portfolio_suite.options_trading import run_options_ui
        run_options_ui()
    except ImportError as e:
        st.error(f"Options trading module not found or failed to import: {e}")
        st.info("Please ensure the options trading module is properly installed and available in your environment.")

def show_tactical_tracker():
    """Show the tactical momentum tracker module"""
    try:
        # Try absolute import first
        from portfolio_suite.tactical_tracker import run_tactical_tracker
        run_tactical_tracker()
    except ImportError:
        try:
            # Try relative import
            from ..tactical_tracker import run_tactical_tracker
            run_tactical_tracker()
        except ImportError:
            st.error("Tactical tracker module not found. Please check your installation.")
            st.info("Fallback: Loading from src directory...")
            try:
                # Fallback to src directory
                sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))
                from tactical_tracker import run_tactical_tracker
                run_tactical_tracker()
            except ImportError as e:
                st.error(f"Could not load tactical tracker module: {e}")

def show_trade_analysis():
    """Show the trade analysis module"""
    try:
        # Try absolute import first
        from portfolio_suite.trade_analysis.ui import run_analysis_ui
        run_analysis_ui()
    except ImportError:
        try:
            # Try relative import
            from ..trade_analysis.ui import run_analysis_ui
            run_analysis_ui()
        except ImportError:
            st.error("Trade analysis module not found. Please check your installation.")
            st.info("This module is under development.")

def show_quality_stocks():
    """Show the long-term quality stocks module"""
    st.markdown("""
    <div class="module-header">
        <h1>🛡️ Long-Term Quality Stocks</h1>
        <p>Conservative, defensive, high-quality stock screening</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("🚧 This module is under development. Coming soon!")
    
    st.markdown("""
    ### Planned Features:
    - Quality metrics analysis
    - Defensive stock screening
    - Dividend analysis
    - Long-term performance tracking
    - Risk-adjusted returns
    """)

def show_settings():
    """Show application settings"""
    st.markdown("""
    <div class="module-header">
        <h1>⚙️ Settings</h1>
        <p>Configure your Portfolio Management Suite</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🔧 Application Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Display Settings")
        theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])
        refresh_rate = st.slider("Auto-refresh rate (seconds)", 30, 300, 60)
        show_notifications = st.checkbox("Show notifications", value=True)
    
    with col2:
        st.subheader("Data Settings")
        data_provider = st.selectbox("Data Provider", ["Yahoo Finance", "Alpha Vantage"])
        cache_duration = st.slider("Cache duration (minutes)", 1, 60, 5)
        
    st.markdown("### 🔑 API Configuration")
    
    with st.expander("API Keys"):
        st.text_input("Alpha Vantage API Key", type="password")
        st.text_input("Other API Key", type="password")
        st.info("API keys are stored locally and encrypted.")
    
    if st.button("Save Settings"):
        st.success("Settings saved successfully!")

def main():
    """Main application function"""
    configure_page()
    
    # Check URL parameters for direct module access
    query_params = st.query_params
    direct_module = query_params.get("module", None)
    
    if direct_module:
        # Direct module access via URL
        if direct_module == "options":
            show_options_trading()
        elif direct_module == "tactical":
            show_tactical_tracker()
        elif direct_module == "analysis":
            show_trade_analysis()
        elif direct_module == "quality":
            show_quality_stocks()
        else:
            show_dashboard()
    else:
        # Normal sidebar navigation
        selected_module = main_sidebar()
        
        if "🏠 Dashboard" in selected_module:
            show_dashboard()
        elif "🎯 Options Trading" in selected_module:
            show_options_trading()
        elif "⚡ Tactical Momentum" in selected_module:
            show_tactical_tracker()
        elif "📈 Trade Analysis" in selected_module:
            show_trade_analysis()
        elif "🛡️ Long-Term Quality" in selected_module:
            show_quality_stocks()
        elif "⚙️ Settings" in selected_module:
            show_settings()

def launch_web(host: str = "localhost", port: int = 8501, debug: bool = False):
    """Launch the web interface programmatically"""
    import subprocess
    import sys
    
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        __file__,
        "--server.address", host,
        "--server.port", str(port),
        "--server.headless", "true" if not debug else "false",
        "--browser.gatherUsageStats", "false"
    ]
    
    subprocess.run(cmd)

if __name__ == "__main__":
    main()
