"""
🎯 Multi-Feature Portfolio Management Suite
===========================================

A comprehensive investment analysis platform with multiple portfolio management tools:
1. Tactical Momentum Portfolio Tracker - Short-term momentum and market health analysis
2. Long-Term Quality Stocks Tracker - Conservative, defensive, high-quality stock screening

Version: 2.0.0
Last Updated: July 3, 2025
"""

import streamlit as st
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Page configuration
st.set_page_config(
    page_title="Portfolio Management Suite",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Edge browser compatibility fixes
st.markdown("""
<style>
/* Edge browser compatibility CSS */
.main > div {
    padding-top: 2rem;
}
.stSelectbox > div > div {
    background-color: white;
}
/* Ensure WebSocket connections work in Edge */
.stApp {
    background-color: #FFFFFF;
}
</style>
""", unsafe_allow_html=True)

# JavaScript for Edge compatibility
st.markdown("""
<script>
// Edge browser compatibility JavaScript
(function() {
    if (navigator.userAgent.indexOf('Edg') > -1) {
        console.log('Edge browser detected - applying compatibility fixes');
        
        // Force WebSocket polyfill for Edge if needed
        if (typeof WebSocket === 'undefined') {
            console.warn('WebSocket not available in Edge');
        }
        
        // Disable Edge's automatic zoom on inputs
        var viewport = document.querySelector('meta[name="viewport"]');
        if (viewport) {
            viewport.content = 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no';
        }
    }
})();
</script>
""", unsafe_allow_html=True)

def main():
    """Main application entry point with feature selection"""
    
    # Header
    st.title('📊 Portfolio Management Suite v2.0')
    st.markdown("*Professional-grade investment analysis and portfolio management tools*")
    
    # Feature selection in sidebar
    st.sidebar.title("🎯 Select Analysis Tool")
    st.sidebar.markdown("---")
    
    feature = st.sidebar.selectbox(
        "Choose your analysis approach:",
        [
            "🏠 Home - Feature Overview",
            "⚡ Tactical Momentum Tracker", 
            "🛡️ Long-Term Quality Stocks",
            "🎯 Options Trading Tracker"
        ],
        index=0
    )
    
    # Main content area
    if feature == "🏠 Home - Feature Overview":
        show_home_page()
    elif feature == "⚡ Tactical Momentum Tracker":
        show_tactical_tracker()
    elif feature == "🛡️ Long-Term Quality Stocks":
        show_quality_tracker()
    elif feature == "🎯 Options Trading Tracker":
        show_options_tracker()

def show_home_page():
    """Display the home page with feature overview"""
    
    st.markdown("## 🎯 Welcome to Your Portfolio Management Suite")
    st.markdown("Choose from our professional-grade investment analysis tools:")
    
    # Feature comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### ⚡ Tactical Momentum Tracker
        
        **Purpose**: Short-term tactical opportunities
        
        **Best For**:
        - Active traders and momentum investors
        - Weekly/monthly portfolio rotation
        - Market timing strategies
        - Risk-on market conditions
        
        **Key Features**:
        - 🎯 Automated momentum screening
        - 📊 Real-time market health monitoring  
        - 🛡️ Intelligent defensive cash allocation
        - ⚡ Weekly return targets (0.5-3%)
        - 📈 Technical analysis integration
        - 🔄 Portfolio of up to 25 positions
        
        **Investment Horizon**: 1-12 weeks
        **Risk Level**: Moderate to High
        **Turnover**: High (weekly rotation)
        """)
    
    with col2:
        st.markdown("""
        ### 🛡️ Long-Term Quality Stocks
        
        **Purpose**: Conservative anchor portfolio
        
        **Best For**:
        - Long-term investors
        - Conservative portfolios
        - Dividend income focus
        - Risk-off market conditions
        
        **Key Features**:
        - 🛡️ Defensive sector focus
        - 💰 Dividend aristocrats emphasis
        - 📊 Fundamental quality screening
        - 📈 5-year performance validation
        - 🔒 Low volatility (beta ≤ 1.2)
        - 🎯 Portfolio of 10-15 quality stocks
        
        **Investment Horizon**: 3-10 years
        **Risk Level**: Low to Moderate  
        **Turnover**: Very Low (quarterly review)
        """)
    
    # Third column for options tracker
    st.markdown("---")
    st.markdown("### 🎯 Options Trading Tracker")
    st.markdown("""
    **Purpose**: Weekly income generation through options strategies
    
    **Best For**:
    - Options traders seeking consistent income
    - Weekly $500+ income targets
    - Systematic strategy execution
    - Risk-managed options trading
    
    **Key Features**:
    - 🎯 Bull Put & Bear Call Spreads
    - 🦋 Broken Wing Butterflies & Iron Condors
    - 📊 1-week price predictions with technical indicators
    - 💰 Trade P&L tracking and analysis
    - 🔍 Automated trade evaluation (Hold/Close/Adjust)
    - 📈 Strategy performance analytics
    
    **Target**: $500/week income
    **Risk Level**: Moderate (defined-risk strategies)
    **Time Commitment**: Weekly management
    """)
    
    # Usage guidance
    st.markdown("---")
    st.markdown("## 🎯 How to Use This Suite")
    
    st.markdown("""
    ### 🔄 Complementary Strategies
    These tools are designed to work together:
    
    - **🛡️ Core Holdings (50-70%)**: Use Long-Term Quality Stocks for your portfolio foundation
    - **⚡ Tactical Allocation (20-30%)**: Use Momentum Tracker for opportunistic positions  
    - **🎯 Income Generation (10-20%)**: Use Options Tracker for weekly income
    - **📊 Market Conditions**: Switch emphasis based on market regime
    
    ### 📈 Market Regime Guidance
    - **🟢 Bull Markets**: Emphasize Momentum + Options income strategies
    - **🔴 Bear Markets**: Emphasize Quality Stocks + Defensive options
    - **🟡 Uncertain Markets**: Balanced approach with all three tools
    """)
    
    # Getting started
    st.markdown("---")
    st.info("""
    **🚀 Getting Started:**
    1. Choose your analysis tool from the sidebar
    2. Configure your screening parameters  
    3. Run analysis and review recommendations
    4. Monitor and adjust based on market conditions
    """)

def show_tactical_tracker():
    """Load and display the tactical momentum tracker"""
    try:
        # Import the tactical tracker functionality
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from tactical_tracker import run_tactical_tracker
        run_tactical_tracker()
    except ImportError:
        st.error("""
        **Tactical Tracker Module Not Found**
        
        The tactical momentum tracker functionality needs to be imported from the existing streamlit_app.py.
        Please ensure the tactical_tracker.py module is available.
        """)
        
        if st.button("🔄 Load Legacy Tactical Tracker"):
            st.info("Redirecting to legacy tactical tracker functionality...")
            # For now, show instructions to use the original app
            st.markdown("""
            **Temporary Solution:**
            
            Please run the original tactical tracker using:
            ```bash
            streamlit run streamlit_app.py
            ```
            
            We'll integrate this functionality in the next update.
            """)

def show_quality_tracker():
    """Load and display the long-term quality stocks tracker"""
    try:
        # Import the quality tracker functionality
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from quality_tracker import run_quality_tracker
        run_quality_tracker()
    except ImportError:
        st.warning("Quality Tracker module not yet implemented. Creating new functionality...")
        
        # Placeholder for the new quality tracker
        st.markdown("## 🛡️ Long-Term Quality Stocks Tracker")
        st.markdown("*Conservative, defensive, high-quality stock screening for long-term investors*")
        
        st.info("""
        **🚧 Feature In Development**
        
        The Long-Term Quality Stocks Tracker is being implemented with the following capabilities:
        
        - **🟢 Fundamental Quality Screening**
        - **🛡️ Defensive Characteristics Analysis** 
        - **📈 Long-Term Performance Validation**
        - **📊 Weekly Tracking and Monitoring**
        
        This feature will be available in the next update.
        """)
        
        # Basic UI preview
        st.markdown("### 🎯 Screening Configuration (Preview)")
        
        col1, col2 = st.columns(2)
        with col1:
            st.slider("Minimum ROE (%)", 5, 25, 10, help="5-year average ROE threshold")
            st.slider("Maximum Beta", 0.5, 1.5, 1.2, 0.1, help="Volatility limit")
            
        with col2:
            st.slider("Minimum Dividend Yield (%)", 0.0, 8.0, 2.0, 0.5)
            st.slider("Portfolio Size", 5, 20, 10, help="Number of quality stocks")
        
        st.multiselect(
            "Preferred Defensive Sectors",
            ["Consumer Staples", "Healthcare", "Utilities", "Real Estate", "Quality Energy"],
            default=["Consumer Staples", "Healthcare"]
        )
        
        if st.button("🔄 Run Quality Analysis (Coming Soon)"):
            st.info("Quality analysis functionality will be implemented in the next version.")

def show_options_tracker():
    """Load and display the options trading tracker"""
    try:
        # Import the options tracker functionality
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from options_tracker_ui import render_options_tracker
        render_options_tracker()
    except ImportError:
        st.error("""
        **Options Tracker Module Not Found**
        
        The options trading tracker functionality requires the options_tracker module.
        Please ensure both options_tracker.py and options_tracker_ui.py are available.
        """)
        st.markdown("""
        **Manual Setup Required:**
        
        To use the Options Trading Tracker, you need to:
        1. Install required dependencies: `pip install yfinance pandas numpy`
        2. Ensure options_tracker.py and options_tracker_ui.py are in your project directory
        """)

if __name__ == "__main__":
    main()
