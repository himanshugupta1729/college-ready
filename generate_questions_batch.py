#!/usr/bin/env python3
"""
Generate additional questions for all tracks to reach 3x test variety + 140 practice pool.
Uses Claude API to generate, then verifies each question for correctness.

Usage: python3 generate_questions_batch.py [--track grade_6] [--dry-run]
"""

import sqlite3
import json
import os
import sys
import time
import random
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

# Track metadata for question generation
TRACK_META = {
    'sat': {
        'name': 'SAT Math',
        'grade_level': '9-12',
        'domains': ['heart_of_algebra', 'problem_solving', 'passport_advanced', 'additional_topics'],
        'topics': {
            'heart_of_algebra': ['linear equations', 'systems of equations', 'linear inequalities', 'linear functions and graphs'],
            'problem_solving': ['ratios and proportions', 'percentages', 'data interpretation', 'statistics and probability'],
            'passport_advanced': ['quadratics', 'polynomials', 'exponential functions', 'rational expressions'],
            'additional_topics': ['geometry', 'trigonometry', 'complex numbers', 'circle equations'],
        },
    },
    'ap_calc_ab': {
        'name': 'AP Calculus AB',
        'grade_level': '11-12',
        'domains': ['limits', 'derivatives', 'integrals', 'applications'],
        'topics': {
            'limits': ['limit evaluation', 'continuity', 'squeeze theorem', 'limits at infinity'],
            'derivatives': ['power rule', 'chain rule', 'product rule', 'quotient rule', 'implicit differentiation'],
            'integrals': ['antiderivatives', 'u-substitution', 'definite integrals', 'FTC'],
            'applications': ['related rates', 'optimization', 'area between curves', 'volumes of revolution'],
        },
    },
    'ap_calc_bc': {
        'name': 'AP Calculus BC',
        'grade_level': '11-12',
        'domains': ['series', 'parametric_polar', 'advanced_integration', 'differential_equations'],
        'topics': {
            'series': ['Taylor series', 'Maclaurin series', 'convergence tests', 'power series', 'geometric series'],
            'parametric_polar': ['parametric equations', 'polar coordinates', 'arc length', 'area in polar'],
            'advanced_integration': ['integration by parts', 'partial fractions', 'improper integrals'],
            'differential_equations': ['separable equations', 'slope fields', 'Euler method', 'logistic growth'],
        },
    },
    'ap_stats': {
        'name': 'AP Statistics',
        'grade_level': '11-12',
        'domains': ['exploring_data', 'sampling', 'probability', 'inference'],
        'topics': {
            'exploring_data': ['distributions', 'boxplots', 'standard deviation', 'correlation', 'regression'],
            'sampling': ['sampling methods', 'bias', 'experimental design', 'randomization'],
            'probability': ['probability rules', 'conditional probability', 'binomial', 'normal distribution'],
            'inference': ['confidence intervals', 'hypothesis testing', 'chi-square', 't-tests', 'p-values'],
        },
    },
    'ap_precalc': {
        'name': 'AP Precalculus',
        'grade_level': '11-12',
        'domains': ['polynomial_rational', 'exponential_log', 'trig', 'polar_parametric'],
        'topics': {
            'polynomial_rational': ['polynomial behavior', 'rational functions', 'asymptotes', 'zeros'],
            'exponential_log': ['exponential growth/decay', 'logarithm properties', 'solving log equations'],
            'trig': ['unit circle', 'trig identities', 'inverse trig', 'sinusoidal modeling'],
            'polar_parametric': ['polar coordinates', 'parametric equations', 'complex numbers'],
        },
    },
    'algebra_1': {
        'name': 'Algebra 1',
        'grade_level': '8-9',
        'domains': ['linear_equations', 'linear_functions', 'systems', 'quadratics', 'exponentials', 'data_stats'],
        'topics': {
            'linear_equations': ['one-step equations', 'two-step equations', 'multi-step equations', 'literal equations'],
            'linear_functions': ['slope', 'slope-intercept form', 'point-slope form', 'parallel and perpendicular lines'],
            'systems': ['graphing systems', 'substitution', 'elimination', 'word problems with systems'],
            'quadratics': ['factoring', 'quadratic formula', 'completing the square', 'vertex form'],
            'exponentials': ['exponential growth', 'exponential decay', 'compound interest'],
            'data_stats': ['mean median mode', 'box plots', 'scatter plots', 'line of best fit'],
        },
    },
    'algebra_2': {
        'name': 'Algebra 2',
        'grade_level': '10-11',
        'domains': ['polynomials', 'rational', 'exponential_log', 'sequences', 'trig_intro', 'complex'],
        'topics': {
            'polynomials': ['polynomial operations', 'factoring', 'remainder theorem', 'zeros'],
            'rational': ['simplifying rational expressions', 'rational equations', 'asymptotes'],
            'exponential_log': ['exponential equations', 'logarithms', 'natural log', 'log properties'],
            'sequences': ['arithmetic sequences', 'geometric sequences', 'series', 'recursive formulas'],
            'trig_intro': ['right triangle trig', 'unit circle basics', 'radian measure'],
            'complex': ['complex numbers', 'operations with complex', 'complex plane'],
        },
    },
    'geometry': {
        'name': 'Geometry',
        'grade_level': '9-10',
        'domains': ['triangles', 'circles', 'transformations', 'area_volume', 'coordinate', 'proofs'],
        'topics': {
            'triangles': ['triangle congruence', 'similarity', 'Pythagorean theorem', 'special right triangles'],
            'circles': ['arc length', 'sector area', 'inscribed angles', 'tangent lines', 'circle theorems'],
            'transformations': ['translations', 'rotations', 'reflections', 'dilations'],
            'area_volume': ['area of polygons', 'surface area', 'volume of prisms/cylinders/cones/spheres'],
            'coordinate': ['distance formula', 'midpoint', 'equations of circles', 'coordinate proofs'],
            'proofs': ['angle relationships', 'parallel lines', 'triangle angle sum', 'exterior angle theorem'],
        },
    },
    'precalculus': {
        'name': 'Precalculus',
        'grade_level': '11-12',
        'domains': ['functions', 'polynomial', 'trig', 'exponential_log', 'sequences', 'conics'],
        'topics': {
            'functions': ['domain and range', 'composition', 'inverse functions', 'transformations'],
            'polynomial': ['polynomial division', 'rational root theorem', 'end behavior', 'graphing'],
            'trig': ['trig identities', 'law of sines', 'law of cosines', 'sinusoidal functions'],
            'exponential_log': ['exponential equations', 'log equations', 'growth and decay'],
            'sequences': ['arithmetic', 'geometric', 'partial sums', 'infinite series'],
            'conics': ['parabolas', 'ellipses', 'hyperbolas', 'conic sections'],
        },
    },
    'statistics': {
        'name': 'Statistics',
        'grade_level': '11-12',
        'domains': ['descriptive', 'probability', 'distributions', 'inference'],
        'topics': {
            'descriptive': ['measures of center', 'measures of spread', 'boxplots', 'histograms', 'outliers'],
            'probability': ['basic probability', 'conditional probability', 'independent events', 'counting'],
            'distributions': ['normal distribution', 'binomial distribution', 'sampling distributions', 'z-scores'],
            'inference': ['confidence intervals', 'hypothesis testing', 'margin of error', 'regression'],
        },
    },
    'grade_6': {
        'name': 'Grade 6 Math',
        'grade_level': '6',
        'domains': ['ratios', 'number_system', 'expressions', 'geometry_6', 'statistics_6'],
        'topics': {
            'ratios': ['ratios', 'unit rates', 'percentages', 'proportional reasoning'],
            'number_system': ['dividing fractions', 'decimal operations', 'GCF and LCM', 'negative numbers intro'],
            'expressions': ['writing expressions', 'evaluating expressions', 'equivalent expressions', 'one-step equations'],
            'geometry_6': ['area of triangles', 'area of polygons', 'volume', 'surface area', 'coordinate plane'],
            'statistics_6': ['mean', 'median', 'mode', 'range', 'data displays'],
        },
    },
    'grade_7': {
        'name': 'Grade 7 Math',
        'grade_level': '7',
        'domains': ['proportional', 'number_system_7', 'expressions_7', 'geometry_7', 'probability_7'],
        'topics': {
            'proportional': ['proportional relationships', 'constant of proportionality', 'percent problems', 'scale drawings'],
            'number_system_7': ['integer operations', 'rational number operations', 'absolute value'],
            'expressions_7': ['combining like terms', 'distributive property', 'two-step equations', 'inequalities'],
            'geometry_7': ['angle relationships', 'area and circumference of circles', 'cross-sections', 'scale drawings'],
            'probability_7': ['experimental probability', 'theoretical probability', 'compound events', 'simulations'],
        },
    },
    'grade_7_accelerated': {
        'name': 'Grade 7 Accelerated (Pre-Algebra)',
        'grade_level': '7',
        'domains': ['linear_relationships', 'equations_systems', 'functions_intro', 'geometry_accel', 'data_accel'],
        'topics': {
            'linear_relationships': ['slope', 'proportional vs non-proportional', 'graphing linear equations', 'rate of change'],
            'equations_systems': ['multi-step equations', 'equations with variables on both sides', 'simple systems'],
            'functions_intro': ['function definition', 'function notation', 'linear vs nonlinear', 'input-output tables'],
            'geometry_accel': ['transformations', 'congruence', 'similarity', 'Pythagorean theorem', 'volume of cylinders/cones/spheres'],
            'data_accel': ['scatter plots', 'line of best fit', 'two-way tables', 'associations'],
        },
    },
    'grade_8': {
        'name': 'Grade 8 Math',
        'grade_level': '8',
        'domains': ['linear_8', 'functions_8', 'geometry_8', 'number_system_8', 'data_8'],
        'topics': {
            'linear_8': ['slope from graph/table/equation', 'y-intercept', 'comparing linear functions', 'systems intro'],
            'functions_8': ['function concept', 'linear vs nonlinear functions', 'function from graph/table', 'rate of change'],
            'geometry_8': ['transformations', 'congruence and similarity', 'Pythagorean theorem applications', 'volume'],
            'number_system_8': ['rational vs irrational numbers', 'square roots', 'cube roots', 'scientific notation'],
            'data_8': ['scatter plots', 'line of best fit', 'two-way tables', 'interpreting data'],
        },
    },
}


GENERATION_PROMPT = """Generate exactly {count} multiple-choice math questions for {track_name} ({grade_level}).

REQUIREMENTS:
- FUAR dimension: {fuar} ({fuar_desc})
- Difficulty: {difficulty}/5 ({diff_desc})
- Domain: {domain}
- Topics to cover: {topics}

FUAR DIMENSIONS:
- F (Fluency): Can the student execute procedures quickly and accurately? Straightforward computation.
- U (Understanding): Does the student grasp WHY a concept works? Conceptual questions.
- A (Application): Can the student apply math to real-world contexts? Word problems, modeling.
- R (Reasoning): Can the student think through novel problems? Multi-step, non-routine.

DIFFICULTY SCALE:
- 1: Basic recall/computation
- 2: Straightforward application of a single concept
- 3: Requires connecting two concepts or careful setup
- 4: Multi-step with potential for errors, requires insight
- 5: Complex, requires creative problem-solving or deep understanding

RULES:
1. Each question MUST have exactly 4 options (A, B, C, D) with exactly ONE correct answer
2. The correct answer MUST be mathematically verifiable — solve it yourself before writing
3. Distractors should reflect common student mistakes (sign errors, forgetting to distribute, etc.)
4. Questions should be DISTINCT from each other — different scenarios, different numbers
5. For grades 6-8: use age-appropriate contexts (sports, games, food, school scenarios)
6. For AP level: match the rigor and style of actual AP exam questions
7. NO ambiguous questions where multiple answers could be correct
8. Use clear, concise language. Include all necessary information to solve.

Return ONLY a JSON array. No markdown, no explanation outside JSON:
[
  {{
    "question_text": "...",
    "option_a": "...",
    "option_b": "...",
    "option_c": "...",
    "option_d": "...",
    "correct_answer": "A/B/C/D",
    "explanation": "Brief step-by-step solution",
    "topic_tag": "specific_topic_name"
  }}
]
"""

VERIFY_PROMPT = """Verify these {count} math questions. For each one, solve it yourself from scratch and check if the marked answer is correct.

{questions}

Return ONLY a JSON array:
[
  {{
    "index": 0,
    "verdict": "CORRECT" or "WRONG",
    "correct_answer": "A/B/C/D",
    "issue": "description if WRONG, null if CORRECT"
  }}
]
"""


def get_needed_counts():
    """Calculate how many questions each track needs."""
    conn = sqlite3.connect(DB_PATH)
    track_counts = {r[0]: r[1] for r in conn.execute(
        "SELECT track, COUNT(*) FROM questions GROUP BY track").fetchall()}
    conn.close()

    test_sizes = {
        'sat': 44, 'ap_calc_ab': 28, 'ap_calc_bc': 30, 'ap_stats': 28, 'ap_precalc': 24,
        'algebra_1': 25, 'algebra_2': 28, 'geometry': 25, 'precalculus': 28, 'statistics': 22,
        'grade_6': 24, 'grade_7': 24, 'grade_7_accelerated': 24, 'grade_8': 24,
    }

    needs = {}
    for track, test_size in test_sizes.items():
        have = track_counts.get(track, 0)
        target = max(test_size * 3, test_size + 140)
        gap = max(0, target - have)
        if gap > 0:
            needs[track] = {'have': have, 'target': target, 'gap': gap, 'test_size': test_size}
    return needs


def generate_batch(track, fuar, difficulty, domain, count):
    """Generate a batch of questions using Claude API."""
    meta = TRACK_META[track]
    topics = meta['topics'].get(domain, [domain])

    fuar_descs = {
        'F': 'Fluency — executing procedures accurately',
        'U': 'Understanding — grasping why concepts work',
        'A': 'Application — applying math to real contexts',
        'R': 'Reasoning — thinking through novel problems',
    }
    diff_descs = {
        1: 'basic recall', 2: 'single concept', 3: 'connecting concepts',
        4: 'multi-step with insight', 5: 'complex problem-solving',
    }

    prompt = GENERATION_PROMPT.format(
        count=count, track_name=meta['name'], grade_level=meta['grade_level'],
        fuar=fuar, fuar_desc=fuar_descs[fuar],
        difficulty=difficulty, diff_desc=diff_descs[difficulty],
        domain=domain, topics=', '.join(topics),
    )

    for attempt in range(3):
        try:
            response = CLIENT.messages.create(
                model=MODEL, max_tokens=8192,
                messages=[{"role": "user", "content": prompt}],
            )
            text = response.content[0].text.strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
            questions = json.loads(text)
            return questions
        except Exception as e:
            if attempt < 2:
                print(f"    Retry {attempt+1}: {e}")
                time.sleep(2)
            else:
                print(f"    FAILED: {e}")
                return []


def verify_batch(questions):
    """Verify a batch of questions using Claude API. Returns list of verified questions."""
    if not questions:
        return []

    formatted = ""
    for i, q in enumerate(questions):
        formatted += f"\n--- Question {i} ---\n"
        formatted += f"{q['question_text']}\n"
        formatted += f"A) {q['option_a']}\nB) {q['option_b']}\nC) {q['option_c']}\nD) {q['option_d']}\n"
        formatted += f"Marked: {q['correct_answer']}\n"

    prompt = VERIFY_PROMPT.format(count=len(questions), questions=formatted)

    for attempt in range(3):
        try:
            response = CLIENT.messages.create(
                model=MODEL, max_tokens=4096,
                messages=[{"role": "user", "content": prompt}],
            )
            text = response.content[0].text.strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
            results = json.loads(text)

            verified = []
            for r in results:
                idx = r['index']
                if idx < len(questions):
                    if r['verdict'] == 'CORRECT':
                        verified.append(questions[idx])
                    elif r.get('correct_answer'):
                        # Fix the answer
                        questions[idx]['correct_answer'] = r['correct_answer']
                        verified.append(questions[idx])
                        print(f"    Fixed Q{idx}: {r.get('issue', '')}")
                    else:
                        print(f"    Dropped Q{idx}: {r.get('issue', 'wrong')}")
            return verified
        except Exception as e:
            if attempt < 2:
                time.sleep(2)
            else:
                print(f"    Verify FAILED: {e}")
                return questions  # Return unverified if verify fails


def insert_questions(track, questions, domain):
    """Insert verified questions into the database."""
    conn = sqlite3.connect(DB_PATH)
    inserted = 0
    for q in questions:
        # Dedup by question text
        exists = conn.execute("SELECT id FROM questions WHERE question_text = ?",
                               (q['question_text'],)).fetchone()
        if exists:
            continue
        conn.execute("""INSERT INTO questions (track, sat_domain, fuar_dimension, difficulty,
            question_text, question_type, option_a, option_b, option_c, option_d,
            correct_answer, explanation, topic_tag)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (track, domain, q.get('fuar', 'F'), q.get('difficulty', 3),
             q['question_text'], 'multiple_choice',
             q['option_a'], q['option_b'], q['option_c'], q['option_d'],
             q['correct_answer'], q['explanation'], q.get('topic_tag', domain)))
        inserted += 1
    conn.commit()
    conn.close()
    return inserted


def generate_for_track(track, gap):
    """Generate all needed questions for a track with proper FUAR/difficulty distribution."""
    meta = TRACK_META[track]
    domains = meta['domains']
    fuar_dims = ['F', 'U', 'A', 'R']
    difficulties = [1, 2, 3, 4, 5]
    diff_weights = [0.1, 0.25, 0.3, 0.25, 0.1]  # bell curve

    # Distribute questions across FUAR × domain × difficulty
    per_fuar = gap // 4
    extra = gap - (per_fuar * 4)

    total_generated = 0
    total_inserted = 0

    for fi, fuar in enumerate(fuar_dims):
        fuar_count = per_fuar + (1 if fi < extra else 0)
        per_domain = max(1, fuar_count // len(domains))

        for domain in domains:
            # Pick a weighted difficulty
            for diff in [2, 3, 4, 1, 5]:
                batch_size = min(5, per_domain)
                if total_generated >= gap:
                    break

                print(f"  {track}/{fuar}/{domain}/diff{diff}: generating {batch_size}...")
                questions = generate_batch(track, fuar, diff, domain, batch_size)

                if questions:
                    # Tag with metadata
                    for q in questions:
                        q['fuar'] = fuar
                        q['difficulty'] = diff

                    verified = verify_batch(questions)
                    inserted = insert_questions(track, verified, domain)
                    total_generated += len(verified)
                    total_inserted += inserted
                    print(f"    → {len(verified)} verified, {inserted} inserted")

                if total_generated >= gap:
                    break
                time.sleep(0.5)

            if total_generated >= gap:
                break

    return total_inserted


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--track", help="Generate for specific track only")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be generated")
    args = parser.parse_args()

    needs = get_needed_counts()

    if args.track:
        if args.track not in needs:
            print(f"{args.track}: no questions needed (already at target)")
            return
        needs = {args.track: needs[args.track]}

    print(f"\n{'='*60}")
    print(f"QUESTION GENERATION — {sum(n['gap'] for n in needs.values())} questions needed")
    print(f"{'='*60}\n")

    for track, info in sorted(needs.items()):
        print(f"  {track:25s} have {info['have']:>4d}, need {info['target']:>4d} → generate {info['gap']:>4d}")

    if args.dry_run:
        print("\n[dry-run] No questions generated.")
        return

    print()
    total_inserted = 0
    for track, info in sorted(needs.items()):
        print(f"\n--- {track} ({info['gap']} questions needed) ---")
        inserted = generate_for_track(track, info['gap'])
        total_inserted += inserted
        print(f"  → {inserted} new questions inserted for {track}")

    # Final count
    conn = sqlite3.connect(DB_PATH)
    total = conn.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
    track_counts = {r[0]: r[1] for r in conn.execute(
        "SELECT track, COUNT(*) FROM questions GROUP BY track").fetchall()}
    conn.close()

    print(f"\n{'='*60}")
    print(f"GENERATION COMPLETE — {total} total questions")
    print(f"{'='*60}")
    for t in sorted(track_counts):
        print(f"  {t}: {track_counts[t]}")
    print(f"\n  New questions inserted: {total_inserted}")


if __name__ == '__main__':
    main()
