"""
🛡️ Long-Term Quality Stocks Tracker Module  
==========================================

Conservative, defensive, high-quality stock screening for long-term investors.
Focus on fundamental quality, defensive characteristics, and long-term performance.
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

# Quality screening constants
DEFENSIVE_SECTORS = {
    'Consumer Staples': ['KO', 'PG', 'PEP', 'WMT', 'CL', 'KMB', 'GIS', 'K', 'CPB', 'CLX'],
    'Healthcare': ['JNJ', 'ABT', 'PFE', 'MRK', 'UNH', 'CVS', 'MDT', 'TMO', 'DHR', 'BMY'],
    'Utilities': ['ES', 'NEE', 'DTE', 'AEP', 'EXC', 'SO', 'D', 'PEG', 'XEL', 'ED'],
    'Real Estate': ['O', 'WELL', 'VTR', 'AMT', 'CCI', 'EQIX', 'PLD', 'SPG', 'EQR', 'AVB'],
    'Quality Energy': ['XOM', 'CVX', 'EPD', 'KMI', 'OKE', 'ENB', 'SRE', 'TRP', 'ET', 'MPLX']
}

PRE_SEED_UNIVERSE = [
    'JNJ', 'KO', 'PG', 'PEP', 'MSFT', 'ABT', 'XOM', 'CVX', 'EPD', 'ES', 'O',
    'UNH', 'MRK', 'NEE', 'WMT', 'CL', 'VZ', 'T', 'MDT', 'TMO', 'DHR', 'BMY',
    'PFE', 'DTE', 'AEP', 'EXC', 'SO', 'D', 'AMT', 'CCI', 'EQIX', 'PLD'
]

def run_quality_tracker():
    """Main function to run the long-term quality stocks tracker interface"""
    
    st.markdown("## 🛡️ Long-Term Quality Stocks Tracker")
    st.markdown("*Conservative, defensive, high-quality stock screening for long-term investors*")
    
    # Initialize tracker
    tracker = QualityStocksTracker()
    
    # Sidebar configuration
    st.sidebar.markdown("### 🎯 Quality Screening Configuration")
    
    portfolio_size = st.sidebar.slider("Portfolio Size", 5, 20, 10, 
                                      help="Number of quality stocks to select")
    
    min_roe = st.sidebar.slider("Minimum ROE (%)", 5, 25, 10, 
                               help="5-year average ROE threshold")
    
    max_beta = st.sidebar.slider("Maximum Beta", 0.5, 1.5, 1.2, 0.1,
                                help="Maximum volatility (beta) allowed")
    
    min_dividend_yield = st.sidebar.slider("Minimum Dividend Yield (%)", 0.0, 8.0, 1.0, 0.5,
                                          help="Minimum dividend yield requirement")
    
    min_market_cap = st.sidebar.selectbox("Minimum Market Cap", 
                                         ["$10B", "$25B", "$50B", "$100B"],
                                         index=1, help="Minimum market capitalization")
    
    st.sidebar.markdown("### 🛡️ Defensive Sector Focus")
    
    preferred_sectors = st.sidebar.multiselect(
        "Preferred Defensive Sectors",
        list(DEFENSIVE_SECTORS.keys()),
        default=["Consumer Staples", "Healthcare", "Utilities"],
        help="Focus on specific defensive sectors"
    )
    
    exclude_unprofitable = st.sidebar.checkbox("Exclude Unprofitable Stocks", True,
                                              help="Require positive net income and free cash flow")
    
    require_dividend_history = st.sidebar.checkbox("Require Dividend History", True,
                                                   help="Require consistent dividend payments")
    
    # Main content
    if st.button("🔍 Run Quality Analysis", type="primary"):
        with st.spinner("🔍 Analyzing quality stocks and fundamentals..."):
            
            # Run screening
            results = run_quality_screening(tracker, portfolio_size, min_roe, max_beta, 
                                          min_dividend_yield, min_market_cap, preferred_sectors,
                                          exclude_unprofitable, require_dividend_history)
            
            if results:
                # Display results
                display_quality_results(results, tracker)
                
                # Generate weekly tracking
                display_weekly_tracking(results, tracker)
            else:
                st.warning("No qualifying quality stocks found with current screening criteria.")
    
    # Educational section
    display_quality_education()


class QualityStocksTracker:
    """Tracker for long-term quality stocks analysis"""
    
    def __init__(self):
        self.results_file = "quality_results.pkl"
        self.spy_benchmark = None
    
    def get_stock_fundamentals(self, ticker: str) -> Dict:
        """Get fundamental data for a stock"""
        try:
            stock = yf.Ticker(ticker)
            
            # Get basic info
            info = stock.info
            
            # Get financial data
            financials = stock.financials
            balance_sheet = stock.balance_sheet
            cash_flow = stock.cashflow
            
            # Get historical data for performance analysis
            hist_data = stock.history(period="5y")
            
            if hist_data.empty:
                return None
            
            # Calculate key metrics
            current_price = hist_data['Close'].iloc[-1]
            
            # Performance metrics
            ytd_return = self.calculate_ytd_return(hist_data)
            one_year_return = self.calculate_period_return(hist_data, 252)  # ~1 year
            five_year_return = self.calculate_period_return(hist_data, 1260)  # ~5 years
            
            # Volatility (beta approximation)
            if self.spy_benchmark is None:
                spy = yf.Ticker("SPY")
                self.spy_benchmark = spy.history(period="5y")
            
            beta = self.calculate_beta(hist_data, self.spy_benchmark)
            
            # Dividend yield
            dividend_yield = info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0
            
            # Market cap
            market_cap = info.get('marketCap', 0)
            
            # Financial metrics
            net_income = info.get('netIncomeToCommon', 0)
            free_cash_flow = info.get('freeCashflow', 0)
            roe = info.get('returnOnEquity', 0) * 100 if info.get('returnOnEquity') else 0
            
            # Sector and industry
            sector = info.get('sector', 'Unknown')
            industry = info.get('industry', 'Unknown')
            
            return {
                'ticker': ticker,
                'company_name': info.get('longName', ticker),
                'sector': sector,
                'industry': industry,
                'current_price': current_price,
                'market_cap': market_cap,
                'dividend_yield': dividend_yield,
                'beta': beta,
                'ytd_return': ytd_return,
                'one_year_return': one_year_return,
                'five_year_return': five_year_return,
                'net_income': net_income,
                'free_cash_flow': free_cash_flow,
                'roe': roe,
                'info': info
            }
            
        except Exception as e:
            st.warning(f"Error analyzing {ticker}: {str(e)}")
            return None
    
    def calculate_ytd_return(self, hist_data: pd.DataFrame) -> float:
        """Calculate year-to-date return"""
        try:
            current_year = datetime.now().year
            ytd_start = datetime(current_year, 1, 1)
            
            # Find the first trading day of the year
            ytd_data = hist_data[hist_data.index >= ytd_start]
            if len(ytd_data) < 2:
                return 0.0
            
            start_price = ytd_data['Close'].iloc[0]
            current_price = ytd_data['Close'].iloc[-1]
            
            return ((current_price - start_price) / start_price) * 100
        except:
            return 0.0
    
    def calculate_period_return(self, hist_data: pd.DataFrame, days: int) -> float:
        """Calculate return over a specific period"""
        try:
            if len(hist_data) < days:
                return 0.0
            
            start_price = hist_data['Close'].iloc[-days]
            end_price = hist_data['Close'].iloc[-1]
            
            return ((end_price - start_price) / start_price) * 100
        except:
            return 0.0
    
    def calculate_beta(self, stock_data: pd.DataFrame, benchmark_data: pd.DataFrame) -> float:
        """Calculate beta relative to benchmark"""
        try:
            # Align data by date
            combined = pd.concat([stock_data['Close'], benchmark_data['Close']], axis=1, join='inner')
            combined.columns = ['stock', 'benchmark']
            
            # Calculate returns
            combined['stock_returns'] = combined['stock'].pct_change()
            combined['benchmark_returns'] = combined['benchmark'].pct_change()
            
            # Drop NaN values
            combined = combined.dropna()
            
            if len(combined) < 50:  # Need sufficient data
                return 1.0
            
            # Calculate beta
            covariance = combined['stock_returns'].cov(combined['benchmark_returns'])
            benchmark_variance = combined['benchmark_returns'].var()
            
            if benchmark_variance == 0:
                return 1.0
            
            beta = covariance / benchmark_variance
            return beta
        except:
            return 1.0
    
    def passes_quality_filters(self, stock_data: Dict, min_roe: float, max_beta: float,
                             min_dividend_yield: float, min_market_cap_str: str,
                             preferred_sectors: List[str], exclude_unprofitable: bool,
                             require_dividend_history: bool) -> bool:
        """Check if stock passes quality filters"""
        
        if not stock_data:
            return False
        
        # Market cap filter
        market_cap_thresholds = {
            "$10B": 10e9,
            "$25B": 25e9,
            "$50B": 50e9,
            "$100B": 100e9
        }
        
        min_market_cap = market_cap_thresholds.get(min_market_cap_str, 25e9)
        if stock_data['market_cap'] < min_market_cap:
            return False
        
        # Beta filter
        if stock_data['beta'] > max_beta:
            return False
        
        # ROE filter
        if stock_data['roe'] < min_roe:
            return False
        
        # Dividend yield filter
        if stock_data['dividend_yield'] < min_dividend_yield:
            return False
        
        # Profitability filter
        if exclude_unprofitable:
            if stock_data['net_income'] <= 0 or stock_data['free_cash_flow'] <= 0:
                return False
        
        # Dividend history filter
        if require_dividend_history:
            if stock_data['dividend_yield'] < 0.5:  # Minimum threshold for dividend history
                return False
        
        # Sector filter
        if preferred_sectors and stock_data['sector'] not in preferred_sectors:
            # Check if ticker is in preferred sector stocks
            ticker_in_preferred = False
            for sector in preferred_sectors:
                if sector in DEFENSIVE_SECTORS and stock_data['ticker'] in DEFENSIVE_SECTORS[sector]:
                    ticker_in_preferred = True
                    break
            
            if not ticker_in_preferred:
                return False
        
        return True


def run_quality_screening(tracker: QualityStocksTracker, portfolio_size: int, min_roe: float,
                         max_beta: float, min_dividend_yield: float, min_market_cap: str,
                         preferred_sectors: List[str], exclude_unprofitable: bool,
                         require_dividend_history: bool) -> List[Dict]:
    """Run the quality stock screening process"""
    
    # Build universe of stocks to screen
    universe = PRE_SEED_UNIVERSE.copy()
    
    # Add stocks from preferred sectors
    for sector in preferred_sectors:
        if sector in DEFENSIVE_SECTORS:
            universe.extend(DEFENSIVE_SECTORS[sector])
    
    # Remove duplicates
    universe = list(set(universe))
    
    # Screen each stock
    qualified_stocks = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, ticker in enumerate(universe):
        status_text.text(f"Analyzing {ticker}... ({i+1}/{len(universe)})")
        progress_bar.progress((i + 1) / len(universe))
        
        # Get fundamental data
        stock_data = tracker.get_stock_fundamentals(ticker)
        
        if stock_data and tracker.passes_quality_filters(
            stock_data, min_roe, max_beta, min_dividend_yield, min_market_cap,
            preferred_sectors, exclude_unprofitable, require_dividend_history
        ):
            qualified_stocks.append(stock_data)
    
    # Clean up progress indicators
    progress_bar.empty()
    status_text.empty()
    
    # Sort by quality score (combination of metrics)
    for stock in qualified_stocks:
        stock['quality_score'] = calculate_quality_score(stock)
    
    qualified_stocks.sort(key=lambda x: x['quality_score'], reverse=True)
    
    # Limit to portfolio size
    return qualified_stocks[:portfolio_size]


def calculate_quality_score(stock_data: Dict) -> float:
    """Calculate a composite quality score"""
    
    score = 0
    
    # ROE contribution (0-25 points)
    roe = stock_data['roe']
    score += min(roe, 25)
    
    # Dividend yield contribution (0-20 points)
    div_yield = stock_data['dividend_yield']
    score += min(div_yield * 2.5, 20)
    
    # Low volatility bonus (0-15 points)
    beta = stock_data['beta']
    if beta < 0.8:
        score += 15
    elif beta < 1.0:
        score += 10
    elif beta < 1.2:
        score += 5
    
    # Performance contribution (0-30 points)
    five_year_return = stock_data['five_year_return']
    if five_year_return > 100:  # >100% over 5 years
        score += 30
    elif five_year_return > 50:
        score += 20
    elif five_year_return > 20:
        score += 10
    
    # Market cap stability bonus (0-10 points)
    market_cap = stock_data['market_cap']
    if market_cap > 100e9:  # >$100B
        score += 10
    elif market_cap > 50e9:
        score += 5
    
    return score


def display_quality_results(results: List[Dict], tracker: QualityStocksTracker):
    """Display quality stock analysis results"""
    
    st.markdown("### 🛡️ Quality Stock Analysis Results")
    
    if not results:
        st.warning("No stocks qualified under the current screening criteria.")
        return
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Qualified Stocks", len(results))
    
    with col2:
        avg_dividend_yield = np.mean([r['dividend_yield'] for r in results])
        st.metric("Avg Dividend Yield", f"{avg_dividend_yield:.1f}%")
    
    with col3:
        avg_beta = np.mean([r['beta'] for r in results])
        st.metric("Avg Beta", f"{avg_beta:.2f}")
    
    with col4:
        avg_roe = np.mean([r['roe'] for r in results])
        st.metric("Avg ROE", f"{avg_roe:.1f}%")
    
    # Detailed results table
    st.markdown("#### 📊 Detailed Quality Analysis")
    
    # Prepare data for display
    display_data = []
    for stock in results:
        display_data.append({
            'Ticker': stock['ticker'],
            'Company': stock['company_name'][:30] + "..." if len(stock['company_name']) > 30 else stock['company_name'],
            'Sector': stock['sector'],
            'Price': f"${stock['current_price']:.2f}",
            'Market Cap': f"${stock['market_cap']/1e9:.1f}B",
            'Div Yield': f"{stock['dividend_yield']:.1f}%",
            'Beta': f"{stock['beta']:.2f}",
            'ROE': f"{stock['roe']:.1f}%",
            'YTD Return': f"{stock['ytd_return']:.1f}%",
            '1Y Return': f"{stock['one_year_return']:.1f}%",
            '5Y Return': f"{stock['five_year_return']:.1f}%",
            'Quality Score': f"{stock['quality_score']:.1f}"
        })
    
    df = pd.DataFrame(display_data)
    st.dataframe(df, use_container_width=True)
    
    # Sector breakdown
    st.markdown("#### 🏢 Sector Allocation")
    
    sector_counts = {}
    for stock in results:
        sector = stock['sector']
        sector_counts[sector] = sector_counts.get(sector, 0) + 1
    
    sector_df = pd.DataFrame(list(sector_counts.items()), columns=['Sector', 'Count'])
    sector_df['Percentage'] = (sector_df['Count'] / len(results) * 100).round(1)
    
    st.dataframe(sector_df, use_container_width=True)


def display_weekly_tracking(results: List[Dict], tracker: QualityStocksTracker):
    """Display weekly tracking information"""
    
    st.markdown("### 📅 Weekly Tracking Overview")
    
    st.info("""
    **🔄 Weekly Tracking Logic:**
    
    - **Consistency Check**: Monitor if stocks maintain quality criteria
    - **Performance Update**: Track 1-week and 1-month returns
    - **Flag Changes**: Alert if any stock drops out of filters
    - **Minimal Turnover**: Expect very low rotation week-to-week
    """)
    
    # Performance tracking preview
    st.markdown("#### 📈 Performance Tracking (This Week)")
    
    # This would be implemented with historical tracking
    st.markdown("""
    *Weekly performance tracking will be implemented with historical data storage.*
    
    **Key Metrics to Track:**
    - Weekly price change
    - Monthly performance vs SPY
    - Dividend announcements
    - Fundamental changes (earnings, ratios)
    - Sector rotation impact
    """)


def display_quality_education():
    """Display educational content about quality investing"""
    
    st.markdown("---")
    st.markdown("### 📚 Quality Investing Education")
    
    with st.expander("🎯 What Makes a Quality Stock?"):
        st.markdown("""
        **Quality stocks typically exhibit:**
        
        - **🟢 Consistent Profitability**: Positive earnings and cash flow
        - **💰 Dividend Reliability**: Regular dividend payments and history
        - **🛡️ Low Volatility**: Beta ≤ 1.2 for stability
        - **📈 Strong ROE**: Return on equity >10% demonstrates efficiency
        - **🏢 Defensive Sectors**: Consumer staples, healthcare, utilities
        - **💪 Market Leadership**: Large market cap for stability
        """)
    
    with st.expander("🎯 Long-Term Investment Strategy"):
        st.markdown("""
        **Quality investing approach:**
        
        - **🔒 Buy and Hold**: Minimal turnover, 3-10 year horizon
        - **🛡️ Risk Management**: Lower volatility than growth stocks
        - **💰 Income Generation**: Dividends provide steady cash flow
        - **🔄 Compounding**: Reinvest dividends for long-term growth
        - **📊 Diversification**: Spread across defensive sectors
        - **⚖️ Balance**: Complement growth/momentum strategies
        """)
    
    with st.expander("🎯 When to Use Quality Stocks"):
        st.markdown("""
        **Ideal market conditions:**
        
        - **🔴 Bear Markets**: Defensive characteristics shine
        - **📉 High Volatility**: Lower beta provides stability
        - **💰 Income Focus**: Retirement or income-oriented portfolios
        - **🛡️ Risk-Off Periods**: Flight to quality during uncertainty
        - **📊 Core Holdings**: 60-80% of conservative portfolios
        - **⚖️ Rebalancing**: Counterweight to growth/momentum positions
        """)
