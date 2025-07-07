#!/usr/bin/env python3
"""Setup script for Portfolio Management Suite"""

from setuptools import setup, find_packages
import os

# Read requirements from requirements.txt
def read_requirements():
    """Read requirements from requirements.txt file"""
    req_file = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(req_file):
        with open(req_file, 'r') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

# Read long description from README
def read_long_description():
    """Read long description from README.md"""
    readme_file = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_file):
        with open(readme_file, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

setup(
    name="portfolio-management-suite",
    version="2.0.0",
    author="Portfolio Manager",
    author_email="manager@example.com",
    description="Comprehensive investment analysis platform with portfolio management tools",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/portfolio-management-suite",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.900",
        ],
        "gui": [
            "rumps>=0.3.0; sys_platform == 'darwin'",
            "pystray>=0.19.0; sys_platform != 'darwin'",
        ]
    },
    entry_points={
        "console_scripts": [
            "portfolio-suite=portfolio_suite.__main__:main",
            "portfolio-suite-web=portfolio_suite.__main__:main",
            "portfolio-options=portfolio_suite.options_trading.cli:main",
            "portfolio-tactical=portfolio_suite.tactical_tracker.cli:main",
            "portfolio-analysis=portfolio_suite.trade_analysis.cli:main",
        ],
        "gui_scripts": [
            "Portfolio Suite=portfolio_suite.__main__:main",
        ]
    },
    include_package_data=True,
    package_data={
        "portfolio_suite": [
            "data/*.csv",
            "data/*.json",
            "ui/assets/*",
            "gui/assets/*",
        ]
    },
    zip_safe=False,
)
