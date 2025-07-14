
# 📈 Dual-Model Stock Price Prediction Algorithm

This document outlines the technical specification and implementation logic for generating 1- to 2-week price range predictions for stocks or ETFs using a dual-model system combining ATR-based volatility and regime-based directional bias.

---

## ✅ Inputs

| Input               | Type         | Description |
|--------------------|--------------|-------------|
| `ticker`           | `str`        | Stock symbol (e.g., AAPL, SPY) |
| `price_history`    | `DataFrame`  | Daily OHLCV data (min 30–60 rows) |
| `current_price`    | `float`      | Latest closing price |
| `iv_pct` (optional)| `float`      | Weekly implied volatility in decimal (e.g., 0.035 for 3.5%) |

---

## 📊 Algorithm Steps

### Step 1: ATR Calculation
Use a 14-day ATR to estimate base volatility.

```python
atr_14 = price_history['Close'].rolling(window=14).apply(lambda x: x.max() - x.min())
```

### Step 2: Regime Score Calculation

```python
# RSI
rsi_bias = -0.2 if RSI > 70 else (0.2 if RSI < 30 else 0.0)

# MACD
macd_bias = 0.1 if MACD > MACD_Signal else -0.1

# Momentum
momentum = (current_price - price_5_days_ago) / price_5_days_ago
momentum_bias = 0.1 if momentum > 0.02 else (-0.1 if momentum < -0.02 else 0.0)

# Combined regime score
regime_score = rsi_bias + macd_bias + momentum_bias
```

### Step 3: Target Price Calculation

```python
bias_pct = regime_score * 0.01
target_price = current_price * (1 + bias_pct)
```

### Step 4: ATR Range Calculation

```python
atr_value = atr_14.iloc[-1]
predicted_low = target_price - atr_value
predicted_high = target_price + atr_value
```

### Step 5: Optional IV Overlay

```python
iv_range = current_price * iv_pct
iv_low = current_price - iv_range
iv_high = current_price + iv_range
```

---

## 📤 Output Format

```json
{
  "ticker": "AAPL",
  "current_price": 95.92,
  "target_mid": 97.84,
  "predicted_low": 90.23,
  "predicted_high": 105.44,
  "range_width_$": 15.21,
  "range_width_%": 15.86,
  "iv_range": "92.88 – 98.96"
}
```

---

## 🧠 Accuracy Tuning

- Default regime score limits: ±0.2 (tune as needed)
- Use wider ATR for high-volatility tickers (e.g., NVDA, TECL)
- IV overlay optional: used for extra context

---

## 🛠 External Requirements

- Python Libraries: `pandas`, `numpy`
- Optional APIs: `yfinance`, `alphaquery`, `finnhub` for IV and prices

---

## 🔁 Suggested Execution

| Task              | Frequency |
|------------------|-----------|
| Data fetch        | Daily     |
| Prediction update | Weekly or Biweekly |
