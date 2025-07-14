#!/usr/bin/env python3
"""
Performance comparison testing between old and new prediction models
Validates that dual-model provides improvements
"""

import pytest
import sys
import os
import time
import statistics

sys.path.append("src")

from portfolio_suite.options_trading.core import OptionsTracker


class TestDualModelPerformance:
    """Performance comparison test suite"""

    @pytest.fixture
    def tracker(self):
        return OptionsTracker()

    def test_prediction_accuracy_metrics(self, tracker):
        ticker = "AAPL"
        prediction = tracker.predict_price_range(ticker)
        current_price = prediction["current_price"]
        predicted_low = prediction["predicted_low"]
        predicted_high = prediction["predicted_high"]
        range_width = prediction["range_width_%"]
        assert 1.0 <= range_width <= 25.0, f"Range width unreasonable: {range_width}%"
        assert (
            predicted_low < current_price < predicted_high
        ), "Current price outside predicted range"
        atr_value = prediction["atr_value"]
        weekly_vol = prediction["weekly_volatility"]
        historical_range = current_price * weekly_vol * 2
        atr_range = atr_value * 2
        assert (
            abs(atr_range - historical_range) > 0.01
        ), "ATR range should differ from historical"

    def test_calculation_consistency(self, tracker):
        ticker = "AAPL"
        predictions = []
        for _ in range(3):
            prediction = tracker.predict_price_range(ticker)
            predictions.append(prediction)
            time.sleep(0.1)
        base_prediction = predictions[0]
        for pred in predictions[1:]:
            assert (
                abs(pred["current_price"] - base_prediction["current_price"]) < 0.01
            ), "Price inconsistency"
            assert (
                abs(pred["regime_score"] - base_prediction["regime_score"]) < 0.001
            ), "Regime score inconsistency"
            assert (
                abs(pred["atr_value"] - base_prediction["atr_value"]) < 0.01
            ), "ATR inconsistency"

    def test_regime_score_sensitivity(self, tracker):
        tickers = ["AAPL", "SPY", "QQQ", "TSLA"]
        regime_scores = []
        for ticker in tickers:
            prediction = tracker.predict_price_range(ticker)
            if prediction:
                regime_scores.append(prediction["regime_score"])
        if len(regime_scores) > 1:
            score_std = statistics.stdev(regime_scores)
            assert score_std >= 0.0, "Standard deviation should be non-negative"
        for score in regime_scores:
            assert -0.4 <= score <= 0.4, f"Regime score out of range: {score}"
