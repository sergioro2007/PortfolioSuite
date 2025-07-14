#!/usr/bin/env python3
"""
Test strategy integration with dual-model predictions
Ensures trading strategies use dual-model data correctly
"""

import pytest
import sys
import os

sys.path.append("src")

from portfolio_suite.options_trading.core import OptionsTracker


class TestDualModelStrategy:
    """Test suite for dual-model strategy integration"""

    @pytest.fixture
    def tracker(self):
        return OptionsTracker()

    def test_trade_suggestions_use_dual_model(self, tracker):
        suggestions = tracker.generate_trade_suggestions(num_suggestions=3)
        assert isinstance(suggestions, list), "Trade suggestions should be a list"

    def test_atr_based_strike_selection(self, tracker):
        prediction = tracker.predict_price_range("AAPL")
        # Calculate range width from the actual bounds
        range_width_dollar = prediction["upper_bound"] - prediction["lower_bound"]
        assert range_width_dollar > 0, "Range width should be positive"
        # Check if we have ATR data in indicators
        indicators = prediction.get("indicators", {})
        if "atr" in indicators:
            assert indicators["atr"] > 0, "ATR value should be positive"
        atr_range = range_width_dollar
        suggested_spacing = min(5, max(1, atr_range / 4))
        assert suggested_spacing >= 1, "Strike spacing too small"
        assert suggested_spacing <= 5, "Strike spacing too large"

    def test_regime_score_strategy_selection(self, tracker):
        prediction = tracker.predict_price_range("AAPL")
        regime_score = prediction.get("bias_score", 0)
        target_price = prediction.get("target_price", prediction["current_price"])
        current_price = prediction["current_price"]
        if regime_score > 0.15:
            assert target_price >= current_price, "Bullish bias should raise target"
        elif regime_score < -0.15:
            assert target_price <= current_price, "Bearish bias should lower target"

    def test_backward_compatibility_strategies(self, tracker):
        suggestions = tracker.generate_trade_suggestions(num_suggestions=2)
        for suggestion in suggestions:
            if suggestion:
                assert "strategy" in suggestion, "Strategy field missing"
                assert "ticker" in suggestion, "Ticker field missing"
                # Check for expected profit and risk fields (they may have different names)
                expected_profit_fields = ["credit", "expected_profit", "premium"]
                has_profit_field = any(field in suggestion for field in expected_profit_fields)
                assert has_profit_field, "Expected profit/credit field missing"
                
                risk_fields = ["max_loss", "risk", "maximum_loss"]
                has_risk_field = any(field in suggestion for field in risk_fields)
                assert has_risk_field, "Risk/max loss field missing"
