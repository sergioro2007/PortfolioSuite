"""
📈 Trade Analysis CLI Module
===========================

Command-line interface for trade analysis and strategy generation.
Provides command-line tools for analyzing trading opportunities.
"""

import argparse
import sys
from typing import List, Optional

from .core import TradeAnalyzer, run_trade_analysis


def main():
    """Main CLI entry point for trade analysis"""
    parser = argparse.ArgumentParser(
        description="Portfolio Suite - Trade Analysis Tools",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  portfolio-analysis analyze AAPL
  portfolio-analysis suggest SPY QQQ AAPL
  portfolio-analysis summary
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze a single symbol')
    analyze_parser.add_argument('symbol', help='Stock ticker symbol to analyze')
    
    # Suggest command
    suggest_parser = subparsers.add_parser('suggest', help='Generate trade suggestions')
    suggest_parser.add_argument('symbols', nargs='+', help='Stock ticker symbols to analyze')
    suggest_parser.add_argument('--min-confidence', type=float, default=0.5,
                               help='Minimum confidence score (0.0-1.0)')
    
    # Summary command
    subparsers.add_parser('summary', help='Show portfolio performance summary')
    
    # Default command (quick analysis)
    subparsers.add_parser('quick', help='Quick analysis of default symbols')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'analyze':
            analyze_symbol_cli(args.symbol)
        elif args.command == 'suggest':
            generate_suggestions_cli(args.symbols, args.min_confidence)
        elif args.command == 'summary':
            show_summary_cli()
        elif args.command == 'quick':
            quick_analysis_cli()
    except KeyboardInterrupt:
        print("\n⏹️  Analysis interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def analyze_symbol_cli(symbol: str):
    """Analyze a single symbol via CLI"""
    print(f"🔍 Analyzing {symbol.upper()}...")
    print("=" * 50)
    
    analyzer = TradeAnalyzer()
    analysis = analyzer.analyze_symbol(symbol.upper())
    
    if "error" in analysis:
        print(f"❌ {analysis['error']}")
        return
    
    # Display results
    print(f"📊 Analysis Results for {analysis['symbol']}")
    print(f"Current Price: ${analysis['current_price']:.2f}")
    print(f"20-Day SMA:    ${analysis['sma_20']:.2f}")
    print(f"50-Day SMA:    ${analysis['sma_50']:.2f}")
    print(f"Volatility:    {analysis['volatility']*100:.1f}%")
    print(f"52W High:      ${analysis['high_52w']:.2f}")
    print(f"52W Low:       ${analysis['low_52w']:.2f}")
    print(f"Trend:         {analysis['trend']}")
    print(f"Signal:        {analysis['signal']}")
    
    # Price position
    position = (analysis['current_price'] - analysis['low_52w']) / (analysis['high_52w'] - analysis['low_52w'])
    print(f"Position:      {position:.1%} of 52-week range")
    
    print(f"\nAnalysis Date: {analysis['analysis_date'][:10]}")


def generate_suggestions_cli(symbols: List[str], min_confidence: float):
    """Generate trade suggestions via CLI"""
    print(f"💡 Generating trade suggestions for {len(symbols)} symbols...")
    print("=" * 60)
    
    analyzer = TradeAnalyzer()
    suggestions = analyzer.generate_trade_suggestions(symbols)
    
    # Filter by confidence
    filtered_suggestions = [s for s in suggestions if s['confidence'] >= min_confidence]
    
    if not filtered_suggestions:
        print(f"❌ No suggestions found with confidence >= {min_confidence}")
        print(f"📊 Total analyzed: {len(symbols)} symbols")
        print(f"📈 Raw suggestions: {len(suggestions)}")
        return
    
    print(f"✅ Found {len(filtered_suggestions)} trade suggestions:")
    print()
    
    for i, suggestion in enumerate(filtered_suggestions, 1):
        potential_return = ((suggestion['target_price'] - suggestion['current_price']) / suggestion['current_price'] * 100)
        
        print(f"{i}. {suggestion['symbol']} - {suggestion['action']}")
        print(f"   Current:    ${suggestion['current_price']:.2f}")
        print(f"   Target:     ${suggestion['target_price']:.2f}")
        print(f"   Stop Loss:  ${suggestion['stop_loss']:.2f}")
        print(f"   Confidence: {suggestion['confidence']:.2f}")
        print(f"   Return:     {potential_return:.1f}%")
        print()


def show_summary_cli():
    """Show portfolio summary via CLI"""
    print("📈 Portfolio Performance Summary")
    print("=" * 40)
    
    analyzer = TradeAnalyzer()
    summary = analyzer.get_portfolio_summary()
    
    if "message" in summary:
        print(summary["message"])
        print("\n🚀 Quick Start Guide:")
        print("1. Use 'portfolio-analysis analyze SYMBOL' to analyze stocks")
        print("2. Use 'portfolio-analysis suggest SYMBOL1 SYMBOL2' for trade ideas")
        print("3. Record trades manually to track performance")
        return
    
    print(f"Total Trades:   {summary['total_trades']}")
    print(f"Total P&L:      ${summary['total_profit']:.2f}")
    print(f"Win Rate:       {summary['win_rate']:.1f}%")
    print(f"Average Return: ${summary['average_return']:.2f}")
    
    if analyzer.trade_history:
        print("\n📊 Recent Trades:")
        for trade in analyzer.trade_history[-5:]:  # Show last 5 trades
            print(f"  {trade['trade_id']}: ${trade['profit_loss']:.2f} ({trade['return_percentage']:.1f}%)")


def quick_analysis_cli():
    """Perform quick analysis of default symbols"""
    print("⚡ Quick Analysis - Default Watchlist")
    print("=" * 45)
    
    # Use the existing function from core
    suggestions = run_trade_analysis()
    
    if suggestions:
        print("✅ Analysis complete. Use 'portfolio-analysis suggest' for detailed suggestions.")
    else:
        print("❌ No trade suggestions found in quick analysis.")


if __name__ == '__main__':
    main()
