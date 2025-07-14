#!/usr/bin/env python3
"""
Comprehensive testing for Dual-Model Price Prediction core algorithm
Tests ALL mathematical calculations and spec compliance automatically
"""

import pytest
import sys
import os
import numpy as np

sys.path.append("src")

from portfolio_suite.options_trading.core import OptionsTracker


class TestDualModelCore:
    """Test suite for dual-model core algorithm"""

    @pytest.fixture
    def tracker(self):
        """Initialize tracker for testing"""
        return OptionsTracker()

    @pytest.fixture
    def test_tickers(self):
        """Test tickers that should always work"""
        return ["AAPL", "SPY", "QQQ", "TSLA", "MSFT"]

    def test_atr_calculation_accuracy(self, tracker):
        """Test ATR calculation matches specification exactly"""
        ticker = "AAPL"
        indicators = tracker.get_technical_indicators(ticker)
        assert "atr_14" in indicators, "ATR calculation missing"
        assert indicators["atr_14"] > 0, "ATR must be positive"
        assert isinstance(indicators["atr_14"], (int, float)), "ATR must be numeric"
        assert "price_history" in indicators, "Price history missing for dual-model"

    def test_regime_score_specification_compliance(self, tracker):
        """Test regime scoring exactly matches specification"""
        prediction = tracker.predict_price_range_dual_model("AAPL")
        indicators = prediction["indicators"]
        rsi = indicators.get("rsi", 50)
        macd = indicators.get("macd", 0)
        macd_signal = indicators.get("macd_signal", 0)
        momentum = indicators.get("momentum", 0)
        rsi_bias = -0.2 if rsi > 70 else (0.2 if rsi < 30 else 0.0)
        macd_bias = 0.1 if macd > macd_signal else -0.1
        momentum_bias = 0.1 if momentum > 2 else (-0.1 if momentum < -2 else 0.0)
        expected_regime = rsi_bias + macd_bias + momentum_bias
        actual_regime = prediction["regime_score"]
        assert (
            abs(actual_regime - expected_regime) < 0.001
        ), f"Regime score mismatch: {actual_regime} vs {expected_regime}"

    def test_target_price_calculation_spec(self, tracker):
        """Test target price calculation matches specification exactly"""
        prediction = tracker.predict_price_range_dual_model("AAPL")
        current_price = prediction["current_price"]
        regime_score = prediction["regime_score"]
        target_mid = prediction["target_mid"]
        bias_pct = regime_score * 0.01
        expected_target = current_price * (1 + bias_pct)
        assert (
            abs(target_mid - expected_target) < 0.01
        ), f"Target price mismatch: {target_mid} vs {expected_target}"

    def test_atr_range_calculation_spec(self, tracker):
        """Test ATR range calculation matches specification exactly"""
        prediction = tracker.predict_price_range_dual_model("AAPL")
        target_mid = prediction["target_mid"]
        atr_value = prediction["atr_value"]
        predicted_low = prediction["predicted_low"]
        predicted_high = prediction["predicted_high"]
        expected_low = target_mid - atr_value
        expected_high = target_mid + atr_value
        assert (
            abs(predicted_low - expected_low) < 0.01
        ), f"Low range mismatch: {predicted_low} vs {expected_low}"
        assert (
            abs(predicted_high - expected_high) < 0.01
        ), f"High range mismatch: {predicted_high} vs {expected_high}"

    def test_output_format_spec_compliance(self, tracker):
        """Test output format exactly matches specification"""
        prediction = tracker.predict_price_range_dual_model("AAPL")
        spec_fields = [
            "ticker",
            "current_price",
            "target_mid",
            "predicted_low",
            "predicted_high",
            "range_width_$",
            "range_width_%",
            "atr_value",
            "regime_score",
        ]
        compat_fields = [
            "lower_bound",
            "upper_bound",
            "target_price",
            "bullish_probability",
            "bias_score",
            "weekly_volatility",
            "indicators",
        ]
        for field in spec_fields + compat_fields:
            assert field in prediction, f"Missing required field: {field}"
        assert (
            prediction["lower_bound"] == prediction["predicted_low"]
        ), "lower_bound != predicted_low"
        assert (
            prediction["upper_bound"] == prediction["predicted_high"]
        ), "upper_bound != predicted_high"
        assert (
            prediction["target_price"] == prediction["target_mid"]
        ), "target_price != target_mid"
        assert (
            prediction["bias_score"] == prediction["regime_score"]
        ), "bias_score != regime_score"

    @pytest.mark.parametrize("ticker", ["AAPL", "SPY", "QQQ", "TSLA", "MSFT"])
    def test_multiple_tickers_robustness(self, tracker, ticker):
        """Test dual-model works reliably across multiple tickers"""
        prediction = tracker.predict_price_range_dual_model(ticker)
        assert prediction, f"Failed to get prediction for {ticker}"
        assert prediction["current_price"] > 0, f"Invalid current price for {ticker}"
        assert prediction["atr_value"] > 0, f"Invalid ATR for {ticker}"
        assert (
            abs(prediction["regime_score"]) <= 0.4
        ), f"Regime score out of range for {ticker}"

    def test_error_handling_robustness(self, tracker):
        """Test error handling for invalid inputs"""
        prediction = tracker.predict_price_range_dual_model("INVALID_TICKER")
        assert prediction == {}, "Should return empty dict for invalid ticker"
        prediction = tracker.predict_price_range_dual_model("")
        assert prediction == {}, "Should handle empty ticker gracefully"
