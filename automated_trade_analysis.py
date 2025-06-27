import datetime

def suggest_strategy(market_sentiment, stock_range, vix_level):
    """
    Suggests an options strategy based on market sentiment, stock range, and VIX level.
    """
    # Use stock_range to help decide if the stock is in a range or trending
    if 'support' in stock_range.lower() and 'resistance' in stock_range.lower():
        range_bound = True
    else:
        range_bound = False

    if vix_level > 20:
        if market_sentiment == 'bullish':
            return 'Bull Put Spread' if not range_bound else 'Iron Condor'
        elif market_sentiment == 'bearish':
            return 'Bear Call Spread' if not range_bound else 'Iron Condor'
        else:
            return 'Iron Condor or Butterfly'
    else:
        if market_sentiment == 'bullish':
            return 'Long Call Butterfly' if not range_bound else 'Broken Wing Butterfly'
        elif market_sentiment == 'bearish':
            return 'Long Put Butterfly' if not range_bound else 'Broken Wing Butterfly'
        else:
            return 'Broken Wing Butterfly'

def trade_fits_plan(credit, max_risk, expiration_days, entry_day, holding_period, trades_this_week, trades_today):
    checks = {
        'Credit $100–$150': 100 <= credit <= 150,
        'Max risk $350–$400': 350 <= max_risk <= 400,
        'Expiration 10–14 days out': 10 <= expiration_days <= 14,
        'Entry Mon/Tue/Wed': entry_day in ['Monday', 'Tuesday', 'Wednesday'],
        '1-week holding': holding_period == 7,
        '2–4 trades/week, max 2/day': 2 <= trades_this_week <= 4 and trades_today <= 2
    }
    return checks

def analyze_trade(symbol, market_sentiment, stock_range, vix_level, credit, max_risk, expiration_date, entry_date, holding_period, trades_this_week, trades_today):
    strategy = suggest_strategy(market_sentiment, stock_range, vix_level)
    expiration_days = (expiration_date - entry_date).days
    entry_day = entry_date.strftime('%A')
    checks = trade_fits_plan(credit, max_risk, expiration_days, entry_day, holding_period, trades_this_week, trades_today)
    print(f"\nTrade Analysis for {symbol}")
    print(f"Market Sentiment: {market_sentiment}")
    print(f"Stock Range: {stock_range}")
    print(f"VIX Level: {vix_level}")
    print(f"Strategy (AI Suggested): {strategy}")
    print(f"Credit: ${credit}")
    print(f"Max Risk: ${max_risk}")
    print(f"Expiration: {expiration_date} ({expiration_days} days)")
    print(f"Entry Date: {entry_date} ({entry_day})")
    print(f"Holding Period: {holding_period} days")
    print("\nChecklist:")
    for item, passed in checks.items():
        print(f"[{'x' if passed else ' '}] {item}")
    print("\nNotes: Fill in additional notes and hedging plan as needed.")

# Example usage
if __name__ == "__main__":
    symbol = "QQQ"
    market_sentiment = "bullish"  # or 'bearish', 'neutral'
    stock_range = "Support 530, Resistance 550"
    vix_level = 18
    credit = 120
    max_risk = 380
    expiration_date = datetime.date(2025, 7, 10)
    entry_date = datetime.date(2025, 6, 30)
    holding_period = 7
    trades_this_week = 2
    trades_today = 1
    analyze_trade(symbol, market_sentiment, stock_range, vix_level, credit, max_risk, expiration_date, entry_date, holding_period, trades_this_week, trades_today)
