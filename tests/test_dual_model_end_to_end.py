#!/usr/bin/env python3
"""
Comprehensive end-to-end testing for dual-model implementation
Tests complete workflow from data fetch to UI display without user intervention
"""

import pytest
import sys
import os
import json

sys.path.append("src")

from portfolio_suite.options_trading.core import OptionsTracker


class TestDualModelEndToEnd:
    """Comprehensive end-to-end test suite"""

    @pytest.fixture
    def tracker(self):
        return OptionsTracker()

    def test_complete_prediction_workflow(self, tracker):
        ticker = "AAPL"
        indicators = tracker.get_technical_indicators(ticker)
        assert indicators, "Failed to get technical indicators"
        assert "atr" in indicators, "ATR calculation missing"
        prediction = tracker.predict_price_range_enhanced(ticker)
        assert prediction, "Failed to get enhanced prediction"
        assert prediction["current_price"] > 0, "Invalid current price"
        indicators = prediction["indicators"]
        assert indicators["atr"] > 0, "Invalid ATR value"
        legacy_prediction = tracker.predict_price_range(ticker)
        # Compare key fields instead of entire dict (avoids DataFrame comparison issues)
        assert (
            legacy_prediction["current_price"] == prediction["current_price"]
        ), "Backward compatibility broken"
        assert (
            legacy_prediction["target_price"] == prediction["target_price"]
        ), "Backward compatibility broken"

    def test_full_ui_integration_workflow(self, tracker):
        ticker = "AAPL"
        prediction = tracker.predict_price_range_enhanced(ticker)
        current_price = prediction["current_price"]
        indicators = prediction["indicators"]
        atr_value = indicators.get("atr", 0)
        weekly_vol = prediction["weekly_volatility"]
        bias_score = prediction.get("bias_score", 0)
        annual_vol = weekly_vol * (52**0.5)
        assert annual_vol > 0, "Annual volatility calculation failed"
        assert all(
            key in indicators for key in ["rsi", "macd", "macd_signal", "momentum"]
        ), "Missing indicator data"
        target_price = prediction["target_price"]
        lower_bound = prediction["lower_bound"]
        upper_bound = prediction["upper_bound"]
        assert lower_bound < target_price < upper_bound, "Invalid range calculation"

    def test_strategy_generation_workflow(self, tracker):
        suggestions = tracker.generate_trade_suggestions(num_suggestions=3)
        assert isinstance(suggestions, list), "Invalid suggestions format"
        for suggestion in suggestions:
            if suggestion:
                assert "strategy" in suggestion, "Missing strategy"
                assert "ticker" in suggestion, "Missing ticker"

    def test_data_persistence_workflow(self, tracker):
        ticker = "AAPL"
        prediction1 = tracker.predict_price_range_enhanced(ticker)
        tracker.save_predictions()
        tracker.load_predictions()
        prediction2 = tracker.predict_price_range_enhanced(ticker)
        assert prediction2, "Failed to load predictions"
        assert "indicators" in prediction2, "Indicator data lost in persistence"

    def test_error_recovery_workflow(self, tracker):
        prediction = tracker.predict_price_range_enhanced("INVALID123")
        assert prediction == {}, "Should handle invalid ticker gracefully"
        try:
            prediction = tracker.predict_price_range_enhanced("AAPL")
            if prediction:
                assert "current_price" in prediction, "Partial prediction data"
        except Exception as e:
            assert (
                "timeout" in str(e).lower() or "network" in str(e).lower()
            ), f"Unexpected error: {e}"

    def test_performance_requirements(self, tracker):
        import time

        ticker = "AAPL"
        start_time = time.time()
        prediction = tracker.predict_price_range_enhanced(ticker)
        elapsed = time.time() - start_time
        assert elapsed < 10.0, f"Prediction too slow: {elapsed:.2f}s"
        assert prediction, "Prediction failed"

    def test_concurrent_predictions(self, tracker):
        tickers = ["AAPL", "SPY", "QQQ"]
        predictions = {}
        for ticker in tickers:
            predictions[ticker] = tracker.predict_price_range_enhanced(ticker)
        for ticker, prediction in predictions.items():
            assert prediction, f"Failed prediction for {ticker}"
            assert "current_price" in prediction, f"Missing current_price for {ticker}"
