"""
⚡ Tactical Momentum Portfolio Tracker Module
============================================

Extracted tactical momentum functionality for the multi-feature portfolio suite.
This module contains all the tactical momentum analysis, market health monitoring,
and defensive cash allocation features from the original application.
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
import json
import time
from typing import Dict, List, Tuple, Optional
from bs4 import BeautifulSoup
import re
import pickle
import os
import warnings
import logging

# Suppress warnings and reduce verbose output
warnings.filterwarnings('ignore')
logging.getLogger("yfinance").setLevel(logging.ERROR)
logging.getLogger("requests").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)

# Constants
DEFENSIVE_ETFS = ['XLP', 'XLV', 'SH', 'PSQ']
VIX_THRESHOLD = 20
BREADTH_THRESHOLD = 60
DROP_THRESHOLD = -3.0  # Exit if drop > 3%
WATCH_THRESHOLD = -1.5  # Watch if drop > 1.5%
MOMENTUM_THRESHOLD = 2.0  # Strong momentum if gain > 2%
MIN_MARKET_CAP = 5e9  # $5B
WEEKLY_TARGET = 2.0  # 2% weekly target

def run_tactical_tracker():
    """Main function to run the tactical momentum tracker interface"""
    
    st.markdown("## ⚡ Tactical Momentum Portfolio Tracker")
    st.markdown("*Identify and manage tactical stock/ETF positions based on momentum and market health*")
    
    # Initialize tracker
    tracker = PortfolioTracker()
    
    # Sidebar configuration - matching original layout
    st.sidebar.header("📊 Portfolio Configuration")
    
    # Discovery mode selection - matching original
    discovery_mode = st.sidebar.radio(
        "Ticker Selection Mode:",
        ["🤖 Auto-Discovery", "📝 Manual Input"],
        index=0,  # Default to Auto-Discovery
        help="Auto-discovery finds qualifying tickers automatically"
    )
    
    if discovery_mode == "📝 Manual Input":
        # Manual ticker input (original functionality)
        default_tickers = "AAPL,MSFT,NVDA,GOOGL,AMZN,META,TSLA,SPY,QQQ,IWM"
        tickers_input = st.sidebar.text_area(
            "Enter tickers (comma separated):",
            value=default_tickers,
            height=100,
            help="Enter up to 10 tickers with market cap > $5B"
        )
        use_auto_discovery = False
    else:
        st.sidebar.info("🔍 Auto-discovery will scan for qualifying momentum stocks")
        tickers_input = ""
        use_auto_discovery = True
    
    portfolio_size = st.sidebar.slider("Max Portfolio Size", 5, 15, 10)
    
    # Add defensive allocation toggle
    defensive_mode = st.sidebar.checkbox("Enable Defensive Mode", help="Allocate 10-20% to defensive ETFs when market conditions deteriorate")
    
    # Discovery settings for auto mode
    if use_auto_discovery:
        st.sidebar.subheader("🎯 Discovery Settings")
        min_rs_score = st.sidebar.slider("Min RS Score", 20, 80, 25, help="Minimum relative strength score (0-100 scale)")
        min_weekly_target = st.sidebar.slider("Min Weekly Target (%)", 0.5, 3.0, 1.0, help="Minimum average weekly return")
    else:
        # Manual mode settings
        min_rs_score = st.sidebar.slider("Min RS Score", 20, 100, 30, help="Minimum relative strength score (higher = more selective)")
        min_weekly_target = st.sidebar.slider("Min Weekly Return Target (%)", 0.5, 5.0, 1.5, 0.1, help="Minimum average weekly return requirement")
    
    st.sidebar.markdown("### 🎯 Allocation Settings")
    
    strong_buy_weight = st.sidebar.slider("Strong Buy Weight (%)", 8, 20, 12, 1,
                                         help="Allocation percentage for strong buy positions")
    
    moderate_buy_weight = st.sidebar.slider("Moderate Buy Weight (%)", 3, 12, 6, 1,
                                           help="Allocation percentage for moderate buy positions")
    
    allow_defensive_cash = st.sidebar.checkbox("Allow Defensive Cash Allocation", True,
                                              help="Enable automatic cash allocation based on market conditions")
    
    # Main content - Button to analyze
    if st.button("🔄 Analyze Portfolio", type="primary"):
        with st.spinner("🔍 Analyzing market conditions..."):
            
            # Get market health
            market_health = tracker.get_market_health()
            
            # Display market health
            display_market_health(market_health)
            
            # Initialize variables
            discovered_tickers = []
            
            # Ticker discovery and analysis
            if use_auto_discovery:
                # Auto-discovery mode
                results = run_screening(tracker, portfolio_size, min_rs_score, min_weekly_target, market_health)
            else:
                # Manual ticker analysis (original logic)
                ticker_list = [t.strip().upper() for t in tickers_input.split(',') if t.strip()]
                
                st.header("📊 Manual Ticker Analysis")
                st.info(f"🎯 Analyzing {len(ticker_list)} specified tickers: {', '.join(ticker_list)}")
                
                with st.spinner("📈 Analyzing specified tickers..."):
                    results = analyze_manual_tickers(tracker, ticker_list, min_rs_score, min_weekly_target)
                
            if results:
                # Generate recommendations
                recommendations = tracker.generate_portfolio_recommendations(
                    results, portfolio_size, min_rs_score, min_weekly_target, market_health
                )
                
                # Display results
                display_recommendations(recommendations, strong_buy_weight, moderate_buy_weight, 
                                      market_health, allow_defensive_cash, tracker)
            else:
                st.warning("No qualifying stocks found with current screening criteria.")


def analyze_manual_tickers(tracker, ticker_list: List[str], 
                          min_rs_score: float, min_weekly_target: float) -> List[Dict]:
    """Analyze manually specified tickers - matching original app logic"""
    results = []
    progress_bar = st.progress(0)
    
    for i, ticker in enumerate(ticker_list):
        try:
            # Update progress
            progress_bar.progress((i + 1) / len(ticker_list))
            
            # Use lenient defaults for initial analysis (matching original app)
            # The stricter filtering will happen later in get_top_picks()
            result = tracker.analyze_ticker_momentum(ticker, 25, 1.0)
            
            if result:
                # Add momentum score calculation
                momentum_score = (
                    result['avg_weekly_return'] * 0.4 +  # 40% weight on avg weekly return
                    result['rs_score'] * 0.3 +  # 30% weight on relative strength
                    result['weeks_above_target'] * 5 * 0.2 +  # 20% weight on consistency 
                    (1 if result['daily_change'] > 0 else -2) * 0.1  # 10% weight on recent momentum
                )
                result['momentum_score'] = momentum_score
                results.append(result)
                
        except Exception as e:
            st.warning(f"Error analyzing {ticker}: {e}")
            continue
    
    progress_bar.empty()
    
    # Filter to only qualifying results
    qualified_results = [r for r in results if r.get('meets_criteria', False)]
    
    if qualified_results:
        st.success(f"✅ {len(qualified_results)} out of {len(results)} tickers passed screening")
    else:
        st.warning(f"⚠️ None of the {len(results)} analyzed tickers passed screening criteria")
    
    return qualified_results


class PortfolioTracker:
    """
    Portfolio tracker for tactical momentum analysis and market health monitoring.
    
    This class handles momentum screening, defensive allocation, and market health
    analysis for the tactical portfolio management strategy.
    """
    def __init__(self):
        self.portfolio = {}
        self.market_data = {}
        self.results_file = "portfolio_results.pkl"
    
    def get_market_health(self) -> Dict:
        """Calculate comprehensive market health indicators for automatic defensive mode"""
        try:
            # Get VIX data (fear gauge)
            vix = yf.Ticker("^VIX")
            vix_data = vix.history(period="10d")
            current_vix = vix_data['Close'].iloc[-1] if not vix_data.empty else 20
            vix_ma5 = vix_data['Close'].rolling(5).mean().iloc[-1] if len(vix_data) >= 5 else current_vix
            
            # Get SPY data for trend analysis
            spy = yf.Ticker("SPY")
            spy_data = spy.history(period="100d")
            if not spy_data.empty:
                current_spy = spy_data['Close'].iloc[-1]
                ma_20 = spy_data['Close'].rolling(20).mean().iloc[-1]
                ma_50 = spy_data['Close'].rolling(50).mean().iloc[-1]
                spy_above_ma20 = current_spy > ma_20
                spy_above_ma50 = current_spy > ma_50
                
                # Calculate recent volatility
                daily_returns = spy_data['Close'].pct_change().dropna()
                recent_volatility = daily_returns.tail(10).std() * 100
                
                # Calculate momentum (10-day vs 30-day moving averages)
                ma_10 = spy_data['Close'].rolling(10).mean().iloc[-1]
                ma_30 = spy_data['Close'].rolling(30).mean().iloc[-1]
                momentum_positive = ma_10 > ma_30
            else:
                spy_above_ma20 = spy_above_ma50 = momentum_positive = True
                recent_volatility = 1.0
                
            # Enhanced breadth calculation (proxy using sector performance)
            try:
                sectors = ['XLK', 'XLF', 'XLV', 'XLE', 'XLI']  # Tech, Finance, Health, Energy, Industrial
                sector_strength = 0
                
                for sector in sectors:
                    sector_data = yf.Ticker(sector).history(period="20d")
                    if not sector_data.empty and len(sector_data) >= 10:
                        sector_current = sector_data['Close'].iloc[-1]
                        sector_ma10 = sector_data['Close'].rolling(10).mean().iloc[-1]
                        if sector_current > sector_ma10:
                            sector_strength += 1
                            
                breadth_percentage = (sector_strength / len(sectors)) * 100
            except:
                breadth_percentage = 60  # Neutral default
            
            # Determine market regime based on multiple factors
            defensive_signals = 0
            max_signals = 6
            
            # Signal 1: High VIX (fear)
            if current_vix > VIX_THRESHOLD:
                defensive_signals += 1
                
            # Signal 2: Rising VIX trend
            if current_vix > vix_ma5 * 1.1:
                defensive_signals += 1
                
            # Signal 3: SPY below key moving averages
            if not spy_above_ma20:
                defensive_signals += 1
                
            # Signal 4: Poor breadth
            if breadth_percentage < BREADTH_THRESHOLD:
                defensive_signals += 1
                
            # Signal 5: High volatility
            if recent_volatility > 2.5:  # >2.5% daily volatility is concerning
                defensive_signals += 1
                
            # Signal 6: Negative momentum
            if not momentum_positive:
                defensive_signals += 1
            
            # Calculate defensive score (0-100)
            defensive_score = (defensive_signals / max_signals) * 100
            
            # Determine market regime
            if defensive_score >= 66:  # 4+ signals
                market_regime = "HIGHLY_DEFENSIVE"
            elif defensive_score >= 50:  # 3+ signals  
                market_regime = "DEFENSIVE"
            elif defensive_score >= 33:  # 2+ signals
                market_regime = "CAUTIOUS"
            else:
                market_regime = "AGGRESSIVE"
            
            return {
                'vix': current_vix,
                'vix_trend': 'Rising' if current_vix > vix_ma5 * 1.05 else 'Falling',
                'breadth': breadth_percentage,
                'spy_above_ma20': spy_above_ma20,
                'spy_above_ma50': spy_above_ma50,
                'volatility': recent_volatility,
                'momentum_positive': momentum_positive,
                'defensive_signals': defensive_signals,
                'defensive_score': defensive_score,
                'market_regime': market_regime,
                'is_defensive': defensive_score >= 50,
                'auto_adjust_needed': defensive_score >= 70  # Only auto-adjust in high stress situations
            }
        except Exception as e:
            st.error(f"Error getting market health: {e}")
            return {'vix': 0, 'breadth': 100, 'spy_above_ma': True, 'is_defensive': False}
    
    def calculate_simple_allocation(self, strong_buys: List[Dict], moderate_buys: List[Dict], 
                                   strong_buy_weight: float = 12.0, moderate_buy_weight: float = 6.0, 
                                   market_health: Dict = None, allow_cash: bool = True) -> Dict:
        """Calculate simple two-tier allocation with optional cash in defensive conditions"""
        if not strong_buys and not moderate_buys:
            return {
                'allocations': [],
                'total_allocated': 0,
                'remaining_cash': 100,
                'num_positions': 0,
                'was_scaled': False,
                'scale_factor': 1.0,
                'raw_total': 0,
                'defensive_cash': 100,
                'market_regime': market_health.get('market_regime', 'UNKNOWN') if market_health else 'UNKNOWN'
            }
        
        # Determine if we should hold defensive cash based on market conditions
        defensive_cash_pct = 0
        market_regime = market_health.get('market_regime', 'AGGRESSIVE') if market_health else 'AGGRESSIVE'
        
        if allow_cash and market_health:
            if market_regime == "HIGHLY_DEFENSIVE":
                defensive_cash_pct = 30  # Hold 30% cash in extreme conditions
            elif market_regime == "DEFENSIVE":
                defensive_cash_pct = 15  # Hold 15% cash in defensive conditions
            elif market_regime == "CAUTIOUS":
                defensive_cash_pct = 5   # Hold small cash buffer
        
        # Calculate target allocation percentage for stocks
        target_stock_allocation = 100 - defensive_cash_pct
        
        # Convert weights to integers for clean allocations
        strong_weight = int(round(strong_buy_weight))
        moderate_weight = int(round(moderate_buy_weight))
        
        # Calculate initial allocation
        initial_allocations = []
        initial_total = 0
        
        # Add strong buys
        for pick in strong_buys:
            initial_allocations.append({
                'ticker': pick['ticker'],
                'category': 'Strong Buy',
                'allocation': strong_weight,
                'momentum_score': pick['momentum_score'],
                'weekly_return': pick['avg_weekly_return'],
                'priority': 1  # Higher priority
            })
            initial_total += strong_weight
        
        # Add moderate buys
        for pick in moderate_buys:
            initial_allocations.append({
                'ticker': pick['ticker'],
                'category': 'Moderate Buy',
                'allocation': moderate_weight,
                'momentum_score': pick['momentum_score'],
                'weekly_return': pick['avg_weekly_return'],
                'priority': 2  # Lower priority
            })
            initial_total += moderate_weight
        
        # Adjust to target stock allocation (not necessarily 100%)
        difference = target_stock_allocation - initial_total
        was_scaled = difference != 0
        
        if difference != 0:
            # Sort by priority (strong buys first) then by momentum score
            sorted_allocations = sorted(initial_allocations, 
                                      key=lambda x: (x['priority'], -x['momentum_score']))
            
            if difference > 0:
                # Need to add more allocation - distribute among highest priority/momentum
                for i in range(abs(difference)):
                    idx = i % len(sorted_allocations)
                    sorted_allocations[idx]['allocation'] += 1
            else:
                # Need to reduce allocation - take from lowest priority/momentum
                sorted_allocations.reverse()  # Start from lowest priority
                for i in range(abs(difference)):
                    idx = i % len(sorted_allocations)
                    if sorted_allocations[idx]['allocation'] > 1:  # Don't go below 1%
                        sorted_allocations[idx]['allocation'] -= 1
                    else:
                        # If we can't reduce this one, try the next
                        continue
            
            # Update the allocations
            for i, alloc in enumerate(sorted_allocations):
                initial_allocations[i] = alloc
        
        # Remove priority field for clean output
        final_allocations = []
        total_allocated = 0
        for alloc in initial_allocations:
            clean_alloc = {
                'ticker': alloc['ticker'],
                'category': alloc['category'],
                'allocation': alloc['allocation'],
                'momentum_score': alloc['momentum_score'],
                'weekly_return': alloc['weekly_return']
            }
            final_allocations.append(clean_alloc)
            total_allocated += alloc['allocation']
        
        return {
            'allocations': final_allocations,
            'total_allocated': total_allocated,
            'remaining_cash': defensive_cash_pct,  # Defensive cash allocation
            'num_positions': len(final_allocations),
            'was_scaled': was_scaled,
            'scale_factor': total_allocated / initial_total if initial_total > 0 else 1.0,
            'raw_total': initial_total,
            'defensive_cash': defensive_cash_pct,
            'market_regime': market_regime,
            'target_stock_allocation': target_stock_allocation
        }
    
    def generate_portfolio_recommendations(self, results: List[Dict], portfolio_size: int = 15,
                                         min_rs_score: float = 30, min_weekly_target: float = 1.5,
                                         market_health: Dict = None) -> Dict:
        """Generate portfolio recommendations - matching original logic exactly"""
        
        # Use get_top_picks to get properly sorted results (momentum score descending)
        top_picks = self.get_top_picks(results, portfolio_size, min_rs_score, min_weekly_target)
        
        # Separate into strong buys and moderate buys using same logic as original
        strong_buys = [r for r in top_picks if r['momentum_score'] > 15 and r['avg_weekly_return'] > 2.0]
        moderate_buys = [r for r in top_picks if r['momentum_score'] > 10 and r not in strong_buys]
        watch_list = [r for r in top_picks if r not in strong_buys and r not in moderate_buys]

        return {
            'top_picks': top_picks,  # This is the key - return the ranked top picks
            'strong_buys': strong_buys,
            'moderate_buys': moderate_buys,
            'watch_list': watch_list,
            'all_qualified': top_picks,
            'total_screened': len(results),
            'total_qualified': len(top_picks)
        }
    
    def passes_filters(self, result: Dict, min_rs_score: float = 30, min_weekly_target: float = 1.5) -> bool:
        """Check if a ticker passes tactical momentum filters with user-defined thresholds"""
        
        # First check user-defined thresholds
        rs_score = result.get('rs_score', 0)
        avg_weekly_return_pct = result.get('avg_weekly_return', 0)
        
        # Handle None values
        if rs_score is None:
            rs_score = 0
        if avg_weekly_return_pct is None:
            avg_weekly_return_pct = 0
        
        # Apply user-defined minimum thresholds first
        if rs_score < min_rs_score:
            result['qualification_reason'] = f"RS Score too low: {rs_score:.1f} < {min_rs_score}"
            return False
            
        if avg_weekly_return_pct < min_weekly_target:
            # Allow exceptions for special momentum patterns BEFORE rejecting
            # Check for high-quality patterns that can bypass weekly threshold
            
            # Get weekly data for special pattern checks
            weekly_returns_pct = [r * 100 for r in result.get('weekly_returns', [])]
            if not weekly_returns_pct or len(weekly_returns_pct) != 4:
                result['qualification_reason'] = f"Weekly return too low: {avg_weekly_return_pct:.1f}% < {min_weekly_target}%"
                return False
                
            max_weekly_return = max(weekly_returns_pct)
            positive_weeks = sum(1 for r in weekly_returns_pct if r > 0)
            weeks_above_3pct = sum(1 for r in weekly_returns_pct if r > 3.0)
            total_return = sum(weekly_returns_pct)
            
            # Exception 1: High RS Quality Stock (META pattern) - RS >55 AND avg >0.8% AND 2+ positive AND max >6%
            if rs_score >= 55 and avg_weekly_return_pct >= 0.8 and positive_weeks >= 2 and max_weekly_return >= 6.0:
                result['qualification_reason'] = f"High-quality momentum: RS {rs_score:.1f}, avg {avg_weekly_return_pct:.1f}%, max {max_weekly_return:.1f}%"
                return True
            
            # Exception 2: Explosive Single Week (META/Tech pattern) - Max >7% AND total >3% AND 2+ positive
            if max_weekly_return >= 7.0 and total_return >= 3.0 and positive_weeks >= 2:
                result['qualification_reason'] = f"Explosive week: max {max_weekly_return:.1f}%, total {total_return:.1f}%"
                return True
            
            # Exception 3: Sector/Energy Play (WMB pattern) - 1+ weeks >3% AND max >3% AND positive weeks >=2
            if weeks_above_3pct >= 1 and max_weekly_return >= 3.0 and positive_weeks >= 2 and rs_score >= 40:
                result['qualification_reason'] = f"Sector play: max {max_weekly_return:.1f}%, {weeks_above_3pct}/4 weeks >3%"
                return True
            
            # No exceptions apply - reject for low weekly return
            result['qualification_reason'] = f"Weekly return too low: {avg_weekly_return_pct:.1f}% < {min_weekly_target}%"
            return False
        
        # If user thresholds are met, proceed with additional tactical filters
        weekly_returns_pct = [r * 100 for r in result.get('weekly_returns', [])]
        weeks_above_2pct = result.get('weeks_above_target', 0)
        
        if not weekly_returns_pct or len(weekly_returns_pct) != 4:
            return False
        
        # Enhanced metrics for better pattern recognition
        max_weekly_return = max(weekly_returns_pct)
        min_weekly_return = min(weekly_returns_pct)
        positive_weeks = sum(1 for r in weekly_returns_pct if r > 0)
        weeks_above_1pct = sum(1 for r in weekly_returns_pct if r > 1.0)
        weeks_above_3pct = sum(1 for r in weekly_returns_pct if r > 3.0)
        weeks_above_5pct = sum(1 for r in weekly_returns_pct if r > 5.0)
        strong_negative_weeks = sum(1 for r in weekly_returns_pct if r < -4.0)  # Relaxed from -3%
        total_return = sum(weekly_returns_pct)
        
        # Store qualification reason for debugging
        result['qualification_reason'] = ''
        
        # ENHANCED qualification paths for high-confidence momentum (ordered by priority):
        
        # 1. Elite Momentum: 3+ weeks >2% AND avg >2.5% AND min week >-2%
        if weeks_above_2pct >= 3 and avg_weekly_return_pct >= 2.5 and min_weekly_return > -2.0:
            result['qualification_reason'] = f"Elite momentum: {weeks_above_2pct}/4 weeks >2%, avg {avg_weekly_return_pct:.1f}%"
            return True
        
        # 2. Strong Leader: 2+ weeks >2% AND avg >2.0% AND max week >4% AND min week >-3%
        if weeks_above_2pct >= 2 and avg_weekly_return_pct >= 2.0 and max_weekly_return >= 4.0 and min_weekly_return > -3.0:
            result['qualification_reason'] = f"Strong leader: {weeks_above_2pct}/4 weeks >2%, avg {avg_weekly_return_pct:.1f}%, max {max_weekly_return:.1f}%"
            return True
        
        # 3. Consistent Performer: 3+ weeks >1% AND avg >1.8% AND total >7% AND min week >-2%
        if weeks_above_1pct >= 3 and avg_weekly_return_pct >= 1.8 and total_return >= 7.0 and min_weekly_return > -2.0:
            result['qualification_reason'] = f"Consistent performer: {weeks_above_1pct}/4 weeks >1%, avg {avg_weekly_return_pct:.1f}%"
            return True
        
        # 4. Explosive Breakout: Max week >6% AND avg >1.5% AND 3+ positive weeks
        if max_weekly_return >= 6.0 and avg_weekly_return_pct >= 1.5 and positive_weeks >= 3:
            result['qualification_reason'] = f"Explosive breakout: max {max_weekly_return:.1f}%, avg {avg_weekly_return_pct:.1f}%"
            return True
        
        # 5. Sustained Growth: 4+ weeks >1% AND avg >1.5% AND total >6%
        if weeks_above_1pct >= 4 and avg_weekly_return_pct >= 1.5 and total_return >= 6.0:
            result['qualification_reason'] = f"Sustained growth: {weeks_above_1pct}/4 weeks >1%, avg {avg_weekly_return_pct:.1f}%"
            return True
        
        # 6. High Velocity: 2+ weeks >3% AND avg >1.5% AND min week >-4%
        if weeks_above_target := sum(1 for r in weekly_returns_pct if r > 3.0):
            if weeks_above_target >= 2 and avg_weekly_return_pct >= 1.5 and min_weekly_return > -4.0:
                result['qualification_reason'] = f"High velocity: {weeks_above_target}/4 weeks >3%, avg {avg_weekly_return_pct:.1f}%"
                return True
        
        # 7. Strong Momentum: 2+ weeks >2% AND avg >1.5% AND total >5% AND min week >-3%
        if weeks_above_2pct >= 2 and avg_weekly_return_pct >= 1.5 and total_return >= 5.0 and min_weekly_return > -3.0:
            result['qualification_reason'] = f"Strong momentum: {weeks_above_2pct}/4 weeks >2%, avg {avg_weekly_return_pct:.1f}%"
            return True
        
        # 8. Quality Growth: 3+ positive weeks AND avg >1.5% AND max week >3% AND strong negative weeks = 0
        if positive_weeks >= 3 and avg_weekly_return_pct >= 1.5 and max_weekly_return >= 3.0 and strong_negative_weeks == 0:
            result['qualification_reason'] = f"Quality growth: {positive_weeks}/4 positive weeks, avg {avg_weekly_return_pct:.1f}%"
            return True
        
        # 9. RS Leader: High relative strength + decent performance (for quality stocks like NVDA, META)
        if rs_score >= 45 and avg_weekly_return_pct >= 1.2 and positive_weeks >= 2 and min_weekly_return > -5.0:
            result['qualification_reason'] = f"RS leader: RS {rs_score:.1f}, avg {avg_weekly_return_pct:.1f}%, {positive_weeks}/4 positive"
            return True
        
        # 10. Sector Strength: Good total return + limited downside (for energy, materials)
        if total_return >= 4.0 and min_weekly_return > -4.0 and positive_weeks >= 2 and max_weekly_return >= 2.5:
            result['qualification_reason'] = f"Sector strength: total {total_return:.1f}%, max {max_weekly_return:.1f}%, min {min_weekly_return:.1f}%"
            return True
        
        # 11. Momentum Emergence: 1+ weeks >3% AND avg >1.0% AND total >3% AND max week >4%
        weeks_above_3pct_local = sum(1 for r in weekly_returns_pct if r > 3.0)
        if weeks_above_3pct_local >= 1 and avg_weekly_return_pct >= 1.0 and total_return >= 3.0 and max_weekly_return >= 4.0:
            result['qualification_reason'] = f"Momentum emergence: {weeks_above_3pct_local}/4 weeks >3%, avg {avg_weekly_return_pct:.1f}%"
            return True
        
        # Didn't qualify - store reason
        if avg_weekly_return_pct < -1.0:
            result['qualification_reason'] = f"Too negative: avg {avg_weekly_return_pct:.1f}%"
        elif max_weekly_return < 2.0:
            result['qualification_reason'] = f"No significant moves: max {max_weekly_return:.1f}%"
        elif strong_negative_weeks >= 3:
            result['qualification_reason'] = f"Too many disasters: {strong_negative_weeks}/4 weeks <-4%"
        elif positive_weeks <= 1:
            result['qualification_reason'] = f"Too few positive weeks: {positive_weeks}/4"
        else:
            result['qualification_reason'] = f"Weak signals: {weeks_above_2pct}/4 weeks >2%, avg {avg_weekly_return_pct:.1f}%"
        
        return False
    
    def get_weekly_returns(self, ticker: str, weeks: int = 5) -> Optional[List[float]]:
        """Get weekly returns for a ticker using proper weekly grouping"""
        try:
            end = datetime.today()
            start = end - timedelta(days=weeks * 7 + 7)  # Add extra week for safety
            df = yf.download(ticker, start=start, end=end, interval='1d', auto_adjust=True)
            if df.empty or len(df) < 7:
                return None
                
            # Extract just the Close prices as a Series
            if isinstance(df.columns, pd.MultiIndex):
                # For multiindex columns (when downloading single ticker), get the Close column
                close_prices = df[('Close', ticker)]
            else:
                # For simple columns
                close_prices = df['Close']
                
            # Group by ISO calendar week
            close_df = close_prices.to_frame(name='Close')
            close_df['Week'] = close_prices.index.to_series().dt.isocalendar().week
            weekly_close = close_df.groupby('Week')['Close'].last()
            
            # Calculate returns and convert to list properly
            returns_series = weekly_close.pct_change().dropna()
            returns = returns_series.tolist()
            
            return returns[-4:] if len(returns) >= 4 else returns  # last 4 weeks
        except Exception:
            return None

    def analyze_ticker_momentum(self, ticker: str, min_rs_score: float = 30, min_weekly_target: float = 1.5) -> Optional[Dict]:
        """Analyze momentum for a single ticker with robust error handling"""
        try:
            # Create ticker object
            stock = yf.Ticker(ticker)
            
            # Try to get basic info first
            try:
                info = stock.info
                market_cap = info.get('marketCap', 0)
                name = info.get('shortName', ticker)
            except Exception:
                market_cap = 1e9  # Default to $1B
                name = ticker
            
            # Try to get price data
            try:
                hist = stock.history(period="1mo")  # 1 month of data
                if hist.empty:
                    return None
                
                current_price = float(hist['Close'].iloc[-1])
                
                # Simple calculations
                if len(hist) >= 2:
                    prev_price = float(hist['Close'].iloc[-2])
                    daily_change = ((current_price - prev_price) / prev_price) * 100
                else:
                    daily_change = 0
                
                # Simple weekly return calculation
                if len(hist) >= 7:
                    week_ago_price = float(hist['Close'].iloc[-7])
                    weekly_return = ((current_price - week_ago_price) / week_ago_price) * 100
                else:
                    weekly_return = 0
                    
                # Get proper weekly returns using fixed method
                weekly_returns = self.get_weekly_returns(ticker, 4)
                if weekly_returns and len(weekly_returns) > 0:
                    weeks_above_target = sum(1 for ret in weekly_returns if ret >= min_weekly_target/100)  # Use parameter
                    avg_weekly_return = np.mean(weekly_returns) * 100  # Convert to percentage
                    weekly_returns_display = weekly_returns
                else:
                    weeks_above_target = 1 if weekly_return >= min_weekly_target else 0
                    avg_weekly_return = weekly_return
                    weekly_returns_display = [weekly_return/100]  # Convert to decimal for display
                
                # Calculate a more realistic RS score
                if len(hist) >= 20:
                    # Use 20-day moving average and longer period for better RS calculation
                    ma_20 = hist['Close'].rolling(20).mean().iloc[-1]
                    # RS as percentage above/below 20-day MA, scaled to 0-100 range
                    price_vs_ma = ((current_price - ma_20) / ma_20) * 100
                    # Normalize to 0-100 scale where 50 = at MA, >50 = above MA
                    rs_score = max(0, min(100, 50 + price_vs_ma * 2))
                elif len(hist) >= 10:
                    # Fallback to 10-day MA
                    ma_10 = hist['Close'].rolling(10).mean().iloc[-1]
                    price_vs_ma = ((current_price - ma_10) / ma_10) * 100
                    rs_score = max(0, min(100, 50 + price_vs_ma * 3))
                else:
                    rs_score = 50  # Neutral score if insufficient data
                
                result = {
                    'ticker': ticker,
                    'name': name,
                    'current_price': current_price,
                    'market_cap': market_cap,
                    'daily_change': daily_change,
                    'weekly_returns': weekly_returns_display,
                    'weeks_above_target': weeks_above_target,
                    'avg_weekly_return': avg_weekly_return,
                    'rs_score': rs_score,
                    'meets_criteria': False,  # Will be set by passes_filters
                    'qualification_reason': ''  # Will be set by passes_filters
                }
                
                # Apply enhanced filtering logic with user parameters
                meets_criteria = self.passes_filters(result, min_rs_score, min_weekly_target)
                result['meets_criteria'] = meets_criteria
                
                return result
                
            except Exception:
                return None
                
        except Exception:
            return None
    
    def get_position_status(self, daily_change: float) -> Tuple[str, str]:
        """Determine position status based on daily change"""
        if daily_change <= DROP_THRESHOLD:
            return "🚨 EXIT", "danger"
        elif daily_change <= WATCH_THRESHOLD:
            return "⚠️ WATCH", "warning"
        elif daily_change >= MOMENTUM_THRESHOLD:
            return "🚀 STRONG", "success"
        else:
            return "✅ HOLD", "info"
    
    def get_top_picks(self, results: List[Dict], count: int = 10, min_rs_score: float = 30, min_weekly_target: float = 1.5) -> List[Dict]:
        """Select top picks based on momentum score - only considers strictly filtered tickers"""
        if not results:
            return []
            
        # First, apply strict tactical filters - only score qualified tickers
        qualified_results = []
        for result in results:
            # Set meets_criteria based on passes_filters
            result['meets_criteria'] = self.passes_filters(result, min_rs_score, min_weekly_target)
            if result['meets_criteria']:
                qualified_results.append(result)
        
        if not qualified_results:
            return []
            
        # Calculate momentum score for each qualified ticker
        scored_results = []
        for result in qualified_results:
            # Momentum score combines multiple factors
            momentum_score = (
                result['avg_weekly_return'] * 0.4 +  # 40% weight on avg weekly return
                result['rs_score'] * 0.3 +  # 30% weight on relative strength
                result['weeks_above_target'] * 5 * 0.2 +  # 20% weight on consistency 
                (1 if result['daily_change'] > 0 else -2) * 0.1  # 10% weight on recent momentum
            )
            
            result_copy = result.copy()
            result_copy['momentum_score'] = momentum_score
            scored_results.append(result_copy)
        
        # Sort by momentum score descending
        scored_results.sort(key=lambda x: x['momentum_score'], reverse=True)
        
        return scored_results[:count]


def display_market_health(market_health: Dict):
    """Display market health indicators"""
    
    st.subheader("🌡️ Market Health & Automatic Defensive Mode")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        vix = market_health.get('vix', 0)
        vix_trend = market_health.get('vix_trend', 'Neutral')
        st.metric("VIX (Fear)", f"{vix:.1f}", 
                 delta=vix_trend, delta_color="inverse")
        
    with col2:
        breadth = market_health.get('breadth', 0)
        st.metric("Market Breadth", f"{breadth:.0f}%")
        
    with col3:
        spy_status = "Above MA20" if market_health.get('spy_above_ma20', True) else "Below MA20"
        st.metric("SPY Trend", spy_status)
        
    with col4:
        volatility = market_health.get('volatility', 1.0)
        st.metric("Volatility", f"{volatility:.1f}%")
        
    with col5:
        regime = market_health.get('market_regime', 'AGGRESSIVE')
        defensive_score = market_health.get('defensive_score', 0)
        
        # Color code based on regime
        if regime == "HIGHLY_DEFENSIVE":
            regime_color = "🔴"
        elif regime == "DEFENSIVE":
            regime_color = "🟠"
        elif regime == "CAUTIOUS":
            regime_color = "🟡"
        else:
            regime_color = "🟢"
            
        st.metric("Auto Mode", f"{regime_color} {regime}", 
                 delta=f"{defensive_score:.0f}% defensive signals")
    
    # Enhanced market alert with regime information
    if market_health.get('auto_adjust_needed', False):
        regime = market_health.get('market_regime', 'AGGRESSIVE')
        
        if regime == "HIGHLY_DEFENSIVE":
            st.error(f"""
            🚨 **HIGHLY DEFENSIVE MODE ACTIVATED**  
            Market conditions suggest high caution and defensive positioning.
            """)
        elif regime == "DEFENSIVE":
            st.warning(f"""
            ⚠️ **DEFENSIVE MODE ACTIVATED**  
            Market conditions suggest cautious positioning.
            """)
        elif regime == "CAUTIOUS":
            st.info(f"""
            ⚡ **CAUTIOUS MODE**  
            Market conditions suggest balanced approach.
            """)
        else:
            st.success(f"""
            🚀 **AGGRESSIVE MODE**  
            Market conditions favor full momentum strategy.
            """)


def run_screening(tracker: PortfolioTracker, portfolio_size: int, min_rs_score: float, 
                 min_weekly_target: float, market_health: Dict) -> List[Dict]:
    """Run screening process with automatic ticker discovery"""
    
    st.header("🤖 Automated Ticker Discovery")
    
    with st.spinner("🔍 Discovering qualifying momentum tickers..."):
        discovered_tickers = discover_momentum_tickers()
        
    st.info(f"📊 Found {len(discovered_tickers)} candidate tickers for screening")
    
    with st.spinner("📈 Screening candidates against momentum criteria..."):
        qualified_results = screen_discovered_tickers(tracker, discovered_tickers, 
                                                    min_rs_score, min_weekly_target, market_health)
        
    if qualified_results:
        st.success(f"✅ {len(qualified_results)} tickers passed comprehensive screening")
        return qualified_results
    else:
        st.warning("⚠️ No tickers passed auto-discovery screening. Try adjusting criteria.")
        return []

def discover_momentum_tickers() -> List[str]:
    """Automatically discover qualifying tickers from various sources"""
    discovered_tickers = set()
    
    try:
        # Method 1: Top market cap stocks from major indices
        sp500_tickers = get_sp500_leaders()
        discovered_tickers.update(sp500_tickers)
        st.info(f"📈 Added {len(sp500_tickers)} S&P 500 leaders")
        
        # Method 2: ETF leaders by volume and momentum
        etf_tickers = get_etf_leaders()
        discovered_tickers.update(etf_tickers)
        st.info(f"📊 Added {len(etf_tickers)} popular ETFs")
        
        # Method 3: Momentum stocks from various sources
        momentum_tickers = get_momentum_stocks()
        discovered_tickers.update(momentum_tickers)
        st.info(f"🚀 Added {len(momentum_tickers)} momentum candidates")
        
    except Exception as e:
        st.warning(f"Auto-discovery had some issues: {e}. Using fallback list.")
        # Fallback to comprehensive curated list (matching original)
        discovered_tickers.update([
            # Major tech stocks
            'AAPL', 'MSFT', 'NVDA', 'GOOGL', 'AMZN', 'META', 'TSLA', 'AMD', 'CRM',
            # Major indices and ETFs
            'SPY', 'QQQ', 'IWM', 'XLK', 'XLF', 'XLI', 'XLV', 'XLE', 'XLY',
            # Financial leaders
            'JPM', 'BAC', 'V', 'MA', 'BRK-B',
            # Growth stocks
            'SNOW', 'DDOG', 'CRWD', 'NET', 'PLTR'
        ])
    
    final_list = sorted(list(discovered_tickers))[:50]  # Sort for consistency, limit to 50
    st.info(f"🎯 Total unique tickers discovered: {len(final_list)}")
    return final_list

def get_sp500_leaders() -> List[str]:
    """Get top market cap S&P 500 stocks"""
    try:
        # Get S&P 500 components - simplified approach
        sp500_leaders = [
            'AAPL', 'MSFT', 'NVDA', 'AMZN', 'GOOGL', 'META', 'GOOG', 'BRK-B',
            'LLY', 'AVGO', 'JPM', 'TSLA', 'UNH', 'XOM', 'V', 'PG', 'MA', 'HD',
            'JNJ', 'COST', 'ABBV', 'NFLX', 'BAC', 'CRM', 'CVX', 'KO', 'AMD',
            'PEP', 'TMO', 'WMT', 'ACN', 'MRK', 'DIS', 'ABT', 'CSCO', 'ADBE'
        ]
        return sp500_leaders
    except Exception:
        return []

def get_etf_leaders() -> List[str]:
    """Get popular ETFs with high volume"""
    try:
        etf_leaders = [
            'SPY', 'QQQ', 'IWM', 'EFA', 'VTI', 'VEA', 'IEFA', 'VWO', 'VNQ',
            'XLK', 'XLF', 'XLV', 'XLI', 'XLE', 'XLP', 'XLY', 'XLU', 'XLB',
            'ARKK', 'ARKQ', 'ARKG', 'TLT', 'GLD', 'SLV', 'USO', 'SQQQ', 'TQQQ'
        ]
        return etf_leaders
    except Exception:
        return []

def get_momentum_stocks() -> List[str]:
    """Get diversified momentum stocks across sectors for better portfolio spread"""
    try:
        # Expanded and diversified list for better 8-10 stock selection (matching original)
        momentum_stocks = [
            # Large-cap Tech Leaders (proven momentum)
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'AMD', 'CRM', 'ADBE',
            
            # High-growth Software/Cloud 
            'SNOW', 'PLTR', 'NOW', 'DDOG', 'CRWD', 'NET', 'ZS', 'OKTA', 'WDAY', 'ADSK',
            
            # Financial Sector (rate beneficiaries)
            'JPM', 'BAC', 'WFC', 'GS', 'MS', 'V', 'MA', 'AXP', 'BRK-B', 'C',
            
            # Healthcare/Biotech (defensive growth)
            'UNH', 'JNJ', 'PFE', 'ABBV', 'TMO', 'DHR', 'ABT', 'AMGN', 'GILD', 'BMY',
            
            # Energy/Materials (commodity plays)
            'XOM', 'CVX', 'COP', 'WMB', 'KMI', 'EPD', 'SLB', 'HAL', 'EOG', 'PXD',
            
            # Consumer Discretionary (spending themes)
            'HD', 'LOW', 'DIS', 'COST', 'TGT', 'NKE', 'SBUX', 'MCD', 'CMG', 'LULU',
            
            # Industrial/Infrastructure
            'CAT', 'DE', 'BA', 'RTX', 'LMT', 'GE', 'HON', 'MMM', 'UNP', 'FDX',
            
            # Emerging Growth/Momentum
            'ROKU', 'SQ', 'SHOP', 'ZM', 'DOCU', 'PINS', 'SNAP', 'RBLX', 'U', 'FSLY',
            
            # REITs/Utilities (yield + growth)
            'PLD', 'AMT', 'CCI', 'EQIX', 'DLR', 'NEE', 'SO', 'D', 'EXC', 'SRE',
            
            # Financial Services/Asset Management
            'SEIC', 'BLK', 'SCHW', 'SPGI', 'MCO', 'ICE', 'CME', 'NDAQ', 'MSCI', 'TRV'
        ]
        return momentum_stocks
    except Exception:
        return []

def screen_discovered_tickers(tracker: PortfolioTracker, tickers: List[str], 
                            min_rs_score: float, min_weekly_target: float, 
                            market_health: Dict) -> List[Dict]:
    """Screen discovered tickers against momentum criteria - matching original logic"""
    qualified_results = []
    progress_bar = st.progress(0)
    
    # Set max results based on portfolio requirements
    max_results = 25  # Allow more candidates for better selection
    
    for i, ticker in enumerate(tickers):
        try:
            # Update progress
            progress_bar.progress((i + 1) / len(tickers))
            
            # Analyze ticker
            result = tracker.analyze_ticker_momentum(ticker, min_rs_score, min_weekly_target)
            
            if result and result.get('meets_criteria', False):
                # Apply basic market cap filter (matching original)
                market_cap = result.get('market_cap', 0)
                if market_cap > MIN_MARKET_CAP:
                    # Add momentum score for compatibility
                    result['momentum_score'] = result.get('rs_score', 0) * 0.2 + result.get('avg_weekly_return', 0) * 5
                    qualified_results.append(result)
                
        except Exception:
            # Skip problematic tickers silently (matching original)
            continue
    
    progress_bar.empty()
    
    # Sort by average weekly return for consistency (best performers first) - matching original
    qualified_results.sort(key=lambda x: x.get('avg_weekly_return', 0), reverse=True)
    return qualified_results[:max_results]


def display_recommendations(recommendations: Dict, strong_buy_weight: float, moderate_buy_weight: float,
                           market_health: Dict, allow_defensive_cash: bool, tracker: PortfolioTracker):
    """Display portfolio recommendations and allocation - matching original layout"""
    
    # Get the ranked top picks (matching original app)
    top_picks = recommendations.get('top_picks', [])
    strong_buys = recommendations['strong_buys']
    moderate_buys = recommendations['moderate_buys']
    
    # Display main portfolio section (matching original)
    st.header("🎯 YOUR RECOMMENDED PORTFOLIO")
    st.subheader(f"Top {len(top_picks)} Momentum Picks (Ranked by Score)")
    
    if top_picks:
        # Display top picks in a clean format (matching original exactly)
        portfolio_data = []
        for i, pick in enumerate(top_picks, 1):
            status, _ = tracker.get_position_status(pick['daily_change'])
            portfolio_data.append({
                'Rank': f"#{i}",
                'Ticker': pick['ticker'],
                'Name': pick['name'][:25] + "..." if len(pick['name']) > 25 else pick['name'],
                'Price': f"${pick['current_price']:.2f}",
                'Weekly Return': pick['avg_weekly_return'],  # Raw number for column formatting
                'Momentum Score': pick['momentum_score'],    # Raw number for column formatting
                'Status': status
            })
        
        portfolio_df = pd.DataFrame(portfolio_data)
        st.dataframe(
            portfolio_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Rank": st.column_config.TextColumn("Rank", width="small"),
                "Weekly Return": st.column_config.NumberColumn(
                    "Weekly Return",
                    format="%.1f%%"
                ),
                "Momentum Score": st.column_config.NumberColumn(
                    "Momentum Score",
                    format="%.1f"
                ),
                "Status": st.column_config.TextColumn("Status", width="small")
            }
        )
    
    # Calculate allocation using simplified version
    allocation_data = tracker.calculate_simple_allocation(
        strong_buys, moderate_buys, strong_buy_weight, moderate_buy_weight,
        market_health, allow_defensive_cash
    )
    
    # Display allocation summary
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Positions", allocation_data['num_positions'])
    
    with col2:
        st.metric("Stock Allocation", f"{allocation_data['total_allocated']}%")
    
    with col3:
        defensive_cash = allocation_data.get('defensive_cash', 0)
        st.metric("Defensive Cash", f"{defensive_cash}%")
    
    with col4:
        regime = allocation_data.get('market_regime', 'UNKNOWN')
        st.metric("Market Regime", regime)
