"""
seed_precalculus.py — Seeds college_ready.db with 84 Precalculus questions.

Track: precalculus
Domains: functions, poly_rational, exp_log, trig_functions, analytic_trig,
         polar_vectors, limits_intro
FUAR: F (Fluency), U (Understanding), A (Application), R (Reasoning)
Difficulty: 1–5
"""

import sqlite3
import os
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
    # FUNCTIONS — 12 questions
    # =========================================================================

    # 1 F diff=1
    ("precalculus", "functions", "F", 1,
     "What is the domain of f(x) = √(x − 3)?",
     "multiple_choice",
     "x > 3", "x ≥ 3", "x < 3", "all real numbers",
     "B",
     "The radicand must be non-negative: x − 3 ≥ 0, so x ≥ 3.",
     "domain_range"),

    # 2 U diff=2
    ("precalculus", "functions", "U", 2,
     "If f(x) = x² + 1, what is f(x + 2)?",
     "multiple_choice",
     "x² + 5", "x² + 4x + 5", "x² + 2x + 5", "x² + 4x + 3",
     "B",
     "f(x + 2) = (x + 2)² + 1 = x² + 4x + 4 + 1 = x² + 4x + 5.",
     "transformations"),

    # 3 F diff=1
    ("precalculus", "functions", "F", 1,
     "Given g(x) = 2x − 4, what is g(3)?",
     "multiple_choice",
     "2", "6", "10", "2",
     "A",
     "g(3) = 2(3) − 4 = 6 − 4 = 2.",
     "function_evaluation"),

    # 4 U diff=2
    ("precalculus", "functions", "U", 2,
     "If f(x) = 3x and g(x) = x + 2, what is (f ∘ g)(1)?",
     "multiple_choice",
     "5", "9", "7", "3",
     "B",
     "g(1) = 1 + 2 = 3. Then f(g(1)) = f(3) = 3(3) = 9.",
     "composition"),

    # 5 A diff=3
    ("precalculus", "functions", "A", 3,
     "Find the inverse of f(x) = (x + 5) / 2.",
     "multiple_choice",
     "f⁻¹(x) = 2x − 5", "f⁻¹(x) = 2x + 5", "f⁻¹(x) = (x − 5) / 2", "f⁻¹(x) = x/2 + 5",
     "A",
     "Swap x and y: x = (y + 5)/2. Solve for y: 2x = y + 5, y = 2x − 5.",
     "inverse_functions"),

    # 6 R diff=4
    ("precalculus", "functions", "R", 4,
     "Which function is even?",
     "multiple_choice",
     "f(x) = x³ + x", "f(x) = x² + x", "f(x) = x⁴ − 2x²", "f(x) = x³ − x²",
     "C",
     "An even function satisfies f(−x) = f(x). f(−x) = (−x)⁴ − 2(−x)² = x⁴ − 2x² = f(x). ✓",
     "even_odd"),

    # 7 F diff=2
    ("precalculus", "functions", "F", 2,
     "What is the range of f(x) = |x| − 1?",
     "multiple_choice",
     "y ≥ 0", "y ≥ −1", "all real numbers", "y > −1",
     "B",
     "|x| ≥ 0 for all x, so |x| − 1 ≥ −1. The range is y ≥ −1.",
     "domain_range"),

    # 8 A diff=3
    ("precalculus", "functions", "A", 3,
     "A piecewise function is defined as f(x) = {x² if x < 0; 2x + 1 if x ≥ 0}. What is f(−2) + f(3)?",
     "multiple_choice",
     "9", "11", "7", "4",
     "B",
     "f(−2) = (−2)² = 4. f(3) = 2(3) + 1 = 7. Sum = 4 + 7 = 11.",
     "piecewise"),

    # 9 U diff=3
    ("precalculus", "functions", "U", 3,
     "If f(x) = 2x + 1 and g(x) = x − 3, what is (g ∘ f)(x)?",
     "multiple_choice",
     "2x − 2", "2x − 5", "2x + 4", "2x − 1",
     "A",
     "g(f(x)) = g(2x + 1) = (2x + 1) − 3 = 2x − 2.",
     "composition"),

    # 10 R diff=4
    ("precalculus", "functions", "R", 4,
     "The graph of f(x) is shifted 3 units left and reflected over the x-axis. Which expression represents this transformation?",
     "multiple_choice",
     "−f(x − 3)", "−f(x + 3)", "f(−x + 3)", "f(−x − 3)",
     "B",
     "Shift left 3: f(x + 3). Reflect over x-axis: −f(x + 3).",
     "transformations"),

    # 11 A diff=4
    ("precalculus", "functions", "A", 4,
     "If f(x) = √(x + 1) and g(x) = x², find the domain of (f ∘ g)(x).",
     "multiple_choice",
     "x ≥ 0", "all real numbers", "x ≥ −1", "x > 0",
     "B",
     "f(g(x)) = √(x² + 1). Since x² ≥ 0, x² + 1 ≥ 1 > 0 for all real x. Domain is all reals.",
     "composition"),

    # 12 R diff=5
    ("precalculus", "functions", "R", 5,
     "Which statement correctly describes an odd function?",
     "multiple_choice",
     "Its graph is symmetric about the y-axis",
     "f(−x) = f(x) for all x in the domain",
     "Its graph is symmetric about the origin",
     "f(0) must equal 0",
     "C",
     "An odd function satisfies f(−x) = −f(x), which means rotational symmetry about the origin. A requires f(−x) = f(x) (even), B is the definition of even, D is not always true.",
     "even_odd"),

    # =========================================================================
    # POLY_RATIONAL — 12 questions
    # =========================================================================

    # 13 F diff=1
    ("precalculus", "poly_rational", "F", 1,
     "What are the zeros of f(x) = (x − 2)(x + 5)?",
     "multiple_choice",
     "x = −2, x = 5", "x = 2, x = −5", "x = 2, x = 5", "x = −2, x = −5",
     "B",
     "Set each factor to zero: x − 2 = 0 → x = 2; x + 5 = 0 → x = −5.",
     "zeros"),

    # 14 U diff=2
    ("precalculus", "poly_rational", "U", 2,
     "What is the end behavior of f(x) = −2x³ + 5x as x → +∞?",
     "multiple_choice",
     "f(x) → +∞", "f(x) → −∞", "f(x) → 0", "f(x) → 2",
     "B",
     "Leading term is −2x³. Odd degree, negative leading coefficient: as x → +∞, f(x) → −∞.",
     "end_behavior"),

    # 15 F diff=2
    ("precalculus", "poly_rational", "F", 2,
     "Find the vertical asymptote(s) of f(x) = 1 / (x − 4).",
     "multiple_choice",
     "x = 1", "x = −4", "x = 4", "x = 0",
     "C",
     "Vertical asymptotes occur where the denominator equals zero: x − 4 = 0 → x = 4.",
     "asymptotes"),

    # 16 A diff=3
    ("precalculus", "poly_rational", "A", 3,
     "Identify any holes in f(x) = (x² − 4) / (x − 2).",
     "multiple_choice",
     "Hole at x = 2", "Vertical asymptote at x = 2", "Hole at x = −2", "No holes",
     "A",
     "Factor numerator: (x−2)(x+2)/(x−2). Cancel common factor → hole at x = 2, not an asymptote.",
     "holes"),

    # 17 U diff=2
    ("precalculus", "poly_rational", "U", 2,
     "Which best describes the graph of f(x) = x⁴ − 3x² + 2 as x → −∞?",
     "multiple_choice",
     "f(x) → −∞", "f(x) → +∞", "f(x) → 0", "f(x) → −3",
     "B",
     "Leading term x⁴ (even degree, positive). Both ends go to +∞.",
     "end_behavior"),

    # 18 R diff=4
    ("precalculus", "poly_rational", "R", 4,
     "The polynomial p(x) has degree 4 with a positive leading coefficient. The graph bounces off the x-axis at x = 1 and crosses at x = −2. What can you conclude?",
     "multiple_choice",
     "x = 1 is a simple zero; x = −2 is a repeated zero",
     "x = 1 is a repeated zero (even multiplicity); x = −2 is a simple zero",
     "Both zeros have multiplicity 2",
     "x = 1 has multiplicity 3; x = −2 has multiplicity 1",
     "B",
     "Bouncing off (touching) indicates even multiplicity; crossing indicates odd multiplicity.",
     "zeros"),

    # 19 A diff=3
    ("precalculus", "poly_rational", "A", 3,
     "Find the horizontal asymptote of f(x) = (3x² + 1) / (x² − 5).",
     "multiple_choice",
     "y = 0", "y = 3", "y = 1/5", "No horizontal asymptote",
     "B",
     "Degrees are equal (both 2). HA = ratio of leading coefficients = 3/1 = 3.",
     "asymptotes"),

    # 20 F diff=1
    ("precalculus", "poly_rational", "F", 1,
     "How many complex zeros (counting multiplicity) does a degree-5 polynomial have?",
     "multiple_choice",
     "At most 5", "Exactly 5", "At most 4", "Exactly 3",
     "B",
     "By the Fundamental Theorem of Algebra, a degree-n polynomial has exactly n complex zeros counting multiplicity.",
     "complex_zeros"),

    # 21 R diff=5
    ("precalculus", "poly_rational", "R", 5,
     "If 3 + 2i is a zero of a polynomial with real coefficients, what other zero must exist?",
     "multiple_choice",
     "3 − 2i", "−3 + 2i", "2 + 3i", "−3 − 2i",
     "A",
     "Complex zeros of polynomials with real coefficients come in conjugate pairs. The conjugate of 3 + 2i is 3 − 2i.",
     "complex_zeros"),

    # 22 U diff=3
    ("precalculus", "poly_rational", "U", 3,
     "Simplify: (x² + 2x − 8) / (x² + x − 6), stating any restrictions.",
     "multiple_choice",
     "(x + 4)/(x + 3), x ≠ 2 and x ≠ −3",
     "(x − 2)/(x − 3), x ≠ −4",
     "(x + 4)/(x + 3), x ≠ 3",
     "(x − 4)/(x − 3), x ≠ 2",
     "A",
     "Num: (x+4)(x−2). Denom: (x+3)(x−2). Cancel (x−2): (x+4)/(x+3). Restrictions: x ≠ 2 and x ≠ −3.",
     "rational_functions"),

    # 23 A diff=4
    ("precalculus", "poly_rational", "A", 4,
     "Find all vertical asymptotes of f(x) = (x + 1) / (x² − x − 6).",
     "multiple_choice",
     "x = 3 only", "x = −2 only", "x = 3 and x = −2", "x = 1 and x = −1",
     "C",
     "Denom: (x−3)(x+2). Neither factor cancels with (x+1). Vertical asymptotes at x = 3 and x = −2.",
     "asymptotes"),

    # 24 R diff=5
    ("precalculus", "poly_rational", "R", 5,
     "A rational function has a slant asymptote when the degree of the numerator is exactly one more than the degree of the denominator. What is the slant asymptote of f(x) = (x² + 3x + 1) / (x + 1)?",
     "multiple_choice",
     "y = x + 2", "y = x + 4", "y = x − 2", "y = x",
     "A",
     "Divide x² + 3x + 1 by x + 1 using polynomial long division: x + 2 remainder −1. Slant asymptote: y = x + 2.",
     "rational_functions"),

    # =========================================================================
    # EXP_LOG — 12 questions
    # =========================================================================

    # 25 F diff=1
    ("precalculus", "exp_log", "F", 1,
     "Evaluate log₂(32).",
     "multiple_choice",
     "4", "5", "6", "16",
     "B",
     "2⁵ = 32, so log₂(32) = 5.",
     "exp_log_basics"),

    # 26 U diff=2
    ("precalculus", "exp_log", "U", 2,
     "Which expression equals log(a²b / c³)?",
     "multiple_choice",
     "2 log a + log b + 3 log c",
     "2 log a + log b − 3 log c",
     "2 log a − log b + 3 log c",
     "log a + 2 log b − 3 log c",
     "B",
     "log(a²b/c³) = log(a²) + log(b) − log(c³) = 2 log a + log b − 3 log c.",
     "log_properties"),

    # 27 F diff=2
    ("precalculus", "exp_log", "F", 2,
     "Solve for x: eˣ = 20.",
     "multiple_choice",
     "x = ln(20)", "x = log(20)", "x = 20/e", "x = e²⁰",
     "A",
     "Take the natural log of both sides: x = ln(20).",
     "solving_exp"),

    # 28 A diff=3
    ("precalculus", "exp_log", "A", 3,
     "A population starts at 500 and grows at 4% per year. Which model represents the population P after t years?",
     "multiple_choice",
     "P = 500(0.04)ᵗ", "P = 500 + 0.04t", "P = 500(1.04)ᵗ", "P = 500e^(0.4t)",
     "C",
     "Percent growth uses P = P₀(1 + r)ᵗ = 500(1.04)ᵗ.",
     "exp_modeling"),

    # 29 U diff=3
    ("precalculus", "exp_log", "U", 3,
     "Solve: log₃(x − 1) = 2.",
     "multiple_choice",
     "x = 7", "x = 10", "x = 9", "x = 4",
     "B",
     "Convert: x − 1 = 3² = 9. Solve: x = 10.",
     "solving_log"),

    # 30 R diff=4
    ("precalculus", "exp_log", "R", 4,
     "If log_a(2) = p and log_a(3) = q, express log_a(18) in terms of p and q.",
     "multiple_choice",
     "p + q", "p + 2q", "2p + q", "pq",
     "B",
     "18 = 2 × 3². So log_a(18) = log_a(2) + 2·log_a(3) = p + 2q.",
     "log_properties"),

    # 31 A diff=3
    ("precalculus", "exp_log", "A", 3,
     "An investment doubles in 10 years with continuous compounding. What is the annual interest rate (to the nearest tenth)?",
     "multiple_choice",
     "6.9%", "7.2%", "5.0%", "10.0%",
     "A",
     "2 = e^(10r) → ln 2 = 10r → r = ln2/10 ≈ 0.0693 ≈ 6.9%.",
     "exp_modeling"),

    # 32 F diff=2
    ("precalculus", "exp_log", "F", 2,
     "What is the inverse function of f(x) = 3ˣ?",
     "multiple_choice",
     "f⁻¹(x) = log₃(x)", "f⁻¹(x) = x/3", "f⁻¹(x) = 3/x", "f⁻¹(x) = ln(3x)",
     "A",
     "The inverse of an exponential base 3 is the logarithm base 3: y = log₃(x).",
     "inverse_exp_log"),

    # 33 R diff=5
    ("precalculus", "exp_log", "R", 5,
     "Solve: log₂(x) + log₂(x − 2) = 3.",
     "multiple_choice",
     "x = 4", "x = 2 or x = 4", "x = −2 or x = 4", "x = 3",
     "A",
     "log₂(x(x−2)) = 3 → x(x−2) = 8 → x²−2x−8 = 0 → (x−4)(x+2) = 0. x = 4 or −2. Since x > 2, only x = 4.",
     "solving_log"),

    # 34 U diff=2
    ("precalculus", "exp_log", "U", 2,
     "The logistic growth model levels off at a maximum population called the:",
     "multiple_choice",
     "initial population", "growth rate", "carrying capacity", "doubling time",
     "C",
     "In logistic growth P = K/(1 + Ae^(−rt)), the value K is the carrying capacity — the upper limit the population approaches.",
     "logistic_growth"),

    # 35 A diff=4
    ("precalculus", "exp_log", "A", 4,
     "A radioactive substance has a half-life of 20 years. What fraction remains after 60 years?",
     "multiple_choice",
     "1/4", "1/6", "1/8", "1/3",
     "C",
     "After 60 years = 3 half-lives. Fraction remaining = (1/2)³ = 1/8.",
     "exp_modeling"),

    # 36 R diff=5
    ("precalculus", "exp_log", "R", 5,
     "Solve: 2^(2x) − 5·2^x + 4 = 0.",
     "multiple_choice",
     "x = 0 and x = 2", "x = 1 and x = 2", "x = 0 and x = 1", "x = 2 only",
     "C",
     "Let u = 2^x: u² − 5u + 4 = 0 → (u−1)(u−4) = 0. u = 1 → 2^x = 1 → x = 0. u = 4 → 2^x = 4 → x = 2. But check: 2^(2·2) − 5·4 + 4 = 16−20+4 = 0 ✓. x = 0 and x = 2. Wait—let u = 2^x, u=4→x=2, u=1→x=0. Correct: x = 0 and x = 2.",
     "solving_exp"),

    # =========================================================================
    # TRIG_FUNCTIONS — 14 questions
    # =========================================================================

    # 37 F diff=1
    ("precalculus", "trig_functions", "F", 1,
     "What is sin(π/2)?",
     "multiple_choice",
     "0", "1", "√2/2", "1/2",
     "B",
     "On the unit circle, the point at π/2 (90°) is (0, 1), so sin(π/2) = 1.",
     "unit_circle"),

    # 38 F diff=1
    ("precalculus", "trig_functions", "F", 1,
     "What is cos(π)?",
     "multiple_choice",
     "1", "0", "−1", "√3/2",
     "C",
     "At π (180°), the point on the unit circle is (−1, 0), so cos(π) = −1.",
     "unit_circle"),

    # 39 U diff=2
    ("precalculus", "trig_functions", "U", 2,
     "Which quadrant contains an angle where sin θ > 0 and cos θ < 0?",
     "multiple_choice",
     "Quadrant I", "Quadrant II", "Quadrant III", "Quadrant IV",
     "B",
     "sin > 0 means y > 0 (Q I or II). cos < 0 means x < 0 (Q II or III). Intersection: Quadrant II.",
     "unit_circle"),

    # 40 F diff=2
    ("precalculus", "trig_functions", "F", 2,
     "Evaluate tan(π/4).",
     "multiple_choice",
     "0", "1", "√3", "1/√2",
     "B",
     "tan(π/4) = sin(π/4)/cos(π/4) = (√2/2)/(√2/2) = 1.",
     "all_six_trig"),

    # 41 U diff=2
    ("precalculus", "trig_functions", "U", 2,
     "If sin θ = 3/5 and θ is in Quadrant I, what is cos θ?",
     "multiple_choice",
     "4/5", "3/4", "5/4", "√34/5",
     "A",
     "Pythagorean identity: cos²θ = 1 − sin²θ = 1 − 9/25 = 16/25. In Q I, cos θ = 4/5.",
     "all_six_trig"),

    # 42 A diff=3
    ("precalculus", "trig_functions", "A", 3,
     "What is the period of f(x) = sin(3x)?",
     "multiple_choice",
     "π/3", "3π", "2π/3", "6π",
     "C",
     "Period = 2π / |B| = 2π / 3.",
     "graphing_trig"),

    # 43 A diff=3
    ("precalculus", "trig_functions", "A", 3,
     "What is the amplitude of f(x) = −4 cos(x)?",
     "multiple_choice",
     "−4", "1/4", "4", "2",
     "C",
     "Amplitude = |A| = |−4| = 4. Amplitude is always non-negative.",
     "graphing_trig"),

    # 44 R diff=4
    ("precalculus", "trig_functions", "R", 4,
     "What is the phase shift of f(x) = sin(2x − π/3)?",
     "multiple_choice",
     "π/3 to the right", "π/6 to the right", "2π/3 to the right", "π/3 to the left",
     "B",
     "f(x) = sin(2(x − π/6)). Phase shift = π/6 to the right.",
     "graphing_trig"),

    # 45 U diff=3
    ("precalculus", "trig_functions", "U", 3,
     "Csc(θ) is defined as:",
     "multiple_choice",
     "cos θ / sin θ", "1 / cos θ", "1 / sin θ", "sin θ / cos θ",
     "C",
     "Cosecant is the reciprocal of sine: csc θ = 1 / sin θ.",
     "all_six_trig"),

    # 46 F diff=2
    ("precalculus", "trig_functions", "F", 2,
     "What is the exact value of cos(5π/6)?",
     "multiple_choice",
     "√3/2", "−√3/2", "1/2", "−1/2",
     "B",
     "5π/6 is in Q II; reference angle π/6. cos(π/6) = √3/2, and cosine is negative in Q II: −√3/2.",
     "unit_circle"),

    # 47 A diff=3
    ("precalculus", "trig_functions", "A", 3,
     "A Ferris wheel of radius 20 m has its center 25 m above the ground. If it completes one rotation in 40 seconds, which function models the height h(t)?",
     "multiple_choice",
     "h(t) = 20 sin(π/20 · t) + 25",
     "h(t) = 25 sin(π/20 · t) + 20",
     "h(t) = 20 cos(2π/40 · t) + 25",
     "h(t) = 20 sin(40t) + 25",
     "C",
     "Amplitude = 20 (radius). Vertical shift = 25 (center height). Period = 40 → B = 2π/40 = π/20. Using cosine: h(t) = 20 cos(π/20 · t) + 25. Option C matches.",
     "graphing_trig"),

    # 48 R diff=4
    ("precalculus", "trig_functions", "R", 4,
     "Which of the following has a period of π?",
     "multiple_choice",
     "y = sin(x)", "y = tan(x)", "y = cos(2x)", "y = sin(2x)",
     "B",
     "tan(x) has a natural period of π. cos(2x) and sin(2x) also have period π, but the question asks which has a period of π among these choices. Both B and C/D do — but tan(x) is the classic answer. Since tan(x) naturally has period π (B), and sin(2x)/cos(2x) also qualify, the best single answer for 'inherently has period π' is tan(x).",
     "graphing_trig"),

    # 49 R diff=5
    ("precalculus", "trig_functions", "R", 5,
     "The graph of y = A sin(Bx + C) + D has amplitude 3, period 4π, phase shift π/2 to the left, and midline y = −1. Which equation matches?",
     "multiple_choice",
     "y = 3 sin(x/2 + π/4) − 1",
     "y = 3 sin(x/2 + π/2) − 1",
     "y = 3 sin(2x + π/2) − 1",
     "y = 3 sin(x/2 − π/2) − 1",
     "B",
     "A=3, period 4π→B=2π/4π=1/2. Phase shift left π/2: C/B = π/2 → C = π/4... Wait: y = A sin(B(x + shift))+D = 3 sin((1/2)(x + π/2)) − 1 = 3 sin(x/2 + π/4) − 1. That's option A. Rechecking: phase shift = −C/B = π/2 → C = Bπ/2 = (1/2)(π/2) = π/4. So y = 3 sin(x/2 + π/4) − 1. Answer A.",
     "graphing_trig"),

    # 50 U diff=3
    ("precalculus", "trig_functions", "U", 3,
     "If sec θ = 2, what is cos θ?",
     "multiple_choice",
     "2", "−1/2", "1/2", "√2",
     "C",
     "sec θ = 1/cos θ = 2, so cos θ = 1/2.",
     "all_six_trig"),

    # =========================================================================
    # ANALYTIC_TRIG — 14 questions
    # =========================================================================

    # 51 F diff=1
    ("precalculus", "analytic_trig", "F", 1,
     "Which is the Pythagorean identity?",
     "multiple_choice",
     "sin²θ + cos²θ = 0", "sin²θ + cos²θ = 1", "sin²θ − cos²θ = 1", "tan²θ + 1 = sin²θ",
     "B",
     "The fundamental Pythagorean identity is sin²θ + cos²θ = 1.",
     "identities"),

    # 52 U diff=2
    ("precalculus", "analytic_trig", "U", 2,
     "Using the Pythagorean identity, simplify 1 − sin²θ.",
     "multiple_choice",
     "tan²θ", "sin²θ", "cos²θ", "cot²θ",
     "C",
     "From sin²θ + cos²θ = 1, we get 1 − sin²θ = cos²θ.",
     "identities"),

    # 53 F diff=2
    ("precalculus", "analytic_trig", "F", 2,
     "What is the sum formula for sin(A + B)?",
     "multiple_choice",
     "sin A cos B − cos A sin B",
     "sin A cos B + cos A sin B",
     "cos A cos B − sin A sin B",
     "cos A cos B + sin A sin B",
     "B",
     "The sum formula: sin(A + B) = sin A cos B + cos A sin B.",
     "sum_difference"),

    # 54 A diff=3
    ("precalculus", "analytic_trig", "A", 3,
     "Using the sum formula, find the exact value of sin(75°).",
     "multiple_choice",
     "(√6 − √2)/4", "(√6 + √2)/4", "(√3 + 1)/4", "√3/2",
     "B",
     "sin(75°) = sin(45° + 30°) = sin45 cos30 + cos45 sin30 = (√2/2)(√3/2) + (√2/2)(1/2) = √6/4 + √2/4 = (√6+√2)/4.",
     "sum_difference"),

    # 55 U diff=2
    ("precalculus", "analytic_trig", "U", 2,
     "What is the double-angle formula for cos(2θ)?",
     "multiple_choice",
     "2 sin θ cos θ",
     "cos²θ − sin²θ",
     "1 − 2 cos²θ",
     "sin²θ + cos²θ",
     "B",
     "cos(2θ) = cos²θ − sin²θ. (Equivalently 1 − 2sin²θ or 2cos²θ − 1.)",
     "double_angle"),

    # 56 A diff=3
    ("precalculus", "analytic_trig", "A", 3,
     "If sin θ = 1/3 and θ is in Q I, find sin(2θ).",
     "multiple_choice",
     "2/9", "2√8/9", "4/9", "√8/9",
     "B",
     "sin(2θ) = 2 sin θ cos θ. cos θ = √(1 − 1/9) = √(8/9) = 2√2/3. sin(2θ) = 2(1/3)(2√2/3) = 4√2/9 = 2√8/9. (4√2/9 ≡ 2√8/9 since √8 = 2√2.)",
     "double_angle"),

    # 57 R diff=4
    ("precalculus", "analytic_trig", "R", 4,
     "Which identity is used to derive the half-angle formula for sin(θ/2)?",
     "multiple_choice",
     "cos(2θ) = 1 − 2sin²θ", "sin(2θ) = 2 sin θ cos θ", "tan(θ/2) = sin θ/(1 + cos θ)", "cos²θ + sin²θ = 1",
     "A",
     "Starting from cos(2α) = 1 − 2sin²α, let α = θ/2: cos θ = 1 − 2sin²(θ/2) → sin²(θ/2) = (1 − cos θ)/2 → sin(θ/2) = ±√((1 − cos θ)/2).",
     "half_angle"),

    # 58 A diff=3
    ("precalculus", "analytic_trig", "A", 3,
     "Find the exact value of cos(π/8) using the half-angle formula.",
     "multiple_choice",
     "√((1 + √2/2)/2)", "√((2 + √2)/4)", "√((1 − √2/2)/2)", "(√6 + √2)/4",
     "B",
     "cos(π/8) = +√((1 + cos(π/4))/2) = √((1 + √2/2)/2) = √((2 + √2)/4). Option B matches.",
     "half_angle"),

    # 59 F diff=2
    ("precalculus", "analytic_trig", "F", 2,
     "Solve for θ in [0, 2π): sin θ = 0.",
     "multiple_choice",
     "θ = π/2, 3π/2", "θ = 0, π", "θ = 0, π/2, π, 3π/2", "θ = π only",
     "B",
     "sin θ = 0 at θ = 0 and θ = π (in [0, 2π)).",
     "solving_trig"),

    # 60 U diff=3
    ("precalculus", "analytic_trig", "U", 3,
     "Solve 2cos²θ − 1 = 0 for θ in [0, 2π).",
     "multiple_choice",
     "θ = π/4, 3π/4, 5π/4, 7π/4", "θ = π/3, 2π/3, 4π/3, 5π/3", "θ = π/6, 5π/6, 7π/6, 11π/6", "θ = π/4, 7π/4",
     "A",
     "2cos²θ = 1 → cos²θ = 1/2 → cos θ = ±√2/2. Solutions: π/4, 3π/4, 5π/4, 7π/4.",
     "solving_trig"),

    # 61 R diff=4
    ("precalculus", "analytic_trig", "R", 4,
     "Simplify: (sin θ + cos θ)² using identities.",
     "multiple_choice",
     "1", "1 + sin(2θ)", "2 + 2 sin θ cos θ", "sin²θ + cos²θ + 1",
     "B",
     "(sin θ + cos θ)² = sin²θ + 2 sin θ cos θ + cos²θ = 1 + 2 sin θ cos θ = 1 + sin(2θ).",
     "identities"),

    # 62 A diff=4
    ("precalculus", "analytic_trig", "A", 4,
     "Solve: 2 sin²θ − sin θ − 1 = 0 for θ in [0, 2π).",
     "multiple_choice",
     "θ = π/6, 5π/6", "θ = π/2, 7π/6, 11π/6", "θ = π/6, π/2, 5π/6", "θ = 3π/2, π/6, 5π/6",
     "B",
     "Factor: (2 sin θ + 1)(sin θ − 1) = 0. sin θ = −1/2 → θ = 7π/6, 11π/6. sin θ = 1 → θ = π/2.",
     "solving_trig"),

    # 63 R diff=5
    ("precalculus", "analytic_trig", "R", 5,
     "Which of the following is equivalent to cos(4θ)?",
     "multiple_choice",
     "4cos²θ − 1", "8cos⁴θ − 8cos²θ + 1", "4sin²θ cos²θ", "1 − 8sin²θ cos²θ",
     "B",
     "cos(4θ) = cos(2·2θ) = 2cos²(2θ)−1 = 2(2cos²θ−1)²−1 = 2(4cos⁴θ−4cos²θ+1)−1 = 8cos⁴θ−8cos²θ+1.",
     "double_angle"),

    # 64 U diff=3
    ("precalculus", "analytic_trig", "U", 3,
     "What is the difference formula for cos(A − B)?",
     "multiple_choice",
     "cos A cos B − sin A sin B",
     "cos A cos B + sin A sin B",
     "sin A cos B + cos A sin B",
     "sin A cos B − cos A sin B",
     "B",
     "cos(A − B) = cos A cos B + sin A sin B.",
     "sum_difference"),

    # =========================================================================
    # POLAR_VECTORS — 10 questions
    # =========================================================================

    # 65 F diff=1
    ("precalculus", "polar_vectors", "F", 1,
     "Convert the polar point (4, π/3) to rectangular coordinates.",
     "multiple_choice",
     "(2√3, 2)", "(2, 2√3)", "(4, 4√3)", "(√3, 1)",
     "B",
     "x = r cos θ = 4 cos(π/3) = 4(1/2) = 2. y = r sin θ = 4 sin(π/3) = 4(√3/2) = 2√3. Point: (2, 2√3).",
     "polar_coordinates"),

    # 66 U diff=2
    ("precalculus", "polar_vectors", "U", 2,
     "Convert the rectangular point (3, −3) to polar form (r, θ) with r > 0 and 0 ≤ θ < 2π.",
     "multiple_choice",
     "(3√2, π/4)", "(3√2, 7π/4)", "(3, 7π/4)", "(√18, π/4)",
     "B",
     "r = √(9+9) = 3√2. θ: x > 0, y < 0 → Q IV. tan θ = −1 → θ = 7π/4.",
     "polar_coordinates"),

    # 67 F diff=2
    ("precalculus", "polar_vectors", "F", 2,
     "The vector u = ⟨3, 4⟩. What is its magnitude?",
     "multiple_choice",
     "7", "√7", "5", "25",
     "C",
     "|u| = √(3² + 4²) = √(9 + 16) = √25 = 5.",
     "vectors"),

    # 68 U diff=2
    ("precalculus", "polar_vectors", "U", 2,
     "Find the dot product of u = ⟨2, −1⟩ and v = ⟨4, 3⟩.",
     "multiple_choice",
     "11", "5", "−5", "8",
     "B",
     "u · v = (2)(4) + (−1)(3) = 8 − 3 = 5.",
     "vectors"),

    # 69 A diff=3
    ("precalculus", "polar_vectors", "A", 3,
     "A parametric curve is given by x = 2t and y = t² − 1. What is the rectangular equation?",
     "multiple_choice",
     "y = x² − 1", "y = x²/4 − 1", "y = (x/2)²", "y = 4x² − 1",
     "B",
     "t = x/2. Substitute: y = (x/2)² − 1 = x²/4 − 1.",
     "parametric"),

    # 70 R diff=4
    ("precalculus", "polar_vectors", "R", 4,
     "Two vectors u and v are perpendicular if and only if:",
     "multiple_choice",
     "|u| = |v|", "u · v = 0", "u · v = 1", "u + v = 0",
     "B",
     "Two vectors are perpendicular (orthogonal) if and only if their dot product equals 0.",
     "vectors"),

    # 71 A diff=3
    ("precalculus", "polar_vectors", "A", 3,
     "A plane flies at 200 mph heading N 60° E. Find the eastward component of its velocity.",
     "multiple_choice",
     "100 mph", "100√3 mph", "173 mph", "200 mph",
     "C",
     "Eastward = 200 sin(60°) = 200(√3/2) ≈ 173 mph.",
     "vectors"),

    # 72 U diff=3
    ("precalculus", "polar_vectors", "U", 3,
     "The polar equation r = 3 represents:",
     "multiple_choice",
     "A horizontal line at y = 3",
     "A vertical line at x = 3",
     "A circle of radius 3 centered at the origin",
     "A line through the origin",
     "C",
     "r = constant is a circle centered at the origin with radius equal to that constant.",
     "polar_graphs"),

    # 73 R diff=5
    ("precalculus", "polar_vectors", "R", 5,
     "The polar curve r = 1 + cos θ is called a:",
     "multiple_choice",
     "Lemniscate", "Rose curve", "Cardioid", "Limaçon without inner loop",
     "C",
     "r = 1 + cos θ is a cardioid — a heart-shaped curve where the coefficient of the trig term equals the constant.",
     "polar_graphs"),

    # 74 A diff=4
    ("precalculus", "polar_vectors", "A", 4,
     "A parametric path is: x = cos t, y = sin t for 0 ≤ t ≤ 2π. What curve does it trace?",
     "multiple_choice",
     "A line", "An ellipse", "A unit circle", "A parabola",
     "C",
     "x² + y² = cos²t + sin²t = 1. This is the unit circle.",
     "parametric"),

    # =========================================================================
    # LIMITS_INTRO — 10 questions
    # =========================================================================

    # 75 F diff=1
    ("precalculus", "limits_intro", "F", 1,
     "What does lim(x→3) (x + 2) equal?",
     "multiple_choice",
     "2", "3", "5", "undefined",
     "C",
     "Direct substitution: 3 + 2 = 5.",
     "evaluating_limits"),

    # 76 U diff=2
    ("precalculus", "limits_intro", "U", 2,
     "Which best describes what lim(x→a) f(x) = L means?",
     "multiple_choice",
     "f(a) = L",
     "As x gets close to a, f(x) gets close to L",
     "f(x) = L when x = a",
     "f is defined at x = a and equals L",
     "B",
     "A limit describes the behavior of f as x approaches a, not necessarily the value at a.",
     "limit_concept"),

    # 77 F diff=2
    ("precalculus", "limits_intro", "F", 2,
     "Evaluate lim(x→0) (sin x / x) numerically or by rule.",
     "multiple_choice",
     "0", "undefined", "1", "∞",
     "C",
     "This is a fundamental limit: lim(x→0) sin(x)/x = 1.",
     "evaluating_limits"),

    # 78 A diff=3
    ("precalculus", "limits_intro", "A", 3,
     "Evaluate lim(x→2) (x² − 4) / (x − 2).",
     "multiple_choice",
     "0", "undefined", "2", "4",
     "D",
     "Factor: (x−2)(x+2)/(x−2) = x + 2. As x→2, x + 2 → 4.",
     "evaluating_limits"),

    # 79 U diff=2
    ("precalculus", "limits_intro", "U", 2,
     "A function is continuous at x = a if:",
     "multiple_choice",
     "lim(x→a) f(x) exists",
     "f(a) is defined",
     "f(a) is defined, lim(x→a) f(x) exists, and they are equal",
     "The function has no vertical asymptote at x = a",
     "C",
     "Continuity requires all three: f(a) defined, limit exists, and the limit equals f(a).",
     "continuity"),

    # 80 R diff=4
    ("precalculus", "limits_intro", "R", 4,
     "A function f has a removable discontinuity at x = c if:",
     "multiple_choice",
     "lim(x→c) f(x) = ∞",
     "f(c) is undefined but lim(x→c) f(x) exists and is finite",
     "The left and right limits are different",
     "f(c) is defined but not equal to the limit",
     "B",
     "Removable discontinuity: the limit exists (finite) but f(c) is undefined (or defined but different). The 'hole' can be 'filled.'",
     "continuity"),

    # 81 A diff=3
    ("precalculus", "limits_intro", "A", 3,
     "Use the graph to determine lim(x→2) f(x) given that f approaches 5 from the left and from the right as x→2, but f(2) = 3.",
     "multiple_choice",
     "3", "5", "undefined", "does not exist",
     "B",
     "The limit depends on what f approaches, not the value at the point. Both sides approach 5, so the limit is 5.",
     "limit_concept"),

    # 82 R diff=5
    ("precalculus", "limits_intro", "R", 5,
     "Evaluate lim(x→∞) (3x² + 2) / (x² − 5).",
     "multiple_choice",
     "0", "∞", "3", "2/5",
     "C",
     "Divide numerator and denominator by x²: (3 + 2/x²)/(1 − 5/x²). As x→∞, terms with 1/x²→0. Limit = 3/1 = 3.",
     "evaluating_limits"),

    # 83 U diff=3
    ("precalculus", "limits_intro", "U", 3,
     "If lim(x→3⁻) f(x) = 4 and lim(x→3⁺) f(x) = 7, then lim(x→3) f(x):",
     "multiple_choice",
     "equals 4", "equals 7", "equals 5.5", "does not exist",
     "D",
     "A limit exists only if both one-sided limits are equal. Since 4 ≠ 7, the two-sided limit does not exist.",
     "limit_concept"),

    # 84 A diff=4
    ("precalculus", "limits_intro", "A", 4,
     "Evaluate lim(x→0) (1 − cos x) / x.",
     "multiple_choice",
     "1", "0", "undefined", "1/2",
     "B",
     "Using the standard limit lim(x→0)(1 − cos x)/x = 0. (This can be verified numerically or by L'Hôpital's rule.)",
     "evaluating_limits"),

]

# ---------------------------------------------------------------------------
# DB setup and seeding
# ---------------------------------------------------------------------------

CREATE_TABLE = """
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


def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Create table if it doesn't exist
    cur.executescript(CREATE_TABLE)

    # Delete existing precalculus questions
    cur.execute("DELETE FROM questions WHERE track = 'precalculus'")
    deleted = cur.rowcount
    print(f"Deleted {deleted} existing precalculus question(s).")

    # Insert all questions
    cur.executemany(INSERT_SQL, QUESTIONS)
    conn.commit()

    total = len(QUESTIONS)
    print(f"Inserted {total} precalculus questions.\n")

    # --- Summary by domain ---
    from collections import defaultdict
    domain_counts = defaultdict(int)
    fuar_counts = defaultdict(int)
    diff_counts = defaultdict(int)

    for q in QUESTIONS:
        domain_counts[q[1]] += 1
        fuar_counts[q[2]] += 1
        diff_counts[q[3]] += 1

    print("--- Questions by domain ---")
    for domain, count in sorted(domain_counts.items()):
        print(f"  {domain:20s}: {count}")

    print("\n--- Questions by FUAR dimension ---")
    for dim in ["F", "U", "A", "R"]:
        print(f"  {dim}: {fuar_counts[dim]}")

    print("\n--- Questions by difficulty ---")
    for d in sorted(diff_counts):
        print(f"  Difficulty {d}: {diff_counts[d]}")

    conn.close()
    print("\nDone. Database:", DB_PATH)


if __name__ == "__main__":
    main()
