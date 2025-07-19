"""
📊 Trade Memory Management
=========================

Module for managing trade memory, historical data, and trade summaries.
"""

import csv
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class TradeMemory:
    """Manages trade memory and historical summaries"""
    
    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = Path(data_dir) if data_dir else Path("data/trades")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.memory_file = self.data_dir / "Trading_Memory_Summary_2025-06-26.csv"
        self._initialize_memory_file()
    
    def _initialize_memory_file(self):
        """Initialize the trading memory CSV file with sample data"""
        if not self.memory_file.exists():
            self._create_sample_memory_data()
    
    def _create_sample_memory_data(self):
        """Create sample trading memory data"""
        try:
            with open(self.memory_file, 'w', newline='') as f:
                writer = csv.writer(f)
                
                # Write header
                writer.writerow([
                    'Date', 'Symbol', 'Action', 'Quantity', 'Price', 
                    'Total Value', 'Trade ID', 'Running P&L', 'Notes'
                ])
                
                # Sample trade data
                sample_trades = [
                    ['2025-06-01', 'AAPL', 'BUY', 100, '$150.25', '$15,025.00', 'AAPL_20250601_001', '-$15,025.00', 'Initial position'],
                    ['2025-06-02', 'MSFT', 'BUY', 50, '$300.75', '$15,037.50', 'MSFT_20250602_001', '-$30,062.50', 'Tech diversification'],
                    ['2025-06-03', 'GOOGL', 'BUY', 25, '$2,500.00', '$62,500.00', 'GOOGL_20250603_001', '-$92,562.50', 'Growth position'],
                    ['2025-06-05', 'AAPL', 'SELL', 50, '$155.00', '$7,750.00', 'AAPL_20250605_001', '-$84,812.50', 'Profit taking'],
                    ['2025-06-08', 'TSLA', 'BUY', 30, '$220.50', '$6,615.00', 'TSLA_20250608_001', '-$91,427.50', 'EV exposure'],
                    ['2025-06-10', 'SPY', 'BUY', 200, '$420.25', '$84,050.00', 'SPY_20250610_001', '-$175,477.50', 'Market hedge'],
                    ['2025-06-12', 'MSFT', 'SELL', 25, '$305.50', '$7,637.50', 'MSFT_20250612_001', '-$167,840.00', 'Partial profit'],
                    ['2025-06-15', 'QQQ', 'BUY', 75, '$350.00', '$26,250.00', 'QQQ_20250615_001', '-$194,090.00', 'Tech ETF'],
                    ['2025-06-18', 'GOOGL', 'SELL', 10, '$2,550.00', '$25,500.00', 'GOOGL_20250618_001', '-$168,590.00', 'Rebalancing'],
                    ['2025-06-20', 'NVDA', 'BUY', 20, '$450.00', '$9,000.00', 'NVDA_20250620_001', '-$177,590.00', 'AI exposure'],
                    ['2025-06-22', 'AAPL', 'SELL', 50, '$158.75', '$7,937.50', 'AAPL_20250622_001', '-$169,652.50', 'Final AAPL exit'],
                    ['2025-06-25', 'SPY', 'SELL', 100, '$425.00', '$42,500.00', 'SPY_20250625_001', '-$127,152.50', 'Hedge reduction'],
                ]
                
                for trade in sample_trades:
                    writer.writerow(trade)
                
            logger.info(f"Created sample trading memory data at {self.memory_file}")
            
        except Exception as e:
            logger.error(f"Error creating sample memory data: {e}")
    
    def load_memory_data(self) -> List[Dict[str, Any]]:
        """Load trading memory data from CSV"""
        trades = []
        
        try:
            with open(self.memory_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    trades.append(dict(row))
            
            logger.info(f"Loaded {len(trades)} trades from memory")
            return trades
            
        except Exception as e:
            logger.error(f"Error loading memory data: {e}")
            return []
    
    def analyze_memory_performance(self) -> Dict[str, Any]:
        """Analyze performance from memory data"""
        trades = self.load_memory_data()
        
        if not trades:
            return {"error": "No trade data available"}
        
        # Parse trading data
        symbols = set()
        total_buy_value = 0
        total_sell_value = 0
        trade_count = len(trades)
        
        for trade in trades:
            symbols.add(trade['Symbol'])
            
            # Parse price and total value (remove $ and commas)
            total_value_str = trade['Total Value'].replace('$', '').replace(',', '')
            total_value = float(total_value_str)
            
            if trade['Action'] == 'BUY':
                total_buy_value += total_value
            elif trade['Action'] == 'SELL':
                total_sell_value += total_value
        
        # Calculate metrics
        net_invested = total_buy_value - total_sell_value
        realized_pnl = total_sell_value - total_buy_value if total_buy_value > 0 else 0
        
        # Get final P&L from last trade
        final_pnl_str = trades[-1]['Running P&L'].replace('$', '').replace(',', '')
        final_pnl = float(final_pnl_str)
        
        return {
            'total_trades': trade_count,
            'unique_symbols': len(symbols),
            'symbols_traded': list(symbols),
            'total_buy_value': total_buy_value,
            'total_sell_value': total_sell_value,
            'net_invested': net_invested,
            'realized_pnl': realized_pnl,
            'final_running_pnl': final_pnl,
            'date_range': {
                'start': trades[0]['Date'] if trades else None,
                'end': trades[-1]['Date'] if trades else None
            }
        }
    
    def get_symbol_performance(self, symbol: str) -> Dict[str, Any]:
        """Get performance for a specific symbol"""
        trades = self.load_memory_data()
        symbol_trades = [t for t in trades if t['Symbol'] == symbol]
        
        if not symbol_trades:
            return {"error": f"No trades found for {symbol}"}
        
        buy_trades = [t for t in symbol_trades if t['Action'] == 'BUY']
        sell_trades = [t for t in symbol_trades if t['Action'] == 'SELL']
        
        total_bought = sum(float(t['Total Value'].replace('$', '').replace(',', '')) 
                          for t in buy_trades)
        total_sold = sum(float(t['Total Value'].replace('$', '').replace(',', '')) 
                        for t in sell_trades)
        
        return {
            'symbol': symbol,
            'total_trades': len(symbol_trades),
            'buy_trades': len(buy_trades),
            'sell_trades': len(sell_trades),
            'total_bought': total_bought,
            'total_sold': total_sold,
            'realized_pnl': total_sold - total_bought if buy_trades else 0,
            'trades': symbol_trades
        }
    
    def update_memory_with_new_trade(self, trade_data: Dict[str, Any]):
        """Update memory file with new trade"""
        try:
            with open(self.memory_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    trade_data.get('date', datetime.now().strftime('%Y-%m-%d')),
                    trade_data['symbol'],
                    trade_data['action'],
                    trade_data['quantity'],
                    f"${trade_data['price']:.2f}",
                    f"${trade_data['total_value']:.2f}",
                    trade_data.get('trade_id', ''),
                    trade_data.get('running_pnl', '$0.00'),
                    trade_data.get('notes', '')
                ])
            
            logger.info(f"Updated memory with new trade: {trade_data['symbol']}")
            
        except Exception as e:
            logger.error(f"Error updating memory: {e}")