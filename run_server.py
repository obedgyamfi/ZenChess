# run_server.py
import os
import sys
import uvicorn
from pathlib import Path

# --- Ensure project root is in sys.path ---
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# --- Set working directory to project root ---
os.chdir(BASE_DIR)

# --- Run server ---
if __name__ == "__main__":
    uvicorn.run(
        "backend.api.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
