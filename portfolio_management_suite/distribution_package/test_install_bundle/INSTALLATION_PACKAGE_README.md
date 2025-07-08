dist/

# Portfolio Management Suite Installation Guide

## Quick Start (Recommended)

1. **Obtain the Install Bundle**
   - Download or copy the file: `portfolio_management_suite_install_bundle.zip` (found in the `distribution_package/` folder).

2. **Extract the Bundle**
   - Unzip the bundle on your target machine:
     ```sh
     unzip portfolio_management_suite_install_bundle.zip
     cd portfolio_management_suite_install_bundle
     ```

3. **Run the One-Click Installer**
   - Execute the install script (it will set up a virtual environment, install the package, and create launcher scripts):
     ```sh
     bash quick_install.sh
     ```

4. **Launch the Application**
   - Use the generated launcher scripts:
     - `launch_web.sh` — Launches the main Streamlit web app.
     - `launch_gui.sh` — (If available) Launches the GUI app.
     - `analyze.sh` — (If available) Runs the analysis tool.

---

## Details & Troubleshooting

- The installer will use the `.whl` file for fastest install if present, or fall back to the `.tar.gz` source package.
- All dependencies are installed from the public PyPI index.
- The install process is self-contained and does not affect your system Python or other environments.
- If you need to reinstall, simply delete the extracted folder and repeat the steps above.

---

## Advanced: Manual Installation

If you only have the `.tar.gz` or `.whl` file:

1. Create and activate a Python virtual environment:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install the package:
   ```sh
   pip install portfolio_management_suite-*.whl
   # or, if only the .tar.gz is present:
   pip install portfolio_management_suite-*.tar.gz
   ```
3. Run the app:
   ```sh
   streamlit run portfolio_suite/ui/main_app.py
   ```

---

## Packaging Notes

- The install bundle includes:
  - The latest `.whl` and/or `.tar.gz` package
  - `quick_install.sh` (the one-click installer)
  - This README
- For best results, always distribute the full install bundle zip.
- For packaging best practices, ensure your package includes a `README.md`, `LICENSE`, and correct license metadata in `pyproject.toml`.
