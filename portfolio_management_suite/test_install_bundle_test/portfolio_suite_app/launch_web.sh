#!/bin/bash
cd "$(dirname "$0")"
source .venv/bin/activate
main_app_path=$(python -c 'import sys; import portfolio_suite.ui.main_app; sys.stdout.write(portfolio_suite.ui.main_app.__file__)')
streamlit run "$main_app_path"
