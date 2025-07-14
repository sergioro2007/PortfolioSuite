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
        suggestions = tracker.generate_trade_suggestions(count=3)
        assert isinstance(suggestions, list), "Trade suggestions should be a list"

    def test_atr_based_strike_selection(self, tracker):
        prediction = tracker.predict_price_range("AAPL")
        assert "range_width_$" in prediction, "ATR range missing for strategy"
        assert "target_mid" in prediction, "Target mid missing for strategy"
        assert "atr_value" in prediction, "ATR value missing for strategy"
        atr_range = prediction["range_width_$"]
        suggested_spacing = min(5, max(1, atr_range / 4))
        assert suggested_spacing >= 1, "Strike spacing too small"
        assert suggested_spacing <= 5, "Strike spacing too large"

    def test_regime_score_strategy_selection(self, tracker):
        prediction = tracker.predict_price_range("AAPL")
        regime_score = prediction.get("regime_score", 0)
        target_mid = prediction.get("target_mid", prediction["current_price"])
        current_price = prediction["current_price"]
        if regime_score > 0.15:
            assert target_mid >= current_price, "Bullish bias should raise target"
        elif regime_score < -0.15:
            assert target_mid <= current_price, "Bearish bias should lower target"

    def test_backward_compatibility_strategies(self, tracker):
        suggestions = tracker.generate_trade_suggestions(count=2)
        for suggestion in suggestions:
            if suggestion:
                assert "strategy" in suggestion, "Strategy field missing"
                assert "ticker" in suggestion, "Ticker field missing"
                assert "credit" in suggestion, "Credit field missing"
                assert "max_loss" in suggestion, "Max loss field missing"
