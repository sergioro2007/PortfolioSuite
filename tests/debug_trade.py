#!/usr/bin/env python3

from src.options_tracker import OptionsTracker

tracker = OptionsTracker()
suggestions = tracker.generate_trade_suggestions(1)

if suggestions:
    suggestion = suggestions[0]
    print('Suggested Trade:')
    for leg in suggestion['legs']:
        print(f'{leg["action"]} {leg["type"]} ${leg["strike"]:.2f} @ ${leg["price"]:.2f}')
    
    print(f'\nStrategy: {suggestion["strategy"]}')
    print(f'Ticker: {suggestion["ticker"]}')
    
    if suggestion['strategy'] == 'Iron Condor':
        print(f'Put Long: {suggestion["put_long_strike"]}')
        print(f'Put Short: {suggestion["put_short_strike"]}')
        print(f'Call Short: {suggestion["call_short_strike"]}')
        print(f'Call Long: {suggestion["call_long_strike"]}')
