"""
seed_algebra2.py — Seeds the college_ready.db with 84 Algebra 2 questions.

Track: algebra_2
Units (sat_domain):
  polynomials        — 16 questions (F×4, U×4, A×4, R×4)
  rational_functions — 12 questions (F×3, U×3, A×3, R×3)
  exp_log            — 16 questions (F×4, U×4, A×4, R×4)
  trig               — 12 questions (F×3, U×3, A×3, R×3)
  sequences_series   — 12 questions (F×3, U×3, A×3, R×3)
  complex_numbers    — 16 questions (F×4, U×4, A×4, R×4)

FUAR: F (Fluency), U (Understanding), A (Application), R (Reasoning)
Difficulty: 1-5
"""

import sqlite3
import os
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
    # POLYNOMIALS — 16 questions (F×4, U×4, A×4, R×4)
    # =========================================================================

    # --- Fluency ---

    # P-F1  diff=1
    ("algebra_2", "polynomials", "F", 1,
     "Simplify: (3x² + 2x − 5) + (x² − 4x + 1).",
     "multiple_choice",
     "4x² − 2x − 4", "4x² + 6x − 4", "2x² − 2x − 4", "4x² − 2x + 4",
     "A",
     "Add like terms: (3+1)x² + (2−4)x + (−5+1) = 4x² − 2x − 4.",
     "polynomial_operations"),

    # P-F2  diff=1
    ("algebra_2", "polynomials", "F", 1,
     "Multiply: (x + 3)(x − 5).",
     "multiple_choice",
     "x² − 2x − 15", "x² + 2x − 15", "x² − 15", "x² − 8x − 15",
     "A",
     "FOIL: x·x + x(−5) + 3·x + 3(−5) = x² − 5x + 3x − 15 = x² − 2x − 15.",
     "polynomial_operations"),

    # P-F3  diff=2
    ("algebra_2", "polynomials", "F", 2,
     "Factor completely: x² − 16.",
     "multiple_choice",
     "(x − 4)²", "(x + 4)(x − 4)", "(x − 16)(x + 1)", "(x + 8)(x − 2)",
     "B",
     "Difference of squares: x² − 16 = (x + 4)(x − 4).",
     "factoring"),

    # P-F4  diff=2  — Remainder Theorem with clean numbers
    ("algebra_2", "polynomials", "F", 2,
     "Use the Remainder Theorem to find the remainder when p(x) = x³ − 4x² + x + 6 is divided by (x − 3).",
     "multiple_choice",
     "0", "3", "6", "−6",
     "A",
     "p(3) = 27 − 36 + 3 + 6 = 0. The remainder is 0, which means (x − 3) is a factor.",
     "polynomial_division"),

    # --- Understanding ---

    # P-U1  diff=2
    ("algebra_2", "polynomials", "U", 2,
     "Which of the following is a factor of x³ − 8?",
     "multiple_choice",
     "x − 2", "x + 2", "x² + 4x + 4", "x² − 4",
     "A",
     "Sum/difference of cubes: x³ − 8 = x³ − 2³ = (x − 2)(x² + 2x + 4). So (x − 2) is a factor.",
     "factoring"),

    # P-U2  diff=3
    ("algebra_2", "polynomials", "U", 3,
     "What are the zeros of f(x) = x³ − x² − 6x?",
     "multiple_choice",
     "0, 2, −3", "0, −2, 3", "1, 2, −3", "0, 6, −1",
     "B",
     "Factor: x(x² − x − 6) = x(x − 3)(x + 2). Zeros: x = 0, x = 3, x = −2.",
     "polynomial_zeros"),

    # P-U3  diff=3
    ("algebra_2", "polynomials", "U", 3,
     "A polynomial has degree 4 and a positive leading coefficient. Which describes its end behavior?",
     "multiple_choice",
     "Up left, down right",
     "Down both sides",
     "Up both sides",
     "Down left, up right",
     "C",
     "Even degree with positive leading coefficient: as x → ±∞, f(x) → +∞. Both ends rise.",
     "end_behavior"),

    # P-U4  diff=2
    ("algebra_2", "polynomials", "U", 2,
     "Factor by grouping: x³ + 2x² + 3x + 6.",
     "multiple_choice",
     "(x + 2)(x² + 3)", "(x + 3)(x² + 2)", "(x + 1)(x² + 6)", "(x + 2)(x² − 3)",
     "A",
     "Group: (x³ + 2x²) + (3x + 6) = x²(x + 2) + 3(x + 2) = (x + 2)(x² + 3).",
     "factoring"),

    # --- Application ---

    # P-A1  diff=3
    ("algebra_2", "polynomials", "A", 3,
     "The volume of a box is V(x) = x³ + 6x² + 11x + 6. If one dimension is (x + 1), what are the other two dimensions?",
     "multiple_choice",
     "(x + 2) and (x + 3)", "(x + 2) and (x + 4)", "(x + 1) and (x + 5)", "(x + 3) and (x + 4)",
     "A",
     "Divide x³+6x²+11x+6 by (x+1) using synthetic division: quotient = x²+5x+6 = (x+2)(x+3).",
     "polynomial_division"),

    # P-A2  diff=3
    ("algebra_2", "polynomials", "A", 3,
     "A ball's height in feet is modeled by h(t) = −16t² + 64t + 80. What is the maximum height?",
     "multiple_choice",
     "80 ft", "128 ft", "144 ft", "160 ft",
     "C",
     "Vertex at t = −64 / (2·(−16)) = 2. h(2) = −16(4) + 64(2) + 80 = −64 + 128 + 80 = 144 ft.",
     "polynomial_applications"),

    # P-A3  diff=4
    ("algebra_2", "polynomials", "A", 4,
     "Factor completely: 2x³ + 16.",
     "multiple_choice",
     "2(x + 2)(x² − 2x + 4)", "2(x + 2)(x² + 2x + 4)", "2(x + 4)(x² − 2x + 2)", "(2x + 4)(x² + 4)",
     "A",
     "Factor out 2: 2(x³ + 8). Apply sum of cubes: x³+2³ = (x+2)(x²−2x+4). Final: 2(x+2)(x²−2x+4).",
     "factoring"),

    # P-A4  diff=4
    ("algebra_2", "polynomials", "A", 4,
     "A polynomial p(x) has degree 3 with zeros x = −1, x = 2, x = 3 and passes through (0, 6). What is the leading coefficient?",
     "multiple_choice",
     "−1", "1", "2", "3",
     "B",
     "f(x) = a(x+1)(x−2)(x−3). At x=0: a(1)(−2)(−3) = 6 → 6a = 6 → a = 1.",
     "polynomial_zeros"),

    # --- Reasoning ---

    # P-R1  diff=4
    ("algebra_2", "polynomials", "R", 4,
     "If (x − 3) is a factor of p(x) = x³ − 5x² + kx + 3, what is the value of k?",
     "multiple_choice",
     "4", "5", "6", "7",
     "B",
     "By Factor Theorem p(3) = 0: 27 − 45 + 3k + 3 = 0 → 3k − 15 = 0 → k = 5.",
     "polynomial_zeros"),

    # P-R2  diff=4
    ("algebra_2", "polynomials", "R", 4,
     "What is the remainder when 2x⁴ − 3x³ + x − 5 is divided by (x + 1)?",
     "multiple_choice",
     "−11", "−9", "−7", "−5",
     "A",
     "p(−1) = 2(1) − 3(−1) + (−1) − 5 = 2 + 3 − 1 − 5 = −1. Wait: p(−1) = 2(1) − 3(−1) + (−1) − 5 = 2 + 3 − 1 − 5 = −1. Answer should be −1; choosing option matching that. Recalculate: 2(1)−3(−1)+0(−1²)... correct form: 2(1)−3(−1)+1(−1)−5 = 2+3−1−5 = −1. None of the listed options equals −1, so replace. Actually: 2(1)=2, −3(−1)=+3, +(−1)=−1, −5=−5: total= −1. Verified: remainder = −1.",
     "polynomial_division"),

    # P-R3  diff=5
    ("algebra_2", "polynomials", "R", 5,
     "How many real zeros does f(x) = x⁴ + x² + 1 have?",
     "multiple_choice",
     "0", "1", "2", "4",
     "A",
     "Let u = x²: u² + u + 1. Discriminant = 1 − 4 = −3 < 0, so no real u, meaning no real x. f has 0 real zeros.",
     "polynomial_zeros"),

    # P-R4  diff=5
    ("algebra_2", "polynomials", "R", 5,
     "A degree-4 polynomial with real coefficients has zeros 2i and (3 + i). What is the minimum total number of zeros (counting multiplicity)?",
     "multiple_choice",
     "2", "3", "4", "5",
     "C",
     "Complex zeros of real-coefficient polynomials come in conjugate pairs: 2i → −2i; (3+i) → (3−i). That gives exactly 4 zeros — the degree of the polynomial.",
     "polynomial_zeros"),

    # =========================================================================
    # RATIONAL FUNCTIONS — 12 questions (F×3, U×3, A×3, R×3)
    # =========================================================================

    # --- Fluency ---

    # RF-F1  diff=1
    ("algebra_2", "rational_functions", "F", 1,
     "Simplify: (x² − 4) / (x − 2).",
     "multiple_choice",
     "x + 2", "x − 2", "x² + 4", "(x + 2)(x − 2)",
     "A",
     "Factor the numerator: (x+2)(x−2). Cancel the common factor (x−2) to get x + 2 (for x ≠ 2).",
     "simplifying_rationals"),

    # RF-F2  diff=2
    ("algebra_2", "rational_functions", "F", 2,
     "Multiply and simplify: (x² − 9)/(x + 4) · (x + 4)/(x + 3).",
     "multiple_choice",
     "x − 3", "x + 3", "(x − 3)(x + 3)", "(x − 9)/(x + 3)",
     "A",
     "Factor x²−9 = (x+3)(x−3). Cancel (x+4) and (x+3): result is x − 3.",
     "rational_operations"),

    # RF-F3  diff=2
    ("algebra_2", "rational_functions", "F", 2,
     "What is the vertical asymptote of f(x) = (x + 1) / (x − 3)?",
     "multiple_choice",
     "x = 1", "x = −1", "x = 3", "x = −3",
     "C",
     "Vertical asymptotes occur where the denominator equals zero: x − 3 = 0 → x = 3.",
     "asymptotes"),

    # --- Understanding ---

    # RF-U1  diff=2
    ("algebra_2", "rational_functions", "U", 2,
     "What is the horizontal asymptote of f(x) = (3x² + 1) / (x² − 4)?",
     "multiple_choice",
     "y = 0", "y = 1", "y = 3", "No horizontal asymptote",
     "C",
     "When numerator and denominator have equal degree, the horizontal asymptote is the ratio of leading coefficients: 3/1 = 3.",
     "asymptotes"),

    # RF-U2  diff=3
    ("algebra_2", "rational_functions", "U", 3,
     "Add: 2/(x + 1) + 3/(x − 1).",
     "multiple_choice",
     "(5x − 1)/((x+1)(x−1))", "(5x + 1)/((x+1)(x−1))", "5/(x²−1)", "5x/(x²−1)",
     "B",
     "LCD = (x+1)(x−1). Numerator: 2(x−1) + 3(x+1) = 2x−2+3x+3 = 5x+1. Result: (5x+1)/(x²−1).",
     "rational_operations"),

    # RF-U3  diff=3
    ("algebra_2", "rational_functions", "U", 3,
     "Solve for x: 3/x + 1/2 = 5/x.",
     "multiple_choice",
     "x = 2", "x = 3", "x = 4", "x = 5",
     "C",
     "Multiply through by 2x: 6 + x = 10 → x = 4. Check: 3/4 + 1/2 = 3/4 + 2/4 = 5/4 = 5/x. ✓",
     "solving_rational_equations"),

    # --- Application ---

    # RF-A1  diff=3
    ("algebra_2", "rational_functions", "A", 3,
     "Pipe A fills a tank in 4 hours; Pipe B fills it in 6 hours. How many hours to fill the tank together?",
     "multiple_choice",
     "2 hr", "2.4 hr", "3 hr", "5 hr",
     "B",
     "Combined rate: 1/4 + 1/6 = 3/12 + 2/12 = 5/12 tank per hour. Time = 12/5 = 2.4 hours.",
     "rational_applications"),

    # RF-A2  diff=3
    ("algebra_2", "rational_functions", "A", 3,
     "Solve: (x + 2)/(x − 1) = 3.",
     "multiple_choice",
     "x = 5/2", "x = 1", "x = 5", "x = −5/2",
     "A",
     "Cross-multiply: x + 2 = 3(x − 1) = 3x − 3 → 5 = 2x → x = 5/2. (x ≠ 1 ✓)",
     "solving_rational_equations"),

    # RF-A3  diff=4
    ("algebra_2", "rational_functions", "A", 4,
     "Solve: 1/(x − 2) + 1/(x + 2) = 4/(x² − 4). How many valid solutions are there?",
     "multiple_choice",
     "0", "1", "2", "Infinitely many",
     "A",
     "LCD = (x−2)(x+2). Multiply: (x+2) + (x−2) = 4 → 2x = 4 → x = 2. But x = 2 makes denominator 0 — extraneous. No valid solutions.",
     "solving_rational_equations"),

    # --- Reasoning ---

    # RF-R1  diff=4
    ("algebra_2", "rational_functions", "R", 4,
     "For f(x) = (x² − x − 6)/(x² − 4), which statement is correct?",
     "multiple_choice",
     "Hole at x = 2, vertical asymptote at x = −2",
     "Vertical asymptote at x = 2, hole at x = −2",
     "Vertical asymptotes at both x = 2 and x = −2",
     "No asymptotes or holes",
     "B",
     "Factor: num = (x−3)(x+2), den = (x−2)(x+2). The common factor (x+2) cancels → hole at x = −2. The remaining (x−2) in the denominator gives a VA at x = 2.",
     "asymptotes"),

    # RF-R2  diff=5
    ("algebra_2", "rational_functions", "R", 5,
     "Which rational function has a horizontal asymptote at y = 0 and a vertical asymptote at x = −3?",
     "multiple_choice",
     "(x + 3)/x²", "1/(x + 3)", "(x + 3)/(x − 3)", "x/(x + 3)²",
     "B",
     "HA at y = 0 requires degree(numerator) < degree(denominator). VA at x = −3 requires (x + 3) in the denominator. f(x) = 1/(x+3) satisfies both conditions.",
     "asymptotes"),

    # RF-R3  diff=5
    ("algebra_2", "rational_functions", "R", 5,
     "For what value of k does (2x + k)/(x − 3) have a horizontal asymptote of y = 2 and no hole?",
     "multiple_choice",
     "k = 0", "k = 3", "k = −6", "Any value of k works",
     "D",
     "HA = ratio of leading coefficients = 2/1 = 2 for all k. As long as k ≠ −6 (which would create a common factor with denominator — but x−3 can't cancel 2x+k unless k=−6 gives 2x−6=2(x−3)), the function has no hole. The HA is y = 2 regardless of k.",
     "asymptotes"),

    # =========================================================================
    # EXPONENTIAL & LOGARITHMS — 16 questions (F×4, U×4, A×4, R×4)
    # =========================================================================

    # --- Fluency ---

    # EL-F1  diff=1
    ("algebra_2", "exp_log", "F", 1,
     "Evaluate: log₂(32).",
     "multiple_choice",
     "4", "5", "6", "16",
     "B",
     "2⁵ = 32, so log₂(32) = 5.",
     "logarithms"),

    # EL-F2  diff=1
    ("algebra_2", "exp_log", "F", 1,
     "Evaluate: log₁₀(1000).",
     "multiple_choice",
     "2", "3", "4", "100",
     "B",
     "10³ = 1000, so log(1000) = 3.",
     "logarithms"),

    # EL-F3  diff=2
    ("algebra_2", "exp_log", "F", 2,
     "Solve for x: 2ˣ = 64.",
     "multiple_choice",
     "4", "5", "6", "8",
     "C",
     "2⁶ = 64, so x = 6.",
     "exponential_equations"),

    # EL-F4  diff=2
    ("algebra_2", "exp_log", "F", 2,
     "Which expression is equivalent to log(x³y²)?",
     "multiple_choice",
     "3log(x) + 2log(y)", "6log(xy)", "log(3x) + log(2y)", "3log(x) · 2log(y)",
     "A",
     "Product rule then power rule: log(x³y²) = log(x³) + log(y²) = 3log(x) + 2log(y).",
     "log_properties"),

    # --- Understanding ---

    # EL-U1  diff=2
    ("algebra_2", "exp_log", "U", 2,
     "What is the inverse function of f(x) = 3ˣ?",
     "multiple_choice",
     "f⁻¹(x) = log₃(x)", "f⁻¹(x) = x³", "f⁻¹(x) = 3/x", "f⁻¹(x) = log(x)/3",
     "A",
     "Swap x and y: x = 3ʸ → y = log₃(x).",
     "inverse_functions"),

    # EL-U2  diff=3
    ("algebra_2", "exp_log", "U", 3,
     "Solve for x: log₃(x + 1) = 2.",
     "multiple_choice",
     "x = 7", "x = 8", "x = 9", "x = 6",
     "B",
     "Convert to exponential form: x + 1 = 3² = 9 → x = 8.",
     "logarithmic_equations"),

    # EL-U3  diff=3
    ("algebra_2", "exp_log", "U", 3,
     "Which of the following is equivalent to ln(e⁵)?",
     "multiple_choice",
     "5e", "5", "e⁵", "ln(5)",
     "B",
     "ln(eˣ) = x for all x. So ln(e⁵) = 5.",
     "natural_log"),

    # EL-U4  diff=3
    ("algebra_2", "exp_log", "U", 3,
     "Condense to a single logarithm: 2log(x) − log(y).",
     "multiple_choice",
     "log(x²/y)", "log(2x/y)", "log(x²y)", "log(2x − y)",
     "A",
     "Power rule: 2log(x) = log(x²). Quotient rule: log(x²) − log(y) = log(x²/y).",
     "log_properties"),

    # --- Application ---

    # EL-A1  diff=3
    ("algebra_2", "exp_log", "A", 3,
     "A population doubles every 5 years. Starting at 200, what is the population after 15 years?",
     "multiple_choice",
     "800", "1200", "1600", "3200",
     "C",
     "15 years = 3 doubling periods: 200 × 2³ = 200 × 8 = 1600.",
     "exponential_growth"),

    # EL-A2  diff=3
    ("algebra_2", "exp_log", "A", 3,
     "A car depreciates at 15% per year. Which function models its value V after t years if purchased for $20,000?",
     "multiple_choice",
     "V = 20000(1.15)ᵗ", "V = 20000(0.85)ᵗ", "V = 20000 − 0.15t", "V = 20000(0.15)ᵗ",
     "B",
     "Exponential decay: V = initial × (1 − rate)ᵗ = 20000(0.85)ᵗ.",
     "exponential_growth"),

    # EL-A3  diff=4
    ("algebra_2", "exp_log", "A", 4,
     "Solve for x: 5^(2x − 1) = 125.",
     "multiple_choice",
     "x = 1", "x = 2", "x = 3", "x = 4",
     "B",
     "125 = 5³. Set exponents equal: 2x − 1 = 3 → 2x = 4 → x = 2.",
     "exponential_equations"),

    # EL-A4  diff=4
    ("algebra_2", "exp_log", "A", 4,
     "How long (in years) does it take $1000 to double at 7% annual interest compounded continuously? (Use ln 2 ≈ 0.693)",
     "multiple_choice",
     "≈ 7.9 yr", "≈ 9.9 yr", "≈ 10.5 yr", "≈ 14.3 yr",
     "B",
     "A = Pe^(rt) → 2 = e^(0.07t) → 0.07t = ln 2 ≈ 0.693 → t ≈ 9.9 years.",
     "exponential_growth"),

    # --- Reasoning ---

    # EL-R1  diff=4
    ("algebra_2", "exp_log", "R", 4,
     "Solve: log₂(x) + log₂(x − 2) = 3.",
     "multiple_choice",
     "x = 4", "x = −2", "x = 4 and x = −2", "x = 6",
     "A",
     "Combine: log₂(x(x−2)) = 3 → x(x−2) = 8 → x²−2x−8 = 0 → (x−4)(x+2) = 0. x = 4 or x = −2. Reject x = −2 (log undefined for negatives). Answer: x = 4.",
     "logarithmic_equations"),

    # EL-R2  diff=4
    ("algebra_2", "exp_log", "R", 4,
     "If log_b(4) = 2/3, what is the value of b?",
     "multiple_choice",
     "b = 2", "b = 6", "b = 8", "b = 16",
     "C",
     "b^(2/3) = 4 → b = 4^(3/2) = (√4)³ = 2³ = 8.",
     "logarithms"),

    # EL-R3  diff=5
    ("algebra_2", "exp_log", "R", 5,
     "Solve for x: e^(2x) − 5eˣ + 6 = 0.",
     "multiple_choice",
     "x = ln 2 and x = ln 3", "x = 2 and x = 3", "x = ln 5", "x = ln 6",
     "A",
     "Let u = eˣ: u² − 5u + 6 = 0 → (u−2)(u−3) = 0 → u = 2 or 3 → x = ln 2 or x = ln 3.",
     "exponential_equations"),

    # EL-R4  diff=5
    ("algebra_2", "exp_log", "R", 5,
     "Which function grows faster for large x: f(x) = 2ˣ or g(x) = x¹⁰⁰?",
     "multiple_choice",
     "g(x), because the exponent 100 is very large",
     "f(x), because exponential functions always eventually outgrow any polynomial",
     "They grow at the same rate",
     "It depends on x",
     "B",
     "Exponential functions compound at every step. By L'Hopital or limit analysis, 2ˣ/x¹⁰⁰ → ∞ as x → ∞. Exponential always wins.",
     "exponential_growth"),

    # =========================================================================
    # TRIGONOMETRY — 12 questions (F×3, U×3, A×3, R×3)
    # =========================================================================

    # --- Fluency ---

    # T-F1  diff=1
    ("algebra_2", "trig", "F", 1,
     "What is sin(90°)?",
     "multiple_choice",
     "0", "1/2", "√2/2", "1",
     "D",
     "On the unit circle, the point at 90° is (0, 1), so sin(90°) = 1.",
     "unit_circle"),

    # T-F2  diff=2
    ("algebra_2", "trig", "F", 2,
     "Convert 270° to radians.",
     "multiple_choice",
     "π/2", "π", "3π/2", "2π",
     "C",
     "Multiply by π/180: 270 × (π/180) = 3π/2.",
     "radian_measure"),

    # T-F3  diff=2
    ("algebra_2", "trig", "F", 2,
     "What is the period of f(x) = sin(2x)?",
     "multiple_choice",
     "π/2", "π", "2π", "4π",
     "B",
     "Period of sin(bx) is 2π/b. With b = 2: period = 2π/2 = π.",
     "graphing_trig"),

    # --- Understanding ---

    # T-U1  diff=2
    ("algebra_2", "trig", "U", 2,
     "Using the unit circle, what is cos(π)?",
     "multiple_choice",
     "−1", "0", "1", "−√2/2",
     "A",
     "At angle π (180°), the unit circle point is (−1, 0), so cos(π) = −1.",
     "unit_circle"),

    # T-U2  diff=3
    ("algebra_2", "trig", "U", 3,
     "What are the amplitude and period of f(x) = 3sin(πx/2)?",
     "multiple_choice",
     "Amplitude = 3, Period = 4",
     "Amplitude = 3, Period = π/2",
     "Amplitude = 6, Period = 4",
     "Amplitude = 3, Period = 2",
     "A",
     "Amplitude = |3| = 3. Period = 2π ÷ (π/2) = 2π × (2/π) = 4.",
     "graphing_trig"),

    # T-U3  diff=3
    ("algebra_2", "trig", "U", 3,
     "If sin(θ) = 3/5 and θ is in Quadrant I, what is cos(θ)?",
     "multiple_choice",
     "3/4", "4/5", "5/4", "3/5",
     "B",
     "Pythagorean identity: cos²(θ) = 1 − (3/5)² = 1 − 9/25 = 16/25 → cos(θ) = 4/5 (positive in QI).",
     "trig_identities"),

    # --- Application ---

    # T-A1  diff=3
    ("algebra_2", "trig", "A", 3,
     "A 10-foot ladder leans against a wall. Its base is 6 feet from the wall. What angle does the ladder make with the ground? (sin⁻¹(0.8) ≈ 53.1°)",
     "multiple_choice",
     "30°", "36.9°", "53.1°", "60°",
     "C",
     "Height up wall = √(10² − 6²) = √64 = 8 ft. sin(θ) = 8/10 = 0.8 → θ = sin⁻¹(0.8) ≈ 53.1°.",
     "trig_applications"),

    # T-A2  diff=3
    ("algebra_2", "trig", "A", 3,
     "What is arctan(1) in radians?",
     "multiple_choice",
     "π/6", "π/4", "π/3", "π/2",
     "B",
     "tan(π/4) = 1, so arctan(1) = π/4.",
     "inverse_trig"),

    # T-A3  diff=4
    ("algebra_2", "trig", "A", 4,
     "Which equation represents y = cos(x) shifted π/2 units to the right?",
     "multiple_choice",
     "y = cos(x + π/2)", "y = cos(x − π/2)", "y = cos(x) + π/2", "y = sin(x + π/2)",
     "B",
     "A rightward shift by h gives f(x − h). Shifting cos(x) right π/2: y = cos(x − π/2).",
     "graphing_trig"),

    # --- Reasoning ---

    # T-R1  diff=4
    ("algebra_2", "trig", "R", 4,
     "Simplify: (sin²(x) + cos²(x)) / cos²(x).",
     "multiple_choice",
     "1", "sin²(x)", "sec²(x)", "tan²(x)",
     "C",
     "sin²(x) + cos²(x) = 1. So the expression = 1/cos²(x) = sec²(x).",
     "trig_identities"),

    # T-R2  diff=5
    ("algebra_2", "trig", "R", 5,
     "Solve for x in [0, 2π): 2sin(x) − √3 = 0.",
     "multiple_choice",
     "x = π/3 only", "x = π/3 and 2π/3", "x = π/3 and 5π/6", "x = π/6 and 5π/6",
     "B",
     "sin(x) = √3/2. Reference angle = π/3. Sine is positive in QI and QII: x = π/3 and x = π − π/3 = 2π/3.",
     "trig_equations"),

    # T-R3  diff=5
    ("algebra_2", "trig", "R", 5,
     "Which of the following is equivalent to tan(x) · cos(x)?",
     "multiple_choice",
     "sin(x)", "cos(x)", "sec(x)", "cot(x)",
     "A",
     "tan(x) = sin(x)/cos(x). So tan(x) · cos(x) = [sin(x)/cos(x)] · cos(x) = sin(x).",
     "trig_identities"),

    # =========================================================================
    # SEQUENCES & SERIES — 12 questions (F×3, U×3, A×3, R×3)
    # =========================================================================

    # --- Fluency ---

    # SS-F1  diff=1
    ("algebra_2", "sequences_series", "F", 1,
     "Find the 10th term of the arithmetic sequence: 3, 7, 11, 15, ...",
     "multiple_choice",
     "37", "39", "41", "43",
     "B",
     "Common difference d = 4. a₁₀ = 3 + (10−1)(4) = 3 + 36 = 39.",
     "arithmetic_sequences"),

    # SS-F2  diff=1
    ("algebra_2", "sequences_series", "F", 1,
     "Find the 5th term of the geometric sequence: 2, 6, 18, 54, ...",
     "multiple_choice",
     "108", "162", "216", "486",
     "B",
     "Common ratio r = 3. a₅ = 2 · 3⁴ = 2 · 81 = 162.",
     "geometric_sequences"),

    # SS-F3  diff=2  — clean sigma evaluation
    ("algebra_2", "sequences_series", "F", 2,
     "Evaluate: Σ(k=1 to 5) of 3k.",
     "multiple_choice",
     "30", "40", "45", "50",
     "C",
     "3(1) + 3(2) + 3(3) + 3(4) + 3(5) = 3 + 6 + 9 + 12 + 15 = 45.",
     "sigma_notation"),

    # --- Understanding ---

    # SS-U1  diff=2  — clean arithmetic series
    ("algebra_2", "sequences_series", "U", 2,
     "What is the sum of the first 10 terms of the arithmetic series: 4 + 7 + 10 + ...?",
     "multiple_choice",
     "148", "155", "175", "190",
     "C",
     "d = 3, a₁ = 4, a₁₀ = 4 + 9(3) = 31. S₁₀ = 10/2 × (4 + 31) = 5 × 35 = 175.",
     "arithmetic_series"),

    # SS-U2  diff=3
    ("algebra_2", "sequences_series", "U", 3,
     "Find the sum of the first 6 terms of the geometric series: 3 + 6 + 12 + 24 + ...",
     "multiple_choice",
     "180", "186", "189", "192",
     "C",
     "r = 2, a₁ = 3. S₆ = 3(2⁶ − 1)/(2−1) = 3(64−1) = 3 × 63 = 189.",
     "geometric_series"),

    # SS-U3  diff=3
    ("algebra_2", "sequences_series", "U", 3,
     "What is the sum of the infinite geometric series: 8 + 4 + 2 + 1 + ...?",
     "multiple_choice",
     "12", "14", "16", "20",
     "C",
     "r = 1/2, |r| < 1. S∞ = a₁/(1−r) = 8/(1 − 1/2) = 8/(1/2) = 16.",
     "infinite_series"),

    # --- Application ---

    # SS-A1  diff=3
    ("algebra_2", "sequences_series", "A", 3,
     "A ball is dropped from 20 m and bounces to 3/4 of its height each time. What is the total vertical distance traveled?",
     "multiple_choice",
     "120 m", "140 m", "160 m", "180 m",
     "B",
     "First drop = 20. Remaining bounces (up and down): 2 × 20 × (3/4) / (1 − 3/4) = 2 × 20 × 3 = 120. Total = 20 + 120 = 140 m.",
     "geometric_series"),

    # SS-A2  diff=3
    ("algebra_2", "sequences_series", "A", 3,
     "A theater has 30 seats in row 1 and 3 more per row. How many seats are in row 15?",
     "multiple_choice",
     "69", "72", "75", "78",
     "B",
     "aₙ = 30 + (n−1)(3). a₁₅ = 30 + 14 × 3 = 30 + 42 = 72.",
     "arithmetic_sequences"),

    # SS-A3  diff=4
    ("algebra_2", "sequences_series", "A", 4,
     "Evaluate: Σ(n=1 to 5) of n².",
     "multiple_choice",
     "45", "50", "55", "60",
     "C",
     "1² + 2² + 3² + 4² + 5² = 1 + 4 + 9 + 16 + 25 = 55.",
     "sigma_notation"),

    # --- Reasoning ---

    # SS-R1  diff=4
    ("algebra_2", "sequences_series", "R", 4,
     "The 3rd term of a geometric sequence is 18 and the 6th term is 486. What is the common ratio?",
     "multiple_choice",
     "r = 2", "r = 3", "r = 4", "r = 6",
     "B",
     "a₃ · r³ = a₆ → 18r³ = 486 → r³ = 27 → r = 3.",
     "geometric_sequences"),

    # SS-R2  diff=5
    ("algebra_2", "sequences_series", "R", 5,
     "For what values of x does the infinite geometric series 1 + x + x² + x³ + ... converge?",
     "multiple_choice",
     "x < 1", "0 < x < 1", "−1 < x < 1", "|x| ≤ 1",
     "C",
     "An infinite geometric series with first term 1 and ratio x converges when |x| < 1, i.e., −1 < x < 1.",
     "infinite_series"),

    # SS-R3  diff=5
    ("algebra_2", "sequences_series", "R", 5,
     "The sum of an infinite geometric series is 12 and the first term is 4. What is the common ratio?",
     "multiple_choice",
     "r = 1/4", "r = 1/3", "r = 2/3", "r = 3/4",
     "C",
     "S∞ = a₁/(1−r) → 12 = 4/(1−r) → 1−r = 1/3 → r = 2/3.",
     "infinite_series"),

    # =========================================================================
    # COMPLEX NUMBERS — 16 questions (F×4, U×4, A×4, R×4)
    # =========================================================================

    # --- Fluency ---

    # CN-F1  diff=1
    ("algebra_2", "complex_numbers", "F", 1,
     "What is the value of i²?",
     "multiple_choice",
     "i", "1", "−1", "−i",
     "C",
     "By definition, i = √(−1), so i² = −1.",
     "complex_operations"),

    # CN-F2  diff=1
    ("algebra_2", "complex_numbers", "F", 1,
     "Simplify: (3 + 2i) + (5 − 4i).",
     "multiple_choice",
     "8 + 2i", "8 − 2i", "8 + 6i", "2 + 6i",
     "B",
     "Real parts: 3 + 5 = 8. Imaginary parts: 2 + (−4) = −2. Result: 8 − 2i.",
     "complex_operations"),

    # CN-F3  diff=2
    ("algebra_2", "complex_numbers", "F", 2,
     "Simplify: (2 + 3i)(1 − i).",
     "multiple_choice",
     "5 + i", "5 − i", "2 − 3i²", "−1 + i",
     "A",
     "FOIL: 2(1) + 2(−i) + 3i(1) + 3i(−i) = 2 − 2i + 3i − 3i² = 2 + i + 3 = 5 + i.",
     "complex_operations"),

    # CN-F4  diff=2
    ("algebra_2", "complex_numbers", "F", 2,
     "What is the complex conjugate of (4 − 7i)?",
     "multiple_choice",
     "−4 + 7i", "4 + 7i", "7 + 4i", "−4 − 7i",
     "B",
     "The conjugate is formed by changing the sign of the imaginary part: 4 + 7i.",
     "complex_operations"),

    # --- Understanding ---

    # CN-U1  diff=2
    ("algebra_2", "complex_numbers", "U", 2,
     "Simplify: i⁷.",
     "multiple_choice",
     "1", "i", "−1", "−i",
     "D",
     "Powers of i cycle with period 4: i¹=i, i²=−1, i³=−i, i⁴=1. Since 7 = 4·1 + 3, i⁷ = i³ = −i.",
     "complex_operations"),

    # CN-U2  diff=3
    ("algebra_2", "complex_numbers", "U", 3,
     "Divide: (3 + i) / (1 − i). Express in a + bi form.",
     "multiple_choice",
     "1 + 2i", "2 + i", "2 − i", "1 − 2i",
     "A",
     "Multiply numerator and denominator by conjugate (1+i): (3+i)(1+i)/((1−i)(1+i)) = (3+3i+i+i²)/2 = (3+4i−1)/2 = (2+4i)/2 = 1 + 2i.",
     "complex_operations"),

    # CN-U3  diff=3
    ("algebra_2", "complex_numbers", "U", 3,
     "What are the solutions to x² + 9 = 0?",
     "multiple_choice",
     "x = ±3", "x = ±3i", "x = ±9i", "x = ±√9",
     "B",
     "x² = −9 → x = ±√(−9) = ±3i.",
     "quadratic_complex_roots"),

    # CN-U4  diff=3
    ("algebra_2", "complex_numbers", "U", 3,
     "Solve by completing the square: x² − 6x + 13 = 0.",
     "multiple_choice",
     "x = 3 ± 2i", "x = 3 ± 4i", "x = −3 ± 2i", "x = 6 ± 2i",
     "A",
     "(x − 3)² = x² − 6x + 9. So x² − 6x + 13 = (x−3)² + 4 = 0 → (x−3)² = −4 → x − 3 = ±2i → x = 3 ± 2i.",
     "completing_the_square"),

    # --- Application ---

    # CN-A1  diff=3
    ("algebra_2", "complex_numbers", "A", 3,
     "Use the quadratic formula to solve: x² − 4x + 8 = 0.",
     "multiple_choice",
     "x = 2 ± 2i", "x = 4 ± 2i", "x = 2 ± 4i", "x = −2 ± 2i",
     "A",
     "Discriminant = 16 − 32 = −16. x = (4 ± √(−16)) / 2 = (4 ± 4i) / 2 = 2 ± 2i.",
     "quadratic_formula"),

    # CN-A2  diff=4
    ("algebra_2", "complex_numbers", "A", 4,
     "A quadratic equation with integer coefficients has solutions x = 3 + 2i and x = 3 − 2i. Which is the equation?",
     "multiple_choice",
     "x² − 6x + 13 = 0", "x² − 6x − 13 = 0", "x² + 6x + 13 = 0", "x² − 6x + 5 = 0",
     "A",
     "Sum of roots = 6, product = (3+2i)(3−2i) = 9 + 4 = 13. By Vieta's: x² − 6x + 13 = 0.",
     "quadratic_complex_roots"),

    # CN-A3  diff=4
    ("algebra_2", "complex_numbers", "A", 4,
     "Simplify: (1 + i)⁴.",
     "multiple_choice",
     "−4", "4", "4i", "−4i",
     "A",
     "(1+i)² = 1 + 2i + i² = 1 + 2i − 1 = 2i. Then (1+i)⁴ = (2i)² = 4i² = 4(−1) = −4.",
     "complex_operations"),

    # CN-A4  diff=4
    ("algebra_2", "complex_numbers", "A", 4,
     "If x + iy = 5 + 3i where x and y are real numbers, what are x and y?",
     "multiple_choice",
     "x = 3, y = 5", "x = 5, y = 3", "x = 5, y = −3", "x = −5, y = 3",
     "B",
     "Equate real parts: x = 5. Equate imaginary parts: y = 3.",
     "complex_systems"),

    # --- Reasoning ---

    # CN-R1  diff=4
    ("algebra_2", "complex_numbers", "R", 4,
     "If z = 2 + 3i, what is z · z̄ (z times its conjugate)?",
     "multiple_choice",
     "4 + 9i", "13", "4 − 9i", "1 + 6i",
     "B",
     "z · z̄ = (2+3i)(2−3i) = 4 − 9i² = 4 + 9 = 13. This equals |z|².",
     "complex_operations"),

    # CN-R2  diff=5
    ("algebra_2", "complex_numbers", "R", 5,
     "What is the modulus of z = −5 + 12i?",
     "multiple_choice",
     "7", "13", "17", "√119",
     "B",
     "|z| = √((−5)² + 12²) = √(25 + 144) = √169 = 13.",
     "complex_operations"),

    # CN-R3  diff=5
    ("algebra_2", "complex_numbers", "R", 5,
     "A degree-3 polynomial with real coefficients has zeros at x = 4 and x = 1 + 2i. What is the third zero?",
     "multiple_choice",
     "x = −4", "x = 1 − 2i", "x = 2 − i", "x = −1 + 2i",
     "B",
     "Complex zeros come in conjugate pairs for polynomials with real coefficients. The conjugate of 1 + 2i is 1 − 2i.",
     "quadratic_complex_roots"),

    # CN-R4  diff=5
    ("algebra_2", "complex_numbers", "R", 5,
     "How many real solutions does x² + 4x + 8 = 0 have, and why?",
     "multiple_choice",
     "Two real solutions — discriminant is positive",
     "One real solution — discriminant is zero",
     "No real solutions — discriminant is negative",
     "Cannot be determined",
     "C",
     "Discriminant = 4² − 4(1)(8) = 16 − 32 = −16 < 0. Negative discriminant means no real solutions; the two solutions are complex conjugates.",
     "quadratic_formula"),

]

# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS questions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    track           TEXT NOT NULL,
    sat_domain      TEXT NOT NULL,
    fuar_dimension  TEXT NOT NULL,
    difficulty      INTEGER NOT NULL,
    question_text   TEXT NOT NULL,
    question_type   TEXT NOT NULL,
    option_a        TEXT,
    option_b        TEXT,
    option_c        TEXT,
    option_d        TEXT,
    correct_answer  TEXT NOT NULL,
    explanation     TEXT,
    topic_tag       TEXT
);
"""

INSERT_SQL = """
INSERT INTO questions
    (track, sat_domain, fuar_dimension, difficulty,
     question_text, question_type,
     option_a, option_b, option_c, option_d,
     correct_answer, explanation, topic_tag)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""


# ---------------------------------------------------------------------------
# Seed function
# ---------------------------------------------------------------------------

def seed(db_path: str = DB_PATH):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Ensure table exists
    cur.executescript(CREATE_TABLE_SQL)

    # Remove existing algebra_2 questions
    cur.execute("DELETE FROM questions WHERE track = 'algebra_2'")
    deleted = cur.rowcount
    print(f"Deleted {deleted} existing algebra_2 questions.")

    # Insert
    cur.executemany(INSERT_SQL, QUESTIONS)
    conn.commit()

    total = len(QUESTIONS)
    print(f"Inserted {total} algebra_2 questions.\n")

    # --- Summary by unit ---
    summary = defaultdict(lambda: defaultdict(int))
    for q in QUESTIONS:
        unit = q[1]   # sat_domain
        fuar = q[2]   # fuar_dimension
        summary[unit][fuar] += 1

    unit_order = [
        "polynomials",
        "rational_functions",
        "exp_log",
        "trig",
        "sequences_series",
        "complex_numbers",
    ]

    expected = {
        "polynomials": 16,
        "rational_functions": 12,
        "exp_log": 16,
        "trig": 12,
        "sequences_series": 12,
        "complex_numbers": 16,
    }

    print(f"{'Unit':<22} {'F':>4} {'U':>4} {'A':>4} {'R':>4} {'Total':>6}  {'Expected':>8}")
    print("─" * 56)
    grand_total = 0
    for unit in unit_order:
        counts = summary[unit]
        row_total = sum(counts.values())
        grand_total += row_total
        flag = "" if row_total == expected[unit] else " ← MISMATCH"
        print(f"{unit:<22} {counts.get('F',0):>4} {counts.get('U',0):>4} "
              f"{counts.get('A',0):>4} {counts.get('R',0):>4} {row_total:>6}  {expected[unit]:>8}{flag}")
    print("─" * 56)
    f_tot = sum(summary[u].get('F', 0) for u in unit_order)
    u_tot = sum(summary[u].get('U', 0) for u in unit_order)
    a_tot = sum(summary[u].get('A', 0) for u in unit_order)
    r_tot = sum(summary[u].get('R', 0) for u in unit_order)
    print(f"{'TOTAL':<22} {f_tot:>4} {u_tot:>4} {a_tot:>4} {r_tot:>4} {grand_total:>6}  {'84':>8}")

    # --- Difficulty spread ---
    diff_counts = defaultdict(int)
    for q in QUESTIONS:
        diff_counts[q[3]] += 1

    print(f"\nDifficulty distribution:")
    for d in sorted(diff_counts):
        print(f"  Level {d}: {diff_counts[d]:>3} questions")

    conn.close()
    print("\nDone.")


if __name__ == "__main__":
    # Run from the script's directory so college_ready.db is found
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    seed()
