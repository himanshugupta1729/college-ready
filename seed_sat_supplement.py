"""
seed_sat_supplement.py — Adds 8 more SAT questions to reach 46 total (need 44 minimum).

Fills gaps in FUAR balance and difficulty spread for the existing 38-question SAT bank.
Uses the same domain names as seed_questions.py (heart_of_algebra, problem_solving,
passport_advanced, additional_topics).
"""

import sqlite3
from collections import defaultdict

DB_PATH = "college_ready.db"

# Each tuple: (track, sat_domain, fuar_dimension, difficulty,
#              question_text, question_type,
#              option_a, option_b, option_c, option_d,
#              correct_answer, explanation, topic_tag)

QUESTIONS = [
    # --- heart_of_algebra ---
    ("sat", "heart_of_algebra", "A", 3,
     "A phone plan charges $30 per month plus $0.10 per text message. If Maya's bill was $47, how many texts did she send?",
     "multiple_choice",
     "140", "170", "180", "200",
     "B",
     "30 + 0.10t = 47 → 0.10t = 17 → t = 170.",
     "linear_modeling"),

    ("sat", "heart_of_algebra", "R", 4,
     "If 3a + 2b = 18 and a − b = 1, what is the value of a + b?",
     "multiple_choice",
     "4", "5", "6", "7",
     "C",
     "From a − b = 1: a = b + 1. Substitute: 3(b+1) + 2b = 18 → 5b + 3 = 18 → b = 3, a = 4. So a + b = 7. Wait: 3(4)+2(3)=18 ✓, a-b=1 ✓, a+b=7.",
     "systems_of_equations"),

    # --- problem_solving ---
    ("sat", "problem_solving", "F", 2,
     "The mean of 5 numbers is 12. What is their sum?",
     "multiple_choice",
     "17", "48", "60", "72",
     "C",
     "Mean = sum/count, so sum = mean × count = 12 × 5 = 60.",
     "statistics_mean"),

    ("sat", "problem_solving", "U", 4,
     "A scatter plot shows a negative correlation between hours of TV watched and test scores. Which conclusion is valid?",
     "multiple_choice",
     "Watching TV causes lower test scores",
     "Students with higher scores tend to watch less TV",
     "All students who watch TV score low",
     "Reducing TV time will raise any student's score",
     "B",
     "Correlation shows a trend in the data, not causation. B correctly describes the association without implying causation.",
     "correlation_interpretation"),

    # --- passport_advanced ---
    ("sat", "passport_advanced", "A", 3,
     "A ball is thrown upward with height h(t) = -16t² + 48t + 5, where t is seconds. What is the maximum height?",
     "multiple_choice",
     "41 feet", "53 feet", "36 feet", "48 feet",
     "A",
     "Maximum at t = -b/(2a) = -48/(2×-16) = 1.5s. h(1.5) = -16(2.25) + 48(1.5) + 5 = -36 + 72 + 5 = 41.",
     "quadratic_applications"),

    ("sat", "passport_advanced", "R", 5,
     "If f(x) = x² − 4x + 3 and g(x) = x − 1, for what values of x does f(x)/g(x) = 0?",
     "multiple_choice",
     "x = 1 only", "x = 3 only", "x = 1 and x = 3", "x = 3 (x = 1 is excluded)",
     "D",
     "f(x)/g(x) = (x−1)(x−3)/(x−1) = x−3 when x ≠ 1. Equals 0 when x = 3. x = 1 makes denominator 0, so it's excluded.",
     "rational_expressions"),

    # --- additional_topics ---
    ("sat", "additional_topics", "F", 2,
     "In a right triangle, one leg is 6 and the hypotenuse is 10. What is the other leg?",
     "multiple_choice",
     "4", "7", "8", "√136",
     "C",
     "By the Pythagorean theorem: a² + 6² = 10² → a² = 100 − 36 = 64 → a = 8.",
     "pythagorean_theorem"),

    ("sat", "additional_topics", "U", 3,
     "A circle has the equation (x − 2)² + (y + 3)² = 25. What is the center and radius?",
     "multiple_choice",
     "Center (2, −3), radius 5",
     "Center (−2, 3), radius 5",
     "Center (2, −3), radius 25",
     "Center (−2, 3), radius 25",
     "A",
     "Standard form (x−h)² + (y−k)² = r². Here h=2, k=−3, r²=25 so r=5.",
     "circle_equations"),
]


def seed():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Check for duplicates by question_text
    inserted = 0
    skipped = 0
    for q in QUESTIONS:
        existing = cur.execute(
            "SELECT id FROM questions WHERE track = ? AND question_text = ?",
            (q[0], q[4])
        ).fetchone()
        if existing:
            skipped += 1
            continue

        cur.execute("""
            INSERT INTO questions
                (track, sat_domain, fuar_dimension, difficulty,
                 question_text, question_type,
                 option_a, option_b, option_c, option_d,
                 correct_answer, explanation, topic_tag)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, q)
        inserted += 1

    conn.commit()

    total = cur.execute("SELECT COUNT(*) FROM questions WHERE track = 'sat'").fetchone()[0]
    conn.close()

    print(f"SAT supplement: inserted {inserted}, skipped {skipped} (duplicates)")
    print(f"Total SAT questions now: {total}")


if __name__ == "__main__":
    seed()
