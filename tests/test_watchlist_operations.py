import sys
sys.path.append('.')
from src.options_tracker import OptionsTracker

def test_watchlist_refresh_and_expansion():
    """Test the watchlist refresh and expansion functionality"""
    print('=== TESTING WATCHLIST REFRESH AND EXPANSION ===')
    tracker = OptionsTracker()
    
    # Get initial watchlist size
    initial_size = len(tracker.watchlist)
    print(f"Initial watchlist size: {initial_size} tickers")
    
    # Print the initial tickers
    print("\nInitial watchlist tickers:")
    for ticker in list(tracker.watchlist.keys())[:10]:  # Show first 10
        print(f"- {ticker}")
    
    # Test watchlist refresh
    print("\nTesting watchlist refresh...")
    tracker.refresh_watchlist()
    
    # Verify refresh maintained similar size
    refresh_size = len(tracker.watchlist)
    print(f"Refreshed watchlist size: {refresh_size} tickers")
    if abs(refresh_size - initial_size) > 2:
        print(f"⚠️ Significant size change after refresh: {initial_size} -> {refresh_size}")
    else:
        print("✅ Watchlist size maintained after refresh")
    
    # Test watchlist expansion
    print("\nTesting watchlist expansion...")
    additional_tickers = 5
    tracker.expand_watchlist_with_high_options_volume(min_additional_tickers=additional_tickers)
    
    # Verify expansion increased size
    expanded_size = len(tracker.watchlist)
    print(f"Expanded watchlist size: {expanded_size} tickers")
    if expanded_size > refresh_size:
        print(f"✅ Watchlist successfully expanded: +{expanded_size - refresh_size} tickers")
    else:
        print(f"❌ Watchlist failed to expand: {refresh_size} -> {expanded_size}")
    
    # Print the new tickers added
    print("\nFull expanded watchlist tickers:")
    for ticker in tracker.watchlist.keys():
        print(f"- {ticker}")
    
    # Test integration with trade suggestion generation
    print("\nTesting integration with trade suggestion generation...")
    suggestions = tracker.generate_trade_suggestions(num_suggestions=3, min_profit_target=1.0)
    
    print(f"\nGenerated {len(suggestions)} trade suggestions")
    for i, suggestion in enumerate(suggestions):
        ticker = suggestion['ticker']
        strategy = suggestion['strategy']
        profit = suggestion.get('profit_target', 0) * 100  # Per contract
        confidence = suggestion.get('confidence', 0)
        print(f"{i+1}. {ticker} {strategy}: ${profit:.2f}/contract profit target, {confidence:.0f}% confidence")
        
        # Verify profit target enforcement
        if profit < 100:
            print(f"❌ Trade suggestion has profit target below $100/contract: ${profit:.2f}")
        
    if len(suggestions) > 0:
        print("✅ Successfully generated trade suggestions using dynamic watchlist")
    else:
        print("❌ Failed to generate any trade suggestions")

if __name__ == "__main__":
    test_watchlist_refresh_and_expansion()
