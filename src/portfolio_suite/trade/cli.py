#!/usr/bin/env python3
"""
📊 Trade Analysis CLI
====================

Command line interface for the trade analysis system.
"""

import sys
import argparse
from pathlib import Path
import json

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from portfolio_suite.trade import TradeRepository, TradeManager, TradeMemory, TradeReporter
from portfolio_suite.trade.core import Trade


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(description="Trade Analysis CLI")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add trade command
    add_parser = subparsers.add_parser('add', help='Add a new trade')
    add_parser.add_argument('symbol', help='Stock symbol')
    add_parser.add_argument('action', choices=['BUY', 'SELL'], help='Trade action')
    add_parser.add_argument('quantity', type=int, help='Number of shares')
    add_parser.add_argument('price', type=float, help='Price per share')
    
    # List trades command
    list_parser = subparsers.add_parser('list', help='List trades')
    list_parser.add_argument('--symbol', help='Filter by symbol')
    
    # Portfolio command
    subparsers.add_parser('portfolio', help='Show portfolio positions')
    
    # Memory analysis command
    subparsers.add_parser('memory', help='Analyze memory data')
    
    # Generate report command
    report_parser = subparsers.add_parser('report', help='Generate analysis report')
    report_parser.add_argument('--output', help='Output file name')
    
    # Create template command
    subparsers.add_parser('template', help='Create analysis template')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize components
    trade_manager = TradeManager()
    trade_memory = TradeMemory()
    trade_reporter = TradeReporter()
    
    try:
        if args.command == 'add':
            success = trade_manager.execute_trade(
                args.symbol, args.action, args.quantity, args.price
            )
            if success:
                print(f"✅ Trade added: {args.action} {args.quantity} {args.symbol} @ ${args.price}")
            else:
                print("❌ Failed to add trade")
        
        elif args.command == 'list':
            trades = trade_manager.repository.get_trades(symbol=args.symbol)
            if trades:
                print(f"\n📊 Found {len(trades)} trades:")
                print("-" * 80)
                for trade in trades:
                    print(f"{trade.trade_date.split('T')[0]} | {trade.symbol} | {trade.action} | "
                          f"{trade.quantity} @ ${trade.price:.2f} | ${trade.total_value:.2f}")
            else:
                print("No trades found")
        
        elif args.command == 'portfolio':
            positions = trade_manager.repository.get_positions()
            if positions:
                print(f"\n💼 Portfolio Positions:")
                print("-" * 60)
                for symbol, position in positions.items():
                    print(f"{symbol}: {position['quantity']} shares @ ${position['avg_price']:.2f}")
            else:
                print("No active positions")
        
        elif args.command == 'memory':
            performance = trade_memory.analyze_memory_performance()
            if 'error' not in performance:
                print(f"\n📈 Memory Analysis:")
                print("-" * 40)
                print(f"Total Trades: {performance['total_trades']}")
                print(f"Unique Symbols: {performance['unique_symbols']}")
                print(f"Total Buy Value: ${performance['total_buy_value']:,.2f}")
                print(f"Total Sell Value: ${performance['total_sell_value']:,.2f}")
                print(f"Realized P&L: ${performance['realized_pnl']:,.2f}")
                print(f"Final Running P&L: ${performance['final_running_pnl']:,.2f}")
                print(f"Period: {performance['date_range']['start']} to {performance['date_range']['end']}")
            else:
                print(f"Error: {performance['error']}")
        
        elif args.command == 'report':
            memory_data = trade_memory.analyze_memory_performance()
            if 'error' not in memory_data:
                report_file = trade_reporter.generate_analysis_report(memory_data, args.output)
                if report_file:
                    print(f"✅ Report generated: {report_file}")
                else:
                    print("❌ Failed to generate report")
            else:
                print(f"Error: {memory_data['error']}")
        
        elif args.command == 'template':
            template_file = trade_reporter.create_analysis_template()
            if template_file:
                print(f"✅ Template created: {template_file}")
            else:
                print("❌ Failed to create template")
    
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()