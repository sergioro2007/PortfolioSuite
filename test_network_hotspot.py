#!/usr/bin/env python3
"""
Test network connectivity with mobile hotspot
"""

import socket
import requests
import yfinance as yf
from datetime import datetime
import sys
import os

# Add path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_network_connectivity():
    """Test various levels of network connectivity"""
    
    print('=== Mobile Hotspot Network Tests ===')
    print(f'Timestamp: {datetime.now().strftime("%H:%M:%S")}')
    print()

    tests_passed = 0
    total_tests = 5

    # Test 1: Basic internet connectivity
    print('1. Testing basic internet connectivity...')
    try:
        socket.create_connection(('8.8.8.8', 53), timeout=3)
        print('✅ SUCCESS: Basic internet CONNECTED')
        tests_passed += 1
    except Exception as e:
        print(f'❌ FAILED: Basic internet - {str(e)}')

    # Test 2: DNS resolution
    print('2. Testing DNS resolution...')
    try:
        socket.gethostbyname('google.com')
        print('✅ SUCCESS: DNS resolution WORKING')
        tests_passed += 1
    except Exception as e:
        print(f'❌ FAILED: DNS resolution - {str(e)}')

    # Test 3: HTTPS requests
    print('3. Testing HTTPS requests...')
    try:
        response = requests.get('https://httpbin.org/get', timeout=5)
        print(f'✅ SUCCESS: HTTPS requests WORKING (status: {response.status_code})')
        tests_passed += 1
    except Exception as e:
        print(f'❌ FAILED: HTTPS requests - {str(e)}')

    # Test 4: Yahoo Finance API specifically
    print('4. Testing Yahoo Finance API...')
    try:
        response = requests.get('https://query1.finance.yahoo.com/v8/finance/chart/AAPL', timeout=10)
        print(f'✅ SUCCESS: Yahoo Finance API ACCESSIBLE (status: {response.status_code})')
        tests_passed += 1
    except Exception as e:
        print(f'❌ FAILED: Yahoo Finance API - {str(e)}')

    # Test 5: yfinance library
    print('5. Testing yfinance library...')
    try:
        ticker = yf.Ticker('AAPL')
        hist = ticker.history(period='1d')
        if not hist.empty:
            price = hist['Close'].iloc[-1]
            print(f'✅ SUCCESS: yfinance WORKING (AAPL: ${price:.2f})')
            tests_passed += 1
        else:
            print('⚠️  WARNING: yfinance NO DATA returned')
    except Exception as e:
        print(f'❌ FAILED: yfinance - {str(e)}')

    print()
    print(f'=== Network Test Summary ===')
    print(f'Tests Passed: {tests_passed}/{total_tests}')
    
    if tests_passed >= 4:
        print('🎉 NETWORK STATUS: EXCELLENT - Full functionality available')
        return True
    elif tests_passed >= 2:
        print('⚠️  NETWORK STATUS: LIMITED - Some features may not work')
        return False
    else:
        print('❌ NETWORK STATUS: POOR - Most features will be unavailable')
        return False

def test_options_tracker():
    """Test the Options Tracker with current network"""
    print()
    print('=== Options Tracker Network Test ===')
    
    try:
        from portfolio_suite.options_trading.core import OptionsTracker
        
        tracker = OptionsTracker()
        tracker.force_network_recheck()
        status = tracker.check_network_status()
        
        print(f'Options Tracker Detection:')
        print(f'  - Online: {status["is_online"]}')
        print(f'  - Network Type: {status["network_type"]}')
        print(f'  - Message: {status["status_message"]}')
        print(f'  - Last Check: {status.get("last_check", "Unknown")}')
        
        return status["is_online"]
        
    except Exception as e:
        print(f'❌ FAILED: Could not test Options Tracker - {str(e)}')
        return False

if __name__ == "__main__":
    network_ok = test_network_connectivity()
    tracker_ok = test_options_tracker()
    
    print()
    print('=== Final Assessment ===')
    if network_ok and tracker_ok:
        print('🎉 SUCCESS: Network is working and Options Tracker should function normally!')
    elif network_ok and not tracker_ok:
        print('⚠️  MIXED: Network works but Options Tracker still detects issues')
    else:
        print('❌ ISSUES: Network connectivity problems detected')
