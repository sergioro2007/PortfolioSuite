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

Version: 1.0.0
Last Updated: July 5, 2025
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
        self.trades_file = "options_trades.pkl"
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
        
        # Watchlist tickers with current forecast data
        self.watchlist = {
            'SPY': {'current_price': 620.45, 'range_68': (615, 635), 'target_zone': 625, 'bias_prob': 0.70},
            'QQQ': {'current_price': 550.80, 'range_68': (545, 572), 'target_zone': 559, 'bias_prob': 0.75},
            'AAPL': {'current_price': 212.44, 'range_68': (210, 220), 'target_zone': 215, 'bias_prob': 0.70},
            'MSFT': {'current_price': 491.09, 'range_68': (490, 507), 'target_zone': 498, 'bias_prob': 0.70},
            'NVDA': {'current_price': 157.25, 'range_68': (152, 166), 'target_zone': 160, 'bias_prob': 0.70},
            'TECL': {'current_price': 93.99, 'range_68': (85, 101), 'target_zone': 93, 'bias_prob': 0.70},
            'XLE': {'current_price': 86.93, 'range_68': (84, 90), 'target_zone': 87, 'bias_prob': 0.60},
            'SMH': {'current_price': 281.25, 'range_68': (255, 257), 'target_zone': 256, 'bias_prob': 0.60}
        }
    
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
    
    def generate_trade_suggestions(self, num_suggestions: int = 3) -> List[Dict]:
        """Generate new trade suggestions based on market analysis"""
        suggestions = []
        
        try:
            # Analyze each ticker for opportunities
            for ticker, forecast in self.watchlist.items():
                prediction = self.predict_price_range(ticker)
                if not prediction:
                    continue
                
                current_price = prediction['current_price']
                bullish_prob = prediction['bullish_probability']
                bias_score = prediction['bias_score']
                
                # Generate strategy suggestions based on bias
                if bias_score > 0.1:  # Bullish bias
                    # Bull Put Spread
                    short_strike = current_price * 0.95
                    long_strike = current_price * 0.90
                    credit = (short_strike - long_strike) * 0.3
                    max_loss = (short_strike - long_strike) * 100 - credit
                    
                    suggestions.append({
                        'ticker': ticker,
                        'strategy': 'Bull Put Spread',
                        'bias': 'Bullish',
                        'bullish_prob': bullish_prob,
                        'short_strike': short_strike,
                        'long_strike': long_strike,
                        'credit': credit,
                        'max_loss': max_loss,
                        'profit_target': credit * 0.5,
                        'expiration': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
                        'confidence': min(90, 50 + bias_score * 100)
                    })
                
                elif bias_score < -0.1:  # Bearish bias
                    # Bear Call Spread
                    short_strike = current_price * 1.05
                    long_strike = current_price * 1.10
                    credit = (long_strike - short_strike) * 0.3
                    max_loss = (long_strike - short_strike) * 100 - credit
                    
                    suggestions.append({
                        'ticker': ticker,
                        'strategy': 'Bear Call Spread',
                        'bias': 'Bearish',
                        'bullish_prob': bullish_prob,
                        'short_strike': short_strike,
                        'long_strike': long_strike,
                        'credit': credit,
                        'max_loss': max_loss,
                        'profit_target': credit * 0.5,
                        'expiration': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
                        'confidence': min(90, 50 + abs(bias_score) * 100)
                    })
                
                else:  # Neutral bias
                    # Iron Condor
                    put_short = current_price * 0.95
                    put_long = current_price * 0.90
                    call_short = current_price * 1.05
                    call_long = current_price * 1.10
                    
                    credit = ((put_short - put_long) + (call_long - call_short)) * 0.3
                    max_loss = max((put_short - put_long), (call_long - call_short)) * 100 - credit
                    
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
                        'profit_target': credit * 0.5,
                        'expiration': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
                        'confidence': min(90, 60 + abs(0.5 - bullish_prob) * 100)
                    })
            
            # Sort by confidence and return top suggestions
            suggestions.sort(key=lambda x: x['confidence'], reverse=True)
            return suggestions[:num_suggestions]
            
        except Exception as e:
            st.error(f"Error generating trade suggestions: {e}")
            return []
    
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
            return {'total_pnl': 0, 'avg_weekly': 0, 'win_rate': 0}
        
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
