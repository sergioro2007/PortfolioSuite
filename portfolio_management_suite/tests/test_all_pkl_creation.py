import os
import pickle
import shutil
from portfolio_suite.options_trading.core import OptionsTracker
from portfolio_suite.tactical_tracker.core import PortfolioTracker

def test_options_trades_pkl_creation(tmp_path):
    data_dir = tmp_path / "data"
    trades_file = data_dir / "options_trades.pkl"
    tracker = OptionsTracker()
    tracker.trades_file = str(trades_file)
    tracker.trades = [{"test": "trade"}]
    tracker.save_trades()
    assert trades_file.exists(), "options_trades.pkl was not created!"
    with open(trades_file, "rb") as f:
        trades = pickle.load(f)
    assert trades == [{"test": "trade"}]

def test_edit_trade(tmp_path):
    data_dir = tmp_path / "data"
    trades_file = data_dir / "options_trades.pkl"
    tracker = OptionsTracker()
    tracker.trades_file = str(trades_file)
    tracker.trades = [{"id": 1, "symbol": "AAPL", "qty": 10}]
    tracker.save_trades()
    tracker.edit_trade(1, {"qty": 20})
    tracker.save_trades()
    with open(trades_file, "rb") as f:
        trades = pickle.load(f)
    assert trades[0]["qty"] == 20

def test_delete_trade(tmp_path):
    data_dir = tmp_path / "data"
    trades_file = data_dir / "options_trades.pkl"
    tracker = OptionsTracker()
    tracker.trades_file = str(trades_file)
    tracker.trades = [
        {"id": 1, "symbol": "AAPL", "qty": 10},
        {"id": 2, "symbol": "MSFT", "qty": 5}
    ]
    tracker.save_trades()
    tracker.delete_trade(1)
    tracker.save_trades()
    with open(trades_file, "rb") as f:
        trades = pickle.load(f)
    assert len(trades) == 1
    assert trades[0]["id"] == 2

def test_predictions_pkl_creation(tmp_path):
    predictions_file = tmp_path / "price_predictions.pkl"
    tracker = OptionsTracker()
    tracker.predictions_file = str(predictions_file)
    tracker.predictions = {"AAPL": 123}
    tracker.save_predictions()
    assert predictions_file.exists(), "price_predictions.pkl was not created!"
    with open(predictions_file, "rb") as f:
        preds = pickle.load(f)
    assert preds == {"AAPL": 123}

def test_portfolio_results_pkl_creation(tmp_path):
    data_dir = tmp_path / "data"
    results_file = data_dir / "portfolio_results.pkl"
    if data_dir.exists():
        shutil.rmtree(data_dir)
    tracker = PortfolioTracker()
    tracker.results_file = str(results_file)
    tracker.save_results([{"test": "result"}])
    assert results_file.exists(), "portfolio_results.pkl was not created!"
    with open(results_file, "rb") as f:
        results = pickle.load(f)
    assert any(r.get("results") == [{"test": "result"}] for r in results), f"Unexpected results: {results}"
