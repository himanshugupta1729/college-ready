"""Supplemental Algebra 2 questions — 84 questions."""
import sqlite3, os

DB_PATH = os.environ.get('DATABASE_PATH', 'college_ready.db')

# Each tuple: (track, sat_domain, fuar_dimension, difficulty,
#              question_text, question_type,
#              option_a, option_b, option_c, option_d,
#              correct_answer, explanation, topic_tag)
#
# Domains: polynomials(14), rational(14), exponential_log(14), sequences(14), trig_intro(14), complex(14)
# FUAR: ~21 each (F:21, U:21, A:21, R:21)
# Difficulty bell: 1→8, 2→21, 3→25, 4→21, 5→9

QUESTIONS = [

    # =========================================================================
    # POLYNOMIALS — 14 questions
    # =========================================================================

    # diff=1
    ("algebra_2", "polynomials", "F", 1,
     "What is the degree of the polynomial 5x⁴ − 3x² + 7x − 2?",
     "multiple_choice",
     "2", "3", "4", "5",
     "C",
     "The degree is the highest power of x, which is 4.",
     "polynomial_degree"),

    # diff=2
    ("algebra_2", "polynomials", "F", 2,
     "Divide (x³ − 8) by (x − 2) using synthetic division. What is the quotient?",
     "multiple_choice",
     "x² + 2x + 4", "x² − 2x + 4", "x² + 4x + 4", "x² − 4x + 4",
     "A",
     "x³ − 8 = (x − 2)(x² + 2x + 4) by the difference of cubes factorization a³ − b³ = (a−b)(a²+ab+b²) with a=x, b=2.",
     "polynomial_division"),

    # diff=2
    ("algebra_2", "polynomials", "U", 2,
     "Which of the following is a factor of x³ + 3x² − 4x − 12?",
     "multiple_choice",
     "x − 3", "x + 2", "x − 2", "x + 4",
     "C",
     "Factor by grouping: x²(x+3) − 4(x+3) = (x²−4)(x+3) = (x−2)(x+2)(x+3). So (x−2) is a factor.",
     "polynomial_factoring"),

    # diff=2
    ("algebra_2", "polynomials", "U", 2,
     "If f(x) = 2x³ − x + 5, what is f(−1)?",
     "multiple_choice",
     "4", "6", "8", "−4",
     "A",
     "f(−1) = 2(−1)³ − (−1) + 5 = −2 + 1 + 5 = 4.",
     "polynomial_evaluation"),

    # diff=3
    ("algebra_2", "polynomials", "F", 3,
     "Which polynomial has roots x = 1, x = −3, and x = 4?",
     "multiple_choice",
     "(x−1)(x+3)(x−4)", "(x+1)(x−3)(x+4)", "(x−1)(x−3)(x+4)", "(x+1)(x+3)(x−4)",
     "A",
     "A root r means the factor is (x − r). Roots 1, −3, 4 give factors (x−1), (x+3), (x−4).",
     "polynomial_roots"),

    # diff=3
    ("algebra_2", "polynomials", "A", 3,
     "A rectangular box has volume V(x) = x³ + 6x² + 11x + 6. If one dimension is (x+1), what are the other two dimensions?",
     "multiple_choice",
     "(x+2) and (x+3)", "(x+3) and (x+4)", "(x+2) and (x+4)", "(x+1) and (x+6)",
     "A",
     "Divide: x³+6x²+11x+6 ÷ (x+1) = x²+5x+6 = (x+2)(x+3). The other dimensions are (x+2) and (x+3).",
     "polynomial_applications"),

    # diff=3
    ("algebra_2", "polynomials", "U", 3,
     "By the Remainder Theorem, what is the remainder when x⁴ − 2x³ + x − 5 is divided by (x − 2)?",
     "multiple_choice",
     "−3", "3", "1", "−1",
     "A",
     "Substitute x=2: 2⁴ − 2(2³) + 2 − 5 = 16 − 16 + 2 − 5 = −3.",
     "remainder_theorem"),

    # diff=3
    ("algebra_2", "polynomials", "R", 3,
     "How many positive real roots can f(x) = x⁵ − 3x³ + x² − 2x + 1 have, according to Descartes' Rule of Signs?",
     "multiple_choice",
     "1 or 3", "0 or 2", "1, 3, or 5", "0, 2, or 4",
     "D",
     "Sign pattern of nonzero coefficients: x⁵(+), −3x³(−), +x²(+), −2x(−), +1(+). Sign changes: +→−, −→+, +→−, −→+ = 4 changes. By Descartes' Rule, the number of positive real roots is 4, 2, or 0.",
     "descartes_rule"),

    # diff=4
    ("algebra_2", "polynomials", "A", 4,
     "The profit P(x) (in thousands) from selling x units is P(x) = −x³ + 6x² − 9x + 4. For what integer value of x (1 ≤ x ≤ 5) is profit maximized?",
     "multiple_choice",
     "x = 1", "x = 2", "x = 3", "x = 5",
     "C",
     "P(1)=−1+6−9+4=0, P(2)=−8+24−18+4=2, P(3)=−27+54−27+4=4, P(4)=−64+96−36+4=0, P(5)=−125+150−45+4=−16. Maximum is P(3)=4 at x=3.",
     "polynomial_optimization"),

    # diff=4
    ("algebra_2", "polynomials", "R", 4,
     "If x = −2 is a zero of f(x) = x³ + ax² + x + 6, what is the value of a?",
     "multiple_choice",
     "1", "−1", "2", "−2",
     "A",
     "f(−2)=0: (−2)³+a(−2)²+(−2)+6=0 → −8+4a−2+6=0 → 4a+−4=0 → 4a=4 → a=1.",
     "polynomial_root_finding"),

    # diff=4
    ("algebra_2", "polynomials", "F", 4,
     "What is the leading coefficient of the product (2x³ − x + 1)(3x² + 4x − 2)?",
     "multiple_choice",
     "5", "6", "8", "−2",
     "B",
     "The leading term of (2x³)(3x²) = 6x⁵. The leading coefficient is 6.",
     "polynomial_multiplication"),

    # diff=4
    ("algebra_2", "polynomials", "R", 4,
     "A polynomial p(x) of degree 3 has p(0)=6, p(1)=0, p(−1)=0, p(2)=0. What is p(x)?",
     "multiple_choice",
     "3(x−1)(x+1)(x−2)", "−3(x−1)(x+1)(x−2)", "6(x−1)(x+1)(x−2)", "3(x+1)(x+1)(x−2)",
     "B",
     "Roots at 1, −1, 2 → p(x) = k(x−1)(x+1)(x−2). At x=0: k(−1)(1)(−2)=2k=6 → k=3. So p(x)=3(x−1)(x+1)(x−2). Check p(0)=3(−1)(1)(−2)=6. ✓",
     "polynomial_construction"),

    # diff=5
    ("algebra_2", "polynomials", "A", 5,
     "Find all real solutions of x⁴ − 5x² + 4 = 0.",
     "multiple_choice",
     "x = ±1 only", "x = ±2 only", "x = ±1 and x = ±2", "x = 1 and x = 4",
     "C",
     "Let u = x²: u² − 5u + 4 = 0 → (u−1)(u−4)=0 → u=1 or u=4 → x=±1 or x=±2.",
     "biquadratic_equations"),

    # diff=5
    ("algebra_2", "polynomials", "R", 5,
     "For the polynomial f(x) = x³ − 6x² + 11x − 6, how many distinct real roots does it have, and what are they?",
     "multiple_choice",
     "One root: x=1", "Two roots: x=1, x=2", "Three roots: x=1, x=2, x=3", "Three roots: x=−1, x=−2, x=−3",
     "C",
     "Test x=1: 1−6+11−6=0 ✓. Factor: (x−1)(x²−5x+6)=(x−1)(x−2)(x−3). Roots: 1, 2, 3.",
     "polynomial_factoring"),

    # =========================================================================
    # RATIONAL — 14 questions
    # =========================================================================

    # diff=1
    ("algebra_2", "rational", "F", 1,
     "Simplify: (x² − 9) / (x + 3).",
     "multiple_choice",
     "x + 3", "x − 3", "x − 9", "x² − 3",
     "B",
     "x²−9 = (x+3)(x−3). Divide by (x+3): answer is x−3, for x≠−3.",
     "rational_simplification"),

    # diff=2
    ("algebra_2", "rational", "F", 2,
     "What are the vertical asymptotes of f(x) = (x+1) / (x² − x − 6)?",
     "multiple_choice",
     "x = 2 and x = −3", "x = 3 and x = −2", "x = −1 only", "x = 1 only",
     "B",
     "Factor denominator: x²−x−6 = (x−3)(x+2). Vertical asymptotes at x=3 and x=−2 (numerator ≠ 0 at these x).",
     "vertical_asymptotes"),

    # diff=2
    ("algebra_2", "rational", "U", 2,
     "What is the horizontal asymptote of f(x) = (3x² + 1) / (x² − 4)?",
     "multiple_choice",
     "y = 0", "y = 3", "y = 1", "No horizontal asymptote",
     "B",
     "Degrees of numerator and denominator are equal (both 2). Horizontal asymptote = ratio of leading coefficients = 3/1 = 3.",
     "horizontal_asymptotes"),

    # diff=2
    ("algebra_2", "rational", "U", 2,
     "Solve: 2/(x−1) = 3/(x+2).",
     "multiple_choice",
     "x = 7", "x = −7", "x = 8", "x = −8",
     "A",
     "Cross-multiply: 2(x+2) = 3(x−1) → 2x+4 = 3x−3 → x = 7.",
     "rational_equations"),

    # diff=3
    ("algebra_2", "rational", "F", 3,
     "Add the rational expressions: 3/(x+2) + 5/(x−1).",
     "multiple_choice",
     "(8x + 7)/((x+2)(x−1))", "(8x − 7)/((x+2)(x−1))", "(8x + 1)/((x+2)(x−1))", "8/(x+1)",
     "A",
     "LCD = (x+2)(x−1). 3(x−1)/LCD + 5(x+2)/LCD = (3x−3+5x+10)/LCD = (8x+7)/((x+2)(x−1)).",
     "rational_addition"),

    # diff=3
    ("algebra_2", "rational", "A", 3,
     "A pipe can fill a pool in 4 hours. Another pipe can fill it in 6 hours. How long do they take together?",
     "multiple_choice",
     "2.4 hours", "3 hours", "5 hours", "2 hours",
     "A",
     "Combined rate = 1/4 + 1/6 = 5/12 per hour. Time = 12/5 = 2.4 hours.",
     "rational_word_problems"),

    # diff=3
    ("algebra_2", "rational", "U", 3,
     "Find the x-intercept(s) of f(x) = (x² − 4x + 3) / (x² − 1).",
     "multiple_choice",
     "x = 1 and x = 3", "x = 3 only", "x = 1 only", "x = −1 and x = 1",
     "B",
     "Set numerator = 0: x²−4x+3=0 → (x−1)(x−3)=0 → x=1 or x=3. But x=1 makes denominator x²−1=0 (hole), so only x=3 is an x-intercept.",
     "rational_intercepts"),

    # diff=3
    ("algebra_2", "rational", "R", 3,
     "Which function has a removable discontinuity (hole) at x = 2?",
     "multiple_choice",
     "f(x) = (x+2)/(x²−4)", "f(x) = (x−2)/(x²−4)", "f(x) = 1/(x−2)", "f(x) = (x²−4)/(x+2)",
     "B",
     "f(x)=(x−2)/(x²−4)=(x−2)/((x−2)(x+2))=1/(x+2) for x≠2. The (x−2) cancels, giving a hole at x=2.",
     "removable_discontinuity"),

    # diff=4
    ("algebra_2", "rational", "A", 4,
     "The cost to produce x items is C(x) = 500 + 20x. The average cost per item is A(x) = C(x)/x. For what x does average cost equal 25?",
     "multiple_choice",
     "x = 50", "x = 100", "x = 200", "x = 500",
     "B",
     "A(x) = (500+20x)/x = 25 → 500+20x = 25x → 500 = 5x → x = 100.",
     "rational_applications"),

    # diff=4
    ("algebra_2", "rational", "R", 4,
     "Solve: (x+1)/(x−2) > 0. Which interval is correct?",
     "multiple_choice",
     "x < −1 or x > 2", "−1 < x < 2", "x < 2", "x > −1",
     "A",
     "Critical values: x=−1, x=2. Sign chart: x<−1: (−)/(−)=+; −1<x<2: (+)/(−)=−; x>2: (+)/(+)=+. Solution: x<−1 or x>2.",
     "rational_inequalities"),

    # diff=4
    ("algebra_2", "rational", "F", 4,
     "Perform the division: (x³ − 2x² + 5x − 4) ÷ (x − 1) using polynomial long division. What is the remainder?",
     "multiple_choice",
     "0", "−1", "1", "2",
     "A",
     "By Remainder Theorem, substitute x=1: 1−2+5−4=0. Remainder is 0.",
     "polynomial_long_division"),

    # diff=4
    ("algebra_2", "rational", "U", 4,
     "What is the oblique asymptote of f(x) = (x² + 3x + 1) / (x + 2)?",
     "multiple_choice",
     "y = x + 1", "y = x − 1", "y = x + 5", "y = x + 3",
     "A",
     "Divide x²+3x+1 by x+2: x²+3x+1 = (x+1)(x+2) − 1. So f(x) = x+1 − 1/(x+2). Oblique asymptote: y = x+1.",
     "oblique_asymptotes"),

    # diff=5
    ("algebra_2", "rational", "A", 5,
     "A cyclist travels 60 miles with the wind and 40 miles against the wind in the same total time. If wind speed is 5 mph, what is the cyclist's speed in still air?",
     "multiple_choice",
     "15 mph", "20 mph", "25 mph", "30 mph",
     "C",
     "Let speed = s. Time: 60/(s+5) = 40/(s−5). Cross-multiply: 60(s−5)=40(s+5) → 60s−300=40s+200 → 20s=500 → s=25.",
     "rational_distance_problems"),

    # diff=5
    ("algebra_2", "rational", "R", 5,
     "For f(x) = (2x² − x − 1) / (x² − 1), what is the correct description of the graph's behavior?",
     "multiple_choice",
     "Hole at x=1, vertical asymptote at x=−1, horizontal asymptote y=2",
     "Vertical asymptotes at x=1 and x=−1, horizontal asymptote y=2",
     "Hole at x=−1, vertical asymptote at x=1, horizontal asymptote y=2",
     "Hole at x=1, hole at x=−1, horizontal asymptote y=2",
     "A",
     "Factor: (2x+1)(x−1) / ((x+1)(x−1)). Cancel (x−1): gives hole at x=1. Remaining denom (x+1)=0 at x=−1: vertical asymptote. Equal degrees → HA y=2/1=2.",
     "rational_graph_analysis"),

    # =========================================================================
    # EXPONENTIAL & LOGARITHMIC — 14 questions
    # =========================================================================

    # diff=1
    ("algebra_2", "exponential_log", "F", 1,
     "Evaluate: log₂(32).",
     "multiple_choice",
     "4", "5", "6", "16",
     "B",
     "2⁵ = 32, so log₂(32) = 5.",
     "logarithm_evaluation"),

    # diff=2
    ("algebra_2", "exponential_log", "F", 2,
     "Which equation is equivalent to log₃(x) = 4?",
     "multiple_choice",
     "x = 3⁴", "x = 4³", "3 = x⁴", "4 = x³",
     "A",
     "logₐ(x) = b means aᵇ = x. So log₃(x)=4 means x = 3⁴ = 81.",
     "log_exponential_conversion"),

    # diff=2
    ("algebra_2", "exponential_log", "U", 2,
     "Expand using logarithm properties: log(x²y / z).",
     "multiple_choice",
     "2log x + log y − log z", "2log x − log y + log z", "log x + 2log y − log z", "2(log x + log y − log z)",
     "A",
     "log(x²y/z) = log(x²) + log(y) − log(z) = 2log x + log y − log z.",
     "log_properties"),

    # diff=2
    ("algebra_2", "exponential_log", "F", 2,
     "Solve: 2ˣ = 16.",
     "multiple_choice",
     "x = 3", "x = 4", "x = 8", "x = 6",
     "B",
     "16 = 2⁴, so x = 4.",
     "exponential_equations"),

    # diff=3
    ("algebra_2", "exponential_log", "U", 3,
     "Solve: log(x) + log(x − 3) = 1.",
     "multiple_choice",
     "x = 5", "x = −2", "x = 5 or x = −2", "x = 10",
     "A",
     "log[x(x−3)] = 1 → x(x−3) = 10 → x²−3x−10 = 0 → (x−5)(x+2) = 0. x=5 or x=−2. Reject x=−2 (log of negative). x=5.",
     "logarithmic_equations"),

    # diff=3
    ("algebra_2", "exponential_log", "A", 3,
     "A population doubles every 12 years. If the current population is 5,000, what will it be in 24 years?",
     "multiple_choice",
     "10,000", "15,000", "20,000", "25,000",
     "C",
     "In 24 years = 2 doubling periods: 5,000 × 2² = 5,000 × 4 = 20,000.",
     "exponential_growth"),

    # diff=3
    ("algebra_2", "exponential_log", "R", 3,
     "Why is log(−5) undefined in the real number system?",
     "multiple_choice",
     "Logarithms are only defined for base > 1",
     "No real power of 10 gives a negative result",
     "Negative numbers have no square roots",
     "The answer would be imaginary",
     "B",
     "Logarithms are inverses of exponential functions. Since 10ˣ > 0 for all real x, there is no real x such that 10ˣ = −5. So log(−5) is undefined over the reals.",
     "log_domain"),

    # diff=3
    ("algebra_2", "exponential_log", "F", 3,
     "Using change of base, evaluate log₅(125).",
     "multiple_choice",
     "2", "3", "4", "5",
     "B",
     "log₅(125) = log(125)/log(5) = log(5³)/log(5) = 3log(5)/log(5) = 3.",
     "change_of_base"),

    # diff=4
    ("algebra_2", "exponential_log", "A", 4,
     "An investment grows continuously at 6% per year. Using A = Pe^(rt), how long (to the nearest year) does it take to triple?",
     "multiple_choice",
     "≈ 12 years", "≈ 18 years", "≈ 20 years", "≈ 25 years",
     "B",
     "3P = Pe^(0.06t) → ln(3) = 0.06t → t = ln(3)/0.06 ≈ 1.0986/0.06 ≈ 18.3 years ≈ 18 years.",
     "continuous_growth"),

    # diff=4
    ("algebra_2", "exponential_log", "U", 4,
     "Solve: 3^(2x−1) = 27^(x+2).",
     "multiple_choice",
     "x = 7", "x = −7", "x = 5", "x = −5",
     "A",
     "27 = 3³ so 3^(2x−1) = 3^(3(x+2)) = 3^(3x+6). Set exponents equal: 2x−1=3x+6 → −x=7 → x=−7.",
     "exponential_equations_same_base"),

    # diff=4
    ("algebra_2", "exponential_log", "R", 4,
     "The half-life of a substance is 5 days. What fraction remains after 20 days?",
     "multiple_choice",
     "1/4", "1/8", "1/16", "1/20",
     "C",
     "20 days = 4 half-lives. Fraction remaining = (1/2)⁴ = 1/16.",
     "half_life"),

    # diff=4
    ("algebra_2", "exponential_log", "A", 4,
     "Solve: 5^x = 200. Express in terms of log base 5.",
     "multiple_choice",
     "x = log₅(200)", "x = log(200)/log(5)", "x = ln(200)/ln(5)", "All of the above are equivalent",
     "D",
     "x = log₅(200) by definition. By change of base: log(200)/log(5) = ln(200)/ln(5). All three are equal.",
     "solving_exponentials"),

    # diff=5
    ("algebra_2", "exponential_log", "R", 5,
     "Solve: log₂(x+1) − log₂(x−1) = 2.",
     "multiple_choice",
     "x = 5/3", "x = 3", "x = 5", "x = 7",
     "A",
     "log₂[(x+1)/(x−1)] = 2 → (x+1)/(x−1) = 4 → x+1 = 4(x−1) = 4x−4 → 5 = 3x → x = 5/3. Domain check: x=5/3>1 ✓, x+1=8/3>0 ✓, x−1=2/3>0 ✓. Verify: log₂((8/3)/(2/3))=log₂(4)=2 ✓.",
     "logarithmic_equations"),

    # diff=5
    ("algebra_2", "exponential_log", "A", 5,
     "A bank offers 8% annual interest compounded quarterly. What is the effective annual rate (EAR)?",
     "multiple_choice",
     "8.00%", "8.16%", "8.24%", "8.32%",
     "C",
     "EAR = (1 + r/n)ⁿ − 1 = (1 + 0.08/4)⁴ − 1 = (1.02)⁴ − 1 = 1.08243 − 1 = 0.08243 ≈ 8.24%.",
     "compound_interest"),

    # =========================================================================
    # SEQUENCES & SERIES — 14 questions
    # =========================================================================

    # diff=1
    ("algebra_2", "sequences", "F", 1,
     "What is the 10th term of the arithmetic sequence 3, 7, 11, 15, ...?",
     "multiple_choice",
     "37", "39", "41", "43",
     "B",
     "Common difference d=4. aₙ = a₁ + (n−1)d = 3 + 9×4 = 3 + 36 = 39.",
     "arithmetic_sequences"),

    # diff=2
    ("algebra_2", "sequences", "F", 2,
     "What is the sum of the first 20 terms of the arithmetic series with a₁ = 2 and d = 5?",
     "multiple_choice",
     "970", "990", "1010", "1030",
     "A",
     "Sₙ = n/2 × (2a₁ + (n−1)d) = 20/2 × (4 + 95) = 10 × 99 = 990. Wait: 2a₁=4, (n−1)d=19×5=95. S₂₀=10×99=990.",
     "arithmetic_series"),

    # diff=2
    ("algebra_2", "sequences", "U", 2,
     "In a geometric sequence, a₁ = 3 and r = 2. What is a₆?",
     "multiple_choice",
     "48", "96", "72", "192",
     "B",
     "aₙ = a₁ × rⁿ⁻¹. a₆ = 3 × 2⁵ = 3 × 32 = 96.",
     "geometric_sequences"),

    # diff=2
    ("algebra_2", "sequences", "F", 2,
     "Find the sum of the infinite geometric series: 8 + 4 + 2 + 1 + ...",
     "multiple_choice",
     "12", "16", "20", "32",
     "B",
     "r = 1/2, |r| < 1. S = a/(1−r) = 8/(1−1/2) = 8/(1/2) = 16.",
     "infinite_geometric_series"),

    # diff=3
    ("algebra_2", "sequences", "U", 3,
     "Which formula represents the nth term of the sequence 2, 6, 18, 54, ...?",
     "multiple_choice",
     "aₙ = 2·3ⁿ⁻¹", "aₙ = 3·2ⁿ⁻¹", "aₙ = 2n + 3", "aₙ = 2ⁿ + 3",
     "A",
     "Ratio between terms: 6/2 = 3, 18/6 = 3. Geometric with a₁=2, r=3. aₙ = 2·3ⁿ⁻¹.",
     "geometric_nth_term"),

    # diff=3
    ("algebra_2", "sequences", "A", 3,
     "A ball dropped from 10 feet bounces to 60% of its previous height each time. What is the total distance it travels before coming to rest?",
     "multiple_choice",
     "25 feet", "40 feet", "50 feet", "60 feet",
     "B",
     "Total distance = initial drop + 2 × (sum of all bounces) = 10 + 2×(6 + 3.6 + 2.16 + ...) = 10 + 2×(6/(1−0.6)) = 10 + 2×15 = 10 + 30 = 40 feet. Formula: D = h(1+r)/(1−r) = 10(1.6/0.4) = 40.",
     "geometric_series_application"),

    # diff=3
    ("algebra_2", "sequences", "R", 3,
     "The nth term of a sequence is aₙ = n² − n. Which sequence does this produce?",
     "multiple_choice",
     "0, 2, 6, 12, 20, ...", "1, 2, 6, 12, 20, ...", "0, 2, 4, 8, 16, ...", "1, 4, 9, 16, 25, ...",
     "A",
     "a₁=1−1=0, a₂=4−2=2, a₃=9−3=6, a₄=16−4=12, a₅=25−5=20. Sequence: 0,2,6,12,20,...",
     "sequence_formulas"),

    # diff=3
    ("algebra_2", "sequences", "U", 3,
     "Sigma notation: evaluate Σ(k=1 to 5) of (2k + 1).",
     "multiple_choice",
     "25", "30", "35", "40",
     "C",
     "Sum = (3)+(5)+(7)+(9)+(11) = 35.",
     "sigma_notation"),

    # diff=4
    ("algebra_2", "sequences", "A", 4,
     "A company's revenue grows geometrically. Revenue in year 1 is $50,000 and in year 3 is $72,000. What is the common ratio?",
     "multiple_choice",
     "r = 1.1", "r = 1.15", "r = 1.2", "r = 1.25",
     "C",
     "a₃ = a₁ × r² → 72,000 = 50,000 × r² → r² = 1.44 → r = 1.2.",
     "geometric_applications"),

    # diff=4
    ("algebra_2", "sequences", "R", 4,
     "For what value of x does the infinite geometric series x + x²/2 + x³/4 + ... converge?",
     "multiple_choice",
     "|x| < 2", "|x| < 1", "x > 0 only", "All real x",
     "A",
     "The series has first term x and ratio x/2. For convergence: |x/2| < 1 → |x| < 2.",
     "series_convergence"),

    # diff=4
    ("algebra_2", "sequences", "F", 4,
     "Evaluate: Σ(k=1 to 100) of k (sum of first 100 positive integers).",
     "multiple_choice",
     "4,950", "5,000", "5,050", "10,100",
     "C",
     "Sₙ = n(n+1)/2 = 100×101/2 = 5,050.",
     "arithmetic_series_formula"),

    # diff=5
    ("algebra_2", "sequences", "R", 5,
     "The terms a₁=2, a₂=6, a₃=18 form a geometric sequence. If a₄ follows the same geometric ratio, what is a₄?",
     "multiple_choice",
     "24", "36", "54", "72",
     "C",
     "Ratio r = 6/2 = 3. a₄ = 18 × 3 = 54.",
     "geometric_nth_term_extension"),

    # diff=5
    ("algebra_2", "sequences", "A", 5,
     "A loan of $10,000 is repaid in 5 equal annual payments at 8% annual interest. Using the annuity formula P = PV·r/(1−(1+r)⁻ⁿ), which payment is closest?",
     "multiple_choice",
     "$2,304", "$2,505", "$2,783", "$3,000",
     "B",
     "P = 10000 × 0.08/(1−(1.08)⁻⁵) = 800/(1−0.6806) = 800/0.3194 ≈ 2505.",
     "annuity_calculations"),

    # diff=2
    ("algebra_2", "sequences", "R", 2,
     "Is the sequence 5, 5, 5, 5, ... arithmetic, geometric, or both?",
     "multiple_choice",
     "Arithmetic only (d=0)", "Geometric only (r=1)", "Both arithmetic (d=0) and geometric (r=1)", "Neither",
     "C",
     "With d=0 it satisfies the arithmetic definition. With r=1 (each term = 1× previous) it satisfies geometric. It is both.",
     "sequence_classification"),

    # =========================================================================
    # TRIG INTRO — 14 questions
    # =========================================================================

    # diff=1
    ("algebra_2", "trig_intro", "F", 1,
     "Convert 135° to radians.",
     "multiple_choice",
     "π/4", "3π/4", "2π/3", "5π/4",
     "B",
     "135° × (π/180°) = 135π/180 = 3π/4.",
     "degree_radian_conversion"),

    # diff=2
    ("algebra_2", "trig_intro", "F", 2,
     "What is sin(π/6)?",
     "multiple_choice",
     "√3/2", "1/2", "√2/2", "1",
     "B",
     "sin(30°) = sin(π/6) = 1/2.",
     "unit_circle_values"),

    # diff=2
    ("algebra_2", "trig_intro", "F", 2,
     "What is the period of y = sin(2x)?",
     "multiple_choice",
     "π", "2π", "π/2", "4π",
     "A",
     "Period of sin(bx) = 2π/b = 2π/2 = π.",
     "trig_period"),

    # diff=2
    ("algebra_2", "trig_intro", "U", 2,
     "In a right triangle, if sin θ = 3/5, what is cos θ?",
     "multiple_choice",
     "4/5", "3/4", "5/3", "5/4",
     "A",
     "sin²θ + cos²θ = 1 → 9/25 + cos²θ = 1 → cos²θ = 16/25 → cos θ = 4/5 (θ in first quadrant).",
     "pythagorean_identity"),

    # diff=3
    ("algebra_2", "trig_intro", "U", 3,
     "What is the amplitude of y = −4 sin(3x + π)?",
     "multiple_choice",
     "3", "4", "π", "−4",
     "B",
     "Amplitude = |A| = |−4| = 4. (Amplitude is always positive.)",
     "trig_amplitude"),

    # diff=3
    ("algebra_2", "trig_intro", "F", 3,
     "Evaluate cos(7π/6).",
     "multiple_choice",
     "−√3/2", "√3/2", "−1/2", "1/2",
     "A",
     "7π/6 is in the third quadrant (π + π/6). Reference angle = π/6. cos(π/6)=√3/2. In Q3, cos is negative: cos(7π/6) = −√3/2.",
     "unit_circle_extension"),

    # diff=3
    ("algebra_2", "trig_intro", "A", 3,
     "A ladder 10 feet long leans against a wall at an angle of 60° with the ground. How high up the wall does it reach?",
     "multiple_choice",
     "5 feet", "5√2 feet", "5√3 feet", "10 feet",
     "C",
     "Height = 10 × sin(60°) = 10 × (√3/2) = 5√3 feet.",
     "trig_right_triangle"),

    # diff=3
    ("algebra_2", "trig_intro", "R", 3,
     "Which quadrant contains an angle θ where sin θ > 0 and cos θ < 0?",
     "multiple_choice",
     "Quadrant I", "Quadrant II", "Quadrant III", "Quadrant IV",
     "B",
     "sin θ > 0 in Q I and Q II. cos θ < 0 in Q II and Q III. The intersection is Quadrant II.",
     "trig_quadrant_signs"),

    # diff=4
    ("algebra_2", "trig_intro", "A", 4,
     "A surveyor observes the top of a 100-foot building from 200 feet away. What is the angle of elevation to the nearest degree?",
     "multiple_choice",
     "23°", "27°", "30°", "63°",
     "B",
     "tan θ = 100/200 = 0.5 → θ = arctan(0.5) ≈ 26.57° ≈ 27°.",
     "angle_of_elevation"),

    # diff=4
    ("algebra_2", "trig_intro", "U", 4,
     "Find all solutions in [0, 2π) for: 2sin²x − sin x − 1 = 0.",
     "multiple_choice",
     "x = π/2 only", "x = 7π/6 and 11π/6", "x = π/2, 7π/6, 11π/6", "x = π/6 and 5π/6",
     "C",
     "Factor: (2sin x + 1)(sin x − 1)=0. sin x=1 → x=π/2; sin x=−1/2 → x=7π/6, 11π/6.",
     "trig_equations"),

    # diff=4
    ("algebra_2", "trig_intro", "R", 4,
     "Which identity is used to simplify sin²x + cos²x into 1?",
     "multiple_choice",
     "Double angle identity", "Pythagorean identity", "Sum-to-product identity", "Reciprocal identity",
     "B",
     "The fundamental Pythagorean identity is sin²x + cos²x = 1.",
     "trig_identities"),

    # diff=5
    ("algebra_2", "trig_intro", "R", 5,
     "Using the Law of Sines, in triangle ABC, angle A = 30°, angle B = 45°, and side a = 8. Find side b.",
     "multiple_choice",
     "8√2", "4√6", "8√3", "4√2",
     "A",
     "Law of Sines: a/sin A = b/sin B → b = a × sin B / sin A = 8 × sin45° / sin30° = 8 × (√2/2) / (1/2) = 8√2.",
     "law_of_sines"),

    # diff=5
    ("algebra_2", "trig_intro", "A", 5,
     "A sinusoidal function models tides: h(t) = 4 sin(πt/6) + 6, where h is height in feet and t is hours. What is the maximum tide height?",
     "multiple_choice",
     "4 feet", "6 feet", "10 feet", "12 feet",
     "C",
     "Maximum of sin = 1. Max height = 4(1) + 6 = 10 feet.",
     "sinusoidal_models"),

    # diff=1
    ("algebra_2", "trig_intro", "F", 1,
     "What is the value of tan(45°)?",
     "multiple_choice",
     "0", "1", "√3", "√2/2",
     "B",
     "tan(45°) = sin(45°)/cos(45°) = (√2/2)/(√2/2) = 1.",
     "trig_exact_values"),

    # =========================================================================
    # COMPLEX NUMBERS — 14 questions
    # =========================================================================

    # diff=1
    ("algebra_2", "complex", "F", 1,
     "Simplify: i⁴.",
     "multiple_choice",
     "i", "−1", "1", "−i",
     "C",
     "i¹=i, i²=−1, i³=−i, i⁴=1. The pattern repeats every 4 powers.",
     "powers_of_i"),

    # diff=2
    ("algebra_2", "complex", "F", 2,
     "Add the complex numbers: (3 + 4i) + (2 − 7i).",
     "multiple_choice",
     "5 + 3i", "5 − 3i", "1 + 11i", "1 − 3i",
     "B",
     "(3+2) + (4−7)i = 5 − 3i.",
     "complex_addition"),

    # diff=2
    ("algebra_2", "complex", "F", 2,
     "Multiply: (2 + 3i)(1 − i).",
     "multiple_choice",
     "5 + i", "2 − 3i", "5 − i", "−1 + i",
     "A",
     "(2)(1)+(2)(−i)+(3i)(1)+(3i)(−i) = 2−2i+3i−3i² = 2+i+3 = 5+i.",
     "complex_multiplication"),

    # diff=2
    ("algebra_2", "complex", "U", 2,
     "What is the complex conjugate of 4 − 5i?",
     "multiple_choice",
     "4 + 5i", "−4 + 5i", "−4 − 5i", "5 + 4i",
     "A",
     "The complex conjugate of (a + bi) is (a − bi). Conjugate of 4−5i is 4+5i.",
     "complex_conjugate"),

    # diff=3
    ("algebra_2", "complex", "F", 3,
     "Divide: (3 + 4i) / (1 + 2i). Simplify.",
     "multiple_choice",
     "(11 + 2i)/5", "(11 − 2i)/5", "(3 + 2i)/5", "1 + i",
     "B",
     "Multiply numerator and denominator by conjugate (1−2i): (3+4i)(1−2i) = 3−6i+4i−8i² = 3−2i+8 = 11−2i. Denominator: (1+2i)(1−2i) = 1+4=5. Result: (11−2i)/5.",
     "complex_division"),

    # diff=3
    ("algebra_2", "complex", "U", 3,
     "Find the absolute value (modulus) of 3 − 4i.",
     "multiple_choice",
     "1", "5", "7", "25",
     "B",
     "|a + bi| = √(a²+b²) = √(9+16) = √25 = 5.",
     "complex_modulus"),

    # diff=3
    ("algebra_2", "complex", "R", 3,
     "Solve for x (real): x² + 9 = 0.",
     "multiple_choice",
     "x = ±3", "x = ±3i", "x = 3 only", "No solution",
     "B",
     "x² = −9 → x = ±√(−9) = ±3i.",
     "complex_solutions"),

    # diff=3
    ("algebra_2", "complex", "A", 3,
     "The solutions to x² − 2x + 5 = 0 are complex. What are they?",
     "multiple_choice",
     "x = 1 ± 2i", "x = 2 ± i", "x = 1 ± 4i", "x = −1 ± 2i",
     "A",
     "Quadratic formula: x = (2 ± √(4−20))/2 = (2 ± √(−16))/2 = (2 ± 4i)/2 = 1 ± 2i.",
     "complex_quadratic_solutions"),

    # diff=4
    ("algebra_2", "complex", "R", 4,
     "If z = 2 + 3i, compute z·z̄ (z times its conjugate).",
     "multiple_choice",
     "4 + 9i", "13", "−5", "1",
     "B",
     "z·z̄ = (2+3i)(2−3i) = 4 − 6i + 6i − 9i² = 4 + 9 = 13 (since i²=−1).",
     "complex_conjugate_product"),

    # diff=4
    ("algebra_2", "complex", "F", 4,
     "Simplify: i²⁷.",
     "multiple_choice",
     "1", "−1", "i", "−i",
     "D",
     "27 mod 4 = 3 (since 27=4×6+3). i³ = −i. So i²⁷ = −i.",
     "powers_of_i"),

    # diff=4
    ("algebra_2", "complex", "U", 4,
     "In the complex number system, which polynomial always has the same number of zeros (counting multiplicity) as its degree?",
     "multiple_choice",
     "Only quadratics", "Only polynomials with real coefficients", "All polynomials over the complex numbers", "Only odd-degree polynomials",
     "C",
     "The Fundamental Theorem of Algebra states every degree-n polynomial (over ℂ) has exactly n zeros (counting multiplicity) in ℂ.",
     "fundamental_theorem_algebra"),

    # diff=4
    ("algebra_2", "complex", "A", 4,
     "If one root of x² + bx + 10 = 0 is (1 + 3i), what is the value of b?",
     "multiple_choice",
     "−2", "2", "−4", "4",
     "A",
     "Conjugate pairs: other root is (1−3i). Sum of roots = −b/1 = 2 → b = −2. Product check: (1+3i)(1−3i) = 1+9=10 ✓.",
     "complex_root_pairs"),

    # diff=5
    ("algebra_2", "complex", "R", 5,
     "Express (1 + i)⁸ in standard form.",
     "multiple_choice",
     "16", "−16", "16i", "0",
     "A",
     "|1+i|=√2, arg=π/4. So (1+i)=(√2)·e^(iπ/4). (1+i)⁸ = (√2)⁸ · e^(i·2π) = 16·1 = 16.",
     "complex_powers"),

    # diff=5
    ("algebra_2", "complex", "A", 5,
     "Which of the following represents the three cube roots of −8?",
     "multiple_choice",
     "−2 only",
     "−2, 1+i√3, 1−i√3",
     "−2, −1+i√3, −1−i√3",
     "2, −1+i√3, −1−i√3",
     "B",
     "Cube roots of −8=8e^(iπ): magnitude 2, arguments (π+2πk)/3 for k=0,1,2 → π/3, π, 5π/3. In rectangular: 2(cos60°+i·sin60°)=1+i√3; 2(cosπ)=−2; 2(cos300°+i·sin300°)=1−i√3.",
     "cube_roots_complex"),

]


def seed():
    conn = sqlite3.connect(DB_PATH)
    inserted = 0
    for q in QUESTIONS:
        exists = conn.execute(
            "SELECT id FROM questions WHERE question_text = ?", (q[4],)
        ).fetchone()
        if not exists:
            conn.execute(
                """INSERT INTO questions (track, sat_domain, fuar_dimension, difficulty,
                question_text, question_type, option_a, option_b, option_c, option_d,
                correct_answer, explanation, topic_tag) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                q,
            )
            inserted += 1
    conn.commit()
    conn.close()
    print(f"[seed] supplement: {inserted} inserted")
    return inserted


if __name__ == "__main__":
    seed()
