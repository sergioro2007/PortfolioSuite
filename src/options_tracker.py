"""
🎯 Options Trading Tracker
==========================

Weekly income options trading strategy tracker targeting $500/week using:
- Bull Put Spreads
- Bear Call Spreads  
- Broken Wing Butterflies
- Iron Condors

Features:
- Trade memory and evaluation
- 1-week price predictions using technical indicators
- Trade recommendations with detailed analysis
- P&L tracking and strategy optimization

Version: 1                    short_call_price = option_prices.get(f"CALL_{short_strike:g}", 0)
                    long_call_price = option_prices.get(f"CALL_{long_strike:g}", 0)
                    
                    # Use fallback pricing only for missing prices
                    if short_call_price == 0 or long_call_price == 0:
                        fallback_prices = self._fallback_option_prices(ticker, [short_strike, long_strike], expiration_date, 'call')
                        if short_call_price == 0:
                            short_call_price = fallback_prices.get(f"CALL_{short_strike:g}", 1.5)
                        if long_call_price == 0:
                            long_call_price = fallback_prices.get(f"CALL_{long_strike:g}", 0.5)Updated: July 5, 2025
"""

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import json
import pickle
import os
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# Optional plotly imports for enhanced visualizations
try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

class OptionsTracker:
    """Options trading tracker for weekly income strategies"""
    
    def __init__(self):
        self.trades_file = "data/options_trades.pkl"
        self.predictions_file = "price_predictions.pkl"
        self.target_weekly_income = 500
        
        # Load existing trades
        self.trades = self.load_trades()
        self.predictions = self.load_predictions()
        
        # Strategy types
        self.strategy_types = [
            "Bull Put Spread",
            "Bear Call Spread", 
            "Broken Wing Butterfly",
            "Iron Condor",
            "Cash Secured Put",
            "Covered Call",
            "Protective Put"
        ]
        
        # Generate a dynamic watchlist with popular options-active tickers
        # This replaces the previous hard-coded watchlist with real-time data
        self.watchlist = self.generate_dynamic_watchlist()
    
    def load_trades(self) -> List[Dict]:
        """Load existing trades from file"""
        try:
            if os.path.exists(self.trades_file):
                with open(self.trades_file, 'rb') as f:
                    return pickle.load(f)
        except Exception as e:
            st.error(f"Error loading trades: {e}")
        return []
    
    def save_trades(self):
        """Save trades to file"""
        try:
            with open(self.trades_file, 'wb') as f:
                pickle.dump(self.trades, f)
        except Exception as e:
            st.error(f"Error saving trades: {e}")
    
    def load_predictions(self) -> Dict:
        """Load price predictions from file"""
        try:
            if os.path.exists(self.predictions_file):
                with open(self.predictions_file, 'rb') as f:
                    return pickle.load(f)
        except Exception as e:
            st.error(f"Error loading predictions: {e}")
        return {}
    
    def save_predictions(self):
        """Save price predictions to file"""
        try:
            with open(self.predictions_file, 'wb') as f:
                pickle.dump(self.predictions, f)
        except Exception as e:
            st.error(f"Error saving predictions: {e}")
    
    def get_technical_indicators(self, ticker: str, period: str = "3mo") -> Dict:
        """Calculate technical indicators for price prediction"""
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)
            
            if hist.empty:
                return {}
            
            # Calculate indicators
            close = hist['Close']
            volume = hist['Volume']
            
            # Moving averages
            ma_5 = close.rolling(window=5).mean()
            ma_10 = close.rolling(window=10).mean()
            ma_20 = close.rolling(window=20).mean()
            
            # RSI
            delta = close.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            # MACD
            ema_12 = close.ewm(span=12).mean()
            ema_26 = close.ewm(span=26).mean()
            macd = ema_12 - ema_26
            signal = macd.ewm(span=9).mean()
            
            # Bollinger Bands
            bb_middle = close.rolling(window=20).mean()
            bb_std = close.rolling(window=20).std()
            bb_upper = bb_middle + (bb_std * 2)
            bb_lower = bb_middle - (bb_std * 2)
            
            # Volume indicators
            volume_ma = volume.rolling(window=10).mean()
            volume_ratio = volume.iloc[-1] / volume_ma.iloc[-1]
            
            # Current values
            current_price = close.iloc[-1]
            
            return {
                'current_price': current_price,
                'ma_5': ma_5.iloc[-1],
                'ma_10': ma_10.iloc[-1],
                'ma_20': ma_20.iloc[-1],
                'rsi': rsi.iloc[-1],
                'macd': macd.iloc[-1],
                'macd_signal': signal.iloc[-1],
                'bb_upper': bb_upper.iloc[-1],
                'bb_lower': bb_lower.iloc[-1],
                'volume_ratio': volume_ratio,
                'volatility': close.pct_change().std() * np.sqrt(252),
                'momentum': (current_price - close.iloc[-5]) / close.iloc[-5] * 100
            }
        except Exception as e:
            st.error(f"Error calculating indicators for {ticker}: {e}")
            return {}
    
    def predict_price_range(self, ticker: str) -> Dict:
        """Predict 1-week price range using technical indicators"""
        try:
            indicators = self.get_technical_indicators(ticker)
            if not indicators:
                return {}
            
            current_price = indicators['current_price']
            volatility = indicators['volatility']
            
            # Weekly volatility estimate
            weekly_vol = volatility / np.sqrt(52)
            
            # Base prediction range (1 standard deviation)
            base_range = current_price * weekly_vol
            
            # Adjust based on technical indicators
            rsi = indicators.get('rsi', 50)
            macd = indicators.get('macd', 0)
            macd_signal = indicators.get('macd_signal', 0)
            momentum = indicators.get('momentum', 0)
            
            # Bias calculation
            bias_score = 0
            
            # RSI bias
            if rsi > 70:
                bias_score -= 0.2  # Overbought, bearish bias
            elif rsi < 30:
                bias_score += 0.2  # Oversold, bullish bias
            
            # MACD bias
            if macd > macd_signal:
                bias_score += 0.1  # Bullish momentum
            else:
                bias_score -= 0.1  # Bearish momentum
            
            # Momentum bias
            if momentum > 2:
                bias_score += 0.1
            elif momentum < -2:
                bias_score -= 0.1
            
            # Calculate predicted range
            lower_bound = current_price - base_range
            upper_bound = current_price + base_range
            
            # Bias-adjusted target
            bias_adjustment = current_price * bias_score * 0.01
            target_price = current_price + bias_adjustment
            
            # Probability of bullish move
            bullish_prob = 0.5 + (bias_score * 0.5)
            bullish_prob = max(0.1, min(0.9, bullish_prob))
            
            return {
                'current_price': current_price,
                'lower_bound': lower_bound,
                'upper_bound': upper_bound,
                'target_price': target_price,
                'bullish_probability': bullish_prob,
                'bias_score': bias_score,
                'weekly_volatility': weekly_vol,
                'indicators': indicators
            }
        except Exception as e:
            st.error(f"Error predicting price for {ticker}: {e}")
            return {}
    
    def evaluate_trade(self, trade: Dict) -> Dict:
        """Evaluate an existing trade and provide recommendations"""
        try:
            ticker = trade['ticker']
            strategy = trade['strategy']
            expiration = trade['expiration']
            
            # Get current market data
            prediction = self.predict_price_range(ticker)
            if not prediction:
                return {'recommendation': 'HOLD', 'reason': 'Unable to fetch market data'}
            
            current_price = prediction['current_price']
            
            # Days to expiration
            days_to_exp = (datetime.strptime(expiration, '%Y-%m-%d') - datetime.now()).days
            
            # Strategy-specific evaluation
            return self._evaluate_strategy(trade, strategy, current_price, days_to_exp)
            
        except Exception as e:
            return {'recommendation': 'HOLD', 'reason': f'Error evaluating trade: {e}'}
    
    def _evaluate_strategy(self, trade: Dict, strategy: str, current_price: float, days_to_exp: int) -> Dict:
        """Helper method to evaluate specific strategy types"""
        if strategy == "Bull Put Spread":
            return self._evaluate_bull_put_spread(trade, current_price, days_to_exp)
        elif strategy == "Bear Call Spread":
            return self._evaluate_bear_call_spread(trade, current_price, days_to_exp)
        elif strategy == "Iron Condor":
            return self._evaluate_iron_condor(trade, current_price, days_to_exp)
        else:
            return {'recommendation': 'HOLD', 'reason': 'Default hold recommendation'}
    
    def _evaluate_bull_put_spread(self, trade: Dict, current_price: float, days_to_exp: int) -> Dict:
        """Evaluate Bull Put Spread strategy"""
        short_strike = trade['short_strike']
        long_strike = trade['long_strike']
        
        if current_price > short_strike * 1.1:
            return {'recommendation': 'CLOSE', 'reason': 'Well above short strike, capture profits'}
        elif current_price < long_strike * 0.95:
            return {'recommendation': 'CLOSE', 'reason': 'Too close to max loss, cut losses'}
        elif days_to_exp <= 3:
            return {'recommendation': 'CLOSE', 'reason': 'Close to expiration, manage risk'}
        else:
            return {'recommendation': 'HOLD', 'reason': 'Trade within acceptable range'}
    
    def _evaluate_bear_call_spread(self, trade: Dict, current_price: float, days_to_exp: int) -> Dict:
        """Evaluate Bear Call Spread strategy"""
        short_strike = trade['short_strike']
        long_strike = trade['long_strike']
        
        if current_price < short_strike * 0.9:
            return {'recommendation': 'CLOSE', 'reason': 'Well below short strike, capture profits'}
        elif current_price > long_strike * 1.05:
            return {'recommendation': 'CLOSE', 'reason': 'Too close to max loss, cut losses'}
        elif days_to_exp <= 3:
            return {'recommendation': 'CLOSE', 'reason': 'Close to expiration, manage risk'}
        else:
            return {'recommendation': 'HOLD', 'reason': 'Trade within acceptable range'}
    
    def _evaluate_iron_condor(self, trade: Dict, current_price: float, days_to_exp: int) -> Dict:
        """Evaluate Iron Condor strategy"""
        put_short = trade['put_short_strike']
        call_short = trade['call_short_strike']
        
        if put_short < current_price < call_short:
            if days_to_exp <= 5:
                return {'recommendation': 'CLOSE', 'reason': 'In profit zone, close before expiration'}
            else:
                return {'recommendation': 'HOLD', 'reason': 'In profit zone, let time decay work'}
        else:
            return {'recommendation': 'ADJUST', 'reason': 'Outside profit zone, consider adjustment'}
    
    def generate_trade_suggestions(self, num_suggestions: int = 3, min_profit_target: float = 1.0) -> List[Dict]:
        """Generate new trade suggestions based on market analysis
        
        Args:
            num_suggestions: Target number of suggestions to generate
            min_profit_target: Minimum profit target per share (default $1.00 = $100/contract)
        """
        suggestions = []
        
        try:
            print(f"🔍 Analyzing tickers for trade opportunities (min profit target: ${min_profit_target:.2f}/share)")
            
            # Analyze each ticker for opportunities - generate MULTIPLE strategies per ticker
            for ticker, forecast in self.watchlist.items():
                # Process this ticker and try to generate suggestions for it
                print(f"🔍 Processing {ticker}...")
                
                try:
                    prediction = self.predict_price_range(ticker)
                    if not prediction:
                        print(f"  ⚠️ No prediction data for {ticker}, skipping")
                        continue
                    
                    current_price = prediction['current_price']
                    bullish_prob = prediction['bullish_probability']
                    bias_score = prediction['bias_score']
                    
                    print(f"  � {ticker}: Price=${current_price:.2f}, Bias={bias_score:.3f}, Bullish={bullish_prob:.1%}")
                    
                    # Standard expiration date for all strategies
                    expiration_date = "2025-08-01"
                    
                    # Try all three strategy types for each ticker
                    self._try_bull_put_spread(ticker, prediction, expiration_date, min_profit_target, suggestions)
                    self._try_bear_call_spread(ticker, prediction, expiration_date, min_profit_target, suggestions)
                    self._try_iron_condor(ticker, prediction, expiration_date, min_profit_target, suggestions)
                    
                    # Break if we have enough suggestions
                    if len(suggestions) >= num_suggestions * 2:  # Get more than needed, then sort and filter
                        break
                        
                except Exception as e:
                    print(f"  ❌ Error processing {ticker}: {e}")
                    continue
            
            # Sort by confidence and return top suggestions
            suggestions.sort(key=lambda x: x['confidence'], reverse=True)
            
            # If no suggestions were generated, create some basic ones with relaxed criteria
            if not suggestions:
                suggestions = self._generate_fallback_suggestions(min_profit_target)
            
            print(f"✅ Generated {len(suggestions)} trade suggestions")
            return suggestions[:num_suggestions]
            
        except Exception as e:
            print(f"❌ Exception in generate_trade_suggestions: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _try_bull_put_spread(self, ticker, prediction, expiration_date, min_profit_target, suggestions):
        """Try to create a Bull Put Spread suggestion for this ticker"""
        try:
            print(f"  📊 Analyzing Bull Put Spread for {ticker}...")
            
            current_price = prediction['current_price']
            bullish_prob = prediction['bullish_probability']
            bias_score = prediction['bias_score']
            
            # Find appropriate strikes
            short_strike = self.find_available_otm_strike(ticker, current_price, 0.055, 'put', expiration_date)
            long_strike = self.find_available_otm_strike(ticker, current_price, 0.08, 'put', expiration_date)
            option_prices = self.get_option_prices(ticker, [short_strike, long_strike], expiration_date, 'put')
            
            # Get prices
            short_put_price = option_prices.get(f"PUT_{short_strike:g}", 0)
            long_put_price = option_prices.get(f"PUT_{long_strike:g}", 0)
            
            # Use fallback pricing only for missing prices
            if short_put_price == 0 or long_put_price == 0:
                fallback_prices = self._fallback_option_prices(ticker, [short_strike, long_strike], expiration_date, 'put')
                if short_put_price == 0:
                    short_put_price = fallback_prices.get(f"PUT_{short_strike:g}", 2.0)
                if long_put_price == 0:
                    long_put_price = fallback_prices.get(f"PUT_{long_strike:g}", 1.0)
            
            # Calculate trade metrics
            credit = short_put_price - long_put_price
            max_loss = (short_strike - long_strike) - credit
            profit_target = credit * 0.5
            
            # Filter: Only include suggestions with profit target >= configurable minimum
            if profit_target < min_profit_target:
                print(f"   ❌ Skipping Bull Put Spread for {ticker}: Profit target ${profit_target:.2f} < ${min_profit_target:.2f} minimum")
                return False
            
            # Get indicators for reasoning
            indicators = prediction.get('indicators', {})
            rsi = indicators.get('rsi', 50)
            macd = indicators.get('macd', 0)
            macd_signal = indicators.get('macd_signal', 0)
            momentum = indicators.get('momentum', 0)
            macd_status = "bullish" if macd > macd_signal else "bearish"
            
            # RSI status
            if rsi < 30:
                rsi_status = "(oversold - bullish)"
            elif rsi > 70:
                rsi_status = "(overbought - caution)"
            else:
                rsi_status = "(neutral)"
            
            # Create reasoning
            reasoning = f"🐂 BULLISH STRATEGY (Score: {bias_score:.2f})\n\n"
            reasoning += "📈 Technical Analysis:\n"
            reasoning += f"• RSI: {rsi:.1f} {rsi_status}\n"
            reasoning += f"• MACD: {macd_status} momentum\n"
            reasoning += f"• Price momentum: {momentum:.1f}%\n\n"
            reasoning += "🎯 Strategy: Bull Put Spread\n"
            reasoning += f"• Expectation: Price stays above ${short_strike:.2f}\n"
            reasoning += f"• Conservative strikes: ~5.5% below current price\n"
            reasoning += f"• Profit if {ticker} closes above ${short_strike:.2f} at expiration\n"
            reasoning += f"• Max profit: ${credit:.2f}/share (${credit*100:.0f}/contract)\n"
            reasoning += f"• Max loss: ${max_loss:.2f}/share (${max_loss*100:.0f}/contract)\n"
            reasoning += f"• Break-even: ${short_strike - credit:.2f}\n\n"
            reasoning += "⏰ Time Decay: Works in our favor as options lose value"
            
            # Create suggestion
            suggestions.append({
                'ticker': ticker,
                'strategy': 'Bull Put Spread',
                'bias': 'Bullish',
                'bullish_prob': bullish_prob,
                'short_strike': short_strike,
                'long_strike': long_strike,
                'credit': credit,
                'max_loss': max_loss,
                'profit_target': profit_target,
                'expiration': expiration_date,
                'confidence': min(90, 50 + bias_score * 100),
                'reasoning': reasoning,
                'legs': sorted([
                    {'action': 'SELL', 'type': 'PUT', 'strike': short_strike, 'price': short_put_price},
                    {'action': 'BUY', 'type': 'PUT', 'strike': long_strike, 'price': long_put_price}
                ], key=lambda x: x['strike'])
            })
            
            print(f"   ✅ Added Bull Put Spread for {ticker}: ${profit_target:.2f}/share profit target")
            return True
            
        except Exception as e:
            print(f"   ❌ Error generating Bull Put Spread for {ticker}: {e}")
            return False
    
    def _try_bear_call_spread(self, ticker, prediction, expiration_date, min_profit_target, suggestions):
        """Try to create a Bear Call Spread suggestion for this ticker"""
        try:
            print(f"  📊 Analyzing Bear Call Spread for {ticker}...")
            
            current_price = prediction['current_price']
            bullish_prob = prediction['bullish_probability']
            bias_score = prediction['bias_score']
            
            # Find appropriate strikes
            short_strike = self.find_available_otm_strike(ticker, current_price, 0.055, 'call', expiration_date)
            long_strike = self.find_available_otm_strike(ticker, current_price, 0.08, 'call', expiration_date)
            option_prices = self.get_option_prices(ticker, [short_strike, long_strike], expiration_date, 'call')
            
            # Get prices
            short_call_price = option_prices.get(f"CALL_{short_strike:g}", 0)
            long_call_price = option_prices.get(f"CALL_{long_strike:g}", 0)
            
            # Use fallback pricing only for missing prices
            if short_call_price == 0 or long_call_price == 0:
                fallback_prices = self._fallback_option_prices(ticker, [short_strike, long_strike], expiration_date, 'call')
                if short_call_price == 0:
                    short_call_price = fallback_prices.get(f"CALL_{short_strike:g}", 1.5)
                if long_call_price == 0:
                    long_call_price = fallback_prices.get(f"CALL_{long_strike:g}", 0.5)
            
            # Calculate trade metrics
            credit = short_call_price - long_call_price
            max_loss = (long_strike - short_strike) - credit
            profit_target = credit * 0.5
            
            # Filter: Only include suggestions with profit target >= configurable minimum
            if profit_target < min_profit_target:
                print(f"   ❌ Skipping Bear Call Spread for {ticker}: Profit target ${profit_target:.2f} < ${min_profit_target:.2f} minimum")
                return False
            
            # Get indicators for reasoning
            indicators = prediction.get('indicators', {})
            rsi = indicators.get('rsi', 50)
            macd = indicators.get('macd', 0)
            macd_signal = indicators.get('macd_signal', 0)
            momentum = indicators.get('momentum', 0)
            macd_status = "bullish" if macd > macd_signal else "bearish"
            
            # RSI status
            if rsi > 70:
                rsi_status = "(overbought - bearish)"
            elif rsi < 30:
                rsi_status = "(oversold - caution)"
            else:
                rsi_status = "(neutral)"
            
            # Create reasoning
            reasoning = f"🐻 BEARISH STRATEGY (Score: {bias_score:.2f})\n\n"
            reasoning += "📉 Technical Analysis:\n"
            reasoning += f"• RSI: {rsi:.1f} {rsi_status}\n"
            reasoning += f"• MACD: {macd_status} momentum\n"
            reasoning += f"• Price momentum: {momentum:.1f}%\n\n"
            reasoning += "🎯 Strategy: Bear Call Spread\n"
            reasoning += f"• Expectation: Price stays below ${short_strike:.2f}\n"
            reasoning += "• Conservative strikes: ~5.5% above current price\n"
            reasoning += f"• Profit if {ticker} closes below ${short_strike:.2f} at expiration\n"
            reasoning += f"• Max profit: ${credit:.2f}/share (${credit*100:.0f}/contract)\n"
            reasoning += f"• Max loss: ${max_loss:.2f}/share (${max_loss*100:.0f}/contract)\n"
            reasoning += f"• Break-even: ${short_strike + credit:.2f}\n\n"
            reasoning += "⏰ Time Decay: Works in our favor as options lose value"
            
            # Create suggestion
            suggestions.append({
                'ticker': ticker,
                'strategy': 'Bear Call Spread',
                'bias': 'Bearish',
                'bullish_prob': bullish_prob,
                'short_strike': short_strike,
                'long_strike': long_strike,
                'credit': credit,
                'max_loss': max_loss,
                'profit_target': profit_target,
                'expiration': expiration_date,
                'confidence': min(90, 50 + abs(bias_score) * 100),
                'reasoning': reasoning,
                'legs': sorted([
                    {'action': 'SELL', 'type': 'CALL', 'strike': short_strike, 'price': short_call_price},
                    {'action': 'BUY', 'type': 'CALL', 'strike': long_strike, 'price': long_call_price}
                ], key=lambda x: x['strike'])
            })
            
            print(f"   ✅ Added Bear Call Spread for {ticker}: ${profit_target:.2f}/share profit target")
            return True
            
        except Exception as e:
            print(f"   ❌ Error generating Bear Call Spread for {ticker}: {e}")
            return False

    def _try_iron_condor(self, ticker, prediction, expiration_date, min_profit_target, suggestions):
        """Try to create an Iron Condor suggestion for this ticker"""
        try:
            print(f"  📊 Analyzing Iron Condor for {ticker}...")
            
            current_price = prediction['current_price']
            bullish_prob = prediction['bullish_probability']
            bias_score = prediction['bias_score']
            
            # Find appropriate strikes
            put_short = self.find_available_otm_strike(ticker, current_price, 0.055, 'put', expiration_date)
            put_long = self.find_available_otm_strike(ticker, current_price, 0.08, 'put', expiration_date)
            call_short = self.find_available_otm_strike(ticker, current_price, 0.055, 'call', expiration_date)
            call_long = self.find_available_otm_strike(ticker, current_price, 0.08, 'call', expiration_date)
            
            strikes = [put_short, put_long, call_short, call_long]
            option_prices = self.get_option_prices(ticker, strikes, expiration_date, 'both')
            
            # Get prices
            put_short_price = option_prices.get(f"PUT_{put_short:g}", 0)
            put_long_price = option_prices.get(f"PUT_{put_long:g}", 0)
            call_short_price = option_prices.get(f"CALL_{call_short:g}", 0)
            call_long_price = option_prices.get(f"CALL_{call_long:g}", 0)
            
            # Use fallback pricing only for missing prices
            missing_prices = [k for k, v in {
                f"PUT_{put_short:g}": put_short_price, 
                f"PUT_{put_long:g}": put_long_price,
                f"CALL_{call_short:g}": call_short_price,
                f"CALL_{call_long:g}": call_long_price
            }.items() if v == 0]
            
            if missing_prices:
                fallback_prices = self._fallback_option_prices(ticker, strikes, expiration_date, 'both')
                if put_short_price == 0:
                    put_short_price = fallback_prices.get(f"PUT_{put_short:g}", 1.5)
                if put_long_price == 0:
                    put_long_price = fallback_prices.get(f"PUT_{put_long:g}", 1.0)
                if call_short_price == 0:
                    call_short_price = fallback_prices.get(f"CALL_{call_short:g}", 1.0)
                if call_long_price == 0:
                    call_long_price = fallback_prices.get(f"CALL_{call_long:g}", 0.5)
            
            # Calculate trade metrics
            credit = (put_short_price - put_long_price) + (call_short_price - call_long_price)
            max_loss = max((put_short - put_long), (call_long - call_short)) - credit
            profit_target = credit * 0.5
            
            # Filter: Only include suggestions with profit target >= configurable minimum
            if profit_target < min_profit_target:
                print(f"   ❌ Skipping Iron Condor for {ticker}: Profit target ${profit_target:.2f} < ${min_profit_target:.2f} minimum")
                return False
            
            # Get indicators for reasoning
            indicators = prediction.get('indicators', {})
            rsi = indicators.get('rsi', 50)
            macd = indicators.get('macd', 0)
            macd_signal = indicators.get('macd_signal', 0)
            momentum = indicators.get('momentum', 0)
            macd_status = "bullish" if macd > macd_signal else "bearish"
            
            # Create reasoning
            reasoning = f"⚖️ NEUTRAL STRATEGY (Score: {bias_score:.2f})\n\n"
            reasoning += "📊 Technical Analysis:\n"
            reasoning += f"• RSI: {rsi:.1f} (neutral territory)\n"
            reasoning += f"• MACD: {macd_status} momentum (mixed signals)\n"
            reasoning += f"• Price momentum: {momentum:.1f}% (sideways action)\n\n"
            reasoning += "🎯 Strategy: Iron Condor\n"
            reasoning += f"• Expectation: Price stays between ${put_short:.2f} and ${call_short:.2f}\n"
            reasoning += "• Conservative strikes: ~5.5% from current price\n"
            reasoning += f"• Profit zone: ${put_short:.2f} ≤ {ticker} ≤ ${call_short:.2f}\n"
            reasoning += f"• Max profit: ${credit:.2f}/share (${credit*100:.0f}/contract)\n"
            reasoning += f"• Max loss: ${max_loss:.2f}/share (${max_loss*100:.0f}/contract)\n"
            reasoning += f"• Break-even points: ${put_short - credit:.2f} and ${call_short + credit:.2f}\n\n"
            reasoning += "⏰ Time Decay: Works strongly in our favor - all 4 options decay"
            
            # Create suggestion
            suggestions.append({
                'ticker': ticker,
                'strategy': 'Iron Condor',
                'bias': 'Neutral',
                'bullish_prob': bullish_prob,
                'put_short_strike': put_short,
                'put_long_strike': put_long,
                'call_short_strike': call_short,
                'call_long_strike': call_long,
                'credit': credit,
                'max_loss': max_loss,
                'profit_target': profit_target,
                'expiration': expiration_date,
                'confidence': min(90, 60 + abs(0.5 - bullish_prob) * 100),
                'reasoning': reasoning,
                'legs': sorted([
                    {'action': 'SELL', 'type': 'PUT', 'strike': put_short, 'price': put_short_price},
                    {'action': 'BUY', 'type': 'PUT', 'strike': put_long, 'price': put_long_price},
                    {'action': 'SELL', 'type': 'CALL', 'strike': call_short, 'price': call_short_price},
                    {'action': 'BUY', 'type': 'CALL', 'strike': call_long, 'price': call_long_price}
                ], key=lambda x: x['strike'])
            })
            
            print(f"   ✅ Added Iron Condor for {ticker}: ${profit_target:.2f}/share profit target")
            return True
            
        except Exception as e:
            print(f"   ❌ Error generating Iron Condor for {ticker}: {e}")
            return False
            
    def _generate_fallback_suggestions(self, min_profit_target: float) -> List[Dict]:
        """Generate fallback suggestions when normal criteria don't yield enough trades"""
        fallback_suggestions = []
        print("⚠️ No suggestions met strict criteria, generating with relaxed thresholds...")
        
        try:
            # Try the first 5 tickers in the watchlist
            for ticker, forecast in list(self.watchlist.items())[:5]:
                prediction = self.predict_price_range(ticker)
                if not prediction:
                    continue
                
                current_price = prediction['current_price']
                expiration_date = "2025-08-01"
                
                # Try an Iron Condor (neutral strategy works for most market conditions)
                put_short = self.find_available_otm_strike(ticker, current_price, 0.055, 'put', expiration_date)
                put_long = self.find_available_otm_strike(ticker, current_price, 0.08, 'put', expiration_date)
                call_short = self.find_available_otm_strike(ticker, current_price, 0.055, 'call', expiration_date)
                call_long = self.find_available_otm_strike(ticker, current_price, 0.08, 'call', expiration_date)
                
                # Use fallback pricing (since this is already a fallback)
                put_short_price = 1.5
                put_long_price = 1.0
                call_short_price = 1.0
                call_long_price = 0.5
                
                credit = (put_short_price - put_long_price) + (call_short_price - call_long_price)
                max_loss = max((put_short - put_long), (call_long - call_short)) - credit
                profit_target = credit * 0.5
                
                # Still require minimum profit target
                if profit_target < min_profit_target:
                    print(f"   ❌ Skipping fallback for {ticker}: Profit target ${profit_target:.2f} < ${min_profit_target:.2f}")
                    continue
                
                fallback_suggestions.append({
                    'ticker': ticker,
                    'strategy': 'Iron Condor',
                    'bias': 'Neutral',
                    'bullish_prob': 0.5,
                    'put_short_strike': put_short,
                    'put_long_strike': put_long,
                    'call_short_strike': call_short,
                    'call_long_strike': call_long,
                    'credit': credit,
                    'max_loss': max_loss,
                    'profit_target': profit_target,
                    'expiration': expiration_date,
                    'confidence': 60,  # Medium confidence
                    'reasoning': f"📊 FALLBACK STRATEGY for {ticker}\n\nUsing Iron Condor for potential range-bound profits.\nProfit if price stays between ${put_short:.2f} and ${call_short:.2f} at expiration.",
                    'legs': sorted([
                        {'action': 'SELL', 'type': 'PUT', 'strike': put_short, 'price': put_short_price},
                        {'action': 'BUY', 'type': 'PUT', 'strike': put_long, 'price': put_long_price},
                        {'action': 'SELL', 'type': 'CALL', 'strike': call_short, 'price': call_short_price},
                        {'action': 'BUY', 'type': 'CALL', 'strike': call_long, 'price': call_long_price}
                    ], key=lambda x: x['strike'])
                })
                
                print(f"   ✅ Added fallback Iron Condor for {ticker}")
                
                if len(fallback_suggestions) >= 3:
                    break
                    
        except Exception as e:
            print(f"❌ Error generating fallback suggestions: {e}")
        
        return fallback_suggestions
    
    def add_trade(self, trade_data: Dict):
        """Add a new trade to the tracker"""
        trade_data['id'] = len(self.trades) + 1
        trade_data['entry_date'] = datetime.now().strftime('%Y-%m-%d')
        trade_data['status'] = 'Open'
        self.trades.append(trade_data)
        self.save_trades()
    
    def close_trade(self, trade_id: int, exit_price: float, exit_reason: str):
        """Close an existing trade"""
        for trade in self.trades:
            if trade['id'] == trade_id:
                trade['status'] = 'Closed'
                trade['exit_date'] = datetime.now().strftime('%Y-%m-%d')
                trade['exit_price'] = exit_price
                trade['exit_reason'] = exit_reason
                # Calculate P&L
                if trade['strategy'] in ['Bull Put Spread', 'Bear Call Spread', 'Iron Condor']:
                    trade['pnl'] = trade['credit'] - exit_price
                self.save_trades()
                return True
        return False
    
    def get_open_trades(self) -> List[Dict]:
        """Get all open trades"""
        return [trade for trade in self.trades if trade.get('status') == 'Open']
    
    def get_closed_trades(self) -> List[Dict]:
        """Get all closed trades"""
        return [trade for trade in self.trades if trade.get('status') == 'Closed']
    
    def calculate_weekly_pnl(self) -> Dict:
        """Calculate weekly P&L statistics"""
        closed_trades = self.get_closed_trades()
        
        if not closed_trades:
            return {
                'total_pnl': 0, 
                'avg_weekly': 0, 
                'win_rate': 0,
                'total_trades': 0,
                'winning_trades': 0
            }
        
        total_pnl = sum(trade.get('pnl', 0) for trade in closed_trades)
        winning_trades = sum(1 for trade in closed_trades if trade.get('pnl', 0) > 0)
        win_rate = winning_trades / len(closed_trades) if closed_trades else 0
        
        # Estimate weekly average (assuming trades are roughly weekly)
        avg_weekly = total_pnl / max(1, len(closed_trades))
        
        return {
            'total_pnl': total_pnl,
            'avg_weekly': avg_weekly,
            'win_rate': win_rate,
            'total_trades': len(closed_trades),
            'winning_trades': winning_trades
        }
    
    def get_option_prices(self, ticker: str, strikes: List[float], expiration: str, option_type: str = 'both') -> Dict:
        """Get real option prices from yfinance option chains"""
        try:
            stock = yf.Ticker(ticker)
            option_prices = {}
            
            # Get available expiration dates
            try:
                expirations = stock.options
                if not expirations:
                    return self._fallback_option_prices(ticker, strikes, expiration, option_type)
                
                # Find the closest expiration date to our target
                target_date = datetime.strptime(expiration, '%Y-%m-%d').date()
                closest_exp = None
                min_diff = float('inf')
                
                for exp_str in expirations:
                    exp_date = datetime.strptime(exp_str, '%Y-%m-%d').date()
                    diff = abs((exp_date - target_date).days)
                    if diff < min_diff:
                        min_diff = diff
                        closest_exp = exp_str
                
                if not closest_exp:
                    return self._fallback_option_prices(ticker, strikes, expiration, option_type)
                
                # Get option chain for the closest expiration
                option_chain = stock.option_chain(closest_exp)
                
                # Extract prices for our strikes
                for strike in strikes:
                    # Keep decimal strikes intact - don't convert to int!
                    strike_key = f"{strike:g}"  # Formats 172.5 as "172.5", 170.0 as "170"
                    
                    if option_type in ['put', 'both']:
                        # Look for put options at this strike
                        puts = option_chain.puts
                        put_match = puts[puts['strike'] == strike]  # Use exact strike value
                        if not put_match.empty:
                            # Use midpoint of bid/ask or last price
                            bid = put_match['bid'].iloc[0]
                            ask = put_match['ask'].iloc[0]
                            last = put_match['lastPrice'].iloc[0]
                            
                            if bid > 0 and ask > 0:
                                price = (bid + ask) / 2  # Midpoint
                            else:
                                price = last if last > 0 else 0.01
                            
                            option_prices[f"PUT_{strike_key}"] = round(price, 2)
                    
                    if option_type in ['call', 'both']:
                        # Look for call options at this strike
                        calls = option_chain.calls
                        call_match = calls[calls['strike'] == strike]  # Use exact strike value
                        if not call_match.empty:
                            # Use midpoint of bid/ask or last price
                            bid = call_match['bid'].iloc[0]
                            ask = call_match['ask'].iloc[0]
                            last = call_match['lastPrice'].iloc[0]
                            
                            if bid > 0 and ask > 0:
                                price = (bid + ask) / 2  # Midpoint
                            else:
                                price = last if last > 0 else 0.01
                            
                            option_prices[f"CALL_{strike_key}"] = round(price, 2)
                
                return option_prices
                
            except Exception as e:
                st.warning(f"Could not fetch real option prices for {ticker}: {e}")
                return self._fallback_option_prices(ticker, strikes, expiration, option_type)
            
        except Exception as e:
            st.error(f"Error getting option prices for {ticker}: {e}")
            return self._fallback_option_prices(ticker, strikes, expiration, option_type)
    
    def _fallback_option_prices(self, ticker: str, strikes: List[float], expiration: str, option_type: str = 'both') -> Dict:
        """Fallback to estimated prices if real prices unavailable"""
        try:
            option_prices = {}
            
            # Get current price and calculate time to expiration
            current_price = self.watchlist.get(ticker, {}).get('current_price', 100)
            
            # Calculate days to expiration
            exp_date = datetime.strptime(expiration, '%Y-%m-%d')
            days_to_exp = max(1, (exp_date - datetime.now()).days)
            time_factor = max(0.1, days_to_exp / 365)  # Annualized time
            
            # Estimate volatility based on ticker (more realistic estimates)
            volatility_map = {
                'SPY': 0.15, 'QQQ': 0.20, 'AAPL': 0.25, 'MSFT': 0.22, 
                'NVDA': 0.35, 'TECL': 0.45, 'XLE': 0.25, 'SMH': 0.30
            }
            volatility = volatility_map.get(ticker, 0.25)
            
            for strike in strikes:
                strike_key = f"{strike:g}"  # Keep decimal format
                
                if option_type in ['put', 'both']:
                    # For puts: intrinsic value + time value
                    intrinsic_put = max(0, strike - current_price)
                    
                    # Time value based on moneyness and volatility
                    moneyness = abs(strike - current_price) / current_price
                    
                    if strike >= current_price:
                        time_value = current_price * volatility * time_factor * 0.4
                    elif moneyness <= 0.02:
                        time_value = current_price * volatility * time_factor * 0.7
                    elif moneyness <= 0.05:
                        time_value = current_price * volatility * time_factor * 0.5
                    elif moneyness <= 0.10:
                        time_value = current_price * volatility * time_factor * 0.3
                    else:
                        time_value = current_price * volatility * time_factor * 0.1
                    
                    # Apply decay for very short term
                    if days_to_exp <= 30:
                        time_value *= days_to_exp / 30
                    
                    price = intrinsic_put + time_value
                    option_prices[f"PUT_{strike_key}"] = round(max(0.01, price), 2)
                
                if option_type in ['call', 'both']:
                    # For calls: intrinsic value + time value
                    intrinsic_call = max(0, current_price - strike)
                    
                    # Time value based on moneyness and volatility
                    moneyness = abs(current_price - strike) / current_price
                    
                    if strike <= current_price:
                        time_value = current_price * volatility * time_factor * 0.4
                    elif moneyness <= 0.02:
                        time_value = current_price * volatility * time_factor * 0.7
                    elif moneyness <= 0.05:
                        time_value = current_price * volatility * time_factor * 0.5
                    elif moneyness <= 0.10:
                        time_value = current_price * volatility * time_factor * 0.3
                    else:
                        time_value = current_price * volatility * time_factor * 0.1
                    
                    # Apply decay for very short term
                    if days_to_exp <= 30:
                        time_value *= days_to_exp / 30
                    
                    price = intrinsic_call + time_value
                    option_prices[f"CALL_{strike_key}"] = round(max(0.01, price), 2)
            
            return option_prices
            
        except Exception as e:
            st.error(f"Error in fallback pricing for {ticker}: {e}")
            return {}
    
    def find_realistic_strike(self, price: float) -> float:
        """Find the nearest realistic option strike price"""
        # Most options have strikes at:
        # - Whole dollars for stocks over $25
        # - Half dollars (x.50) for stocks $10-$25  
        # - Sometimes quarter dollars (x.25, x.75) for liquid stocks
        
        if price >= 25:
            # Round to nearest whole dollar
            return round(price)
        elif price >= 10:
            # Round to nearest 0.50
            return round(price * 2) / 2
        else:
            # Round to nearest 0.25 for lower priced stocks
            return round(price * 4) / 4
    
    def get_strike_chain(self, current_price: float, num_strikes: int = 10) -> List[float]:
        """Generate a realistic strike chain around current price"""
        strikes = []
        base_strike = self.find_realistic_strike(current_price)
        
        # Determine strike increment
        if current_price >= 100:
            increment = 5  # $5 increments for high-priced stocks
        elif current_price >= 25:
            increment = 2.5  # $2.50 increments
        elif current_price >= 10:
            increment = 1  # $1 increments
        else:
            increment = 0.5  # $0.50 increments
        
        # Generate strikes above and below
        for i in range(-num_strikes//2, num_strikes//2 + 1):
            strike = base_strike + (i * increment)
            if strike > 0:
                strikes.append(strike)
        
        return sorted(strikes)
    
    def get_available_strikes(self, ticker: str, expiration_date: str) -> List[float]:
        """Get actually available strikes for a specific ticker and expiration date"""
        try:
            stock = yf.Ticker(ticker)
            
            # Check if options data is available
            if not hasattr(stock, 'options') or not stock.options:
                print(f"No options data available for {ticker}")
                return []
            
            # Find the closest expiration to our target
            target_date = datetime.strptime(expiration_date, '%Y-%m-%d').date()
            closest_exp = None
            min_diff = float('inf')
            
            for exp_str in stock.options:
                exp_date = datetime.strptime(exp_str, '%Y-%m-%d').date()
                diff = abs((exp_date - target_date).days)
                if diff < min_diff:
                    min_diff = diff
                    closest_exp = exp_str
            
            if not closest_exp:
                return []
            
            # Get option chain for the closest expiration
            option_chain = stock.option_chain(closest_exp)
            
            # Extract all available strikes
            calls_strikes = set(option_chain.calls['strike'])
            puts_strikes = set(option_chain.puts['strike'])
            
            # Combine call and put strikes
            available_strikes = calls_strikes.union(puts_strikes)
            
            return sorted(available_strikes)
            
        except Exception as e:
            print(f"Error getting available strikes for {ticker}: {e}")
            return []

    def find_available_otm_strike(self, ticker: str, current_price: float, distance_pct: float, 
                                  option_type: str, expiration_date: str) -> float:
        """Find an actually available OTM strike at approximately the given distance"""
        try:
            # First try to get actually available strikes
            available_strikes = self.get_available_strikes(ticker, expiration_date)
            
            if available_strikes:
                # Calculate target strike price based on distance percentage
                target_strike = self._calculate_target_strike(current_price, distance_pct, option_type)
                
                # Find the closest available strike to our target
                closest_strike = min(available_strikes, 
                                     key=lambda x: abs(x - target_strike))
                
                # Ensure strike is properly OTM
                closest_strike = self._ensure_otm_strike(closest_strike, current_price, 
                                                        option_type, available_strikes)
                
                return closest_strike
            
            # Fallback to theoretical calculation if no available strikes
            print("No available strikes found, falling back to theoretical calculation")
            return self.find_otm_strikes(current_price, distance_pct, option_type)
            
        except Exception as e:
            print(f"Error finding OTM strike for {ticker}: {e}")
            return self.find_otm_strikes(current_price, distance_pct, option_type)
    
    def _calculate_target_strike(self, current_price: float, distance_pct: float, option_type: str) -> float:
        """Helper to calculate target strike based on option type"""
        if option_type == 'put':
            # For puts, we want strikes below current price
            return current_price * (1 - distance_pct)
        else:
            # For calls, we want strikes above current price
            return current_price * (1 + distance_pct)
    
    def _ensure_otm_strike(self, strike: float, current_price: float, option_type: str, 
                           available_strikes: List[float]) -> float:
        """Helper to ensure strike is properly OTM based on option type"""
        # For puts, ensure strike is below current price (OTM put)
        if option_type == 'put' and strike >= current_price:
            # Filter for strikes below current price
            otm_strikes = [s for s in available_strikes if s < current_price]
            if otm_strikes:
                return max(otm_strikes)  # highest strike below current price
        
        # For calls, ensure strike is above current price (OTM call)
        elif option_type == 'call' and strike <= current_price:
            # Filter for strikes above current price
            otm_strikes = [s for s in available_strikes if s > current_price]
            if otm_strikes:
                return min(otm_strikes)  # lowest strike above current price
        
        return strike

    def generate_dynamic_watchlist(self) -> Dict:
        """
        Dynamically generate a watchlist of popular options-active tickers.
        
        Returns:
            Dict: A dictionary of tickers with their calculated parameters:
                - current_price: Current market price of the stock
                - range_68: A tuple representing 68% probability range (1 std dev) for price movement
                - target_zone: Predicted price target based on technical analysis
                - bias_prob: Probability of a bullish move (>0.5 is bullish, <0.5 is bearish)
        """
        print("Generating dynamic watchlist of popular options-active tickers...")
        watchlist = {}
        
        # Start with popular ETFs and stocks known for options liquidity
        popular_tickers = [
            # Major ETFs
            'SPY', 'QQQ', 'IWM', 'XLE', 'SMH', 'TECL',
            # Large Cap Tech
            'AAPL', 'MSFT', 'NVDA', 'GOOGL', 'AMZN', 'META', 'TSLA',
            # Other High Volume Options Stocks
            'AMD', 'INTC', 'CRM', 'NFLX'
        ]
        
        # Process each ticker to get parameters
        for ticker in popular_tickers:
            try:
                # Get stock data and calculate parameters
                ticker_data = self._calculate_ticker_parameters(ticker)
                if ticker_data:
                    watchlist[ticker] = ticker_data
                    print(f"Added {ticker} to watchlist: Price=${ticker_data['current_price']:.2f}, "
                          f"Range=${ticker_data['range_68'][0]:.2f}-${ticker_data['range_68'][1]:.2f}, "
                          f"Target=${ticker_data['target_zone']:.2f}, "
                          f"Bias={ticker_data['bias_prob']:.2f}")
            except Exception as e:
                print(f"Error processing {ticker}: {e}")
                continue
        
        print(f"Generated watchlist with {len(watchlist)} tickers")
        return watchlist
    
    def _calculate_ticker_parameters(self, ticker: str) -> Optional[Dict]:
        """
        Calculate all necessary parameters for a ticker to be used in the watchlist.
        
        Parameters explained:
        - current_price: The current market price of the stock (fetched from yfinance)
        - range_68: A tuple representing the price range with 68% probability (one standard deviation)
                   Calculated based on historical volatility and represents approximately
                   where the price is expected to stay 68% of the time over the next week.
        - target_zone: The predicted price target based on technical indicators and trend analysis
                      This is a weighted calculation using moving averages, RSI, and price momentum.
        - bias_prob: The probability of a bullish move (>0.5 is bullish bias, <0.5 is bearish)
                    This is derived from technical indicators like RSI, MACD, and price momentum.
        
        Args:
            ticker: The ticker symbol to analyze
        
        Returns:
            Dict or None: Parameters for this ticker or None if unable to calculate
        """
        try:
            # First get stock data from yfinance
            stock = yf.Ticker(ticker)
            hist = stock.history(period="3mo")  # 3 months of data
            
            if hist.empty:
                print(f"No historical data for {ticker}")
                return None
            
            # Calculate current price
            current_price = hist['Close'].iloc[-1]
            
            # Calculate historical volatility
            daily_returns = hist['Close'].pct_change().dropna()
            hist_volatility = daily_returns.std() * np.sqrt(252)  # Annualized volatility
            
            # Calculate expected weekly volatility
            weekly_vol = hist_volatility / np.sqrt(52)  # Weekly volatility
            
            # Calculate 68% probability range (1 standard deviation)
            # 68% of the time, price should stay within this range for the next week
            price_range_low = current_price * (1 - weekly_vol)
            price_range_high = current_price * (1 + weekly_vol)
            range_68 = (price_range_low, price_range_high)
            
            # Calculate technical indicators for bias calculation
            indicators = self.get_technical_indicators(ticker)
            
            # Calculate bias score using technical indicators
            bias_score = 0
            
            # RSI contribution to bias
            rsi = indicators.get('rsi', 50)
            if rsi > 70:  # Overbought
                bias_score -= 0.15  # Bearish bias
            elif rsi < 30:  # Oversold
                bias_score += 0.15  # Bullish bias
            
            # MACD contribution to bias
            macd = indicators.get('macd', 0)
            macd_signal = indicators.get('macd_signal', 0)
            if macd > macd_signal:
                bias_score += 0.1  # Bullish momentum
            else:
                bias_score -= 0.1  # Bearish momentum
            
            # Moving average contribution
            ma_20 = indicators.get('ma_20', current_price)
            if current_price > ma_20:
                bias_score += 0.1  # Price above MA20 is bullish
            else:
                bias_score -= 0.1  # Price below MA20 is bearish
            
            # Price momentum contribution
            momentum = indicators.get('momentum', 0)
            if momentum > 2:
                bias_score += 0.1  # Strong upward momentum
            elif momentum < -2:
                bias_score -= 0.1  # Strong downward momentum
            
            # Convert bias score to probability (centered at 0.5)
            bias_prob = 0.5 + (bias_score * 0.5)
            bias_prob = max(0.1, min(0.9, bias_prob))  # Clamp between 0.1 and 0.9
            
            # Calculate target zone based on current price and bias
            # More bullish = higher target, more bearish = lower target
            bias_adjustment = current_price * bias_score * 0.01  # 1% per 0.1 bias_score
            target_zone = current_price + bias_adjustment
            
            return {
                'current_price': current_price,
                'range_68': range_68,
                'target_zone': target_zone,
                'bias_prob': bias_prob
            }
            
        except Exception as e:
            print(f"Error calculating parameters for {ticker}: {e}")
            return None
    
    def refresh_watchlist(self):
        """
        Refresh the watchlist with the latest market data.
        Call this method to update all ticker data before generating trade suggestions.
        """
        print("Refreshing watchlist with latest market data...")
        self.watchlist = self.generate_dynamic_watchlist()
        print(f"Watchlist refreshed with {len(self.watchlist)} tickers")
    
    def expand_watchlist_with_high_options_volume(self, min_additional_tickers: int = 5):
        """
        Expand the existing watchlist with additional tickers that have high options volume.
        This helps ensure we always have enough quality tickers to generate suggestions.
        
        Args:
            min_additional_tickers: Minimum number of additional tickers to add
        """
        # In a production environment, this would query an API for high options volume
        # For this implementation, we'll add additional tickers known for options liquidity
        potential_additions = [
            'JPM', 'BAC', 'C', 'WFC',  # Banks
            'XLF', 'XLK', 'XLV', 'XLU', 'XLI',  # Sector ETFs
            'BABA', 'JD', 'PDD',  # China tech
            'UBER', 'LYFT', 'DASH',  # Gig economy
            'COIN', 'SQ', 'PYPL',  # Fintech
            'ROKU', 'DIS', 'CMCSA',  # Media
            'MU', 'TSM', 'QCOM',  # Semiconductors
            'F', 'GM', 'NIO'  # Auto
        ]
        
        print(f"Expanding watchlist with high options volume tickers...")
        added_count = 0
        
        for ticker in potential_additions:
            if ticker in self.watchlist:
                continue  # Skip if already in watchlist
                
            ticker_data = self._calculate_ticker_parameters(ticker)
            if ticker_data:
                self.watchlist[ticker] = ticker_data
                added_count += 1
                print(f"Added {ticker} to watchlist: Price=${ticker_data['current_price']:.2f}")
                
                if added_count >= min_additional_tickers:
                    break
        
        print(f"Expanded watchlist with {added_count} additional tickers. Total tickers: {len(self.watchlist)}")
