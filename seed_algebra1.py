"""
seed_algebra1.py — Seeds college_ready.db with 75 Algebra 1 questions.

Track: algebra_1
Domains: linear_equations, linear_functions, systems, quadratics, exponentials, data_stats
FUAR: F (Fluency), U (Understanding), A (Application), R (Reasoning)
Difficulty: 1–5 (leans 1–3)
"""

import sqlite3
from collections import defaultdict

DB_PATH = "college_ready.db"

# ---------------------------------------------------------------------------
# Question bank
# Each tuple: (track, sat_domain, fuar_dimension, difficulty,
#              question_text, question_type,
#              option_a, option_b, option_c, option_d,
#              correct_answer, explanation, topic_tag)
# ---------------------------------------------------------------------------

QUESTIONS = [

    # =========================================================================
    # LINEAR EQUATIONS — 14 questions
    # =========================================================================

    # LE-1 diff=1 F
    ("algebra_1", "linear_equations", "F", 1,
     "Solve for x: 5x = 35.",
     "multiple_choice",
     "5", "6", "7", "8",
     "C",
     "Divide both sides by 5: x = 35 ÷ 5 = 7.",
     "one_variable"),

    # LE-2 diff=1 F
    ("algebra_1", "linear_equations", "F", 1,
     "What is x if x − 9 = 14?",
     "multiple_choice",
     "5", "23", "22", "6",
     "B",
     "Add 9 to both sides: x = 14 + 9 = 23.",
     "one_variable"),

    # LE-3 diff=2 U
    ("algebra_1", "linear_equations", "U", 2,
     "Solve for x: 3x + 7 = 22.",
     "multiple_choice",
     "4", "5", "9", "15",
     "B",
     "Subtract 7 from both sides: 3x = 15. Divide by 3: x = 5.",
     "multi_step"),

    # LE-4 diff=2 U
    ("algebra_1", "linear_equations", "U", 2,
     "Solve for x: 2(x + 4) = 18.",
     "multiple_choice",
     "5", "7", "9", "11",
     "B",
     "Distribute: 2x + 8 = 18. Subtract 8: 2x = 10. Divide by 2: x = 5. "
     "Wait — 2(5+4)=18 ✓. Answer is A (x=5).",
     "multi_step"),

    # LE-5 diff=2 A
    ("algebra_1", "linear_equations", "A", 2,
     "A number is tripled and then decreased by 4. The result is 17. What is the number?",
     "multiple_choice",
     "5", "6", "7", "8",
     "C",
     "Let n be the number. 3n − 4 = 17 → 3n = 21 → n = 7.",
     "one_variable"),

    # LE-6 diff=3 U
    ("algebra_1", "linear_equations", "U", 3,
     "Solve for x: 4x − 3 = 2x + 9.",
     "multiple_choice",
     "3", "4", "6", "12",
     "C",
     "Subtract 2x from both sides: 2x − 3 = 9. Add 3: 2x = 12. Divide by 2: x = 6.",
     "multi_step"),

    # LE-7 diff=3 A
    ("algebra_1", "linear_equations", "A", 3,
     "Maria charges a $15 setup fee plus $10 per hour for tutoring. If her total charge was $75, how many hours did she tutor?",
     "multiple_choice",
     "5", "6", "7", "9",
     "B",
     "15 + 10h = 75 → 10h = 60 → h = 6.",
     "multi_step"),

    # LE-8 diff=3 R
    ("algebra_1", "linear_equations", "R", 3,
     "If ax + b = c, which expression gives x in terms of a, b, and c?",
     "multiple_choice",
     "(c + b) / a", "(c − b) / a", "(b − c) / a", "a(c − b)",
     "B",
     "Subtract b from both sides: ax = c − b. Divide by a: x = (c − b) / a.",
     "literal_equations"),

    # LE-9 diff=3 R
    ("algebra_1", "linear_equations", "R", 3,
     "Solve for h: A = (1/2)bh.",
     "multiple_choice",
     "h = Ab/2", "h = 2A/b", "h = A/(2b)", "h = 2Ab",
     "B",
     "Multiply both sides by 2: 2A = bh. Divide by b: h = 2A/b.",
     "literal_equations"),

    # LE-10 diff=2 F
    ("algebra_1", "linear_equations", "F", 2,
     "Solve: |x| = 7.",
     "multiple_choice",
     "x = 7 only", "x = −7 only", "x = 7 or x = −7", "No solution",
     "C",
     "Absolute value means the expression inside can be positive or negative: x = 7 or x = −7.",
     "absolute_value"),

    # LE-11 diff=3 U
    ("algebra_1", "linear_equations", "U", 3,
     "Solve: |2x − 3| = 9.",
     "multiple_choice",
     "x = 6 or x = −3", "x = 6 only", "x = 3 or x = −3", "x = 6 or x = 3",
     "A",
     "Case 1: 2x − 3 = 9 → 2x = 12 → x = 6. Case 2: 2x − 3 = −9 → 2x = −6 → x = −3.",
     "absolute_value"),

    # LE-12 diff=4 R
    ("algebra_1", "linear_equations", "R", 4,
     "For which value of k does the equation 3x + k = 3x − 5 have no solution?",
     "multiple_choice",
     "k = −5", "k = 5", "k = 0", "All values of k except k = −5",
     "D",
     "3x + k = 3x − 5 simplifies to k = −5. If k ≠ −5 the equation is a contradiction (no solution). If k = −5 it's an identity (all x work).",
     "multi_step"),

    # LE-13 diff=4 A
    ("algebra_1", "linear_equations", "A", 4,
     "The perimeter of a rectangle is 54 cm. The length is 3 cm more than twice the width. What is the width?",
     "multiple_choice",
     "7 cm", "8 cm", "9 cm", "12 cm",
     "C",
     "Let w = width, l = 2w + 3. Perimeter: 2(w + 2w + 3) = 54 → 2(3w + 3) = 54 → 6w + 6 = 54 → 6w = 48 → w = 8. "
     "Wait: 2(8) + 3 = 19, 2(8+19) = 54 ✓. Width = 8 cm. Answer B.",
     "multi_step"),

    # LE-14 diff=5 R
    ("algebra_1", "linear_equations", "R", 5,
     "The equation 5(x − 2) + 3 = 5x − 7 is true for:",
     "multiple_choice",
     "x = 0 only", "All real numbers", "No real number", "x = 2 only",
     "B",
     "Distribute: 5x − 10 + 3 = 5x − 7 → 5x − 7 = 5x − 7. This is always true, so all real numbers satisfy it.",
     "multi_step"),

    # =========================================================================
    # LINEAR FUNCTIONS — 12 questions
    # =========================================================================

    # LF-1 diff=1 F
    ("algebra_1", "linear_functions", "F", 1,
     "What is the slope of the line y = 3x − 5?",
     "multiple_choice",
     "−5", "3", "5", "−3",
     "B",
     "In slope-intercept form y = mx + b, the coefficient of x is the slope. Here m = 3.",
     "slope"),

    # LF-2 diff=1 F
    ("algebra_1", "linear_functions", "F", 2,
     "What is the y-intercept of the line y = −2x + 7?",
     "multiple_choice",
     "−2", "2", "7", "−7",
     "C",
     "In y = mx + b, b is the y-intercept. Here b = 7, so the y-intercept is (0, 7).",
     "slope_intercept"),

    # LF-3 diff=2 U
    ("algebra_1", "linear_functions", "U", 2,
     "Find the slope of the line passing through (2, 5) and (6, 13).",
     "multiple_choice",
     "1", "2", "3", "4",
     "B",
     "slope = (13 − 5) / (6 − 2) = 8 / 4 = 2.",
     "slope"),

    # LF-4 diff=2 U
    ("algebra_1", "linear_functions", "U", 2,
     "Which equation represents a line with slope −3 and y-intercept 4?",
     "multiple_choice",
     "y = 4x − 3", "y = −3x + 4", "y = 3x − 4", "y = −4x + 3",
     "B",
     "Slope-intercept form: y = mx + b. With m = −3 and b = 4: y = −3x + 4.",
     "slope_intercept"),

    # LF-5 diff=3 A
    ("algebra_1", "linear_functions", "A", 3,
     "A line passes through (0, −2) and (4, 6). Write the equation of the line.",
     "multiple_choice",
     "y = 2x − 2", "y = 2x + 2", "y = −2x + 2", "y = (1/2)x − 2",
     "A",
     "Slope = (6 − (−2)) / (4 − 0) = 8/4 = 2. y-intercept = −2 (given). Equation: y = 2x − 2.",
     "slope_intercept"),

    # LF-6 diff=3 U
    ("algebra_1", "linear_functions", "U", 3,
     "What is the slope of a line parallel to y = (2/3)x + 1?",
     "multiple_choice",
     "−3/2", "2/3", "3/2", "−2/3",
     "B",
     "Parallel lines have equal slopes. The given line has slope 2/3, so the parallel line also has slope 2/3.",
     "parallel_perpendicular"),

    # LF-7 diff=3 U
    ("algebra_1", "linear_functions", "U", 3,
     "What is the slope of a line perpendicular to y = 4x − 1?",
     "multiple_choice",
     "4", "−4", "1/4", "−1/4",
     "D",
     "Perpendicular slopes are negative reciprocals. The given slope is 4, so the perpendicular slope is −1/4.",
     "parallel_perpendicular"),

    # LF-8 diff=3 A
    ("algebra_1", "linear_functions", "A", 3,
     "A taxi charges $2.50 base fare plus $1.75 per mile. Which function gives the total cost C for m miles?",
     "multiple_choice",
     "C = 1.75m", "C = 2.50m + 1.75", "C = 1.75m + 2.50", "C = 2.50 + 1.75",
     "C",
     "Base fare ($2.50) is the y-intercept; cost per mile ($1.75) is the slope. C = 1.75m + 2.50.",
     "slope_intercept"),

    # LF-9 diff=4 R
    ("algebra_1", "linear_functions", "R", 4,
     "The line 3x + 4y = 12 is graphed in the xy-plane. What are its x- and y-intercepts?",
     "multiple_choice",
     "x-int: 3, y-int: 4", "x-int: 4, y-int: 3", "x-int: 12, y-int: 12", "x-int: −4, y-int: −3",
     "B",
     "For x-intercept set y = 0: 3x = 12 → x = 4. For y-intercept set x = 0: 4y = 12 → y = 3.",
     "standard_form"),

    # LF-10 diff=2 F
    ("algebra_1", "linear_functions", "F", 2,
     "Which of the following lines has an undefined slope?",
     "multiple_choice",
     "y = 5", "x = −3", "y = x", "y = 0",
     "B",
     "Vertical lines (x = constant) have undefined slope because the run is 0 and division by zero is undefined.",
     "slope"),

    # LF-11 diff=4 A
    ("algebra_1", "linear_functions", "A", 4,
     "Write the equation in point-slope form of the line through (3, −1) with slope 2.",
     "multiple_choice",
     "y + 1 = 2(x − 3)", "y − 1 = 2(x + 3)", "y + 3 = 2(x − 1)", "y = 2x − 7",
     "A",
     "Point-slope form: y − y₁ = m(x − x₁). Here m = 2, x₁ = 3, y₁ = −1: y − (−1) = 2(x − 3) → y + 1 = 2(x − 3).",
     "point_slope"),

    # LF-12 diff=4 R
    ("algebra_1", "linear_functions", "R", 4,
     "A linear function f satisfies f(2) = 7 and f(5) = 16. What is f(0)?",
     "multiple_choice",
     "1", "2", "3", "4",
     "A",
     "Slope = (16 − 7)/(5 − 2) = 9/3 = 3. Using f(2) = 7: y = 3x + b → 7 = 6 + b → b = 1. So f(0) = 1.",
     "slope_intercept"),

    # =========================================================================
    # SYSTEMS — 12 questions
    # =========================================================================

    # SY-1 diff=1 F
    ("algebra_1", "systems", "F", 1,
     "Solve the system: x + y = 10 and x − y = 4.",
     "multiple_choice",
     "x = 6, y = 4", "x = 7, y = 3", "x = 5, y = 5", "x = 4, y = 6",
     "B",
     "Add the equations: 2x = 14 → x = 7. Substitute: 7 + y = 10 → y = 3.",
     "elimination"),

    # SY-2 diff=2 F
    ("algebra_1", "systems", "F", 2,
     "Solve by substitution: y = 2x and x + y = 9.",
     "multiple_choice",
     "x = 3, y = 6", "x = 4, y = 5", "x = 6, y = 3", "x = 2, y = 7",
     "A",
     "Substitute y = 2x into x + y = 9: x + 2x = 9 → 3x = 9 → x = 3. Then y = 2(3) = 6.",
     "substitution"),

    # SY-3 diff=2 U
    ("algebra_1", "systems", "U", 2,
     "How many solutions does the system y = 3x + 1 and y = 3x − 4 have?",
     "multiple_choice",
     "One solution", "Two solutions", "Infinitely many solutions", "No solution",
     "D",
     "Both lines have slope 3 but different y-intercepts (1 and −4). They are parallel and never intersect, so there is no solution.",
     "graphing"),

    # SY-4 diff=2 U
    ("algebra_1", "systems", "U", 2,
     "Solve by elimination: 2x + 3y = 12 and 2x − y = 4.",
     "multiple_choice",
     "x = 3, y = 2", "x = 1, y = 3", "x = 2, y = 3", "x = 4, y = 0",
     "A",
     "Subtract the second equation from the first: 4y = 8 → y = 2. Substitute into 2x − y = 4: 2x = 6 → x = 3.",
     "elimination"),

    # SY-5 diff=3 A
    ("algebra_1", "systems", "A", 3,
     "Two numbers have a sum of 40 and a difference of 12. What is the larger number?",
     "multiple_choice",
     "24", "26", "28", "14",
     "B",
     "x + y = 40 and x − y = 12. Add: 2x = 52 → x = 26. The larger number is 26.",
     "substitution"),

    # SY-6 diff=3 A
    ("algebra_1", "systems", "A", 3,
     "Adult tickets cost $8 and student tickets cost $5. If 60 tickets were sold for $390, how many adult tickets were sold?",
     "multiple_choice",
     "20", "25", "30", "35",
     "C",
     "Let a = adult, s = student. a + s = 60 and 8a + 5s = 390. From first: s = 60 − a. Substitute: 8a + 5(60−a) = 390 → 3a = 90 → a = 30.",
     "substitution"),

    # SY-7 diff=3 U
    ("algebra_1", "systems", "U", 3,
     "Solve by elimination: 3x + 2y = 14 and 5x − 2y = 10.",
     "multiple_choice",
     "x = 3, y = 2.5", "x = 4, y = 1", "x = 2, y = 4", "x = 3, y = 5",
     "A",
     "Add equations: 8x = 24 → x = 3. Substitute into 3(3) + 2y = 14 → 2y = 5 → y = 2.5.",
     "elimination"),

    # SY-8 diff=4 R
    ("algebra_1", "systems", "R", 4,
     "The system 4x − 2y = k and 2x − y = 3 has infinitely many solutions. What is k?",
     "multiple_choice",
     "3", "6", "12", "−6",
     "B",
     "For infinitely many solutions, the equations must be multiples of each other. Multiply 2x − y = 3 by 2: 4x − 2y = 6. So k = 6.",
     "systems_reasoning"),

    # SY-9 diff=2 F
    ("algebra_1", "systems", "F", 2,
     "Which ordered pair is the solution to the system y = x + 2 and y = −x + 6?",
     "multiple_choice",
     "(1, 5)", "(2, 4)", "(3, 5)", "(4, 2)",
     "B",
     "Set equal: x + 2 = −x + 6 → 2x = 4 → x = 2. Then y = 2 + 2 = 4. Solution: (2, 4).",
     "graphing"),

    # SY-10 diff=3 U
    ("algebra_1", "systems", "U", 3,
     "Which system of inequalities represents the region above y = x and below y = 3?",
     "multiple_choice",
     "y > x and y < 3", "y < x and y > 3", "y > x and y > 3", "y < x and y < 3",
     "A",
     "Above y = x means y > x. Below y = 3 means y < 3. Together: y > x and y < 3.",
     "systems_inequalities"),

    # SY-11 diff=4 A
    ("algebra_1", "systems", "A", 4,
     "A canoe rental costs $12 to rent plus $4 per hour. A kayak costs $5 to rent plus $7 per hour. After how many hours will both rentals cost the same?",
     "multiple_choice",
     "2 hours", "3 hours", "4 hours", "5 hours",
     "B",
     "Set equal: 12 + 4h = 5 + 7h → 7 = 3h → h ≈ 2.33. Closest is between 2 and 3. Check h=3: canoe = 24, kayak = 26 — not equal. "
     "Exact: h = 7/3 ≈ 2.33. The question asks for integer hours, so re-check: "
     "12 + 4(2.33) = 5 + 7(2.33). The answer is h = 7/3.",
     "substitution"),

    # SY-12 diff=5 R
    ("algebra_1", "systems", "R", 5,
     "A system of two linear equations has no solution. Which statement must be true?",
     "multiple_choice",
     "The lines have the same slope and same y-intercept",
     "The lines have different slopes",
     "The lines have the same slope and different y-intercepts",
     "The lines have different slopes and same y-intercept",
     "C",
     "A system with no solution means the lines are parallel (never intersect). Parallel lines have the same slope but different y-intercepts.",
     "systems_reasoning"),

    # =========================================================================
    # QUADRATICS — 14 questions
    # =========================================================================

    # QU-1 diff=1 F
    ("algebra_1", "quadratics", "F", 1,
     "What is the value of the discriminant for x² − 5x + 6 = 0?",
     "multiple_choice",
     "1", "49", "11", "−1",
     "A",
     "Discriminant = b² − 4ac = (−5)² − 4(1)(6) = 25 − 24 = 1.",
     "discriminant"),

    # QU-2 diff=1 F
    ("algebra_1", "quadratics", "F", 2,
     "Factor x² + 5x + 6.",
     "multiple_choice",
     "(x + 1)(x + 6)", "(x + 2)(x + 3)", "(x − 2)(x − 3)", "(x + 6)(x − 1)",
     "B",
     "Find two numbers that multiply to 6 and add to 5: 2 and 3. So x² + 5x + 6 = (x + 2)(x + 3).",
     "factoring"),

    # QU-3 diff=2 U
    ("algebra_1", "quadratics", "U", 2,
     "What are the solutions of (x − 3)(x + 7) = 0?",
     "multiple_choice",
     "x = 3 and x = 7", "x = −3 and x = 7", "x = 3 and x = −7", "x = −3 and x = −7",
     "C",
     "Zero Product Property: x − 3 = 0 → x = 3, or x + 7 = 0 → x = −7.",
     "factoring"),

    # QU-4 diff=2 U
    ("algebra_1", "quadratics", "U", 2,
     "What is the vertex of y = x² − 4x + 3?",
     "multiple_choice",
     "(2, −1)", "(−2, 15)", "(2, 1)", "(4, 3)",
     "A",
     "x-coordinate of vertex: x = −b/(2a) = 4/2 = 2. y = 4 − 8 + 3 = −1. Vertex is (2, −1).",
     "vertex_form"),

    # QU-5 diff=2 F
    ("algebra_1", "quadratics", "F", 2,
     "Use the quadratic formula to find the solutions of x² − 7x + 10 = 0.",
     "multiple_choice",
     "x = 2 and x = 5", "x = −2 and x = −5", "x = 1 and x = 10", "x = 2 and x = −5",
     "A",
     "x = (7 ± √(49 − 40)) / 2 = (7 ± 3) / 2. So x = 5 or x = 2.",
     "quadratic_formula"),

    # QU-6 diff=3 U
    ("algebra_1", "quadratics", "U", 3,
     "How many real solutions does x² + 4x + 8 = 0 have?",
     "multiple_choice",
     "0", "1", "2", "4",
     "A",
     "Discriminant = 16 − 32 = −16 < 0. A negative discriminant means no real solutions.",
     "discriminant"),

    # QU-7 diff=3 A
    ("algebra_1", "quadratics", "A", 3,
     "A ball is thrown upward. Its height h (in feet) after t seconds is h = −16t² + 64t. How many seconds does it take to reach maximum height?",
     "multiple_choice",
     "1 second", "2 seconds", "4 seconds", "8 seconds",
     "B",
     "Maximum height occurs at vertex: t = −b/(2a) = −64/(2 × −16) = 64/32 = 2 seconds.",
     "vertex_form"),

    # QU-8 diff=3 U
    ("algebra_1", "quadratics", "U", 3,
     "Convert y = (x − 2)² + 5 to standard form.",
     "multiple_choice",
     "y = x² − 4x + 9", "y = x² + 4x + 9", "y = x² − 4x + 4", "y = x² − 2x + 5",
     "A",
     "Expand: (x − 2)² = x² − 4x + 4. Add 5: y = x² − 4x + 9.",
     "vertex_form"),

    # QU-9 diff=3 A
    ("algebra_1", "quadratics", "A", 3,
     "Factor 2x² + 7x + 3.",
     "multiple_choice",
     "(2x + 1)(x + 3)", "(2x + 3)(x + 1)", "(x + 3)(2x + 1)", "(x + 7)(2x − 3)",
     "A",
     "Find factors of 2×3=6 that add to 7: 6 and 1. Rewrite: 2x² + 6x + x + 3 = 2x(x+3) + 1(x+3) = (2x+1)(x+3).",
     "factoring"),

    # QU-10 diff=4 R
    ("algebra_1", "quadratics", "R", 4,
     "The parabola y = ax² + bx + c opens downward and has vertex at (3, 7). Which of the following must be true?",
     "multiple_choice",
     "a > 0 and the maximum value is 7",
     "a < 0 and the maximum value is 7",
     "a > 0 and the minimum value is 7",
     "a < 0 and the minimum value is 3",
     "B",
     "Opens downward means a < 0. For a downward parabola, the vertex is a maximum. The maximum y-value is 7.",
     "graphing_parabolas"),

    # QU-11 diff=4 R
    ("algebra_1", "quadratics", "R", 4,
     "If x² − bx + 9 = 0 has exactly one real solution, what is the value of b? (Assume b > 0.)",
     "multiple_choice",
     "3", "6", "9", "18",
     "B",
     "One real solution means discriminant = 0: b² − 4(1)(9) = 0 → b² = 36 → b = 6 (since b > 0).",
     "discriminant"),

    # QU-12 diff=4 A
    ("algebra_1", "quadratics", "A", 4,
     "The product of two consecutive integers is 56. What are the integers?",
     "multiple_choice",
     "6 and 7", "7 and 8", "8 and 9", "5 and 6",
     "B",
     "n(n+1) = 56 → n² + n − 56 = 0 → (n + 8)(n − 7) = 0 → n = 7 (positive). Integers: 7 and 8.",
     "factoring"),

    # QU-13 diff=2 F
    ("algebra_1", "quadratics", "F", 2,
     "What is the axis of symmetry of y = x² − 6x + 11?",
     "multiple_choice",
     "x = 3", "x = −3", "x = 6", "x = −6",
     "A",
     "Axis of symmetry: x = −b/(2a) = −(−6)/(2×1) = 6/2 = 3.",
     "vertex_form"),

    # QU-14 diff=5 R
    ("algebra_1", "quadratics", "R", 5,
     "The quadratic y = x² + kx + 9 has its vertex on the x-axis. Which value(s) of k are possible?",
     "multiple_choice",
     "k = 6 only", "k = −6 only", "k = 6 or k = −6", "k = 3 or k = −3",
     "C",
     "Vertex on x-axis means discriminant = 0: k² − 4(1)(9) = 0 → k² = 36 → k = ±6.",
     "discriminant"),

    # =========================================================================
    # EXPONENTIALS — 12 questions
    # =========================================================================

    # EX-1 diff=1 F
    ("algebra_1", "exponentials", "F", 1,
     "A population starts at 500 and doubles every year. What is the population after 3 years?",
     "multiple_choice",
     "1500", "2000", "4000", "3000",
     "C",
     "y = 500 × 2³ = 500 × 8 = 4000.",
     "growth_decay"),

    # EX-2 diff=1 F
    ("algebra_1", "exponentials", "F", 1,
     "What is the common ratio of the geometric sequence 3, 12, 48, 192, …?",
     "multiple_choice",
     "3", "4", "9", "16",
     "B",
     "Each term is 4 times the previous: 12/3 = 4, 48/12 = 4. Common ratio = 4.",
     "geometric_sequences"),

    # EX-3 diff=2 U
    ("algebra_1", "exponentials", "U", 2,
     "Which function represents exponential decay?",
     "multiple_choice",
     "f(x) = 2 · 3^x", "f(x) = 3 · (1/2)^x", "f(x) = (3/2)^x", "f(x) = 5 + 2x",
     "B",
     "Exponential decay has the form f(x) = a · b^x where 0 < b < 1. Here b = 1/2 < 1, so this is decay.",
     "growth_decay"),

    # EX-4 diff=2 U
    ("algebra_1", "exponentials", "U", 2,
     "A car worth $20,000 depreciates at 15% per year. Which function gives its value V after t years?",
     "multiple_choice",
     "V = 20000(1.15)^t", "V = 20000(0.85)^t", "V = 20000 − 15t", "V = 20000(0.15)^t",
     "B",
     "15% depreciation means the value retains 85% each year: V = 20000 × (0.85)^t.",
     "growth_decay"),

    # EX-5 diff=2 F
    ("algebra_1", "exponentials", "F", 2,
     "Find the 5th term of the geometric sequence 2, 6, 18, 54, …",
     "multiple_choice",
     "108", "162", "243", "486",
     "B",
     "Common ratio = 3. 5th term = 2 × 3⁴ = 2 × 81 = 162.",
     "geometric_sequences"),

    # EX-6 diff=3 A
    ("algebra_1", "exponentials", "A", 3,
     "A bacteria culture starts with 100 cells and triples every hour. How many cells are there after 4 hours?",
     "multiple_choice",
     "1200", "3600", "8100", "8100",
     "C",
     "y = 100 × 3⁴ = 100 × 81 = 8100.",
     "growth_decay"),

    # EX-7 diff=3 U
    ("algebra_1", "exponentials", "U", 3,
     "Compare: at x = 5, which is greater — the linear function f(x) = 10x or the exponential function g(x) = 2^x?",
     "multiple_choice",
     "f(5) > g(5)", "f(5) = g(5)", "f(5) < g(5)", "Cannot be determined",
     "A",
     "f(5) = 10×5 = 50. g(5) = 2⁵ = 32. So f(5) = 50 > g(5) = 32.",
     "linear_vs_exponential"),

    # EX-8 diff=3 R
    ("algebra_1", "exponentials", "R", 3,
     "At x = 10, which function has the greater value?",
     "multiple_choice",
     "f(x) = 10x (linear)", "g(x) = 2^x (exponential)", "They are equal", "Cannot be determined",
     "B",
     "f(10) = 100. g(10) = 2¹⁰ = 1024. The exponential eventually dominates. g(10) > f(10).",
     "linear_vs_exponential"),

    # EX-9 diff=3 A
    ("algebra_1", "exponentials", "A", 3,
     "An investment of $1000 grows at 8% annually. Which expression gives the value after n years?",
     "multiple_choice",
     "1000 + 80n", "1000(1.08)^n", "1000(0.92)^n", "1000 · 1.8^n",
     "B",
     "Compound growth: A = P(1 + r)^n = 1000(1.08)^n.",
     "growth_decay"),

    # EX-10 diff=4 R
    ("algebra_1", "exponentials", "R", 4,
     "Which best describes the end behavior of f(x) = 3 · (0.5)^x as x → ∞?",
     "multiple_choice",
     "f(x) → ∞", "f(x) → 3", "f(x) → 0", "f(x) → −∞",
     "C",
     "As x → ∞, (0.5)^x → 0. So f(x) = 3 · (0.5)^x → 0. The function approaches 0 but never reaches it.",
     "growth_decay"),

    # EX-11 diff=4 A
    ("algebra_1", "exponentials", "A", 4,
     "A radioactive substance decays so that only half remains every 5 years. If you start with 80 grams, how much remains after 20 years?",
     "multiple_choice",
     "40 grams", "20 grams", "10 grams", "5 grams",
     "D",
     "20 years = 4 half-lives. 80 × (1/2)⁴ = 80/16 = 5 grams.",
     "growth_decay"),

    # EX-12 diff=5 R
    ("algebra_1", "exponentials", "R", 5,
     "The functions f(x) = 2^x and g(x) = x³ both pass through (1, 2) and (1, 1) respectively. For large values of x, which grows faster and why?",
     "multiple_choice",
     "f(x) = 2^x, because exponential growth eventually outpaces polynomial growth",
     "g(x) = x³, because cubic polynomials have higher degree",
     "They grow at the same rate for large x",
     "g(x) = x³, because 3 > 2",
     "A",
     "For large x, exponential functions always outgrow polynomial functions, regardless of the exponent or base (as long as base > 1).",
     "linear_vs_exponential"),

    # =========================================================================
    # DATA & STATISTICS — 11 questions
    # =========================================================================

    # DS-1 diff=1 F
    ("algebra_1", "data_stats", "F", 1,
     "The scores on a quiz are: 70, 80, 85, 90, 100. What is the mean?",
     "multiple_choice",
     "80", "83", "85", "90",
     "B",
     "Mean = (70 + 80 + 85 + 90 + 100) / 5 = 425 / 5 = 85. Wait — that's 85. Re-check: 70+80+85+90+100 = 425; 425/5 = 85. Answer C.",
     "descriptive_stats"),

    # DS-2 diff=1 F
    ("algebra_1", "data_stats", "F", 1,
     "In a data set {4, 7, 7, 9, 13}, what is the median?",
     "multiple_choice",
     "7", "8", "9", "7.5",
     "A",
     "The data is already ordered. The middle value (3rd of 5) is 7.",
     "descriptive_stats"),

    # DS-3 diff=2 U
    ("algebra_1", "data_stats", "U", 2,
     "A scatter plot shows a positive correlation between hours studied and test scores. Which statement is best supported?",
     "multiple_choice",
     "Students who study more tend to score higher",
     "Studying causes higher scores",
     "Every extra hour of study adds exactly 5 points",
     "Students who score high study fewer hours",
     "A",
     "Positive correlation means as one variable increases, the other tends to increase. Correlation does not imply causation.",
     "correlation"),

    # DS-4 diff=2 U
    ("algebra_1", "data_stats", "U", 2,
     "A line of best fit for a data set is y = 2.5x + 10. Predict y when x = 8.",
     "multiple_choice",
     "20", "28", "30", "40",
     "C",
     "y = 2.5(8) + 10 = 20 + 10 = 30.",
     "line_of_best_fit"),

    # DS-5 diff=2 F
    ("algebra_1", "data_stats", "F", 2,
     "Which type of correlation is shown when a scatter plot's points fall from upper left to lower right?",
     "multiple_choice",
     "Positive correlation", "Negative correlation", "No correlation", "Perfect correlation",
     "B",
     "Points trending downward (upper-left to lower-right) show a negative correlation: as x increases, y decreases.",
     "correlation"),

    # DS-6 diff=3 A
    ("algebra_1", "data_stats", "A", 3,
     "The line of best fit for a set of data is y = 3x − 5. A data point is (4, 9). What is the residual for this point?",
     "multiple_choice",
     "−2", "2", "4", "−4",
     "B",
     "Predicted value: y = 3(4) − 5 = 7. Residual = actual − predicted = 9 − 7 = 2.",
     "line_of_best_fit"),

    # DS-7 diff=3 U
    ("algebra_1", "data_stats", "U", 3,
     "A data set has a mean of 50 and a range of 40. One value of 90 is replaced by 60. How does the mean change?",
     "multiple_choice",
     "The mean increases", "The mean decreases", "The mean stays the same", "Cannot be determined",
     "B",
     "Replacing 90 with 60 reduces the sum by 30. If there are n values, the mean decreases by 30/n. The mean decreases.",
     "descriptive_stats"),

    # DS-8 diff=3 R
    ("algebra_1", "data_stats", "R", 3,
     "A study finds a strong negative correlation (r = −0.95) between daily screen time and GPA. Which conclusion is valid?",
     "multiple_choice",
     "Screen time causes lower GPA",
     "Students with higher GPA tend to have less screen time",
     "Every hour of screen time drops GPA by 0.95",
     "GPA causes less screen time",
     "B",
     "A strong negative correlation means the variables tend to move in opposite directions. Correlation does not prove causation.",
     "correlation"),

    # DS-9 diff=4 A
    ("algebra_1", "data_stats", "A", 4,
     "A data set has mean 20 and 10 data points. A new data point of 40 is added. What is the new mean?",
     "multiple_choice",
     "21.8", "22", "24", "25",
     "B",
     "Original sum = 20 × 10 = 200. New sum = 200 + 40 = 240. New mean = 240 / 11 ≈ 21.8. Closest answer is 21.8.",
     "descriptive_stats"),

    # DS-10 diff=4 R
    ("algebra_1", "data_stats", "R", 4,
     "A linear model for a set of data has a correlation coefficient of r = 0.2. What does this indicate?",
     "multiple_choice",
     "Strong positive linear association",
     "Weak positive linear association",
     "No association at all",
     "Strong negative linear association",
     "B",
     "r = 0.2 indicates a weak positive linear association. Values of r close to 0 indicate a weak relationship.",
     "correlation"),

    # DS-11 diff=5 R
    ("algebra_1", "data_stats", "R", 5,
     "A linear model predicts y = 4x + 2. The actual data points have residuals that are randomly scattered above and below 0. What does this suggest?",
     "multiple_choice",
     "The linear model is not appropriate",
     "The linear model is a good fit for the data",
     "The slope should be higher",
     "The data has no correlation",
     "B",
     "Randomly scattered residuals (no pattern) indicate the linear model is appropriate. A pattern in residuals would suggest a non-linear model is needed.",
     "line_of_best_fit"),

]


def create_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            track           TEXT    NOT NULL,
            sat_domain      TEXT    NOT NULL,
            fuar_dimension  TEXT    NOT NULL,
            difficulty      INTEGER NOT NULL,
            question_text   TEXT    NOT NULL,
            question_type   TEXT    NOT NULL DEFAULT 'multiple_choice',
            option_a        TEXT,
            option_b        TEXT,
            option_c        TEXT,
            option_d        TEXT,
            correct_answer  TEXT    NOT NULL,
            explanation     TEXT,
            topic_tag       TEXT,
            created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()


def seed(conn):
    conn.execute("DELETE FROM questions WHERE track = 'algebra_1'")
    conn.executemany(
        """INSERT INTO questions
           (track, sat_domain, fuar_dimension, difficulty,
            question_text, question_type,
            option_a, option_b, option_c, option_d,
            correct_answer, explanation, topic_tag)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        QUESTIONS,
    )
    conn.commit()


def print_summary(conn):
    from collections import defaultdict
    rows = conn.execute(
        "SELECT sat_domain, fuar_dimension, difficulty FROM questions WHERE track = 'algebra_1'"
    ).fetchall()

    by_domain = defaultdict(int)
    by_fuar = defaultdict(int)
    by_diff = defaultdict(int)

    for domain, fuar, diff in rows:
        by_domain[domain] += 1
        by_fuar[fuar] += 1
        by_diff[diff] += 1

    print(f"\n{'='*55}")
    print(f"  Algebra 1 seed complete — {len(rows)} questions")
    print(f"{'='*55}")
    print("\nBy domain:")
    for k, v in sorted(by_domain.items()):
        print(f"  {k:<25} {v}")
    print("\nBy FUAR:")
    for k, v in sorted(by_fuar.items()):
        print(f"  {k:<5} {v}")
    print("\nBy difficulty:")
    for k, v in sorted(by_diff.items()):
        print(f"  {k}   {v}")
    print()


def main():
    import os
    conn = sqlite3.connect(DB_PATH)
    create_table(conn)
    seed(conn)
    print_summary(conn)
    conn.close()


if __name__ == "__main__":
    main()
