#!/usr/bin/env python3
"""
One-time batch: Generate worked solutions, wrong-answer analyses, and
interactive simulations for every question in the College Ready DB.

Usage:
    python3 generate_solutions.py                  # process all missing
    python3 generate_solutions.py --limit 50       # process 50 at a time
    python3 generate_solutions.py --question-id 42 # single question
    python3 generate_solutions.py --dry-run        # preview prompt, no API call

Resume-safe: only processes questions where worked_solution_json IS NULL.
"""

import os, sys, json, time, sqlite3, argparse, logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

DB_PATH = os.environ.get('DATABASE_PATH', 'college_ready.db')

PROMPT_TEMPLATE = """You are a math tutor creating review materials for a high school student who got this question wrong on a practice test.

**Question:** {question_text}

**Options:**
A) {option_a}
B) {option_b}
C) {option_c}
D) {option_d}

**Correct Answer:** {correct_answer}

**Topic:** {sat_domain} | **Skill:** {fuar_dimension} | **Difficulty:** {difficulty}/5

Produce a JSON object with exactly these two keys:

### 1. "worked_solution" — array of step objects
Each step:
{{"step": 1, "title": "short action title", "math": "the actual math expression/equation", "why": "plain-English explanation of WHY this step works"}}
- 3-5 steps max
- Write math in simple text (no LaTeX). Use × for multiply, ÷ for divide, √ for roots, ^ for exponents.
- Each step should be a single logical action (don't combine two operations)
- The final step should clearly state the answer

### 2. "wrong_answer_analyses" — object keyed by the 3 wrong option letters
For each wrong option:
{{"mistake": "what YOU probably did wrong (1 sentence, written in second person — say 'You likely...' not 'The student likely...')", "tip": "how to avoid this mistake next time (1 sentence, second person)"}}
Only include the 3 WRONG options, not the correct one.
IMPORTANT: Always write in second person ("You picked...", "You probably...", "You confused..."). Never say "the student".

Return ONLY the JSON object, no markdown fences, no extra text.
"""


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=5000")
    return conn


def call_claude(prompt, question_id):
    """Call Claude API with retry logic."""
    import anthropic
    client = anthropic.Anthropic(timeout=60.0)

    for attempt in range(3):
        try:
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text.strip()
        except Exception as e:
            err = str(e).lower()
            if 'credit' in err or 'auth' in err or 'invalid' in err:
                raise
            wait = (attempt + 1) * 5
            logging.warning(f'  Q#{question_id} attempt {attempt+1} failed: {e}. Retry in {wait}s...')
            time.sleep(wait)

    raise Exception(f"All 3 attempts failed for question {question_id}")


def parse_response(raw_text, question_id):
    """Parse Claude's JSON response, handling common formatting issues."""
    text = raw_text.strip()

    # Strip markdown fences if present (```json ... ```)
    if text.startswith('```'):
        # Remove opening fence line
        first_newline = text.find('\n')
        if first_newline > 0:
            text = text[first_newline + 1:]
        else:
            text = text[3:]
    if text.rstrip().endswith('```'):
        text = text[:text.rfind('```')].rstrip()

    text = text.strip()

    # Try direct parse first
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        # Try raw_decode (handles trailing text after valid JSON)
        try:
            decoder = json.JSONDecoder()
            data, _ = decoder.raw_decode(text)
        except (json.JSONDecodeError, ValueError):
            # Last resort: find the outermost { ... }
            start = text.find('{')
            if start >= 0:
                depth = 0
                in_string = False
                escape = False
                end = start
                for i in range(start, len(text)):
                    c = text[i]
                    if escape:
                        escape = False
                        continue
                    if c == '\\' and in_string:
                        escape = True
                        continue
                    if c == '"' and not escape:
                        in_string = not in_string
                        continue
                    if not in_string:
                        if c == '{':
                            depth += 1
                        elif c == '}':
                            depth -= 1
                            if depth == 0:
                                end = i + 1
                                break
                try:
                    data = json.loads(text[start:end])
                except (json.JSONDecodeError, ValueError) as e:
                    logging.error(f'  Q#{question_id} JSON parse error: {e}')
                    logging.error(f'  Raw text (first 500 chars): {text[:500]}')
                    return None
            else:
                logging.error(f'  Q#{question_id} no JSON object found')
                return None

    # Validate and normalize structure
    if not isinstance(data.get('worked_solution'), list):
        logging.error(f'  Q#{question_id} missing worked_solution array. Keys: {list(data.keys())}')
        return None
    if not isinstance(data.get('wrong_answer_analyses'), dict):
        logging.error(f'  Q#{question_id} missing wrong_answer_analyses dict. Keys: {list(data.keys())}')
        return None

    return data


def process_question(conn, question, dry_run=False):
    """Generate and store solution for one question."""
    q = dict(question)
    qid = q['id']

    fuar_map = {'F': 'Fluency', 'U': 'Understanding', 'A': 'Application', 'R': 'Reasoning'}

    prompt = PROMPT_TEMPLATE.format(
        question_text=q['question_text'],
        option_a=q['option_a'] or '',
        option_b=q['option_b'] or '',
        option_c=q['option_c'] or '',
        option_d=q['option_d'] or '',
        correct_answer=q['correct_answer'],
        sat_domain=q['sat_domain'] or 'General',
        fuar_dimension=fuar_map.get(q['fuar_dimension'], q['fuar_dimension']),
        difficulty=q['difficulty'],
        question_id=qid
    )

    if dry_run:
        print(f"\n{'='*60}")
        print(f"Question #{qid}: {q['question_text'][:80]}...")
        print(f"Prompt length: {len(prompt)} chars")
        print(f"{'='*60}")
        return True

    logging.info(f'  Processing Q#{qid}: {q["question_text"][:60]}...')

    raw = call_claude(prompt, qid)
    data = parse_response(raw, qid)

    if not data:
        logging.error(f'  Q#{qid} FAILED — skipping (will retry next run)')
        return False

    # Store in DB
    conn.execute("""
        UPDATE questions SET
            worked_solution_json = ?,
            wrong_answer_analyses = ?
        WHERE id = ?
    """, (
        json.dumps(data['worked_solution']),
        json.dumps(data['wrong_answer_analyses']),
        qid
    ))
    conn.commit()

    logging.info(f'  Q#{qid} ✓ ({len(data["worked_solution"])} steps)')
    return True


def main():
    parser = argparse.ArgumentParser(description='Generate worked solutions + simulations')
    parser.add_argument('--limit', type=int, default=0, help='Max questions to process (0=all)')
    parser.add_argument('--question-id', type=int, default=0, help='Process single question')
    parser.add_argument('--dry-run', action='store_true', help='Preview prompts without API calls')
    parser.add_argument('--force', action='store_true', help='Regenerate even if already done')
    args = parser.parse_args()

    conn = get_connection()

    # Ensure columns exist
    for col in ['worked_solution_json', 'wrong_answer_analyses', 'simulation_html']:
        try:
            conn.execute(f"ALTER TABLE questions ADD COLUMN {col} TEXT")
        except Exception:
            pass

    if args.question_id:
        questions = conn.execute("SELECT * FROM questions WHERE id = ?", (args.question_id,)).fetchall()
    elif args.force:
        query = "SELECT * FROM questions ORDER BY id"
        if args.limit:
            query += f" LIMIT {args.limit}"
        questions = conn.execute(query).fetchall()
    else:
        query = "SELECT * FROM questions WHERE worked_solution_json IS NULL ORDER BY id"
        if args.limit:
            query += f" LIMIT {args.limit}"
        questions = conn.execute(query).fetchall()

    total = len(questions)
    if total == 0:
        logging.info("All questions already have solutions. Use --force to regenerate.")
        return

    already_done = conn.execute("SELECT COUNT(*) FROM questions WHERE worked_solution_json IS NOT NULL").fetchone()[0]
    logging.info(f"Found {total} questions to process ({already_done} already done)")

    if not args.dry_run:
        logging.info(f"Estimated cost: ~${total * 0.03:.2f} (Sonnet, ~2K tokens/question)")
        logging.info(f"Estimated time: ~{total * 3 / 60:.0f} minutes")
        logging.info("")

    success = 0
    failed = 0

    for i, q in enumerate(questions):
        try:
            if process_question(conn, q, dry_run=args.dry_run):
                success += 1
            else:
                failed += 1
        except KeyboardInterrupt:
            logging.info(f"\nInterrupted. Processed {success}/{i+1}. Resume to continue.")
            break
        except Exception as e:
            logging.error(f'  Q#{q["id"]} ERROR: {e}')
            failed += 1

        # Progress log every 25 questions
        if (i + 1) % 25 == 0:
            logging.info(f"  --- Progress: {i+1}/{total} ({success} ok, {failed} failed) ---")

        # Rate limit: small delay between calls
        if not args.dry_run and i < total - 1:
            time.sleep(1)

    logging.info(f"\nDone. {success} succeeded, {failed} failed out of {total}.")
    if failed > 0:
        logging.info("Run again to retry failed questions (they're still NULL in the DB).")

    conn.close()


if __name__ == '__main__':
    main()
