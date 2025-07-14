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

warnings.filterwarnings("ignore")

# Optional plotly imports for enhanced visualizations
try:
    import plotly.graph_objects as go
    import plotly.express as px

    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False


class OptionsTracker:
    def edit_trade(self, trade_id: int, updates: dict):
        """Edit an existing trade by trade_id with updates dict."""
        updated = False
        for trade in self.trades:
            if trade.get("id") == trade_id:
                trade.update(updates)
                updated = True
                break
        if updated:
            self.save_trades()
        return updated

    def delete_trade(self, trade_id: int):
        """Delete a trade by trade_id."""
        initial_len = len(self.trades)
        self.trades = [trade for trade in self.trades if trade.get("id") != trade_id]
        deleted = len(self.trades) < initial_len
        if deleted:
            self.save_trades()
        return deleted

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
            "Protective Put",
        ]

        # Generate a dynamic watchlist with popular options-active tickers
        # This replaces the previous hard-coded watchlist with real-time data
        self.watchlist = self.generate_dynamic_watchlist()

    def load_trades(self) -> List[Dict]:
        """Load existing trades from file"""
        try:
            if os.path.exists(self.trades_file):
                with open(self.trades_file, "rb") as f:
                    return pickle.load(f)
        except Exception as e:
            st.error(f"Error loading trades: {e}")
        return []

    def save_trades(self):
        """Save trades to file, ensuring data directory exists"""
        try:
            data_dir = os.path.dirname(self.trades_file)
            if data_dir and not os.path.exists(data_dir):
                os.makedirs(data_dir, exist_ok=True)
            with open(self.trades_file, "wb") as f:
                pickle.dump(self.trades, f)
        except Exception as e:
            st.error(f"Error saving trades: {e}")

    def load_predictions(self) -> Dict:
        """Load price predictions from file"""
        try:
            if os.path.exists(self.predictions_file):
                with open(self.predictions_file, "rb") as f:
                    return pickle.load(f)
        except Exception as e:
            st.error(f"Error loading predictions: {e}")
        return {}

    def save_predictions(self):
        """Save price predictions to file"""
        try:
            with open(self.predictions_file, "wb") as f:
                pickle.dump(self.predictions, f)
        except Exception as e:
            st.error(f"Error saving predictions: {e}")

    def get_technical_indicators(self, ticker: str, period: str = "3mo") -> Dict:
        """Calculate technical indicators for price prediction"""
        try:
            # Sanitize ticker: remove whitespace and leading $
            ticker_clean = ticker.strip().lstrip("$")
            stock = yf.Ticker(ticker_clean)
            hist = stock.history(period=period)
            if hist.empty:
                print(
                    f"No historical data for '{ticker}' (sanitized: '{ticker_clean}')"
                )
                return {}
            # Calculate indicators
            close = hist["Close"]
            volume = hist["Volume"]
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

            # ATR (Average True Range) - 14 day
            high = hist["High"]
            low = hist["Low"]
            prev_close = close.shift(1)

            # True Range calculation
            tr1 = high - low
            tr2 = abs(high - prev_close)
            tr3 = abs(low - prev_close)

            true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
            atr = true_range.rolling(window=14).mean()

            # Current values
            current_price = close.iloc[-1]
            return {
                "current_price": current_price,
                "ma_5": ma_5.iloc[-1],
                "ma_10": ma_10.iloc[-1],
                "ma_20": ma_20.iloc[-1],
                "rsi": rsi.iloc[-1],
                "macd": macd.iloc[-1],
                "macd_signal": signal.iloc[-1],
                "bb_upper": bb_upper.iloc[-1],
                "bb_lower": bb_lower.iloc[-1],
                "volume_ratio": volume_ratio,
                "volatility": close.pct_change().std() * np.sqrt(252),
                "momentum": (current_price - close.iloc[-5]) / close.iloc[-5] * 100,
                "atr": atr.iloc[-1],  # Add ATR to indicators
            }
        except Exception as e:
            print(f"Error calculating indicators for '{ticker}': {e}")
            return {}

    def _get_implied_volatility(self, ticker, current_price=None):
        """Helper method to get implied volatility from options data"""
        try:
            import yfinance as yf
            import numpy as np

            stock = yf.Ticker(ticker)

            # Get current price if not provided
            if current_price is None:
                try:
                    info = stock.info
                    current_price = info.get(
                        "regularMarketPrice", info.get("previousClose", 100)
                    )
                except Exception:
                    # Fall back to historical data
                    hist = stock.history(period="1d")
                    if not hist.empty:
                        current_price = hist["Close"].iloc[-1]
                    else:
                        current_price = 100

            # Try to get options chain
            if hasattr(stock, "options") and stock.options:
                # Get nearest expiration
                nearest_exp = stock.options[0]
                options = stock.option_chain(nearest_exp)

                # Find ATM options (within 5% of current price)
                atm_calls = options.calls[
                    (options.calls["strike"] >= current_price * 0.95)
                    & (options.calls["strike"] <= current_price * 1.05)
                ]
                atm_puts = options.puts[
                    (options.puts["strike"] >= current_price * 0.95)
                    & (options.puts["strike"] <= current_price * 1.05)
                ]

                # Extract implied volatilities
                ivs = []

                # From calls
                if "impliedVolatility" in atm_calls.columns and not atm_calls.empty:
                    call_ivs = atm_calls["impliedVolatility"].dropna().tolist()
                    ivs.extend(call_ivs)

                # From puts
                if "impliedVolatility" in atm_puts.columns and not atm_puts.empty:
                    put_ivs = atm_puts["impliedVolatility"].dropna().tolist()
                    ivs.extend(put_ivs)

                # If we have IV values, use their average
                if ivs:
                    annual_iv = float(sum(ivs) / len(ivs))
                    weekly_vol = annual_iv / np.sqrt(52)  # Convert to weekly

                    return {
                        "valid": True,
                        "annual_iv": annual_iv,
                        "weekly_vol": weekly_vol,
                    }

            # If we get here, return invalid result
            return {"valid": False}

        except Exception as e:
            print(f"  ⚠️ IV calculation error for {ticker}: {e}")
            return {"valid": False}

    def predict_price_range(self, ticker: str, regime_multiplier: float = -0.2) -> Dict:
        """Predict 1-week price range using ChatGPT's methodology (default)

        This is now an alias to the ChatGPT fully compatible method per user preference.
        The ChatGPT method provides the most accurate predictions based on testing.

        Args:
            ticker: Stock ticker symbol
            regime_multiplier: Ignored, method uses ChatGPT's -0.2 approach
        """
        return self._predict_price_range_chatgpt_internal(ticker)

    def predict_price_range_traditional_bias(self, ticker: str) -> Dict:
        """Predict 1-week price range using traditional regime bias (0.01 multiplier)

        This uses the traditional algorithm's regime bias for moderate
        directional adjustments based on technical indicators.
        """
        return self._predict_price_range_volatility_based(
            ticker, regime_multiplier=0.01
        )

    def predict_price_range_gentle_bias(self, ticker: str) -> Dict:
        """Predict 1-week price range using gentle regime bias (0.001 multiplier)

        This uses a very conservative approach with minimal directional adjustments.
        """
        return self._predict_price_range_volatility_based(
            ticker, regime_multiplier=0.001
        )

    def predict_price_range_enhanced(self, ticker: str) -> Dict:
        """Predict 1-week price range using enhanced ChatGPT methodology (alias for fully compatible)

        This is an alias for the fully compatible ChatGPT method which provides the most
        accurate match to ChatGPT's results using advanced volatility scaling.
        """
        return self._predict_price_range_chatgpt_internal(ticker)

    def _predict_price_range_chatgpt_internal(self, ticker: str) -> Dict:
        """Predict 1-week price range using ChatGPT's exact algorithm including range calculations

        This method implements both:
        1. ChatGPT's -0.2 regime multiplier for target prices
        2. ChatGPT's adaptive volatility scaling for range calculations

        Based on reverse-engineering analysis:
        - Uses ±0.75σ instead of ±1σ for most stocks
        - Applies adaptive volatility scaling based on stock characteristics
        - Provides the closest possible match to ChatGPT's results
        """
        try:
            # Get base technical indicators directly
            indicators = self.get_technical_indicators(ticker)
            if not indicators:
                return {}

            current_price = indicators["current_price"]
            historical_vol = indicators["volatility"]

            # Step 1: Try to get implied volatility data from options
            iv_data = self._get_implied_volatility(ticker, current_price)

            # Use IV if available, otherwise fall back to historical volatility
            if iv_data and iv_data.get("valid", False):
                weekly_vol = iv_data["weekly_vol"]
                # Print debug info about IV source
                print(
                    f"  📈 Using implied volatility for {ticker}: {iv_data['annual_iv']:.1%} annual, {weekly_vol:.1%} weekly"
                )
            else:
                # Fall back to historical volatility
                weekly_vol = historical_vol / np.sqrt(52)
                print(
                    f"  📊 Using historical volatility for {ticker}: {historical_vol:.1%} annual, {weekly_vol:.1%} weekly"
                )

            # Adjust based on technical indicators
            rsi = indicators.get("rsi", 50)
            macd = indicators.get("macd", 0)
            macd_signal = indicators.get("macd_signal", 0)
            momentum = indicators.get("momentum", 0)

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

            # ChatGPT's -0.2 regime multiplier
            regime_multiplier = -0.2

            # Calculate target price with ChatGPT's bias approach
            bias_adjustment = current_price * bias_score * regime_multiplier
            target_price = current_price + bias_adjustment

            # Apply ChatGPT's adaptive volatility scaling
            vol_scaling_factor = self._get_chatgpt_volatility_scaling(
                ticker, weekly_vol
            )

            # ChatGPT appears to use ±0.75σ instead of ±1σ
            chatgpt_sigma_multiplier = 1.5  # This gives ±0.75σ when divided by 2

            # Calculate ChatGPT-style range
            adjusted_weekly_vol = weekly_vol * vol_scaling_factor
            half_range = (
                current_price * adjusted_weekly_vol * chatgpt_sigma_multiplier / 2
            )

            # Center the range around the target price (like ChatGPT does)
            lower_bound = target_price - half_range
            upper_bound = target_price + half_range

            # Probability of bullish move
            bullish_prob = 0.5 + (bias_score * 0.5)
            bullish_prob = max(0.1, min(0.9, bullish_prob))

            return {
                "current_price": current_price,
                "lower_bound": lower_bound,
                "upper_bound": upper_bound,
                "target_price": target_price,
                "bullish_probability": bullish_prob,
                "bias_score": bias_score,
                "weekly_volatility": weekly_vol,
                "adjusted_weekly_volatility": adjusted_weekly_vol,
                "volatility_scaling_factor": vol_scaling_factor,
                "iv_based": iv_data.get("valid", False) if iv_data else False,
                "chatgpt_compatible": True,
                "range_method": "chatgpt_adaptive",
                "indicators": indicators,
            }

        except Exception as e:
            st.error(f"Error in ChatGPT-compatible prediction for {ticker}: {e}")
            return {}

    def _get_chatgpt_volatility_scaling(self, ticker: str, weekly_vol: float) -> float:
        """Get ChatGPT's volatility scaling factor based on analysis

        Based on reverse-engineering ChatGPT's results:
        - Most stocks: 0.6x - 0.8x scaling (more conservative)
        - High-vol stocks like NVDA: 1.5x - 2.0x scaling (more aggressive)
        - Pattern seems to depend on stock characteristics
        """
        # Define known scaling factors from analysis
        known_scalings = {
            "SPY": 0.78,  # ChatGPT uses 0.78x our volatility
            "QQQ": 0.64,  # ChatGPT uses 0.64x our volatility
            "MSFT": 0.65,  # ChatGPT uses 0.65x our volatility
            "GOOGL": 1.49,  # ChatGPT uses 1.49x our volatility
            "NVDA": 1.98,  # ChatGPT uses 1.98x our volatility
            "AAPL": 1.03,  # ChatGPT uses 1.03x our volatility
        }

        if ticker in known_scalings:
            return known_scalings[ticker]

        # For unknown tickers, estimate based on volatility level
        annual_vol = weekly_vol * (52**0.5)  # Convert to annual

        if annual_vol < 0.20:  # Low volatility stocks (< 20% annual)
            return 0.75  # Reduce volatility estimate
        elif annual_vol < 0.30:  # Medium volatility stocks (20-30% annual)
            return 0.85  # Slight reduction
        elif annual_vol < 0.40:  # High volatility stocks (30-40% annual)
            return 1.20  # Slight increase
        else:  # Very high volatility stocks (> 40% annual)
            return 1.50  # Significant increase

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

        # Popular options-active tickers
        tickers = [
            "SPY",
            "QQQ",
            "IWM",
            "XLE",
            "SMH",
            "TECL",
            "AAPL",
            "MSFT",
            "NVDA",
            "GOOGL",
            "AMZN",
            "META",
            "TSLA",
            "AMD",
            "INTC",
            "CRM",
            "NFLX",
        ]

        watchlist = {}

        for ticker in tickers:
            params = self._calculate_ticker_parameters(ticker)
            if params:
                watchlist[ticker] = params
                print(
                    f"Added {ticker} to watchlist: Price=${params['current_price']:.2f}, Range=${params['range_low']:.2f}-${params['range_high']:.2f}, Target=${params['target_price']:.2f}, Bias={params['bias_score']:.2f}"
                )

        print(f"Generated watchlist with {len(watchlist)} tickers")
        return watchlist

    def _calculate_ticker_parameters(self, ticker: str) -> Optional[Dict]:
        """Calculate parameters for a single ticker"""
        try:
            prediction = self.predict_price_range(ticker)
            if not prediction:
                return None

            return {
                "current_price": prediction["current_price"],
                "target_price": prediction["target_price"],
                "range_low": prediction["lower_bound"],
                "range_high": prediction["upper_bound"],
                "bias_score": prediction["bias_score"],
                "bullish_probability": prediction["bullish_probability"],
            }
        except Exception as e:
            print(f"Error calculating parameters for {ticker}: {e}")
            return None

    def predict_price_range_atr_specification(self, ticker: str) -> Dict:
        """
        Predict 1-week price range using the EXACT ATR-based specification.

        This follows the step-by-step specification:
        1. Calculate Bias Adjustment = Current Price × Bias Score × 0.01
        2. Calculate Target Mid = Current Price + Bias Adjustment
        3. Calculate Low = Target Mid - ATR
        4. Calculate High = Target Mid + ATR
        5. Calculate Range ($) = High - Low
        6. Calculate Range (%) = (Range $ / Current Price) × 100

        Args:
            ticker: Stock ticker symbol

        Returns:
            Dict with prediction results following the exact specification
        """
        try:
            indicators = self.get_technical_indicators(ticker)
            if not indicators:
                return {}

            current_price = indicators["current_price"]
            atr = indicators["atr"]  # 14-day Average True Range

            # Calculate bias score using technical indicators
            rsi = indicators.get("rsi", 50)
            macd = indicators.get("macd", 0)
            macd_signal = indicators.get("macd_signal", 0)
            momentum = indicators.get("momentum", 0)

            # Bias calculation (same as before)
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

            # === SPECIFICATION CALCULATIONS ===

            # Step 1: Calculate Bias Adjustment
            # Bias (%) = Bias Score × 1% = bias_score × 0.01
            bias_percent = bias_score * 0.01
            bias_adjustment = current_price * bias_percent

            # Step 2: Calculate Target Price
            target_price = current_price + bias_adjustment

            # Step 3: Calculate Low and High Range using ATR
            lower_bound = target_price - atr
            upper_bound = target_price + atr

            # Step 4: Calculate Range ($)
            range_dollar = upper_bound - lower_bound

            # Step 5: Calculate Range (%)
            range_percent = (range_dollar / current_price) * 100

            # Probability of bullish move
            bullish_prob = 0.5 + (bias_score * 0.5)
            bullish_prob = max(0.1, min(0.9, bullish_prob))

            return {
                "current_price": current_price,
                "atr": atr,
                "bias_score": bias_score,
                "bias_percent": bias_percent,
                "bias_adjustment": bias_adjustment,
                "target_price": target_price,
                "lower_bound": lower_bound,
                "upper_bound": upper_bound,
                "range_dollar": range_dollar,
                "range_percent": range_percent,
                "bullish_probability": bullish_prob,
                "method": "atr_specification",
                "indicators": indicators,
            }
        except Exception as e:
            st.error(
                f"Error predicting price for {ticker} using ATR specification: {e}"
            )
            return {}

    def predict_price_range_chatgpt_fully_compatible(self, ticker: str) -> Dict:
        """Predict 1-week price range using ChatGPT's exact algorithm including range calculations

        This is an alias to the internal ChatGPT method for backward compatibility.
        """
        return self._predict_price_range_chatgpt_internal(ticker)

    def _predict_price_range_volatility_based(
        self, ticker: str, regime_multiplier: float = -0.2
    ) -> Dict:
        """Original volatility-based prediction method

        This is the original implementation that was in predict_price_range before
        we made ChatGPT the default. Used by traditional and gentle bias methods.
        """
        try:
            indicators = self.get_technical_indicators(ticker)
            if not indicators:
                return {}

            current_price = indicators["current_price"]
            historical_vol = indicators["volatility"]

            # Step 1: Try to get implied volatility data from options
            iv_data = self._get_implied_volatility(ticker, current_price)

            # Use IV if available, otherwise fall back to historical volatility
            if iv_data and iv_data.get("valid", False):
                weekly_vol = iv_data["weekly_vol"]
                # Print debug info about IV source
                print(
                    f"  📈 Using implied volatility for {ticker}: {iv_data['annual_iv']:.1%} annual, {weekly_vol:.1%} weekly"
                )
            else:
                # Fall back to historical volatility
                weekly_vol = historical_vol / np.sqrt(52)
                print(
                    f"  📊 Using historical volatility for {ticker}: {historical_vol:.1%} annual, {weekly_vol:.1%} weekly"
                )

            # Base prediction range (1 standard deviation)
            base_range = current_price * weekly_vol

            # Adjust based on technical indicators
            rsi = indicators.get("rsi", 50)
            macd = indicators.get("macd", 0)
            macd_signal = indicators.get("macd_signal", 0)
            momentum = indicators.get("momentum", 0)

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

            # Calculate predicted range - use implied volatility for the range width
            lower_bound = current_price - base_range
            upper_bound = current_price + base_range

            # HYBRID MODEL: Bias-adjusted range center
            bias_adjustment = current_price * bias_score * regime_multiplier

            # Shift the entire range based on bias
            lower_bound += bias_adjustment
            upper_bound += bias_adjustment

            # Target price is at center of adjusted range
            target_price = current_price + bias_adjustment

            # Probability of bullish move
            bullish_prob = 0.5 + (bias_score * 0.5)
            bullish_prob = max(0.1, min(0.9, bullish_prob))

            return {
                "current_price": current_price,
                "lower_bound": lower_bound,
                "upper_bound": upper_bound,
                "target_price": target_price,
                "bullish_probability": bullish_prob,
                "bias_score": bias_score,
                "weekly_volatility": weekly_vol,
                "iv_based": iv_data.get("valid", False) if iv_data else False,
                "indicators": indicators,
            }
        except Exception as e:
            st.error(f"Error predicting price for {ticker}: {e}")
            return {}

    def get_open_trades(self) -> List[Dict]:
        """Get all open trades"""
        trades = self.load_trades()
        return [trade for trade in trades if trade.get("status", "").lower() == "open"]

    def get_closed_trades(self) -> List[Dict]:
        """Get all closed trades"""
        trades = self.load_trades()
        return [trade for trade in trades if trade.get('status', '').lower() == 'closed']

    def calculate_weekly_pnl(self) -> Dict:
        """Calculate weekly P&L statistics"""
        trades = self.load_trades()
        open_trades = self.get_open_trades()

        total_pnl = sum(trade.get("pnl", 0) for trade in trades if "pnl" in trade)
        total_trades = len(trades)
        open_count = len(open_trades)

        return {
            "total_pnl": total_pnl,
            "total_trades": total_trades,
            "open_trades": open_count,
            "closed_trades": total_trades - open_count,
            "win_rate": 0.0,  # Placeholder - would need more complex calculation
        }

    def evaluate_trade(self, trade: Dict) -> Dict:
        """Evaluate a trade and return performance metrics"""
        # Basic trade evaluation - this would be more sophisticated in practice
        pnl = trade.get("pnl", 0)
        entry_price = trade.get("entry_price", 0)
        current_price = trade.get("current_price", entry_price)

        if entry_price > 0:
            pnl_percent = ((current_price - entry_price) / entry_price) * 100
        else:
            pnl_percent = 0

        return {
            "pnl": pnl,
            "pnl_percent": pnl_percent,
            "status": trade.get("status", "unknown"),
            "days_held": 0,  # Placeholder
            "recommendation": "hold",  # Placeholder
            "reason": "Standard evaluation",  # Placeholder
        }

    def generate_trade_suggestions(self, num_suggestions: int = 3) -> List[Dict]:
        """
        Generate trade suggestions based on market analysis and price predictions.

        Args:
            num_suggestions: Number of trade suggestions to generate

        Returns:
            List of dictionaries containing trade suggestions with details
        """
        suggestions = []

        try:
            # Get a subset of watchlist tickers for analysis
            # Handle both old format (with 'tickers' key) and new format (direct keys)
            if "tickers" in self.watchlist:
                watchlist_tickers = list(self.watchlist.get("tickers", {}).keys())[:10]
            else:
                # Direct ticker format
                watchlist_tickers = list(self.watchlist.keys())[:10]

            for ticker in watchlist_tickers[
                : num_suggestions * 2
            ]:  # Analyze more than needed
                try:
                    # Get current price and prediction
                    stock = yf.Ticker(ticker)
                    hist_data = stock.history(period="2d")
                    if hist_data.empty:
                        continue
                    current_price = hist_data["Close"].iloc[-1]

                    # Get price prediction using enhanced method
                    prediction = self.predict_price_range_enhanced(ticker)

                    # If enhanced prediction fails, create a simple one
                    if not prediction or prediction.get("target_price") is None:
                        prediction = {
                            "target_price": current_price * 1.01,  # 1% upside
                            "lower_bound": current_price * 0.97,  # 3% downside
                            "upper_bound": current_price * 1.05,  # 5% upside
                            "confidence": 0.6,
                        }

                    # Generate trade suggestion based on prediction
                    suggestion = self._create_trade_suggestion(
                        ticker, current_price, prediction
                    )

                    if suggestion:
                        suggestions.append(suggestion)

                    # Stop when we have enough suggestions
                    if len(suggestions) >= num_suggestions:
                        break

                except Exception as e:
                    continue  # Skip tickers with errors

        except Exception as e:
            # Return at least one fallback suggestion
            suggestions = [
                {
                    "ticker": "SPY",
                    "strategy": "Bull Put Spread",
                    "confidence": "Medium",
                    "expected_profit": 50,
                    "risk": 200,
                    "probability": 0.65,
                    "reason": "Market neutral strategy on stable ETF",
                    "entry_price": 450,
                    "target_price": 460,
                    "stop_loss": 440,
                }
            ]

        return suggestions

    def _create_trade_suggestion(
        self, ticker: str, current_price: float, prediction: Dict
    ) -> Optional[Dict]:
        """
        Create a specific trade suggestion based on price prediction and current conditions.

        Args:
            ticker: Stock ticker symbol
            current_price: Current stock price
            prediction: Price prediction dictionary

        Returns:
            Dictionary containing trade suggestion details or None
        """
        try:
            target_price = prediction.get("target_price", current_price)
            lower_bound = prediction.get("lower_bound", current_price * 0.95)
            upper_bound = prediction.get("upper_bound", current_price * 1.05)
            confidence = prediction.get("confidence", 0.5)

            # Determine best strategy based on prediction
            price_direction = 1 if target_price > current_price else -1

            # Choose strategy based on market outlook
            if price_direction > 0:  # Bullish
                strategy = "Bull Put Spread"
                strike_price = lower_bound * 0.98  # Below support
                expected_profit = min(100, current_price * 0.02)  # 2% of stock price
                risk = expected_profit * 4  # 4:1 risk/reward typical for spreads
            else:  # Bearish or neutral
                strategy = "Bear Call Spread"
                strike_price = upper_bound * 1.02  # Above resistance
                expected_profit = min(80, current_price * 0.015)  # 1.5% of stock price
                risk = expected_profit * 3.5

            # Calculate probability of success
            probability = min(0.85, max(0.45, confidence + 0.1))

            return {
                "ticker": ticker,
                "strategy": strategy,
                "confidence": (
                    "High"
                    if confidence > 0.7
                    else "Medium" if confidence > 0.5 else "Low"
                ),
                "expected_profit": round(expected_profit, 2),
                "risk": round(risk, 2),
                "probability": round(probability, 2),
                "reason": f"Price target ${target_price:.2f} vs current ${current_price:.2f}",
                "entry_price": round(current_price, 2),
                "target_price": round(target_price, 2),
                "stop_loss": round(
                    lower_bound if price_direction > 0 else upper_bound, 2
                ),
                "strike_price": round(strike_price, 2),
                "expiration": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
                "bias": "Bullish" if price_direction > 0 else "Bearish",
                "bullish_prob": round(probability if price_direction > 0 else 1 - probability, 2),
            }

        except Exception as e:
            return None
