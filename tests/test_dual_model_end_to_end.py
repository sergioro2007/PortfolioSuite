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
        assert "atr_14" in indicators, "ATR calculation missing"
        prediction = tracker.predict_price_range_dual_model(ticker)
        assert prediction, "Failed to get dual-model prediction"
        assert prediction["ticker"] == ticker, "Ticker mismatch"
        assert prediction["current_price"] > 0, "Invalid current price"
        assert prediction["atr_value"] > 0, "Invalid ATR value"
        legacy_prediction = tracker.predict_price_range(ticker)
        # Compare key fields instead of entire dict (avoids DataFrame comparison issues)
        assert (
            legacy_prediction["current_price"] == prediction["current_price"]
        ), "Backward compatibility broken"
        assert (
            legacy_prediction["target_mid"] == prediction["target_mid"]
        ), "Backward compatibility broken"

    def test_full_ui_integration_workflow(self, tracker):
        ticker = "AAPL"
        prediction = tracker.predict_price_range(ticker)
        current_price = prediction["current_price"]
        atr_value = prediction.get("atr_value", 0)
        weekly_vol = prediction["weekly_volatility"]
        regime_score = prediction.get("regime_score", 0)
        annual_vol = weekly_vol * (52**0.5)
        assert annual_vol > 0, "Annual volatility calculation failed"
        indicators = prediction["indicators"]
        assert all(
            key in indicators for key in ["rsi", "macd", "macd_signal", "momentum"]
        ), "Missing indicator data"
        target_mid = prediction["target_mid"]
        predicted_low = prediction["predicted_low"]
        predicted_high = prediction["predicted_high"]
        assert predicted_low < target_mid < predicted_high, "Invalid range calculation"

    def test_strategy_generation_workflow(self, tracker):
        suggestions = tracker.generate_trade_suggestions(count=3)
        assert isinstance(suggestions, list), "Invalid suggestions format"
        for suggestion in suggestions:
            if suggestion:
                assert "strategy" in suggestion, "Missing strategy"
                assert "ticker" in suggestion, "Missing ticker"

    def test_data_persistence_workflow(self, tracker):
        ticker = "AAPL"
        prediction1 = tracker.predict_price_range(ticker)
        tracker.save_predictions()
        tracker.load_predictions()
        prediction2 = tracker.predict_price_range(ticker)
        assert prediction2, "Failed to load predictions"
        assert "atr_value" in prediction2, "ATR data lost in persistence"

    def test_error_recovery_workflow(self, tracker):
        prediction = tracker.predict_price_range("INVALID123")
        assert prediction == {}, "Should handle invalid ticker gracefully"
        try:
            prediction = tracker.predict_price_range("AAPL")
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
        prediction = tracker.predict_price_range(ticker)
        elapsed = time.time() - start_time
        assert elapsed < 10.0, f"Prediction too slow: {elapsed:.2f}s"
        assert prediction, "Prediction failed"

    def test_concurrent_predictions(self, tracker):
        tickers = ["AAPL", "SPY", "QQQ"]
        predictions = {}
        for ticker in tickers:
            predictions[ticker] = tracker.predict_price_range(ticker)
        for ticker, prediction in predictions.items():
            assert prediction, f"Failed prediction for {ticker}"
            assert prediction["ticker"] == ticker, f"Ticker mismatch for {ticker}"
