#!/usr/bin/env python3
"""Upload exported solutions to Render. Run after export_solutions.py."""
import json, requests, sys

RENDER_URL = "https://college-ready.onrender.com"
EXPORT_FILE = "solutions_export.json"

# Get the secret key from Render env (or pass as arg)
if len(sys.argv) < 2:
    print("Usage: python3 upload_solutions.py <SECRET_KEY>")
    print("Find SECRET_KEY in Render Dashboard → Environment → SECRET_KEY")
    sys.exit(1)

secret_key = sys.argv[1]

with open(EXPORT_FILE) as f:
    solutions = json.load(f)

print(f"Uploading {len(solutions)} solutions to {RENDER_URL}...")

# Upload in batches of 100
batch_size = 100
total_imported = 0

for i in range(0, len(solutions), batch_size):
    batch = solutions[i:i + batch_size]
    resp = requests.post(
        f"{RENDER_URL}/api/import-solutions",
        json={"api_key": secret_key, "solutions": batch},
        timeout=30
    )
    if resp.status_code == 200:
        result = resp.json()
        total_imported += result.get('imported', 0)
        print(f"  Batch {i//batch_size + 1}: {result.get('imported', 0)} imported")
    else:
        print(f"  Batch {i//batch_size + 1} FAILED: {resp.status_code} {resp.text}")

print(f"\nDone. {total_imported} solutions imported to Render.")
