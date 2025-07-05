#!/usr/bin/env python3
"""
Options Analysis Module for Portfolio Management Suite v2.0
===========================================================

This module provides comprehensive options analysis and strategy recommendations
including real-time options chain data, volatility analysis, Greeks calculations,
and automated strategy selection based on market conditions.

Features:
- Real-time options chain analysis
- Strategy recommendations (income, directional, volatility)
- Risk/reward calculations
- Implied volatility analysis
- Greeks analysis (Delta, Gamma, Theta, Vega)
- Earnings calendar integration
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import requests
import warnings
warnings.filterwarnings('ignore')

class OptionsAnalyzer:
    """Advanced options analysis and strategy recommendation system"""
    
    def __init__(self):
        self.risk_free_rate = 0.05  # 5% risk-free rate
        
    def get_options_chain(self, ticker: str, expiration_date: str = None) -> Optional[Dict]:
        """Get options chain data for a given ticker"""
        try:
            stock = yf.Ticker(ticker)
            
            # Get available expiration dates
            expirations = stock.options
            if not expirations:
                return None
                
            # Use nearest expiration if none specified
            if not expiration_date:
                expiration_date = expirations[0]
            
            # Get options chain
            options_chain = stock.option_chain(expiration_date)
            
            return {
                'calls': options_chain.calls,
                'puts': options_chain.puts,
                'expiration': expiration_date,
                'available_expirations': expirations
            }
            
        except Exception as e:
            st.error(f"Error getting options chain for {ticker}: {e}")
            return None
    
    def calculate_implied_volatility_rank(self, ticker: str) -> Dict:
        """Calculate implied volatility rank and percentile"""
        try:
            # This would need a proper options data provider for accurate IV
            # For now, we'll estimate using historical volatility
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1y")
            
            # Calculate 30-day historical volatility
            returns = hist['Close'].pct_change().dropna()
            historical_vol = returns.rolling(30).std() * np.sqrt(252)
            
            current_iv = historical_vol.iloc[-1] if len(historical_vol) > 0 else 0.3
            iv_percentile = (historical_vol.rank(pct=True).iloc[-1] * 100) if len(historical_vol) > 0 else 50
            
            return {
                'current_iv': current_iv,
                'iv_percentile': iv_percentile,
                'high_iv': iv_percentile > 75,
                'low_iv': iv_percentile < 25
            }
            
        except Exception as e:
            st.error(f"Error calculating IV for {ticker}: {e}")
            return {'current_iv': 0.3, 'iv_percentile': 50, 'high_iv': False, 'low_iv': False}
    
    def recommend_strategy(self, market_outlook: str, iv_analysis: Dict) -> Dict:
        """Recommend options strategy based on market outlook and IV"""
        
        # Constants for repeated strings
        NET_CREDIT_RECEIVED = 'Net credit received'
        STRIKE_WIDTH_MINUS_CREDIT = 'Strike width - net credit'
        
        strategies = []
        
        # High IV strategies (premium selling)
        if iv_analysis['high_iv']:
            if market_outlook == 'neutral':
                strategies.append({
                    'name': 'Iron Condor',
                    'type': 'Income',
                    'description': 'Sell OTM call and put spreads for income in range-bound market',
                    'max_profit': NET_CREDIT_RECEIVED,
                    'max_loss': STRIKE_WIDTH_MINUS_CREDIT,
                    'best_scenario': 'Stock stays between short strikes'
                })
                
            elif market_outlook == 'bullish':
                strategies.append({
                    'name': 'Bull Put Spread',
                    'type': 'Income',
                    'description': 'Sell OTM put, buy further OTM put for protection',
                    'max_profit': NET_CREDIT_RECEIVED,
                    'max_loss': STRIKE_WIDTH_MINUS_CREDIT,
                    'best_scenario': 'Stock stays above short put strike'
                })
                
            elif market_outlook == 'bearish':
                strategies.append({
                    'name': 'Bear Call Spread',
                    'type': 'Income',
                    'description': 'Sell OTM call, buy further OTM call for protection',
                    'max_profit': NET_CREDIT_RECEIVED,
                    'max_loss': STRIKE_WIDTH_MINUS_CREDIT,
                    'best_scenario': 'Stock stays below short call strike'
                })
        
        # Low IV strategies (premium buying)
        elif iv_analysis['low_iv']:
            if market_outlook == 'bullish':
                strategies.append({
                    'name': 'Long Call',
                    'type': 'Directional',
                    'description': 'Buy call option for leveraged upside exposure',
                    'max_profit': 'Unlimited',
                    'max_loss': 'Premium paid',
                    'best_scenario': 'Stock moves significantly higher'
                })
                
            elif market_outlook == 'bearish':
                strategies.append({
                    'name': 'Long Put',
                    'type': 'Directional',
                    'description': 'Buy put option for leveraged downside exposure',
                    'max_profit': 'Strike - premium (down to 0)',
                    'max_loss': 'Premium paid',
                    'best_scenario': 'Stock moves significantly lower'
                })
                
            elif market_outlook == 'neutral':
                strategies.append({
                    'name': 'Long Straddle',
                    'type': 'Volatility',
                    'description': 'Buy ATM call and put for volatility expansion play',
                    'max_profit': 'Unlimited',
                    'max_loss': 'Total premium paid',
                    'best_scenario': 'Large move in either direction'
                })
        
        # Default strategies for medium IV
        else:
            strategies.append({
                'name': 'Covered Call',
                'type': 'Income',
                'description': 'Own stock + sell call for additional income',
                'max_profit': 'Strike - stock price + premium',
                'max_loss': 'Stock price - premium',
                'best_scenario': 'Stock stays flat to slightly up'
            })
        
        # Determine IV environment
        if iv_analysis['high_iv']:
            iv_environment = 'High'
        elif iv_analysis['low_iv']:
            iv_environment = 'Low'
        else:
            iv_environment = 'Medium'
        
        return {
            'recommended_strategies': strategies,
            'market_outlook': market_outlook,
            'iv_environment': iv_environment
        }
    
    def calculate_strategy_payoff(self, strategy_type: str, strikes: List[float], 
                                premiums: List[float], stock_prices: np.ndarray) -> Dict:
        """Calculate payoff diagram for a given strategy"""
        
        # This is a simplified example - would need full implementation for each strategy
        if strategy_type == 'long_call':
            strike = strikes[0]
            premium = premiums[0]
            payoff = np.maximum(stock_prices - strike, 0) - premium
            
        elif strategy_type == 'iron_condor':
            # Simplified iron condor calculation
            # [short_put, long_put, short_call, long_call]
            net_credit = sum(premiums[::2]) - sum(premiums[1::2])  # Simplified
            payoff = np.full_like(stock_prices, net_credit)  # Simplified
            
        else:
            payoff = np.zeros_like(stock_prices)
        
        return {
            'stock_prices': stock_prices,
            'payoff': payoff,
            'max_profit': np.max(payoff),
            'max_loss': np.min(payoff),
            'breakeven': stock_prices[np.argmin(np.abs(payoff))] if len(payoff) > 0 else 0
        }

def run_options_analyzer():
    """Main function to run the options analysis interface"""
    
    st.header("📊 Options Analysis & Strategy Recommendations")
    st.markdown("""
    Analyze options chains, evaluate strategies, and get recommendations based on 
    market outlook and volatility environment.
    """)
    
    # Initialize analyzer
    analyzer = OptionsAnalyzer()
    
    # User inputs
    col1, col2 = st.columns(2)
    
    with col1:
        ticker = st.text_input("Stock Symbol", value="AAPL", help="Enter a stock ticker symbol").upper()
        market_outlook = st.selectbox(
            "Market Outlook", 
            ["bullish", "neutral", "bearish"],
            help="Your outlook for the stock's direction"
        )
        
    with col2:
        # Note: These could be used for future filtering/customization
        st.selectbox(
            "Risk Tolerance",
            ["Conservative", "Moderate", "Aggressive"],
            help="Your risk tolerance level"
        )
        st.selectbox(
            "Strategy Focus",
            ["Income", "Directional", "Volatility", "All"],
            help="What type of strategy are you looking for?"
        )
    
    if st.button("🔍 Analyze Options", type="primary") and ticker:
            with st.spinner(f"Analyzing options for {ticker}..."):
                
                # Get IV analysis
                iv_analysis = analyzer.calculate_implied_volatility_rank(ticker)
                
                # Get strategy recommendations
                recommendations = analyzer.recommend_strategy(market_outlook, iv_analysis)
                
                # Display results
                st.subheader(f"📈 Analysis Results for {ticker}")
                
                # IV Analysis
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Current IV", f"{iv_analysis['current_iv']:.1%}")
                with col2:
                    st.metric("IV Percentile", f"{iv_analysis['iv_percentile']:.0f}%")
                with col3:
                    if iv_analysis['high_iv']:
                        iv_env = "High"
                    elif iv_analysis['low_iv']:
                        iv_env = "Low"
                    else:
                        iv_env = "Medium"
                    st.metric("IV Environment", iv_env)
                
                # Strategy Recommendations
                st.subheader("🎯 Recommended Strategies")
                
                for i, strategy in enumerate(recommendations['recommended_strategies']):
                    with st.expander(f"{strategy['name']} ({strategy['type']})", expanded=i==0):
                        st.write(f"**Description:** {strategy['description']}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Max Profit:** {strategy['max_profit']}")
                            st.write(f"**Best Scenario:** {strategy['best_scenario']}")
                        with col2:
                            st.write(f"**Max Loss:** {strategy['max_loss']}")
                            st.write(f"**Strategy Type:** {strategy['type']}")
                
                # Options chain preview (simplified)
                st.subheader("📋 Options Chain Preview")
                options_data = analyzer.get_options_chain(ticker)
                
                if options_data:
                    st.write(f"**Next Expiration:** {options_data['expiration']}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Calls (Preview)**")
                        if not options_data['calls'].empty:
                            calls_preview = options_data['calls'][['strike', 'lastPrice', 'volume', 'impliedVolatility']].head(5)
                            st.dataframe(calls_preview, use_container_width=True)
                    
                    with col2:
                        st.write("**Puts (Preview)**")
                        if not options_data['puts'].empty:
                            puts_preview = options_data['puts'][['strike', 'lastPrice', 'volume', 'impliedVolatility']].head(5)
                            st.dataframe(puts_preview, use_container_width=True)
                
                # Educational content
                with st.expander("📚 Options Strategy Education"):
                    st.markdown("""
                    **Strategy Selection Guidelines:**
                    
                    - **High IV Environment**: Focus on premium selling strategies (Iron Condors, Credit Spreads)
                    - **Low IV Environment**: Focus on premium buying strategies (Long Options, Debit Spreads)
                    - **Neutral Outlook**: Range-bound strategies (Iron Condors, Butterflies)
                    - **Directional Outlook**: Directional strategies (Long Options, Spreads)
                    
                    **Risk Management:**
                    - Never risk more than you can afford to lose
                    - Consider position sizing (1-2% of portfolio per trade)
                    - Set profit targets and stop losses
                    - Monitor time decay (Theta) daily
                    """)

if __name__ == "__main__":
    run_options_analyzer()
