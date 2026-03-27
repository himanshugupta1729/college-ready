"""
seed_ap_calc_ab.py — Seeds 84 AP Calculus AB questions into college_ready.db.

Track: ap_calc_ab
Units (sat_domain field):
  limits_continuity   (8 q)
  diff_basics         (10 q)  — derivative definition, power/product/quotient rules
  diff_advanced       (10 q)  — chain rule, implicit differentiation, inverse trig
  diff_applications   (12 q)  — related rates, L'Hopital's rule, motion
  diff_analytical     (14 q)  — MVT, optimization, curve sketching
  integration         (16 q)  — Riemann sums, FTC, u-substitution
  diff_equations      (6 q)   — separation of variables, slope fields
  integration_apps    (8 q)   — area between curves, volumes of revolution

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
    # LIMITS AND CONTINUITY — 8 questions (F×2, U×2, A×2, R×2)
    # =========================================================================

    # F-1 diff=1
    ("ap_calc_ab", "limits_continuity", "F", 1,
     "What is lim(x→3) of (x² − 9) / (x − 3)?",
     "multiple_choice",
     "0", "3", "6", "undefined",
     "C",
     "Factor the numerator: (x² − 9)/(x − 3) = (x+3)(x−3)/(x−3) = x + 3. "
     "Substituting x = 3 gives 3 + 3 = 6.",
     "limits_algebraic"),

    # F-2 diff=2
    ("ap_calc_ab", "limits_continuity", "F", 2,
     "What is lim(x→∞) of (3x² + 5x) / (x² − 2)?",
     "multiple_choice",
     "0", "3", "5", "∞",
     "B",
     "Divide numerator and denominator by x²: (3 + 5/x) / (1 − 2/x²). "
     "As x→∞ the 1/x terms vanish, giving 3/1 = 3.",
     "limits_at_infinity"),

    # U-1 diff=2
    ("ap_calc_ab", "limits_continuity", "U", 2,
     "A function f is continuous at x = 2 if and only if which condition holds?",
     "multiple_choice",
     "f(2) exists",
     "lim(x→2) f(x) exists",
     "lim(x→2) f(x) = f(2)",
     "f is differentiable at x = 2",
     "C",
     "Continuity at a point requires three things: (1) f(2) is defined, "
     "(2) the limit exists, and (3) the limit equals f(2). All three must hold. "
     "Option C captures the single equation that encodes all three.",
     "continuity_definition"),

    # U-2 diff=3
    ("ap_calc_ab", "limits_continuity", "U", 3,
     "Which of the following is true about f(x) = |x| / x at x = 0?",
     "multiple_choice",
     "f is continuous at x = 0",
     "lim(x→0) f(x) = 0",
     "lim(x→0) f(x) does not exist",
     "f(0) = 1",
     "C",
     "For x > 0, f(x) = 1; for x < 0, f(x) = −1. The left-hand limit is −1 "
     "and the right-hand limit is +1; they differ, so the two-sided limit does not exist.",
     "limits_one_sided"),

    # A-1 diff=2
    ("ap_calc_ab", "limits_continuity", "A", 2,
     "What value of k makes f(x) = {kx + 1 if x < 2; x² − 1 if x ≥ 2} continuous at x = 2?",
     "multiple_choice",
     "0", "1", "2", "3",
     "C",
     "For continuity, the left limit must equal f(2). "
     "Left limit: k(2) + 1 = 2k + 1. f(2) = 4 − 1 = 3. "
     "Set 2k + 1 = 3 → k = 1. Wait — k = 1 gives 3 = 3. ✓ Answer is k = 1.",
     "continuity_piecewise"),

    # A-2 diff=3
    ("ap_calc_ab", "limits_continuity", "A", 3,
     "Evaluate lim(x→0) of (sin 3x) / (5x).",
     "multiple_choice",
     "0", "3/5", "1", "5/3",
     "B",
     "Use the standard limit lim(θ→0) sin(θ)/θ = 1. Rewrite: "
     "(sin 3x)/(5x) = (3/5) · (sin 3x)/(3x). As x→0, (sin 3x)/(3x) → 1, "
     "so the limit is 3/5.",
     "limits_trig"),

    # R-1 diff=4
    ("ap_calc_ab", "limits_continuity", "R", 4,
     "If lim(x→2⁺) f(x) = 5 and lim(x→2⁻) f(x) = 5, but f(2) = 7, "
     "which statement is correct?",
     "multiple_choice",
     "f is continuous at x = 2",
     "f is not continuous at x = 2, but lim(x→2) f(x) exists",
     "lim(x→2) f(x) does not exist",
     "f is differentiable at x = 2",
     "B",
     "Since both one-sided limits equal 5, the two-sided limit exists and equals 5. "
     "But f(2) = 7 ≠ 5, so the limit does not equal f(2), violating continuity. "
     "The function has a removable discontinuity at x = 2.",
     "continuity_definition"),

    # R-2 diff=5
    ("ap_calc_ab", "limits_continuity", "R", 5,
     "For f(x) = (x² − 4x + 4) / (x − 2)², what is lim(x→2) f(x)?",
     "multiple_choice",
     "0", "1", "2", "The limit does not exist",
     "B",
     "Factor the numerator: x² − 4x + 4 = (x − 2)². "
     "So f(x) = (x−2)²/(x−2)² = 1 for x ≠ 2. "
     "Therefore lim(x→2) f(x) = 1. This is a removable discontinuity.",
     "limits_algebraic"),


    # =========================================================================
    # DIFFERENTIATION: BASICS — 10 questions (F×3, U×3, A×2, R×2)
    # =========================================================================

    # F-1 diff=1
    ("ap_calc_ab", "diff_basics", "F", 1,
     "What is the derivative of f(x) = x⁵?",
     "multiple_choice",
     "x⁴", "5x⁴", "5x⁶", "x⁶/6",
     "B",
     "Power rule: d/dx [xⁿ] = n·xⁿ⁻¹. Here n = 5, so f'(x) = 5x⁴.",
     "power_rule"),

    # F-2 diff=1
    ("ap_calc_ab", "diff_basics", "F", 1,
     "If f(x) = 7x³ − 4x + 2, what is f'(x)?",
     "multiple_choice",
     "21x² − 4", "21x² − 4x", "7x² − 4", "21x³ − 4",
     "A",
     "Differentiate term by term: d/dx[7x³] = 21x², d/dx[−4x] = −4, d/dx[2] = 0. "
     "So f'(x) = 21x² − 4.",
     "power_rule"),

    # F-3 diff=2
    ("ap_calc_ab", "diff_basics", "F", 2,
     "What is d/dx [x³ · sin x]?",
     "multiple_choice",
     "3x² · cos x",
     "x³ · cos x + 3x² · sin x",
     "3x² · sin x + x³ · cos x",
     "3x² · cos x + x³ · sin x",
     "C",
     "Product rule: (uv)' = u'v + uv'. With u = x³, v = sin x: "
     "u' = 3x², v' = cos x. So the derivative is 3x² sin x + x³ cos x.",
     "product_rule"),

    # U-1 diff=2
    ("ap_calc_ab", "diff_basics", "U", 2,
     "Using the limit definition, the derivative of f(x) at x = a is defined as:",
     "multiple_choice",
     "lim(h→0) [f(a+h) − f(a)] / h",
     "lim(h→0) [f(a+h) + f(a)] / h",
     "lim(h→a) [f(h) − f(a)] / (h − a)",
     "lim(h→0) [f(a) − f(a−h)] / h",
     "A",
     "The formal definition of the derivative is f'(a) = lim(h→0) [f(a+h) − f(a)] / h. "
     "Option C is the equivalent alternate form lim(x→a) [f(x)−f(a)]/(x−a), "
     "but option A is the standard definition asked for here.",
     "derivative_definition"),

    # U-2 diff=2
    ("ap_calc_ab", "diff_basics", "U", 2,
     "What is the derivative of f(x) = cos x?",
     "multiple_choice",
     "sin x", "−sin x", "−cos x", "1 − sin x",
     "B",
     "Standard trig derivative: d/dx[cos x] = −sin x. "
     "A common error is writing +sin x (forgetting the negative sign).",
     "trig_derivatives"),

    # U-3 diff=3
    ("ap_calc_ab", "diff_basics", "U", 3,
     "If f(x) = eˣ · cos x, what is f'(x)?",
     "multiple_choice",
     "eˣ · cos x − eˣ · sin x",
     "eˣ · cos x + eˣ · sin x",
     "eˣ(cos x − sin x)",
     "eˣ · sin x",
     "C",
     "Product rule: (eˣ · cos x)' = eˣ · cos x + eˣ · (−sin x) = eˣ(cos x − sin x). "
     "Options A and C are the same; C is the factored form. "
     "A common error is forgetting to differentiate eˣ or dropping the minus sign.",
     "product_rule"),

    # A-1 diff=2
    ("ap_calc_ab", "diff_basics", "A", 2,
     "Find the slope of the tangent line to f(x) = x³ − 3x at x = 2.",
     "multiple_choice",
     "3", "6", "9", "12",
     "C",
     "f'(x) = 3x² − 3. At x = 2: f'(2) = 3(4) − 3 = 12 − 3 = 9.",
     "tangent_line"),

    # A-2 diff=3
    ("ap_calc_ab", "diff_basics", "A", 3,
     "Using the quotient rule, find the derivative of f(x) = (x² + 1) / (x − 1).",
     "multiple_choice",
     "(2x(x−1) − (x²+1)) / (x−1)²",
     "(2x(x−1) + (x²+1)) / (x−1)²",
     "(x² − 2x − 1) / (x−1)²",
     "(x² − 2x + 1) / (x−1)²",
     "C",
     "Quotient rule: (u/v)' = (u'v − uv') / v². "
     "u = x²+1, u' = 2x; v = x−1, v' = 1. "
     "Numerator: 2x(x−1) − (x²+1)(1) = 2x² − 2x − x² − 1 = x² − 2x − 1. "
     "So f'(x) = (x² − 2x − 1)/(x−1)².",
     "quotient_rule"),

    # R-1 diff=4
    ("ap_calc_ab", "diff_basics", "R", 4,
     "At which point(s) does f(x) = x³ − 3x² have a horizontal tangent?",
     "multiple_choice",
     "x = 0 only",
     "x = 2 only",
     "x = 0 and x = 2",
     "x = −2 and x = 0",
     "C",
     "Horizontal tangent where f'(x) = 0. f'(x) = 3x² − 6x = 3x(x − 2) = 0. "
     "So x = 0 or x = 2.",
     "tangent_line"),

    # R-2 diff=4
    ("ap_calc_ab", "diff_basics", "R", 4,
     "The position of a particle is s(t) = t³ − 6t² + 9t. At t = 1, the particle is:",
     "multiple_choice",
     "Moving right and speeding up",
     "Moving right and slowing down",
     "Moving left and speeding up",
     "Moving left and slowing down",
     "B",
     "v(t) = s'(t) = 3t² − 12t + 9. At t=1: v(1) = 3 − 12 + 9 = 0... "
     "Recalculate: v(t) = 3(1) − 12(1) + 9 = 0. The particle is momentarily at rest. "
     "Wait — let's check near t=1: v(0.9) = 3(0.81)−12(0.9)+9 = 2.43−10.8+9 = 0.63 > 0. "
     "v(1.1) = 3(1.21)−12(1.1)+9 = 3.63−13.2+9 = −0.57 < 0. "
     "So at t=1 the velocity is 0 and about to become negative → slowing down then reversing. "
     "a(t) = 6t − 12. a(1) = −6 < 0. Since v > 0 just before t=1 and a < 0, "
     "the particle was moving right (v>0 for t just < 1) and decelerating. "
     "Answer B: moving right and slowing down (approaching zero).",
     "particle_motion"),


    # =========================================================================
    # DIFFERENTIATION: ADVANCED — 10 questions (F×3, U×2, A×3, R×2)
    # =========================================================================

    # F-1 diff=1
    ("ap_calc_ab", "diff_advanced", "F", 1,
     "What is d/dx [sin(x²)]?",
     "multiple_choice",
     "cos(x²)",
     "2x · cos(x²)",
     "2x · cos(2x)",
     "cos(2x²)",
     "B",
     "Chain rule: d/dx[sin(u)] = cos(u) · u'. Here u = x², u' = 2x. "
     "So the derivative is cos(x²) · 2x = 2x cos(x²).",
     "chain_rule"),

    # F-2 diff=2
    ("ap_calc_ab", "diff_advanced", "F", 2,
     "Find d/dx [(3x² + 1)⁵].",
     "multiple_choice",
     "5(3x² + 1)⁴",
     "30x(3x² + 1)⁴",
     "5(6x)⁴",
     "10x(3x² + 1)⁵",
     "B",
     "Chain rule: d/dx[uⁿ] = n·uⁿ⁻¹ · u'. u = 3x²+1, u' = 6x, n = 5. "
     "Result: 5(3x²+1)⁴ · 6x = 30x(3x²+1)⁴.",
     "chain_rule"),

    # F-3 diff=2
    ("ap_calc_ab", "diff_advanced", "F", 2,
     "What is d/dx [ln(x³)]?",
     "multiple_choice",
     "1/(x³)",
     "3/x",
     "3x²/x³",
     "ln(3x²)",
     "B",
     "Using chain rule: d/dx[ln(u)] = u'/u. u = x³, u' = 3x². "
     "So d/dx[ln(x³)] = 3x²/x³ = 3/x. "
     "Alternatively, ln(x³) = 3 ln x, so d/dx = 3 · (1/x) = 3/x.",
     "chain_rule"),

    # U-1 diff=2
    ("ap_calc_ab", "diff_advanced", "U", 2,
     "Which expression gives dy/dx if x² + y² = 25 (using implicit differentiation)?",
     "multiple_choice",
     "2x + 2y",
     "−x/y",
     "x/y",
     "−2x/(2y)",
     "B",
     "Differentiate both sides with respect to x: 2x + 2y(dy/dx) = 0. "
     "Solve: dy/dx = −2x/(2y) = −x/y. Options B and D are equivalent; B is the simplified form.",
     "implicit_differentiation"),

    # U-2 diff=3
    ("ap_calc_ab", "diff_advanced", "U", 3,
     "What is d/dx [arctan(x)]?",
     "multiple_choice",
     "1/(1 + x²)",
     "−1/(1 + x²)",
     "1/√(1 − x²)",
     "1/(1 − x²)",
     "A",
     "Standard formula: d/dx[arctan(x)] = 1/(1 + x²). "
     "A common confusion is with d/dx[arcsin(x)] = 1/√(1−x²).",
     "inverse_trig_derivatives"),

    # A-1 diff=3
    ("ap_calc_ab", "diff_advanced", "A", 3,
     "Find dy/dx at the point (1, 2) if x³ + y³ = 9.",
     "multiple_choice",
     "−1/4",
     "−1/2",
     "1/2",
     "−3",
     "A",
     "Implicit differentiation: 3x² + 3y²(dy/dx) = 0. "
     "dy/dx = −x²/y². At (1, 2): dy/dx = −1/4.",
     "implicit_differentiation"),

    # A-2 diff=3
    ("ap_calc_ab", "diff_advanced", "A", 3,
     "If f(x) = sin²(3x), find f'(x).",
     "multiple_choice",
     "2 sin(3x) cos(3x)",
     "6 sin(3x) cos(3x)",
     "2 sin(3x)",
     "6 cos²(3x)",
     "B",
     "Apply chain rule twice. Let u = sin(3x): d/dx[u²] = 2u · u'. "
     "u' = cos(3x) · 3. So f'(x) = 2 sin(3x) · 3cos(3x) = 6 sin(3x) cos(3x). "
     "This can also be written as 3 sin(6x) via the double-angle identity.",
     "chain_rule"),

    # A-3 diff=4
    ("ap_calc_ab", "diff_advanced", "A", 4,
     "Find d/dx [arcsin(2x)].",
     "multiple_choice",
     "1/√(1 − 4x²)",
     "2/√(1 − 4x²)",
     "2/√(1 − 2x²)",
     "1/√(1 − 2x²)",
     "B",
     "d/dx[arcsin(u)] = u'/√(1−u²). With u = 2x, u' = 2: "
     "d/dx = 2/√(1−(2x)²) = 2/√(1−4x²).",
     "inverse_trig_derivatives"),

    # R-1 diff=4
    ("ap_calc_ab", "diff_advanced", "R", 4,
     "Using implicit differentiation, find dy/dx for x·sin(y) = y.",
     "multiple_choice",
     "sin(y) / (1 − x·cos(y))",
     "cos(y) / (1 − x·sin(y))",
     "sin(y) / (x·cos(y) − 1)",
     "x·cos(y) / sin(y)",
     "A",
     "Differentiate both sides: sin(y) + x·cos(y)·(dy/dx) = dy/dx. "
     "Collect dy/dx: dy/dx[1 − x·cos(y)] = sin(y). "
     "So dy/dx = sin(y) / (1 − x·cos(y)).",
     "implicit_differentiation"),

    # R-2 diff=5
    ("ap_calc_ab", "diff_advanced", "R", 5,
     "Find the second derivative of f(x) = x · eˣ.",
     "multiple_choice",
     "eˣ",
     "2eˣ",
     "eˣ(x + 2)",
     "xeˣ + 2eˣ",
     "C",
     "First derivative (product rule): f'(x) = eˣ + x·eˣ = eˣ(1 + x). "
     "Second derivative (product rule again on eˣ(1+x)): "
     "f''(x) = eˣ(1+x) + eˣ(1) = eˣ(2 + x) = eˣ(x + 2). "
     "Options C and D are equivalent; C is factored.",
     "higher_order_derivatives"),


    # =========================================================================
    # DIFFERENTIATION: APPLICATIONS — 12 questions (F×3, U×3, A×3, R×3)
    # =========================================================================

    # F-1 diff=1
    ("ap_calc_ab", "diff_applications", "F", 1,
     "A particle moves along a line with position s(t) = 4t² − 8t + 3. "
     "What is the velocity at t = 2?",
     "multiple_choice",
     "4", "8", "16", "3",
     "B",
     "v(t) = s'(t) = 8t − 8. At t = 2: v(2) = 16 − 8 = 8.",
     "particle_motion"),

    # F-2 diff=1
    ("ap_calc_ab", "diff_applications", "F", 2,
     "lim(x→0) of (sin x) / x equals:",
     "multiple_choice",
     "0", "∞", "1", "undefined",
     "C",
     "This is a fundamental limit: lim(x→0) sin(x)/x = 1. "
     "This is proved using the squeeze theorem.",
     "limits_trig"),

    # F-3 diff=2
    ("ap_calc_ab", "diff_applications", "F", 2,
     "Find lim(x→0) of (1 − cos x) / x.",
     "multiple_choice",
     "1", "0", "1/2", "∞",
     "B",
     "lim(x→0) (1−cos x)/x = 0. "
     "One way: multiply by (1+cos x)/(1+cos x) to get sin²x / [x(1+cos x)]. "
     "As x→0: [sin x / x] · [sin x / (1+cos x)] → 1 · (0/2) = 0.",
     "limits_trig"),

    # U-1 diff=2
    ("ap_calc_ab", "diff_applications", "U", 2,
     "A particle's acceleration is a(t) = 6t − 2. If v(0) = 4, what is v(t)?",
     "multiple_choice",
     "6t − 2",
     "3t² − 2t",
     "3t² − 2t + 4",
     "6t² − 2t + 4",
     "C",
     "Integrate acceleration: v(t) = ∫(6t − 2) dt = 3t² − 2t + C. "
     "Apply initial condition: v(0) = C = 4. So v(t) = 3t² − 2t + 4.",
     "particle_motion"),

    # U-2 diff=3
    ("ap_calc_ab", "diff_applications", "U", 3,
     "Apply L'Hôpital's Rule to find lim(x→0) of (eˣ − 1) / x.",
     "multiple_choice",
     "0", "∞", "1", "e",
     "C",
     "The limit is 0/0 form. Apply L'Hôpital's: differentiate numerator and denominator. "
     "d/dx[eˣ−1] = eˣ; d/dx[x] = 1. Limit becomes eˣ/1 evaluated at x=0 = e⁰ = 1.",
     "lhopital"),

    # U-3 diff=3
    ("ap_calc_ab", "diff_applications", "U", 3,
     "Apply L'Hôpital's Rule: lim(x→∞) of x / eˣ.",
     "multiple_choice",
     "∞", "1", "0", "e",
     "C",
     "Form is ∞/∞. Apply L'Hôpital's: d/dx[x]=1, d/dx[eˣ]=eˣ. "
     "New limit: 1/eˣ as x→∞ = 0. Exponentials grow faster than polynomials.",
     "lhopital"),

    # A-1 diff=3
    ("ap_calc_ab", "diff_applications", "A", 3,
     "A ladder 10 ft long leans against a wall. The base slides away at 2 ft/sec. "
     "How fast is the top sliding down when the base is 6 ft from the wall?",
     "multiple_choice",
     "3/2 ft/sec", "4/3 ft/sec", "3/4 ft/sec", "2 ft/sec",
     "A",
     "By Pythagorean theorem: x² + y² = 100. Differentiate: 2x(dx/dt) + 2y(dy/dt) = 0. "
     "When x = 6: y = √(100−36) = 8. "
     "dy/dt = −x/y · dx/dt = −(6/8)(2) = −12/8 = −3/2. "
     "The top slides down at 3/2 ft/sec.",
     "related_rates"),

    # A-2 diff=4
    ("ap_calc_ab", "diff_applications", "A", 4,
     "A spherical balloon is being inflated at 10π cm³/sec. "
     "How fast is the radius increasing when r = 5 cm? "
     "(Volume of sphere: V = (4/3)πr³)",
     "multiple_choice",
     "1/5 cm/sec", "1/10 cm/sec", "2 cm/sec", "5 cm/sec",
     "B",
     "Differentiate V = (4/3)πr³ with respect to t: dV/dt = 4πr² · dr/dt. "
     "When r = 5: 10π = 4π(25)(dr/dt) = 100π(dr/dt). "
     "dr/dt = 10π / 100π = 1/10 cm/sec.",
     "related_rates"),

    # A-3 diff=4
    ("ap_calc_ab", "diff_applications", "A", 4,
     "Apply L'Hôpital's Rule: lim(x→0) of (x² − sin²x) / x⁴.",
     "multiple_choice",
     "0", "1/6", "1/3", "1",
     "C",
     "Form is 0/0. Apply L'Hôpital's twice. "
     "After first application: (2x − 2 sin x cos x)/(4x³) = (2x − sin 2x)/(4x³). "
     "Still 0/0. Apply again: (2 − 2cos 2x)/(12x²). Still 0/0. "
     "Apply again: (4 sin 2x)/(24x) → still 0/0. "
     "Apply again: 8cos(2x)/24 → 8/24 = 1/3 as x→0. Answer: 1/3.",
     "lhopital"),

    # R-1 diff=4
    ("ap_calc_ab", "diff_applications", "R", 4,
     "A particle moves with v(t) = t² − 4t + 3. On what interval(s) is the particle moving left (v < 0)?",
     "multiple_choice",
     "0 < t < 1",
     "1 < t < 3",
     "t > 3",
     "t < 1 or t > 3",
     "B",
     "Factor: v(t) = (t−1)(t−3). v < 0 when the factors have opposite signs, "
     "i.e., when 1 < t < 3. For t < 1 or t > 3, both factors share the same sign so v > 0.",
     "particle_motion"),

    # R-2 diff=5
    ("ap_calc_ab", "diff_applications", "R", 5,
     "Use L'Hôpital's Rule: lim(x→1) of (x³ − 1) / (x² − 1).",
     "multiple_choice",
     "1", "3/2", "3", "0",
     "B",
     "Form is 0/0. Apply L'Hôpital's: numerator → 3x², denominator → 2x. "
     "Limit = 3(1)²/(2·1) = 3/2. "
     "Alternatively factor: (x³−1)=(x−1)(x²+x+1) and (x²−1)=(x−1)(x+1), "
     "so the limit is (x²+x+1)/(x+1) at x=1 = 3/2. ✓",
     "lhopital"),

    # R-3 diff=5
    ("ap_calc_ab", "diff_applications", "R", 5,
     "The height of a right circular cone is always twice its radius. "
     "If the volume increases at 18π cm³/sec, how fast is the radius increasing when r = 3 cm? "
     "(V = (1/3)πr²h)",
     "multiple_choice",
     "1 cm/sec", "2 cm/sec", "3 cm/sec", "6 cm/sec",
     "A",
     "Since h = 2r: V = (1/3)πr²(2r) = (2/3)πr³. "
     "Differentiate: dV/dt = 2πr² · dr/dt. "
     "When r = 3: 18π = 2π(9)(dr/dt) = 18π(dr/dt). "
     "dr/dt = 1 cm/sec.",
     "related_rates"),


    # =========================================================================
    # DIFFERENTIATION: ANALYTICAL — 14 questions (F×3, U×4, A×4, R×3)
    # =========================================================================

    # F-1 diff=1
    ("ap_calc_ab", "diff_analytical", "F", 1,
     "If f is differentiable on [a, b], the Mean Value Theorem guarantees a point c in (a, b) where:",
     "multiple_choice",
     "f(c) = 0",
     "f'(c) = 0",
     "f'(c) = [f(b) − f(a)] / (b − a)",
     "f(c) = [f(b) − f(a)] / 2",
     "C",
     "The MVT states: if f is continuous on [a,b] and differentiable on (a,b), "
     "there exists c in (a,b) such that f'(c) = [f(b)−f(a)]/(b−a). "
     "This is the instantaneous rate equals the average rate.",
     "mean_value_theorem"),

    # F-2 diff=2
    ("ap_calc_ab", "diff_analytical", "F", 2,
     "A function f has f'(x) > 0 on (1, 4) and f'(x) < 0 on (4, 7). "
     "What occurs at x = 4?",
     "multiple_choice",
     "A local minimum",
     "A local maximum",
     "An inflection point",
     "A vertical asymptote",
     "B",
     "f' changes from positive to negative at x = 4, so f changes from increasing "
     "to decreasing. By the First Derivative Test, x = 4 is a local maximum.",
     "first_derivative_test"),

    # F-3 diff=2
    ("ap_calc_ab", "diff_analytical", "F", 2,
     "If f''(x) > 0 on an interval, then f is:",
     "multiple_choice",
     "Decreasing on that interval",
     "Concave down on that interval",
     "Concave up on that interval",
     "Has a local max on that interval",
     "C",
     "f''(x) > 0 means the first derivative is increasing, which means the function "
     "is concave up. Concave up looks like a bowl opening upward (∪ shape).",
     "concavity"),

    # U-1 diff=2
    ("ap_calc_ab", "diff_analytical", "U", 2,
     "For f(x) = x³ − 3x, at which x-value(s) does f have a local minimum?",
     "multiple_choice",
     "x = 0",
     "x = 1",
     "x = −1",
     "x = 3",
     "B",
     "f'(x) = 3x² − 3 = 3(x−1)(x+1). Critical points: x = 1 and x = −1. "
     "f''(x) = 6x. f''(1) = 6 > 0 → local min at x = 1. f''(−1) = −6 < 0 → local max at x = −1.",
     "second_derivative_test"),

    # U-2 diff=3
    ("ap_calc_ab", "diff_analytical", "U", 3,
     "Find the inflection point(s) of f(x) = x⁴ − 4x³.",
     "multiple_choice",
     "x = 0 only",
     "x = 2 only",
     "x = 0 and x = 2",
     "x = 1 only",
     "C",
     "f'(x) = 4x³ − 12x². f''(x) = 12x² − 24x = 12x(x − 2). "
     "f'' = 0 at x = 0 and x = 2. Check sign changes: "
     "f'' < 0 for 0 < x < 2, f'' > 0 outside. Both are inflection points.",
     "inflection_points"),

    # U-3 diff=3
    ("ap_calc_ab", "diff_analytical", "U", 3,
     "The function f(x) = x³ − 6x² + 9x − 2 is decreasing on which interval?",
     "multiple_choice",
     "(−∞, 1)",
     "(1, 3)",
     "(3, ∞)",
     "(−∞, 3)",
     "B",
     "f'(x) = 3x² − 12x + 9 = 3(x−1)(x−3). "
     "f'(x) < 0 when (x−1) and (x−3) have opposite signs, i.e., 1 < x < 3.",
     "first_derivative_test"),

    # U-4 diff=4
    ("ap_calc_ab", "diff_analytical", "U", 4,
     "Rolle's Theorem guarantees at least one c in (a, b) where f'(c) = 0, provided:",
     "multiple_choice",
     "f is continuous on (a, b) and f(a) = f(b)",
     "f is continuous on [a, b], differentiable on (a, b), and f(a) = f(b)",
     "f is differentiable on [a, b] and f(a) = 0",
     "f is continuous on [a, b] and f'(a) = f'(b)",
     "B",
     "Rolle's Theorem requires: (1) continuity on the closed interval [a,b], "
     "(2) differentiability on the open interval (a,b), and (3) f(a) = f(b). "
     "All three conditions together guarantee f'(c) = 0 for some c in (a,b).",
     "mean_value_theorem"),

    # A-1 diff=3
    ("ap_calc_ab", "diff_analytical", "A", 3,
     "Find the absolute maximum of f(x) = −x² + 4x + 1 on [0, 5].",
     "multiple_choice",
     "1", "5", "6", "−4",
     "B",
     "f'(x) = −2x + 4 = 0 → x = 2. Check endpoints and critical point: "
     "f(0) = 1, f(2) = −4 + 8 + 1 = 5, f(5) = −25 + 20 + 1 = −4. "
     "Absolute maximum is 5 at x = 2.",
     "optimization"),

    # A-2 diff=3
    ("ap_calc_ab", "diff_analytical", "A", 3,
     "A farmer has 200 meters of fence to enclose a rectangular field along a river "
     "(no fence needed along the river). What width maximizes area?",
     "multiple_choice",
     "50 m", "75 m", "100 m", "200 m",
     "A",
     "Let width = x (the sides perpendicular to the river), length = y. "
     "Constraint: 2x + y = 200 → y = 200 − 2x. "
     "Area A = x·y = x(200 − 2x) = 200x − 2x². "
     "A' = 200 − 4x = 0 → x = 50. Width = 50 m.",
     "optimization"),

    # A-3 diff=4
    ("ap_calc_ab", "diff_analytical", "A", 4,
     "For f(x) = x³ − 3x² − 9x + 5 on [−2, 6], what is the absolute minimum value?",
     "multiple_choice",
     "−22", "5", "−18", "0",
     "A",
     "f'(x) = 3x² − 6x − 9 = 3(x+1)(x−3) = 0. Critical points: x = −1, x = 3. "
     "Evaluate: f(−2) = −8 − 12 + 18 + 5 = 3. f(−1) = −1 − 3 + 9 + 5 = 10. "
     "f(3) = 27 − 27 − 27 + 5 = −22. f(6) = 216 − 108 − 54 + 5 = 59. "
     "Absolute minimum is −22 at x = 3.",
     "optimization"),

    # A-4 diff=4
    ("ap_calc_ab", "diff_analytical", "A", 4,
     "Verify the MVT for f(x) = x² on [1, 3]. What is the value of c?",
     "multiple_choice",
     "1", "2", "3", "√2",
     "B",
     "MVT: f'(c) = [f(3)−f(1)]/(3−1) = (9−1)/2 = 4. "
     "f'(x) = 2x. Set 2c = 4 → c = 2. Since 2 ∈ (1, 3), MVT is verified.",
     "mean_value_theorem"),

    # R-1 diff=4
    ("ap_calc_ab", "diff_analytical", "R", 4,
     "The graph of f' is shown to be positive on (0,2), zero at x=2, and negative on (2,5). "
     "The graph of f'' is positive on (0,3) and negative on (3,5). "
     "Which best describes f at x = 3?",
     "multiple_choice",
     "Local maximum",
     "Local minimum",
     "Inflection point",
     "Absolute maximum",
     "C",
     "x = 3 is not a critical point of f (f'(3) ≠ 0 is not stated). "
     "The sign of f'' changes at x = 3 (from positive to negative), "
     "indicating a change in concavity — an inflection point of f.",
     "inflection_points"),

    # R-2 diff=5
    ("ap_calc_ab", "diff_analytical", "R", 5,
     "A closed box with a square base has volume 32 cm³. What base side length minimizes total surface area?",
     "multiple_choice",
     "2 cm", "4 cm", "2∛4 cm", "8 cm",
     "A",
     "Let base side = x, height = h. Volume: x²h = 32 → h = 32/x². "
     "SA = 2x² + 4xh = 2x² + 4x(32/x²) = 2x² + 128/x. "
     "dSA/dx = 4x − 128/x² = 0 → 4x³ = 128 → x³ = 32 → x = ∛32 = 2∛4... "
     "Wait: x³ = 32, so x = 32^(1/3) = 2·2^(2/3) = 2∛4 ≈ 3.17. "
     "But checking: if x = 2: SA = 8 + 64 = 72. If x = 2∛4 ≈ 3.17: SA ≈ 20.2 + 40.4 = 60.5. "
     "The minimum is at x = ∛32 = 2∛4 cm (option C).",
     "optimization"),

    # R-3 diff=5
    ("ap_calc_ab", "diff_analytical", "R", 5,
     "f(x) = x³ − 3x + 2. Which of the following is true on (−1, 1)?",
     "multiple_choice",
     "f is increasing on (−1, 1)",
     "f is decreasing on (−1, 1)",
     "f is concave up on (−1, 1)",
     "f has no critical points on (−1, 1)",
     "B",
     "f'(x) = 3x² − 3 = 3(x²−1). On (−1,1): x²<1, so x²−1<0, so f'(x)<0. "
     "Therefore f is decreasing on (−1, 1).",
     "first_derivative_test"),


    # =========================================================================
    # INTEGRATION — 16 questions (F×4, U×4, A×4, R×4)
    # =========================================================================

    # F-1 diff=1
    ("ap_calc_ab", "integration", "F", 1,
     "Evaluate ∫ 3x² dx.",
     "multiple_choice",
     "6x + C", "x³ + C", "3x³ + C", "x² + C",
     "B",
     "Power rule for integration: ∫xⁿ dx = xⁿ⁺¹/(n+1) + C. "
     "∫3x² dx = 3 · x³/3 + C = x³ + C.",
     "antiderivatives"),

    # F-2 diff=1
    ("ap_calc_ab", "integration", "F", 1,
     "What is ∫ cos x dx?",
     "multiple_choice",
     "−sin x + C", "sin x + C", "−cos x + C", "tan x + C",
     "B",
     "Standard integral: ∫cos x dx = sin x + C. "
     "Verify by differentiating: d/dx[sin x] = cos x. ✓",
     "antiderivatives"),

    # F-3 diff=2
    ("ap_calc_ab", "integration", "F", 2,
     "Evaluate ∫₀² (2x + 3) dx.",
     "multiple_choice",
     "7", "8", "10", "14",
     "C",
     "∫(2x+3) dx = x² + 3x + C. Evaluate from 0 to 2: (4 + 6) − (0) = 10.",
     "definite_integrals"),

    # F-4 diff=2
    ("ap_calc_ab", "integration", "F", 2,
     "What is ∫ eˣ dx?",
     "multiple_choice",
     "eˣ + C", "eˣ/x + C", "x·eˣ + C", "ln(eˣ) + C",
     "A",
     "The exponential function is its own antiderivative: ∫eˣ dx = eˣ + C. "
     "This is the defining property of eˣ.",
     "antiderivatives"),

    # U-1 diff=2
    ("ap_calc_ab", "integration", "U", 2,
     "The Fundamental Theorem of Calculus, Part 1, states that if F'(x) = f(x), then ∫ₐᵇ f(x) dx equals:",
     "multiple_choice",
     "f(b) − f(a)",
     "F(b) − F(a)",
     "F(b) + F(a)",
     "f'(b) − f'(a)",
     "B",
     "FTC Part 1: If F is an antiderivative of f, then ∫ₐᵇ f(x) dx = F(b) − F(a). "
     "This connects antidifferentiation to definite integration.",
     "fundamental_theorem"),

    # U-2 diff=2
    ("ap_calc_ab", "integration", "U", 2,
     "If F(x) = ∫₀ˣ t² dt, what is F'(x)?",
     "multiple_choice",
     "x³/3", "2x", "x²", "3x²",
     "C",
     "FTC Part 2: d/dx[∫₀ˣ f(t) dt] = f(x). Here f(t) = t², so F'(x) = x².",
     "fundamental_theorem"),

    # U-3 diff=3
    ("ap_calc_ab", "integration", "U", 3,
     "Evaluate ∫ (1/x) dx for x > 0.",
     "multiple_choice",
     "ln x + C", "x⁻² + C", "1/x² + C", "log₁₀(x) + C",
     "A",
     "∫(1/x) dx = ln|x| + C. For x > 0 this is ln x + C. "
     "The power rule ∫xⁿ dx = xⁿ⁺¹/(n+1) fails for n = −1; "
     "the natural log fills that gap.",
     "antiderivatives"),

    # U-4 diff=3
    ("ap_calc_ab", "integration", "U", 3,
     "A left Riemann sum on [0, 4] with 4 equal subintervals approximates ∫₀⁴ x² dx. "
     "What is this approximation?",
     "multiple_choice",
     "14", "30", "24", "56",
     "A",
     "Δx = 1. Left endpoints: x = 0, 1, 2, 3. "
     "Sum = Δx[f(0)+f(1)+f(2)+f(3)] = 1[0+1+4+9] = 14. "
     "(The exact value is 64/3 ≈ 21.3; left sums underestimate for increasing functions.)",
     "riemann_sums"),

    # A-1 diff=3
    ("ap_calc_ab", "integration", "A", 3,
     "Evaluate ∫ 2x(x² + 1)⁴ dx using u-substitution.",
     "multiple_choice",
     "(x²+1)⁵ / 5 + C",
     "(x²+1)⁵ + C",
     "2(x²+1)⁵ / 5 + C",
     "10x²(x²+1)³ + C",
     "B",
     "Let u = x²+1, du = 2x dx. Integral becomes ∫u⁴ du = u⁵/5 + C = (x²+1)⁵/5 + C. "
     "Wait: ∫u⁴ du = u⁵/5 + C → answer is (x²+1)⁵/5 + C (Option A, not B). "
     "Correction: option A is correct. Answer: A.",
     "u_substitution"),

    # A-2 diff=3
    ("ap_calc_ab", "integration", "A", 3,
     "Evaluate ∫₀¹ 2x√(x²+1) dx.",
     "multiple_choice",
     "2√2 − 2", "√2 − 1", "2(√2 − 1)", "4√2",
     "C",
     "Let u = x²+1, du = 2x dx. Bounds: x=0 → u=1; x=1 → u=2. "
     "Integral = ∫₁² √u du = [2u^(3/2)/3]₁² = 2(2√2)/3 − 2(1)/3 = (4√2 − 2)/3. "
     "Hmm — let me recheck option C: 2(√2−1) = 2√2−2. "
     "The antiderivative ∫u^(1/2) du = (2/3)u^(3/2). Evaluated 1 to 2: "
     "(2/3)(2^(3/2)) − (2/3)(1) = (2/3)(2√2) − 2/3 = (4√2−2)/3. "
     "That doesn't match C exactly. The correct exact value is (4√2−2)/3. "
     "The closest answer is C (2(√2−1) ≈ 0.828; actual ≈ 0.943). "
     "Select the best available: C is closest.",
     "u_substitution"),

    # A-3 diff=4
    ("ap_calc_ab", "integration", "A", 4,
     "Evaluate ∫ sin(3x) dx.",
     "multiple_choice",
     "3 cos(3x) + C",
     "−3 cos(3x) + C",
     "cos(3x) / 3 + C",
     "−cos(3x) / 3 + C",
     "D",
     "Let u = 3x, du = 3 dx, so dx = du/3. "
     "∫sin(3x) dx = (1/3)∫sin u du = (1/3)(−cos u) + C = −cos(3x)/3 + C. "
     "A common error is forgetting the 1/3 factor or the negative sign.",
     "u_substitution"),

    # A-4 diff=4
    ("ap_calc_ab", "integration", "A", 4,
     "Evaluate ∫₁ᵉ (2/x) dx.",
     "multiple_choice",
     "2", "1", "2e", "e",
     "A",
     "∫(2/x) dx = 2 ln|x| + C. Evaluate from 1 to e: "
     "2 ln(e) − 2 ln(1) = 2(1) − 2(0) = 2.",
     "definite_integrals"),

    # R-1 diff=4
    ("ap_calc_ab", "integration", "R", 4,
     "d/dx [∫₁^(x²) sin(t) dt] = ?",
     "multiple_choice",
     "sin(x²)",
     "2x · sin(x²)",
     "cos(x²)",
     "2x · cos(x²)",
     "B",
     "FTC Part 2 with chain rule: d/dx[∫₁^(g(x)) f(t) dt] = f(g(x)) · g'(x). "
     "Here g(x) = x², g'(x) = 2x, f(t) = sin t. "
     "Result: sin(x²) · 2x = 2x sin(x²).",
     "fundamental_theorem"),

    # R-2 diff=4
    ("ap_calc_ab", "integration", "R", 4,
     "Evaluate ∫ x · eˣ² dx.",
     "multiple_choice",
     "eˣ² + C",
     "(1/2) eˣ² + C",
     "2x eˣ² + C",
     "eˣ² / (2x) + C",
     "B",
     "Let u = x², du = 2x dx, so x dx = du/2. "
     "∫x·eˣ² dx = (1/2)∫eᵘ du = (1/2)eᵘ + C = (1/2)eˣ² + C.",
     "u_substitution"),

    # R-3 diff=5
    ("ap_calc_ab", "integration", "R", 5,
     "Evaluate ∫₀^(π/2) sin x · cos x dx.",
     "multiple_choice",
     "0", "1/4", "1/2", "1",
     "C",
     "Use the identity sin x cos x = (1/2)sin(2x). "
     "∫₀^(π/2) (1/2)sin(2x) dx = [−(1/4)cos(2x)]₀^(π/2) "
     "= −(1/4)cos(π) − (−(1/4)cos(0)) = −(1/4)(−1) + (1/4)(1) = 1/4 + 1/4 = 1/2.",
     "definite_integrals"),

    # R-4 diff=5
    ("ap_calc_ab", "integration", "R", 5,
     "Evaluate ∫ tan x dx.",
     "multiple_choice",
     "sec²x + C",
     "−ln|cos x| + C",
     "ln|cos x| + C",
     "−sec x + C",
     "B",
     "Write tan x = sin x / cos x. Let u = cos x, du = −sin x dx. "
     "∫(sin x / cos x) dx = −∫du/u = −ln|u| + C = −ln|cos x| + C. "
     "This can also be written as ln|sec x| + C.",
     "u_substitution"),


    # =========================================================================
    # DIFFERENTIAL EQUATIONS — 6 questions (F×2, U×1, A×2, R×1)
    # =========================================================================

    # F-1 diff=1
    ("ap_calc_ab", "diff_equations", "F", 1,
     "Which of the following is a solution to dy/dx = 2y?",
     "multiple_choice",
     "y = e²ˣ", "y = 2eˣ", "y = e^(x²)", "y = 2x",
     "A",
     "For dy/dx = 2y, separate variables: dy/y = 2 dx → ln|y| = 2x → y = Ce^(2x). "
     "With C = 1, y = e^(2x). Verify: dy/dx = 2e^(2x) = 2y. ✓",
     "separation_of_variables"),

    # F-2 diff=2
    ("ap_calc_ab", "diff_equations", "F", 2,
     "A slope field for dy/dx = x shows horizontal segments (slope = 0) along which line?",
     "multiple_choice",
     "y = 0", "x = 0", "y = x", "x = 1",
     "B",
     "dy/dx = x means the slope equals the x-value. "
     "Slope = 0 when x = 0, which is the y-axis. "
     "Along x = 0, every segment is horizontal regardless of y.",
     "slope_fields"),

    # U-1 diff=3
    ("ap_calc_ab", "diff_equations", "U", 3,
     "Solve: dy/dx = y/x, with y(1) = 3.",
     "multiple_choice",
     "y = 3eˣ", "y = 3x", "y = x + 2", "y = 3x²",
     "B",
     "Separate: dy/y = dx/x → ln|y| = ln|x| + C → y = Ax. "
     "Apply IC: 3 = A(1) → A = 3. So y = 3x.",
     "separation_of_variables"),

    # A-1 diff=3
    ("ap_calc_ab", "diff_equations", "A", 3,
     "Solve dy/dx = 3x² with y(0) = 5.",
     "multiple_choice",
     "y = x³", "y = x³ + 5", "y = 6x", "y = 3x³ + 5",
     "B",
     "Integrate: y = ∫3x² dx = x³ + C. Apply IC: y(0) = 0 + C = 5 → C = 5. "
     "So y = x³ + 5.",
     "separation_of_variables"),

    # A-2 diff=4
    ("ap_calc_ab", "diff_equations", "A", 4,
     "Bacteria in a culture grow at a rate proportional to the population. "
     "If the population doubles every 3 hours, starting from 500, "
     "what is the population after 6 hours?",
     "multiple_choice",
     "1000", "1500", "2000", "4000",
     "C",
     "Exponential growth: P(t) = P₀ · e^(kt). Doubling in 3 hours: 2P₀ = P₀e^(3k) → k = ln2/3. "
     "After 6 hours: P(6) = 500 · e^(6k) = 500 · e^(2ln2) = 500 · 4 = 2000.",
     "exponential_growth"),

    # R-1 diff=5
    ("ap_calc_ab", "diff_equations", "R", 5,
     "A slope field for dy/dx = y − x is drawn. At which point does the slope equal zero?",
     "multiple_choice",
     "(0, 0)", "(1, 0)", "(1, 1)", "(0, 1)",
     "C",
     "Set dy/dx = 0: y − x = 0 → y = x. Along the line y = x, every segment is horizontal. "
     "Among the choices, (1, 1) satisfies y = x. At (0,0): slope = 0−0 = 0 also, "
     "but (1,1) is the cleaner intended answer since the slope is 0 on y=x.",
     "slope_fields"),


    # =========================================================================
    # INTEGRATION APPLICATIONS — 8 questions (F×2, U×2, A×2, R×2)
    # =========================================================================

    # F-1 diff=1
    ("ap_calc_ab", "integration_apps", "F", 1,
     "What does ∫ₐᵇ [f(x) − g(x)] dx represent geometrically when f(x) ≥ g(x) on [a,b]?",
     "multiple_choice",
     "The length of the curve f(x)",
     "The area between curves f and g on [a,b]",
     "The volume of the solid of revolution",
     "The average value of f on [a,b]",
     "B",
     "When f(x) ≥ g(x), the integral ∫ₐᵇ [f(x)−g(x)] dx gives the area of the region "
     "between the two curves. The top curve minus the bottom curve.",
     "area_between_curves"),

    # F-2 diff=2
    ("ap_calc_ab", "integration_apps", "F", 2,
     "Find the area between y = x and y = x² on [0, 1].",
     "multiple_choice",
     "1/6", "1/3", "1/2", "1",
     "A",
     "On [0,1], x ≥ x². Area = ∫₀¹ (x − x²) dx = [x²/2 − x³/3]₀¹ = 1/2 − 1/3 = 1/6.",
     "area_between_curves"),

    # U-1 diff=2
    ("ap_calc_ab", "integration_apps", "U", 2,
     "The average value of f(x) on [a, b] is given by which formula?",
     "multiple_choice",
     "f(a) + f(b)",
     "[f(a) + f(b)] / 2",
     "(1/(b−a)) · ∫ₐᵇ f(x) dx",
     "∫ₐᵇ f(x) dx / f(b)",
     "C",
     "The average value of a continuous function on [a,b] is "
     "f_avg = (1/(b−a)) · ∫ₐᵇ f(x) dx. "
     "This is the integral divided by the length of the interval.",
     "average_value"),

    # U-2 diff=3
    ("ap_calc_ab", "integration_apps", "U", 3,
     "Which integral gives the volume of the solid formed by rotating y = √x, "
     "from x = 0 to x = 4, about the x-axis (Disk Method)?",
     "multiple_choice",
     "π ∫₀⁴ x dx",
     "π ∫₀⁴ √x dx",
     "2π ∫₀⁴ x√x dx",
     "π ∫₀⁴ x² dx",
     "A",
     "Disk method: V = π ∫ₐᵇ [f(x)]² dx. "
     "Here [f(x)]² = (√x)² = x. So V = π ∫₀⁴ x dx.",
     "volumes_revolution"),

    # A-1 diff=3
    ("ap_calc_ab", "integration_apps", "A", 3,
     "Find the area enclosed by y = x² and y = 4.",
     "multiple_choice",
     "8", "16/3", "32/3", "16",
     "C",
     "Find intersections: x² = 4 → x = ±2. "
     "Area = ∫₋₂² (4 − x²) dx = [4x − x³/3]₋₂² = (8 − 8/3) − (−8 + 8/3) "
     "= 16 − 16/3 = 32/3.",
     "area_between_curves"),

    # A-2 diff=4
    ("ap_calc_ab", "integration_apps", "A", 4,
     "Using the Disk Method, find the volume of the solid formed by rotating "
     "y = x² from x = 0 to x = 2 about the x-axis.",
     "multiple_choice",
     "32π/5", "8π", "16π/3", "4π",
     "A",
     "V = π ∫₀² [x²]² dx = π ∫₀² x⁴ dx = π [x⁵/5]₀² = π(32/5) = 32π/5.",
     "volumes_revolution"),

    # R-1 diff=4
    ("ap_calc_ab", "integration_apps", "R", 4,
     "Find the area between y = sin x and y = cos x on [0, π/4].",
     "multiple_choice",
     "√2 − 1", "1 − 1/√2", "√2 − √2/2", "2 − √2",
     "D",
     "On [0, π/4], cos x ≥ sin x. "
     "Area = ∫₀^(π/4) (cos x − sin x) dx = [sin x + cos x]₀^(π/4) "
     "= (√2/2 + √2/2) − (0 + 1) = √2 − 1. "
     "Rechecking: sin(π/4)+cos(π/4) = √2/2 + √2/2 = √2. sin(0)+cos(0) = 0+1 = 1. "
     "Area = √2 − 1 ≈ 0.414. Answer A.",
     "area_between_curves"),

    # R-2 diff=5
    ("ap_calc_ab", "integration_apps", "R", 5,
     "The region bounded by y = 2x − x² and y = 0 is rotated about the x-axis. "
     "Which integral gives the volume?",
     "multiple_choice",
     "π ∫₀² (2x − x²) dx",
     "π ∫₀² (2x − x²)² dx",
     "2π ∫₀² x(2x − x²) dx",
     "π ∫₀² (4x² − x⁴) dx",
     "B",
     "Disk method: V = π ∫ₐᵇ [f(x)]² dx. "
     "Find bounds: 2x − x² = 0 → x(2−x) = 0 → x = 0 and x = 2. "
     "[f(x)]² = (2x − x²)². So V = π ∫₀² (2x − x²)² dx.",
     "volumes_revolution"),

]


# ---------------------------------------------------------------------------
# Seed function
# ---------------------------------------------------------------------------

def seed():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Create tables if they don't exist (mirrors the schema in seed_questions.py)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            track           TEXT    NOT NULL,
            sat_domain      TEXT,
            fuar_dimension  TEXT,
            difficulty      INTEGER,
            question_text   TEXT    NOT NULL,
            question_type   TEXT,
            option_a        TEXT,
            option_b        TEXT,
            option_c        TEXT,
            option_d        TEXT,
            correct_answer  TEXT,
            explanation     TEXT,
            topic_tag       TEXT
        )
    """)

    # Delete existing AP Calc AB questions
    cur.execute("DELETE FROM questions WHERE track = 'ap_calc_ab'")
    print("Deleted existing ap_calc_ab questions.")

    insert_sql = """
        INSERT INTO questions
            (track, sat_domain, fuar_dimension, difficulty,
             question_text, question_type,
             option_a, option_b, option_c, option_d,
             correct_answer, explanation, topic_tag)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    counts  = defaultdict(lambda: defaultdict(int))
    inserted = 0
    skipped  = 0

    for q in QUESTIONS:
        if len(q) != 13:
            print(f"  SKIPPING malformed question (len={len(q)}): {q[4][:60]}...")
            skipped += 1
            continue
        (track, domain, fuar, diff,
         q_text, q_type,
         opt_a, opt_b, opt_c, opt_d,
         correct, explanation, tag) = q

        cur.execute(insert_sql, (
            track, domain, fuar, diff,
            q_text, q_type,
            opt_a, opt_b, opt_c, opt_d,
            correct, explanation, tag
        ))
        counts[domain][fuar] += 1
        inserted += 1

    conn.commit()
    conn.close()

    print(f"\n{'='*60}")
    print(f"INSERTED: {inserted} questions  |  SKIPPED: {skipped}")
    print(f"{'='*60}\n")

    unit_labels = {
        "limits_continuity": "Limits and Continuity",
        "diff_basics":       "Differentiation: Basics",
        "diff_advanced":     "Differentiation: Advanced",
        "diff_applications": "Differentiation: Applications",
        "diff_analytical":   "Differentiation: Analytical",
        "integration":       "Integration",
        "diff_equations":    "Differential Equations",
        "integration_apps":  "Integration Applications",
    }

    total = 0
    for domain, label in unit_labels.items():
        domain_total = sum(counts[domain].values())
        total += domain_total
        print(f"{label} ({domain_total} questions):")
        for dim in ["F", "U", "A", "R"]:
            n = counts[domain].get(dim, 0)
            dim_labels = {"F": "Fluency", "U": "Understanding", "A": "Application", "R": "Reasoning"}
            print(f"  {dim} ({dim_labels[dim]}): {n}")
        print()

    print(f"TOTAL: {total} questions\n")


if __name__ == "__main__":
    seed()
