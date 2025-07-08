#!/bin/bash
cd "$(dirname "$0")"
source .venv/bin/activate
python -m portfolio_suite.trade_analysis.cli "$@"
