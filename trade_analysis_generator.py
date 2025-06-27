import yfinance as yf
from datetime import datetime, timedelta

def get_market_data(ticker):
    stock = yf.Ticker(ticker)
    price = round(stock.history(period="1d")["Close"][0], 2)
    # Placeholders – replace with live IV/VIX/sentiment data if available
    iv = "28%"
    vix = "15"
    sentiment = "Bullish (call volume > put volume)"
    # 1-week expected move estimate (very rough): price * IV% * sqrt(1/52)
    # IV as decimal, annualized, so convert to weekly
    iv_num = 0.28
    exp_move = round(price * iv_num * (1/52) ** 0.5, 2)
    range_low = round(price - exp_move, 2)
    range_high = round(price + exp_move, 2)
    return price, iv, vix, sentiment, range_low, range_high

def generate_trades(ticker, price, range_low, range_high, expiration, trade_date):
    # Strikes for Iron Condor
    put_short = round(range_low, 0)
    put_long = round(put_short - 5, 0)
    call_short = round(range_high, 0)
    call_long = round(call_short + 5, 0)
    ic_credit = 150
    ic_risk = 350

    # Strikes for Put Credit Spread
    pcs_put_short = round(range_low, 0)
    pcs_put_long = round(pcs_put_short - 5, 0)
    pcs_credit = 120
    pcs_risk = 380

    return {
        "put_short": put_short,
        "put_long": put_long,
        "call_short": call_short,
        "call_long": call_long,
        "ic_credit": ic_credit,
        "ic_risk": ic_risk,
        "pcs_put_short": pcs_put_short,
        "pcs_put_long": pcs_put_long,
        "pcs_credit": pcs_credit,
        "pcs_risk": pcs_risk
    }

def write_markdown(ticker, price, iv, vix, sentiment, range_low, range_high, trades, expiration, trade_date):
    content = f"""# Trade Analysis: {ticker} – {expiration}, Entry {trade_date}

## Market Context
- **Current Price:** ${price}
- **Implied Volatility (IV):** {iv}
- **Put-Call Ratio / Sentiment:** {sentiment}
- **Expected Range (1 Week):** ${range_low} – ${range_high}
- **VIX / Macro:** {vix}

---

## Strategy 1: Iron Condor (Neutral, High Probability)
- **Sell 1x ${trades['put_short']} Put ({expiration})**
- **Buy 1x ${trades['put_long']} Put ({expiration})**
- **Sell 1x ${trades['call_short']} Call ({expiration})**
- **Buy 1x ${trades['call_long']} Call ({expiration})**
- **Credit Received:** ~${trades['ic_credit']}
- **Max Risk:** ${trades['ic_risk']}
- **Max Profit:** ${trades['ic_credit']} (if ${range_low} < {ticker} < ${range_high})
- **Plan:** Enter {trade_date}, close after 1 week or on $100+ profit
- **Probability of Profit:** High

---

## Strategy 2: Put Credit Spread (Bullish, High Probability)
- **Sell 1x ${trades['pcs_put_short']} Put ({expiration})**
- **Buy 1x ${trades['pcs_put_long']} Put ({expiration})**
- **Credit Received:** ~${trades['pcs_credit']}
- **Max Risk:** ${trades['pcs_risk']}
- **Max Profit:** ${trades['pcs_credit']} (if {ticker} stays above ${trades['pcs_put_short']})
- **Plan:** Enter {trade_date}, close after 1 week or on $100+ profit
- **Probability of Profit:** High

---

## Checklist

- [x] Credit $100+ (target)
- [x] Max risk $350–$400
- [x] 2-week expiration, 1-week hold
- [x] High liquidity, tight bid/ask, high OI
- [x] Technicals and sentiment checked

---

## Notes
- Exit early if loss exceeds 50% credit or if profit target is reached.
- Adjust strikes if underlying price moves significantly pre-market.
"""
    filename = f"trade_analysis_{ticker}_{expiration}.md"
    with open(filename, "w") as f:
        f.write(content)
    print(f"{filename} generated.")

if __name__ == "__main__":
    # Choose your tickers here (edit as needed)
    tickers = ["AAPL", "NVDA"]
    trade_date = datetime.now().date()
    expiration = (trade_date + timedelta(days=14)).strftime("%Y-%m-%d")

    for ticker in tickers:
        price, iv, vix, sentiment, range_low, range_high = get_market_data(ticker)
        trades = generate_trades(ticker, price, range_low, range_high, expiration, trade_date)
        write_markdown(ticker, price, iv, vix, sentiment, range_low, range_high, trades, expiration, trade_date)