"""
Verify ALL 1,107 questions for mathematical correctness using Claude API.

Exports questions in batches by track, asks Claude to verify each question's
correct answer, and flags any errors.

Usage: python verify_all_questions.py [--track sat] [--batch-size 25]
"""

import sqlite3
import json
import os
import sys
import time
import argparse
from datetime import datetime

try:
    import anthropic
except ImportError:
    print("ERROR: pip install anthropic")
    sys.exit(1)

DB_PATH = os.environ.get('DATABASE_PATH', 'college_ready.db')
CLIENT = anthropic.Anthropic()
MODEL = "claude-sonnet-4-20250514"

SYSTEM_PROMPT = """You are a math verification agent. Your job is to check whether each multiple-choice math question has the correct answer marked.

For each question, you must:
1. Solve the problem yourself from scratch
2. Compare your answer to the marked correct answer
3. Report whether the marked answer is CORRECT or WRONG

Be extremely careful with:
- Sign errors
- Off-by-one errors
- Unit conversions
- Domain restrictions (e.g., square roots of negatives)
- Whether the question asks for x, 2x, f(x), etc.
- AP-level calculus, statistics, and precalculus concepts

Respond in JSON format ONLY. No markdown, no explanation outside the JSON.
Return an array of objects, one per question:
[
  {
    "id": <question_id>,
    "marked_answer": "<A/B/C/D>",
    "correct_answer": "<A/B/C/D>",
    "verdict": "CORRECT" or "WRONG",
    "your_solution": "<brief solution showing your work>",
    "issue": "<description of error if WRONG, null if CORRECT>"
  }
]
"""


def get_questions(track=None):
    """Load all questions, optionally filtered by track."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    if track:
        rows = conn.execute(
            "SELECT id, track, question_text, option_a, option_b, option_c, option_d, "
            "correct_answer, explanation, difficulty, fuar_dimension "
            "FROM questions WHERE track = ? ORDER BY id", (track,)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT id, track, question_text, option_a, option_b, option_c, option_d, "
            "correct_answer, explanation, difficulty, fuar_dimension "
            "FROM questions ORDER BY track, id"
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def format_batch(questions):
    """Format a batch of questions for the verification prompt."""
    lines = []
    for q in questions:
        lines.append(f"""--- Question {q['id']} (Track: {q['track']}, Difficulty: {q['difficulty']}, FUAR: {q['fuar_dimension']}) ---
{q['question_text']}

A) {q['option_a']}
B) {q['option_b']}
C) {q['option_c']}
D) {q['option_d']}

Marked correct answer: {q['correct_answer']}
Explanation given: {q['explanation']}
""")
    return "\n".join(lines)


def verify_batch(questions, retries=2):
    """Send a batch of questions to Claude for verification."""
    prompt = f"""Verify each of the following {len(questions)} math questions. Solve each one yourself and check if the marked answer is correct.

{format_batch(questions)}

Return your results as a JSON array. ONLY output the JSON array, nothing else."""

    for attempt in range(retries + 1):
        try:
            response = CLIENT.messages.create(
                model=MODEL,
                max_tokens=8192,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}],
            )
            text = response.content[0].text.strip()
            # Try to parse JSON - handle potential markdown wrapping
            if text.startswith("```"):
                text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
            results = json.loads(text)
            return results
        except (json.JSONDecodeError, Exception) as e:
            if attempt < retries:
                print(f"  Retry {attempt + 1}/{retries} due to: {e}")
                time.sleep(2)
            else:
                print(f"  FAILED after {retries + 1} attempts: {e}")
                return None


def main():
    parser = argparse.ArgumentParser(description="Verify math question correctness")
    parser.add_argument("--track", type=str, help="Verify only this track (e.g., sat, grade_6)")
    parser.add_argument("--batch-size", type=int, default=20, help="Questions per API call (default: 20)")
    parser.add_argument("--output", type=str, default="verification_results.json", help="Output file")
    args = parser.parse_args()

    questions = get_questions(args.track)
    print(f"\n{'='*60}")
    print(f"QUESTION VERIFICATION — {len(questions)} questions")
    if args.track:
        print(f"Track filter: {args.track}")
    print(f"Batch size: {args.batch_size}")
    print(f"Estimated API calls: {(len(questions) + args.batch_size - 1) // args.batch_size}")
    print(f"{'='*60}\n")

    all_results = []
    errors = []
    failed_batches = []

    # Process in batches
    for i in range(0, len(questions), args.batch_size):
        batch = questions[i:i + args.batch_size]
        batch_num = i // args.batch_size + 1
        total_batches = (len(questions) + args.batch_size - 1) // args.batch_size

        tracks_in_batch = set(q['track'] for q in batch)
        print(f"Batch {batch_num}/{total_batches} — IDs {batch[0]['id']}-{batch[-1]['id']} "
              f"({', '.join(tracks_in_batch)})")

        results = verify_batch(batch)

        if results is None:
            failed_batches.append({
                'batch': batch_num,
                'ids': [q['id'] for q in batch],
            })
            print(f"  ⚠ Batch failed — will need manual review")
            continue

        for r in results:
            all_results.append(r)
            if r.get('verdict') == 'WRONG':
                errors.append(r)
                print(f"  ❌ Q{r['id']}: Marked {r['marked_answer']}, "
                      f"should be {r['correct_answer']} — {r.get('issue', '')}")

        correct_in_batch = sum(1 for r in results if r.get('verdict') == 'CORRECT')
        wrong_in_batch = sum(1 for r in results if r.get('verdict') == 'WRONG')
        print(f"  ✓ {correct_in_batch} correct, {'❌ ' + str(wrong_in_batch) + ' WRONG' if wrong_in_batch else 'all good'}")

        # Rate limiting
        if i + args.batch_size < len(questions):
            time.sleep(1)

    # Summary
    print(f"\n{'='*60}")
    print(f"VERIFICATION COMPLETE")
    print(f"{'='*60}")
    print(f"Total verified: {len(all_results)}/{len(questions)}")
    print(f"Correct: {len(all_results) - len(errors)}")
    print(f"Errors found: {len(errors)}")
    if failed_batches:
        print(f"Failed batches (need manual review): {len(failed_batches)}")

    if errors:
        print(f"\n--- ERRORS ---")
        for e in errors:
            print(f"  Q{e['id']}: Marked {e['marked_answer']} → Should be {e['correct_answer']}")
            print(f"    Solution: {e.get('your_solution', 'N/A')}")
            print(f"    Issue: {e.get('issue', 'N/A')}")
            print()

    # Save results
    output = {
        'timestamp': datetime.now().isoformat(),
        'total_questions': len(questions),
        'total_verified': len(all_results),
        'correct_count': len(all_results) - len(errors),
        'error_count': len(errors),
        'failed_batches': failed_batches,
        'errors': errors,
        'all_results': all_results,
    }

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), args.output)
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\nFull results saved to: {output_path}")


if __name__ == '__main__':
    main()
