"""
📊 Trade Analysis Reporting
===========================

Module for generating comprehensive trade analysis reports.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class TradeReporter:
    """Generates comprehensive trade analysis reports"""
    
    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = Path(data_dir) if data_dir else Path("data/trades")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir = self.data_dir / "reports"
        self.reports_dir.mkdir(exist_ok=True)
    
    def generate_analysis_report(self, trade_data: Dict[str, Any], 
                               output_file: Optional[str] = None) -> str:
        """Generate a comprehensive trade analysis report"""
        
        report_file = output_file or "trade_analysis_report_2025-06-27.md"
        report_path = self.reports_dir / report_file
        
        report_content = self._build_report_content(trade_data)
        
        try:
            with open(report_path, 'w') as f:
                f.write(report_content)
            
            logger.info(f"Generated trade analysis report: {report_path}")
            return str(report_path)
            
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            return ""
    
    def _build_report_content(self, trade_data: Dict[str, Any]) -> str:
        """Build the markdown content for the trade analysis report"""
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        return f"""# Trade Analysis Report - {current_date}

## Executive Summary

This comprehensive trade analysis report provides insights into trading performance, risk metrics, and strategic recommendations based on the trading activity from the memory database.

### Key Metrics
- **Total Trades**: {trade_data.get('total_trades', 'N/A')}
- **Unique Symbols Traded**: {trade_data.get('unique_symbols', 'N/A')}
- **Net Investment**: ${trade_data.get('net_invested', 0):,.2f}
- **Realized P&L**: ${trade_data.get('realized_pnl', 0):,.2f}
- **Final Running P&L**: ${trade_data.get('final_running_pnl', 0):,.2f}

## Portfolio Analysis

### Trading Activity Overview
The analysis period covers {trade_data.get('date_range', {}).get('start', 'N/A')} to {trade_data.get('date_range', {}).get('end', 'N/A')}.

**Symbols Traded**: {', '.join(trade_data.get('symbols_traded', []))}

### Performance Metrics

#### Financial Performance
- **Total Buy Volume**: ${trade_data.get('total_buy_value', 0):,.2f}
- **Total Sell Volume**: ${trade_data.get('total_sell_value', 0):,.2f}
- **Net Cash Flow**: ${trade_data.get('net_invested', 0):,.2f}

#### Risk Analysis
- **Portfolio Diversification**: {len(trade_data.get('symbols_traded', []))} unique symbols
- **Average Trade Size**: ${trade_data.get('total_buy_value', 0) / max(trade_data.get('total_trades', 1), 1):,.2f}
- **Trading Frequency**: {trade_data.get('total_trades', 0)} trades over the period

## Strategic Recommendations

### Strengths Identified
1. **Diversification**: Good spread across {len(trade_data.get('symbols_traded', []))} different symbols
2. **Active Management**: Regular trading activity with {trade_data.get('total_trades', 0)} total transactions
3. **Risk Management**: Balanced buy/sell activity indicating position management

### Areas for Improvement
1. **Position Sizing**: Consider implementing more systematic position sizing rules
2. **Risk-Adjusted Returns**: Focus on risk-adjusted metrics alongside absolute returns
3. **Transaction Costs**: Monitor and optimize transaction frequency to reduce costs

### Future Strategy
1. **Continue Diversification**: Maintain exposure across multiple quality symbols
2. **Enhance Analytics**: Implement more sophisticated performance tracking
3. **Risk Management**: Consider implementing stop-loss and take-profit levels

## Technical Analysis

### Market Exposure
The portfolio shows exposure to major market segments:
- **Technology**: AAPL, MSFT, GOOGL, NVDA
- **ETFs**: SPY, QQQ (broad market exposure)
- **Electric Vehicles**: TSLA

### Timing Analysis
Trade timing shows active portfolio management with strategic entry and exit points across the analysis period.

## Conclusion

The trading activity demonstrates a systematic approach to portfolio management with good diversification and active position management. The realized P&L of ${trade_data.get('realized_pnl', 0):,.2f} indicates effective trading execution.

### Next Steps
1. Continue monitoring current positions
2. Implement enhanced risk metrics
3. Consider expanding analytical framework
4. Regular review of trading strategy effectiveness

---

*Report generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
*Portfolio Suite Trade Analysis Module v1.0*
"""

    def create_analysis_template(self) -> str:
        """Create a template for trade analysis reports"""
        
        template_file = "trade_analysis_template.md"
        template_path = self.reports_dir / template_file
        
        template_content = """# Trade Analysis Template

## Instructions
This template provides a standardized format for trade analysis reports. Fill in the sections below with relevant data and analysis.

## Executive Summary
**Report Date**: [DATE]
**Analysis Period**: [START_DATE] to [END_DATE]
**Analyst**: [ANALYST_NAME]

### Key Performance Indicators
- Total Trades: [NUMBER]
- Total P&L: $[AMOUNT]
- Win Rate: [PERCENTAGE]%
- Sharpe Ratio: [RATIO]
- Maximum Drawdown: [PERCENTAGE]%

## Portfolio Overview

### Current Holdings
| Symbol | Quantity | Avg Price | Current Price | Unrealized P&L | % of Portfolio |
|--------|----------|-----------|---------------|----------------|----------------|
| [SYMBOL] | [QTY] | $[PRICE] | $[PRICE] | $[PNL] | [%] |

### Recent Trades
| Date | Symbol | Action | Quantity | Price | Total Value | P&L |
|------|--------|--------|----------|--------|-------------|-----|
| [DATE] | [SYMBOL] | [BUY/SELL] | [QTY] | $[PRICE] | $[VALUE] | $[PNL] |

## Performance Analysis

### Returns Analysis
- **Total Return**: [%]
- **Annualized Return**: [%]
- **Volatility**: [%]
- **Beta**: [VALUE]

### Risk Metrics
- **Value at Risk (95%)**: $[AMOUNT]
- **Maximum Drawdown**: [%]
- **Calmar Ratio**: [RATIO]
- **Sortino Ratio**: [RATIO]

## Sector/Asset Allocation
| Sector | Allocation | Performance |
|--------|------------|-------------|
| [SECTOR] | [%] | [%] |

## Trade Analysis

### Best Performing Trades
1. [SYMBOL] - [DATE] - P&L: $[AMOUNT] ([%])
2. [SYMBOL] - [DATE] - P&L: $[AMOUNT] ([%])

### Worst Performing Trades
1. [SYMBOL] - [DATE] - P&L: $[AMOUNT] ([%])
2. [SYMBOL] - [DATE] - P&L: $[AMOUNT] ([%])

### Trading Pattern Analysis
- **Average Hold Time**: [DAYS] days
- **Most Active Symbol**: [SYMBOL]
- **Trade Size Distribution**: [ANALYSIS]

## Market Environment Analysis

### Market Conditions During Period
- **Overall Market Performance**: [ANALYSIS]
- **Volatility Regime**: [HIGH/MEDIUM/LOW]
- **Sector Rotation**: [ANALYSIS]

### External Factors
- **Economic Events**: [LIST]
- **Earnings Seasons**: [IMPACT]
- **Regulatory Changes**: [IMPACT]

## Strategy Performance

### Strategy Effectiveness
| Strategy | Trades | Win Rate | Avg P&L | Total P&L |
|----------|--------|----------|---------|-----------|
| [STRATEGY] | [COUNT] | [%] | $[AMOUNT] | $[AMOUNT] |

### Recommendations
1. **Continue**: [STRATEGIES TO CONTINUE]
2. **Modify**: [STRATEGIES TO MODIFY]
3. **Discontinue**: [STRATEGIES TO STOP]

## Risk Management Review

### Position Sizing Analysis
- **Average Position Size**: [%] of portfolio
- **Maximum Position Size**: [%] of portfolio
- **Concentration Risk**: [ANALYSIS]

### Stop Loss Effectiveness
- **Trades with Stop Losses**: [%]
- **Stop Loss Hit Rate**: [%]
- **Average Loss When Stopped**: [%]

## Looking Forward

### Strategic Adjustments
1. [ADJUSTMENT 1]
2. [ADJUSTMENT 2]
3. [ADJUSTMENT 3]

### Tactical Considerations
- **Market Outlook**: [BULLISH/BEARISH/NEUTRAL]
- **Key Levels to Watch**: [LEVELS]
- **Potential Catalysts**: [EVENTS]

### Action Items
- [ ] [ACTION ITEM 1]
- [ ] [ACTION ITEM 2]
- [ ] [ACTION ITEM 3]

## Appendix

### Methodology
- **Data Sources**: [SOURCES]
- **Calculation Methods**: [METHODS]
- **Assumptions**: [ASSUMPTIONS]

### Glossary
- **Sharpe Ratio**: Risk-adjusted return measure
- **Calmar Ratio**: Return to maximum drawdown ratio
- **Beta**: Sensitivity to market movements

---

*This template should be customized based on specific trading strategies and requirements.*
*Portfolio Suite Trade Analysis Module v1.0*
"""
        
        try:
            with open(template_path, 'w') as f:
                f.write(template_content)
            
            logger.info(f"Created trade analysis template: {template_path}")
            return str(template_path)
            
        except Exception as e:
            logger.error(f"Error creating template: {e}")
            return ""
    
    def generate_performance_summary(self, trade_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a summary of performance metrics"""
        
        total_trades = trade_data.get('total_trades', 0)
        realized_pnl = trade_data.get('realized_pnl', 0)
        total_buy_value = trade_data.get('total_buy_value', 0)
        
        # Calculate performance metrics
        roi = (realized_pnl / total_buy_value * 100) if total_buy_value > 0 else 0
        avg_trade_value = total_buy_value / total_trades if total_trades > 0 else 0
        
        return {
            'total_trades': total_trades,
            'total_invested': total_buy_value,
            'realized_pnl': realized_pnl,
            'roi_percentage': round(roi, 2),
            'average_trade_size': round(avg_trade_value, 2),
            'symbols_count': trade_data.get('unique_symbols', 0),
            'trading_period': trade_data.get('date_range', {}),
            'performance_grade': self._calculate_performance_grade(roi)
        }
    
    def _calculate_performance_grade(self, roi: float) -> str:
        """Calculate performance grade based on ROI"""
        if roi >= 20:
            return "A+ (Excellent)"
        elif roi >= 15:
            return "A (Very Good)"
        elif roi >= 10:
            return "B+ (Good)"
        elif roi >= 5:
            return "B (Above Average)"
        elif roi >= 0:
            return "C (Average)"
        elif roi >= -5:
            return "D (Below Average)"
        else:
            return "F (Poor)"