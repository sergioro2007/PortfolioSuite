import sys
sys.path.append('.')
from src.options_tracker import OptionsTracker

def test_dynamic_watchlist_generation():
    """Test the dynamic watchlist generation functionality"""
    print('=== TESTING DYNAMIC WATCHLIST GENERATION ===')
    tracker = OptionsTracker()

    # Check if watchlist was generated
    print(f'Watchlist has {len(tracker.watchlist)} tickers')

    # Print first 5 tickers and their parameters
    print('\nSample of watchlist tickers:')
    for i, (ticker, data) in enumerate(list(tracker.watchlist.items())[:5]):
        print(f'{ticker}: Price=${data["current_price"]:.2f}, ' +
            f'Range=(${data["range_68"][0]:.2f}, ${data["range_68"][1]:.2f}), ' +
            f'Target=${data["target_zone"]:.2f}, ' +
            f'Bias={data["bias_prob"]:.2f}'
            )

    # Verify all expected parameters exist
    print('\nVerifying parameter structure:')
    missing_params = []
    for ticker, data in tracker.watchlist.items():
        for param in ['current_price', 'range_68', 'target_zone', 'bias_prob']:
            if param not in data:
                missing_params.append((ticker, param))

    if missing_params:
        print('Missing parameters:')
        for ticker, param in missing_params:
            print(f'- {ticker}: missing {param}')
    else:
        print('✅ All tickers have the expected parameters')

    # Verify parameter value ranges
    print('\nVerifying parameter values:')
    invalid_values = []
    for ticker, data in tracker.watchlist.items():
        # Check price is positive
        if data['current_price'] <= 0:
            invalid_values.append((ticker, 'current_price', data['current_price']))
        
        # Check range makes sense (low < high)
        if data['range_68'][0] >= data['range_68'][1]:
            invalid_values.append((ticker, 'range_68', data['range_68']))
        
        # Check bias probability is between 0 and 1
        if not 0 <= data['bias_prob'] <= 1:
            invalid_values.append((ticker, 'bias_prob', data['bias_prob']))

    if invalid_values:
        print('Invalid parameter values:')
        for ticker, param, value in invalid_values:
            print(f'- {ticker}: {param} = {value}')
    else:
        print('✅ All parameter values are within expected ranges')

if __name__ == "__main__":
    test_dynamic_watchlist_generation()
