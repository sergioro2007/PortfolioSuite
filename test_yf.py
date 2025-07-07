import yfinance as yf
print("Successfully imported yfinance")
stock = yf.Ticker("AAPL")
print(f"Got stock info for AAPL: {stock.info.get("regularMarketPrice")}")
