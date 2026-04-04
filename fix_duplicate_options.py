"""One-time fix: duplicate answer options in question bank.
Run on production: python3 fix_duplicate_options.py
"""
import sqlite3, os
DB = os.environ.get('DATABASE_PATH', 'college_ready.db')
conn = sqlite3.connect(DB)
fixes = [
    (1045, 'option_d', '96'),
    (1057, 'option_d', '120'),
    (1402, 'option_d', '8400'),
    (1581, 'option_d', '-2'),
    (1669, 'option_c', '82.4'),
    (2063, 'option_d', '35 bpm'),
    (2844, 'option_c', '(0.480, 0.560)'),
    (1391, 'option_c', '(2x − 1)(x − 3)'),
]
for qid, col, val in fixes:
    conn.execute(f'UPDATE questions SET {col} = ? WHERE id = ?', (val, qid))
    print(f'Fixed Q#{qid}: {col} → {val}')
conn.commit()
print(f'\nDone. {len(fixes)} questions fixed.')
