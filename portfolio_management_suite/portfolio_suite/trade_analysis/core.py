"""
📈 Trade Analysis Core Module
============================

Core functionality for trade analysis and strategy generation.
This module provides tools for analyzing trading opportunities,
generating trade suggestions, and tracking trade performance.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
import yfinance as yf
import warnings

warnings.filterwarnings('ignore')


class TradeAnalyzer:
    """Main class for trade analysis and strategy generation"""
    
    def __init__(self):
        """Initialize the trade analyzer"""
        self.watchlist = {}
        self.trade_history = []
        self.performance_metrics = {}
        
    def analyze_symbol(self, symbol: str) -> Dict[str, Any]:
        """
        Analyze a single symbol for trading opportunities
        
        Args:
            symbol: Stock ticker symbol
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            ticker = yf.Ticker(symbol)
            
            # Get historical data
            hist = ticker.history(period="6mo")
            if hist.empty:
                return {"error": f"No data available for {symbol}"}
            
            # Basic technical analysis
            current_price = hist['Close'].iloc[-1]
            sma_20 = hist['Close'].rolling(20).mean().iloc[-1]
            sma_50 = hist['Close'].rolling(50).mean().iloc[-1]
            
            # Volatility analysis
            returns = hist['Close'].pct_change().dropna()
            volatility = returns.std() * np.sqrt(252)  # Annualized volatility
            
            # Support/resistance levels
            high_52w = hist['High'].max()
            low_52w = hist['Low'].min()
            
            analysis = {
                "symbol": symbol,
                "current_price": round(current_price, 2),
                "sma_20": round(sma_20, 2),
                "sma_50": round(sma_50, 2),
                "volatility": round(volatility, 4),
                "high_52w": round(high_52w, 2),
                "low_52w": round(low_52w, 2),
                "trend": self._determine_trend(current_price, sma_20, sma_50),
                "signal": self._generate_signal(current_price, sma_20, sma_50),
                "analysis_date": datetime.now().isoformat()
            }
            
            return analysis
            
        except Exception as e:
            return {"error": f"Error analyzing {symbol}: {str(e)}"}
    
    def _determine_trend(self, price: float, sma_20: float, sma_50: float) -> str:
        """Determine the current trend based on moving averages"""
        if price > sma_20 > sma_50:
            return "Bullish"
        elif price < sma_20 < sma_50:
            return "Bearish"
        else:
            return "Neutral"
    
    def _generate_signal(self, price: float, sma_20: float, sma_50: float) -> str:
        """Generate trading signal based on technical analysis"""
        if price > sma_20 and sma_20 > sma_50:
            return "BUY"
        elif price < sma_20 and sma_20 < sma_50:
            return "SELL"
        else:
            return "HOLD"
    
    def generate_trade_suggestions(self, symbols: List[str]) -> List[Dict[str, Any]]:
        """
        Generate trade suggestions for a list of symbols
        
        Args:
            symbols: List of ticker symbols to analyze
            
        Returns:
            List of trade suggestions
        """
        suggestions = []
        
        for symbol in symbols:
            analysis = self.analyze_symbol(symbol)
            
            if "error" not in analysis and analysis["signal"] == "BUY":
                suggestion = {
                    "symbol": symbol,
                    "action": "BUY",
                    "current_price": analysis["current_price"],
                    "target_price": analysis["current_price"] * 1.05,  # 5% target
                    "stop_loss": analysis["current_price"] * 0.95,     # 5% stop loss
                    "confidence": self._calculate_confidence(analysis),
                    "analysis": analysis
                }
                suggestions.append(suggestion)
        
        return sorted(suggestions, key=lambda x: x["confidence"], reverse=True)
    
    def _calculate_confidence(self, analysis: Dict[str, Any]) -> float:
        """Calculate confidence score for a trade suggestion"""
        confidence = 0.5  # Base confidence
        
        # Add confidence based on trend strength
        if analysis["trend"] == "Bullish":
            confidence += 0.2
        elif analysis["trend"] == "Bearish":
            confidence -= 0.2
        
        # Adjust for volatility (lower volatility = higher confidence)
        if analysis["volatility"] < 0.2:
            confidence += 0.1
        elif analysis["volatility"] > 0.4:
            confidence -= 0.1
        
        return min(max(confidence, 0.0), 1.0)  # Clamp between 0 and 1
    
    def track_trade_performance(self, trade_id: str, entry_price: float, 
                              exit_price: float, quantity: int) -> Dict[str, Any]:
        """
        Track the performance of a completed trade
        
        Args:
            trade_id: Unique identifier for the trade
            entry_price: Entry price per share
            exit_price: Exit price per share
            quantity: Number of shares traded
            
        Returns:
            Trade performance metrics
        """
        profit_loss = (exit_price - entry_price) * quantity
        return_pct = ((exit_price - entry_price) / entry_price) * 100
        
        performance = {
            "trade_id": trade_id,
            "entry_price": entry_price,
            "exit_price": exit_price,
            "quantity": quantity,
            "profit_loss": round(profit_loss, 2),
            "return_percentage": round(return_pct, 2),
            "trade_date": datetime.now().isoformat()
        }
        
        self.trade_history.append(performance)
        return performance
    
    def get_portfolio_summary(self) -> Dict[str, Any]:
        """Get a summary of portfolio performance"""
        if not self.trade_history:
            return {"message": "No trades recorded yet"}
        
        total_trades = len(self.trade_history)
        total_profit = sum(trade["profit_loss"] for trade in self.trade_history)
        winning_trades = len([t for t in self.trade_history if t["profit_loss"] > 0])
        win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
        
        return {
            "total_trades": total_trades,
            "total_profit": round(total_profit, 2),
            "winning_trades": winning_trades,
            "win_rate": round(win_rate, 2),
            "average_return": round(total_profit / total_trades, 2) if total_trades > 0 else 0
        }


def run_trade_analysis():
    """Main function to run trade analysis - for compatibility"""
    analyzer = TradeAnalyzer()
    
    # Default watchlist for analysis
    default_symbols = ['SPY', 'QQQ', 'AAPL', 'MSFT', 'GOOGL']
    
    print("🔍 Analyzing symbols...")
    suggestions = analyzer.generate_trade_suggestions(default_symbols)
    
    print(f"\n📈 Found {len(suggestions)} trade suggestions:")
    for suggestion in suggestions:
        print(f"- {suggestion['symbol']}: {suggestion['action']} at ${suggestion['current_price']}")
        print(f"  Target: ${suggestion['target_price']:.2f}, Stop: ${suggestion['stop_loss']:.2f}")
        print(f"  Confidence: {suggestion['confidence']:.2f}")
        print()
    
    return suggestions
