"""
📊 Trade Repository Core
=======================

Core functionality for trade management and analysis.
"""

import json
import csv
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Trade:
    """Represents a single trade with all relevant data"""
    
    def __init__(self, symbol: str, action: str, quantity: int, price: float, 
                 trade_date: Optional[str] = None, trade_id: Optional[str] = None):
        self.trade_id = trade_id or f"{symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.symbol = symbol.upper()
        self.action = action.upper()  # BUY, SELL
        self.quantity = quantity
        self.price = price
        self.trade_date = trade_date or datetime.now().isoformat()
        self.total_value = quantity * price
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert trade to dictionary"""
        return {
            'trade_id': self.trade_id,
            'symbol': self.symbol,
            'action': self.action,
            'quantity': self.quantity,
            'price': self.price,
            'total_value': self.total_value,
            'trade_date': self.trade_date
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Trade':
        """Create trade from dictionary"""
        return cls(
            symbol=data['symbol'],
            action=data['action'],
            quantity=data['quantity'],
            price=data['price'],
            trade_date=data.get('trade_date'),
            trade_id=data.get('trade_id')
        )


class TradeRepository:
    """Repository for managing trade data"""
    
    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = Path(data_dir) if data_dir else Path("data/trades")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.trades_file = self.data_dir / "trades.json"
        self.csv_file = self.data_dir / "Trading_Memory_Summary_2025-06-26.csv"
        self._trades: List[Trade] = []
        self._load_trades()
    
    def _load_trades(self):
        """Load trades from storage"""
        if self.trades_file.exists():
            try:
                with open(self.trades_file, 'r') as f:
                    trades_data = json.load(f)
                    self._trades = [Trade.from_dict(data) for data in trades_data]
                logger.info(f"Loaded {len(self._trades)} trades from storage")
            except Exception as e:
                logger.error(f"Error loading trades: {e}")
                self._trades = []
    
    def _save_trades(self):
        """Save trades to storage"""
        try:
            trades_data = [trade.to_dict() for trade in self._trades]
            with open(self.trades_file, 'w') as f:
                json.dump(trades_data, f, indent=2)
            logger.info(f"Saved {len(self._trades)} trades to storage")
        except Exception as e:
            logger.error(f"Error saving trades: {e}")
    
    def add_trade(self, trade: Trade) -> bool:
        """Add a new trade"""
        try:
            self._trades.append(trade)
            self._save_trades()
            self._update_csv_summary()
            logger.info(f"Added trade: {trade.symbol} {trade.action} {trade.quantity}@{trade.price}")
            return True
        except Exception as e:
            logger.error(f"Error adding trade: {e}")
            return False
    
    def get_trades(self, symbol: Optional[str] = None, 
                  start_date: Optional[str] = None,
                  end_date: Optional[str] = None) -> List[Trade]:
        """Get trades with optional filtering"""
        filtered_trades = self._trades
        
        if symbol:
            filtered_trades = [t for t in filtered_trades if t.symbol == symbol.upper()]
        
        if start_date:
            filtered_trades = [t for t in filtered_trades if t.trade_date >= start_date]
        
        if end_date:
            filtered_trades = [t for t in filtered_trades if t.trade_date <= end_date]
        
        return filtered_trades
    
    def get_positions(self) -> Dict[str, Dict[str, Any]]:
        """Get current positions for all symbols"""
        positions = {}
        
        for trade in self._trades:
            symbol = trade.symbol
            if symbol not in positions:
                positions[symbol] = {'quantity': 0, 'total_cost': 0, 'avg_price': 0}
            
            if trade.action == 'BUY':
                positions[symbol]['quantity'] += trade.quantity
                positions[symbol]['total_cost'] += trade.total_value
            elif trade.action == 'SELL':
                positions[symbol]['quantity'] -= trade.quantity
                positions[symbol]['total_cost'] -= trade.total_value
        
        # Calculate average prices
        for symbol, position in positions.items():
            if position['quantity'] > 0:
                position['avg_price'] = position['total_cost'] / position['quantity']
            else:
                position['avg_price'] = 0
        
        # Filter out zero positions
        return {k: v for k, v in positions.items() if v['quantity'] != 0}
    
    def _update_csv_summary(self):
        """Update the CSV summary file"""
        try:
            with open(self.csv_file, 'w', newline='') as f:
                writer = csv.writer(f)
                
                # Write header
                writer.writerow([
                    'Date', 'Symbol', 'Action', 'Quantity', 'Price', 
                    'Total Value', 'Trade ID', 'Running P&L'
                ])
                
                running_pnl = 0
                for trade in sorted(self._trades, key=lambda x: x.trade_date):
                    # Simple P&L calculation (this would be more complex in reality)
                    if trade.action == 'SELL':
                        running_pnl += trade.total_value
                    else:
                        running_pnl -= trade.total_value
                    
                    writer.writerow([
                        trade.trade_date.split('T')[0],  # Date only
                        trade.symbol,
                        trade.action,
                        trade.quantity,
                        f"${trade.price:.2f}",
                        f"${trade.total_value:.2f}",
                        trade.trade_id,
                        f"${running_pnl:.2f}"
                    ])
                
            logger.info(f"Updated CSV summary at {self.csv_file}")
        except Exception as e:
            logger.error(f"Error updating CSV summary: {e}")


class TradeManager:
    """High-level trade management interface"""
    
    def __init__(self, repository: Optional[TradeRepository] = None):
        self.repository = repository or TradeRepository()
    
    def execute_trade(self, symbol: str, action: str, quantity: int, price: float) -> bool:
        """Execute a trade"""
        trade = Trade(symbol, action, quantity, price)
        return self.repository.add_trade(trade)
    
    def get_portfolio_value(self, current_prices: Dict[str, float]) -> float:
        """Calculate current portfolio value"""
        positions = self.repository.get_positions()
        total_value = 0
        
        for symbol, position in positions.items():
            if symbol in current_prices:
                total_value += position['quantity'] * current_prices[symbol]
        
        return total_value
    
    def get_trade_summary(self) -> Dict[str, Any]:
        """Get comprehensive trade summary"""
        trades = self.repository.get_trades()
        positions = self.repository.get_positions()
        
        total_trades = len(trades)
        buy_trades = len([t for t in trades if t.action == 'BUY'])
        sell_trades = len([t for t in trades if t.action == 'SELL'])
        
        return {
            'total_trades': total_trades,
            'buy_trades': buy_trades,
            'sell_trades': sell_trades,
            'active_positions': len(positions),
            'symbols_traded': len(set(t.symbol for t in trades)),
            'date_range': {
                'first_trade': min((t.trade_date for t in trades), default=None),
                'last_trade': max((t.trade_date for t in trades), default=None)
            }
        }