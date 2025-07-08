#!/bin/bash
cd "$(dirname "$0")"
source .venv/bin/activate
streamlit run portfolio_suite/ui/main_app.py
