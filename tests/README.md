# Test Organization

This directory contains the Portfolio Suite test framework, organized for clarity and maintainability.

## Directory Structure

### `/tests/` (Main Test Suite)

- `test_*.py` - Core functional tests that run as part of the main test suite
- These tests validate the core functionality and ensure system reliability

### `/tests/analysis/` (Analysis & Research)

Files used for algorithmic analysis, comparison studies, and research:

- `analyze_range_differences.py` - Range prediction analysis
- `chatgpt_atr_verification.py` - ChatGPT algorithm verification
- `compare_*.py` - Algorithm comparison studies
- `comprehensive_atr_analysis.py` - ATR analysis
- `final_*.py` - Analysis summaries
- `investigate_*.py` - Investigation scripts
- `simple_atr_analysis.py` - Simple ATR analysis

### `/tests/debug/` (Debug & Quick Tests)

Debugging utilities and quick test scripts:

- `debug_*.py` - Debugging utilities
- `quick_test*.py` - Quick validation scripts

### `/tests/verification/` (Algorithm Verification)

Scripts that verify specific algorithms and specifications:

- `verify_algorithm.py` - Main algorithm verification
- `verify_atr_specification.py` - ATR specification verification
- `verify_chatgpt_formula.py` - ChatGPT formula verification

## Running Tests

### Main Test Suite

```bash
# Run all core tests
./.venv/bin/python -m pytest tests/ --tb=short

# Run specific test categories
./.venv/bin/python -m pytest tests/test_dual_model*.py
./.venv/bin/python -m pytest tests/test_options*.py
```

### Analysis Scripts

```bash
# Run analysis scripts individually
cd tests/analysis
./.venv/bin/python analyze_range_differences.py
```

### Debug Scripts

```bash
# Run debug scripts individually
cd tests/debug
./.venv/bin/python debug_predictions.py
```

### Verification Scripts

```bash
# Run verification scripts individually
cd tests/verification
./.venv/bin/python verify_algorithm.py
```

## Test Coverage

See `TEST_COVERAGE_SUMMARY.md` for comprehensive test coverage details.

## Adding New Tests

1. **Core functionality tests**: Add to `/tests/test_*.py`
2. **Analysis scripts**: Add to `/tests/analysis/`
3. **Debug utilities**: Add to `/tests/debug/`
4. **Algorithm verification**: Add to `/tests/verification/`

All new tests should follow the existing naming conventions and include proper documentation.
