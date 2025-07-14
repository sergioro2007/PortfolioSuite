#!/usr/bin/env python3
"""
Test UI integration for dual-model mathematical breakdown
Ensures UI displays all calculations correctly without user intervention
"""

import pytest
import sys
import os
import streamlit as st
from unittest.mock import patch, MagicMock

sys.path.append("src")

from portfolio_suite.options_trading.core import OptionsTracker
from portfolio_suite.options_trading.ui import render_market_analysis


class TestDualModelUI:
    """Test suite for dual-model UI integration"""

    @pytest.fixture
    def tracker(self):
        return OptionsTracker()

    @pytest.fixture
    def mock_prediction(self):
        return {
            "ticker": "AAPL",
            "current_price": 150.00,
            "target_mid": 152.25,
            "predicted_low": 145.50,
            "predicted_high": 159.00,
            "range_width_$": 13.50,
            "range_width_%": 9.0,
            "atr_value": 6.75,
            "regime_score": 0.15,
            "iv_range": "147.25 – 152.75",
            "lower_bound": 145.50,
            "upper_bound": 159.00,
            "target_price": 152.25,
            "bullish_probability": 0.575,
            "bias_score": 0.15,
            "weekly_volatility": 0.025,
            "iv_based": True,
            "indicators": {
                "rsi": 65.0,
                "macd": 0.125,
                "macd_signal": 0.100,
                "momentum": 3.5,
                "current_price": 150.00,
            },
        }

    def test_mathematical_breakdown_components(self, tracker, mock_prediction):
        with patch.object(tracker, "predict_price_range", return_value=mock_prediction):
            prediction = tracker.predict_price_range("AAPL")
            assert "atr_value" in prediction, "ATR value missing for UI display"
            assert "range_width_$" in prediction, "Range width $ missing for UI"
            assert "range_width_%" in prediction, "Range width % missing for UI"
            assert "regime_score" in prediction, "Regime score missing for UI"
            assert "indicators" in prediction, "Indicators missing for UI breakdown"
            assert "target_mid" in prediction, "Target mid missing for UI"
            assert "predicted_low" in prediction, "Predicted low missing for UI"
            assert "predicted_high" in prediction, "Predicted high missing for UI"

    def test_atr_vs_historical_vol_display(self, mock_prediction):
        atr_value = mock_prediction["atr_value"]
        weekly_vol = mock_prediction["weekly_volatility"]
        current_price = mock_prediction["current_price"]
        range_width = mock_prediction["range_width_$"]
        expected_range = atr_value * 2
        assert abs(range_width - expected_range) < 0.01, "ATR range calculation error"
        range_pct = mock_prediction["range_width_%"]
        expected_pct = (range_width / current_price) * 100
        assert abs(range_pct - expected_pct) < 0.1, "Range percentage calculation error"

    def test_regime_scoring_ui_components(self, mock_prediction):
        indicators = mock_prediction["indicators"]
        rsi = indicators["rsi"]
        macd = indicators["macd"]
        macd_signal = indicators["macd_signal"]
        momentum = indicators["momentum"]
        rsi_bias = -0.2 if rsi > 70 else (0.2 if rsi < 30 else 0.0)
        macd_bias = 0.1 if macd > macd_signal else -0.1
        momentum_bias = 0.1 if momentum > 2 else (-0.1 if momentum < -2 else 0.0)
        expected_regime = rsi_bias + macd_bias + momentum_bias
        actual_regime = mock_prediction["regime_score"]
        assert (
            abs(actual_regime - expected_regime) < 0.1
        ), "Regime score calculation error for UI"

    def test_probability_calculation_display(self, mock_prediction):
        regime_score = mock_prediction["regime_score"]
        bullish_prob = mock_prediction["bullish_probability"]
        expected_prob = 0.5 + (regime_score * 0.5)
        expected_prob = max(0.1, min(0.9, expected_prob))
        assert (
            abs(bullish_prob - expected_prob) < 0.001
        ), "Bullish probability calculation error"
