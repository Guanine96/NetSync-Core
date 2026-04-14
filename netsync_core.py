"""
NetSync Core v1.0.0
Author: Petar Pekovic (Guanine96)
Description: Automated Infrastructure Recovery & Data Synchronization Engine.
Handles Wi-Fi protocol resets, VPN tunneling, and UI-based RPA synchronization.
"""

import os
import sys
import time
import subprocess
import logging
import json
import threading
import socket
import ctypes
import tkinter as tk
from tkinter import scrolledtext

# Automation Libraries
import psutil
import pyautogui
from pywinauto import Desktop

class NetSyncEngine:
    """Core logic for network recovery and application automation."""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger("NetSyncEngine")

    def check_internet(self) -> bool:
        """Standard socket-based connectivity check."""
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except (socket.timeout, OSError):
            return False

    def recover_wifi_connection(self) -> bool:
        """ 
        Aggressive Wi-Fi recovery protocol.
        Uses PowerShell for adapter reset and PyAutoGUI for OS-level interaction.
        """
        self.logger.info("Initiating hardware-level network recovery...")
        
        # Step 1: PowerShell Adapter Reset
        ps_cmd = "Get-NetAdapter -InterfaceDescription *Wireless* | Enable-NetAdapter -Confirm:$false"
        subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-Command", ps_cmd], 
                       shell=True, capture_output=True)
        
        time.sleep(3)
        if self.check_internet(): return True

        # Step 2: OS Quick Settings Simulation (Win+A)
        try:
            pyautogui.hotkey('win', 'a')
            time.sleep(1.5)
            pyautogui.press('tab')
            pyautogui.press('space')
            time.sleep(0.5)
            pyautogui.press('esc')
            
            self.logger.info("Virtual Wi-Fi switch toggled. Waiting for DHCP lease...")
            time.sleep(15)
        except Exception as e:
            self.logger.error(f"UI Simulation failed: {e}")

        return self.check_internet()

    def run_sync_sequence(self, vpn_path, vpn_id, app_path):
        """Main RPA sequence: Recover Net -> Start VPN -> Launch App -> Trigger Sync."""
        try:
            if not self.check_internet():
                if not self.recover_wifi_connection():
                    self.logger.error("Critical Failure: Connectivity could not be restored.")
                    return

            self.logger.info("Connectivity stable. Starting VPN tunnel...")
            
            # 1. Start VPN Tunnel
            subprocess.Popen([vpn_path, f"--connect-shortcut={vpn_id}"], shell=False)
            time.sleep(30) # Time for handshake and IP assignment

            # 2. Launch Target Application
            self.logger.info("Launching synchronization target...")
            os.startfile(app_path)
            time.sleep(20)

            # 3. RPA: Automated Click for Data Replication
            desktop = Desktop(backend="uia")
            # Using Regex to find any window containing 'Replication'
            app_window = desktop.window(title_re=".*Replication.*")
            
            if app_window.exists(timeout=20):
                app_window.set_focus()
                rect = app_window.rectangle()
                # Relative offsets from config
                pyautogui.click(rect.left + 40, rect.top + 90)
                self.logger.info("Synchronization signal sent successfully.")
            else:
                self.logger.error("Target UI not detected.")

        except Exception as e:
            self.logger.error(f"Execution Error: {str(e)}")

# --- UI HANDLER FOR LOGGING ---
class TextHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget
    def emit(self, record):
        msg = self.format(record)
        self.text_widget.after(0, lambda: self._append(msg))
    def _append(self, msg):
        self.text_widget.configure(state='normal')
        self.text_widget.insert(tk.END, msg + '\n')
        self.text_widget.configure(state='disabled')
        self.text_widget.yview(tk.END)

# --- MAIN APP INTERFACE ---
class NetSyncApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NetSync Enterprise v1.0")
        self.root.geometry("600x400")
        self.root.configure(bg="#121212") # Dark aesthetic
        
        self.setup_ui()
        self.engine = NetSyncEngine(config={})

    def setup_ui(self):
        tk.Label(self.root, text="NETSYNC CORE", font=("Arial", 18, "bold"), fg="#00ffcc", bg="#121212").pack(pady=10)
        self.log_area = scrolledtext.ScrolledText(self.root, bg="#1e1e1e", fg="#ffffff", font=("Consolas", 10))
        self.log_area.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Integrate Logging
        handler = TextHandler(self.log_area)
        logging.basicConfig(level=logging.INFO, handlers=[handler])

    def start(self):
        # In production, paths would come from a secure config file
        threading.Thread(target=self.engine.run_sync_sequence, 
                         args=("path/to/vpn.exe", "12345", "path/to/app.exe"), 
                         daemon=True).start()

if __name__ == "__main__":
    # Check for Admin privileges (required for network adapter control)
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("Admin privileges required. Restarting...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    else:
        root = tk.Tk()
        app = NetSyncApp(root)
        root.mainloop()
