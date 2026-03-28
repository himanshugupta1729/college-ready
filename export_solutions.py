#!/usr/bin/env python3
"""Export worked solutions from local DB as JSON for upload to Render."""
import os, json, sqlite3

DB_PATH = os.environ.get('DATABASE_PATH', 'college_ready.db')
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row

rows = conn.execute("""
    SELECT id, worked_solution_json, wrong_answer_analyses
    FROM questions
    WHERE worked_solution_json IS NOT NULL
""").fetchall()

data = []
for r in rows:
    data.append({
        'id': r['id'],
        'worked_solution_json': r['worked_solution_json'],
        'wrong_answer_analyses': r['wrong_answer_analyses'],
    })

out_path = 'solutions_export.json'
with open(out_path, 'w') as f:
    json.dump(data, f)

print(f'Exported {len(data)} solutions to {out_path}')
conn.close()
