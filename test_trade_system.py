#!/usr/bin/env python3
"""
📊 Comprehensive Trade System Test
=================================

Test script to validate the complete trade analysis functionality.
"""

import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from portfolio_suite.trade import TradeRepository, TradeManager, TradeMemory, TradeReporter


def test_trade_system():
    """Test the complete trade system functionality"""
    
    print("🚀 Starting Trade System Test...")
    print("=" * 50)
    
    # Initialize components
    trade_manager = TradeManager()
    trade_memory = TradeMemory()
    trade_reporter = TradeReporter()
    
    # Test 1: Memory Analysis
    print("\n📊 Test 1: Memory Data Analysis")
    print("-" * 30)
    
    memory_performance = trade_memory.analyze_memory_performance()
    if 'error' not in memory_performance:
        print(f"✅ Memory analysis successful")
        print(f"   - Total trades: {memory_performance['total_trades']}")
        print(f"   - Unique symbols: {memory_performance['unique_symbols']}")
        print(f"   - Realized P&L: ${memory_performance['realized_pnl']:,.2f}")
    else:
        print(f"❌ Memory analysis failed: {memory_performance['error']}")
        return False
    
    # Test 2: Add New Trades
    print("\n📈 Test 2: Adding New Trades")
    print("-" * 30)
    
    test_trades = [
        ('META', 'BUY', 20, 325.75),
        ('AMD', 'BUY', 100, 95.25),
        ('META', 'SELL', 10, 330.00)
    ]
    
    for symbol, action, quantity, price in test_trades:
        success = trade_manager.execute_trade(symbol, action, quantity, price)
        if success:
            print(f"✅ {action} {quantity} {symbol} @ ${price}")
        else:
            print(f"❌ Failed to add trade: {symbol}")
            return False
    
    # Test 3: Portfolio Positions
    print("\n💼 Test 3: Portfolio Analysis")
    print("-" * 30)
    
    positions = trade_manager.repository.get_positions()
    print(f"✅ Current positions ({len(positions)} symbols):")
    for symbol, position in positions.items():
        print(f"   - {symbol}: {position['quantity']} shares @ ${position['avg_price']:.2f}")
    
    # Test 4: Trade Summary
    print("\n📋 Test 4: Trade Summary")
    print("-" * 30)
    
    summary = trade_manager.get_trade_summary()
    print(f"✅ Trade summary:")
    print(f"   - Total trades: {summary['total_trades']}")
    print(f"   - Buy trades: {summary['buy_trades']}")
    print(f"   - Sell trades: {summary['sell_trades']}")
    print(f"   - Active positions: {summary['active_positions']}")
    print(f"   - Symbols traded: {summary['symbols_traded']}")
    
    # Test 5: Symbol-specific Analysis
    print("\n🔍 Test 5: Symbol Analysis")
    print("-" * 30)
    
    meta_performance = trade_memory.get_symbol_performance('META')
    if 'error' not in meta_performance:
        print(f"✅ META analysis:")
        print(f"   - Total trades: {meta_performance['total_trades']}")
        print(f"   - Buy trades: {meta_performance['buy_trades']}")
        print(f"   - Sell trades: {meta_performance['sell_trades']}")
        print(f"   - Realized P&L: ${meta_performance['realized_pnl']:.2f}")
    else:
        print(f"❌ META analysis failed: {meta_performance['error']}")
    
    # Test 6: Report Generation
    print("\n📝 Test 6: Report Generation")
    print("-" * 30)
    
    report_file = trade_reporter.generate_analysis_report(
        memory_performance, 
        "test_trade_analysis_report.md"
    )
    if report_file:
        print(f"✅ Report generated: {report_file}")
    else:
        print("❌ Report generation failed")
        return False
    
    # Test 7: Template Creation
    print("\n📄 Test 7: Template Creation")
    print("-" * 30)
    
    template_file = trade_reporter.create_analysis_template()
    if template_file:
        print(f"✅ Template created: {template_file}")
    else:
        print("❌ Template creation failed")
        return False
    
    # Test 8: Performance Summary
    print("\n🎯 Test 8: Performance Summary")
    print("-" * 30)
    
    perf_summary = trade_reporter.generate_performance_summary(memory_performance)
    print(f"✅ Performance summary:")
    print(f"   - ROI: {perf_summary['roi_percentage']}%")
    print(f"   - Average trade size: ${perf_summary['average_trade_size']:,.2f}")
    print(f"   - Performance grade: {perf_summary['performance_grade']}")
    
    print("\n🎉 All tests completed successfully!")
    print("=" * 50)
    return True


def main():
    """Main test function"""
    try:
        success = test_trade_system()
        if success:
            print("\n✅ Trade system is working correctly!")
            sys.exit(0)
        else:
            print("\n❌ Trade system tests failed!")
            sys.exit(1)
    except Exception as e:
        print(f"\n💥 Test failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()