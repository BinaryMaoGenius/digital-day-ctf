#!/usr/bin/env python3
"""Debug wrapper to capture startup errors with full traceback."""
import sys
import os
import logging
import traceback

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(name)s: %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr),
        logging.FileHandler('server_debug.log', mode='w', encoding='utf-8')
    ],
    force=True
)

print("=== Debug wrapper started ===", flush=True)

try:
    print("Step 1: importing handlers...", flush=True)
    from handlers import update_db, start_server
    print("Step 2: update_db...", flush=True)
    update_db()
    print("Step 3: start_server...", flush=True)
    start_server()
except SystemExit as e:
    print(f"SystemExit: {e}", flush=True)
    traceback.print_exc()
except Exception as e:
    print(f"EXCEPTION: {type(e).__name__}: {e}", flush=True)
    traceback.print_exc()
finally:
    print("=== Debug wrapper ended ===", flush=True)
