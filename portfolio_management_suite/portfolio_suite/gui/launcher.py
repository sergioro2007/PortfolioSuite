"""
GUI Launcher for Portfolio Management Suite
==========================================

Cross-platform desktop launcher that provides:
- Menu bar/system tray integration
- Background Streamlit server management
- Browser launch and management
- Graceful shutdown handling
"""

import sys
import os
import subprocess
import threading
import time
import webbrowser
import signal
from typing import Optional

# Platform-specific imports
try:
    if sys.platform == "darwin":  # macOS
        import rumps
        HAS_RUMPS = True
    else:
        HAS_RUMPS = False
except ImportError:
    HAS_RUMPS = False

try:
    import pystray
    from PIL import Image
    HAS_PYSTRAY = True
except ImportError:
    HAS_PYSTRAY = False

class PortfolioSuiteLauncher:
    """Main launcher class for Portfolio Management Suite"""
    
    def __init__(self):
        self.streamlit_process: Optional[subprocess.Popen] = None
        self.server_port = 8501
        self.server_url = f"http://localhost:{self.server_port}"
        self.is_running = False
        
    def start_streamlit_server(self):
        """Start the Streamlit server in the background"""
        try:
            # Find the main app module
            app_module = "portfolio_suite.ui.main_app"
            
            # Start Streamlit server
            cmd = [
                sys.executable, "-m", "streamlit", "run",
                "--server.port", str(self.server_port),
                "--server.address", "localhost",
                "--server.headless", "true",
                "--browser.gatherUsageStats", "false",
                "-m", app_module
            ]
            
            self.streamlit_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE
            )
            
            # Wait for server to start
            self._wait_for_server()
            self.is_running = True
            
        except Exception as e:
            print(f"Failed to start Streamlit server: {e}")
            return False
        
        return True
    
    def _wait_for_server(self, timeout=30):
        """Wait for the Streamlit server to be ready"""
        import urllib.request
        import urllib.error
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                urllib.request.urlopen(self.server_url, timeout=1)
                return True
            except (urllib.error.URLError, OSError):
                time.sleep(0.5)
        
        raise TimeoutError("Streamlit server failed to start within timeout")
    
    def open_browser(self):
        """Open the web interface in the default browser"""
        if self.is_running:
            webbrowser.open(self.server_url)
    
    def stop_server(self):
        """Stop the Streamlit server"""
        if self.streamlit_process:
            self.streamlit_process.terminate()
            try:
                self.streamlit_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.streamlit_process.kill()
            self.streamlit_process = None
        self.is_running = False
    
    def restart_server(self):
        """Restart the Streamlit server"""
        self.stop_server()
        time.sleep(1)
        self.start_streamlit_server()


class MacOSLauncher(PortfolioSuiteLauncher):
    """macOS-specific launcher using rumps for menu bar integration"""
    
    def __init__(self):
        super().__init__()
        if not HAS_RUMPS:
            raise ImportError("rumps not available for macOS menu bar integration")
        
        self.app = rumps.App("📊 Portfolio Suite", "📊")
        self.setup_menu()
    
    def setup_menu(self):
        """Setup the macOS menu bar menu"""
        self.app.menu = [
            "Launch Dashboard",
            "Options Trading",
            "Tactical Tracker", 
            "Trade Analysis",
            None,  # Separator
            "Restart Server",
            None,  # Separator
            "About",
        ]
        
        # Bind menu actions
        self.app.menu["Launch Dashboard"].set_callback(self.launch_dashboard)
        self.app.menu["Options Trading"].set_callback(self.launch_options)
        self.app.menu["Tactical Tracker"].set_callback(self.launch_tactical)
        self.app.menu["Trade Analysis"].set_callback(self.launch_analysis)
        self.app.menu["Restart Server"].set_callback(self.restart_server)
        self.app.menu["About"].set_callback(self.show_about)
    
    def launch_dashboard(self, _):
        """Launch main dashboard"""
        if not self.is_running:
            self.start_streamlit_server()
        self.open_browser()
    
    def launch_options(self, _):
        """Launch options trading module"""
        if not self.is_running:
            self.start_streamlit_server()
        webbrowser.open(f"{self.server_url}?module=options")
    
    def launch_tactical(self, _):
        """Launch tactical tracker module"""
        if not self.is_running:
            self.start_streamlit_server()
        webbrowser.open(f"{self.server_url}?module=tactical")
    
    def launch_analysis(self, _):
        """Launch trade analysis module"""
        if not self.is_running:
            self.start_streamlit_server()
        webbrowser.open(f"{self.server_url}?module=analysis")
    
    def restart_server(self, _):
        """Restart the server"""
        super().restart_server()
        rumps.notification("Portfolio Suite", "Server Restarted", "The application server has been restarted.")
    
    def show_about(self, _):
        """Show about dialog"""
        rumps.alert(
            title="Portfolio Management Suite",
            message="Version 2.0.0\n\nComprehensive investment analysis platform with portfolio management tools.",
            ok="OK"
        )
    
    def run(self):
        """Run the macOS application"""
        # Start server in background
        threading.Thread(target=self.start_streamlit_server, daemon=True).start()
        
        # Setup cleanup on exit
        def cleanup(signum, frame):
            self.stop_server()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, cleanup)
        signal.signal(signal.SIGTERM, cleanup)
        
        # Run the app
        self.app.run()


class CrossPlatformLauncher(PortfolioSuiteLauncher):
    """Cross-platform launcher using pystray for system tray integration"""
    
    def __init__(self):
        super().__init__()
        if not HAS_PYSTRAY:
            raise ImportError("pystray not available for system tray integration")
        
        # Create a simple icon (you can replace with actual icon file)
        image = Image.new('RGB', (64, 64), color='blue')
        
        menu = pystray.Menu(
            pystray.MenuItem("Launch Dashboard", self.launch_dashboard),
            pystray.MenuItem("Options Trading", self.launch_options),
            pystray.MenuItem("Tactical Tracker", self.launch_tactical),
            pystray.MenuItem("Trade Analysis", self.launch_analysis),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Restart Server", self.restart_server),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit", self.quit_app)
        )
        
        self.icon = pystray.Icon("portfolio_suite", image, "Portfolio Suite", menu)
    
    def launch_dashboard(self):
        """Launch main dashboard"""
        if not self.is_running:
            self.start_streamlit_server()
        self.open_browser()
    
    def launch_options(self):
        """Launch options trading module"""
        if not self.is_running:
            self.start_streamlit_server()
        webbrowser.open(f"{self.server_url}?module=options")
    
    def launch_tactical(self):
        """Launch tactical tracker module"""
        if not self.is_running:
            self.start_streamlit_server()
        webbrowser.open(f"{self.server_url}?module=tactical")
    
    def launch_analysis(self):
        """Launch trade analysis module"""
        if not self.is_running:
            self.start_streamlit_server()
        webbrowser.open(f"{self.server_url}?module=analysis")
    
    def restart_server(self):
        """Restart the server"""
        super().restart_server()
    
    def quit_app(self):
        """Quit the application"""
        self.stop_server()
        self.icon.stop()
    
    def run(self):
        """Run the cross-platform application"""
        # Start server in background
        threading.Thread(target=self.start_streamlit_server, daemon=True).start()
        
        # Run the system tray app
        self.icon.run()


def launch_gui():
    """Launch the appropriate GUI for the current platform"""
    try:
        if sys.platform == "darwin" and HAS_RUMPS:
            # Use macOS menu bar integration
            launcher = MacOSLauncher()
        elif HAS_PYSTRAY:
            # Use cross-platform system tray
            launcher = CrossPlatformLauncher()
        else:
            # Fallback to simple launcher
            launcher = PortfolioSuiteLauncher()
            launcher.start_streamlit_server()
            launcher.open_browser()
            
            # Keep running
            try:
                while launcher.is_running:
                    time.sleep(1)
            except KeyboardInterrupt:
                launcher.stop_server()
            return
        
        launcher.run()
        
    except Exception as e:
        print(f"Failed to launch GUI: {e}")
        print("Falling back to web interface...")
        
        # Fallback to simple web launch
        launcher = PortfolioSuiteLauncher()
        launcher.start_streamlit_server()
        launcher.open_browser()
        
        try:
            while launcher.is_running:
                time.sleep(1)
        except KeyboardInterrupt:
            launcher.stop_server()


if __name__ == "__main__":
    launch_gui()
