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
                    # Bull Put Spread - Use realistic strikes
                    short_strike = self.find_otm_strikes(current_price, 0.05, 'put')  # 5% OTM put
                    long_strike = self.find_otm_strikes(current_price, 0.10, 'put')   # 10% OTM put
                    
                    # Get option prices
                    expiration_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
                    option_prices = self.get_option_prices(ticker, [short_strike, long_strike], expiration_date, 'put')
                    
                    short_put_price = option_prices.get(f"PUT_{short_strike}", 0)
                    long_put_price = option_prices.get(f"PUT_{long_strike}", 0)
                    credit = short_put_price - long_put_price
                    max_loss = (short_strike - long_strike) - credit
                    
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
                        'expiration': expiration_date,
                        'confidence': min(90, 50 + bias_score * 100),
                        'legs': [
                            {'action': 'SELL', 'type': 'PUT', 'strike': short_strike, 'price': short_put_price},
                            {'action': 'BUY', 'type': 'PUT', 'strike': long_strike, 'price': long_put_price}
                        ]
                    })
                
                elif bias_score < -0.1:  # Bearish bias
                    # Bear Call Spread - Use realistic strikes  
                    short_strike = self.find_otm_strikes(current_price, 0.05, 'call')  # 5% OTM call
                    long_strike = self.find_otm_strikes(current_price, 0.10, 'call')   # 10% OTM call
                    
                    # Get option prices
                    expiration_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
                    option_prices = self.get_option_prices(ticker, [short_strike, long_strike], expiration_date, 'call')
                    
                    short_call_price = option_prices.get(f"CALL_{short_strike}", 0)
                    long_call_price = option_prices.get(f"CALL_{long_strike}", 0)
                    credit = short_call_price - long_call_price
                    max_loss = (long_strike - short_strike) - credit
                    
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
                        'expiration': expiration_date,
                        'confidence': min(90, 50 + abs(bias_score) * 100),
                        'legs': [
                            {'action': 'SELL', 'type': 'CALL', 'strike': short_strike, 'price': short_call_price},
                            {'action': 'BUY', 'type': 'CALL', 'strike': long_strike, 'price': long_call_price}
                        ]
                    })
                
                else:  # Neutral bias
                    # Iron Condor - Use realistic strikes
                    put_short = self.find_otm_strikes(current_price, 0.05, 'put')    # 5% OTM put
                    put_long = self.find_otm_strikes(current_price, 0.10, 'put')     # 10% OTM put  
                    call_short = self.find_otm_strikes(current_price, 0.05, 'call')  # 5% OTM call
                    call_long = self.find_otm_strikes(current_price, 0.10, 'call')   # 10% OTM call
                    
                    # Get option prices
                    expiration_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
                    strikes = [put_short, put_long, call_short, call_long]
                    option_prices = self.get_option_prices(ticker, strikes, expiration_date, 'both')
                    
                    put_short_price = option_prices.get(f"PUT_{put_short}", 0)
                    put_long_price = option_prices.get(f"PUT_{put_long}", 0)
                    call_short_price = option_prices.get(f"CALL_{call_short}", 0)
                    call_long_price = option_prices.get(f"CALL_{call_long}", 0)
                    
                    credit = (put_short_price - put_long_price) + (call_short_price - call_long_price)
                    max_loss = max((put_short - put_long), (call_long - call_short)) - credit
                    
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
                        'expiration': expiration_date,
                        'confidence': min(90, 60 + abs(0.5 - bullish_prob) * 100),
                        'legs': [
                            {'action': 'SELL', 'type': 'PUT', 'strike': put_short, 'price': put_short_price},
                            {'action': 'BUY', 'type': 'PUT', 'strike': put_long, 'price': put_long_price},
                            {'action': 'SELL', 'type': 'CALL', 'strike': call_short, 'price': call_short_price},
                            {'action': 'BUY', 'type': 'CALL', 'strike': call_long, 'price': call_long_price}
                        ]
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
        """Get estimated option prices for given strikes and expiration"""
        try:
            # Get stock data for volatility calculation
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1mo")
            
            if hist.empty:
                return {}
            
            current_price = hist['Close'].iloc[-1]
            volatility = hist['Close'].pct_change().std() * np.sqrt(252)
            
            # Days to expiration
            exp_date = datetime.strptime(expiration, '%Y-%m-%d')
            days_to_exp = (exp_date - datetime.now()).days
            time_to_exp = days_to_exp / 365.0
            
            # Simplified Black-Scholes approximation for option pricing
            option_prices = {}
            
            for strike in strikes:
                # Put price estimation
                if option_type in ['put', 'both']:
                    # Simplified intrinsic + time value with better estimates
                    put_intrinsic = max(0, strike - current_price)
                    
                    # Distance from current price affects time value
                    distance_factor = abs(strike - current_price) / current_price
                    time_value_multiplier = max(0.1, 1 - distance_factor * 2)  # Reduce for far OTM
                    
                    put_time_value = volatility * current_price * np.sqrt(time_to_exp) * 0.15 * time_value_multiplier
                    put_price = max(0.05, put_intrinsic + put_time_value)  # Minimum $0.05
                    option_prices[f"PUT_{strike}"] = put_price
                
                # Call price estimation
                if option_type in ['call', 'both']:
                    # Simplified intrinsic + time value with better estimates
                    call_intrinsic = max(0, current_price - strike)
                    
                    # Distance from current price affects time value
                    distance_factor = abs(strike - current_price) / current_price
                    time_value_multiplier = max(0.1, 1 - distance_factor * 2)  # Reduce for far OTM
                    
                    call_time_value = volatility * current_price * np.sqrt(time_to_exp) * 0.15 * time_value_multiplier
                    call_price = max(0.05, call_intrinsic + call_time_value)  # Minimum $0.05
                    option_prices[f"CALL_{strike}"] = call_price
            
            return option_prices
            
        except Exception as e:
            st.error(f"Error getting option prices for {ticker}: {e}")
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
    
    def find_otm_strikes(self, current_price: float, distance_pct: float, option_type: str) -> float:
        """Find realistic OTM strikes at approximately the given distance"""
        target_price = current_price * (1 + distance_pct if option_type == 'call' else 1 - distance_pct)
        
        # Get available strikes
        strike_chain = self.get_strike_chain(current_price, 20)
        
        if option_type == 'call':
            # Find first strike above target
            for strike in strike_chain:
                if strike >= target_price:
                    return strike
            return strike_chain[-1]  # Return highest if none found
        else:  # put
            # Find first strike below target
            for strike in reversed(strike_chain):
                if strike <= target_price:
                    return strike
            return strike_chain[0]  # Return lowest if none found
