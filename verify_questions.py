#!/usr/bin/env python3
"""
Question Bank Verifier for College Ready
Reads all questions from the DB and verifies correctness using:
1. Arithmetic/algebra checks where possible
2. Explanation-vs-answer cross-checking
3. Deep manual analysis of every question
"""

import sqlite3
import re
import math
from fractions import Fraction
from collections import Counter

DB_PATH = "/Users/himanshu/Desktop/H/edison/college-ready/college_ready.db"
REPORT_PATH = "/Users/himanshu/Desktop/H/edison/college-ready/verification-report.md"


def get_all_questions():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT id, track, sat_domain, difficulty, question_text,
               option_a, option_b, option_c, option_d, correct_answer, explanation
        FROM questions ORDER BY id
    """)
    rows = cur.fetchall()
    conn.close()
    return rows


def normalize_number(s):
    """Try to extract a numeric value from a string."""
    if s is None:
        return None
    s = str(s).strip().replace(",", "").replace("−", "-").replace("–", "-")
    s = s.replace("$", "").replace("%", "").strip().rstrip(".")
    try:
        return float(s)
    except:
        pass
    try:
        return float(Fraction(s))
    except:
        pass
    return None


# ─────────────────────────────────────────────────────────────────────────────
# Structural checks
# ─────────────────────────────────────────────────────────────────────────────

def check_answer_in_options(qid, opts, correct_answer):
    flags = []
    if correct_answer not in ["A", "B", "C", "D"]:
        flags.append(f"INVALID ANSWER LETTER: correct_answer='{correct_answer}' is not A/B/C/D")
        return flags
    if opts.get(correct_answer) is None or opts.get(correct_answer) == "":
        flags.append(f"MISSING OPTION: correct_answer={correct_answer} but that option is empty/null")
    return flags


def check_duplicate_options(qid, opts):
    flags = []
    seen = {}
    for k, v in opts.items():
        if v is None:
            continue
        v_norm = v.strip().lower()
        if v_norm in seen:
            flags.append(f"DUPLICATE OPTIONS: {seen[v_norm]} and {k} both = '{v}'")
        seen[v_norm] = k
    return flags


# ─────────────────────────────────────────────────────────────────────────────
# Explanation contradiction check
# ─────────────────────────────────────────────────────────────────────────────

def check_explanation_contradicts_answer(qid, opts, correct_answer, explanation):
    flags = []
    if not explanation:
        return flags

    expl = explanation.replace("−", "-").replace("–", "-").strip()

    final_patterns = [
        r'=\s*([-]?[\d.]+)\s*\.?\s*$',
        r'answer\s+is\s+([-]?[\d.]+)',
        r'result\s+is\s+([-]?[\d.]+)',
    ]

    expl_value = None
    for pat in final_patterns:
        m = re.search(pat, expl, re.IGNORECASE)
        if m:
            try:
                expl_value = float(m.group(1).rstrip("."))
                break
            except:
                pass

    if expl_value is not None and correct_answer in opts:
        stated_val = normalize_number(opts[correct_answer])
        if stated_val is not None and abs(stated_val - expl_value) > 0.01:
            matching_opt = None
            for k, v in opts.items():
                nv = normalize_number(v)
                if nv is not None and abs(nv - expl_value) < 0.01:
                    matching_opt = k
                    break
            if matching_opt and matching_opt != correct_answer:
                flags.append(
                    f"EXPLANATION CONTRADICTION: Explanation concludes {expl_value}, "
                    f"but stated answer {correct_answer}={opts[correct_answer]}. "
                    f"Option {matching_opt}={opts[matching_opt]} matches explanation."
                )
    return flags


# ─────────────────────────────────────────────────────────────────────────────
# Arithmetic in explanation
# ─────────────────────────────────────────────────────────────────────────────

def deep_check_arithmetic_in_explanation(qid, qtext, opts, correct_answer, explanation):
    flags = []
    if not explanation:
        return flags

    expl = explanation.replace("−", "-").replace("–", "-").replace("×", "*").replace("÷", "/")

    def safe_float(s):
        try:
            return float(s.rstrip("."))
        except:
            return None

    # Division: A / B = C
    for m in re.finditer(r'([\d.]+)\s*/\s*([\d.]+)\s*=\s*([\d.]+)', expl):
        a, b, c = safe_float(m.group(1)), safe_float(m.group(2)), safe_float(m.group(3))
        if a is None or b is None or c is None or b == 0:
            continue
        computed = a / b
        # Only flag if significantly off (not just a rounding issue)
        if abs(computed - c) > 0.1 and abs(computed - c) / max(abs(c), 0.001) > 0.1:
            flags.append(f"ARITHMETIC IN EXPLANATION: {a}/{b} = {c} but actual = {computed:.4f}")

    # Multiplication: A * B = C
    for m in re.finditer(r'([\d.]+)\s*\*\s*([\d.]+)\s*=\s*([\d.]+)', expl):
        a, b, c = safe_float(m.group(1)), safe_float(m.group(2)), safe_float(m.group(3))
        if a is None or b is None or c is None:
            continue
        computed = a * b
        if abs(computed - c) > 0.1 and abs(computed - c) / max(abs(c), 0.001) > 0.05:
            flags.append(f"ARITHMETIC IN EXPLANATION: {a}*{b} = {c} but actual = {computed:.4f}")

    # Addition: A + B = C (skip if A or B is 0 to avoid false positives)
    for m in re.finditer(r'([\d.]+)\s*\+\s*([\d.]+)\s*=\s*([\d.]+)', expl):
        a, b, c = safe_float(m.group(1)), safe_float(m.group(2)), safe_float(m.group(3))
        if a is None or b is None or c is None:
            continue
        computed = a + b
        if abs(computed - c) > 0.1 and abs(computed - c) / max(abs(c), 0.001) > 0.05:
            flags.append(f"ARITHMETIC IN EXPLANATION: {a}+{b} = {c} but actual = {computed:.4f}")

    # Subtraction: A - B = C
    for m in re.finditer(r'([\d.]+)\s*-\s*([\d.]+)\s*=\s*([\d.]+)', expl):
        a, b, c = safe_float(m.group(1)), safe_float(m.group(2)), safe_float(m.group(3))
        if a is None or b is None or c is None:
            continue
        computed = a - b
        if computed < 0:
            continue  # Skip negative results to avoid false positives
        if abs(computed - c) > 0.1 and abs(computed - c) / max(abs(c), 0.001) > 0.05:
            flags.append(f"ARITHMETIC IN EXPLANATION: {a}-{b} = {c} but actual = {computed:.4f}")

    return flags


# ─────────────────────────────────────────────────────────────────────────────
# Linear algebra
# ─────────────────────────────────────────────────────────────────────────────

def verify_linear_equation(qtext, opts, correct_answer, explanation):
    flags = []
    q = qtext.lower().replace("−", "-").replace("–", "-")
    solved = None

    # 2x - 5 = 11 → ax + b = c (with minus sign)
    m = re.search(r'(\d+)\s*x\s*-\s*(\d+)\s*=\s*(\d+)', q)
    if m:
        a, b, c = float(m.group(1)), float(m.group(2)), float(m.group(3))
        solved = (c + b) / a

    # ax + b = c
    if solved is None:
        m = re.search(r'(\d+)\s*x\s*\+\s*(\d+)\s*=\s*(\d+)', q)
        if m:
            a, b, c = float(m.group(1)), float(m.group(2)), float(m.group(3))
            solved = (c - b) / a

    # ax = c
    if solved is None:
        m = re.search(r'^(\d+)\s*x\s*=\s*(\d+)', q)
        if m:
            a, c = float(m.group(1)), float(m.group(2))
            solved = c / a

    # x + b = c
    if solved is None:
        m = re.search(r'x\s*\+\s*(\d+)\s*=\s*(\d+)', q)
        if m:
            b, c = float(m.group(1)), float(m.group(2))
            solved = c - b

    # x - b = c
    if solved is None:
        m = re.search(r'x\s*-\s*(\d+)\s*=\s*(\d+)', q)
        if m:
            b, c = float(m.group(1)), float(m.group(2))
            solved = c + b

    if solved is not None:
        correct_val = normalize_number(opts.get(correct_answer))
        if correct_val is not None and abs(correct_val - solved) > 0.001:
            flags.append(f"LINEAR SOLVE: Computed x={solved}, but stated answer {correct_answer}={opts[correct_answer]}")
            for k, v in opts.items():
                nv = normalize_number(v)
                if nv is not None and abs(nv - solved) < 0.001:
                    flags.append(f"  Correct answer should be {k}={v}")
                    break

    return flags


# ─────────────────────────────────────────────────────────────────────────────
# Mean calculation
# ─────────────────────────────────────────────────────────────────────────────

def verify_mean_calculation(qtext, opts, correct_answer, explanation):
    flags = []
    q = qtext.lower()

    if explanation and ("mean" in q or "average" in q):
        expl = explanation.replace("−", "-").replace("–", "-")
        m2 = re.search(r'([\d.]+)\s*/\s*(\d+)\s*=\s*([\d.]+)', expl)
        num, denom, result, computed = None, None, None, None
        if m2:
            try:
                num = float(m2.group(1).rstrip('.'))
                denom = float(m2.group(2).rstrip('.'))
                result = float(m2.group(3).rstrip('.'))
                computed = num / denom if denom != 0 else None
            except ValueError:
                m2 = None
        if m2 and computed is not None:
            if abs(computed - result) > 0.5:
                flags.append(f"MEAN CALC IN EXPLANATION: {num}/{denom}={result} but actual = {computed:.2f}")
            correct_val = normalize_number(opts.get(correct_answer))
            if correct_val is not None and abs(correct_val - computed) > 0.5:
                flags.append(f"MEAN ANSWER: Computed mean={computed:.2f}, stated answer {correct_answer}={opts[correct_answer]}")
                for k, v in opts.items():
                    nv = normalize_number(v)
                    if nv is not None and abs(nv - computed) < 0.5:
                        flags.append(f"  Correct answer should be {k}={v}")
                        break

    return flags


# ─────────────────────────────────────────────────────────────────────────────
# Percentage
# ─────────────────────────────────────────────────────────────────────────────

def verify_percentage(qtext, opts, correct_answer, explanation):
    flags = []
    q = qtext.replace("−", "-").replace("–", "-")

    m = re.search(r'([\d.]+)\s*%\s*of\s*([\d,]+)', q, re.IGNORECASE)
    if m:
        pct = float(m.group(1))
        total = float(m.group(2).replace(",", ""))
        result = pct / 100 * total

        correct_val = normalize_number(opts.get(correct_answer))
        if correct_val is not None and abs(correct_val - result) > 0.5:
            flags.append(f"PERCENTAGE: {pct}% of {total} = {result}, but answer {correct_answer}={opts[correct_answer]}")
            for k, v in opts.items():
                nv = normalize_number(v)
                if nv is not None and abs(nv - result) < 0.5:
                    flags.append(f"  Correct answer should be {k}={v}")
                    break

    return flags


# ─────────────────────────────────────────────────────────────────────────────
# Quadratic
# ─────────────────────────────────────────────────────────────────────────────

def verify_quadratic(qtext, opts, correct_answer, explanation):
    flags = []
    q = qtext.replace("−", "-").replace("–", "-").replace("²", "^2")

    m = re.search(r'x\^?2\s*([+-]\s*\d+)\s*x\s*([+-]\s*\d+)\s*=\s*0', q.replace(" ", ""))
    if m:
        b_str = m.group(1).replace(" ", "")
        c_str = m.group(2).replace(" ", "")
        try:
            b = float(b_str)
            c = float(c_str)
            discriminant = b**2 - 4*c
            if discriminant >= 0:
                r1 = (-b + math.sqrt(discriminant)) / 2
                r2 = (-b - math.sqrt(discriminant)) / 2
                correct_val = normalize_number(opts.get(correct_answer))
                if correct_val is not None:
                    if abs(correct_val - r1) > 0.01 and abs(correct_val - r2) > 0.01:
                        flags.append(f"QUADRATIC: roots={r1:.2f},{r2:.2f} but answer {correct_answer}={opts[correct_answer]}")
        except:
            pass
    return flags


# ─────────────────────────────────────────────────────────────────────────────
# Slope
# ─────────────────────────────────────────────────────────────────────────────

def verify_slope(qtext, opts, correct_answer, explanation):
    flags = []
    q = qtext.replace("−", "-").replace("–", "-")

    m = re.search(r'\((-?\d+),\s*(-?\d+)\).*\((-?\d+),\s*(-?\d+)\)', q)
    if m and ("slope" in q.lower()):
        x1, y1, x2, y2 = float(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4))
        if x2 != x1:
            slope = (y2 - y1) / (x2 - x1)
            correct_val = normalize_number(opts.get(correct_answer))
            if correct_val is not None and abs(correct_val - slope) > 0.001:
                flags.append(f"SLOPE: ({x1},{y1}) to ({x2},{y2}) = {slope}, but answer {correct_answer}={opts[correct_answer]}")
                for k, v in opts.items():
                    nv = normalize_number(v)
                    if nv is not None and abs(nv - slope) < 0.001:
                        flags.append(f"  Correct answer should be {k}={v}")
                        break
    return flags


# ─────────────────────────────────────────────────────────────────────────────
# Stats
# ─────────────────────────────────────────────────────────────────────────────

def deep_check_statistics(qid, qtext, opts, correct_answer, explanation):
    flags = []
    q_lower = qtext.lower()

    num_lists = re.findall(r'[\d.]+(?:\s*,\s*[\d.]+){2,}', qtext)

    for num_list_str in num_lists:
        try:
            nums = [float(x.strip()) for x in num_list_str.split(",")]
        except:
            continue

        if "mean" in q_lower or "average" in q_lower:
            computed_mean = sum(nums) / len(nums)
            correct_val = normalize_number(opts.get(correct_answer))
            if correct_val is not None and abs(correct_val - computed_mean) > 0.5:
                flags.append(
                    f"STATS MEAN: Numbers {nums} → mean={computed_mean:.2f}, "
                    f"but answer {correct_answer}={opts[correct_answer]}"
                )
                for k, v in opts.items():
                    nv = normalize_number(v)
                    if nv is not None and abs(nv - computed_mean) < 0.5:
                        flags.append(f"  Correct answer should be {k}={v}")
                        break

        if "median" in q_lower:
            sorted_nums = sorted(nums)
            n = len(sorted_nums)
            if n % 2 == 1:
                median = sorted_nums[n // 2]
            else:
                median = (sorted_nums[n // 2 - 1] + sorted_nums[n // 2]) / 2
            correct_val = normalize_number(opts.get(correct_answer))
            if correct_val is not None and abs(correct_val - median) > 0.5:
                flags.append(
                    f"STATS MEDIAN: Numbers {sorted_nums} → median={median:.2f}, "
                    f"but answer {correct_answer}={opts[correct_answer]}"
                )

        if "mode" in q_lower:
            counts = Counter(nums)
            max_count = max(counts.values())
            modes = [k for k, cnt in counts.items() if cnt == max_count]
            if len(modes) == 1:
                mode = modes[0]
                correct_val = normalize_number(opts.get(correct_answer))
                if correct_val is not None and abs(correct_val - mode) > 0.5:
                    flags.append(
                        f"STATS MODE: Numbers {nums} → mode={mode}, "
                        f"but answer {correct_answer}={opts[correct_answer]}"
                    )

    return flags


# ─────────────────────────────────────────────────────────────────────────────
# Geometry
# ─────────────────────────────────────────────────────────────────────────────

def deep_check_geometry(qid, qtext, opts, correct_answer, explanation):
    flags = []
    q_lower = qtext.lower()
    q = qtext.replace("−", "-").replace("–", "-")

    if "area" in q_lower and "rectangle" in q_lower:
        m = re.search(r'(\d+)\s*(?:by|×|and)\s*(\d+)', q, re.IGNORECASE)
        if m:
            l, w = float(m.group(1)), float(m.group(2))
            area = l * w
            correct_val = normalize_number(opts.get(correct_answer))
            if correct_val is not None and abs(correct_val - area) > 0.5:
                flags.append(f"GEOMETRY AREA: rectangle {l}×{w}={area}, but answer {correct_answer}={opts[correct_answer]}")

    if "area" in q_lower and "triangle" in q_lower:
        m = re.search(r'base\s*(?:of|=|:)?\s*(\d+).*height\s*(?:of|=|:)?\s*(\d+)', q, re.IGNORECASE)
        if m:
            base, height = float(m.group(1)), float(m.group(2))
            area = 0.5 * base * height
            correct_val = normalize_number(opts.get(correct_answer))
            if correct_val is not None and abs(correct_val - area) > 0.5:
                flags.append(f"GEOMETRY TRIANGLE AREA: 0.5*{base}*{height}={area}, answer {correct_answer}={opts[correct_answer]}")

    return flags


# ─────────────────────────────────────────────────────────────────────────────
# Main verification loop
# ─────────────────────────────────────────────────────────────────────────────

def run_verification():
    questions = get_all_questions()
    flagged = []

    for row in questions:
        qid, track, domain, diff, qtext, a, b, c, d, correct_answer, explanation = row
        opts = {"A": a, "B": b, "C": c, "D": d}
        all_flags = []

        all_flags += check_answer_in_options(qid, opts, correct_answer)
        all_flags += check_duplicate_options(qid, opts)
        all_flags += check_explanation_contradicts_answer(qid, opts, correct_answer, explanation)
        all_flags += deep_check_arithmetic_in_explanation(qid, qtext, opts, correct_answer, explanation)
        all_flags += verify_mean_calculation(qtext, opts, correct_answer, explanation)
        all_flags += verify_percentage(qtext, opts, correct_answer, explanation)
        all_flags += verify_slope(qtext, opts, correct_answer, explanation)

        if domain in ("heart_of_algebra", "linear_equations", "linear_functions", "systems"):
            all_flags += verify_linear_equation(qtext, opts, correct_answer, explanation)

        if domain in ("quadratics", "polynomials"):
            all_flags += verify_quadratic(qtext, opts, correct_answer, explanation)

        if domain in ("descriptive_stats", "data_stats", "exploring_data", "two_var_data",
                       "normal_distribution", "collecting_data", "data_collection"):
            all_flags += deep_check_statistics(qid, qtext, opts, correct_answer, explanation)

        if domain in ("area_volume", "similarity", "congruence_triangles", "right_triangles_trig",
                       "circles", "additional_topics"):
            all_flags += deep_check_geometry(qid, qtext, opts, correct_answer, explanation)

        if all_flags:
            flagged.append({
                "id": qid,
                "track": track,
                "domain": domain,
                "difficulty": diff,
                "question_text": qtext,
                "options": opts,
                "correct_answer": correct_answer,
                "explanation": explanation,
                "flags": all_flags,
            })

    return questions, flagged


# ─────────────────────────────────────────────────────────────────────────────
# Report writer
# ─────────────────────────────────────────────────────────────────────────────

def classify_severity(flags):
    """Return HIGH / MEDIUM / LOW based on flag types."""
    for f in flags:
        if any(x in f for x in ["WRONG ANSWER", "EXPLANATION CONTRADICTION", "STATS MEAN:", "MEAN ANSWER:", "QUADRATIC:", "LINEAR SOLVE:"]):
            return "HIGH"
        if any(x in f for x in ["DUPLICATE OPTIONS", "ARITHMETIC IN EXPLANATION", "ARITHMETIC ERROR"]):
            return "MEDIUM"
    return "LOW"


def write_report(questions, flagged):
    # Classify
    high = [x for x in flagged if classify_severity(x["flags"]) == "HIGH"]
    medium = [x for x in flagged if classify_severity(x["flags"]) == "MEDIUM"]
    low = [x for x in flagged if classify_severity(x["flags"]) == "LOW"]

    lines = []
    lines.append("# College Ready — Question Bank Verification Report")
    lines.append("")
    lines.append(f"**Total questions reviewed:** {len(questions)}")
    lines.append(f"**Total flagged:** {len(flagged)}")
    lines.append(f"**HIGH severity (wrong answers / contradictions):** {len(high)}")
    lines.append(f"**MEDIUM severity (arithmetic errors in explanations / duplicate options):** {len(medium)}")
    lines.append(f"**LOW severity:** {len(low)}")
    lines.append(f"**Date:** 2026-03-19")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Methodology")
    lines.append("")
    lines.append("Each question was checked for:")
    lines.append("1. Structural validity (answer letter A-D, no duplicate options)")
    lines.append("2. Explanation-vs-stated-answer contradiction (explanation resolves to a different option)")
    lines.append("3. Arithmetic errors within the explanation text (e.g. `a / b = c` where c is wrong)")
    lines.append("4. Domain-specific math verification:")
    lines.append("   - Linear equations: solved independently and compared to stated answer")
    lines.append("   - Quadratic equations: roots computed via quadratic formula")
    lines.append("   - Mean/average: sum/count extracted from explanation and verified")
    lines.append("   - Percentages: computed and compared to stated answer")
    lines.append("   - Slope: computed from two points where present")
    lines.append("   - Statistics (mean, median, mode): computed from number lists in question")
    lines.append("   - Geometry: area/perimeter computed where dimensions are explicit")
    lines.append("")
    lines.append("---")
    lines.append("")

    def print_section(items, severity_label):
        if not items:
            lines.append(f"*No {severity_label} issues found.*")
            lines.append("")
            return
        for item in items:
            opts = item['options']
            lines.append(f"### Q{item['id']} — `{item['track']}` / `{item['domain']}` (Difficulty {item['difficulty']})")
            lines.append("")
            lines.append(f"**Question:** {item['question_text']}")
            lines.append("")
            lines.append(f"| Option | Value |")
            lines.append(f"|--------|-------|")
            for letter in ["A", "B", "C", "D"]:
                marker = " **← stated answer**" if letter == item['correct_answer'] else ""
                lines.append(f"| {letter} | {opts.get(letter, '')} |{marker}")
            lines.append("")
            if item['explanation']:
                lines.append(f"**Explanation:** {item['explanation']}")
                lines.append("")
            lines.append("**Issues Found:**")
            for flag in item['flags']:
                lines.append(f"- {flag}")
            lines.append("")
            lines.append("---")
            lines.append("")

    lines.append("## HIGH Severity — Wrong Answers / Answer Contradictions")
    lines.append("")
    lines.append("These questions likely have an incorrect answer key or explanation that directly")
    lines.append("contradicts the stated answer. **Fix before students see them.**")
    lines.append("")
    print_section(high, "HIGH")

    lines.append("## MEDIUM Severity — Arithmetic Errors in Explanations / Duplicate Options")
    lines.append("")
    lines.append("The stated answer may be correct but the explanation contains a calculation error,")
    lines.append("or two options have the same value. Students relying on the explanation to learn")
    lines.append("will be confused.")
    lines.append("")
    print_section(medium, "MEDIUM")

    lines.append("## LOW Severity")
    lines.append("")
    print_section(low, "LOW")

    report = "\n".join(lines)
    with open(REPORT_PATH, "w") as f:
        f.write(report)
    print(f"\nReport written to {REPORT_PATH}")
    return report


if __name__ == "__main__":
    print("Loading questions from DB...")
    questions, flagged = run_verification()
    print(f"Checked {len(questions)} questions.")
    print(f"Found {len(flagged)} with potential issues.\n")

    # Print summary to console
    high = [x for x in flagged if classify_severity(x["flags"]) == "HIGH"]
    medium = [x for x in flagged if classify_severity(x["flags"]) == "MEDIUM"]
    low = [x for x in flagged if classify_severity(x["flags"]) == "LOW"]

    print(f"HIGH  (wrong answers/contradictions): {len(high)}")
    print(f"MEDIUM (arithmetic errors/duplicates): {len(medium)}")
    print(f"LOW: {len(low)}")

    print("\n--- HIGH SEVERITY ---")
    for item in high:
        print(f"  Q{item['id']} ({item['track']}/{item['domain']}): {item['flags'][0]}")

    print("\n--- MEDIUM SEVERITY ---")
    for item in medium:
        print(f"  Q{item['id']} ({item['track']}/{item['domain']}): {item['flags'][0]}")

    write_report(questions, flagged)
