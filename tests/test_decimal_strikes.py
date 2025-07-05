"""
Test script to verify OptionStrat URL generation for decimal strikes
"""

from src.options_tracker_ui import generate_optionstrat_url

def test_iron_condor_decimal_strikes():
    """Test Iron Condor URL generation with half-dollar strikes"""
    
    suggestion = {
        'ticker': 'SPY',
        'strategy': 'Iron Condor',
        'put_long_strike': 570.0,
        'put_short_strike': 572.5,  # Half-dollar strike
        'call_short_strike': 580.0,
        'call_long_strike': 582.5,  # Half-dollar strike
        'expiration': '2025-08-01'
    }
    
    url = generate_optionstrat_url(suggestion)
    print(f"Generated URL: {url}")
    
    # Check if the URL contains the decimal strikes
    assert "572.5" in url, f"URL should contain 572.5 but got: {url}"
    assert "582.5" in url, f"URL should contain 582.5 but got: {url}"
    
    print("✅ Decimal strikes preserved in URL!")

def test_bull_put_spread_decimal_strikes():
    """Test Bull Put Spread URL generation with half-dollar strikes"""
    
    suggestion = {
        'ticker': 'SPY',
        'strategy': 'Bull Put Spread',
        'short_strike': 572.5,  # Half-dollar strike
        'long_strike': 570.0,
        'expiration': '2025-08-01'
    }
    
    url = generate_optionstrat_url(suggestion)
    print(f"Generated URL: {url}")
    
    # Check if the URL contains the decimal strike
    assert "572.5" in url, f"URL should contain 572.5 but got: {url}"
    
    print("✅ Decimal strikes preserved in Bull Put Spread URL!")

if __name__ == "__main__":
    print("Testing OptionStrat URL generation with decimal strikes...")
    test_iron_condor_decimal_strikes()
    test_bull_put_spread_decimal_strikes()
    print("All tests passed!")
