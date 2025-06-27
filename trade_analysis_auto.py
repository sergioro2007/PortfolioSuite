import yfinance as yf
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import re

def get_top_option_stocks(n=2):
    """
    Scrape Barchart's most active options page and return top n stock tickers.
    """
    url = "https://www.barchart.com/options/most-active/stocks"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.content, "html.parser")
    tickers = []
    for row in soup.select("table .bc-table-row"):
        symbol_cell = row.select_one(".symbol div")
        if symbol_cell:
            symbol = symbol_cell.get_text(strip=True)
            if re.match(r"^[A-Z]{1,5}$",