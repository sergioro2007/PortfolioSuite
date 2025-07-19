"""
🎯 Options Trading Tracker UI
============================

Streamlit interface for the Options Trading Tracker
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add the parent directories to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
src_dir = os.path.dirname(parent_dir)
for path in [current_dir, parent_dir, src_dir]:
    if path not in sys.path:
        sys.path.insert(0, path)

# Import the OptionsTracker - try multiple import strategies
OptionsTracker = None
import_error = None

# Strategy 1: Relative import (when running as module)
try:
    from .core import OptionsTracker
except ImportError as e1:
    import_error = str(e1)
    
    # Strategy 2: Direct import from same directory
    try:
        from core import OptionsTracker
    except ImportError as e2:
        
        # Strategy 3: Absolute import
        try:
            from portfolio_suite.options_trading.core import OptionsTracker
        except ImportError as e3:
            
            # Strategy 4: Force the path and import
            try:
                import sys
                core_path = os.path.join(current_dir, 'core.py')
                if os.path.exists(core_path):
                    import importlib.util
                    spec = importlib.util.spec_from_file_location("core", core_path)
                    core_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(core_module)
                    OptionsTracker = core_module.OptionsTracker
                else:
                    raise ImportError(f"Could not find core.py at {core_path}")
            except Exception as e4:
                # If all strategies fail, we'll show an error in the UI
                pass

# If import failed, show error in UI instead of crashing
def show_import_error():
    st.error("🚨 **Options Trading Module Import Error**")
    st.warning(f"Failed to import OptionsTracker: {import_error}")
    
    with st.expander("🔧 Troubleshooting Steps", expanded=True):
        st.write("**1. Check Virtual Environment:**")
        st.code("source .venv/bin/activate")
        
        st.write("**2. Install Dependencies:**")
        st.code("pip install -r requirements.txt")
        
        st.write("**3. Verify File Structure:**")
        st.write("Make sure these files exist:")
        st.write("- `src/portfolio_suite/options_trading/core.py`")
        st.write("- `src/portfolio_suite/options_trading/ui.py`")
        
        st.write("**4. Current Python Paths:**")
        for i, path in enumerate(sys.path[:8]):
            st.write(f"   {i+1}. `{path}`")
    
    st.info("💡 **Quick Fix:** Try restarting the application with:")
    st.code("cd /Users/soliv112/PersonalProjects/PortfolioSuite && source .venv/bin/activate && streamlit run options_direct.py")
    
    st.stop()  # Stop execution here

if OptionsTracker is None:
    show_import_error()

def generate_descriptive_title(suggestion: dict) -> str:
    """Generate a descriptive title for a trade suggestion"""
    ticker = suggestion['ticker']
    strategy = suggestion['strategy']
    expiration = suggestion.get('expiration', '2025-08-01')
    
    # Format expiration date to be more readable (e.g., "Aug 1st")
    try:
        exp_date = datetime.strptime(expiration, '%Y-%m-%d')
        month_name = exp_date.strftime('%b')
        day = exp_date.day
        day_suffix = 'st' if day == 1 or day == 21 or day == 31 else 'nd' if day == 2 or day == 22 else 'rd' if day == 3 or day == 23 else 'th'
        formatted_date = f"{month_name} {day}{day_suffix}"
    except:
        formatted_date = expiration
    
    # Build strike information based on strategy
    if strategy == 'Bull Put Spread':
        short_strike = suggestion.get('short_strike', 0)
        long_strike = suggestion.get('long_strike', 0)
        strikes_info = f"{long_strike:.0f}/{short_strike:.0f}"
    elif strategy == 'Bear Call Spread':
        short_strike = suggestion.get('short_strike', 0)
        long_strike = suggestion.get('long_strike', 0)
        strikes_info = f"{short_strike:.0f}/{long_strike:.0f}"
    elif strategy == 'Iron Condor':
        put_short = suggestion.get('put_short_strike', 0)
        put_long = suggestion.get('put_long_strike', 0)
        call_short = suggestion.get('call_short_strike', 0)
        call_long = suggestion.get('call_long_strike', 0)
        strikes_info = f"{put_long:.0f}/{put_short:.0f}/{call_short:.0f}/{call_long:.0f}"
    else:
        # Fallback for other strategies
        strikes_info = ""
        short_strike = suggestion.get('short_strike', suggestion.get('strike_price', 0))
        if short_strike:
            strikes_info = f"{short_strike:.0f}"
            long_strike = suggestion.get('long_strike', 0)
            if long_strike:
                strikes_info += f"/{long_strike:.0f}"
    
    # Construct the descriptive title
    if strikes_info:
        title = f"{ticker} {formatted_date} {strikes_info} {strategy}"
    else:
        title = f"{ticker} {formatted_date} {strategy}"
    
    return title

def generate_optionstrat_url(suggestion: dict) -> str:
    """Generate the correct OptionStrat URL for a trade suggestion"""
    ticker = suggestion['ticker']
    strategy = suggestion['strategy']
    
    # Base URL
    base_url = "https://optionstrat.com/build/"
    
    if strategy == 'Bull Put Spread':
        # Format: /bull-put-spread/TICKER/-.TICKER250801P575,.TICKER250801P580
        # SELL higher strike put, BUY lower strike put
        short_strike = suggestion.get('short_strike', suggestion.get('strike_price', 0))
        long_strike = suggestion.get('long_strike', short_strike - 5 if short_strike else 0)
        exp_date = suggestion.get('expiration', '2025-08-01')
        
        # Convert YYYY-MM-DD to YYMMDD format for option symbols
        exp_obj = datetime.strptime(exp_date, '%Y-%m-%d')
        exp_symbol = exp_obj.strftime('%y%m%d')  # 250801 instead of 20250801
        
        # OptionStrat format: SELL gets minus, BUY doesn't - preserve decimals
        short_symbol = f"-.{ticker}{exp_symbol}P{short_strike:g}"  # SELL (minus sign)
        long_symbol = f".{ticker}{exp_symbol}P{long_strike:g}"     # BUY (no minus)
        url = f"{base_url}bull-put-spread/{ticker}/{short_symbol},{long_symbol}"
        
    elif strategy == 'Bear Call Spread':
        # Format: /bear-call-spread/TICKER/-.TICKER250801C660,.TICKER250801C680
        # SELL lower strike call, BUY higher strike call
        short_strike = suggestion.get('short_strike', suggestion.get('strike_price', 0))
        long_strike = suggestion.get('long_strike', short_strike + 5 if short_strike else 0)
        exp_date = suggestion.get('expiration', '2025-08-01')
        
        # Convert YYYY-MM-DD to YYMMDD format for option symbols
        exp_obj = datetime.strptime(exp_date, '%Y-%m-%d')
        exp_symbol = exp_obj.strftime('%y%m%d')  # 250801 instead of 20250801
        
        # OptionStrat format: SELL gets minus, BUY doesn't - preserve decimals
        short_symbol = f"-.{ticker}{exp_symbol}C{short_strike:g}"  # SELL (minus sign)
        long_symbol = f".{ticker}{exp_symbol}C{long_strike:g}"     # BUY (no minus)
        url = f"{base_url}bear-call-spread/{ticker}/{short_symbol},{long_symbol}"
        
    elif strategy == 'Iron Condor':
        # OptionStrat Iron Condor format: .SPY250801P575,-.SPY250801P590,-.SPY250801C660,.SPY250801C680
        base_strike = suggestion.get('strike_price', 0)
        put_long = suggestion.get('put_long_strike', base_strike - 10 if base_strike else 0)
        put_short = suggestion.get('put_short_strike', base_strike - 5 if base_strike else 0) 
        call_short = suggestion.get('call_short_strike', base_strike + 5 if base_strike else 0)
        call_long = suggestion.get('call_long_strike', base_strike + 10 if base_strike else 0)
        exp_date = suggestion.get('expiration', '2025-08-01')
        
        # Convert YYYY-MM-DD to YYMMDD format for option symbols
        exp_obj = datetime.strptime(exp_date, '%Y-%m-%d')
        exp_symbol = exp_obj.strftime('%y%m%d')  # 250801 instead of 20250801
        
        # Create option symbols in OptionStrat format - preserve decimals for half-dollar strikes
        put_long_symbol = f".{ticker}{exp_symbol}P{put_long:g}"    # Buy put (long)
        put_short_symbol = f"-.{ticker}{exp_symbol}P{put_short:g}"  # Sell put (short, has minus)
        call_short_symbol = f"-.{ticker}{exp_symbol}C{call_short:g}" # Sell call (short, has minus)
        call_long_symbol = f".{ticker}{exp_symbol}C{call_long:g}"   # Buy call (long)
        
        # Combine in order: PUT_LONG,PUT_SHORT,CALL_SHORT,CALL_LONG
        symbols = f"{put_long_symbol},{put_short_symbol},{call_short_symbol},{call_long_symbol}"
        url = f"{base_url}iron-condor/{ticker}/{symbols}"
        
    elif strategy == 'Short Strangle':
        # Format: /short-strangle/TICKER/.TICKER250801P575,-.TICKER250801C660
        put_strike = suggestion.get('put_strike', suggestion.get('short_put_strike'))
        call_strike = suggestion.get('call_strike', suggestion.get('short_call_strike'))
        exp_date = suggestion.get('expiration', '2025-08-01')
        
        # Convert YYYY-MM-DD to YYMMDD format for option symbols
        exp_obj = datetime.strptime(exp_date, '%Y-%m-%d')
        exp_symbol = exp_obj.strftime('%y%m%d')  # 250801 instead of 20250801
        
        # OptionStrat format: .TICKER250801P575,-.TICKER250801C660 - preserve decimals
        put_symbol = f".{ticker}{exp_symbol}P{put_strike:g}"   # Sell put (short)
        call_symbol = f"-.{ticker}{exp_symbol}C{call_strike:g}" # Sell call (short)
        url = f"{base_url}short-strangle/{ticker}/{put_symbol},{call_symbol}"
        
    elif strategy == 'Cash Secured Put':
        # Format: /cash-secured-put/TICKER/.TICKER250801P575
        strike = suggestion.get('strike', suggestion.get('put_strike'))
        exp_date = suggestion.get('expiration', '2025-08-01')
        
        # Convert YYYY-MM-DD to YYMMDD format for option symbols
        exp_obj = datetime.strptime(exp_date, '%Y-%m-%d')
        exp_symbol = exp_obj.strftime('%y%m%d')  # 250801 instead of 20250801
        
        # OptionStrat format: .TICKER250801P575 (sell put) - preserve decimals
        put_symbol = f".{ticker}{exp_symbol}P{strike:g}"
        url = f"{base_url}cash-secured-put/{ticker}/{put_symbol}"
        
    elif strategy == 'Covered Call':
        # Format: /covered-call/TICKER/-.TICKER250801C575
        strike = suggestion.get('strike', suggestion.get('call_strike'))
        exp_date = suggestion.get('expiration', '2025-08-01')
        
        # Convert YYYY-MM-DD to YYMMDD format for option symbols
        exp_obj = datetime.strptime(exp_date, '%Y-%m-%d')
        exp_symbol = exp_obj.strftime('%y%m%d')  # 250801 instead of 20250801
        
        # OptionStrat format: -.TICKER250801C575 (sell call) - preserve decimals
        call_symbol = f"-.{ticker}{exp_symbol}C{strike:g}"
        url = f"{base_url}covered-call/{ticker}/{call_symbol}"
        
    else:
        # Fallback to generic strategy page
        strategy_name = strategy.lower().replace(' ', '-')
        url = f"{base_url}{strategy_name}/{ticker}"
    
    return url

def render_options_tracker():
    """Main Options Trading Tracker interface"""
    
    st.title("🎯 Options Trading Tracker")
    st.markdown("**Weekly Income Strategy Tracker** - Target: $500/week")
    
    # Initialize tracker
    if 'options_tracker' not in st.session_state:
        st.session_state.options_tracker = OptionsTracker()
    
    tracker = st.session_state.options_tracker
    
    # Network status check and display
    network_status = tracker.check_network_status()
    
    # Display network status
    st.sidebar.header("🌐 Network Status")
    if network_status['is_online']:
        st.sidebar.success(network_status['status_message'])
        st.sidebar.caption(f"Last checked: {network_status.get('last_check', 'Unknown')}")
    else:
        st.sidebar.error(network_status['status_message'])
        st.sidebar.caption(f"Last checked: {network_status.get('last_check', 'Unknown')}")
        
        # Show specific guidance for corporate networks
        if network_status['network_type'] == 'corporate_blocked':
            with st.sidebar.expander("🏢 Corporate Network Solutions", expanded=True):
                st.write("**Recommended Solutions:**")
                for i, rec in enumerate(network_status['recommendations'], 1):
                    st.write(f"{i}. {rec}")
                
                st.write("**Technical Details:**")
                st.write("• DNS resolution blocked for external domains")
                st.write("• Yahoo Finance APIs inaccessible")
                st.write("• Alternative: Use mobile hotspot")
                
                st.info("💡 **Tip**: Application works fully from home networks")
        
        # Show limited functionality warning
        st.warning("⚠️ **Limited Functionality**: Some features require internet access to financial data sources.")
    
    # Add network refresh button
    if st.sidebar.button("🔄 Check Network Now", help="Force immediate network connectivity check"):
        # Force a fresh check using the dedicated method
        st.session_state.options_tracker.force_network_recheck()
        st.rerun()
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard", 
        "💡 New Trades", 
        "📈 Market Analysis", 
        "🔍 Trade Management",
        "📋 Trade History"
    ])
    
    with tab1:
        render_dashboard(tracker)
    
    with tab2:
        render_new_trades(tracker)
    
    with tab3:
        render_market_analysis(tracker)
    
    with tab4:
        render_trade_management(tracker)
    
    with tab5:
        render_trade_history(tracker)

def render_dashboard(tracker: OptionsTracker):
    """Render the main dashboard"""
    
    st.header("📊 Portfolio Overview")
    
    # Get performance stats
    stats = tracker.calculate_weekly_pnl()
    open_trades = tracker.get_open_trades()
    
    # Performance metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total P&L", 
            f"${stats.get('total_pnl', 0):.2f}",
            delta=f"${stats.get('avg_weekly', 0):.2f}/week"
        )
    
    with col2:
        st.metric(
            "Win Rate", 
            f"{stats.get('win_rate', 0):.1%}",
            delta=f"{stats.get('winning_trades', 0)}/{stats.get('total_trades', 0)} trades"
        )
    
    with col3:
        st.metric(
            "Open Trades", 
            len(open_trades),
            delta="Active positions"
        )
    
    with col4:
        weekly_target = 500
        avg_weekly = stats.get('avg_weekly', 0)
        progress = (avg_weekly / weekly_target) * 100 if weekly_target > 0 else 0
        st.metric(
            "Target Progress", 
            f"{progress:.1f}%",
            delta=f"${weekly_target - avg_weekly:.2f} to target"
        )
    
    # Open trades summary
    if open_trades:
        st.subheader("🔗 Active Trades")

        # Build table with OptionStrat links for Ticker
        trades_data = []
        for trade in open_trades:
            try:
                evaluation = tracker.evaluate_trade(trade)
            except Exception:
                evaluation = {'recommendation': 'REVIEW', 'reason': 'Error evaluating trade'}
                
            credit_per_contract = trade.get('credit', 0) * 100
            max_loss_per_contract = trade.get('max_loss', 0) * 100
            
            # Generate OptionStrat URL for this trade
            try:
                optionstrat_url = generate_optionstrat_url(trade)
                ticker_link = f"[**{trade.get('ticker', 'UNKNOWN')}**]({optionstrat_url})"
            except Exception:
                ticker_link = trade.get('ticker', 'UNKNOWN')
                
            trades_data.append({
                'Ticker': ticker_link,
                'Strategy': trade.get('strategy', 'UNKNOWN'),
                'Entry Date': trade.get('entry_date', 'N/A'),
                'Expiration': trade.get('expiration', 'N/A'),
                'Credit': f"${credit_per_contract:.0f} (${trade.get('credit', 0):.2f})",
                'Max Loss': f"${max_loss_per_contract:.0f} (${trade.get('max_loss', 0):.2f})",
                'Recommendation': evaluation.get('recommendation', 'REVIEW'),
                'Reason': evaluation.get('reason', 'No evaluation available')
            })

        # Use st.write with st.markdown for clickable links
        df = pd.DataFrame(trades_data)
        # Color code recommendations
        def highlight_recommendation(val):
            if val == 'CLOSE':
                return 'background-color: #ffcccc'
            elif val == 'ADJUST':
                return 'background-color: #fff4cc'
            else:
                return 'background-color: #ccffcc'

        # Show as HTML for clickable links
        st.write("**Click ticker to view on OptionStrat**")
        st.dataframe(df.style.applymap(highlight_recommendation, subset=['Recommendation']), use_container_width=True)
        # Show as markdown table for links (Streamlit's dataframe disables links)
        st.markdown(df.to_markdown(index=False), unsafe_allow_html=True)
    else:
        st.info("No active trades. Check the 'New Trades' tab for suggestions!")

def render_new_trades(tracker: OptionsTracker):
    """Render new trade suggestions"""
    
    st.header("💡 Trade Suggestions")
    
    # Check network connectivity first
    network_status = tracker.check_network_status()
    
    if not network_status.get('is_online', True):
        st.warning("⚠️ **Trade suggestions unavailable** - Requires internet access for market data")
        
        if network_status.get('network_type') == 'corporate_blocked':
            st.info("🏢 **Corporate Network**: Trade generation requires external financial data sources")
            
            with st.expander("🔧 Solutions for Trade Generation", expanded=True):
                st.write("**To generate new trade suggestions:**")
                st.write("• Use mobile hotspot for data connectivity")
                st.write("• Access from home network") 
                st.write("• Request IT to whitelist financial APIs")
                
                st.write("**Available Features:**")
                st.write("• Trade management (existing trades)")
                st.write("• Trade history and analysis")
                st.write("• Manual trade entry")
        
        st.info("💡 You can still manually add trades or manage existing positions")
        return
    
    # Generate suggestions
    if st.button("🔄 Generate New Suggestions", type="primary"):
        with st.spinner("Analyzing markets and generating trade ideas..."):
            try:
                suggestions = tracker.generate_trade_suggestions(3)
                st.session_state.trade_suggestions = suggestions
            except Exception as e:
                st.error(f"Unable to generate suggestions: {str(e)}")
                if "DNS" in str(e) or "resolve" in str(e):
                    st.info("This appears to be a network connectivity issue. Try from a different network.")
                return
    
    # Show suggestions
    if hasattr(st.session_state, 'trade_suggestions'):
        suggestions = st.session_state.trade_suggestions
        
        if suggestions:
            for i, suggestion in enumerate(suggestions):
                # Generate descriptive title using the helper function
                descriptive_title = generate_descriptive_title(suggestion)
                st.subheader(f"💼 Suggestion #{i+1}: {descriptive_title}")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Strategy:** {suggestion['strategy']}")
                    st.write(f"**Bias:** {suggestion['bias']} ({suggestion['bullish_prob']:.1%} bullish probability)")
                    st.write(f"**Confidence:** {suggestion['confidence']}")
                    
                    # Show detailed reasoning if available
                    if 'reasoning' in suggestion:
                        with st.expander("🧠 Strategy Reasoning", expanded=True):
                            st.text(suggestion['reasoning'])
                    
                    # Detailed leg information
                    if 'legs' in suggestion:
                        st.write("**Trade Legs:**")
                        legs_data = []
                        for leg in suggestion['legs']:
                            legs_data.append({
                                'Action': leg['action'],
                                'Type': leg['type'],
                                'Strike': f"${leg['strike']:.2f}",
                                'Est. Price': f"${leg['price']:.2f}",
                                'Strike_Sort': leg['strike']  # For sorting by strike price
                            })
                        
                        # Sort legs by strike price (smallest on top)
                        legs_data.sort(key=lambda x: x['Strike_Sort'])
                        
                        # Remove the sort key before displaying
                        for leg in legs_data:
                            del leg['Strike_Sort']
                        
                        legs_df = pd.DataFrame(legs_data)
                        st.dataframe(legs_df, use_container_width=True, hide_index=True)
                    
                    # Strategy details (fallback for older format)
                    else:
                        if suggestion['strategy'] == 'Bull Put Spread':
                            short_strike = suggestion.get('short_strike', suggestion.get('strike_price', 0))
                            long_strike = suggestion.get('long_strike', short_strike - 5 if short_strike else 0)
                            st.write(f"**Short Put:** ${short_strike:.2f}")
                            st.write(f"**Long Put:** ${long_strike:.2f}")
                        elif suggestion['strategy'] == 'Bear Call Spread':
                            short_strike = suggestion.get('short_strike', suggestion.get('strike_price', 0))
                            long_strike = suggestion.get('long_strike', short_strike + 5 if short_strike else 0)
                            st.write(f"**Short Call:** ${short_strike:.2f}")
                            st.write(f"**Long Call:** ${long_strike:.2f}")
                        elif suggestion['strategy'] == 'Iron Condor':
                            put_short = suggestion.get('put_short_strike', suggestion.get('strike_price', 0))
                            put_long = suggestion.get('put_long_strike', put_short - 5 if put_short else 0)
                            call_short = suggestion.get('call_short_strike', suggestion.get('strike_price', 0))
                            call_long = suggestion.get('call_long_strike', call_short + 5 if call_short else 0)
                            st.write(f"**Put Spread:** ${put_long:.2f} / ${put_short:.2f}")
                            st.write(f"**Call Spread:** ${call_short:.2f} / ${call_long:.2f}")
                
                with col2:
                    # Options contracts are for 100 shares, so multiply by 100 for actual dollar amounts
                    credit_per_contract = suggestion.get('credit', suggestion.get('expected_profit', 0) / 100) * 100
                    max_loss_per_contract = suggestion.get('max_loss', suggestion.get('risk', 0)) * 100
                    profit_target_per_contract = suggestion.get('profit_target', suggestion.get('expected_profit', 0)) * 100
                    max_profit_per_contract = credit_per_contract  # Max profit = credit received
                    
                    # Display both spread price and contract value
                    credit_per_share = suggestion.get('credit', suggestion.get('expected_profit', 0) / 100)
                    max_loss_per_share = suggestion.get('max_loss', suggestion.get('risk', 0) / 100)
                    
                    st.metric(
                        "Credit", 
                        f"${credit_per_contract:.0f}",
                        delta=f"${credit_per_share:.2f}/share"
                    )
                    st.metric(
                        "Max Loss", 
                        f"${max_loss_per_contract:.0f}",
                        delta=f"${max_loss_per_share:.2f}/share"
                    )
                    st.metric(
                        "Profit Target (50%)", 
                        f"${profit_target_per_contract:.0f}",
                        delta=f"Max: ${max_profit_per_contract:.0f}"
                    )
                    
                    # Add explanation for profit target
                    with st.expander("💡 Profit Exit Strategy", expanded=False):
                        st.write(f"""
                        **50% Profit Rule**: Exit when you've captured 50% of maximum profit.
                        
                        • **Max Profit**: ${max_profit_per_contract:.0f} (keep entire credit if held to expiration)
                        • **Profit Target**: ${profit_target_per_contract:.0f} (recommended early exit point)
                        
                        **Why exit at 50%?**
                        • Reduces time decay risk
                        • Locks in most of the profit early
                        • Frees up capital for new trades
                        • Avoids last-minute price movements
                        
                        You can always hold to expiration for max profit, but 50% is a proven risk management strategy.
                        """)
                
                # OptionStrat link - Generate correct URL for the suggested trade
                optionstrat_url = generate_optionstrat_url(suggestion)
                st.markdown(f"[📊 View on OptionStrat]({optionstrat_url})")
                
                # Add trade button
                if st.button(f"✅ Add Trade #{i+1}", key=f"add_trade_{i}"):
                    tracker.add_trade(suggestion)
                    st.success(f"Added {suggestion['strategy']} trade for {suggestion['ticker']}!")
                    st.rerun()
                
                st.divider()
        else:
            st.warning("No suitable trade suggestions found at this time.")
    else:
        st.info("Click 'Generate New Suggestions' to get trade recommendations!")

def render_market_analysis(tracker: OptionsTracker):
    """Render market analysis and predictions"""
    
    st.header("📈 Market Analysis & Predictions")
    
    # Check network connectivity for market data
    network_status = tracker.check_network_status()
    if not network_status.get('is_online', True):
        st.warning("⚠️ **Market data unavailable** - Network connectivity required for real-time analysis")
        
        if network_status.get('network_type') == 'corporate_blocked':
            st.info("🏢 **Corporate Network Detected**: Market analysis requires external data sources that may be blocked by your corporate firewall.")
            
            with st.expander("💡 Alternative Solutions", expanded=True):
                st.write("**Options:**")
                st.write("1. **Mobile Hotspot**: Use mobile data for market analysis")
                st.write("2. **Home Network**: Full functionality available outside corporate network")
                st.write("3. **IT Request**: Ask IT to whitelist financial data domains")
                st.write("4. **VPN**: If permitted, use VPN to access external data")
        
        st.info("📊 **Offline Mode**: Trade management and history features remain available")
        return
    
    # Watchlist analysis
    st.subheader("📊 Watchlist Forecast")
    
    forecast_data = []
    try:
        for ticker, forecast in tracker.watchlist.items():
            prediction = tracker.predict_price_range(ticker)
            
            if prediction:
                forecast_data.append({
                    'Ticker': ticker,
                    'Current Price': f"${prediction['current_price']:.2f}",
                    '68% Range': f"${prediction['lower_bound']:.2f} - ${prediction['upper_bound']:.2f}",
                    'Target Zone': f"${prediction['target_price']:.2f}",
                    'Bullish Prob': f"{prediction['bullish_probability']:.1%}",
                    'Bias Score': f"{prediction['bias_score']:.2f}",
                    'Weekly Vol': f"{prediction['weekly_volatility']:.1%}"
                })
    except Exception as e:
        st.error(f"Unable to fetch market data: {str(e)}")
        st.info("This may be due to network restrictions or external API limitations.")
        return
    
    if forecast_data:
        df = pd.DataFrame(forecast_data)
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No market data available. Check network connectivity.")
    
    # Detailed analysis for selected ticker
    st.subheader("🔍 Detailed Technical Analysis")
    
    selected_ticker = st.selectbox(
        "Select ticker for detailed analysis:",
        list(tracker.watchlist.keys())
    )
    
    if selected_ticker:
        prediction = tracker.predict_price_range(selected_ticker)
        
        if prediction:
            # Summary Section
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**📊 Price Prediction Summary:**")
                st.write(f"Current: ${prediction['current_price']:.2f}")
                st.write(f"Target: ${prediction['target_price']:.2f}")
                st.write(f"Range: ${prediction['lower_bound']:.2f} - ${prediction['upper_bound']:.2f}")
                st.write(f"Bullish Probability: {prediction['bullish_probability']:.1%}")
            
            with col2:
                indicators = prediction['indicators']
                st.write("**📈 Technical Indicators:**")
                st.write(f"RSI: {indicators.get('rsi', 0):.1f}")
                st.write(f"MACD: {indicators.get('macd', 0):.3f}")
                st.write(f"5-day MA: ${indicators.get('ma_5', 0):.2f}")
                st.write(f"Volume Ratio: {indicators.get('volume_ratio', 0):.2f}x")
                st.write(f"Momentum: {indicators.get('momentum', 0):.2f}%")
            
            # Mathematical Breakdown Section
            st.subheader("🧮 Mathematical Calculation Breakdown")
            
            # Dual-Model Detection and ATR-Based Volatility Analysis
            is_dual_model = prediction.get('method') == 'dual_model_atr_specification' or 'atr_value' in prediction
            
            if is_dual_model:
                with st.expander("📊 Step 1: ATR-Based Volatility Analysis", expanded=True):
                    current_price = prediction['current_price']
                    atr_value = prediction.get('atr_value', 0)
                    weekly_vol = prediction['weekly_volatility']
                    iv_based = prediction.get('iv_based', False)

                    st.write("**🎯 Dual-Model Volatility Comparison:**")

                    # ATR Analysis
                    st.write("**🎯 ATR (Average True Range) - Primary Model:**")
                    st.success("✅ Using 14-day ATR for range calculation")
                    st.write("- More responsive to recent price action")
                    st.write("- Accounts for gaps and limit moves")
                    st.write("- Industry standard for volatility measurement")

                    # Historical Vol Comparison
                    annual_vol = weekly_vol * np.sqrt(52)
                    st.write("**📊 Historical Volatility - Comparison:**")
                    if iv_based:
                        st.info("📈 Implied Volatility overlay available")
                    else:
                        st.info("📊 Using historical volatility for IV comparison")

                    st.write("**Calculation Comparison:**")
                    st.code(f"""
ATR (14-day): ${atr_value:.2f}
Historical Vol: {annual_vol:.1%} annual, {weekly_vol:.1%} weekly
ATR Range Width: ${prediction.get('range_width_$', 0):.2f} ({prediction.get('range_width_%', 0):.1%})

ATR-Based Range: ${prediction.get('predicted_low', 0):.2f} - ${prediction.get('predicted_high', 0):.2f}
                    """)

                    # IV Overlay if available
                    if prediction.get('iv_range'):
                        st.write("**📈 Implied Volatility Overlay:**")
                        st.code(f"""
ATR Range: ${prediction.get('predicted_low', 0):.2f} - ${prediction.get('predicted_high', 0):.2f}
IV Range:  {prediction['iv_range']}
                        """)
            else:
                # Legacy volatility analysis for non-dual-model predictions
                with st.expander("📊 Step 1: Volatility Analysis", expanded=True):
                    current_price = prediction['current_price']
                    weekly_vol = prediction['weekly_volatility']
                    iv_based = prediction.get('iv_based', False)
                    
                    st.write("**Volatility Source:**")
                    if iv_based:
                        st.success("✅ Using Implied Volatility from options market")
                        st.write("- More accurate as it reflects market expectations")
                        st.write("- Derived from current option prices")
                    else:
                        st.info("📊 Using Historical Volatility (IV unavailable)")
                        st.write("- Based on past 3-month price movements")
                        st.write("- Annualized volatility divided by √52 for weekly")
                    
                    st.write("**Calculation:**")
                    annual_vol = weekly_vol * np.sqrt(52)
                    st.code(f"""
Weekly Volatility = {weekly_vol:.3f} ({weekly_vol:.1%})
Annual Volatility = {annual_vol:.3f} ({annual_vol:.1%})
Base Range = Current Price × Weekly Vol
Base Range = ${current_price:.2f} × {weekly_vol:.3f} = ${current_price * weekly_vol:.2f}
                    """)
            
            # Dual-Model Step 2: Technical Bias / Regime Scoring
            if is_dual_model:
                with st.expander("⚖️ Step 2: Standardized Regime Scoring", expanded=True):
                    indicators = prediction['indicators']
                    rsi = indicators.get('rsi', 50)
                    macd = indicators.get('macd', 0)
                    macd_signal = indicators.get('macd_signal', 0)
                    momentum = indicators.get('momentum', 0)
                    regime_score = prediction.get('regime_score', 0)

                    st.write("**🎯 Dual-Model Specification Compliance:**")
                    st.write("Following exact algorithm from Dual_Model_Price_Prediction_Spec.md")

                    st.write("**Individual Regime Components:**")

                    # RSI Bias (exact spec)
                    rsi_bias = -0.2 if rsi > 70 else (0.2 if rsi < 30 else 0.0)
                    if rsi > 70:
                        st.write(f"🔴 RSI Bias: {rsi:.1f} > 70 (Overbought) → -0.2")
                    elif rsi < 30:
                        st.write(f"🟢 RSI Bias: {rsi:.1f} < 30 (Oversold) → +0.2")
                    else:
                        st.write(f"🟡 RSI Bias: {rsi:.1f} (Neutral) → 0.0")

                    # MACD Bias (exact spec)
                    macd_bias = 0.1 if macd > macd_signal else -0.1
                    macd_direction = "Bullish" if macd > macd_signal else "Bearish"
                    macd_color = "🟢" if macd > macd_signal else "🔴"
                    st.write(f"{macd_color} MACD Bias: {macd:.3f} vs {macd_signal:.3f} ({macd_direction}) → {macd_bias:+.1f}")

                    # Momentum Bias (exact spec)
                    momentum_bias = 0.1 if momentum > 2 else (-0.1 if momentum < -2 else 0.0)
                    if momentum > 2:
                        st.write(f"🟢 Momentum Bias: {momentum:.2f}% > 2% (Strong Up) → +0.1")
                    elif momentum < -2:
                        st.write(f"🔴 Momentum Bias: {momentum:.2f}% < -2% (Strong Down) → -0.1")
                    else:
                        st.write(f"🟡 Momentum Bias: {momentum:.2f}% (Neutral) → 0.0")

                    st.write("**🧮 Regime Score Calculation:**")
                    st.code(f"""
# Dual-Model Specification:
rsi_bias = {rsi_bias:+.1f}
macd_bias = {macd_bias:+.1f}
momentum_bias = {momentum_bias:+.1f}

regime_score = rsi_bias + macd_bias + momentum_bias
regime_score = {regime_score:+.2f}
                    """)
            else:
                # Legacy technical bias calculation for non-dual-model predictions
                with st.expander("⚖️ Step 2: Technical Bias Calculation", expanded=True):
                    rsi = indicators.get('rsi', 50)
                    macd = indicators.get('macd', 0)
                    macd_signal = indicators.get('macd_signal', 0)
                    momentum = indicators.get('momentum', 0)
                    bias_score = prediction.get('bias_score', 0)
                    
                    st.write("**Individual Bias Components:**")
                    
                    # RSI Bias
                    rsi_bias = 0
                    if rsi > 70:
                        rsi_bias = -0.2
                        st.write(f"🔴 RSI Bias: {rsi:.1f} > 70 (Overbought) → -0.2")
                    elif rsi < 30:
                        rsi_bias = 0.2
                        st.write(f"🟢 RSI Bias: {rsi:.1f} < 30 (Oversold) → +0.2")
                    
                    # Calculate macd_bias and momentum_bias for total bias
                    macd_bias = 0.1 if macd > macd_signal else -0.1
                    momentum_bias = 0.1 if momentum > 2 else (-0.1 if momentum < -2 else 0.0)
                    
                    st.write("**Total Bias Score:**")
                    st.code(f"""
Total Bias = RSI + MACD + Momentum
Total Bias = {rsi_bias:+.1f} + {macd_bias:+.1f} + {momentum_bias:+.1f} = {bias_score:+.2f}
                    """)

            # Dual-Model Step 3: Range Calculation
            if is_dual_model:
                with st.expander("🎯 Step 3: Dual-Model Range Calculation", expanded=True):
                    current_price = prediction['current_price']
                    target_mid = prediction.get('target_mid', prediction.get('target_price', current_price))
                    atr_value = prediction.get('atr_value', 0)
                    regime_score = prediction.get('regime_score', 0)
                    predicted_low = prediction.get('predicted_low', prediction.get('lower_bound', 0))
                    predicted_high = prediction.get('predicted_high', prediction.get('upper_bound', 0))

                    st.write("**🎯 Target Price Calculation (Spec):**")
                    bias_pct = regime_score * 0.01
                    st.code(f"""
# Step 1: Target Price
bias_pct = regime_score × 0.01 = {regime_score:.3f} × 0.01 = {bias_pct:.5f}
target_mid = current_price × (1 + bias_pct)
target_mid = ${current_price:.2f} × (1 + {bias_pct:.5f}) = ${target_mid:.2f}
                    """)

                    st.write("**📊 ATR Range Calculation (Spec):**")
                    st.code(f"""
# Step 2: ATR Range
ATR (14-day) = ${atr_value:.2f}
predicted_low = target_mid - atr_value = ${target_mid:.2f} - ${atr_value:.2f} = ${predicted_low:.2f}
predicted_high = target_mid + atr_value = ${target_mid:.2f} + ${atr_value:.2f} = ${predicted_high:.2f}

Range Width = ${prediction.get('range_width_$', 0):.2f} ({prediction.get('range_width_%', 0):.1f}% of current price)
                    """)

                    # Show IV overlay if available
                    if prediction.get('iv_range'):
                        st.write("**📈 IV Overlay Comparison:**")
                        st.code(f"""
ATR Range: ${predicted_low:.2f} - ${predicted_high:.2f}
IV Range:  {prediction['iv_range']}
                        """)
            else:
                # Legacy final price range calculation for non-dual-model predictions
                with st.expander("🎯 Step 3: Final Price Range Calculation", expanded=True):
                    current_price = prediction['current_price']
                    target_price = prediction.get('target_price', current_price)
                    lower_bound = prediction.get('lower_bound', current_price * 0.95)
                    upper_bound = prediction.get('upper_bound', current_price * 1.05)
                    
                    st.write("**🎯 Target Price Calculation:**")
                    st.code(f"""
Target Price = ${target_price:.2f}
                    """)
                    
                    st.write("**🎯 Range Calculation:**")
                    st.code(f"""
Lower Bound = ${lower_bound:.2f}
Upper Bound = ${upper_bound:.2f}
Range Width = ${upper_bound - lower_bound:.2f} ({((upper_bound - lower_bound) / current_price * 100):.1f}%)
                    """)

def render_trade_management(tracker: OptionsTracker):
    """Render trade management interface"""
    
    st.header("🔍 Trade Management")
    
    open_trades = tracker.get_open_trades()
    
    if not open_trades:
        st.info("No open trades to manage.")
        return
    
    for i, trade in enumerate(open_trades):
        # Handle trades without ID (legacy data)
        trade_id = trade.get('id', f'legacy_{i}')
        ticker = trade.get('ticker', 'UNKNOWN')
        strategy = trade.get('strategy', 'UNKNOWN')
        
        st.subheader(f"Trade #{trade_id}: {ticker} {strategy}")
        
        try:
            evaluation = tracker.evaluate_trade(trade)
        except Exception as e:
            evaluation = {'recommendation': 'REVIEW', 'reason': f'Error evaluating: {str(e)}'}
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write(f"**Entry Date:** {trade.get('entry_date', 'N/A')}")
            st.write(f"**Expiration:** {trade.get('expiration', 'N/A')}")
            st.write(f"**Credit:** ${trade.get('credit', 0) * 100:.0f}")
            st.write(f"**Recommendation:** {evaluation.get('recommendation', 'REVIEW')}")
            st.write(f"**Reason:** {evaluation.get('reason', 'No evaluation available')}")
        
        with col2:
            if st.button("✅ Close Trade", key=f"close_{trade_id}", type="primary"):
                exit_price = st.number_input("Exit Price:", value=0.0, step=0.01, key=f"exit_price_{trade_id}")
                exit_reason = st.text_input("Exit Reason:", key=f"exit_reason_{trade_id}")
                
                if exit_price > 0 and exit_reason:
                    # Handle trades without proper ID
                    if 'id' in trade and hasattr(tracker, 'close_trade'):
                        if tracker.close_trade(trade['id'], exit_price, exit_reason):
                            st.success("Trade closed successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to close trade.")
                    else:
                        st.warning("⚠️ Legacy trade format - manual closing required")
        
        with col3:
            if st.button("🗑️ Delete Trade", key=f"delete_{trade_id}"):
                # Handle trades without proper ID
                if 'id' in trade and hasattr(tracker, 'delete_trade'):
                    if tracker.delete_trade(trade['id']):
                        st.success("Trade deleted!")
                        st.rerun()
                    else:
                        st.error("Failed to delete trade.")
                else:
                    st.warning("⚠️ Legacy trade format - manual deletion required")
        
        st.divider()

def render_trade_history(tracker: OptionsTracker):
    # Render trade history and analytics
    
    st.header("📋 Trade History")
    
    closed_trades = tracker.get_closed_trades()
    
    if not closed_trades:
        st.info("No closed trades yet.")
        return
    
    # Performance summary
    stats = tracker.calculate_weekly_pnl()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Trades", stats['total_trades'])
    
    with col2:
        st.metric("Total P&L", f"${stats['total_pnl']:.2f}")
    
    with col3:
        st.metric("Win Rate", f"{stats['win_rate']:.1%}")
    
    # Trade history table
    st.subheader("📊 Trade History Details")
    
    history_data = []
    for trade in closed_trades:
        # Options contracts are for 100 shares, so multiply by 100 for actual dollar amounts
        credit_per_contract = trade.get('credit', 0) * 100
        exit_price_per_contract = trade.get('exit_price', 0) * 100
        pnl_per_contract = trade.get('pnl', 0) * 100
        
        history_data.append({
            'ID': trade['id'],
            'Ticker': trade['ticker'],
            'Strategy': trade['strategy'],
            'Entry Date': trade['entry_date'],
            'Exit Date': trade.get('exit_date', ''),
            'Credit': f"${credit_per_contract:.0f} (${trade.get('credit', 0):.2f})",
            'Exit Price': f"${exit_price_per_contract:.0f} (${trade.get('exit_price', 0):.2f})",
            'P&L': f"${pnl_per_contract:.0f} (${trade.get('pnl', 0):.2f})",
            'Exit Reason': trade.get('exit_reason', '')
        })
    
    df = pd.DataFrame(history_data)
    
    # Color code P&L
    def highlight_pnl(val):
        if 'P&L' in val.name:
            pnl_value = float(val.str.replace('$', '').str.replace(',', ''))
            return ['background-color: #ccffcc' if x > 0 else 'background-color: #ffcccc' for x in pnl_value]
        return [''] * len(val)
    
    styled_df = df.style.apply(highlight_pnl, axis=0)
    st.dataframe(styled_df, use_container_width=True)
    
    # Strategy performance breakdown
    st.subheader("📈 Strategy Performance")
    
    strategy_stats = {}
    for trade in closed_trades:
        strategy = trade['strategy']
        # Options contracts are for 100 shares, so multiply by 100 for actual dollar amounts
        pnl_per_contract = trade.get('pnl', 0) * 100
        
        if strategy not in strategy_stats:
            strategy_stats[strategy] = {'trades': 0, 'total_pnl': 0, 'wins': 0}
        
        strategy_stats[strategy]['trades'] += 1
        strategy_stats[strategy]['total_pnl'] += pnl_per_contract
        if pnl_per_contract > 0:
            strategy_stats[strategy]['wins'] += 1
    
    strategy_data = []
    for strategy, stats in strategy_stats.items():
        win_rate = stats['wins'] / stats['trades'] if stats['trades'] > 0 else 0
        avg_pnl = stats['total_pnl'] / stats['trades'] if stats['trades'] > 0 else 0
        
        strategy_data.append({
            'Strategy': strategy,
            'Trades': stats['trades'],
            'Total P&L': f"${stats['total_pnl']:.0f}",
            'Avg P&L': f"${avg_pnl:.0f}",
            'Win Rate': f"{win_rate:.1%}"
        })
    
    if strategy_data:
        strategy_df = pd.DataFrame(strategy_data)
        st.dataframe(strategy_df, use_container_width=True)

def run_options_tracker_ui():
    # Main entry point for the options tracker UI
    render_options_tracker()

def run_options_ui():
    # Alternative entry point for the options tracker UI.
    render_options_tracker()

# Export the main function
__all__ = ['render_options_tracker', 'run_options_tracker_ui', 'run_options_ui']

# Run the app when executed as main
if __name__ == "__main__":
    render_options_tracker()
