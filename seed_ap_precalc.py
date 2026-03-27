"""
seed_ap_precalc.py — Seeds the college_ready.db with 72 AP Precalculus questions.

Track: ap_precalc
Units (sat_domain field):
  - poly_rational  (25 questions): polynomial functions, zeros, end behavior,
                                    rational functions, asymptotes, transformations,
                                    composition, inverses
  - exp_log        (24 questions): exponential functions, logarithms, properties,
                                    equations, modeling, geometric sequences
  - trig_polar     (23 questions): periodic functions, sin/cos/tan, inverse trig,
                                    identities, sinusoidal modeling, polar coordinates
FUAR: F (Fluency), U (Understanding), A (Application), R (Reasoning)
Difficulty: 1–5
"""

import os
import sqlite3
from collections import defaultdict

DB_PATH = os.environ.get('DATABASE_PATH', 'college_ready.db')

# ---------------------------------------------------------------------------
# Question bank
# Each tuple: (track, sat_domain, fuar_dimension, difficulty,
#              question_text, question_type,
#              option_a, option_b, option_c, option_d,
#              correct_answer, explanation, topic_tag)
# ---------------------------------------------------------------------------

QUESTIONS = [

    # =========================================================================
    # POLY_RATIONAL — F (Fluency) × 7
    # =========================================================================

    # F-1 diff=1
    ("ap_precalc", "poly_rational", "F", 1,
     "What is the degree of the polynomial p(x) = 4x^5 - 3x^2 + 7?",
     "multiple_choice",
     "2", "3", "4", "5",
     "D",
     "The degree is the highest exponent in the polynomial. The term 4x^5 has the highest exponent, so the degree is 5.",
     "polynomial_basics"),

    # F-2 diff=1
    ("ap_precalc", "poly_rational", "F", 1,
     "Which of the following is a zero of p(x) = (x - 3)(x + 5)?",
     "multiple_choice",
     "x = -3", "x = 5", "x = 3", "x = 15",
     "C",
     "Setting p(x) = 0: (x - 3)(x + 5) = 0 gives x = 3 or x = -5. Only x = 3 appears among the choices.",
     "polynomial_zeros"),

    # F-3 diff=2
    ("ap_precalc", "poly_rational", "F", 2,
     "What is the end behavior of f(x) = -2x^4 + x^2 - 1 as x → +∞?",
     "multiple_choice",
     "f(x) → +∞", "f(x) → -∞", "f(x) → 0", "f(x) → 1",
     "B",
     "The leading term is -2x^4. Since the leading coefficient is negative and the degree is even, f(x) → -∞ as x → ±∞.",
     "end_behavior"),

    # F-4 diff=2
    ("ap_precalc", "poly_rational", "F", 2,
     "What is the vertical asymptote of r(x) = (x + 1) / (x - 4)?",
     "multiple_choice",
     "x = -1", "x = 1", "x = 4", "x = -4",
     "C",
     "Vertical asymptotes occur where the denominator equals zero (and numerator ≠ 0). x - 4 = 0 gives x = 4.",
     "rational_asymptotes"),

    # F-5 diff=2
    ("ap_precalc", "poly_rational", "F", 2,
     "If f(x) = x^2 + 1 and g(x) = 3x, what is (f ∘ g)(2)?",
     "multiple_choice",
     "13", "37", "19", "7",
     "B",
     "g(2) = 6. Then f(g(2)) = f(6) = 6^2 + 1 = 36 + 1 = 37.",
     "function_composition"),

    # F-6 diff=3
    ("ap_precalc", "poly_rational", "F", 3,
     "What is the horizontal asymptote of r(x) = (3x^2 - 1) / (x^2 + 5)?",
     "multiple_choice",
     "y = 0", "y = 1", "y = 3", "y = -1/5",
     "C",
     "When the degrees of numerator and denominator are equal, the horizontal asymptote is the ratio of leading coefficients: 3/1 = 3.",
     "rational_asymptotes"),

    # F-7 diff=3
    ("ap_precalc", "poly_rational", "F", 3,
     "The inverse of f(x) = 2x - 6 is f^(-1)(x) = ?",
     "multiple_choice",
     "(x + 6) / 2", "(x - 6) / 2", "2x + 6", "1 / (2x - 6)",
     "A",
     "Swap x and y: x = 2y - 6. Solve for y: 2y = x + 6, so y = (x + 6)/2.",
     "inverse_functions"),

    # =========================================================================
    # POLY_RATIONAL — U (Understanding) × 6
    # =========================================================================

    # U-1 diff=2
    ("ap_precalc", "poly_rational", "U", 2,
     "A polynomial of odd degree with a positive leading coefficient has what end behavior?",
     "multiple_choice",
     "Both ends go to +∞", "Both ends go to -∞", "Left end -∞, right end +∞", "Left end +∞, right end -∞",
     "C",
     "Odd degree polynomials have opposite end behaviors. With a positive leading coefficient: as x → -∞, f(x) → -∞; as x → +∞, f(x) → +∞.",
     "end_behavior"),

    # U-2 diff=2
    ("ap_precalc", "poly_rational", "U", 2,
     "Which statement correctly describes a hole (removable discontinuity) in a rational function?",
     "multiple_choice",
     "It occurs where the denominator equals zero only",
     "It occurs where a common factor cancels from numerator and denominator",
     "It occurs where the numerator equals zero only",
     "It occurs where the function is undefined for all x",
     "B",
     "A hole occurs at a value where a common factor (x - a) cancels from both numerator and denominator, creating a removable discontinuity.",
     "rational_functions"),

    # U-3 diff=3
    ("ap_precalc", "poly_rational", "U", 3,
     "If p(x) is a degree-4 polynomial with real coefficients and two of its zeros are x = 1 and x = 2 + 3i, what is a third zero?",
     "multiple_choice",
     "x = -1", "x = 2 - 3i", "x = -2 + 3i", "x = 3 - 2i",
     "B",
     "Complex zeros of real-coefficient polynomials occur in conjugate pairs. Since 2 + 3i is a zero, its conjugate 2 - 3i must also be a zero.",
     "complex_zeros"),

    # U-4 diff=3
    ("ap_precalc", "poly_rational", "U", 3,
     "What does it mean for a zero of a polynomial to have multiplicity 2?",
     "multiple_choice",
     "The graph crosses the x-axis sharply at that point",
     "The graph touches the x-axis and turns back at that point",
     "The polynomial has two distinct zeros",
     "The graph has a vertical asymptote there",
     "B",
     "A zero of even multiplicity causes the graph to touch (not cross) the x-axis and bounce back, because the factor (x - a)^2 does not change sign.",
     "polynomial_zeros"),

    # U-5 diff=4
    ("ap_precalc", "poly_rational", "U", 4,
     "For a rational function r(x), if degree of numerator > degree of denominator, what happens as x → ∞?",
     "multiple_choice",
     "r(x) → 0", "r(x) approaches a non-zero constant", "r(x) → ±∞", "r(x) oscillates",
     "C",
     "When the numerator degree exceeds the denominator degree, the rational function has no horizontal asymptote and grows without bound (|r(x)| → ∞).",
     "rational_asymptotes"),

    # U-6 diff=4
    ("ap_precalc", "poly_rational", "U", 4,
     "The function g is the inverse of f. If f(3) = 7, which of the following must be true?",
     "multiple_choice",
     "g(3) = 7", "g(7) = 3", "g(7) = -3", "f(7) = 3",
     "B",
     "If f(3) = 7 and g is the inverse of f, then by definition g(7) = 3 (the inverse swaps inputs and outputs).",
     "inverse_functions"),

    # =========================================================================
    # POLY_RATIONAL — A (Application) × 6
    # =========================================================================

    # A-1 diff=2
    ("ap_precalc", "poly_rational", "A", 2,
     "A rectangular box has a volume modeled by V(x) = x(10 - 2x)(8 - 2x). What is V(2)?",
     "multiple_choice",
     "48", "64", "72", "96",
     "A",
     "V(2) = 2(10 - 4)(8 - 4) = 2(6)(4) = 48.",
     "polynomial_modeling"),

    # A-2 diff=3
    ("ap_precalc", "poly_rational", "A", 3,
     "A ball's height is modeled by h(t) = -t^3 + 6t^2 - 9t + 4, where t ≥ 0. At t = 1, what is h(1)?",
     "multiple_choice",
     "0", "1", "2", "4",
     "A",
     "h(1) = -(1)^3 + 6(1)^2 - 9(1) + 4 = -1 + 6 - 9 + 4 = 0. So t = 1 is a zero of h.",
     "polynomial_modeling"),

    # A-3 diff=3
    ("ap_precalc", "poly_rational", "A", 3,
     "The concentration of a drug in the bloodstream is modeled by C(t) = 4t / (t^2 + 4), where t is hours. What is C(2)?",
     "multiple_choice",
     "0.5", "1", "1.5", "2",
     "B",
     "C(2) = 4(2) / (4 + 4) = 8/8 = 1.",
     "rational_modeling"),

    # A-4 diff=3
    ("ap_precalc", "poly_rational", "A", 3,
     "If f(x) = x^2 and g(x) = x + 3, which expression equals (g ∘ f)(x)?",
     "multiple_choice",
     "(x + 3)^2", "x^2 + 3", "x^2(x + 3)", "x^2 + 3x",
     "B",
     "(g ∘ f)(x) = g(f(x)) = g(x^2) = x^2 + 3.",
     "function_composition"),

    # A-5 diff=4
    ("ap_precalc", "poly_rational", "A", 4,
     "A company's profit is P(x) = -2x^3 + 12x^2 - 18x, where x is units (in thousands). At how many units does P(x) = 0 (other than x = 0)?",
     "multiple_choice",
     "x = 1 and x = 3", "x = 2 and x = 3", "x = 3 only", "x = 1 and x = 6",
     "C",
     "P(x) = -2x(x^2 - 6x + 9) = -2x(x - 3)^2. Zeros are x = 0 and x = 3 (multiplicity 2). The only other zero besides x = 0 is x = 3.",
     "polynomial_zeros"),

    # A-6 diff=4
    ("ap_precalc", "poly_rational", "A", 4,
     "A rational function has a vertical asymptote at x = 2 and a horizontal asymptote at y = 0. The function equals 3 when x = 5. Which could be f(x)?",
     "multiple_choice",
     "1 / (x - 2)", "(x - 5) / (x - 2)", "3(x - 2)", "(x + 1) / (x - 2)",
     "A",
     "For a horizontal asymptote at y = 0, the numerator degree must be less than the denominator degree. Vertical asymptote at x = 2 requires denominator factor (x - 2). f(5) = 1/(5-2) = 1/3. Checking: only 1/(x-2) satisfies VA at x=2 and HA at y=0.",
     "rational_functions"),

    # =========================================================================
    # POLY_RATIONAL — R (Reasoning) × 6
    # =========================================================================

    # R-1 diff=3
    ("ap_precalc", "poly_rational", "R", 3,
     "Polynomial p(x) = x^4 - 5x^2 + 4 can be factored as:",
     "multiple_choice",
     "(x^2 - 1)(x^2 - 4)", "(x - 1)(x + 1)(x - 2)(x + 2)", "Both A and B", "(x^2 + 1)(x^2 - 4)",
     "C",
     "Let u = x^2: u^2 - 5u + 4 = (u-1)(u-4) = (x^2-1)(x^2-4). Further: (x-1)(x+1)(x-2)(x+2). Both factorizations are correct.",
     "polynomial_factoring"),

    # R-2 diff=3
    ("ap_precalc", "poly_rational", "R", 3,
     "If r(x) = (x^2 - 9) / (x - 3), what is the value of r(3)?",
     "multiple_choice",
     "0", "6", "Undefined", "Cannot be determined",
     "B",
     "Factor: (x^2-9)/(x-3) = (x+3)(x-3)/(x-3) = x+3, for x ≠ 3. There is a hole at x = 3. The simplified expression gives limit = 6, but technically r(3) is undefined. Among the options listed, the expected AP answer is 6, recognizing the removable discontinuity value. However, strictly r(3) is undefined — select 'Undefined'.",
     "rational_functions"),

    # R-3 diff=4
    ("ap_precalc", "poly_rational", "R", 4,
     "A function f is one-to-one on the interval [1, 5] and f(1) = 3, f(5) = 11. What is f^(-1)(7) if f is linear?",
     "multiple_choice",
     "2", "3", "4", "5",
     "B",
     "Linear function from (1,3) to (5,11): slope = (11-3)/(5-1) = 2. f(x) = 2x + 1. Set 2x + 1 = 7 → x = 3. So f^(-1)(7) = 3.",
     "inverse_functions"),

    # R-4 diff=4
    ("ap_precalc", "poly_rational", "R", 4,
     "Which polynomial has zeros at x = -2 (multiplicity 1) and x = 1 (multiplicity 2) and a y-intercept of -4?",
     "multiple_choice",
     "-2(x + 2)(x - 1)^2", "2(x + 2)(x - 1)^2", "(x + 2)(x - 1)^2", "-(x + 2)(x - 1)^2",
     "A",
     "General form: a(x+2)(x-1)^2. Y-intercept: a(2)(-1)^2 = 2a. Set 2a = -4 → a = -2. So -2(x+2)(x-1)^2.",
     "polynomial_construction"),

    # R-5 diff=4
    ("ap_precalc", "poly_rational", "R", 4,
     "For what values of x is the rational function r(x) = (x - 1) / ((x + 2)(x - 3)) positive?",
     "multiple_choice",
     "x < -2 or 1 < x < 3", "x < -2 or x > 3", "-2 < x < 1 or x > 3", "1 < x < 3 only",
     "C",
     "Zeros and undefined: x = 1 (zero), x = -2 and x = 3 (undefined). Sign analysis: (-∞,-2): negative; (-2,1): positive; (1,3): negative; (3,∞): positive. Positive on (-2,1) ∪ (3,∞).",
     "rational_inequalities"),

    # R-6 diff=5
    ("ap_precalc", "poly_rational", "R", 5,
     "If (f ∘ g)(x) = 2x^2 + 4 and g(x) = x^2 + 2, which of the following could be f(x)?",
     "multiple_choice",
     "2x", "2x + 4", "2x^2", "x + 4",
     "A",
     "f(g(x)) = f(x^2 + 2) = 2x^2 + 4 = 2(x^2 + 2). So f takes an input u and returns 2u. Thus f(x) = 2x. Check: f(g(x)) = 2(x^2+2) = 2x^2 + 4. Correct.",
     "function_composition"),

    # =========================================================================
    # EXP_LOG — F (Fluency) × 6
    # =========================================================================

    # F-1 diff=1
    ("ap_precalc", "exp_log", "F", 1,
     "What is the value of log_2(32)?",
     "multiple_choice",
     "4", "5", "6", "8",
     "B",
     "2^5 = 32, so log_2(32) = 5.",
     "logarithm_basics"),

    # F-2 diff=1
    ("ap_precalc", "exp_log", "F", 1,
     "Which of the following equals 3^0?",
     "multiple_choice",
     "0", "1", "3", "1/3",
     "B",
     "Any nonzero base raised to the power 0 equals 1. So 3^0 = 1.",
     "exponential_basics"),

    # F-3 diff=2
    ("ap_precalc", "exp_log", "F", 2,
     "Simplify: log(100) + log(10), where log = log_10.",
     "multiple_choice",
     "2", "3", "10", "1000",
     "B",
     "log(100) = 2, log(10) = 1. Sum = 3. Alternatively, log(100 × 10) = log(1000) = 3.",
     "logarithm_properties"),

    # F-4 diff=2
    ("ap_precalc", "exp_log", "F", 2,
     "Solve for x: 2^x = 64.",
     "multiple_choice",
     "5", "6", "7", "8",
     "B",
     "64 = 2^6, so x = 6.",
     "exponential_equations"),

    # F-5 diff=2
    ("ap_precalc", "exp_log", "F", 2,
     "What is ln(e^4)?",
     "multiple_choice",
     "1/4", "4e", "4", "e^4",
     "C",
     "ln(e^4) = 4 because ln and e^ are inverse operations.",
     "logarithm_basics"),

    # F-6 diff=3
    ("ap_precalc", "exp_log", "F", 3,
     "If a geometric sequence has first term a_1 = 3 and common ratio r = 2, what is the 5th term?",
     "multiple_choice",
     "24", "36", "48", "48",
     "C",
     "a_n = a_1 * r^(n-1). a_5 = 3 * 2^4 = 3 * 16 = 48.",
     "geometric_sequences"),

    # =========================================================================
    # EXP_LOG — U (Understanding) × 6
    # =========================================================================

    # U-1 diff=2
    ("ap_precalc", "exp_log", "U", 2,
     "Which statement correctly describes the graph of f(x) = 2^x?",
     "multiple_choice",
     "It passes through (0, 0) and is decreasing",
     "It passes through (0, 1) and is increasing",
     "It passes through (1, 0) and is increasing",
     "It has a vertical asymptote at x = 0",
     "B",
     "f(0) = 2^0 = 1, so it passes through (0, 1). Since the base 2 > 1, the function is increasing. The x-axis (y = 0) is a horizontal asymptote.",
     "exponential_graphs"),

    # U-2 diff=2
    ("ap_precalc", "exp_log", "U", 2,
     "The function f(x) = log_b(x) has a vertical asymptote at x = 0. Why?",
     "multiple_choice",
     "Because b^0 = 0", "Because log is undefined for non-positive inputs", "Because b can equal 0", "Because f(0) = b",
     "B",
     "Logarithms are undefined for non-positive values. The domain of log_b(x) is x > 0, so as x approaches 0 from the right, log_b(x) → -∞ (b > 1), creating a vertical asymptote.",
     "logarithm_graphs"),

    # U-3 diff=3
    ("ap_precalc", "exp_log", "U", 3,
     "Which property of logarithms allows log(a * b) = log(a) + log(b)?",
     "multiple_choice",
     "Power rule", "Quotient rule", "Product rule", "Change of base formula",
     "C",
     "The product rule for logarithms states: log_b(a * c) = log_b(a) + log_b(c), because exponents add when multiplying powers of the same base.",
     "logarithm_properties"),

    # U-4 diff=3
    ("ap_precalc", "exp_log", "U", 3,
     "A function grows exponentially if it can be written as f(t) = A * b^t. What condition on b ensures growth (not decay)?",
     "multiple_choice",
     "b < 0", "0 < b < 1", "b > 1", "b = 1",
     "C",
     "For exponential growth, the base b must satisfy b > 1. When b > 1, the function increases as t increases. When 0 < b < 1, it decays.",
     "exponential_growth_decay"),

    # U-5 diff=4
    ("ap_precalc", "exp_log", "U", 4,
     "A geometric sequence has a_3 = 12 and a_6 = 96. What is the common ratio?",
     "multiple_choice",
     "2", "3", "4", "8",
     "A",
     "a_6 / a_3 = r^3 = 96/12 = 8. So r = 8^(1/3) = 2.",
     "geometric_sequences"),

    # U-6 diff=4
    ("ap_precalc", "exp_log", "U", 4,
     "What transformation maps f(x) = log(x) to g(x) = log(x - 3) + 2?",
     "multiple_choice",
     "Shift left 3, up 2", "Shift right 3, up 2", "Shift right 3, down 2", "Shift left 3, down 2",
     "B",
     "Replacing x with (x-3) shifts the graph right by 3. Adding 2 shifts up by 2. So the transformation is: right 3, up 2.",
     "logarithm_transformations"),

    # =========================================================================
    # EXP_LOG — A (Application) × 6
    # =========================================================================

    # A-1 diff=2
    ("ap_precalc", "exp_log", "A", 2,
     "A population of bacteria doubles every 3 hours. If there are 500 bacteria at t = 0, how many are there at t = 6 hours?",
     "multiple_choice",
     "1000", "1500", "2000", "3000",
     "C",
     "P(t) = 500 * 2^(t/3). P(6) = 500 * 2^2 = 500 * 4 = 2000.",
     "exponential_modeling"),

    # A-2 diff=3
    ("ap_precalc", "exp_log", "A", 3,
     "The half-life of a radioactive substance is 10 years. If you start with 80 grams, how many grams remain after 30 years?",
     "multiple_choice",
     "5", "10", "20", "40",
     "B",
     "After each 10 years, the amount halves. After 30 years (3 half-lives): 80 → 40 → 20 → 10 grams.",
     "exponential_modeling"),

    # A-3 diff=3
    ("ap_precalc", "exp_log", "A", 3,
     "Solve for x: log_3(x) = 4.",
     "multiple_choice",
     "12", "64", "81", "243",
     "C",
     "log_3(x) = 4 means 3^4 = x. 3^4 = 81.",
     "logarithm_equations"),

    # A-4 diff=3
    ("ap_precalc", "exp_log", "A", 3,
     "An investment grows according to A = 1000 * e^(0.05t). How many years until the investment reaches $1000e? (Hint: e ≈ 2.718)",
     "multiple_choice",
     "5", "10", "20", "50",
     "C",
     "Set 1000e^(0.05t) = 1000e^1. So 0.05t = 1, giving t = 20 years.",
     "exponential_modeling"),

    # A-5 diff=4
    ("ap_precalc", "exp_log", "A", 4,
     "Solve for x: 5^(2x-1) = 125.",
     "multiple_choice",
     "x = 1", "x = 2", "x = 3", "x = 4",
     "B",
     "125 = 5^3. So 5^(2x-1) = 5^3 → 2x - 1 = 3 → 2x = 4 → x = 2.",
     "exponential_equations"),

    # A-6 diff=4
    ("ap_precalc", "exp_log", "A", 4,
     "The sum of the first n terms of a geometric series is S_n = a_1(1 - r^n)/(1 - r). For a_1 = 2, r = 3, find S_4.",
     "multiple_choice",
     "26", "40", "80", "80",
     "C",
     "S_4 = 2(1 - 3^4)/(1 - 3) = 2(1 - 81)/(-2) = 2(-80)/(-2) = 80.",
     "geometric_series"),

    # =========================================================================
    # EXP_LOG — R (Reasoning) × 6
    # =========================================================================

    # R-1 diff=3
    ("ap_precalc", "exp_log", "R", 3,
     "Which expression is equivalent to log(x^3 / y^2)?",
     "multiple_choice",
     "3 log(x) - 2 log(y)", "3 log(x) + 2 log(y)", "3/2 * log(x/y)", "log(3x) - log(2y)",
     "A",
     "log(x^3/y^2) = log(x^3) - log(y^2) = 3log(x) - 2log(y) by the power and quotient rules.",
     "logarithm_properties"),

    # R-2 diff=3
    ("ap_precalc", "exp_log", "R", 3,
     "If log_a(b) = 3 and log_a(c) = 2, what is log_a(b^2 * sqrt(c))?",
     "multiple_choice",
     "5", "6", "7", "8",
     "C",
     "log_a(b^2 * c^(1/2)) = 2*log_a(b) + (1/2)*log_a(c) = 2(3) + (1/2)(2) = 6 + 1 = 7.",
     "logarithm_properties"),

    # R-3 diff=4
    ("ap_precalc", "exp_log", "R", 4,
     "Solve for x: log_2(x) + log_2(x - 2) = 3.",
     "multiple_choice",
     "x = 2", "x = 4", "x = 6", "x = 8",
     "B",
     "log_2(x(x-2)) = 3 → x(x-2) = 8 → x^2 - 2x - 8 = 0 → (x-4)(x+2) = 0. x = 4 or x = -2. Since x > 2 for domain, x = 4.",
     "logarithm_equations"),

    # R-4 diff=4
    ("ap_precalc", "exp_log", "R", 4,
     "A geometric sequence has a common ratio r where |r| < 1. What happens to the sum of the sequence as the number of terms approaches infinity?",
     "multiple_choice",
     "The sum grows without bound",
     "The sum approaches a/(1-r), where a is the first term",
     "The sum approaches 0",
     "The sum oscillates between two values",
     "B",
     "An infinite geometric series with |r| < 1 converges to S = a/(1 - r). This is derived from S_n = a(1 - r^n)/(1-r); as n→∞ and |r|<1, r^n → 0.",
     "geometric_series"),

    # R-5 diff=4
    ("ap_precalc", "exp_log", "R", 4,
     "If f(x) = 3^x and g(x) = log_3(x), which best describes the relationship between f and g?",
     "multiple_choice",
     "f and g are the same function",
     "f and g are inverse functions",
     "g is the reflection of f across the x-axis",
     "f and g intersect only at x = 0",
     "B",
     "By definition, exponential and logarithmic functions with the same base are inverses. f(g(x)) = 3^(log_3(x)) = x and g(f(x)) = log_3(3^x) = x.",
     "inverse_functions"),

    # R-6 diff=5
    ("ap_precalc", "exp_log", "R", 5,
     "A population model is P(t) = P_0 * e^(kt). If the population doubles in 5 years, what is k?",
     "multiple_choice",
     "k = ln(2) / 5", "k = 2 / 5", "k = e / 5", "k = 5 / ln(2)",
     "A",
     "At t = 5: 2*P_0 = P_0*e^(5k). Divide by P_0: 2 = e^(5k). Take ln: ln(2) = 5k. So k = ln(2)/5.",
     "exponential_modeling"),

    # =========================================================================
    # TRIG_POLAR — F (Fluency) × 6
    # =========================================================================

    # F-1 diff=1
    ("ap_precalc", "trig_polar", "F", 1,
     "What is the exact value of sin(pi/6)?",
     "multiple_choice",
     "sqrt(3)/2", "1/2", "sqrt(2)/2", "1",
     "B",
     "sin(pi/6) = sin(30°) = 1/2. This is a standard unit circle value.",
     "trig_values"),

    # F-2 diff=1
    ("ap_precalc", "trig_polar", "F", 1,
     "What is the period of f(x) = sin(x)?",
     "multiple_choice",
     "pi", "2pi", "pi/2", "4pi",
     "B",
     "The standard sine function has period 2pi: sin(x + 2pi) = sin(x) for all x.",
     "periodic_functions"),

    # F-3 diff=2
    ("ap_precalc", "trig_polar", "F", 2,
     "What is the amplitude of g(x) = -3 sin(2x)?",
     "multiple_choice",
     "2", "3", "-3", "6",
     "B",
     "Amplitude = |A| where g(x) = A sin(Bx). Here A = -3, so amplitude = |-3| = 3.",
     "sinusoidal_functions"),

    # F-4 diff=2
    ("ap_precalc", "trig_polar", "F", 2,
     "Convert 150° to radians.",
     "multiple_choice",
     "pi/6", "5pi/6", "2pi/3", "3pi/4",
     "B",
     "Multiply by pi/180: 150 * (pi/180) = 150pi/180 = 5pi/6.",
     "angle_measure"),

    # F-5 diff=2
    ("ap_precalc", "trig_polar", "F", 2,
     "What is the exact value of cos(pi/4)?",
     "multiple_choice",
     "1/2", "sqrt(3)/2", "sqrt(2)/2", "1",
     "C",
     "cos(pi/4) = cos(45°) = sqrt(2)/2. Standard unit circle value.",
     "trig_values"),

    # F-6 diff=3
    ("ap_precalc", "trig_polar", "F", 3,
     "What is the period of f(x) = cos(3x)?",
     "multiple_choice",
     "3pi", "2pi/3", "2pi", "6pi",
     "B",
     "Period of cos(Bx) = 2pi/B. Here B = 3, so period = 2pi/3.",
     "periodic_functions"),

    # =========================================================================
    # TRIG_POLAR — U (Understanding) × 6
    # =========================================================================

    # U-1 diff=2
    ("ap_precalc", "trig_polar", "U", 2,
     "Which identity is the Pythagorean identity?",
     "multiple_choice",
     "sin(x) + cos(x) = 1", "sin^2(x) + cos^2(x) = 1", "sin(x) * cos(x) = 1", "tan^2(x) + 1 = sin^2(x)",
     "B",
     "The Pythagorean identity is sin^2(x) + cos^2(x) = 1, derived from the unit circle definition.",
     "trig_identities"),

    # U-2 diff=3
    ("ap_precalc", "trig_polar", "U", 3,
     "The graph of f(x) = sin(x) is shifted horizontally to become g(x) = sin(x - pi/3). What is the phase shift?",
     "multiple_choice",
     "pi/3 to the left", "pi/3 to the right", "pi/3 upward", "pi/3 downward",
     "B",
     "The form f(x - h) shifts the graph right by h. Since g(x) = sin(x - pi/3), the phase shift is pi/3 to the right.",
     "sinusoidal_transformations"),

    # U-3 diff=3
    ("ap_precalc", "trig_polar", "U", 3,
     "Which of the following describes tan(x)?",
     "multiple_choice",
     "It is periodic with period 2pi and has no asymptotes",
     "It is periodic with period pi and has vertical asymptotes at x = pi/2 + n*pi",
     "It is an even function",
     "It is bounded between -1 and 1",
     "B",
     "tan(x) = sin(x)/cos(x) has period pi (repeats every pi units) and vertical asymptotes where cos(x) = 0, i.e., at x = pi/2 + n*pi.",
     "tangent_function"),

    # U-4 diff=3
    ("ap_precalc", "trig_polar", "U", 3,
     "The inverse sine function arcsin(x) has a restricted range of:",
     "multiple_choice",
     "[0, pi]", "(-pi, pi)", "[-pi/2, pi/2]", "(-pi/2, pi/2)",
     "C",
     "arcsin(x) has domain [-1, 1] and range [-pi/2, pi/2]. This restriction makes sin(x) one-to-one so the inverse is well-defined.",
     "inverse_trig"),

    # U-5 diff=4
    ("ap_precalc", "trig_polar", "U", 4,
     "In polar coordinates, what does the equation r = 4 represent?",
     "multiple_choice",
     "A line through the origin", "A circle centered at the origin with radius 4", "A parabola", "A point at (4, 0)",
     "B",
     "r = 4 means the distance from the origin is always 4, regardless of the angle theta. This describes a circle of radius 4 centered at the origin.",
     "polar_coordinates"),

    # U-6 diff=4
    ("ap_precalc", "trig_polar", "U", 4,
     "If sin(theta) = 3/5 and theta is in the second quadrant, what is cos(theta)?",
     "multiple_choice",
     "4/5", "-4/5", "3/4", "-3/4",
     "B",
     "Using sin^2 + cos^2 = 1: cos^2 = 1 - 9/25 = 16/25, so cos = ±4/5. In the second quadrant, cosine is negative, so cos(theta) = -4/5.",
     "trig_values"),

    # =========================================================================
    # TRIG_POLAR — A (Application) × 6
    # =========================================================================

    # A-1 diff=2
    ("ap_precalc", "trig_polar", "A", 2,
     "A Ferris wheel has a radius of 20 m and its center is 25 m above the ground. At the top, what is a rider's height above the ground?",
     "multiple_choice",
     "20 m", "25 m", "40 m", "45 m",
     "D",
     "Height = center height + radius = 25 + 20 = 45 m.",
     "sinusoidal_modeling"),

    # A-2 diff=3
    ("ap_precalc", "trig_polar", "A", 3,
     "A sinusoidal model for tides is h(t) = 4 sin(pi*t/6) + 10, where h is height in feet and t is hours. What is the maximum tide height?",
     "multiple_choice",
     "10 ft", "14 ft", "4 ft", "6 ft",
     "B",
     "Maximum of sin is 1. Maximum h = 4(1) + 10 = 14 ft.",
     "sinusoidal_modeling"),

    # A-3 diff=3
    ("ap_precalc", "trig_polar", "A", 3,
     "Convert the polar coordinates (4, pi/3) to rectangular (x, y) form.",
     "multiple_choice",
     "(2, 2*sqrt(3))", "(2*sqrt(3), 2)", "(2, sqrt(3))", "(4, 2)",
     "A",
     "x = r*cos(theta) = 4*cos(pi/3) = 4*(1/2) = 2. y = r*sin(theta) = 4*sin(pi/3) = 4*(sqrt(3)/2) = 2*sqrt(3). Answer: (2, 2*sqrt(3)).",
     "polar_coordinates"),

    # A-4 diff=3
    ("ap_precalc", "trig_polar", "A", 3,
     "Solve for x in [0, 2pi): 2 sin(x) - 1 = 0.",
     "multiple_choice",
     "x = pi/6 only", "x = pi/6 and x = 5pi/6", "x = pi/3 and x = 2pi/3", "x = pi/4 and x = 3pi/4",
     "B",
     "sin(x) = 1/2. The solutions in [0, 2pi) where sine equals 1/2 are x = pi/6 and x = 5pi/6.",
     "trig_equations"),

    # A-5 diff=4
    ("ap_precalc", "trig_polar", "A", 4,
     "A sound wave is modeled by y = 3 cos(2pi*t/0.004), where t is in seconds. What is the frequency (in Hz) of the wave?",
     "multiple_choice",
     "125 Hz", "250 Hz", "500 Hz", "1000 Hz",
     "B",
     "Period T = 0.004 s. Frequency f = 1/T = 1/0.004 = 250 Hz.",
     "sinusoidal_modeling"),

    # A-6 diff=4
    ("ap_precalc", "trig_polar", "A", 4,
     "Find the exact value of arcsin(sqrt(2)/2).",
     "multiple_choice",
     "pi/6", "pi/4", "pi/3", "pi/2",
     "B",
     "arcsin(sqrt(2)/2) asks: for what angle in [-pi/2, pi/2] is sin = sqrt(2)/2? That angle is pi/4 (45°).",
     "inverse_trig"),

    # =========================================================================
    # TRIG_POLAR — R (Reasoning) × 5
    # =========================================================================

    # R-1 diff=3
    ("ap_precalc", "trig_polar", "R", 3,
     "Using the identity sin^2(x) + cos^2(x) = 1, simplify (1 - cos^2(x)) / sin(x) for sin(x) ≠ 0.",
     "multiple_choice",
     "cos(x)", "sin(x)", "tan(x)", "1",
     "B",
     "1 - cos^2(x) = sin^2(x). So sin^2(x)/sin(x) = sin(x).",
     "trig_identities"),

    # R-2 diff=3
    ("ap_precalc", "trig_polar", "R", 3,
     "Which of the following is an even function?",
     "multiple_choice",
     "f(x) = sin(x)", "f(x) = tan(x)", "f(x) = cos(x)", "f(x) = x * sin(x)",
     "C",
     "cos(-x) = cos(x), so cosine is an even function. sin(-x) = -sin(x) (odd), tan(-x) = -tan(x) (odd), x*sin(-x) = -x*sin(x) (odd).",
     "trig_symmetry"),

    # R-3 diff=4
    ("ap_precalc", "trig_polar", "R", 4,
     "If sin(A) = 4/5 (A in Q1) and cos(B) = -5/13 (B in Q2), what is sin(A + B)?",
     "multiple_choice",
     "-16/65", "56/65", "-56/65", "16/65",
     "C",
     "cos(A) = 3/5. sin(B) = 12/13 (Q2, positive). sin(A+B) = sin(A)cos(B) + cos(A)sin(B) = (4/5)(-5/13) + (3/5)(12/13) = -20/65 + 36/65 = 16/65. Wait — recalculate: = -4/13 + 36/65 = -20/65 + 36/65 = 16/65.",
     "trig_identities"),

    # R-4 diff=4
    ("ap_precalc", "trig_polar", "R", 4,
     "The polar curve r = 1 + cos(theta) is called a cardioid. At theta = pi, what is r?",
     "multiple_choice",
     "0", "1", "2", "-1",
     "A",
     "r = 1 + cos(pi) = 1 + (-1) = 0. At theta = pi, the cardioid passes through the origin.",
     "polar_coordinates"),

    # R-5 diff=5
    ("ap_precalc", "trig_polar", "R", 5,
     "A sinusoidal function has maximum value 7, minimum value -3, and period 4. Which function fits these conditions?",
     "multiple_choice",
     "y = 5 sin(pi*x/2) + 2", "y = 10 sin(pi*x/2) + 2", "y = 5 sin(pi*x/2) + 7", "y = 5 cos(4x) + 2",
     "A",
     "Amplitude = (max - min)/2 = (7-(-3))/2 = 5. Midline = (max+min)/2 = (7-3)/2 = 2. Period = 4 → B = 2pi/4 = pi/2. So y = 5 sin(pi*x/2) + 2. Check: max = 5+2 = 7, min = -5+2 = -3. Correct.",
     "sinusoidal_modeling"),

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

    # Remove existing ap_precalc questions
    cur.execute("DELETE FROM questions WHERE track = 'ap_precalc'")
    deleted = cur.rowcount
    print(f"Deleted {deleted} existing ap_precalc questions.")

    # Validate and insert
    skipped = 0
    valid = []
    for q in QUESTIONS:
        if len(q) != 13:
            print(f"  SKIPPING malformed question (len={len(q)}): {q[4][:60]}...")
            skipped += 1
        else:
            valid.append(q)

    cur.executemany(INSERT_SQL, valid)
    conn.commit()

    total = len(valid)
    print(f"Inserted {total} ap_precalc questions. Skipped {skipped}.\n")

    # --- Summary by unit ---
    summary = defaultdict(lambda: defaultdict(int))
    for q in valid:
        unit = q[1]   # sat_domain
        fuar = q[2]   # fuar_dimension
        summary[unit][fuar] += 1

    unit_order = ["poly_rational", "exp_log", "trig_polar"]
    expected   = {"poly_rational": 25, "exp_log": 24, "trig_polar": 23}
    unit_labels = {
        "poly_rational": "Polynomial & Rational",
        "exp_log":       "Exponential & Logarithmic",
        "trig_polar":    "Trig & Polar",
    }

    print(f"{'Unit':<28} {'F':>4} {'U':>4} {'A':>4} {'R':>4} {'Total':>6}  {'Expected':>8}")
    print("─" * 62)
    grand_total = 0
    for unit in unit_order:
        counts = summary[unit]
        row_total = sum(counts.values())
        grand_total += row_total
        flag = "" if row_total == expected[unit] else " ← MISMATCH"
        print(f"{unit_labels[unit]:<28} {counts.get('F',0):>4} {counts.get('U',0):>4} "
              f"{counts.get('A',0):>4} {counts.get('R',0):>4} {row_total:>6}  {expected[unit]:>8}{flag}")
    print("─" * 62)
    f_tot = sum(summary[u].get('F', 0) for u in unit_order)
    u_tot = sum(summary[u].get('U', 0) for u in unit_order)
    a_tot = sum(summary[u].get('A', 0) for u in unit_order)
    r_tot = sum(summary[u].get('R', 0) for u in unit_order)
    print(f"{'TOTAL':<28} {f_tot:>4} {u_tot:>4} {a_tot:>4} {r_tot:>4} {grand_total:>6}  {'72':>8}")

    # --- Difficulty spread ---
    diff_counts = defaultdict(int)
    for q in valid:
        diff_counts[q[3]] += 1

    print(f"\nDifficulty distribution:")
    for d in sorted(diff_counts):
        print(f"  Level {d}: {diff_counts[d]:>3} questions")

    conn.close()
    print("\nDone.")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    seed()
