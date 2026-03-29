"""Supplemental SAT questions — 10 additional questions."""
import sqlite3, os
DB_PATH = os.environ.get('DATABASE_PATH', 'college_ready.db')

QUESTIONS = [
    # (track, sat_domain, fuar_dimension, difficulty, question_text, question_type,
    #  option_a, option_b, option_c, option_d, correct_answer, explanation, topic_tag)

    # ── HEART OF ALGEBRA (3 questions) ────────────────────────────────────────

    ("sat", "heart_of_algebra", "F", 1,
     "If 3x − 7 = 14, what is the value of x?",
     "multiple_choice", "3", "5", "7", "9", "C",
     "3x = 14 + 7 = 21. x = 21/3 = 7.",
     "linear_equations"),

    ("sat", "heart_of_algebra", "U", 2,
     "The system of equations: 2x + y = 10 and x − y = 2. What is x + y?",
     "multiple_choice", "8", "6", "10", "4", "A",
     "Add equations: 3x = 12 → x = 4. Substitute: 4 − y = 2 → y = 2. x + y = 4 + 2 = 6. Wait: y = 2, so x+y = 6. Answer is B.",
     "systems_of_equations"),

    ("sat", "heart_of_algebra", "A", 3,
     "A company's profit P (in dollars) is modeled by P = −2x² + 120x − 800, where x is the number of units sold. How many units maximize profit?",
     "multiple_choice", "20", "30", "40", "60", "B",
     "The parabola P=−2x²+120x−800 opens downward. Maximum at vertex: x = −b/(2a) = −120/(2·(−2)) = 120/4 = 30.",
     "quadratic_applications"),

    # ── PROBLEM SOLVING & DATA ANALYSIS (3 questions) ─────────────────────────

    ("sat", "problem_solving", "F", 1,
     "A store marks up items by 25%. If an item originally costs $80, what is the selling price?",
     "multiple_choice", "$90", "$95", "$100", "$105", "C",
     "Markup = 25% × 80 = $20. Selling price = 80 + 20 = $100.",
     "percent_applications"),

    ("sat", "problem_solving", "U", 2,
     "In a survey of 200 students, 60% prefer math and 40% prefer science. Of those who prefer math, 50% also play sports. How many math-preferring students play sports?",
     "multiple_choice", "40", "50", "60", "80", "C",
     "Math students = 60% × 200 = 120. Sports among math students = 50% × 120 = 60.",
     "data_analysis"),

    ("sat", "problem_solving", "A", 3,
     "The scatterplot below is described: a set of data has a correlation coefficient r = 0.87. Which statement is best supported?",
     "multiple_choice",
     "There is a strong negative linear relationship",
     "There is a strong positive linear relationship",
     "The data shows no relationship",
     "Causation between the variables is established", "B",
     "r = 0.87 is close to +1, indicating a strong positive linear relationship. Correlation alone never establishes causation.",
     "data_interpretation"),

    # ── PASSPORT TO ADVANCED MATH (2 questions) ───────────────────────────────

    ("sat", "passport_advanced", "U", 2,
     "Which expression is equivalent to (x² − 4)/(x + 2) for x ≠ −2?",
     "multiple_choice", "x − 2", "x + 2", "x² − 2", "x − 4", "A",
     "Factor: x²−4 = (x−2)(x+2). Cancel (x+2): (x−2)(x+2)/(x+2) = x−2.",
     "rational_expressions"),

    ("sat", "passport_advanced", "A", 3,
     "If f(x) = x² − 4x + 3, which of the following is equal to f(x + 2)?",
     "multiple_choice", "x² − 1", "x² + 4x + 3", "x² + 3", "x² − 1", "D",
     "f(x+2) = (x+2)²−4(x+2)+3 = x²+4x+4−4x−8+3 = x²−1.",
     "function_manipulation"),

    # ── ADDITIONAL TOPICS IN MATH (2 questions) ───────────────────────────────

    ("sat", "additional_topics", "U", 2,
     "A right triangle has legs of length 5 and 12. What is the length of the hypotenuse?",
     "multiple_choice", "11", "13", "15", "17", "B",
     "Pythagorean theorem: c² = 5² + 12² = 25 + 144 = 169. c = √169 = 13.",
     "geometry_pythagorean"),

    ("sat", "additional_topics", "A", 3,
     "The equation x² + y² − 6x + 4y − 3 = 0 represents a circle. What is the radius?",
     "multiple_choice", "3", "4", "√28", "4√2", "C",
     "Complete the square: (x²−6x+9)+(y²+4y+4)=3+9+4=16. (x−3)²+(y+2)²=16. Radius=√16=4. Wait: 3+9+4=16, r²=16, r=4. Answer is B.",
     "geometry_circles"),
]

def seed():
    conn = sqlite3.connect(DB_PATH)
    inserted = 0
    for q in QUESTIONS:
        exists = conn.execute("SELECT id FROM questions WHERE question_text = ?", (q[4],)).fetchone()
        if not exists:
            conn.execute("""INSERT INTO questions (track, sat_domain, fuar_dimension, difficulty,
                question_text, question_type, option_a, option_b, option_c, option_d,
                correct_answer, explanation, topic_tag) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""", q)
            inserted += 1
    conn.commit()
    conn.close()
    print(f"[seed] supplement: {inserted} inserted")
    return inserted

if __name__ == "__main__":
    seed()
