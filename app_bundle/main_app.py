import sys
import os
import threading
import time
import uvicorn

# ---- PATH FIX ----
if hasattr(sys, "_MEIPASS"):
    sys.path.append(sys._MEIPASS)
else:
    sys.path.append(os.path.dirname(__file__))

from backend.app.main import app
from jarvis.jarvis_core import start_jarvis


def run_backend():
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="warning"
    )


if __name__ == "__main__":
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()

    time.sleep(2)
    start_jarvis()
