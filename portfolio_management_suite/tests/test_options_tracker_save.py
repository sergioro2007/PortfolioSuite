import os
import pickle
import shutil
from portfolio_suite.options_trading.core import OptionsTracker

def test_save_trades_creates_data_dir_and_file(tmp_path):
    # Setup: ensure clean temp dir
    data_dir = tmp_path / "data"
    trades_file = data_dir / "options_trades.pkl"
    if data_dir.exists():
        shutil.rmtree(data_dir)
    # Patch tracker to use temp path
    tracker = OptionsTracker()
    tracker.trades_file = str(trades_file)
    tracker.trades = [{"test": "trade"}]
    tracker.save_trades()
    assert trades_file.exists(), "options_trades.pkl was not created!"
    # Check contents
    with open(trades_file, "rb") as f:
        trades = pickle.load(f)
    assert trades == [{"test": "trade"}], f"Unexpected trades: {trades}"
