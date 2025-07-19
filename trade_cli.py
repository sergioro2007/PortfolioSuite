#!/usr/bin/env python3
"""
📊 Unified Trade CLI
===================

Combined command line interface for both legacy trade analysis 
and new enhanced trade management functionality.
"""

import sys
import argparse
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from portfolio_suite.trade_analysis import TradeAnalyzer, ENHANCED_FEATURES_AVAILABLE

if ENHANCED_FEATURES_AVAILABLE:
    from portfolio_suite.trade_analysis import TradeRepository, TradeManager, TradeMemory, TradeReporter


def run_legacy_analysis(symbols):
    """Run legacy trade analysis"""
    print("🔍 Running Legacy Trade Analysis...")
    analyzer = TradeAnalyzer()
    
    for symbol in symbols:
        analysis = analyzer.analyze_symbol(symbol)
        if 'error' not in analysis:
            print(f"\n📈 {symbol} Analysis:")
            print(f"  Current Price: ${analysis['current_price']}")
            print(f"  Trend: {analysis['trend']}")
            print(f"  Signal: {analysis['signal']}")
            print(f"  SMA 20: ${analysis['sma_20']}")
            print(f"  SMA 50: ${analysis['sma_50']}")
            print(f"  Volatility: {analysis['volatility']:.2%}")
        else:
            print(f"❌ {symbol}: {analysis['error']}")


def run_enhanced_analysis():
    """Run enhanced trade analysis with new functionality"""
    if not ENHANCED_FEATURES_AVAILABLE:
        print("❌ Enhanced features not available. Trade module not found.")
        return
    
    print("🚀 Running Enhanced Trade Analysis...")
    
    trade_memory = TradeMemory()
    trade_reporter = TradeReporter()
    
    # Analyze memory data
    memory_data = trade_memory.analyze_memory_performance()
    if 'error' not in memory_data:
        print(f"\n📊 Trading Memory Analysis:")
        print(f"  Total Trades: {memory_data['total_trades']}")
        print(f"  Symbols Traded: {memory_data['unique_symbols']}")
        print(f"  Realized P&L: ${memory_data['realized_pnl']:,.2f}")
        print(f"  Period: {memory_data['date_range']['start']} to {memory_data['date_range']['end']}")
        
        # Generate performance summary
        perf_summary = trade_reporter.generate_performance_summary(memory_data)
        print(f"  ROI: {perf_summary['roi_percentage']}%")
        print(f"  Performance Grade: {perf_summary['performance_grade']}")
    else:
        print(f"❌ Memory analysis failed: {memory_data['error']}")


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(description="Unified Trade Analysis CLI")
    subparsers = parser.add_subparsers(dest='mode', help='Analysis mode')
    
    # Legacy analysis mode
    legacy_parser = subparsers.add_parser('legacy', help='Run legacy trade analysis')
    legacy_parser.add_argument('symbols', nargs='+', help='Stock symbols to analyze')
    
    # Enhanced analysis mode
    enhanced_parser = subparsers.add_parser('enhanced', help='Run enhanced trade analysis')
    
    # Combined mode
    combined_parser = subparsers.add_parser('combined', help='Run both analyses')
    combined_parser.add_argument('symbols', nargs='+', help='Stock symbols to analyze')
    
    # Status check
    subparsers.add_parser('status', help='Check system status')
    
    args = parser.parse_args()
    
    if not args.mode:
        parser.print_help()
        return
    
    try:
        if args.mode == 'legacy':
            run_legacy_analysis(args.symbols)
        
        elif args.mode == 'enhanced':
            run_enhanced_analysis()
        
        elif args.mode == 'combined':
            print("🔄 Running Combined Analysis...")
            print("=" * 50)
            run_legacy_analysis(args.symbols)
            print("\n" + "=" * 50)
            run_enhanced_analysis()
        
        elif args.mode == 'status':
            print("📋 Trade Analysis System Status")
            print("-" * 30)
            print(f"Legacy Analysis: ✅ Available")
            print(f"Enhanced Features: {'✅ Available' if ENHANCED_FEATURES_AVAILABLE else '❌ Not Available'}")
            
            if ENHANCED_FEATURES_AVAILABLE:
                trade_manager = TradeManager()
                summary = trade_manager.get_trade_summary()
                positions = trade_manager.repository.get_positions()
                
                print(f"\nTrade System Status:")
                print(f"  Total Trades: {summary['total_trades']}")
                print(f"  Active Positions: {len(positions)}")
                print(f"  Symbols in Portfolio: {summary['symbols_traded']}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()