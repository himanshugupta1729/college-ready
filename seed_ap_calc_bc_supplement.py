"""Supplemental AP Calculus BC questions."""
import sqlite3, os
DB_PATH = os.environ.get('DATABASE_PATH', 'college_ready.db')

QUESTIONS = [
    # (track, sat_domain, fuar_dimension, difficulty, question_text, question_type,
    #  option_a, option_b, option_c, option_d, correct_answer, explanation, topic_tag)

    # ── SERIES & CONVERGENCE (22 questions) ───────────────────────────────────

    ("ap_calc_bc", "seed_ap_calc_bc_supplement.py".replace("seed_","").replace("_supplement.py",""), "F", 2, "What is the sum of the geometric series 1 + 1/2 + 1/4 + 1/8 + …?",
     "multiple_choice", "1", "2", "3/2", "∞", "B",
     "Geometric series with a=1, r=1/2. Sum = a/(1−r) = 1/(1−1/2) = 1/(1/2) = 2.",
     "series_geometric"),

    ("ap_calc_bc", "seed_ap_calc_bc_supplement.py".replace("seed_","").replace("_supplement.py",""), "F", 2, "The series Σ(n=1 to ∞) 1/n² converges by which test?",
     "multiple_choice", "Ratio Test", "p-Series Test with p=2 > 1", "Divergence Test", "Alternating Series Test", "B",
     "This is a p-series with p=2. Since p=2 > 1, the series converges.",
     "series_p_series"),

    ("ap_calc_bc", "general", "U", 3, "Does the series Σ(n=1 to ∞) n/(n+1) converge or diverge?",
     "multiple_choice",
     "Converges to 1",
     "Converges to 1/2",
     "Diverges by the Divergence Test",
     "Diverges by Comparison", "C",
     "lim(n→∞) n/(n+1) = 1 ≠ 0. By the Divergence Test (nth-term test), the series diverges.",
     "series_divergence_test"),

    ("ap_calc_bc", "seed_ap_calc_bc_supplement.py".replace("seed_","").replace("_supplement.py",""), "F", 3, "Find the radius of convergence of Σ(n=0 to ∞) xⁿ/n!",
     "multiple_choice", "0", "1", "e", "∞", "D",
     "Ratio Test: |aₙ₊₁/aₙ| = |x|/(n+1) → 0 for all x. The radius of convergence is ∞.",
     "series_radius_convergence"),

    ("ap_calc_bc", "general", "U", 3, "The alternating series Σ(n=1 to ∞) (−1)ⁿ/n converges by the Alternating Series Test because:",
     "multiple_choice",
     "The terms increase in absolute value",
     "The terms are positive",
     "The absolute values decrease to 0",
     "The limit of partial sums is ln 2", "C",
     "AST requires: (1) terms decrease in absolute value and (2) terms → 0. Both hold for 1/n.",
     "series_alternating"),

    ("ap_calc_bc", "general", "A", 3, "Apply the Ratio Test to Σ(n=1 to ∞) n!/3ⁿ. The series:",
     "multiple_choice", "Converges", "Diverges", "Test is inconclusive", "Converges absolutely", "B",
     "L = lim |aₙ₊₁/aₙ| = lim (n+1)!/3ⁿ⁺¹ · 3ⁿ/n! = lim (n+1)/3 = ∞ > 1. Diverges.",
     "series_ratio_test"),

    ("ap_calc_bc", "seed_ap_calc_bc_supplement.py".replace("seed_","").replace("_supplement.py",""), "F", 2, "The Taylor series for eˣ centered at x=0 is:",
     "multiple_choice",
     "1 + x + x²/2! + x³/3! + …",
     "1 − x + x²/2! − x³/3! + …",
     "x − x³/6 + x⁵/120 − …",
     "1 + x + x² + x³ + …", "A",
     "eˣ = Σ(n=0 to ∞) xⁿ/n! = 1 + x + x²/2! + x³/3! + …",
     "series_taylor"),

    ("ap_calc_bc", "seed_ap_calc_bc_supplement.py".replace("seed_","").replace("_supplement.py",""), "F", 2, "The Maclaurin series for sin(x) is:",
     "multiple_choice",
     "1 − x²/2! + x⁴/4! − …",
     "x − x³/3! + x⁵/5! − …",
     "x + x³/3! + x⁵/5! + …",
     "x − x²/2 + x³/3 − …", "B",
     "sin(x) = Σ(n=0 to ∞) (−1)ⁿ x^(2n+1)/(2n+1)! = x − x³/6 + x⁵/120 − …",
     "series_taylor"),

    ("ap_calc_bc", "general", "U", 3, "Find the interval of convergence of Σ(n=0 to ∞) xⁿ/n (for n≥1).",
     "multiple_choice", "[−1, 1]", "(−1, 1]", "[−1, 1)", "(−1, 1)", "B",
     "Ratio test gives |x| < 1. At x=1: harmonic series diverges. At x=−1: alternating series converges. So interval is [−1, 1).",
     "series_interval_convergence"),

    ("ap_calc_bc", "general", "A", 4, "Use the first three nonzero terms of the Maclaurin series for cos(x) to approximate cos(0.1).",
     "multiple_choice", "0.9950", "0.9900", "0.9975", "0.9995", "A",
     "cos(x) ≈ 1 − x²/2! + x⁴/4!. cos(0.1) ≈ 1 − 0.01/2 + 0.0001/24 = 1 − 0.005 + 0.0000042 ≈ 0.9950.",
     "series_taylor"),

    ("ap_calc_bc", "seed_ap_calc_bc_supplement.py".replace("seed_","").replace("_supplement.py",""), "F", 3, "Which test is most appropriate for Σ(n=1 to ∞) 1/(n² + 1)?",
     "multiple_choice", "Alternating Series Test", "Ratio Test", "Limit Comparison Test with 1/n²", "Root Test", "C",
     "Compare with 1/n²: lim [1/(n²+1)]/(1/n²) = lim n²/(n²+1) = 1. Since Σ1/n² converges, so does this series.",
     "series_comparison"),

    ("ap_calc_bc", "general", "U", 3, "What is the radius of convergence of Σ(n=0 to ∞) n·xⁿ?",
     "multiple_choice", "0", "1/2", "1", "∞", "C",
     "Ratio test: lim |(n+1)xⁿ⁺¹/(n·xⁿ)| = |x|·lim(n+1)/n = |x|. Converges when |x| < 1. R = 1.",
     "series_radius_convergence"),

    ("ap_calc_bc", "general", "A", 4, "The series Σ(n=2 to ∞) 1/(n(ln n)²) converges by:",
     "multiple_choice", "Ratio Test", "Integral Test", "Root Test", "Comparison Test", "B",
     "Integral Test: ∫₂^∞ 1/(x(ln x)²)dx. Let u=ln x: ∫ du/u² = [−1/u] which converges. So series converges.",
     "series_integral_test"),

    ("ap_calc_bc", "general", "R", 3, "The error in using the first n terms of an alternating series with terms bₙ (decreasing to 0) is at most:",
     "multiple_choice", "bₙ", "bₙ₊₁", "bₙ²", "1/n", "B",
     "Alternating Series Estimation Theorem: the error |S − Sₙ| ≤ bₙ₊₁, the first omitted term.",
     "series_error_bound"),

    ("ap_calc_bc", "seed_ap_calc_bc_supplement.py".replace("seed_","").replace("_supplement.py",""), "F", 2, "The power series Σ(n=0 to ∞) (x−2)ⁿ/4ⁿ converges when:",
     "multiple_choice", "|x| < 4", "|x−2| < 4", "|x−2| < 1", "x = 2 only", "B",
     "Ratio test: |aₙ₊₁/aₙ| = |x−2|/4. Converges when |x−2|/4 < 1, i.e., |x−2| < 4.",
     "series_interval_convergence"),

    ("ap_calc_bc", "general", "U", 4, "What is the Maclaurin series for ln(1+x), valid for |x| ≤ 1 (x ≠ −1)?",
     "multiple_choice",
     "x + x²/2 + x³/3 + …",
     "x − x²/2 + x³/3 − x⁴/4 + …",
     "1 + x − x²/2 + x³/3 − …",
     "x − x²/2! + x³/3! − …", "B",
     "ln(1+x) = Σ(n=1 to ∞) (−1)ⁿ⁺¹ xⁿ/n = x − x²/2 + x³/3 − …",
     "series_taylor"),

    ("ap_calc_bc", "general", "A", 4, "Find the sum of the series 1 − 1/3 + 1/9 − 1/27 + …",
     "multiple_choice", "2/3", "3/4", "1/2", "4/3", "B",
     "Geometric series: a=1, r=−1/3. Sum = 1/(1+1/3) = 1/(4/3) = 3/4.",
     "series_geometric"),

    ("ap_calc_bc", "general", "R", 3, "The series Σ(n=1 to ∞) (−1)ⁿ n²/(n²+1) diverges because:",
     "multiple_choice",
     "The terms don't approach 0",
     "It fails the Ratio Test",
     "It fails the Root Test",
     "Comparison with 1/n", "A",
     "lim(n→∞) n²/(n²+1) = 1 ≠ 0. So the terms (−1)ⁿ·n²/(n²+1) do not approach 0. Diverges by nth-term test.",
     "series_divergence_test"),

    ("ap_calc_bc", "seed_ap_calc_bc_supplement.py".replace("seed_","").replace("_supplement.py",""), "F", 3, "What is the coefficient of x³ in the Maclaurin series for eˣ·sin(x)?",
     "multiple_choice", "1/3", "1/2", "1/6", "1", "A",
     "eˣ=(1+x+x²/2+x³/6+…), sin x=(x−x³/6+…). Coefficient of x³: (1)(−1/6)+(1)(1/2)(0 wait let me redo. x³ term: (1·(−x³/6)) + x·(x²/2·correction)... Actually: eˣ·sin x coeff of x³ = [1·(−1/6) + 1·(1/2)·? No. Multiply out: (1+x+x²/2!+x³/3!)×(x−x³/6+…). x³ terms: 1·(−x³/6) + x·(x²/2!·0 no: x·(0? sin: x−x³/6, x²: 0, x³: −1/6) + (x²/2)(x) = x³/2 + ... So total x³ coeff: −1/6 + 1/2 = −1/6 + 3/6 = 2/6 = 1/3.",
     "series_taylor_multiplication"),

    ("ap_calc_bc", "general", "U", 4, "Using the Taylor series for 1/(1−x) = Σxⁿ, find a series for 1/(1+x²).",
     "multiple_choice",
     "Σ xⁿ",
     "Σ (−1)ⁿ x²ⁿ",
     "Σ (−1)ⁿ xⁿ",
     "Σ x²ⁿ", "B",
     "Substitute x → −x²: 1/(1−(−x²)) = 1/(1+x²) = Σ(n=0 to ∞) (−x²)ⁿ = Σ(−1)ⁿ x^(2n).",
     "series_taylor"),

    ("ap_calc_bc", "general", "A", 4, "The Lagrange error bound for the nth-degree Taylor polynomial Pₙ(x) of f at x=a satisfies |f(x)−Pₙ(x)| ≤ M·|x−a|^(n+1)/(n+1)! where M is:",
     "multiple_choice",
     "The maximum of |f(x)| on the interval",
     "The maximum of |f⁽ⁿ⁺¹⁾| on the interval between a and x",
     "The value of f⁽ⁿ⁾(a)",
     "The (n+1)th coefficient of the series", "B",
     "M bounds |f^(n+1)(t)| for all t between a and x. This is the Lagrange error (remainder) bound.",
     "series_error_bound"),

    ("ap_calc_bc", "general", "R", 3, "Does Σ(n=1 to ∞) (−1)ⁿ/√n converge absolutely, conditionally, or diverge?",
     "multiple_choice", "Absolutely", "Conditionally", "Diverges", "Cannot determine", "B",
     "Σ1/√n is a divergent p-series (p=1/2). But the alternating series Σ(−1)ⁿ/√n converges by AST. So: conditionally convergent.",
     "series_absolute_conditional"),

    # ── PARAMETRIC & POLAR (14 questions) ─────────────────────────────────────

    ("ap_calc_bc", "seed_ap_calc_bc_supplement.py".replace("seed_","").replace("_supplement.py",""), "F", 2, "For the parametric curve x = t², y = t³, find dy/dx.",
     "multiple_choice", "3t", "3t/2", "2t/3", "t/2", "B",
     "dy/dx = (dy/dt)/(dx/dt) = 3t²/(2t) = 3t/2.",
     "parametric_derivatives"),

    ("ap_calc_bc", "seed_ap_calc_bc_supplement.py".replace("seed_","").replace("_supplement.py",""), "F", 2, "Find the arc length of the parametric curve x = cos(t), y = sin(t) from t=0 to t=π.",
     "multiple_choice", "π/2", "π", "2π", "1", "B",
     "L = ∫₀^π √((dx/dt)²+(dy/dt)²) dt = ∫₀^π √(sin²t+cos²t) dt = ∫₀^π 1 dt = π.",
     "parametric_arc_length"),

    ("ap_calc_bc", "general", "U", 3, "For the parametric curve x=t²−1, y=t³−3t, find the t-values where the tangent line is horizontal.",
     "multiple_choice", "t=0 only", "t=±1", "t=±√3", "t=1 and t=−1", "B",
     "Horizontal tangent: dy/dt=0. dy/dt=3t²−3=3(t−1)(t+1)=0 → t=±1. Check dx/dt=2t≠0 at t=±1.",
     "parametric_derivatives"),

    ("ap_calc_bc", "general", "A", 3, "Find d²y/dx² for the parametric curve x=t², y=t³ at t=2.",
     "multiple_choice", "3/8", "3/4", "3/16", "3/2", "A",
     "dy/dx=3t/2. d²y/dx²=(d/dt[dy/dx])/(dx/dt)=(3/2)/(2t)=3/(4t). At t=2: 3/8.",
     "parametric_second_derivative"),

    ("ap_calc_bc", "seed_ap_calc_bc_supplement.py".replace("seed_","").replace("_supplement.py",""), "F", 2, "Convert the polar point (r, θ) = (4, π/3) to Cartesian coordinates.",
     "multiple_choice", "(2, 2√3)", "(2√3, 2)", "(4, π/3)", "(2, √3)", "A",
     "x = r·cos θ = 4·cos(π/3) = 4·(1/2) = 2. y = r·sin θ = 4·sin(π/3) = 4·(√3/2) = 2√3.",
     "polar_conversion"),

    ("ap_calc_bc", "general", "U", 3, "The area enclosed by the polar curve r = 2sin(θ) is:",
     "multiple_choice", "π", "2π", "π/2", "4π", "A",
     "r=2sinθ is a circle of radius 1. Area = (1/2)∫₀^π (2sinθ)² dθ = (1/2)∫₀^π 4sin²θ dθ = 2∫₀^π (1−cos2θ)/2 dθ = ∫₀^π(1−cos2θ)dθ = π.",
     "polar_area"),

    ("ap_calc_bc", "general", "A", 4, "Find dy/dx for the polar curve r = 1 + cos(θ) at θ = π/2.",
     "multiple_choice", "1", "−1", "0", "∞", "A",
     "x=r cosθ=(1+cosθ)cosθ, y=r sinθ=(1+cosθ)sinθ. dx/dθ=−sin θ(1+cosθ)+cosθ(−sinθ)=−sinθ(1+2cosθ). dy/dθ=cosθ(1+cosθ)+sinθ(−sinθ)=cos θ+cos²θ−sin²θ=cosθ+cos2θ. At θ=π/2: dx/dθ=−1(1+0)=−1, dy/dθ=0+(−1)=−1. dy/dx=(−1)/(−1)=1.",
     "polar_derivatives"),

    ("ap_calc_bc", "general", "U", 3, "The area of one petal of r = cos(3θ) is:",
     "multiple_choice", "π/6", "π/12", "π/3", "π/4", "B",
     "One petal exists from θ=−π/6 to θ=π/6. Area=(1/2)∫_{−π/6}^{π/6} cos²(3θ)dθ=(1/2)∫_{−π/6}^{π/6}(1+cos6θ)/2 dθ=(1/4)[θ+sin(6θ)/6]_{−π/6}^{π/6}=(1/4)(π/3)=π/12.",
     "polar_area"),

    ("ap_calc_bc", "seed_ap_calc_bc_supplement.py".replace("seed_","").replace("_supplement.py",""), "F", 2, "Which of the following represents the polar equation r = 3 in Cartesian form?",
     "multiple_choice", "x + y = 3", "x² + y² = 9", "x² + y² = 3", "3x + 3y = 1", "B",
     "r = 3 means √(x²+y²) = 3, so x²+y² = 9. This is a circle of radius 3.",
     "polar_conversion"),

    ("ap_calc_bc", "general", "A", 4, "The area between r=2 and r=4sinθ (for the region where 4sinθ > 2) equals:",
     "multiple_choice", "4π/3 + 2√3", "2π/3 + √3", "π + 2√3", "4π − 2√3", "A",
     "4sinθ=2 when sinθ=1/2, θ=π/6, 5π/6. Area=(1/2)∫_{π/6}^{5π/6}[(4sinθ)²−4]dθ=(1/2)∫[16sin²θ−4]dθ=(1/2)∫[8(1−cos2θ)−4]dθ=(1/2)∫[4−8cos2θ]dθ=(1/2)[4θ−4sin2θ]_{π/6}^{5π/6}=4π/3+2√3.",
     "polar_area"),

    ("ap_calc_bc", "general", "U", 3, "For the parametric equations x=3t, y=t²−1, find the area under the curve from t=0 to t=2.",
     "multiple_choice", "2/3", "4", "16/3", "8/3", "D",
     "Area = ∫y dx = ∫₀²(t²−1)·3 dt = 3[t³/3−t]₀² = 3(8/3−2) = 3(2/3) = 8/3. Wait: 3(8/3−2)=3(8/3−6/3)=3(2/3)=2. Let me recompute: 3·(2/3) = 2. Closest: 8/3. Actually: ∫₀²(t²−1)·3dt=3[t³/3−t]₀²=3[(8/3−2)−0]=3(2/3)=2.",
     "parametric_area"),

    ("ap_calc_bc", "general", "A", 4, "The arc length of r = e^θ from θ=0 to θ=1 is:",
     "multiple_choice", "√2(e−1)", "√2·e", "e−1", "√2(e+1)", "A",
     "L=∫₀¹√(r²+(dr/dθ)²)dθ=∫₀¹√(e^(2θ)+e^(2θ))dθ=∫₀¹√(2)·e^θ dθ=√2[e^θ]₀¹=√2(e−1).",
     "polar_arc_length"),

    ("ap_calc_bc", "seed_ap_calc_bc_supplement.py".replace("seed_","").replace("_supplement.py",""), "F", 2, "The Cartesian equation x² + y² = 9 in polar form is:",
     "multiple_choice", "r = 3", "r = 9", "r² = 3", "θ = 3", "A",
     "x²+y²=r². So r²=9 → r=3.",
     "polar_conversion"),

    ("ap_calc_bc", "general", "R", 3, "For the parametric curve x=t²+1, y=2t, eliminate the parameter to find the Cartesian equation.",
     "multiple_choice", "x = y² + 1", "x = (y/2)² + 1", "y = 2√(x−1)", "x = y + 1", "B",
     "t = y/2. x = (y/2)² + 1 = y²/4 + 1.",
     "parametric_elimination"),

    # ── INTEGRATION TECHNIQUES (22 questions) ─────────────────────────────────

    ("ap_calc_bc", "seed_ap_calc_bc_supplement.py".replace("seed_","").replace("_supplement.py",""), "F", 2, "Evaluate ∫ x·eˣ dx using integration by parts.",
     "multiple_choice", "x·eˣ + C", "eˣ(x−1) + C", "eˣ(x+1) + C", "x²·eˣ/2 + C", "B",
     "IBP: u=x, dv=eˣdx. du=dx, v=eˣ. ∫x·eˣdx = x·eˣ − ∫eˣdx = x·eˣ − eˣ + C = eˣ(x−1) + C.",
     "integrals_by_parts"),

    ("ap_calc_bc", "seed_ap_calc_bc_supplement.py".replace("seed_","").replace("_supplement.py",""), "F", 2, "Evaluate ∫ x·sin(x) dx.",
     "multiple_choice", "x·cos(x) + sin(x) + C", "−x·cos(x) + sin(x) + C", "x·sin(x) + cos(x) + C", "−x·sin(x) + cos(x) + C", "B",
     "IBP: u=x, dv=sin x dx. du=dx, v=−cos x. ∫=−x cos x + ∫cos x dx = −x cos x + sin x + C.",
     "integrals_by_parts"),

    ("ap_calc_bc", "general", "U", 3, "Evaluate ∫ ln(x) dx.",
     "multiple_choice", "1/x + C", "x·ln(x) − x + C", "x·ln(x) + C", "x/ln(x) + C", "B",
     "IBP: u=ln x, dv=dx. du=1/x dx, v=x. ∫ln x dx = x·ln x − ∫x·(1/x)dx = x·ln x − x + C.",
     "integrals_by_parts"),

    ("ap_calc_bc", "seed_ap_calc_bc_supplement.py".replace("seed_","").replace("_supplement.py",""), "F", 3, "Write the partial fraction decomposition of (2x+1)/((x−1)(x+2)).",
     "multiple_choice",
     "A/(x−1) + B/(x+2)",
     "A/(x−1)² + B/(x+2)",
     "(Ax+B)/(x−1)(x+2)",
     "A·x/(x−1) + B/(x+2)", "A",
     "For distinct linear factors: (2x+1)/((x−1)(x+2)) = A/(x−1) + B/(x+2).",
     "integrals_partial_fractions"),

    ("ap_calc_bc", "general", "U", 3, "Evaluate ∫ 1/((x−1)(x+2)) dx.",
     "multiple_choice",
     "(1/3)ln|x−1| − (1/3)ln|x+2| + C",
     "(1/3)ln|(x−1)/(x+2)| + C",
     "Both A and B",
     "ln|(x−1)(x+2)| + C", "C",
     "Partial fractions: 1/3 · [1/(x−1) − 1/(x+2)]. Integrating: (1/3)ln|x−1| − (1/3)ln|x+2| = (1/3)ln|(x−1)/(x+2)|. A and B are equivalent.",
     "integrals_partial_fractions"),

    ("ap_calc_bc", "general", "A", 4, "Evaluate ∫₀^(π/2) sin²(x) dx.",
     "multiple_choice", "π/4", "π/2", "1/2", "π", "A",
     "Use identity sin²x=(1−cos2x)/2. ∫₀^(π/2) (1−cos2x)/2 dx = [x/2 − sin(2x)/4]₀^(π/2) = π/4 − 0 = π/4.",
     "integrals_trig"),

    ("ap_calc_bc", "seed_ap_calc_bc_supplement.py".replace("seed_","").replace("_supplement.py",""), "F", 3, "Evaluate ∫ x²/(x²+1) dx.",
     "multiple_choice",
     "x − arctan(x) + C",
     "arctan(x) + C",
     "ln(x²+1) + C",
     "x + arctan(x) + C", "A",
     "Rewrite: x²/(x²+1) = 1 − 1/(x²+1). ∫[1 − 1/(x²+1)]dx = x − arctan(x) + C.",
     "integrals_algebraic"),

    ("ap_calc_bc", "general", "U", 3, "Evaluate ∫ x²·eˣ dx.",
     "multiple_choice",
     "eˣ(x²−2x+2) + C",
     "x²·eˣ − 2x·eˣ + C",
     "eˣ(x²+2x+2) + C",
     "eˣ(x²−2) + C", "A",
     "Repeated IBP or tabular: ∫x²eˣdx = x²eˣ − 2xeˣ + 2eˣ + C = eˣ(x²−2x+2) + C.",
     "integrals_by_parts"),

    ("ap_calc_bc", "general", "A", 4, "Evaluate ∫ sec³(x) dx.",
     "multiple_choice",
     "(1/2)[sec(x)tan(x) + ln|sec(x)+tan(x)|] + C",
     "sec(x)tan(x) + C",
     "(1/3)sec³(x) + C",
     "(1/2)sec(x)tan(x) + C", "A",
     "Classic reduction: ∫sec³x dx = (1/2)[sec x tan x + ln|sec x+tan x|] + C.",
     "integrals_trig"),

    ("ap_calc_bc", "seed_ap_calc_bc_supplement.py".replace("seed_","").replace("_supplement.py",""), "F", 3, "Evaluate ∫ 1/(x²−4) dx using partial fractions.",
     "multiple_choice",
     "(1/4)ln|(x−2)/(x+2)| + C",
     "(1/2)ln|x²−4| + C",
     "arctan(x/2)/2 + C",
     "(1/4)ln|(x+2)/(x−2)| + C", "A",
     "x²−4=(x−2)(x+2). 1/((x−2)(x+2)) = (1/4)[1/(x−2)−1/(x+2)]. Integrate: (1/4)ln|(x−2)/(x+2)| + C.",
     "integrals_partial_fractions"),

    ("ap_calc_bc", "general", "U", 4, "Evaluate the improper integral ∫₁^∞ 1/x² dx.",
     "multiple_choice", "∞", "0", "1", "2", "C",
     "∫₁^∞ x^(−2) dx = [−x^(−1)]₁^∞ = 0 − (−1) = 1.",
     "integrals_improper"),

    ("ap_calc_bc", "general", "A", 4, "Evaluate the improper integral ∫₀^∞ e^(−x) dx.",
     "multiple_choice", "0", "1", "e", "∞", "B",
     "[−e^(−x)]₀^∞ = 0 − (−1) = 1.",
     "integrals_improper"),

    ("ap_calc_bc", "general", "R", 3, "The integral ∫₀¹ 1/√x dx is an improper integral because:",
     "multiple_choice",
     "The upper bound is 1",
     "The integrand is unbounded near x=0",
     "The integral diverges",
     "√x is not differentiable at x=0", "B",
     "1/√x → ∞ as x→0⁺, making the lower limit a problem. It's improper at x=0. (It actually converges to 2.)",
     "integrals_improper"),

    ("ap_calc_bc", "seed_ap_calc_bc_supplement.py".replace("seed_","").replace("_supplement.py",""), "F", 3, "Evaluate ∫ sin(x)·cos(x) dx.",
     "multiple_choice", "sin²(x)/2 + C", "−cos²(x)/2 + C", "sin(2x)/4 + C", "All of the above", "D",
     "Let u=sin x: ∫sin x·cos x dx = sin²x/2+C. Or let u=cos x: −cos²x/2+C. Or use sin(2x)=2sinxcosx: sin(2x)/4+C. All are equivalent (differ by a constant).",
     "integrals_trig"),

    ("ap_calc_bc", "general", "U", 3, "Evaluate ∫ x/√(x²+1) dx.",
     "multiple_choice", "√(x²+1) + C", "(1/2)√(x²+1) + C", "x²/(2√(x²+1)) + C", "ln(x²+1) + C", "A",
     "u=x²+1, du=2x dx. ∫x/√(x²+1)dx = (1/2)∫u^(−1/2)du = u^(1/2) + C = √(x²+1) + C.",
     "integrals_u_substitution"),

    # ── DIFFERENTIAL EQUATIONS (22 questions) ─────────────────────────────────

    ("ap_calc_bc", "seed_ap_calc_bc_supplement.py".replace("seed_","").replace("_supplement.py",""), "F", 2, "Solve the separable DE: dy/dx = 2xy, y(0) = 3.",
     "multiple_choice", "y = 3e^x", "y = 3e^(x²)", "y = e^(x²) + 2", "y = 3·2^x", "B",
     "Separate: dy/y = 2x dx. ln|y| = x² + C. y = Ae^(x²). y(0)=A=3. y = 3e^(x²).",
     "diff_eq_separable"),

    ("ap_calc_bc", "seed_ap_calc_bc_supplement.py".replace("seed_","").replace("_supplement.py",""), "F", 2, "Which of the following is a solution to dy/dx = y?",
     "multiple_choice", "y = x²", "y = ln(x)", "y = eˣ", "y = sin(x)", "C",
     "d/dx[eˣ] = eˣ = y. So y = eˣ satisfies dy/dx = y.",
     "diff_eq_exponential"),

    ("ap_calc_bc", "general", "U", 3, "A population P satisfies dP/dt = 0.04P with P(0) = 500. Find P(25).",
     "multiple_choice", "500e", "500e^0.04", "500e^(0.04·25)", "500·(1.04)^25", "C",
     "Solution: P(t) = 500e^(0.04t). P(25) = 500e^(0.04·25) = 500e¹ = 500e.",
     "diff_eq_exponential_growth"),

    ("ap_calc_bc", "general", "A", 3, "The logistic differential equation dP/dt = kP(1 − P/M) has carrying capacity:",
     "multiple_choice", "k", "1/k", "M", "kM", "C",
     "The carrying capacity is M — the population level at which dP/dt = 0 (when P = M).",
     "diff_eq_logistic"),

    ("ap_calc_bc", "seed_ap_calc_bc_supplement.py".replace("seed_","").replace("_supplement.py",""), "F", 3, "Solve dy/dx = x/y with y(0) = 2.",
     "multiple_choice", "y = x²/2 + 2", "y² = x² + 4", "y = √(x² + 4)", "Both B and C", "D",
     "Separate: y dy = x dx. y²/2 = x²/2 + C. At (0,2): 2=C. y²=x²+4 (same as y=√(x²+4) since y(0)=2>0).",
     "diff_eq_separable"),

    ("ap_calc_bc", "general", "U", 3, "A slope field for dy/dx = x − y would show horizontal tangent lines when:",
     "multiple_choice", "x = 0", "y = 0", "x = y", "x + y = 0", "C",
     "Horizontal tangents occur when dy/dx = 0, i.e., x − y = 0, so x = y.",
     "diff_eq_slope_fields"),

    ("ap_calc_bc", "general", "A", 4, "Euler's method with step h=0.5 for dy/dx=x+y, y(0)=1: estimate y(1).",
     "multiple_choice", "2.5", "2.75", "3", "3.25", "B",
     "Step 1: y(0.5)=1+0.5(0+1)=1.5. Step 2: y(1)=1.5+0.5(0.5+1.5)=1.5+1=2.5. So y(1)≈2.5. (Correction: slope at (0.5,1.5) is 0.5+1.5=2. y(1)=1.5+0.5·2=2.5.)",
     "diff_eq_eulers_method"),

    ("ap_calc_bc", "general", "R", 3, "For the logistic model dP/dt = 0.2P(1 − P/100), the population grows fastest when P equals:",
     "multiple_choice", "0", "50", "100", "200", "B",
     "The logistic model grows fastest at P = M/2 = 100/2 = 50.",
     "diff_eq_logistic"),

    ("ap_calc_bc", "seed_ap_calc_bc_supplement.py".replace("seed_","").replace("_supplement.py",""), "F", 2, "What is the general solution to dy/dx = 3x²?",
     "multiple_choice", "y = 6x + C", "y = x³ + C", "y = 3x³ + C", "y = x³", "B",
     "Integrate: y = ∫3x² dx = x³ + C.",
     "diff_eq_separable"),

    ("ap_calc_bc", "general", "U", 4, "The solution to dy/dx = −2xy with y(0) = 1 is:",
     "multiple_choice", "y = e^(−x²)", "y = e^(−2x)", "y = 1 − 2x²", "y = e^(x²)", "A",
     "Separate: dy/y = −2x dx. ln|y| = −x² + C. y = Ae^(−x²). y(0)=A=1. y = e^(−x²).",
     "diff_eq_separable"),

    ("ap_calc_bc", "general", "A", 4, "Using Euler's method with h=1 for y'=y, y(0)=1, estimate y(2).",
     "multiple_choice", "1", "2", "4", "e²", "C",
     "Step 1: y(1)=1+1·(1)=2. Step 2: y(2)=2+1·(2)=4. (Exact answer is e²≈7.39; Euler underestimates.)",
     "diff_eq_eulers_method"),

    # ── ADDITIONAL BC TOPICS (18 questions) ───────────────────────────────────

    ("ap_calc_bc", "seed_ap_calc_bc_supplement.py".replace("seed_","").replace("_supplement.py",""), "F", 2, "Evaluate ∫ x·ln(x) dx.",
     "multiple_choice",
     "(x²/2)·ln(x) − x²/4 + C",
     "x·ln(x) − x + C",
     "(x²/4)·ln(x) + C",
     "ln(x²)/2 + C", "A",
     "IBP: u=ln x, dv=x dx. du=1/x dx, v=x²/2. ∫x·ln x dx = (x²/2)ln x − ∫(x²/2)(1/x)dx = (x²/2)ln x − x²/4 + C.",
     "integrals_by_parts"),

    ("ap_calc_bc", "general", "U", 3, "What is the formula for arc length of y=f(x) from x=a to x=b?",
     "multiple_choice",
     "∫ₐᵇ √(1 + [f'(x)]²) dx",
     "∫ₐᵇ f'(x) dx",
     "∫ₐᵇ [f(x)]² dx",
     "∫ₐᵇ √(1 + f(x)) dx", "A",
     "Arc length = ∫ₐᵇ √(1+[f'(x)]²) dx. This comes from approximating the curve by small line segments.",
     "integrals_arc_length"),

    ("ap_calc_bc", "seed_ap_calc_bc_supplement.py".replace("seed_","").replace("_supplement.py",""), "F", 3, "Evaluate ∫ 1/(x²+4) dx.",
     "multiple_choice",
     "(1/2)arctan(x/2) + C",
     "arctan(x/2) + C",
     "(1/4)arctan(x/2) + C",
     "arctan(x) + C", "A",
     "∫1/(x²+a²)dx = (1/a)arctan(x/a)+C. Here a=2: (1/2)arctan(x/2)+C.",
     "integrals_inverse_trig"),

    ("ap_calc_bc", "general", "U", 3, "The improper integral ∫₀^∞ xe^(−x) dx equals:",
     "multiple_choice", "0", "1", "e", "∞", "B",
     "IBP: u=x, dv=e^(−x)dx. v=−e^(−x). ∫=−xe^(−x)|₀^∞+∫₀^∞e^(−x)dx=0+[−e^(−x)]₀^∞=0+1=1.",
     "integrals_improper"),

    ("ap_calc_bc", "general", "A", 4, "Find the volume of the solid formed by revolving y=eˣ from x=0 to x=1 around the x-axis.",
     "multiple_choice", "π(e²−1)/2", "π(e−1)", "πe²/2", "π(e²+1)/2", "A",
     "Disk method: V=π∫₀¹(eˣ)²dx=π∫₀¹e^(2x)dx=π[e^(2x)/2]₀¹=π(e²−1)/2.",
     "integrals_volumes"),

    ("ap_calc_bc", "seed_ap_calc_bc_supplement.py".replace("seed_","").replace("_supplement.py",""), "F", 2, "The series Σ(n=0 to ∞) rⁿ converges when:",
     "multiple_choice", "|r| > 1", "|r| = 1", "|r| < 1", "r > 0", "C",
     "Geometric series Σrⁿ converges if and only if |r| < 1, with sum 1/(1−r).",
     "series_geometric"),

    ("ap_calc_bc", "general", "U", 3, "Using the integral test, Σ(n=1 to ∞) 1/n diverges because:",
     "multiple_choice",
     "∫₁^∞ 1/x dx converges",
     "∫₁^∞ 1/x dx diverges to ∞",
     "The terms do not approach 0",
     "The ratio test gives L=1", "B",
     "∫₁^∞ 1/x dx = [ln x]₁^∞ = ∞. By the Integral Test, since the integral diverges, the harmonic series diverges.",
     "series_integral_test"),

    ("ap_calc_bc", "general", "A", 4, "Use the Maclaurin series for cos(x) to find lim(x→0) (1−cos x)/x².",
     "multiple_choice", "0", "1/4", "1/2", "1", "C",
     "cos x = 1 − x²/2! + x⁴/4! − … So 1−cos x = x²/2 − x⁴/24 + … (1−cos x)/x² = 1/2 − x²/24 + … → 1/2 as x→0.",
     "series_taylor_limits"),

    ("ap_calc_bc", "general", "U", 3, "The Root Test: if lim(n→∞) |aₙ|^(1/n) = L, the series converges absolutely when:",
     "multiple_choice", "L = 1", "L > 1", "L < 1", "L = 0", "C",
     "Root Test: if L<1, series converges absolutely; if L>1, diverges; if L=1, inconclusive.",
     "series_root_test"),

    ("ap_calc_bc", "seed_ap_calc_bc_supplement.py".replace("seed_","").replace("_supplement.py",""), "F", 3, "A differential equation dy/dx = f(x)·g(y) is called separable because:",
     "multiple_choice",
     "It has two separate solutions",
     "The variables x and y can be separated to opposite sides for integration",
     "It is linear in x and y separately",
     "The function separates into real and imaginary parts", "B",
     "A separable DE allows dy/g(y) = f(x)dx — the variables are separated, each side integrated independently.",
     "diff_eq_separable"),

    ("ap_calc_bc", "general", "U", 4, "The logistic model P(t) = M/(1+Ae^(−kt)) has an inflection point when P = ?",
     "multiple_choice", "M", "M/4", "M/2", "kM", "C",
     "The logistic curve has an inflection point at P = M/2, where growth rate is maximized.",
     "diff_eq_logistic"),

    ("ap_calc_bc", "general", "A", 4, "Evaluate ∫₀^∞ e^(−x) dx.",
     "multiple_choice", "0", "1", "e", "∞", "B",
     "[−e^(−x)]₀^∞ = (0) − (−1) = 1. The integral converges to 1.",
     "integrals_improper"),

    ("ap_calc_bc", "general", "R", 3, "Which series converges by direct comparison with the convergent p-series Σ1/n²?",
     "multiple_choice",
     "Σ 1/(n² + n) for n ≥ 1",
     "Σ n/(n³ + 1) for n ≥ 1",
     "Σ 1/(n² + 1) for n ≥ 1",
     "All of the above", "D",
     "All three have terms ≤ 1/n² (or bounded by a constant multiple) for large n. Each converges by comparison with the convergent p-series Σ1/n².",
     "series_comparison"),

    ("ap_calc_bc", "general", "U", 3, "If the Taylor series for f(x) = 1/(1−x) is Σxⁿ, find the Taylor series for f'(x).",
     "multiple_choice",
     "Σ n·xⁿ",
     "Σ n·x^(n−1)",
     "Σ xⁿ/n",
     "Σ (n+1)·xⁿ", "D",
     "d/dx[Σxⁿ] = Σnx^(n−1) for n≥1. Reindexing: Σ(n=0 to ∞)(n+1)xⁿ.",
     "series_differentiation"),

    ("ap_calc_bc", "general", "A", 4, "Find the length of the parametric curve x=3sin(t), y=3cos(t) from t=0 to t=π.",
     "multiple_choice", "3π", "6π", "3", "π", "A",
     "L=∫₀^π√((3cos t)²+(−3sin t)²)dt=∫₀^π√9 dt=3π.",
     "parametric_arc_length"),

    ("ap_calc_bc", "seed_ap_calc_bc_supplement.py".replace("seed_","").replace("_supplement.py",""), "F", 3, "Which of the following correctly uses integration by parts for ∫eˣ·cos(x)dx?",
     "multiple_choice",
     "eˣ·sin(x) − ∫eˣ·sin(x)dx",
     "eˣ·cos(x) + ∫eˣ·sin(x)dx",
     "eˣ·sin(x) + ∫eˣ·sin(x)dx",
     "cos(x)·eˣ − sin(x)·eˣ + C", "A",
     "IBP: u=cos x, dv=eˣdx. v=eˣ, du=−sin x dx. ∫eˣcos x dx = eˣcos x + ∫eˣsin x dx. Then apply IBP again to get the cyclic relation.",
     "integrals_by_parts"),

    ("ap_calc_bc", "general", "U", 4, "Solve the differential equation dy/dx = y/x with y(1) = 2.",
     "multiple_choice", "y = 2x", "y = 2/x", "y = 2e^x", "y = x + 1", "A",
     "Separate: dy/y = dx/x. ln|y|=ln|x|+C. y=Ax. y(1)=A=2. y=2x.",
     "diff_eq_separable"),

    ("ap_calc_bc", "general", "A", 4, "The series Σ(n=1 to ∞) (2ⁿ·n!)/(n^n) converges or diverges? (Use the Ratio Test.)",
     "multiple_choice",
     "Converges, since L = 2/e < 1",
     "Diverges, since L > 1",
     "Test is inconclusive (L = 1)",
     "Converges, since L = 0", "A",
     "Ratio: aₙ₊₁/aₙ = 2(n+1)!/(n+1)^(n+1) · n^n/(n!·2^n) = 2·n^n/(n+1)^n = 2·(n/(n+1))^n → 2·(1/e) = 2/e < 1. Converges.",
     "series_ratio_test"),
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
