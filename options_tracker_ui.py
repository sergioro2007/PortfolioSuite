"""
🎯 Options Trading Tracker UI
============================

Streamlit interface for the Options Trading Tracker
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from options_tracker import OptionsTracker

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
            f"${stats['total_pnl']:.2f}",
            delta=f"${stats['avg_weekly']:.2f}/week"
        )
    
    with col2:
        st.metric(
            "Win Rate", 
            f"{stats['win_rate']:.1%}",
            delta=f"{stats['winning_trades']}/{stats['total_trades']} trades"
        )
    
    with col3:
        st.metric(
            "Open Trades", 
            len(open_trades),
            delta="Active positions"
        )
    
    with col4:
        weekly_target = 500
        progress = (stats['avg_weekly'] / weekly_target) * 100
        st.metric(
            "Target Progress", 
            f"{progress:.1f}%",
            delta=f"${weekly_target - stats['avg_weekly']:.2f} to target"
        )
    
    # Open trades summary
    if open_trades:
        st.subheader("🔗 Active Trades")
        
        trades_data = []
        for trade in open_trades:
            evaluation = tracker.evaluate_trade(trade)
            
            trades_data.append({
                'Ticker': trade['ticker'],
                'Strategy': trade['strategy'],
                'Entry Date': trade['entry_date'],
                'Expiration': trade['expiration'],
                'Credit': f"${trade.get('credit', 0):.2f}",
                'Max Loss': f"${trade.get('max_loss', 0):.2f}",
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
                st.subheader(f"💼 Suggestion #{i+1}: {suggestion['ticker']}")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Strategy:** {suggestion['strategy']}")
                    st.write(f"**Bias:** {suggestion['bias']} ({suggestion['bullish_prob']:.1%} bullish probability)")
                    st.write(f"**Confidence:** {suggestion['confidence']:.0f}%")
                    
                    # Strategy details
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
                    st.metric("Credit", f"${suggestion['credit']:.2f}")
                    st.metric("Max Loss", f"${suggestion['max_loss']:.2f}")
                    st.metric("Profit Target", f"${suggestion['profit_target']:.2f}")
                
                # OptionStrat link
                optionstrat_url = f"https://optionstrat.com/build/{suggestion['strategy'].lower().replace(' ', '-')}/{suggestion['ticker']}"
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
    
    open_trades = tracker.get_open_trades()
    
    if not open_trades:
        st.info("No open trades to manage.")
        return
    
    # Select trade to manage
    trade_options = [f"{trade['ticker']} - {trade['strategy']} (ID: {trade['id']})" for trade in open_trades]
    selected_trade_idx = st.selectbox("Select trade to manage:", range(len(trade_options)), format_func=lambda x: trade_options[x])
    
    if selected_trade_idx is not None:
        trade = open_trades[selected_trade_idx]
        evaluation = tracker.evaluate_trade(trade)
        
        st.subheader(f"📋 Trade Details: {trade['ticker']}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Strategy:** {trade['strategy']}")
            st.write(f"**Entry Date:** {trade['entry_date']}")
            st.write(f"**Expiration:** {trade['expiration']}")
            st.write(f"**Credit:** ${trade.get('credit', 0):.2f}")
            st.write(f"**Max Loss:** ${trade.get('max_loss', 0):.2f}")
        
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
        history_data.append({
            'ID': trade['id'],
            'Ticker': trade['ticker'],
            'Strategy': trade['strategy'],
            'Entry Date': trade['entry_date'],
            'Exit Date': trade.get('exit_date', ''),
            'Credit': f"${trade.get('credit', 0):.2f}",
            'Exit Price': f"${trade.get('exit_price', 0):.2f}",
            'P&L': f"${trade.get('pnl', 0):.2f}",
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
        pnl = trade.get('pnl', 0)
        
        if strategy not in strategy_stats:
            strategy_stats[strategy] = {'trades': 0, 'total_pnl': 0, 'wins': 0}
        
        strategy_stats[strategy]['trades'] += 1
        strategy_stats[strategy]['total_pnl'] += pnl
        if pnl > 0:
            strategy_stats[strategy]['wins'] += 1
    
    strategy_data = []
    for strategy, stats in strategy_stats.items():
        win_rate = stats['wins'] / stats['trades'] if stats['trades'] > 0 else 0
        avg_pnl = stats['total_pnl'] / stats['trades'] if stats['trades'] > 0 else 0
        
        strategy_data.append({
            'Strategy': strategy,
            'Trades': stats['trades'],
            'Total P&L': f"${stats['total_pnl']:.2f}",
            'Avg P&L': f"${avg_pnl:.2f}",
            'Win Rate': f"{win_rate:.1%}"
        })
    
    if strategy_data:
        strategy_df = pd.DataFrame(strategy_data)
        st.dataframe(strategy_df, use_container_width=True)
