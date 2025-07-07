"""
🎯 Options Trading Tracker UI
============================

Streamlit interface for the Options Trading Tracker
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import sys
import os

# Add the src directory to Python path so modules can find each other
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the OptionsTracker from the current package
try:
    from .core import OptionsTracker
except ImportError:
    # Fallback for backward compatibility
    try:
        from options_tracker import OptionsTracker
    except ImportError:
        # Use a placeholder if neither is available
        class OptionsTracker:
            def __init__(self):
                pass

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
        if 'short_strike' in suggestion:
            strikes_info = f"{suggestion['short_strike']:.0f}"
            if 'long_strike' in suggestion:
                strikes_info += f"/{suggestion['long_strike']:.0f}"
    
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
        short_strike = suggestion['short_strike']  # SELL (higher strike)
        long_strike = suggestion['long_strike']    # BUY (lower strike)
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
        short_strike = suggestion['short_strike']  # SELL (lower strike)
        long_strike = suggestion['long_strike']    # BUY (higher strike)
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
        put_long = suggestion['put_long_strike']
        put_short = suggestion['put_short_strike'] 
        call_short = suggestion['call_short_strike']
        call_long = suggestion['call_long_strike']
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
        
        trades_data = []
        for trade in open_trades:
            evaluation = tracker.evaluate_trade(trade)
            
            # Options contracts are for 100 shares, so multiply by 100 for actual dollar amounts
            credit_per_contract = trade.get('credit', 0) * 100
            max_loss_per_contract = trade.get('max_loss', 0) * 100
            
            trades_data.append({
                'Ticker': trade['ticker'],
                'Strategy': trade['strategy'],
                'Entry Date': trade['entry_date'],
                'Expiration': trade['expiration'],
                'Credit': f"${credit_per_contract:.0f} (${trade.get('credit', 0):.2f})",
                'Max Loss': f"${max_loss_per_contract:.0f} (${trade.get('max_loss', 0):.2f})",
                'Recommendation': evaluation['recommendation'],
                'Reason': evaluation['reason']
            })
        
        df = pd.DataFrame(trades_data)
        
        # Color code recommendations
        def highlight_recommendation(val):
            if val == 'CLOSE':
                return 'background-color: #ffcccc'
            elif val == 'ADJUST':
                return 'background-color: #fff4cc'
            else:
                return 'background-color: #ccffcc'
        
        styled_df = df.style.applymap(highlight_recommendation, subset=['Recommendation'])
        st.dataframe(styled_df, use_container_width=True)
    else:
        st.info("No active trades. Check the 'New Trades' tab for suggestions!")

def render_new_trades(tracker: OptionsTracker):
    """Render new trade suggestions"""
    
    st.header("💡 Trade Suggestions")
    
    # Generate suggestions
    if st.button("🔄 Generate New Suggestions", type="primary"):
        with st.spinner("Analyzing markets and generating trade ideas..."):
            suggestions = tracker.generate_trade_suggestions(3)
            st.session_state.trade_suggestions = suggestions
    
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
                    st.write(f"**Confidence:** {suggestion['confidence']:.0f}%")
                    
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
                            st.write(f"**Short Put:** ${suggestion['short_strike']:.2f}")
                            st.write(f"**Long Put:** ${suggestion['long_strike']:.2f}")
                        elif suggestion['strategy'] == 'Bear Call Spread':
                            st.write(f"**Short Call:** ${suggestion['short_strike']:.2f}")
                            st.write(f"**Long Call:** ${suggestion['long_strike']:.2f}")
                        elif suggestion['strategy'] == 'Iron Condor':
                            st.write(f"**Put Spread:** ${suggestion['put_long_strike']:.2f} / ${suggestion['put_short_strike']:.2f}")
                            st.write(f"**Call Spread:** ${suggestion['call_short_strike']:.2f} / ${suggestion['call_long_strike']:.2f}")
                
                with col2:
                    # Options contracts are for 100 shares, so multiply by 100 for actual dollar amounts
                    credit_per_contract = suggestion['credit'] * 100
                    max_loss_per_contract = suggestion['max_loss'] * 100
                    profit_target_per_contract = suggestion['profit_target'] * 100
                    max_profit_per_contract = credit_per_contract  # Max profit = credit received
                    
                    # Display both spread price and contract value
                    st.metric(
                        "Credit", 
                        f"${credit_per_contract:.0f}",
                        delta=f"${suggestion['credit']:.2f}/share"
                    )
                    st.metric(
                        "Max Loss", 
                        f"${max_loss_per_contract:.0f}",
                        delta=f"${suggestion['max_loss']:.2f}/share"
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
    
    # Watchlist analysis
    st.subheader("📊 Watchlist Forecast")
    
    forecast_data = []
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
    
    if forecast_data:
        df = pd.DataFrame(forecast_data)
        st.dataframe(df, use_container_width=True)
    
    # Detailed analysis for selected ticker
    st.subheader("🔍 Detailed Technical Analysis")
    
    selected_ticker = st.selectbox(
        "Select ticker for detailed analysis:",
        list(tracker.watchlist.keys())
    )
    
    if selected_ticker:
        prediction = tracker.predict_price_range(selected_ticker)
        
        if prediction:
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Price Prediction:**")
                st.write(f"Current: ${prediction['current_price']:.2f}")
                st.write(f"Target: ${prediction['target_price']:.2f}")
                st.write(f"Range: ${prediction['lower_bound']:.2f} - ${prediction['upper_bound']:.2f}")
                st.write(f"Bullish Probability: {prediction['bullish_probability']:.1%}")
            
            with col2:
                indicators = prediction['indicators']
                st.write("**Technical Indicators:**")
                st.write(f"RSI: {indicators.get('rsi', 0):.1f}")
                st.write(f"MACD: {indicators.get('macd', 0):.3f}")
                st.write(f"5-day MA: ${indicators.get('ma_5', 0):.2f}")
                st.write(f"Volume Ratio: {indicators.get('volume_ratio', 0):.2f}x")
                st.write(f"Momentum: {indicators.get('momentum', 0):.2f}%")

def render_trade_management(tracker: OptionsTracker):
    """Render trade management interface"""
    
    st.header("🔍 Trade Management")
    
    # Manual trade entry section
    st.subheader("➕ Add Manual Trade")
    
    with st.expander("Add New Trade Manually"):
        col1, col2 = st.columns(2)
        
        with col1:
            manual_ticker = st.selectbox("Ticker:", list(tracker.watchlist.keys()), key="manual_ticker")
            manual_strategy = st.selectbox("Strategy:", tracker.strategy_types, key="manual_strategy")
            manual_credit = st.number_input("Credit Received:", value=0.0, step=0.01, key="manual_credit")
            manual_max_loss = st.number_input("Max Loss:", value=0.0, step=0.01, key="manual_max_loss")
        
        with col2:
            manual_expiration = st.date_input("Expiration Date:", key="manual_expiration")
            manual_notes = st.text_area("Trade Notes:", key="manual_notes")
        
        # Strategy-specific fields
        if manual_strategy in ["Bull Put Spread", "Bear Call Spread"]:
            col1, col2 = st.columns(2)
            with col1:
                short_strike = st.number_input("Short Strike:", value=0.0, step=0.01, key="manual_short_strike")
            with col2:
                long_strike = st.number_input("Long Strike:", value=0.0, step=0.01, key="manual_long_strike")
        
        elif manual_strategy == "Iron Condor":
            col1, col2 = st.columns(2)
            with col1:
                put_short_strike = st.number_input("Put Short Strike:", value=0.0, step=0.01, key="manual_put_short")
                put_long_strike = st.number_input("Put Long Strike:", value=0.0, step=0.01, key="manual_put_long")
            with col2:
                call_short_strike = st.number_input("Call Short Strike:", value=0.0, step=0.01, key="manual_call_short")
                call_long_strike = st.number_input("Call Long Strike:", value=0.0, step=0.01, key="manual_call_long")
        
        if st.button("✅ Add Manual Trade", type="primary"):
            # Build trade data
            trade_data = {
                'ticker': manual_ticker,
                'strategy': manual_strategy,
                'credit': manual_credit,
                'max_loss': manual_max_loss,
                'expiration': manual_expiration.strftime('%Y-%m-%d'),
                'notes': manual_notes
            }
            
            # Add strategy-specific data
            if manual_strategy in ["Bull Put Spread", "Bear Call Spread"]:
                trade_data['short_strike'] = short_strike
                trade_data['long_strike'] = long_strike
            elif manual_strategy == "Iron Condor":
                trade_data['put_short_strike'] = put_short_strike
                trade_data['put_long_strike'] = put_long_strike
                trade_data['call_short_strike'] = call_short_strike
                trade_data['call_long_strike'] = call_long_strike
            
            tracker.add_trade(trade_data)
            st.success(f"Added manual {manual_strategy} trade for {manual_ticker}!")
            st.rerun()
    
    st.divider()
    
    # Existing trade management
    open_trades = tracker.get_open_trades()
    
    if not open_trades:
        st.info("No open trades to manage.")
        return
    
    st.subheader("📋 Manage Existing Trades")
    
    # Select trade to manage
    trade_options = [f"{trade['ticker']} - {trade['strategy']} (ID: {trade['id']})" for trade in open_trades]
    selected_trade_idx = st.selectbox("Select trade to manage:", range(len(trade_options)), format_func=lambda x: trade_options[x])
    
    if selected_trade_idx is not None:
        trade = open_trades[selected_trade_idx]
        evaluation = tracker.evaluate_trade(trade)
        
        st.subheader(f"📋 Trade Details: {trade['ticker']}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Options contracts are for 100 shares, so multiply by 100 for actual dollar amounts
            credit_per_contract = trade.get('credit', 0) * 100
            max_loss_per_contract = trade.get('max_loss', 0) * 100
            
            st.write(f"**Strategy:** {trade['strategy']}")
            st.write(f"**Entry Date:** {trade['entry_date']}")
            st.write(f"**Expiration:** {trade['expiration']}")
            st.write(f"**Credit:** ${credit_per_contract:.0f} (${trade.get('credit', 0):.2f}/share)")
            st.write(f"**Max Loss:** ${max_loss_per_contract:.0f} (${trade.get('max_loss', 0):.2f}/share)")
        
        with col2:
            # Days to expiration
            days_to_exp = (datetime.strptime(trade['expiration'], '%Y-%m-%d') - datetime.now()).days
            st.metric("Days to Expiration", days_to_exp)
            
            # Current recommendation
            rec_color = {"CLOSE": "🔴", "ADJUST": "🟡", "HOLD": "🟢"}
            st.write(f"**Recommendation:** {rec_color.get(evaluation['recommendation'], '⚪')} {evaluation['recommendation']}")
            st.write(f"**Reason:** {evaluation['reason']}")
        
        # Trade actions
        st.subheader("⚡ Trade Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("✅ Close Trade", type="primary"):
                exit_price = st.number_input("Exit Price:", value=0.0, step=0.01, key="exit_price")
                exit_reason = st.text_input("Exit Reason:", key="exit_reason")
                
                if exit_price > 0 and exit_reason:
                    if tracker.close_trade(trade['id'], exit_price, exit_reason):
                        st.success("Trade closed successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to close trade.")
        
        with col2:
            if st.button("🔄 Adjust Trade"):
                st.info("Adjustment features coming soon!")
        
        with col3:
            if st.button("📝 Add Note"):
                st.info("Note-taking features coming soon!")

def render_trade_history(tracker: OptionsTracker):
    """Render trade history and analytics"""
    
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
    """Main entry point for the options tracker UI"""
    render_options_tracker()

def run_options_ui():
    """Alternative entry point for the options tracker UI"""
    render_options_tracker()

# Export the main function
__all__ = ['render_options_tracker', 'run_options_tracker_ui', 'run_options_ui']
