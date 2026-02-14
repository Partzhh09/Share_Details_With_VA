"""
Launcher for IPO Predict with VA.
Sets up paths so backend and jarvis are found, then starts backend in a thread and runs the voice assistant.
Used as the entry point for the built .exe.
"""
"""

import sys
import os
import threading
import time

def _setup_paths():
    if getattr(sys, "frozen", False):
        base = sys._MEIPASS
        sys.path.insert(0, base)
        sys.path.insert(0, os.path.join(base, "app_bundle"))
    else:
        root = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, root)
        sys.path.insert(0, os.path.join(root, "app_bundle"))

_setup_paths()

import uvicorn
from backend.app.main import app
from jarvis.jarvis_core import start_jarvis


def run_backend():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")


if __name__ == "__main__":
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    time.sleep(2)
    start_jarvis()
"""
