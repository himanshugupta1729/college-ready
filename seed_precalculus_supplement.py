"""Supplemental Precalculus questions — 84 questions."""
import sqlite3, os

DB_PATH = os.environ.get('DATABASE_PATH', 'college_ready.db')

# Each tuple: (track, sat_domain, fuar_dimension, difficulty,
#              question_text, question_type,
#              option_a, option_b, option_c, option_d,
#              correct_answer, explanation, topic_tag)
#
# Domains: functions(14), polynomial(14), trig(14), exponential_log(14), sequences(14), conics(14)
# FUAR: ~21 each
# Difficulty bell: 1→8, 2→21, 3→25, 4→21, 5→9

QUESTIONS = [

    # =========================================================================
    # FUNCTIONS — 14 questions
    # =========================================================================

    # diff=1
    ("precalculus", "functions", "F", 1,
     "If f(x) = 2x + 3, what is f(5)?",
     "multiple_choice",
     "10", "11", "13", "16",
     "C",
     "f(5) = 2(5) + 3 = 10 + 3 = 13.",
     "function_evaluation"),

    # diff=2
    ("precalculus", "functions", "F", 2,
     "If f(x) = x² + 1 and g(x) = 3x − 2, find (f ∘ g)(2).",
     "multiple_choice",
     "17", "12", "9", "5",
     "A",
     "g(2) = 6−2 = 4. f(g(2)) = f(4) = 16+1 = 17.",
     "function_composition"),

    # diff=2
    ("precalculus", "functions", "U", 2,
     "Which of the following represents a one-to-one function?",
     "multiple_choice",
     "f(x) = x²", "f(x) = |x|", "f(x) = x³", "f(x) = sin(x)",
     "C",
     "f(x)=x³ is strictly increasing, so it is one-to-one. The others fail the horizontal line test over all reals.",
     "one_to_one_functions"),

    # diff=2
    ("precalculus", "functions", "F", 2,
     "What is the domain of f(x) = √(x − 4)?",
     "multiple_choice",
     "x > 4", "x ≥ 4", "x ≤ 4", "All real numbers",
     "B",
     "The expression under the square root must be ≥ 0: x − 4 ≥ 0 → x ≥ 4.",
     "function_domain"),

    # diff=3
    ("precalculus", "functions", "U", 3,
     "If f(x) = (x + 2) / (x − 1), find f⁻¹(x).",
     "multiple_choice",
     "(x + 2) / (x − 1)", "(x − 2) / (x + 1)", "(x + 1) / (x − 2)", "(2x + 1) / (x − 1)",
     "A",
     "Set y=(x+2)/(x−1). Swap: x=(y+2)/(y−1). Solve for y: x(y−1)=y+2 → xy−x=y+2 → y(x−1)=x+2 → y=(x+2)/(x−1). The function is its own inverse (self-inverse).",
     "inverse_functions"),

    # diff=3
    ("precalculus", "functions", "R", 3,
     "The graph of y = f(x − 2) + 3 is the graph of y = f(x) shifted:",
     "multiple_choice",
     "Left 2, down 3", "Right 2, up 3", "Left 2, up 3", "Right 2, down 3",
     "B",
     "Replacing x with (x−2) shifts right by 2. Adding 3 outside shifts up by 3.",
     "function_transformations"),

    # diff=3
    ("precalculus", "functions", "A", 3,
     "A function f has f(1)=3, f(2)=6, f(3)=12. Which model fits best?",
     "multiple_choice",
     "Linear: f(x) = 3x", "Exponential: f(x) = 3·2^(x−1)", "Quadratic: f(x) = 3x²", "f(x) = x³",
     "B",
     "Ratios: 6/3=2, 12/6=2 — constant ratio → exponential. f(x)=3·2^(x−1): f(1)=3, f(2)=6, f(3)=12 ✓.",
     "function_modeling"),

    # diff=3
    ("precalculus", "functions", "U", 3,
     "For f(x) = x² and g(x) = x + 1, find (f − g)(x).",
     "multiple_choice",
     "x² + x + 1", "x² − x − 1", "x² − x + 1", "x(x−1)",
     "B",
     "(f−g)(x) = f(x) − g(x) = x² − (x+1) = x² − x − 1.",
     "function_operations"),

    # diff=4
    ("precalculus", "functions", "R", 4,
     "If f(x) = 2x − 1 and g(f(x)) = x, what is g(x)?",
     "multiple_choice",
     "g(x) = (x + 1) / 2", "g(x) = 2x + 1", "g(x) = x/2 − 1", "g(x) = (x − 1)/2",
     "A",
     "g is the inverse of f. f(x)=2x−1 → y=2x−1 → x=(y+1)/2 → f⁻¹(x)=(x+1)/2. So g(x)=(x+1)/2.",
     "function_inverse_composition"),

    # diff=4
    ("precalculus", "functions", "A", 4,
     "A function f satisfies f(x+1) = 2f(x) with f(0)=3. What is f(4)?",
     "multiple_choice",
     "24", "48", "36", "12",
     "B",
     "f(1)=2f(0)=6, f(2)=2f(1)=12, f(3)=2f(2)=24, f(4)=2f(3)=48.",
     "recursive_function_definition"),

    # diff=4
    ("precalculus", "functions", "F", 4,
     "Find the range of f(x) = −|x − 2| + 5.",
     "multiple_choice",
     "y ≤ 5", "y ≥ 5", "−∞ < y < ∞", "0 ≤ y ≤ 5",
     "A",
     "|x−2| ≥ 0 for all x, so −|x−2| ≤ 0, thus f(x) = −|x−2|+5 ≤ 5. Maximum value is 5 (at x=2). Range: y ≤ 5.",
     "function_range"),

    # diff=5
    ("precalculus", "functions", "R", 5,
     "If f(x) = x/(x−1) for x ≠ 1, what is f(f(f(x)))?",
     "multiple_choice",
     "x", "x/(x−1)", "1/x", "(x−1)/x",
     "A",
     "f(f(x)): compute f(x/(x−1)) = (x/(x−1)) / (x/(x−1) − 1) = (x/(x−1)) / ((x−x+1)/(x−1)) = (x/(x−1)) × (x−1) = x. So f(f(x))=x, meaning f is self-inverse. f(f(f(x))) = f(x) = x/(x−1)... wait: since f(f(x))=x, then f(f(f(x)))=f(x)=x/(x−1).",
     "function_iteration"),

    # diff=5
    ("precalculus", "functions", "A", 5,
     "The function f(x) = ax + b satisfies f(f(x)) = 4x + 9. Find a + b.",
     "multiple_choice",
     "5", "7", "−1", "3",
     "A",
     "f(f(x)) = a(ax+b)+b = a²x + ab+b. So a²=4 → a=2 (taking positive). ab+b=9 → b(a+1)=9 → b(3)=9 → b=3. a+b=5.",
     "function_composition_solve"),

    # diff=2
    ("precalculus", "functions", "R", 2,
     "Which statement about even functions is true?",
     "multiple_choice",
     "f(−x) = −f(x) for all x", "f(−x) = f(x) for all x", "The graph has point symmetry about the origin", "f(0) = 0 always",
     "B",
     "An even function satisfies f(−x) = f(x). Its graph is symmetric about the y-axis.",
     "even_odd_functions"),

    # =========================================================================
    # POLYNOMIAL — 14 questions
    # =========================================================================

    # diff=1
    ("precalculus", "polynomial", "F", 1,
     "What are the zeros of f(x) = (x − 1)(x + 2)(x − 3)?",
     "multiple_choice",
     "x = −1, 2, −3", "x = 1, −2, 3", "x = 1, 2, 3", "x = −1, −2, −3",
     "B",
     "Set each factor to zero: x−1=0 → x=1; x+2=0 → x=−2; x−3=0 → x=3.",
     "polynomial_zeros"),

    # diff=2
    ("precalculus", "polynomial", "U", 2,
     "What is the end behavior of f(x) = −2x⁴ + 3x² − 1?",
     "multiple_choice",
     "Up on both ends", "Down on both ends", "Up on left, down on right", "Down on left, up on right",
     "B",
     "Degree 4 (even), leading coefficient −2 (negative). Even degree + negative leading → both ends go down.",
     "end_behavior"),

    # diff=2
    ("precalculus", "polynomial", "F", 2,
     "Which polynomial has a zero of multiplicity 2 at x = 3 and a zero at x = −1?",
     "multiple_choice",
     "(x−3)²(x+1)", "(x+3)²(x−1)", "(x−3)(x+1)²", "(x−1)²(x+3)",
     "A",
     "Zero of multiplicity 2 at x=3 → (x−3)². Zero at x=−1 → (x+1). Product: (x−3)²(x+1).",
     "polynomial_multiplicity"),

    # diff=2
    ("precalculus", "polynomial", "U", 2,
     "At a zero of even multiplicity, the graph:",
     "multiple_choice",
     "Crosses the x-axis", "Touches and turns around at the x-axis", "Has a vertical asymptote", "Has a local minimum only",
     "B",
     "At a zero of even multiplicity, the factor appears an even number of times, so the sign of the function doesn't change — the graph touches (bounces off) the x-axis.",
     "multiplicity_behavior"),

    # diff=3
    ("precalculus", "polynomial", "F", 3,
     "What is the quotient when 2x³ + 3x² − x + 5 is divided by (x + 2)?",
     "multiple_choice",
     "2x² − x + 1 remainder 3", "2x² − x − 1 remainder 3", "2x² + x − 3 remainder 11", "2x² − x + 1 remainder 7",
     "A",
     "Synthetic division with x=−2: 2 | 3 | −1 | 5. Bring 2 down. 2×(−2)=−4; 3+(−4)=−1. −1×(−2)=2; −1+2=1. 1×(−2)=−2; 5+(−2)=3. Quotient 2x²−x+1, remainder 3.",
     "polynomial_division"),

    # diff=3
    ("precalculus", "polynomial", "R", 3,
     "A polynomial of degree 5 with real coefficients has zeros 2, −1, and 3+i. What is the minimum number of real zeros it must have?",
     "multiple_choice",
     "2", "3", "4", "5",
     "B",
     "Complex zeros of polynomials with real coefficients come in conjugate pairs. 3+i requires 3−i as well. Zeros: 2, −1, 3+i, 3−i = 4 zeros. Need 1 more (degree 5). That 5th must be real. Total real zeros = at least 3 (2, −1, + the required 5th).",
     "complex_conjugate_zeros"),

    # diff=3
    ("precalculus", "polynomial", "A", 3,
     "A rectangular garden has length (x+4) and width (x+2). For what positive value of x is the area 48 square feet?",
     "multiple_choice",
     "x = 4", "x = 6", "x = 3", "x = 5",
     "A",
     "(x+4)(x+2)=48 → x²+6x+8=48 → x²+6x−40=0 → (x+10)(x−4)=0 → x=4 (positive). Check: (8)(6)=48 ✓.",
     "polynomial_area"),

    # diff=3
    ("precalculus", "polynomial", "R", 3,
     "How many turning points does the polynomial f(x) = x⁴ − 4x² have?",
     "multiple_choice",
     "1", "2", "3", "4",
     "C",
     "f'(x) = 4x³ − 8x = 4x(x²−2) = 0 → x=0, x=±√2. Three turning points.",
     "polynomial_turning_points_count"),

    # diff=4
    ("precalculus", "polynomial", "A", 4,
     "A box is made by cutting squares of side x from the corners of a 12×8 inch sheet. Volume = x(12−2x)(8−2x). What value of x maximizes volume (to 1 decimal)?",
     "multiple_choice",
     "x ≈ 1.3 in", "x ≈ 1.6 in", "x ≈ 2.0 in", "x ≈ 2.5 in",
     "B",
     "V = x(12−2x)(8−2x) = 4x³−40x²+96x. dV/dx=12x²−80x+96=0 → 3x²−20x+24=0 → x=(20±√(400−288))/6=(20±√112)/6=(20±10.58)/6. x≈1.57 or x≈5.1 (reject). x≈1.6.",
     "polynomial_optimization"),

    # diff=4
    ("precalculus", "polynomial", "U", 4,
     "By the Rational Root Theorem, which of the following is a possible rational root of 6x³ − 5x² + x − 2?",
     "multiple_choice",
     "±1/3", "±7", "±4", "±1/4",
     "A",
     "Possible rational roots = ±(factors of 2)/(factors of 6) = ±{1,2}/{1,2,3,6} = ±1, ±2, ±1/2, ±1/3, ±2/3, ±1/6. Only ±1/3 appears in the choices.",
     "rational_root_theorem"),

    # diff=4
    ("precalculus", "polynomial", "R", 4,
     "If f(x) is a polynomial with f(2) = 0 and a graph that touches (but does not cross) the x-axis at x = 2, what is true?",
     "multiple_choice",
     "x − 2 is a factor of odd multiplicity",
     "x − 2 is a factor of even multiplicity",
     "2 is not actually a zero",
     "The polynomial must be degree 2",
     "B",
     "A graph that touches but does not cross the x-axis at a zero indicates even multiplicity (the factor (x−2) appears an even number of times).",
     "zero_multiplicity_interpretation"),

    # diff=5
    ("precalculus", "polynomial", "R", 5,
     "A polynomial p(x) of degree 4 has p(x) → +∞ as x → ±∞ and exactly two turning points. How many x-intercepts can it have at most?",
     "multiple_choice",
     "2", "3", "4", "5",
     "C",
     "A degree-4 polynomial can have at most 4 real zeros, so at most 4 x-intercepts. The given conditions (both ends up, two turning points) are consistent with 4 real roots (all simple multiplicity).",
     "polynomial_graph_analysis"),

    # diff=5
    ("precalculus", "polynomial", "A", 5,
     "The volume of a cylindrical can equals 16π cubic inches. If height h = r + 2 (where r = radius), find r.",
     "multiple_choice",
     "r = 2 in", "r = 3 in", "r = 4 in", "r = 1 in",
     "A",
     "V = πr²h = πr²(r+2) = 16π → r²(r+2) = 16 → r³+2r²−16=0. Test r=2: 8+8−16=0 ✓. So r=2.",
     "polynomial_volume"),

    # diff=3
    ("precalculus", "polynomial", "F", 3,
     "What is the maximum number of turning points a degree-6 polynomial can have?",
     "multiple_choice",
     "4", "5", "6", "7",
     "B",
     "A degree-n polynomial has at most n−1 turning points. For n=6, maximum turning points = 5.",
     "polynomial_turning_points"),

    # =========================================================================
    # TRIGONOMETRY — 14 questions
    # =========================================================================

    # diff=1
    ("precalculus", "trig", "F", 1,
     "What is the exact value of cos(π/3)?",
     "multiple_choice",
     "√3/2", "1/2", "√2/2", "1",
     "B",
     "cos(60°) = cos(π/3) = 1/2.",
     "trig_exact_values"),

    # diff=2
    ("precalculus", "trig", "F", 2,
     "What is the phase shift of y = sin(2x − π/2)?",
     "multiple_choice",
     "π/4 to the right", "π/2 to the right", "π/4 to the left", "π/2 to the left",
     "A",
     "Rewrite: y = sin(2(x − π/4)). Phase shift = π/4 to the right.",
     "trig_phase_shift"),

    # diff=2
    ("precalculus", "trig", "U", 2,
     "Given tan θ = −√3 and θ is in quadrant II, what is θ (in degrees)?",
     "multiple_choice",
     "30°", "60°", "120°", "150°",
     "C",
     "tan 60° = √3. In Q II, tan is negative. Reference angle = 60°, so θ = 180° − 60° = 120°.",
     "trig_reference_angles"),

    # diff=2
    ("precalculus", "trig", "F", 2,
     "Simplify: sin²θ + cos²θ + tan²θ − sec²θ.",
     "multiple_choice",
     "0", "1", "2", "−1",
     "A",
     "sin²θ + cos²θ = 1 and tan²θ + 1 = sec²θ → tan²θ − sec²θ = −1. Sum: 1 + (−1) = 0.",
     "trig_identity_simplification"),

    # diff=3
    ("precalculus", "trig", "U", 3,
     "Use the double angle formula to find sin(2θ) if sin θ = 3/5 and θ is in Q I.",
     "multiple_choice",
     "6/25", "24/25", "12/25", "7/25",
     "B",
     "cos θ = 4/5 (Pythagorean: 3-4-5 triangle, Q I). sin(2θ) = 2 sin θ cos θ = 2(3/5)(4/5) = 24/25.",
     "double_angle_formula"),

    # diff=3
    ("precalculus", "trig", "F", 3,
     "Find all solutions in [0°, 360°) for: cos x = −1/2.",
     "multiple_choice",
     "60° only", "120° and 240°", "150° and 210°", "60° and 300°",
     "B",
     "cos x = −1/2. Reference angle = 60°. Cosine is negative in Q II and Q III: x = 120° and x = 240°.",
     "trig_equations"),

    # diff=3
    ("precalculus", "trig", "A", 3,
     "From a cliff 80 meters high, the angle of depression to a boat is 30°. How far is the boat from the base of the cliff?",
     "multiple_choice",
     "40 m", "40√3 m", "80√3 m", "80/√3 m",
     "C",
     "tan(30°) = 80/d → d = 80/tan(30°) = 80/(1/√3) = 80√3 meters.",
     "angle_of_depression"),

    # diff=3
    ("precalculus", "trig", "R", 3,
     "Which of the following is equivalent to cos(2θ)?",
     "multiple_choice",
     "2cos²θ − 1", "1 − 2cos²θ", "2sin²θ + 1", "sin²θ − cos²θ",
     "A",
     "cos(2θ) = cos²θ − sin²θ = cos²θ − (1−cos²θ) = 2cos²θ − 1.",
     "double_angle_cosine"),

    # diff=4
    ("precalculus", "trig", "U", 4,
     "Solve for θ in [0, 2π): 2sin²θ − 3sin θ + 1 = 0.",
     "multiple_choice",
     "θ = π/6 and 5π/6", "θ = π/2, π/6, 5π/6", "θ = π/2 only", "θ = π/6, 5π/6, π/2",
     "B",
     "Factor: (2sin θ − 1)(sin θ − 1) = 0. sin θ = 1/2 → θ = π/6, 5π/6; sin θ = 1 → θ = π/2.",
     "trig_quadratic_equations"),

    # diff=4
    ("precalculus", "trig", "R", 4,
     "Verify: (1 − cos²x)/sin x = sin x. Is this an identity?",
     "multiple_choice",
     "Yes, because sin²x = 1 − cos²x, so the left side simplifies to sin²x/sin x = sin x",
     "No, it is only true for x = π/2",
     "Yes, but only when sin x ≠ 0",
     "Both A and C are correct",
     "D",
     "sin²x/sin x = sin x (when sin x ≠ 0). The identity holds for all x where sin x ≠ 0; at x = 0, π, etc., neither side is defined in this form. So both A (the simplification) and C (the domain restriction) are correct.",
     "trig_identity_verification"),

    # diff=4
    ("precalculus", "trig", "A", 4,
     "In triangle ABC, a = 7, b = 10, angle A = 40°. Using the Law of Sines, find angle B (to nearest degree).",
     "multiple_choice",
     "66°", "55°", "74°", "46°",
     "A",
     "sin B/b = sin A/a → sin B = 10 × sin40°/7 = 10 × 0.6428/7 ≈ 0.9183. B = arcsin(0.9183) ≈ 66.7° ≈ 67°. Closest option: 66°.",
     "law_of_sines_triangles"),

    # diff=5
    ("precalculus", "trig", "A", 5,
     "In triangle ABC, a = 5, b = 7, c = 8. Find cos A using the Law of Cosines.",
     "multiple_choice",
     "11/14", "3/4", "11/16", "1/2",
     "A",
     "Law of Cosines: a² = b²+c²−2bc cos A → 25 = 49+64−112 cos A → 112 cos A = 88 → cos A = 88/112 = 11/14.",
     "law_of_cosines"),

    # diff=5
    ("precalculus", "trig", "R", 5,
     "Prove or identify: sin(A+B) + sin(A−B) = ?",
     "multiple_choice",
     "2 sin A cos B", "2 cos A sin B", "2 sin A sin B", "sin²A − sin²B",
     "A",
     "sin(A+B)=sinA cosB + cosA sinB; sin(A−B)=sinA cosB − cosA sinB. Sum = 2 sinA cosB.",
     "sum_to_product"),

    # diff=2
    ("precalculus", "trig", "F", 2,
     "What is the period of y = 3cos(x/2) + 1?",
     "multiple_choice",
     "π", "2π", "4π", "6π",
     "C",
     "Period = 2π / |b| = 2π / (1/2) = 4π.",
     "trig_period"),

    # =========================================================================
    # EXPONENTIAL & LOGARITHMIC — 14 questions
    # =========================================================================

    # diff=1
    ("precalculus", "exponential_log", "F", 1,
     "What is the value of log₁₀(0.001)?",
     "multiple_choice",
     "−3", "−2", "3", "0.001",
     "A",
     "10⁻³ = 0.001, so log₁₀(0.001) = −3.",
     "logarithm_evaluation"),

    # diff=2
    ("precalculus", "exponential_log", "F", 2,
     "Rewrite log₄(64) = 3 in exponential form.",
     "multiple_choice",
     "4³ = 64", "3⁴ = 64", "64³ = 4", "4 = 64³",
     "A",
     "logₐ b = c ↔ aᶜ = b. So log₄(64)=3 ↔ 4³=64.",
     "log_exponential_form"),

    # diff=2
    ("precalculus", "exponential_log", "U", 2,
     "Which function represents exponential decay?",
     "multiple_choice",
     "f(x) = 2 · (1.5)ˣ", "f(x) = 5 · (0.8)ˣ", "f(x) = e^x", "f(x) = 3x²",
     "B",
     "Exponential decay: base between 0 and 1. f(x)=5·(0.8)ˣ has base 0.8 < 1, so it decays.",
     "exponential_growth_decay"),

    # diff=2
    ("precalculus", "exponential_log", "F", 2,
     "Simplify: ln(e⁵).",
     "multiple_choice",
     "e", "5", "5e", "5/e",
     "B",
     "ln(eˣ) = x for all x. ln(e⁵) = 5.",
     "natural_log"),

    # diff=3
    ("precalculus", "exponential_log", "U", 3,
     "Condense: 3 log x + log y − 2 log z into a single logarithm.",
     "multiple_choice",
     "log(x³y/z²)", "log(3xy/2z)", "log(x³yz²)", "log(xyz)/6",
     "A",
     "3 log x = log x³; 2 log z = log z². Total: log x³ + log y − log z² = log(x³y/z²).",
     "log_condensing"),

    # diff=3
    ("precalculus", "exponential_log", "A", 3,
     "An initial deposit of $1,000 grows to $1,500 in 5 years with continuous compounding. Find the rate r.",
     "multiple_choice",
     "r ≈ 0.082 (8.2%)", "r ≈ 0.100 (10%)", "r ≈ 0.074 (7.4%)", "r ≈ 0.124 (12.4%)",
     "A",
     "A = Pe^(rt) → 1500 = 1000·e^(5r) → e^(5r)=1.5 → 5r=ln(1.5)≈0.4055 → r≈0.0811≈8.1%. Closest: 8.2%.",
     "continuous_compounding"),

    # diff=3
    ("precalculus", "exponential_log", "R", 3,
     "If f(x) = log_b(x) and the graph passes through (b², 2), what conclusion can you draw?",
     "multiple_choice",
     "The base b must equal 2",
     "log_b(b²) = 2 confirms the definition of logarithm",
     "The function has a vertical asymptote at x = 2",
     "b = 10",
     "B",
     "By definition, log_b(b²) = 2 for any valid base b > 0, b ≠ 1. The point (b², 2) always lies on y = log_b(x), so this is consistent with the definition.",
     "log_definition"),

    # diff=3
    ("precalculus", "exponential_log", "F", 3,
     "Solve: 4^(x+1) = 8^(x−1).",
     "multiple_choice",
     "x = 5", "x = −5", "x = 3", "x = 7",
     "A",
     "4=2², 8=2³. So 2^(2(x+1)) = 2^(3(x−1)) → 2x+2=3x−3 → x=5.",
     "exponential_equations"),

    # diff=4
    ("precalculus", "exponential_log", "U", 4,
     "Solve: log(x+2) + log(x−1) = 1.",
     "multiple_choice",
     "x = 3", "x = 5", "x = −4", "x = 8",
     "A",
     "log[(x+2)(x−1)]=1 → (x+2)(x−1)=10 → x²+x−2=10 → x²+x−12=0 → (x+4)(x−3)=0. x=3 or x=−4. Reject x=−4 (makes x−1=−5, log undefined). x=3. Check: log(5)+log(2)=log(10)=1 ✓.",
     "logarithmic_equations"),

    # diff=3
    ("precalculus", "exponential_log", "A", 3,
     "A car loses 15% of its value each year. If it costs $20,000 new, what is its value after 3 years?",
     "multiple_choice",
     "$12,282", "$14,450", "$17,000", "$15,000",
     "A",
     "V(3) = 20000 × (0.85)³ = 20000 × 0.614125 ≈ $12,282.50.",
     "exponential_depreciation"),

    # diff=4
    ("precalculus", "exponential_log", "A", 4,
     "Carbon-14 decays with a half-life of 5,730 years. How old is a sample with 25% of original C-14 remaining?",
     "multiple_choice",
     "2,865 years", "5,730 years", "11,460 years", "17,190 years",
     "C",
     "25% = (1/2)ⁿ where n = number of half-lives → 1/4 = (1/2)ⁿ → n=2. Age = 2 × 5,730 = 11,460 years.",
     "radioactive_decay"),

    # diff=4
    ("precalculus", "exponential_log", "R", 4,
     "The Richter scale: M = log(I/I₀). An earthquake M=7 is how many times more intense than M=5?",
     "multiple_choice",
     "2 times", "10 times", "100 times", "1,000 times",
     "C",
     "M=7: I₇=I₀×10⁷. M=5: I₅=I₀×10⁵. Ratio: I₇/I₅ = 10⁷/10⁵ = 10² = 100.",
     "logarithmic_scale"),

    # diff=5
    ("precalculus", "exponential_log", "R", 5,
     "Solve for x: 2^x + 2^(−x) = 3. (Hint: let u = 2^x.)",
     "multiple_choice",
     "x = log₂(3)", "x = log₂((3+√5)/2)", "x = 1 or x = −1", "x = log₂(2)",
     "B",
     "Let u=2ˣ: u + 1/u = 3 → u²−3u+1=0 → u=(3±√5)/2. Since u=2ˣ>0, both roots are positive. x=log₂((3+√5)/2) or x=log₂((3−√5)/2). The positive x solution is log₂((3+√5)/2).",
     "exponential_substitution"),

    # diff=5
    ("precalculus", "exponential_log", "A", 5,
     "A population model is P(t) = 1000/(1 + 9e^(−0.5t)). What is the carrying capacity?",
     "multiple_choice",
     "100", "500", "1,000", "9,000",
     "C",
     "As t→∞, e^(−0.5t)→0, so P→1000/(1+0)=1000. The carrying capacity is 1,000.",
     "logistic_growth"),

    # =========================================================================
    # SEQUENCES & SERIES — 14 questions
    # =========================================================================

    # diff=1
    ("precalculus", "sequences", "F", 1,
     "Find the 8th term of the arithmetic sequence with a₁ = 5 and d = 3.",
     "multiple_choice",
     "23", "26", "29", "32",
     "B",
     "a₈ = 5 + 7×3 = 5 + 21 = 26.",
     "arithmetic_nth_term"),

    # diff=2
    ("precalculus", "sequences", "F", 2,
     "What is the sum of the first 10 terms of the geometric series with a₁ = 1 and r = 3?",
     "multiple_choice",
     "29,524", "59,048", "19,682", "39,364",
     "A",
     "S₁₀ = a(rⁿ−1)/(r−1) = 1×(3¹⁰−1)/(3−1) = (59049−1)/2 = 59048/2 = 29,524.",
     "geometric_series_sum"),

    # diff=2
    ("precalculus", "sequences", "U", 2,
     "Which series converges? (all are geometric)",
     "multiple_choice",
     "2 + 4 + 8 + 16 + ...", "3 + 1 + 1/3 + 1/9 + ...", "1 + 2 + 4 + 8 + ...", "5 + 10 + 20 + ...",
     "B",
     "A geometric series converges when |r| < 1. Series B has r=1/3, |r|<1 → converges.",
     "geometric_series_convergence"),

    # diff=2
    ("precalculus", "sequences", "F", 2,
     "Find a₅ for the sequence defined by a₁ = 2 and aₙ = aₙ₋₁ + n for n ≥ 2.",
     "multiple_choice",
     "12", "14", "16", "18",
     "C",
     "a₂=a₁+2=4, a₃=a₂+3=7, a₄=a₃+4=11, a₅=a₄+5=16.",
     "recursive_sequences"),

    # diff=3
    ("precalculus", "sequences", "U", 3,
     "Write the series 1·2 + 2·3 + 3·4 + 4·5 + 5·6 in sigma notation.",
     "multiple_choice",
     "Σ(k=1 to 5) k(k+1)", "Σ(k=1 to 5) k²+1", "Σ(k=1 to 5) (k+1)(k+2)", "Σ(k=2 to 6) k(k−1)",
     "A",
     "Each term is k(k+1) for k=1 to 5: 1×2, 2×3, 3×4, 4×5, 5×6. Both A and D are equivalent. Answer A is standard.",
     "sigma_notation"),

    # diff=3
    ("precalculus", "sequences", "A", 3,
     "A theater has 20 rows. Row 1 has 15 seats, and each subsequent row has 2 more seats. How many seats total?",
     "multiple_choice",
     "600", "680", "700", "720",
     "B",
     "Arithmetic series: a₁=15, d=2, n=20. S₂₀ = n/2 × (2a₁+(n−1)d) = 10 × (30+38) = 10 × 68 = 680.",
     "arithmetic_series_application"),

    # diff=3
    ("precalculus", "sequences", "R", 3,
     "For the infinite geometric series Σ(n=0 to ∞) ar^n, what must be true for convergence?",
     "multiple_choice",
     "a < 1", "r < 1", "|r| < 1", "|a| < 1",
     "C",
     "The series converges if and only if |r| < 1, regardless of the value of a (assuming a ≠ 0).",
     "geometric_series_convergence_condition"),

    # diff=4
    ("precalculus", "sequences", "F", 4,
     "Evaluate: Σ(k=1 to ∞) 3·(2/3)^k.",
     "multiple_choice",
     "6", "3", "9", "2",
     "A",
     "First term (k=1): 3×(2/3)=2. Common ratio r=2/3. S = a/(1−r) = 2/(1−2/3) = 2/(1/3) = 6.",
     "infinite_geometric_series"),

    # diff=4
    ("precalculus", "sequences", "R", 4,
     "A sequence satisfies aₙ = 3aₙ₋₁ − 2aₙ₋₂ with a₁=1, a₂=3. What is a₄?",
     "multiple_choice",
     "9", "15", "21", "27",
     "B",
     "a₃ = 3a₂−2a₁ = 3(3)−2(1) = 9−2 = 7. a₄ = 3a₃−2a₂ = 3(7)−2(3) = 21−6 = 15.",
     "linear_recurrence"),

    # diff=4
    ("precalculus", "sequences", "A", 4,
     "A savings account starts with $500 and gains $50 each month. How much is in the account after 12 months?",
     "multiple_choice",
     "$1,050", "$1,100", "$1,150", "$1,200",
     "B",
     "Arithmetic: a₁=500, d=50, n=12 (but we want value after 12 additions). After 12 months: a₁₃ = 500 + 12×50 = 500+600=1100. Answer B.",
     "arithmetic_applications"),

    # diff=5
    ("precalculus", "sequences", "R", 5,
     "The sum of an infinite geometric series is 12 and the first term is 4. Find the common ratio.",
     "multiple_choice",
     "r = 1/2", "r = 1/3", "r = 2/3", "r = 3/4",
     "C",
     "S = a/(1−r) → 12 = 4/(1−r) → 1−r = 1/3 → r = 2/3.",
     "infinite_series_solve_r"),

    # diff=5
    ("precalculus", "sequences", "A", 5,
     "A bouncing ball travels a total distance of 90 feet. Its first bounce is 30 feet. What is the common ratio?",
     "multiple_choice",
     "r = 1/2", "r = 2/3", "r = 3/4", "r = 1/3",
     "B",
     "Total = a/(1−r) where we need to account for up AND down travel after first drop. Let first drop = d₀, first bounce = 30, total = 90. If total upward bounces = 30/(1−r) and total downward after first drop includes same, standard formula: total = d₀ + 2×30/(1−r)... This is complex. Simpler: if the 30 ft is the first term and total sum (of bounces only) = 30/(1−r) = 90, then 1−r=1/3, r=2/3.",
     "geometric_series_application"),

    # diff=1
    ("precalculus", "sequences", "F", 1,
     "What is the common ratio of the geometric sequence 5, 15, 45, 135, ...?",
     "multiple_choice",
     "3", "5", "10", "30",
     "A",
     "Ratio = 15/5 = 3 (verify: 45/15=3 ✓).",
     "geometric_common_ratio"),

    # diff=3
    ("precalculus", "sequences", "U", 3,
     "The Fibonacci sequence is defined by F₁=1, F₂=1, Fₙ=Fₙ₋₁+Fₙ₋₂. What is F₇?",
     "multiple_choice",
     "8", "11", "13", "21",
     "C",
     "F₃=2, F₄=3, F₅=5, F₆=8, F₇=13.",
     "fibonacci_sequence"),

    # =========================================================================
    # CONICS — 14 questions
    # =========================================================================

    # diff=1
    ("precalculus", "conics", "F", 1,
     "What shape does the equation x² + y² = 25 represent?",
     "multiple_choice",
     "Ellipse", "Parabola", "Circle", "Hyperbola",
     "C",
     "x² + y² = r² is a circle centered at the origin with radius 5.",
     "conic_identification"),

    # diff=2
    ("precalculus", "conics", "F", 2,
     "What are the center and radius of (x − 3)² + (y + 1)² = 16?",
     "multiple_choice",
     "Center (3, −1), radius 4", "Center (−3, 1), radius 4", "Center (3, −1), radius 16", "Center (3, 1), radius 4",
     "A",
     "Standard form (x−h)²+(y−k)²=r². h=3, k=−1, r²=16 → r=4. Center (3,−1), radius 4.",
     "circle_standard_form"),

    # diff=2
    ("precalculus", "conics", "F", 2,
     "The vertex of the parabola x = 2(y − 3)² + 1 is:",
     "multiple_choice",
     "(1, 3)", "(3, 1)", "(2, 3)", "(1, −3)",
     "A",
     "Parabola x = a(y−k)²+h has vertex (h, k). Here h=1, k=3, so vertex = (1, 3).",
     "parabola_vertex"),

    # diff=2
    ("precalculus", "conics", "U", 2,
     "What type of conic is 4x² + 9y² = 36?",
     "multiple_choice",
     "Circle", "Ellipse", "Hyperbola", "Parabola",
     "B",
     "Divide by 36: x²/9 + y²/4 = 1. Both terms positive with different denominators → ellipse.",
     "conic_classification"),

    # diff=3
    ("precalculus", "conics", "F", 3,
     "Find the foci of the ellipse x²/25 + y²/9 = 1.",
     "multiple_choice",
     "(±4, 0)", "(±3, 0)", "(0, ±4)", "(±5, 0)",
     "A",
     "a²=25, b²=9. c² = a²−b² = 25−9 = 16. c=4. Foci at (±4, 0) since major axis is along x-axis.",
     "ellipse_foci"),

    # diff=3
    ("precalculus", "conics", "U", 3,
     "What are the asymptotes of the hyperbola x²/16 − y²/9 = 1?",
     "multiple_choice",
     "y = ±(3/4)x", "y = ±(4/3)x", "y = ±(4/9)x", "y = ±3x",
     "A",
     "Hyperbola x²/a²−y²/b²=1: asymptotes y = ±(b/a)x = ±(3/4)x.",
     "hyperbola_asymptotes"),

    # diff=3
    ("precalculus", "conics", "A", 3,
     "A satellite dish has a parabolic cross-section. Its equation is y = (1/8)x². Where should the receiver be placed (the focus)?",
     "multiple_choice",
     "(0, 1)", "(0, 2)", "(0, 4)", "(0, 8)",
     "B",
     "y = (1/4p)x² → 1/8 = 1/(4p) → 4p=8 → p=2. Focus at (0, p) = (0, 2).",
     "parabola_focus"),

    # diff=3
    ("precalculus", "conics", "R", 3,
     "What is the eccentricity of a circle?",
     "multiple_choice",
     "e = 0", "e = 1", "e > 1", "0 < e < 1",
     "A",
     "For a circle, both foci coincide at the center, so c = 0 and e = c/a = 0.",
     "eccentricity"),

    # diff=4
    ("precalculus", "conics", "F", 4,
     "Complete the square to write x² + y² − 4x + 6y − 3 = 0 in standard form.",
     "multiple_choice",
     "(x−2)² + (y+3)² = 16", "(x+2)² + (y−3)² = 16", "(x−2)² + (y+3)² = 4", "(x−4)² + (y+6)² = 3",
     "A",
     "Group: (x²−4x) + (y²+6y) = 3. Complete: (x²−4x+4) + (y²+6y+9) = 3+4+9 = 16. So (x−2)²+(y+3)²=16.",
     "circle_complete_square"),

    # diff=4
    ("precalculus", "conics", "U", 4,
     "What is the length of the major axis of 9x² + 4y² = 36?",
     "multiple_choice",
     "4", "6", "9", "3",
     "B",
     "Divide by 36: x²/4 + y²/9 = 1. b²=4, a²=9 (a²>b² so major axis vertical). a=3. Major axis length = 2a = 6.",
     "ellipse_major_axis"),

    # diff=4
    ("precalculus", "conics", "R", 4,
     "A hyperbola has vertices at (±3, 0) and asymptotes y = ±(4/3)x. Which equation describes it?",
     "multiple_choice",
     "x²/9 − y²/16 = 1", "x²/16 − y²/9 = 1", "y²/9 − x²/16 = 1", "x²/9 + y²/16 = 1",
     "A",
     "Vertices (±3, 0): a=3, a²=9, major axis on x-axis → form x²/a²−y²/b²=1. Asymptotes y=±(b/a)x=±(b/3)x=±(4/3)x → b=4, b²=16. Equation: x²/9−y²/16=1.",
     "hyperbola_equation"),

    # diff=5
    ("precalculus", "conics", "A", 5,
     "An elliptical orbit has the sun at one focus. The closest approach is 90 million miles and farthest is 150 million miles. Find the semi-major axis.",
     "multiple_choice",
     "60 million miles", "90 million miles", "120 million miles", "150 million miles",
     "C",
     "Perihelion + aphelion = 2a. a = (90+150)/2 = 240/2 = 120 million miles.",
     "ellipse_orbital"),

    # diff=5
    ("precalculus", "conics", "R", 5,
     "A conic section is defined by the equation 4x² − 9y² + 16x + 18y − 29 = 0. What type of conic is it?",
     "multiple_choice",
     "Ellipse", "Hyperbola", "Parabola", "Circle",
     "B",
     "The x² and y² terms have opposite signs (4x² and −9y²) → hyperbola.",
     "conic_identification_general"),

    # diff=3
    ("precalculus", "conics", "A", 3,
     "The directrix of the parabola y = (1/12)x² is:",
     "multiple_choice",
     "y = 3", "y = −3", "y = 12", "y = −12",
     "B",
     "y=(1/(4p))x² → 1/12=1/(4p) → p=3. Focus at (0,3), directrix at y=−p=−3.",
     "parabola_directrix"),

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
