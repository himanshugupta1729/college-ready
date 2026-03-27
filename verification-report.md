# College Ready — Question Bank Verification Report

**Total questions reviewed:** 864
**Confirmed errors found:** 16
**Date:** 2026-03-19
**Method:** Automated arithmetic checks (verify_questions.py) + manual review of all seed source files

---

## Executive Summary

Out of 864 questions, **16 confirmed errors** were found after cross-referencing the automated script output against the actual seed file source.

| Severity | Count | Type |
|----------|-------|------|
| CRITICAL | 2 | No correct option exists among A–D |
| HIGH | 9 | Wrong answer in answer key (explanation confirms different answer) |
| MEDIUM | 5 | Duplicate options (two choices are identical) |
| LOW | 1 | Ambiguous question — no integer answer is exactly correct |

All items flagged by the automated checker that are NOT in this list were verified as false positives from partial regex matching. See the False Positives section at the bottom.

**All CRITICAL and HIGH items must be fixed before students use this bank.**

---

## CRITICAL — No Correct Option Available

These questions have no option among A–D that equals the mathematically correct answer.

---

### Q612 — `algebra_2` / `polynomials` (Difficulty 4)

**Question:** What is the remainder when 2x⁴ − 3x³ + x − 5 is divided by (x + 1)?

| Option | Value |
|--------|-------|
| A | −11 ← stated answer |
| B | −9 |
| C | −7 |
| D | −5 |

**Correct math:** By the Remainder Theorem, p(−1) = 2(1) − 3(−1) + (−1) − 5 = 2 + 3 − 1 − 5 = **−1**.

**Issue:** The remainder is −1 but none of the four options equals −1. The explanation acknowledges this verbatim: "None of the listed options equals −1, so replace." but still marks A (= −11) as correct. The stated answer −11 is wrong.

**Fix:** Replace option A with "−1" and mark A correct. Or replace the question entirely.

---

### Q844 — `ap_calc_ab` / `integration` (Difficulty 3)

**Question:** Evaluate ∫₀¹ 2x√(x²+1) dx.

| Option | Value |
|--------|-------|
| A | 2√2 − 2 |
| B | √2 − 1 |
| C | 2(√2 − 1) ← stated answer |
| D | 4√2 |

**Correct math:** Let u = x²+1. ∫₁² √u du = [(2/3)u^(3/2)]₁² = (2/3)(2√2) − (2/3)(1) = (4√2 − 2)/3 ≈ **0.943**.

**Issue:** None of the options equals (4√2 − 2)/3. The explanation correctly computes 0.943 and acknowledges "That doesn't match C exactly" and calls option C "the closest." Option C = 2(√2 − 1) ≈ 0.828, which is off by ~12%. This is not an acceptable approximation for a math test.

**Fix:** Replace option C with `(4√2 − 2)/3` and mark C correct.

---

## HIGH — Wrong Answer Key

In all cases below, the explanation performs the correct math and explicitly names a different option as the answer — but the `correct_answer` field in the database was not updated.

---

### Q277 — `ap_calc_ab` / `limits_continuity` (Difficulty 2)

**Question:** What value of k makes f(x) = {kx + 1 if x < 2; x² − 1 if x ≥ 2} continuous at x = 2?

| Option | Value |
|--------|-------|
| A | 0 |
| B | 1 |
| C | 2 ← **STATED ANSWER (WRONG)** |
| D | 3 |

**Explanation says:** "Set 2k + 1 = 3 → k = 1. Wait — k = 1 gives 3 = 3. ✓ **Answer is k = 1.**"

k = 1 is option B. The correct answer is B, not C.

**Fix:** `correct_answer = 'B'`

---

### Q331 — `ap_calc_ab` / `integration` (Difficulty 3)

**Question:** Evaluate ∫ 2x(x² + 1)⁴ dx using u-substitution.

| Option | Value |
|--------|-------|
| A | (x²+1)⁵ / 5 + C |
| B | (x²+1)⁵ + C ← **STATED ANSWER (WRONG)** |
| C | 2(x²+1)⁵ / 5 + C |
| D | 10x²(x²+1)³ + C |

**Explanation says:** "∫u⁴ du = u⁵/5 + C = (x²+1)⁵/5 + C. Wait: answer is (x²+1)⁵/5 + C (Option A, not B). **Correction: option A is correct. Answer: A.**"

The correct answer is (x²+1)⁵/5 + C = option A.

**Fix:** `correct_answer = 'A'`

---

### Q350 — `ap_calc_ab` / `integration_apps` (Difficulty 4)

**Question:** Find the area between y = sin x and y = cos x on [0, π/4].

| Option | Value |
|--------|-------|
| A | √2 − 1 |
| B | 1 − 1/√2 |
| C | √2 − √2/2 |
| D | 2 − √2 ← **STATED ANSWER (WRONG)** |

**Explanation says:** "Area = ∫₀^(π/4) (cos x − sin x) dx = [sin x + cos x]₀^(π/4) = (√2/2 + √2/2) − (0 + 1) = **√2 − 1**. Rechecking: Area = √2 − 1 ≈ 0.414. **Answer A.**"

The correct answer is √2 − 1 = option A.

**Fix:** `correct_answer = 'A'`

---

### Q713 — `ap_calc_ab` / `diff_analytical` (Difficulty 5)

**Question:** A closed box with a square base has volume 32 cm³. What base side length minimizes total surface area?

| Option | Value |
|--------|-------|
| A | 2 cm ← **STATED ANSWER (WRONG)** |
| B | 4 cm |
| C | 2∛4 cm |
| D | 8 cm |

**Explanation says:** "dSA/dx = 4x − 128/x² = 0 → x³ = 32 → x = ∛32 = 2∛4. Wait: x³ = 32, so x = 2∛4 ≈ 3.17. **The minimum is at x = ∛32 = 2∛4 cm (option C).**"

The correct answer is 2∛4 cm = option C.

**Fix:** `correct_answer = 'C'`

---

### Q695 — `algebra_1` / `linear_equations` (Difficulty 2)

**Question:** Solve for x: 2(x + 4) = 18.

| Option | Value |
|--------|-------|
| A | 5 |
| B | 7 ← **STATED ANSWER (WRONG)** |
| C | 9 |
| D | 11 |

**Explanation says:** "2x + 8 = 18 → 2x = 10 → x = 5. Wait — 2(5+4) = 18 ✓. **Answer is A (x = 5).**"

x = 5 is option A. Verification: 2(5+4) = 2(9) = 18 ✓

**Fix:** `correct_answer = 'A'`

---

### Q698 — `algebra_1` / `linear_equations` (Difficulty 4)

**Question:** The perimeter of a rectangle is 54 cm. The length is 3 cm more than twice the width. What is the width?

| Option | Value |
|--------|-------|
| A | 7 cm |
| B | 8 cm |
| C | 9 cm ← **STATED ANSWER (WRONG)** |
| D | 12 cm |

**Explanation says:** "6w + 6 = 54 → 6w = 48 → **w = 8**. Wait: 2(8) + 3 = 19, 2(8+19) = 54 ✓. **Width = 8 cm. Answer B.**"

w = 8 cm is option B. Verification: length = 2(8)+3 = 19, perimeter = 2(8+19) = 54 ✓

**Fix:** `correct_answer = 'B'`

---

### Q757 — `algebra_1` / `data_stats` (Difficulty 1)

**Question:** The scores on a quiz are: 70, 80, 85, 90, 100. What is the mean?

| Option | Value |
|--------|-------|
| A | 80 |
| B | 83 ← **STATED ANSWER (WRONG)** |
| C | 85 |
| D | 90 |

**Explanation says:** "Mean = (70+80+85+90+100)/5 = 425/5 = **85**. Wait — that's 85. Re-check: 70+80+85+90+100 = 425; 425/5 = 85. **Answer C.**"

Mean = 85 = option C. Verification: 425/5 = 85 ✓

**Fix:** `correct_answer = 'C'`

---

### Q765 — `algebra_1` / `data_stats` (Difficulty 4)

**Question:** A data set has mean 20 and 10 data points. A new data point of 40 is added. What is the new mean?

| Option | Value |
|--------|-------|
| A | 21.8 |
| B | 22 ← **STATED ANSWER (WRONG)** |
| C | 24 |
| D | 25 |

**Explanation says:** "Original sum = 20 × 10 = 200. New sum = 200 + 40 = 240. New mean = 240 / 11 ≈ **21.8**. **Closest answer is 21.8.**"

New mean = 240/11 ≈ 21.818 ≈ 21.8 = option A.

**Fix:** `correct_answer = 'A'`

---

### Q818 — `geometry` / `circles` (Difficulty 5)

**Question:** A tangent and a secant are drawn from an external point. The tangent has length 12 and the secant's external segment is 6. What is the secant's total length?

| Option | Value |
|--------|-------|
| A | 18 |
| B | 24 |
| C | 30 ← **STATED ANSWER (WRONG)** |
| D | 36 |

**Explanation says:** "Tangent-Secant theorem: tangent² = external segment × whole secant. 144 = 6 × whole → whole = 24. Wait: 12² = 6 × whole → 144 = 6 × whole → whole = **24**. **Answer B.**"

Whole secant = 144/6 = 24 = option B.

**Fix:** `correct_answer = 'B'`

---

### Q1224 — `ap_precalc` / `trig_polar` (Difficulty 4)

**Question:** If sin(A) = 4/5 (A in Q1) and cos(B) = −5/13 (B in Q2), what is sin(A + B)?

| Option | Value |
|--------|-------|
| A | −16/65 |
| B | 56/65 |
| C | −56/65 ← **STATED ANSWER (WRONG)** |
| D | 16/65 |

**Explanation says:** "cos(A) = 3/5. sin(B) = 12/13. sin(A+B) = (4/5)(−5/13) + (3/5)(12/13) = −20/65 + 36/65 = **16/65**. Wait — recalculate: −20/65 + 36/65 = **16/65**."

sin(A+B) = 16/65 = option D.

**Fix:** `correct_answer = 'D'`

---

## MEDIUM — Duplicate Options

Each of these questions has two options with identical text. Students who look at all four choices will see a repeated option and recognize something is wrong.

---

### Q750 — `algebra_1` / `exponentials` (Difficulty 3)

**Question:** A bacteria culture starts with 100 cells and triples every hour. How many cells after 4 hours?

**Options:** A=1200, B=3600, **C=8100**, **D=8100** (C and D are identical)

Correct answer: C (= 100 × 3⁴ = 8100 ✓). Answer key is right, but D is a copy of C.

**Fix:** Replace option D with a distinct distractor (e.g., 2700).

---

### Q845 — `precalculus` / `functions` (Difficulty 1)

**Question:** Given g(x) = 2x − 4, what is g(3)?

**Options:** **A=2**, B=6, C=10, **D=2** (A and D are identical)

Correct answer: A (= 2(3) − 4 = 2 ✓). Answer key is right, but D is a copy of A.

**Fix:** Replace option D with a distinct distractor (e.g., 4 or −2).

---

### Q933 — `statistics` / `descriptive_stats` (Difficulty 3)

**Question:** Test scores: 72, 85, 90, 68, 95, 88, 72, 79. What is the mean?

**Options:** **A=81.1**, B=80.2, **C=81.1**, D=83.5 (A and C are identical)

Correct answer: A (mean = 649/8 = 81.125 ≈ 81.1 ✓). Answer key is right, but C is a copy of A.

**Fix:** Replace option C with a distinct distractor (e.g., 81.5 or 80.8).

---

### Q1185 — `ap_precalc` / `exp_log` (Difficulty 3)

**Question:** Geometric sequence: a₁ = 3, r = 2. What is the 5th term?

**Options:** A=24, B=36, **C=48**, **D=48** (C and D are identical)

Correct answer: C (= 3 × 2⁴ = 48 ✓). Answer key is right, but D is a copy of C.

**Fix:** Replace option D with a distinct distractor (e.g., 64).

---

### Q1197 — `ap_precalc` / `exp_log` (Difficulty 4)

**Question:** Geometric series: a₁ = 2, r = 3. Find S₄.

**Options:** A=26, B=40, **C=80**, **D=80** (C and D are identical)

Correct answer: C (= 2(1−3⁴)/(1−3) = 2(−80)/(−2) = 80 ✓). Answer key is right, but D is a copy of C.

**Fix:** Replace option D with a distinct distractor (e.g., 162).

---

## LOW — Ambiguous / No Exact Answer

---

### SY-11 — `algebra_1` / `systems` (Difficulty 4)

**Question:** A canoe rental costs $12 plus $4 per hour. A kayak costs $5 plus $7 per hour. After how many hours will both cost the same?

**Options:** A=2 hours, B=3 hours, C=4 hours, D=5 hours

**Issue:** Setting equal: 12 + 4h = 5 + 7h → h = 7/3 ≈ 2.33 hours. No integer option is exactly correct. The explanation acknowledges "the answer is h = 7/3" but marks B (3 hours) — which is not the correct breakeven point.

**Fix options:**
- Rewrite the question with costs that give an integer solution (e.g., canoe: $10 + $3/hr, kayak: $4 + $6/hr → h = 2)
- Or change option A to "7/3 hours" and mark it correct

---

## Automated False Positives (Not Real Errors)

The automated script also flagged ~55 additional items. All were verified as false positives:

| Pattern | Example | Cause |
|---------|---------|-------|
| `9/25 = 16` | `1 − 9/25 = 16/25` | Regex stopped at first integer before `/25` |
| `12 + 15 = 45` | `3+6+9+12+15 = 45` | Matched last two terms of a multi-term sum |
| `10 × 2 = 400` | `20 × 10 × 2 = 400` | Matched last two factors of a multi-factor product |
| `100 + 325 = 225` | `−100 + 325 = 225` | Dropped negative sign on first operand |
| `2/6 = 1` | `2/6 = 1/3` | Stopped at integer before `/3` |
| `8 + 1 = 5` | `−4 + 8 + 1 = 5` | Matched partial sum, missing leading −4 |
| f(b)−f(a) vs F(b)−F(a) | FTC options | Normalized case, treating f and F as equal |

All questions flagged only for these patterns have been reviewed and are correct.

---

## Fix Summary Table

| Q ID | Seed Label | Track/Domain | Current Answer | Correct Answer | Action |
|------|-----------|--------------|----------------|----------------|--------|
| Q612 | P-R2 | algebra_2/polynomials | A (−11) | None | Replace options: add −1, mark it correct |
| Q844 | Integration A-2 | ap_calc_ab/integration | C | Replace with (4√2−2)/3 | Fix option C text |
| Q277 | Limits A-1 | ap_calc_ab/limits_continuity | C | B (k=1) | `correct_answer = 'B'` |
| Q331 | Integration A-1 | ap_calc_ab/integration | B | A | `correct_answer = 'A'` |
| Q350 | IntApps R-1 | ap_calc_ab/integration_apps | D | A | `correct_answer = 'A'` |
| Q713 | DiffAnalytical R-2 | ap_calc_ab/diff_analytical | A | C | `correct_answer = 'C'` |
| Q695 | LE-4 | algebra_1/linear_equations | B | A | `correct_answer = 'A'` |
| Q698 | LE-13 | algebra_1/linear_equations | C | B | `correct_answer = 'B'` |
| Q757 | DS-1 | algebra_1/data_stats | B | C | `correct_answer = 'C'` |
| Q765 | DS-9 | algebra_1/data_stats | B | A | `correct_answer = 'A'` |
| Q818 | CI-12 | geometry/circles | C | B | `correct_answer = 'B'` |
| Q1224 | TrigPolar R-3 | ap_precalc/trig_polar | C | D | `correct_answer = 'D'` |
| Q750 | EX-6 | algebra_1/exponentials | C (correct) | — | Fix duplicate option D |
| Q845 | Functions F-3 | precalculus/functions | A (correct) | — | Fix duplicate option D |
| Q933 | DescStats #7 | statistics/descriptive_stats | A (correct) | — | Fix duplicate option C |
| Q1185 | ExpLog F-6 | ap_precalc/exp_log | C (correct) | — | Fix duplicate option D |
| Q1197 | ExpLog A-6 | ap_precalc/exp_log | C (correct) | — | Fix duplicate option D |
| SY-11 | Systems | algebra_1/systems | B | Rewrite | No exact integer answer |

---

## Verification Script

Saved at `/Users/himanshu/Desktop/H/edison/college-ready/verify_questions.py`.

Run: `cd /Users/himanshu/Desktop/H/edison/college-ready && python3 verify_questions.py`

Re-run after applying fixes to confirm clean results. The script will still produce false positives for the arithmetic-in-explanation checks, but all genuine errors should no longer appear.
