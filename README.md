# College Ready — Math Fit Check

A diagnostic product for high school students that tells them **how they think mathematically**, not just what they score. Built for College Ready Night events and ongoing student engagement.

## What It Does

A student picks their track, takes a 60-70 minute adaptive test, and gets:

1. **FUAR Profile** — scores across four dimensions of mathematical thinking:
   - **Fluency**: Can you execute procedures accurately and efficiently?
   - **Understanding**: Do you grasp *why* the math works, not just *how*?
   - **Application**: Can you use math in unfamiliar, real-world contexts?
   - **Reasoning**: Can you spot patterns and think through novel problems?

2. **Math Archetype** — one of six thinker types assigned based on the FUAR profile:
   - Speed Spark (high Fluency), Deep Diver (high Understanding), Problem Solver (high Application), Pattern Seeker (high Reasoning), Balanced Thinker, Rising Builder

3. **Score Estimate** — SAT estimated score range (for SAT track), AP readiness % (for AP tracks), or course proficiency (for HS courses)

4. **4-Week Daily Practice Plan** — 8 questions/day, 10 minutes, targeted at the student's weakest FUAR dimension. Streak tracking, weekly reassessment.

## Tracks Available (10 total)

| Track | Questions | Time | What It Measures |
|---|---|---|---|
| **SAT Math** | 44 | 70 min | Estimated SAT Math score (200-800) |
| **AP Precalculus** | 24 | 70 min | Readiness for AP Precalc |
| **AP Calculus AB** | 28 | 70 min | Readiness for AP Calc AB |
| **AP Calculus BC** | 30 | 70 min | Readiness for AP Calc BC |
| **AP Statistics** | 28 | 70 min | Readiness for AP Stats |
| **Algebra 1** | 25 | 60 min | Course proficiency |
| **Geometry** | 25 | 60 min | Course proficiency |
| **Algebra 2** | 28 | 60 min | Course proficiency |
| **Precalculus** | 28 | 60 min | Course proficiency |
| **Statistics** | 22 | 60 min | Course proficiency |

## How the Adaptive Test Works

We use the same approach as the Digital SAT — **Multi-Stage Testing (MST)**:

```
MODULE 1 (first half)
├── Medium difficulty questions (difficulty 2-3)
├── Same level for every student
├── Balanced across all 4 FUAR dimensions
├── Establishes baseline performance
│
▼ ADAPTIVE ROUTING (invisible to student)
│
├── Scored 70%+ → routed to HARD pool (difficulty 4-5)
├── Scored 40-70% → routed to MEDIUM pool (difficulty 3-4)
├── Scored <40% → routed to FOUNDATION pool (difficulty 1-2)
│
MODULE 2 (second half)
├── Questions from the routed difficulty pool
├── Still balanced across FUAR dimensions
├── No two students get the same test (random selection from pool)
```

**Why this matters:**
- Strong students don't waste time on easy questions — they get challenged where it counts
- Struggling students don't get crushed by impossible questions — they get assessed at their actual level
- The system gets more precise data in the same time window
- Students experience "Goldilocks difficulty" — challenging but not discouraging

## The FUAR × Content Tagging System

Every question in the bank is dual-tagged:

1. **Content area** (what topic) — e.g., "Heart of Algebra", "Integration", "Circles"
2. **FUAR dimension** (what skill) — Fluency, Understanding, Application, or Reasoning

This means we can tell a student: *"You scored well on Algebra topics but poorly on Geometry — AND within Geometry, your Fluency is fine (you know the formulas) but your Application is weak (you can't use them in word problems)."*

This is the insight no other diagnostic gives. School report cards show topic grades. SAT shows a single score. We show **how you think within each topic**.

### How FUAR Maps to Questions

The same topic can be tested at different FUAR levels:

**Example: Quadratic equations**
- **Fluency**: "Solve x² - 5x + 6 = 0" → Can you execute the procedure?
- **Understanding**: "The equation x² + 6x + 9 = 0 has how many distinct solutions? Why?" → Do you understand the discriminant?
- **Application**: "A ball is thrown with height h(t) = -16t² + 48t + 5. What is the maximum height?" → Can you model a real situation?
- **Reasoning**: "For what value of c does x² - 6x + c = 0 have exactly one solution?" → Can you reason backwards from properties?

## Question Bank

864 questions across all 10 tracks. All original (no copyright issues — generated, not copied from any test). Each question has:
- 4 multiple-choice options where wrong answers represent common student mistakes
- Difficulty rating (1-5)
- FUAR dimension tag
- Content unit tag
- Explanation of the correct answer

### Where Rigved Can Help

1. **FUAR tagging validation** — Are we correctly classifying questions as F, U, A, or R? This is the pedagogical backbone. If a question we tagged as "Reasoning" is actually just "Fluency with extra steps," the FUAR profile will be inaccurate.

2. **Difficulty calibration** — Our difficulty 1-5 ratings are estimated, not empirically validated. Rigved's experience with student performance can help calibrate: "This question is tagged difficulty 3 but most Grade 10 students would find it a 4."

3. **Content coverage gaps** — Are we missing important topics within any track? For example, in AP Calc AB, do we adequately cover related rates and optimization (the topics students struggle with most)?

4. **Question quality** — Are the wrong answer options realistic? Good diagnostic questions have wrong answers that represent specific misconceptions, not random numbers.

5. **Archetype definitions** — Do the six FUAR-based archetypes make pedagogical sense? Should there be more? Fewer? Different combinations?

## The Student Journey

```
COLLEGE READY NIGHT (or online)
│
├── Student registers (name, grade, parent email, track)
├── Takes adaptive test (60-70 min)
├── Gets archetype reveal instantly (in-room moment)
│
▼ 48 HOURS LATER
│
├── Student gets report (empathetic, forward-looking)
├── Parent gets report (data-driven, specific gaps)
│
▼ DAY 3 ONWARDS
│
├── Daily practice: 8 questions, 10 min, focused on weakest dimension
├── Streak tracking (like Whoop — simple, daily, sticky)
├── Weekly reassessment: updated FUAR scores + progress tracking
│
▼ AFTER 4 WEEKS
│
├── Student sees score improvement
├── Natural conversion: "Want to keep improving? Work with a Cuemath tutor."
```

## Tech Stack

- Python + Flask
- SQLite
- Claude API (for report generation — not yet built)
- Deployable on Render

## Status

- [x] All 10 tracks configured with adaptive testing
- [x] 864 questions seeded across all tracks
- [x] FUAR scoring engine + archetype assignment
- [x] Student dashboard + daily practice
- [ ] Report generation (student + parent versions)
- [ ] Question bank review/validation with curriculum team
- [ ] Deployment to production
- [ ] First pilot test with real students
