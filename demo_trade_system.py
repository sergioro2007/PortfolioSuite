#!/usr/bin/env python3
"""
📊 Trade System Demo
===================

Comprehensive demonstration of the new trade repository functionality.
This script showcases all the features implemented in the trade module.
"""

import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from portfolio_suite.trade import TradeRepository, TradeManager, TradeMemory, TradeReporter


def demo_trade_system():
    """Demonstrate the complete trade system"""
    
    print("🎯 TRADE REPOSITORY SYSTEM DEMONSTRATION")
    print("=" * 60)
    print("This demo showcases the comprehensive trade management system")
    print("implemented for the PortfolioSuite repository.\n")
    
    # Initialize all components
    trade_manager = TradeManager()
    trade_memory = TradeMemory()
    trade_reporter = TradeReporter()
    
    print("📋 STEP 1: Historical Memory Analysis")
    print("-" * 40)
    
    # Analyze the historical CSV data
    memory_data = trade_memory.analyze_memory_performance()
    print(f"✅ Loaded historical trading memory:")
    print(f"   📊 Total trades in memory: {memory_data['total_trades']}")
    print(f"   🏷️  Unique symbols: {memory_data['unique_symbols']}")
    print(f"   💰 Total invested: ${memory_data['total_buy_value']:,.2f}")
    print(f"   💸 Total realized: ${memory_data['total_sell_value']:,.2f}")
    print(f"   📈 Net P&L: ${memory_data['realized_pnl']:,.2f}")
    print(f"   📅 Period: {memory_data['date_range']['start']} to {memory_data['date_range']['end']}")
    
    print(f"\n   🎯 Symbols traded: {', '.join(memory_data['symbols_traded'])}")
    
    print(f"\n📋 STEP 2: Current Portfolio Status")
    print("-" * 40)
    
    # Show current live portfolio
    current_positions = trade_manager.repository.get_positions()
    current_summary = trade_manager.get_trade_summary()
    
    print(f"✅ Live portfolio status:")
    print(f"   📊 Total active trades: {current_summary['total_trades']}")
    print(f"   💼 Active positions: {current_summary['active_positions']}")
    print(f"   🏷️  Symbols in portfolio: {current_summary['symbols_traded']}")
    
    if current_positions:
        print(f"\n   Current holdings:")
        for symbol, position in current_positions.items():
            print(f"     • {symbol}: {position['quantity']} shares @ ${position['avg_price']:.2f}")
    
    print(f"\n📋 STEP 3: Sample Trade Execution")
    print("-" * 40)
    
    # Execute some sample trades
    sample_trades = [
        ('NFLX', 'BUY', 15, 485.25),
        ('DIS', 'BUY', 40, 112.75),
    ]
    
    print("✅ Executing sample trades:")
    for symbol, action, quantity, price in sample_trades:
        success = trade_manager.execute_trade(symbol, action, quantity, price)
        if success:
            print(f"   ✓ {action} {quantity} {symbol} @ ${price}")
        else:
            print(f"   ✗ Failed: {action} {quantity} {symbol} @ ${price}")
    
    print(f"\n📋 STEP 4: Symbol-Specific Analysis")
    print("-" * 40)
    
    # Analyze specific symbols from memory
    symbols_to_analyze = ['AAPL', 'MSFT', 'GOOGL']
    
    print("✅ Analyzing individual symbols:")
    for symbol in symbols_to_analyze:
        analysis = trade_memory.get_symbol_performance(symbol)
        if 'error' not in analysis:
            print(f"   📈 {symbol}:")
            print(f"      Trades: {analysis['total_trades']} ({analysis['buy_trades']} buy, {analysis['sell_trades']} sell)")
            print(f"      P&L: ${analysis['realized_pnl']:.2f}")
        else:
            print(f"   ❌ {symbol}: No data available")
    
    print(f"\n📋 STEP 5: Report Generation")
    print("-" * 40)
    
    # Generate comprehensive report
    report_file = trade_reporter.generate_analysis_report(
        memory_data, 
        "comprehensive_demo_report.md"
    )
    
    if report_file:
        print(f"✅ Generated comprehensive report: {report_file}")
        
        # Show performance summary
        perf_summary = trade_reporter.generate_performance_summary(memory_data)
        print(f"   📊 Performance Summary:")
        print(f"      ROI: {perf_summary['roi_percentage']}%")
        print(f"      Avg Trade Size: ${perf_summary['average_trade_size']:,.2f}")
        print(f"      Performance Grade: {perf_summary['performance_grade']}")
    
    print(f"\n📋 STEP 6: Template and Documentation")
    print("-" * 40)
    
    # Create analysis template
    template_file = trade_reporter.create_analysis_template()
    if template_file:
        print(f"✅ Analysis template available at: {template_file}")
    
    # Show file structure
    print(f"\n✅ Generated file structure:")
    print(f"   📁 data/trades/")
    print(f"      📄 Trading_Memory_Summary_2025-06-26.csv  (Historical data)")
    print(f"      📄 trades.json                           (Live trade storage)")
    print(f"      📁 reports/")
    print(f"         📄 trade_analysis_report_2025-06-27.md   (Sample report)")
    print(f"         📄 trade_analysis_template.md            (Report template)")
    print(f"         📄 comprehensive_demo_report.md          (Demo report)")
    
    print(f"\n🎉 DEMONSTRATION COMPLETE!")
    print("=" * 60)
    
    print("\n📚 AVAILABLE CLI COMMANDS:")
    print("  python src/portfolio_suite/trade/cli.py memory      # Analyze memory data")
    print("  python src/portfolio_suite/trade/cli.py portfolio   # View current positions")
    print("  python src/portfolio_suite/trade/cli.py add SYMBOL BUY QTY PRICE")
    print("  python src/portfolio_suite/trade/cli.py report      # Generate analysis report")
    print("  python src/portfolio_suite/trade/cli.py template    # Create report template")
    
    print("\n✨ The trade repository system is fully operational and ready for use!")
    
    return True


if __name__ == "__main__":
    try:
        demo_trade_system()
    except Exception as e:
        print(f"💥 Demo failed: {e}")
        sys.exit(1)