---
type: brief
topic: College Ready + Foundation Math Night — Product Overview
date: 2026-03-28
status: review
version: 1
---

# College Ready Night + Foundation Math Night — Product Overview

**For:** Manan, Rigved, Joita, and team
**From:** Himanshu
**Date:** March 28, 2026

---

## 1. What We've Built

Two branded products running on a single platform:

- **College Ready Night** — for grades 9-12. Adaptive math diagnostic tied to SAT, AP, and course-level tracks. Students get an archetype identity, a full FUAR report, and a personalized daily practice plan.
- **Foundation Math Night** — for grades 6-8. Same adaptive engine, same archetype system, same practice plan infrastructure. Different packaging: grade-level proficiency instead of SAT scores, age-appropriate copy, and middle school tracks (Grade 6, 7, 7 Accelerated, 8).

The end-to-end flow covers everything from the event landing page to daily practice with worked solutions. Same codebase, same database, same admin portal. The platform determines which experience to serve based on the event type and student grade.

This is not a quiz. It is a diagnostic engine that produces a math identity — something students want to share, parents want to understand, and we can use to drive engagement.

---

## 2. The Thinking Behind It

### FUAR Framework

FUAR is Cuemath's proprietary framework for decomposing mathematical ability into four measurable dimensions:

| Dimension | What It Measures | Why It Matters |
|---|---|---|
| **F — Fluency** | Speed and accuracy on practiced procedures | Can the student execute reliably under time pressure? |
| **U — Understanding** | Conceptual depth, transfer to new contexts | Does the student know WHY, not just HOW? |
| **A — Application** | Translating real-world problems into math | Can they model messy situations mathematically? |
| **R — Reasoning** | Logical deduction, proof, novel problem-solving | Can they solve things nobody has taught them? |

Every question in the bank is tagged to exactly one FUAR dimension plus a difficulty level (1-5). This allows per-dimension scoring, not just an aggregate number. A student who scores high on Reasoning but low on Fluency has a completely different profile — and needs a completely different practice plan — than the reverse.

### GRIC Mindset Assessment

After the diagnostic, students take a 12-question mindset quiz measuring four dimensions:

| Dimension | What It Captures |
|---|---|
| **G — Growth** | "I can get better at math through effort" vs. fixed mindset |
| **R — Relevance** | "Math matters for my future" vs. disconnection |
| **I — Interest** | Intrinsic curiosity about math |
| **C — Confidence** | Self-belief when facing hard problems |

GRIC is scored on a 4-point scale per question. The dominant dimensions determine the student's **mindset mode**:
- **Engaged** (Growth or Interest dominant) — the student is intrinsically motivated
- **Guarded** (Relevance or Confidence dominant) — the student's motivation is extrinsic or protective

### 8 Archetypes: Where FUAR Meets Mindset

The FUAR dominant dimension (which of F/U/A/R is highest) crossed with the mindset mode (engaged/guarded) produces one of 8 archetypes. This is the core identity output — the thing students screenshot, share, and remember.

The archetype matrix:

| | Engaged | Guarded |
|---|---|---|
| **Fluency dominant** | Sigma — The Perfectionist | Delta — The Relentless |
| **Understanding dominant** | Pi — The Purist | Theta — The Quiet Genius |
| **Application dominant** | Phi — The Natural | Lambda — The Dormant Force |
| **Reasoning dominant** | Alpha — The Inventor | Gamma — The Maverick |

Why archetypes matter:
1. **Identity drives engagement.** "You're a Theta" is stickier than "You scored 72%." Students internalize it, talk about it, compare with friends.
2. **Shareability.** A share card with a Greek symbol, a tagline, and a mathematician pairing is designed to be posted. Every share is organic reach.
3. **Parent understanding.** Instead of a score that means nothing to a non-math parent, archetypes give them a framework: "Your child sees math deeply but doesn't trust it under pressure — here's what to do."
4. **Targeted practice.** Each archetype maps to a specific growth area, so the practice plan isn't generic — it's built around the student's identity.

### Adaptive MST (Multi-Stage Testing)

The diagnostic uses a two-module adaptive structure:

- **Module 1:** 12 questions, balanced across FUAR dimensions and difficulties
- **Scoring gate:** Module 1 performance routes the student to one of two Module 2 paths
- **Module 2 (Easy):** 12 questions skewed toward difficulty 1-3, more Fluency/Application
- **Module 2 (Hard):** 12 questions skewed toward difficulty 3-5, more Reasoning/Understanding

This adaptive routing means a Grade 7 student who aces Module 1 faces harder questions in Module 2, producing a more accurate profile. A student who struggles gets a fair assessment that doesn't demoralize them.

Total: 24 questions per test. Time: 45 minutes (middle school) to 60 minutes (high school).

---

## 3. The Student Flow

**Step 1 — Landing Page + Registration**
Student arrives at the event-specific registration page. Picks their grade and track (SAT, AP Calculus, Grade 7, etc.). Enters name and email.

**Step 2 — Adaptive Diagnostic Test (24 questions, 45-60 min)**
Module 1 (12 questions) followed by adaptive routing to easy or hard Module 2 (12 more questions). Each question is tagged by FUAR dimension, difficulty, and topic. Timer runs per-module.

**Step 3 — Mindset Quiz (12 GRIC questions, ~2 min)**
Quick self-report across Growth, Relevance, Interest, and Confidence. 4-point scale. Takes under 2 minutes.

**Step 4 — Instant Archetype Reveal**
FUAR dominant dimension + GRIC mindset mode = one of 8 archetypes. Full-screen reveal with Greek symbol, archetype name, tagline, superpower, kryptonite, "This Is You" scenarios, famous mathematician pairings, and personalized study tips.

**Step 5 — Share Card**
One-tap save/share card with the archetype symbol, name, and tagline. Designed for social sharing — Instagram stories, text messages, school group chats.

**Step 6 — Full Student Report**
FUAR dimension scores (radar chart), topic-level heatmap showing strengths and gaps, overall score with school-level percentile context, and the complete archetype profile.

**Step 7 — Parent Report**
Separate report designed for parents. Includes grade-level proficiency assessment (or SAT estimate for HS), FUAR dimension breakdown in parent-friendly language, algebra readiness indicator (for grades 7-8), and specific next steps.

**Step 8 — Dashboard**
Persistent student dashboard with practice plan, progress tracking, FUAR radar chart, and score trajectory over time. For HS: SAT score progress. For MS: grade-level proficiency progress.

**Step 9 — Daily Practice**
Adaptive practice questions targeting the student's weakest FUAR dimensions and topics. Questions pulled from the full question bank for their track, not just the 24 they saw on the test.

**Step 10 — Practice Review**
Every practice question has a step-by-step worked solution with wrong-answer analysis. Not just "the answer is B" — a full explanation of the correct approach and why each wrong answer is wrong.

**Step 11 — Weekly Assessments**
Weekly mini-assessments recalculate FUAR scores and can trigger archetype evolution. A student who was Gamma (brilliant but inconsistent) might become Alpha (brilliant AND disciplined) as their Fluency improves. This evolution is visible on the dashboard.

---

## 4. High School vs. Middle School Differences

The platform handles both through template conditionals, not separate codebases. Here's what changes:

| Element | College Ready (HS, Grades 9-12) | Foundation Math (MS, Grades 6-8) |
|---|---|---|
| **Brand name** | College Ready Night | Foundation Math Night |
| **Tracks** | SAT, AP Calculus AB, AP Calculus BC, AP Statistics, Pre-Calculus, Algebra 2, Geometry, Algebra 1, Integrated Math | Grade 6, Grade 7, Grade 7 Accelerated, Grade 8 |
| **Score presentation** | SAT estimate range + percentile (for SAT track); AP score prediction (for AP tracks) | Grade-level proficiency: Advanced / Proficient / Approaching / Developing |
| **Special indicators** | AP course readiness | Algebra readiness (grades 7-8) |
| **Archetype names** | The Perfectionist, The Relentless, The Purist, The Quiet Genius, The Natural, The Dormant Force, The Inventor, The Maverick | The Machine, The Relentless, The Deep Thinker, The Quiet Genius, The Natural, The Undercover, The Builder, The Wildcard |
| **Archetype copy** | References SAT, AP exams, college readiness | References class tests, homework, grade-level work |
| **Parent concerns addressed** | SAT score prediction, AP readiness, college admission impact | Grade-level mastery, algebra readiness, high school course placement |
| **Test duration** | 60 min | 45 min |
| **Dashboard widget** | "Estimated SAT Math" + SAT Score Progress chart | "Grade-Level Proficiency" + Proficiency Progress chart |

---

## 5. The 8 Archetypes

### Sigma (σ) — Fluency × Engaged

| | High School | Middle School |
|---|---|---|
| **Name** | The Perfectionist | The Machine |
| **Tagline** | "You don't skip steps — and that's why you rarely get things wrong." | "You don't skip steps, and that's why you almost never get things wrong." |
| **Superpower** | Accuracy Under Pressure — executes cleanly on SAT/AP while others rush | Catches errors before they happen; step-by-step process is a machine |
| **Mathematician** | Euclid, Katherine Johnson, Sal Khan | Same |
| **FUAR / Mindset** | Fluency dominant / Engaged | Same |

### Delta (δ) — Fluency × Guarded

| | High School | Middle School |
|---|---|---|
| **Name** | The Relentless | The Relentless |
| **Tagline** | "You outwork everyone — and you know it." | Same |
| **Superpower** | Consistency — floor is higher than most people's ceiling | Even the worst day is better than most people's best |
| **Mathematician** | Ramanujan, Kobe Bryant, Maryam Mirzakhani | Same |
| **FUAR / Mindset** | Fluency dominant / Guarded | Same |

### Pi (π) — Understanding × Engaged

| | High School | Middle School |
|---|---|---|
| **Name** | The Purist | The Deep Thinker |
| **Tagline** | "You don't memorize — you understand." | "You don't memorize. You understand." |
| **Superpower** | Transfer — applies concepts to never-seen-before problems | Figures out new problem types while memorizers freeze |
| **Mathematician** | Feynman, Emmy Noether, Grant Sanderson | Same |
| **FUAR / Mindset** | Understanding dominant / Engaged | Same |

### Theta (θ) — Understanding × Guarded

| | High School | Middle School |
|---|---|---|
| **Name** | The Quiet Genius | The Quiet Genius |
| **Tagline** | "You see things in math that nobody else in the room sees." | Same |
| **Superpower** | Insight — sees connections textbooks don't point out | Notices patterns others walk right past |
| **Mathematician** | Grigori Perelman, Ada Lovelace, Terence Tao | Same |
| **FUAR / Mindset** | Understanding dominant / Guarded | Same |

### Phi (φ) — Application × Engaged

| | High School | Middle School |
|---|---|---|
| **Name** | The Natural | The Natural |
| **Tagline** | "You don't just solve problems — you see the math hiding in everything." | Same (minor punctuation change) |
| **Superpower** | Real-World Modeling — translates messy situations into math frameworks | Sees numbers where others see chaos |
| **Mathematician** | Florence Nightingale, Nate Silver, Elon Musk | Same |
| **FUAR / Mindset** | Application dominant / Engaged | Same |

### Lambda (λ) — Application × Guarded

| | High School | Middle School |
|---|---|---|
| **Name** | The Dormant Force | The Undercover |
| **Tagline** | "You're not bad at math — you're just waiting for math to earn your attention." | Same |
| **Superpower** | Purpose-Driven Focus — rivals anyone when they care | Goes all in when something clicks |
| **Mathematician** | Steve Jobs, Jay-Z, Simone Biles | Same |
| **FUAR / Mindset** | Application dominant / Guarded | Same |

### Alpha (α) — Reasoning × Engaged

| | High School | Middle School |
|---|---|---|
| **Name** | The Inventor | The Builder |
| **Tagline** | "You don't follow methods — you invent them." | Same |
| **Superpower** | Original Thinking — solves problems nobody taught them to solve | Figures out own path while others need step-by-step instructions |
| **Mathematician** | Euler, von Neumann, Maryam Mirzakhani | Same |
| **FUAR / Mindset** | Reasoning dominant / Engaged | Same |

### Gamma (γ) — Reasoning × Guarded

| | High School | Middle School |
|---|---|---|
| **Name** | The Maverick | The Wildcard |
| **Tagline** | "Your best work is brilliant. Your worst work is... interesting." | Same |
| **Superpower** | Breakthrough Thinking — cracks problems open when everyone else is stuck | Thinks in leaps, not steps; jumps over complexity |
| **Mathematician** | Galois, Nikola Tesla, Kanye West | Same |
| **FUAR / Mindset** | Reasoning dominant / Guarded | Same |

---

## 6. Question Bank

**Total: 1,068 questions across 10 tracks. Every question has a worked solution with step-by-step explanation and wrong-answer analysis.**

### High School — 864 questions

| Track | Questions | FUAR Coverage | Difficulty Range |
|---|---|---|---|
| SAT Math | ~96 | Balanced F/U/A/R | 1-5 |
| AP Calculus AB | ~96 | Balanced | 1-5 |
| AP Calculus BC | ~96 | Balanced | 1-5 |
| AP Statistics | ~96 | Balanced | 1-5 |
| Pre-Calculus | ~96 | Balanced | 1-5 |
| Algebra 2 | ~96 | Balanced | 1-5 |
| Geometry | ~96 | Balanced | 1-5 |
| Algebra 1 | ~96 | Balanced | 1-5 |
| Integrated Math | ~96 | Balanced | 1-5 |

### Middle School — 196 questions (4 new tracks)

| Track | Questions | Needed per Test | Surplus | FUAR Balance |
|---|---|---|---|---|
| Grade 6 | 48 | 24 | 2x coverage | Balanced across F/U/A/R, difficulty 1-5 |
| Grade 7 | 48 | 24 | 2x coverage | Balanced |
| Grade 7 Accelerated | 52 | 24 | 2.2x coverage | Slight F skew (acceptable) |
| Grade 8 | 48 | 24 | 2x coverage | Balanced |

### Tagging Structure

Every question carries:
- **Track** — which course/grade it belongs to
- **FUAR dimension** — exactly one of F, U, A, R
- **Difficulty** — 1 (easiest) to 5 (hardest)
- **Topic** — specific content area (e.g., "linear equations," "probability")

### Worked Solutions

All 1,068 questions have generated worked solutions stored in the database. Each solution includes:
- Step-by-step walkthrough of the correct approach
- Why each wrong answer choice is wrong (common misconceptions)
- Generated via Claude API as a one-time batch — no ongoing API cost

---

## 7. How to Test

### For the Team (Rigved, Joita)

**Production URL:** https://college-ready.onrender.com

**Demo events:**
- High school demo: event code `DEMO-2026`
- Middle school demo: event code `FOUNDATION-DEMO`

**Admin portal:** `/admin/login` (credentials: ask Himanshu)

**What to review:**
- **Question quality** — Are questions well-written? Correct difficulty level? Proper FUAR tagging?
- **Archetype accuracy** — Does the assigned archetype feel right for the student's performance pattern?
- **Report content** — Are the FUAR breakdowns, topic heatmaps, and parent reports clear and actionable?
- **FUAR tagging** — Reference doc: `edison/college-ready/fuar-tagging-reference.md`
- **Middle school copy** — Do the MS archetype descriptions, superpower/growth text, and "This Is You" scenarios land for 11-14 year olds?

**Full test flow:**
1. Go to `/register/DEMO-2026` (HS) or `/register/FOUNDATION-DEMO` (MS)
2. Register with any name/email, pick a grade and track
3. Complete the 24-question diagnostic (you can answer randomly to speed-test the flow)
4. Complete the 12-question mindset quiz
5. See the archetype reveal, share card, student report, parent report
6. Access the dashboard, try daily practice, review worked solutions

### For PTAs / School Partners

- Share the event-specific registration link: `college-ready.onrender.com/register/<EVENT_CODE>`
- Students register with name, email, grade, and track
- Results are instant — archetype reveal + report + practice plan delivered immediately after test completion
- Parents receive a separate parent report
- The admin portal tracks participation per event (registration count, completion rate, archetype distribution)
- Demo mode allows retaking the test for experimentation

### For Student Testing

1. Create a demo event in the admin portal (`/admin/login`)
2. Set the event type (high school or middle school), date range, and grade range
3. Share the generated registration link with test students
4. Students go through the full flow independently
5. Collect feedback via direct conversation — the feedback widget has been removed to reduce friction

---

## 8. Technical Details

| Component | Detail |
|---|---|
| **Stack** | Python + Flask + SQLite + Gunicorn |
| **Hosting** | Render (with persistent disk for the SQLite database) |
| **Question generation** | Claude API — one-time batch generation of 1,068 questions + worked solutions, stored in DB |
| **Ongoing API costs** | None for student-facing features. All questions, solutions, and archetype content are pre-generated and stored. |
| **Admin portal** | Full event management — create events, set date ranges, track participation, export data |
| **Database** | Single SQLite database: events, students, responses, practice sessions, weekly assessments |
| **Template system** | Jinja2 with `is_middle_school` context flag — same templates serve both HS and MS with conditionals |
| **Auth** | Session-based for students (no password); admin login with credentials |

---

## 9. What's Next

**Immediate (this week):**
- Complete Foundation Math Night template conditionals (branding, scoring display, dashboard widgets)
- MS-specific archetype copy in all templates (superpower, growth, "This Is You" sections)
- End-to-end testing of the middle school flow

**Short-term:**
- Student testing with real students (shorter diagnostic version TBD for time-constrained settings)
- Feedback collection mechanism (format TBD — direct conversation, survey, or in-app)
- Email notifications for parents (auto-send parent report after test completion)

**Medium-term:**
- Lite quiz — 90-second viral version with 5-6 questions that gives a quick archetype. Designed for share links and social distribution. Not a full diagnostic, but a top-of-funnel hook.
- Archetype evolution tracking — visible progression as students practice (e.g., Gamma evolving to Alpha)
- School-level analytics dashboard for partner schools

---

*Built by Himanshu / Edison. Platform live at college-ready.onrender.com.*
