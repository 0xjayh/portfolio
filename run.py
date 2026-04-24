#!/usr/bin/env python3
"""
Local development server.

First time setup:
    python3 -m venv venv
    source venv/bin/activate        # Mac/Linux
    venv\Scripts\activate           # Windows
    pip install -r requirements.txt
    cp api/.env.example api/.env    # then fill in your DB credentials

Every time after:
    source venv/bin/activate
    python run.py
"""

import sys
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
API_DIR  = os.path.join(ROOT_DIR, "api")

# Add api/ to path so app.py and db.py can find each other
sys.path.insert(0, API_DIR)

# ── Pre-flight checks ──────────────────────────────────────────
env_file = os.path.join(API_DIR, ".env")
if not os.path.exists(env_file):
    print("\n  [ERROR] api/.env not found.")
    print("  Run:  cp api/.env.example api/.env")
    print("  Then fill in your DB_HOST, DB_USER, DB_PASSWORD, DB_NAME.\n")
    sys.exit(1)

try:
    from app import app
except ModuleNotFoundError as e:
    print(f"\n  [ERROR] Missing module: {e}")
    print("  Make sure your venv is active and run:  pip install -r requirements.txt\n")
    sys.exit(1)

# ── Start server ───────────────────────────────────────────────
if __name__ == "__main__":
    print("\n  Portfolio  ->  http://localhost:5000")
    print("  Admin      ->  http://localhost:5000/admin")
    print("  API        ->  http://localhost:5000/api/health")
    print("\n  NOTE: API routes need MySQL running.")
    print("  The portfolio UI will load regardless.\n")
    print("  Ctrl+C to stop\n")
    app.run(debug=True, port=5000, host="127.0.0.1")
