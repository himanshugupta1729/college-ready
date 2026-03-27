---
type: plan
topic: College Ready v2 — Complete Build Plan
date: 2026-03-21
status: ready-to-execute
version: 1
---

# College Ready v2 — Build Plan

Based on Himanshu's feedback (March 20-21) + Scout research (March 21).

## Overview of Changes

The product works end-to-end but needs significant upgrades before a real College Ready Night pilot. The changes fall into 6 areas.

---

## 1. ARCHETYPES — Replace 6 with 16 High School Archetypes

**Current:** 6 generic archetypes (Speed Spark, Deep Diver, Problem Solver, Pattern Seeker, Balanced Thinker, Rising Builder) based on FUAR only.

**Target:** 16 archetypes using FUAR × GRIC (4 × 4), from Drucker's locked design in `drucker/2026-02-27-math-nights-complete.md`.

### The 16 Archetypes

| FUAR \ GRIC | Growth | Relevance | Interest | Confidence |
|---|---|---|---|---|
| **Fluency** | Adaptive Analyst | Applied Quant | Quant Explorer | Confident Executor |
| **Understanding** | Conceptual Strategist | Analytical Translator | Theoretical Mind | Foundational Thinker |
| **Application** | Resilient Innovator | Systems Architect | Creative Mathematician | Strategic Leader |
| **Reasoning** | Evolving Logician | Cross-Domain Analyst | Abstract Thinker | Principled Reasoner |

### Code Changes

**In `app.py`:**
- Replace `ARCHETYPES` dict (6 entries) with 16 entries from Drucker's doc
- Each entry needs: name, tagline, student_description, parent_description, signature_colors, fuar_primary, gric_primary
- Replace `assign_archetype()` function:
  - Old: uses only FUAR scores
  - New: uses FUAR scores (dominant dimension) + GRIC scores (dominant dimension) → lookup 4×4 matrix
- Add `GRIC_DIMENSIONS` dict (parallel to `FUAR_DIMENSIONS`)

### Assignment Logic

```python
def assign_archetype(fuar_scores, gric_scores):
    # 1. Find dominant FUAR dimension (highest score)
    fuar_dominant = max(fuar_scores, key=fuar_scores.get)  # F, U, A, or R

    # 2. Find dominant GRIC dimension (highest score)
    gric_dominant = max(gric_scores, key=gric_scores.get)  # G, R, I, or C

    # 3. Lookup in 4×4 matrix
    matrix = {
        ('F', 'G'): 'adaptive_analyst',
        ('F', 'R'): 'applied_quant',
        ('F', 'I'): 'quant_explorer',
        ('F', 'C'): 'confident_executor',
        # ... all 16
    }
    return matrix.get((fuar_dominant, gric_dominant), 'balanced_thinker')
```

---

## 2. GRIC QUESTIONNAIRE — 12 Questions After the Math Test

**What:** After the 60-min math test, students get a "Your Math Mindset" section — 12 questions, ~4 minutes, one question per screen.

### Questions (from validated instruments, reworded for teens)

**Growth (G):**
1. "My math ability is mostly set — I can learn tricks, but my real talent level won't change much." (reverse)
2. "If I work hard at math, I can genuinely get smarter at it — not just memorize more stuff."
3. "Some people are just born 'math people.' Either you are or you aren't." (reverse)

**Relevance (R):**
4. "Math will actually be useful for what I want to do after high school."
5. "I can see how the math I'm learning connects to real things I care about."
6. "Honestly, I'll never use most of this math in real life." (reverse)

**Interest (I):**
7. "I genuinely enjoy working through math problems — it's kind of satisfying."
8. "When I'm doing math, I sometimes lose track of time because I'm into it."
9. "Math is one of the most boring parts of school for me." (reverse)

**Confidence (C):**
10. "When I see a hard math problem, my first thought is 'I can figure this out.'"
11. "I'm confident I can do well in my current math class if I put in the effort."
12. "Math tests make me anxious because I usually feel unprepared." (reverse)

**Scale:** 6-point, no neutral. Labels: "Not me at all" (1) → "This is SO me" (6)

**Reverse items:** Questions 1, 3, 6, 9, 12 are scored in reverse (6 becomes 1, etc.)

### Code Changes

**Database:**
- Add `gric_questions` table (id, dimension, text, is_reverse, display_order)
- Add `gric_responses` table (id, student_id, question_id, score, answered_at)
- Add columns to `students`: gric_growth, gric_relevance, gric_interest, gric_confidence

**Routes:**
- New route: `/test/mindset` — shown after math test completion
- Template: `templates/mindset_quiz.html` — one question per screen, progress bar, swipeable
- After completion: calculate GRIC scores, combine with FUAR → assign archetype

**Flow change:**
```
Register → Math Test (60 min) → "Your Math Mindset" (4 min) → Archetype Reveal
```

---

## 3. SCORING — Track-Specific (Not Everything = SAT)

**Current:** All tracks map to SAT 200-800. Wrong.

**Target:** Each track type has its own scoring system.

| Track Type | Scoring | Output |
|---|---|---|
| SAT Math | Estimated SAT score (200-800) + percentile | "Estimated: 620-680 (75th-85th percentile)" |
| AP tracks (Precalc, Calc AB, Calc BC, Stats) | AP readiness % + predicted AP score (1-5) | "AP Readiness: 72% — Predicted Score: 4" |
| Course tracks (Algebra 1, Geometry, etc.) | Proficiency level + grade-level positioning | "Proficient — performing at/above grade level" |

### Normalization Approach

For SAT estimation from a 60-min test (vs 3.5 hours):
- We test ~44 questions vs SAT's 54
- Our adaptive routing (MST) gives us better signal per question than linear testing
- Estimate a RANGE, not a point score (±40 points)
- Disclose: "This is an estimate based on a 60-minute diagnostic. Take a full practice SAT for a precise score."

### Code Changes

- Replace `estimate_sat_score()` with `estimate_score(track, fuar_scores, responses)`
- Track-specific scoring functions: `_score_sat()`, `_score_ap()`, `_score_course()`
- AP scoring: map overall accuracy + dimension balance to 1-5 scale
- Course scoring: map to Below/Approaching/Proficient/Advanced

---

## 4. DAILY PRACTICE — Redesign

**Current:** 8 questions/day, 10 min, 7 days/week
**Target:** 10-12 questions/day, 15 min, 5 days/week with streak system

### Key Design Decisions (from Scout research)

- **5-day streaks with 2 built-in rest days** — call them "rest days" not "freeze days"
- **Streak ramp-down, not hard reset** — if they miss 3+ days, streak pauses, doesn't die
- **Show "total days practiced" alongside streak** — even after break, progress isn't lost
- **Archetype evolution as progression** — "You started as Speed Spark. Your Application improved 23%. You're evolving toward Applied Quant."
- **Weekly mini-reassessment** — 5 questions, 3 min, updates the FUAR radar
- **No childish gamification** — Whoop/Strava aesthetic, not Kahoot/Prodigy
- **4-week plan, then reassess** — not infinite loop

### Code Changes

- Update `daily_workouts` table: add `week_day` (Mon-Fri only), `rest_day` boolean
- Add streak freeze logic: 2 free per week, earn more through consistency
- Update `generate_daily_workout()`: 10-12 questions, 15 min target
- Add streak recovery: pause after 3 missed days, show total days practiced
- New template: `templates/streak_dashboard.html` — Whoop-style data visualization

---

## 5. REGISTRATION — Luma + Event-Driven

**Current:** Self-registration on the portal.
**Target:** Students register on Luma (external). On event day, admin enables the test.

### Flow

```
Pre-event: Student registers on Luma (name, email, grade, track)
Event day: Admin imports Luma registrations → creates student accounts
           Admin enables test at a specific time
           Students log in with email + event code
           Test begins for everyone simultaneously
Post-event: Reports generated, emailed to student + parent
```

### Code Changes

- Add `/admin/import-luma` route — CSV upload of Luma registrations
- Add `test_enabled` field to `events` table (boolean + timestamp)
- Add `/admin/enable-test/<event_code>` — toggle test availability
- Student login: email + event code (not self-registration)
- Remove or hide public registration page during events

---

## 6. NAMING & BRANDING

**Current:** App title says "College Ready — SAT Math Diagnostic + FUAR Profile"
**Target:** "College Ready" as the product name throughout.

### Changes
- Landing page: "College Ready" prominently
- Test intro: "College Ready — Find out where you really stand"
- Results: "Your College Ready Profile"
- Remove "MathFit" references if any exist
- Event codes: these are codes like "LINCOLN-HIGH-2026" that tie students to a specific College Ready Night event

---

## 7. REPORTS (Research Done, Design Pending)

**Not building yet** — but the design direction is locked from Scout research:

### Student Report (web-based, interactive)
- FUAR radar chart (hero visualization) with target overlay
- Archetype reveal with personality description
- Pacing gap analysis (Phase 1 vs Phase 2 performance)
- Stamina curve (accuracy by test thirds)
- Topic heatmap (content area strengths/weaknesses)
- Speed vs accuracy quadrant
- 4-week practice plan preview
- Tone: empathetic, empowering, growth-oriented

### Parent Report (PDF, 3 pages)
- Page 1: The headline — SAT/AP estimate, percentile, archetype
- Page 2: What it means — FUAR gaps connected to college outcomes
- Page 3: What to do — 4-week plan, Cuemath offering
- Appendix: full student report attached

### Design: Vignelli will handle visual design when ready.
### Content: Claude API will generate personalized narrative sections.

---

## Build Sequence (Priority Order)

| Priority | What | Est. Effort | Dependencies |
|---|---|---|---|
| P0 | GRIC questionnaire (12 questions + scoring) | 2 hours | None |
| P0 | 16 archetypes (replace 6) + new assignment logic | 1.5 hours | GRIC scoring |
| P0 | Track-specific scoring (SAT/AP/Course) | 1.5 hours | None |
| P1 | Naming/branding updates | 30 min | None |
| P1 | Luma import + event-driven registration | 1.5 hours | None |
| P1 | Daily practice redesign (streaks, 5-day, 15 min) | 2 hours | None |
| P2 | Report generation (student + parent) | 4+ hours | Vignelli design, Claude API |
| P2 | Mobile-responsive templates | 2 hours | None |

**Total P0+P1: ~9 hours of building**

---

## Files That Change

| File | Changes |
|---|---|
| `app.py` | Archetypes (16), GRIC scoring, assignment logic, track-specific scoring, Luma import, event controls, daily practice redesign, naming |
| `templates/test_question.html` | No change (math test stays the same) |
| `templates/mindset_quiz.html` | **NEW** — GRIC questionnaire, one-per-screen |
| `templates/archetype_reveal.html` | Update for 16 archetypes + GRIC profile |
| `templates/dashboard.html` | Update for streak redesign, FUAR+GRIC display |
| `templates/landing.html` | Rename to "College Ready" |
| `templates/admin.html` | Add Luma import, event enable/disable |
| `templates/daily_practice.html` | Update for 10-12 questions, streak visualization |

---

## What's NOT in This Build

- Report generation (needs Vignelli design first)
- Deployment to Render (after testing locally)
- Question bank validation with Rigved (separate workstream)
- AI Counselor (future build)
- Big Five personality integration (embedded in GRIC questions implicitly — no separate measurement needed)
