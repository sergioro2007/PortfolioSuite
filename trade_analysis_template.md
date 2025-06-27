# Trade Analysis: {TICKER} – {Expiration Date}, Entry {Trade Date}

## Market Context
- **Current Price:** {price}
- **Implied Volatility (IV):** {iv}
- **Put-Call Ratio / Sentiment:** {sentiment}
- **Expected Range (1 Week):** ${range_low} – ${range_high}
- **VIX / Macro:** {vix}

---

## Strategy 1: Iron Condor (Neutral, High Probability)
- **Sell 1x ${put_short} Put ({expiration})**
- **Buy 1x ${put_long} Put ({expiration})**
- **Sell 1x ${call_short} Call ({expiration})**
- **Buy 1x ${call_long} Call ({expiration})**
- **Credit Received:** ~${ic_credit}
- **Max Risk:** ${ic_risk}
- **Max Profit:** ${ic_credit} (if {range_low} < {ticker} < {range_high})
- **Plan:** Enter {trade_date}, close after 1 week or on $100+ profit
- **Probability of Profit:** High

---

## Strategy 2: Put Credit Spread (Bullish, High Probability)
- **Sell 1x ${pcs_put_short} Put ({expiration})**
- **Buy 1x ${pcs_put_long} Put ({expiration})**
- **Credit Received:** ~${pcs_credit}
- **Max Risk:** ${pcs_risk}
- **Max Profit:** ${pcs_credit} (if {ticker} stays above ${pcs_put_short})
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