import sys
sys.path.append('.')
from src.options_tracker import OptionsTracker

def test_profit_target_filter():
    """Test the profit target filter with different thresholds"""
    print('=== TESTING PROFIT TARGET FILTER ===')
    
    # Create tracker and expand watchlist for more opportunities
    tracker = OptionsTracker()
    tracker.expand_watchlist_with_high_options_volume(min_additional_tickers=10)
    print(f"Expanded watchlist to {len(tracker.watchlist)} tickers")
    
    # Test with different profit targets
    profit_targets = [0.5, 1.0, 2.0, 5.0]
    
    for target in profit_targets:
        print(f"\n=== Testing with ${target:.2f}/share profit target (${target*100:.0f}/contract) ===")
        suggestions = tracker.generate_trade_suggestions(num_suggestions=5, min_profit_target=target)
        
        # Analyze suggestions
        print(f"Generated {len(suggestions)} suggestions")
        
        if not suggestions:
            print("No suggestions generated, unable to verify profit target filter")
            continue
        
        # Check profit targets
        min_profit = min(s['profit_target'] for s in suggestions)
        max_profit = max(s['profit_target'] for s in suggestions)
        avg_profit = sum(s['profit_target'] for s in suggestions) / len(suggestions)
        
        print(f"Profit range: ${min_profit:.2f}/share to ${max_profit:.2f}/share")
        print(f"Average profit: ${avg_profit:.2f}/share (${avg_profit*100:.0f}/contract)")
        
        # Verify profit target enforcement
        if min_profit < target:
            print(f"❌ Found suggestion with profit below target: ${min_profit:.2f} < ${target:.2f}")
            # Show the offending suggestion
            for s in suggestions:
                if s['profit_target'] < target:
                    print(f"  - {s['ticker']} {s['strategy']}: ${s['profit_target']:.2f}/share")
        else:
            print(f"✅ All suggestions meet or exceed profit target of ${target:.2f}/share")
        
        # Show strategies selected
        strategies = {}
        for s in suggestions:
            strategy = s['strategy']
            if strategy in strategies:
                strategies[strategy] += 1
            else:
                strategies[strategy] = 1
        
        print("Strategy distribution:")
        for strategy, count in strategies.items():
            print(f"  - {strategy}: {count} suggestions")

if __name__ == "__main__":
    test_profit_target_filter()
