---
type: plan
topic: Foundation Math Night for grades 6-8
date: 2026-03-28
status: draft
version: 1
---

# Foundation Math Night — Build Plan

**Goal:** Launch "Foundation Math Night" for grades 6-8 using the existing College Ready Night platform. Minimize new code by leveraging the existing adaptive MST engine, GRIC mindset quiz, admin portal, and practice plan system. Focus changes on branding, age-appropriate copy, scoring presentation, and archetype packaging.

---

## 1. What Can Be Reused As-Is

### Fully Reusable (zero changes needed)

| Component | Why It Works |
|---|---|
| **Adaptive MST test engine** | `select_module1_questions()` and `select_module2_questions()` already query by track. Grade 6-8 tracks (`grade_6`, `grade_7`, `grade_7_accelerated`, `grade_8`) are fully configured in `TRACK_CONFIG` with correct question counts (24 each), timing (45 min), domain weights, and `grade_proficiency` scoring. |
| **GRIC mindset quiz** | 12 questions, 4-point scale. Language is grade-neutral ("I'm either good at math or I'm not"). One exception — see Section 2. |
| **Admin portal** | Event creation already supports `event_type = 'middle_school'` with auto grade range 6-8. Badges (`badge-ms`) already render. Event list filtering works. |
| **Database schema** | `events` table has `event_type`, `grade_min`, `grade_max`. `students` table has `grade`, `track`. No schema changes needed. |
| **Practice plan engine** | `build_practice_plan()` works off FUAR scores and topic heatmap — grade-agnostic. Daily practice question selection queries by track. |
| **Question banks** | 196 questions across 4 middle school tracks. Grade 6: 48, Grade 7: 48, Grade 7 Accelerated: 52, Grade 8: 48. Each track needs 24 for the test (12 per module), so 48 questions per track gives 2x coverage — enough for adaptive routing. |
| **Scoring engine (grade proficiency)** | `calculate_score_info()` already has a `grade_proficiency` branch that produces level (Advanced/Proficient/Approaching/Developing), algebra readiness indicator for grades 7-8, and predicted grade. This is exactly what middle school needs. |
| **FUAR dimension scoring** | `calculate_fuar_scores()` is track-agnostic — works on any question set. |
| **Email confirmation templates** | `confirmation_parent.html` and `confirmation_student.html` — need minor copy check but structure is reusable. |
| **Weekly assessment system** | Track-agnostic, works with any question bank. |

### Templates Reusable With Minor Conditionals

| Template | Status |
|---|---|
| `event_register.html` | Already has `{% if event_type == 'middle_school' %}` conditionals for title, button text, and email requirement. Works. |
| `event_flyer.html` | Already shows "Family Math Night" for middle school events. Needs update to "Foundation Math Night". |
| `admin.html` | Already has middle school option in dropdown. Works. |
| `test_question.html` | Fully reusable — renders questions from DB, no HS-specific copy. |
| `mindset_quiz.html` | Fully reusable — renders GRIC questions from config. |
| `feedback_widget.html` | Generic. Reusable. |

---

## 2. What Needs to Change for Middle School

### 2A. Branding — "Foundation Math Night"

The name "Foundation Math Night" already appears in several places. "Family Math Night" appears in the flyer template and the app.py docstring. These need to be unified to "Foundation Math Night" throughout.

**Locations where branding appears:**

| File | Line(s) | Current Text | Needed Change |
|---|---|---|---|
| `app.py` line 3 | docstring | "Family Math Night" | Change to "Foundation Math Night" |
| `app.py` line 3150 | event name auto-gen | `'Foundation Math Night'` | Already correct |
| `templates/event_register.html` line 76 | h1 | "Foundation Math Night" | Already correct |
| `templates/event_register.html` line 175 | button | "Register for Foundation Math Night" | Already correct |
| `templates/event_flyer.html` line 88 | event type label | "Family Math Night" | Change to "Foundation Math Night" |
| `templates/admin.html` line 149 | dropdown option | "Foundation Math Night (Grades 6-8)" | Already correct |
| `templates/admin.html` line 203 | JS auto-name | "Foundation Math Night" | Already correct |
| `templates/archetype_reveal.html` line 660 | logo bar | "College Ready Night" (hardcoded) | Add conditional: "Foundation Math Night" when middle school |
| `templates/report.html` line 661 | logo bar | Falls back to "College Ready Night" | Add conditional |
| `templates/report_parent.html` line 411 | footer | "College Ready Night" | Add conditional |
| `templates/base.html` line 6 | page title | "College Ready" | Add conditional: "Foundation Math" for MS events |
| `templates/share_card.html` lines 246-247 | CTA + mark | "collegeready.cuemath.com" / "College Ready" | Add conditional |
| `templates/landing.html` line 675 | hero h1 | "College Ready Night" | Need separate landing or conditional |
| `templates/dashboard.html` line 3 | title | "Dashboard -- College Ready" | Add conditional |

### 2B. Archetypes — Critical Architecture Issue

**Current state:** There are TWO archetype systems that conflict.

1. **High School (8 archetypes):** `ARCHETYPES` dict — Sigma, Delta, Pi, Theta, Phi, Lambda, Alpha, Gamma. These have rich content: `symbol`, `greek_name`, `superpower`, `kryptonite`, `this_is_you` (3 relatable scenarios), `minds` (3 famous thinkers), `signature`, `study_tips` (4 tips), `growth`. Assignment uses `ARCHETYPE_MATRIX` with FUAR dominant x mindset mode (engaged/guarded).

2. **Middle School (16 archetypes):** `MIDDLE_ARCHETYPES` dict — Rapid Strategist, Precision Realist, Speed Enthusiast, Sure Shot, etc. These have minimal content: `name`, `tagline`, `student_desc`, `parent_desc`, `fuar`, `gric`, `colors`, `strength`, `growth`. Assignment uses `MIDDLE_ARCHETYPE_MATRIX` with FUAR x GRIC (16 combos).

**The problem:** The `assign_archetype()` function (line 737) ONLY uses `ARCHETYPE_MATRIX` (the HS 8-type system). It maps FUAR dominant x engaged/guarded, always returning one of the 8 Greek letter archetypes. The `MIDDLE_ARCHETYPE_MATRIX` is defined but NEVER called. This means:

- Middle school students currently get assigned HS archetypes (Sigma, Delta, etc.)
- The archetype reveal template (`archetype_reveal.html`) renders `archetype.greek_name`, `archetype.superpower`, `archetype.kryptonite`, `archetype.this_is_you`, `archetype.minds`, `archetype.signature` — none of which exist on middle school archetypes
- If we switch to using `MIDDLE_ARCHETYPES`, the reveal template will break (missing fields)

**Recommended approach:** Use the same 8 Greek letter archetypes for ALL grades (as the comment on line 161 says: "Same 8 types across all grade bands. Packaging differs by age"). The middle school packaging difference should be handled in templates via conditionals, not via a separate archetype dict. The existing `MIDDLE_ARCHETYPES` (16 types) should be treated as dead code.

**What the HS archetype content needs for middle school:**
- `superpower` text references SAT/AP exams — needs MS alternative
- `kryptonite` text is mostly grade-neutral — minor tweaks
- `growth` text references SAT scores, AP exams — needs MS alternative
- `this_is_you` scenarios reference SAT prep, AP courses, college — needs MS alternatives
- `minds` (famous thinkers) — fully reusable, grade-neutral
- `study_tips` — mostly reusable, some reference SAT/AP prep specifically

**Effort:** Add `ms_superpower`, `ms_kryptonite`, `ms_growth`, `ms_this_is_you`, `ms_study_tips` fields to each of the 8 archetypes in `ARCHETYPES`. Templates use `archetype.ms_superpower if is_middle_school else archetype.superpower`.

### 2C. Scoring Presentation

**Current grade proficiency scoring already works.** The `calculate_score_info()` function for `grade_proficiency` tracks returns:
- Proficiency level: Advanced / Proficient / Approaching / Developing
- Grade-level description: "Solid Grade 7 performance -- on track"
- Algebra readiness indicator (grades 7-8): "Algebra Ready" / "Approaching Algebra Readiness" / "Needs Foundation Work"
- Predicted grade: A/B/C/D

**What's missing for the report/dashboard display:**
- The student report template (`report.html`) has SAT-specific score display (SAT estimate range, percentile). For middle school tracks, it should show:
  - Grade-level proficiency percentage (already calculated)
  - Proficiency level badge (Advanced/Proficient/Approaching/Developing)
  - Algebra readiness indicator (for grades 7-8)
  - "Next course readiness" — what the student is ready for next year
- The dashboard (`dashboard.html`) has an "Estimated SAT Math" widget and "SAT Score Progress" chart. These need middle school alternatives:
  - "Grade-Level Proficiency" widget instead of SAT estimate
  - "Proficiency Progress" chart instead of SAT Score Progress
  - FUAR radar chart works as-is

### 2D. Reports

**Student report (`report.html`):**
- Score display section needs conditional for `grade_proficiency` score type (partially exists but SAT/AP get special treatment)
- FUAR breakdown section is grade-neutral — reusable
- Topic heatmap is grade-neutral — reusable
- Practice plan section is grade-neutral — reusable
- Copy changes: remove "College Ready Night" from logo bar, add event-type conditional

**Parent report (`report_parent.html`):**
- Score section has SAT/AP conditionals — needs `grade_proficiency` branch
- FUAR descriptions use SAT-oriented language for the F dimension ("Speed & Accuracy -- can solve SAT problems quickly") — needs MS alternative
- "Next steps for parents" section (line 389-399) has SAT/AP-specific advice — needs MS branch focused on:
  - Algebra readiness and high school math placement
  - Building strong foundations before high school
  - Course-level appropriateness
- Footer references "College Ready Night" — needs conditional

### 2E. Test Intro / Instructions

`test_intro.html` has minimal HS-specific text (just "College Ready" in the title block). The intro experience needs:
- Different framing for 11-14 year olds: "This isn't a test you can fail" tone, emphasis on discovering strengths
- Shorter time expectation (45 min vs 60-70 min for HS)
- No SAT/AP references

### 2F. Question Bank Assessment

| Track | Questions | Needed (24) | Surplus | FUAR Balance | Gaps |
|---|---|---|---|---|---|
| Grade 6 | 48 | 24 | 24 (2x) | Balanced across F/U/A/R with difficulty 1-5 range | None — good MST range |
| Grade 7 | 48 | 24 | 24 (2x) | Balanced | None |
| Grade 7 Accel | 52 | 24 | 28 (2.2x) | F=15, U=12, A=12, R=13 — slight F skew | Minor — acceptable |
| Grade 8 | 48 | 24 | 24 (2x) | Balanced with difficulty 1-5 range | None |

**Assessment:** 196 questions across 4 tracks is sufficient. Each track has 2x the needed questions, giving the adaptive engine enough room to route between easy/hard Module 2 paths. No new questions needed for launch.

---

## 3. What Needs to Be Built New

### 3A. New Routes

No new routes needed. The existing route structure handles middle school:
- `/register/<code>` — already conditionally renders middle school registration
- `/test/<student_id>` — track-agnostic, works with grade 6-8 tracks
- `/archetype/<student_id>` — needs template conditionals but route works
- `/report/<student_id>` — needs template conditionals but route works
- `/report/parent/<student_id>` — needs template conditionals but route works

**One route fix needed:** The `assign_archetype()` function needs to be aware of grade to pass `is_middle_school` context to templates. Currently it returns an archetype key from the 8 HS archetypes — the route handler should pass `is_middle_school = (grade <= 8)` to templates.

### 3B. Landing Page

The current `landing.html` is fully College Ready branded — SAT tiles, AP course lists, "College Ready Night" hero. Two options:

**Option A (Recommended): Conditional landing page.** Add `{% if is_middle_school %}` blocks throughout `landing.html`. Hero becomes "Foundation Math Night", track tiles show grade-level options, value props change from "SAT score" to "grade-level proficiency."

**Option B: Separate landing template.** `landing_foundation.html` — clean separation but more code to maintain.

Recommendation: Option A. The landing page is mostly structure/CSS; the content differences are in ~10 text blocks.

### 3C. Archetype Reveal Packaging

The current reveal (`archetype_reveal.html`) uses a "dark glam" aesthetic — dark gradients, Greek symbols, animated sparkles, signature quotes. This is aspirational and sophisticated, tuned for high schoolers thinking about college.

**For middle school (ages 11-14):**
- The dark aesthetic can still work — kids this age respond to "premium" feeling, not childish
- Greek symbols/names are actually cool for this age group (Percy Jackson generation)
- The content sections need different copy (see Section 2B) but the visual structure works
- **Keep the same reveal template** with conditional content blocks

**Key change:** The reveal template references `archetype.greek_name`, `archetype.symbol`, `archetype.superpower`, etc. Since we're using the same 8 archetypes with MS-specific fields, the template needs conditionals:

```jinja2
{% if is_middle_school %}
  {{ archetype.ms_superpower }}
{% else %}
  {{ archetype.superpower }}
{% endif %}
```

### 3D. Parent Report for Middle School

The parent report (`report_parent.html`) needs a middle school content branch. Different parent concerns:

| High School Parent Cares About | Middle School Parent Cares About |
|---|---|
| SAT score prediction | Grade-level mastery |
| AP course readiness | Is my child on track? |
| College admission impact | Algebra readiness for high school |
| Test prep recommendations | Course placement guidance |
| Competitive positioning | Foundation strength |

The template structure (score card, FUAR breakdown, topic heatmap, next steps) is reusable. Only the text content within each section changes.

---

## 4. Effort Estimate

### Changes Ordered by Priority

| # | Change | Effort | Approach |
|---|---|---|---|
| 1 | **Fix `assign_archetype()` to pass `is_middle_school` to templates** | Small | Add `grade` parameter check, pass flag to render context |
| 2 | **Add MS-specific archetype content fields** to 8 archetypes in `ARCHETYPES` | Medium | Add `ms_superpower`, `ms_kryptonite`, `ms_growth`, `ms_this_is_you`, `ms_study_tips` to each of the 8 archetype dicts |
| 3 | **Archetype reveal template conditionals** | Small | ~10 `{% if is_middle_school %}` blocks in `archetype_reveal.html` |
| 4 | **Student report conditionals** | Medium | Score display section, copy changes in `report.html` |
| 5 | **Parent report MS branch** | Medium | Score section, FUAR descriptions, next-steps section in `report_parent.html` |
| 6 | **Landing page conditionals** | Medium | Hero, track tiles, value props, process steps in `landing.html` |
| 7 | **Dashboard MS conditionals** | Medium | Replace SAT widget/chart with proficiency widget/chart in `dashboard.html` |
| 8 | **Branding unification** | Small | Fix "Family Math Night" to "Foundation Math Night" in flyer template and docstring; add event-type conditionals to logo bars, titles, footers across ~8 templates |
| 9 | **GRIC question r1 conditional** | Small | "after high school" -> "when you grow up" or "in the future" for MS |
| 10 | **Share card conditionals** | Small | CTA URL and brand mark in `share_card.html` |
| 11 | **Email template check** | Small | Review `confirmation_parent.html` and `confirmation_student.html` for HS-specific language |
| 12 | **Test intro copy** | Small | Add MS-friendly intro framing to `test_intro.html` |

### Approach: Conditionals vs. Branched Templates

**Recommendation: Template conditionals (not branched templates).**

Rationale:
- The visual design/CSS is identical — only text content differs
- Branching would double the template count (26 templates -> 40+) and create a maintenance nightmare
- Jinja2 conditionals are clean: `{% if is_middle_school %}` is easy to read and maintain
- The event_type is already passed to most templates — just need to derive `is_middle_school` from it
- Only 1 template would benefit from branching: `landing.html` (if it diverges significantly). Even then, conditionals are manageable.

**Implementation pattern:**
```python
# In each route handler, add to template context:
is_middle_school = (int(student.get('grade', 9)) <= 8)
```

```jinja2
{# In templates #}
{% set is_ms = is_middle_school | default(false) %}
```

### Total Effort Estimate

- **Small changes (items 1, 3, 8, 9, 10, 11, 12):** ~1 day
- **Medium changes (items 2, 4, 5, 6, 7):** ~2-3 days
- **Testing & polish:** ~1 day
- **Total: 4-5 days of focused work**

---

## 5. Content / Copy Changes Needed

### Every Reference to "College", "SAT", "AP", "High School"

#### In `app.py` (Python code)

| Line | Current Text | Middle School Alternative |
|---|---|---|
| 3 | "Family Math Night" (docstring) | "Foundation Math Night" |
| 133 | GRIC r1: "after high school" | "in the future" or "when you're older" |
| 172 | Sigma superpower: "drop points on the SAT or AP exam" | "rush through a test" |
| 211 | Delta growth: "students who score 1500+ on the SAT" | "students who ace their math class" |
| 240 | Pi growth: "Students who dominate AP exams" | "Students who crush advanced math" |
| 427 | (dead code) Confident Executor: "SAT, AP exam, timed test" | N/A (dead code) |
| 438 | (dead code) "college programs where depth matters" | N/A (dead code) |
| 446 | (dead code) "exactly what colleges look for" | N/A (dead code) |
| 456 | (dead code) "honors and AP mathematics, college majors" | N/A (dead code) |
| 465 | (dead code) "college-level math" | N/A (dead code) |
| 502 | (dead code) "college admissions" | N/A (dead code) |
| 521 | (dead code) "interdisciplinary college programs" | N/A (dead code) |

**Note:** Many archetype references are inside `_DEAD_CODE_START` (the old 16-type system). Only the active 8 archetypes in `ARCHETYPES` (sigma through gamma, lines 164-397) need MS alternatives.

#### MS Archetype Content to Write (8 archetypes x 5 fields)

Each archetype needs these MS-specific fields:

| Archetype | Field | HS Version (summary) | MS Version Needed |
|---|---|---|---|
| **Sigma** (The Precision) | `ms_superpower` | "SAT/AP exam accuracy" | "You almost never make careless mistakes on tests" |
| | `ms_growth` | "highest levels of math" | "As math gets harder in high school, being able to try new approaches will set you apart" |
| | `ms_this_is_you` | References SAT prep, calculator, formulas | Rewrite with grade 6-8 scenarios (homework, class tests, group work) |
| **Delta** (The Relentless) | `ms_superpower` | "Consistency" | Keep — already grade-neutral |
| | `ms_growth` | "score 1500+ on the SAT" | "become the strongest student in any math class" |
| | `ms_this_is_you` | References SAT, study sessions | Rewrite: practice sheets, Khan Academy, extra problems |
| **Pi** (The Purist) | `ms_superpower` | "Depth" | Keep — grade-neutral |
| | `ms_growth` | "dominate AP exams" | "crush every math class through high school" |
| | `ms_this_is_you` | References proofs, textbook | Rewrite: class explanations, why questions, teacher conversations |
| **Theta** (The Quiet Genius) | `ms_superpower` | References "Advanced courses" | "advanced math problems" |
| | `ms_growth` | "college applications" theme | "showing what you know in class and on tests" |
| | `ms_this_is_you` | References study groups, college | Rewrite: classroom, homework, friend explanations |
| **Phi** (The Natural) | `ms_superpower` | "Intuition" | Keep — grade-neutral |
| | `ms_growth` | "college-level proof courses" | "harder math where showing your work matters" |
| | `ms_this_is_you` | References mental math, competitions | Mostly grade-neutral, minor tweaks |
| **Lambda** (The Dormant Force) | `ms_superpower` | "Raw application power" | Keep — mostly grade-neutral |
| | `ms_growth` | "AP exam" references | "high school math" |
| | `ms_this_is_you` | References real-world, projects | Mostly grade-neutral |
| **Alpha** (The First Principle) | `ms_superpower` | "Original thinking" | Keep — grade-neutral |
| | `ms_growth` | References "advanced math" | Keep or minor tweak |
| | `ms_this_is_you` | References AMC, MATHCOUNTS | Keep — MATHCOUNTS is middle school! |
| **Gamma** (The Maverick) | `ms_superpower` | "Rule-breaking problem solving" | Keep — grade-neutral |
| | `ms_growth` | References foundations | Keep — very apt for MS |
| | `ms_this_is_you` | References mental math, partial credit | Mostly grade-neutral |

**Key insight:** Most archetype content is MORE grade-neutral than expected. The main changes are in `superpower` (SAT/AP references), `growth` (college references), and `this_is_you` scenarios. `study_tips` and `minds` are largely reusable.

#### In Templates

| Template | Current Text | MS Alternative |
|---|---|---|
| `archetype_reveal.html` line 660 | "College Ready Night" | `{% if is_ms %}Foundation Math Night{% else %}College Ready Night{% endif %}` |
| `report.html` line 661 | Fallback "College Ready Night" | Same conditional |
| `report_parent.html` line 18 | "can solve SAT problems quickly" | "solves problems quickly and accurately" |
| `report_parent.html` line 23 | `track_exam_name = 'SAT Math'` | Conditional: track display name from config |
| `report_parent.html` line 188 | "SAT Estimate" | "Proficiency" (already handled by score_type conditional) |
| `report_parent.html` line 253 | "of SAT Math skills demonstrated" | "of grade-level skills demonstrated" (already in else branch) |
| `report_parent.html` line 258 | "Not an official SAT score" | "Based on grade-level diagnostic" (already in else branch) |
| `report_parent.html` line 398-399 | "Look into SAT prep" / "Review AP course selection" | "Check if current course is the right level" (already in else branch) |
| `report_parent.html` line 411 | "College Ready Night" | Conditional |
| `landing.html` line 675 | "College Ready Night" | "Foundation Math Night" |
| `landing.html` line 680-703 | SAT/AP track tiles | Grade 6/7/8 track tiles |
| `landing.html` line 795 | "predicted SAT or AP score" | "grade-level proficiency score" |
| `landing.html` line 820 | "SAT, AP Calculus, AP Stats" | "Grade 6, 7, or 8 math" |
| `dashboard.html` line 3 | "Dashboard -- College Ready" | Conditional title |
| `dashboard.html` line 635 | "Estimated SAT Math" | "Grade-Level Proficiency" |
| `dashboard.html` line 816 | "fastest path to a higher SAT" | "fastest path to stronger foundations" |
| `dashboard.html` line 832 | "SAT Score Progress" | "Proficiency Progress" |
| `share_card.html` line 246 | "collegeready.cuemath.com" | "foundationmath.cuemath.com" or generic |
| `share_card.html` line 247 | "College Ready" | "Foundation Math" |
| `base.html` line 6 | "College Ready" | Conditional |
| `practice_results.html` line 250 | "SAT score will follow" | "your skills will keep growing" |
| `register.html` lines 538-577 | SAT/AP track selection | Grade-level track selection (this template may be legacy — `event_register.html` is the active one) |

---

## 6. Summary & Recommended Build Order

### Phase 1: Core Functionality (Day 1-2)
1. Fix `assign_archetype()` to pass `is_middle_school` flag
2. Add MS archetype content fields to the 8 `ARCHETYPES`
3. Add `is_middle_school` to all route handler template contexts
4. Update archetype reveal template with conditionals
5. Update student report template with score-type conditionals
6. Fix "Family Math Night" -> "Foundation Math Night" everywhere

### Phase 2: Reports & Dashboard (Day 2-3)
7. Parent report MS branch (score display, FUAR descriptions, next steps)
8. Dashboard MS conditionals (proficiency widget, progress chart)
9. GRIC question r1 text conditional

### Phase 3: Landing & Polish (Day 3-4)
10. Landing page MS conditionals (hero, track tiles, value props)
11. Share card, base template, email templates — branding conditionals
12. Test intro copy for MS
13. Full end-to-end testing with a middle school demo event

### What NOT to Do
- Do NOT build new templates — use conditionals
- Do NOT use the 16-type `MIDDLE_ARCHETYPES` system — use the 8 Greek letter archetypes with MS content fields
- Do NOT add new question banks — 196 questions is sufficient for launch
- Do NOT create a separate app or database — the current multi-event architecture handles both event types
