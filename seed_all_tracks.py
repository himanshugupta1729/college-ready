#!/usr/bin/env python3
"""
seed_all_tracks.py — Seeds ALL question banks for every track in the College Ready app.

Idempotent: each track seed deletes existing questions for that track before inserting,
so running this multiple times is safe and won't create duplicates.

Usage:
    python3 seed_all_tracks.py
"""

import subprocess
import sys
import os
import sqlite3

DB_PATH = os.environ.get('DATABASE_PATH', 'college_ready.db')
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# All seed scripts in order
SEED_SCRIPTS = [
    'seed_questions.py',        # SAT (38 questions)
    'seed_sat_supplement.py',   # SAT supplement (+8 = 46 total)
    'seed_ap_precalc.py',       # AP Precalculus (72)
    'seed_ap_calc_ab.py',       # AP Calculus AB (84)
    'seed_ap_calc_bc.py',       # AP Calculus BC (90)
    'seed_ap_stats.py',         # AP Statistics (84)
    'seed_algebra1.py',         # Algebra 1 (75)
    'seed_geometry.py',         # Geometry (75)
    'seed_algebra2.py',         # Algebra 2 (84)
    'seed_precalculus.py',      # Precalculus (84)
    'seed_statistics.py',       # Statistics (66)
    'seed_grade6.py',           # Grade 6 (24)
    'seed_grade7.py',           # Grade 7 (24)
    'seed_grade7_accel.py',     # Grade 7 Accelerated (24)
    'seed_grade8.py',           # Grade 8 (24)
]

# Minimum questions needed per track (from TRACK_CONFIG)
MINIMUMS = {
    'sat': 44,
    'ap_precalc': 24,
    'ap_calc_ab': 28,
    'ap_calc_bc': 30,
    'ap_stats': 28,
    'algebra_1': 25,
    'geometry': 25,
    'algebra_2': 28,
    'precalculus': 28,
    'statistics': 22,
    'grade_6': 24,
    'grade_7': 24,
    'grade_7_accelerated': 24,
    'grade_8': 24,
}


def main():
    print("=" * 60)
    print("College Ready — Seeding ALL question banks")
    print("=" * 60)

    os.chdir(SCRIPT_DIR)

    # Run each seed script
    for script in SEED_SCRIPTS:
        script_path = os.path.join(SCRIPT_DIR, script)
        if not os.path.exists(script_path):
            print(f"\n  SKIP: {script} (file not found)")
            continue

        print(f"\n--- Running {script} ---")
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"  ERROR: {result.stderr}")
        else:
            # Print just the summary lines
            lines = result.stdout.strip().split('\n')
            for line in lines[-3:]:
                print(f"  {line}")

    # Verify all tracks
    print("\n" + "=" * 60)
    print("VERIFICATION — Question counts vs minimums")
    print("=" * 60)

    conn = sqlite3.connect(DB_PATH)
    all_ok = True
    for track, minimum in sorted(MINIMUMS.items()):
        count = conn.execute(
            "SELECT COUNT(*) FROM questions WHERE track = ?", (track,)
        ).fetchone()[0]
        status = "OK" if count >= minimum else "INSUFFICIENT"
        if status != "OK":
            all_ok = False
        print(f"  {track:25s}: {count:4d} questions (need {minimum:3d}) — {status}")

    conn.close()

    if all_ok:
        print("\nAll tracks have sufficient questions.")
    else:
        print("\nWARNING: Some tracks need more questions!")
        sys.exit(1)


if __name__ == "__main__":
    main()
