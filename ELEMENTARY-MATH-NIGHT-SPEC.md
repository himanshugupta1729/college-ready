---
type: spec
topic: Elementary Math Night — Product Specification
date: 2026-04-02
status: draft
version: 1
---

# Elementary Math Night — Product Specification

**What:** A plug-and-play live event product for elementary school (K-5) Family Math Nights. Facilitator opens a URL, enters an event code, and the product drives the entire event from the projector. Families participate via their phones. Everything is tracked digitally — no self-scoring.

**Two sessions per event:** K-2 (5:30 PM) and 3-5 (6:30 PM). ~50 families per session. Sequential, same room, same facilitator.

**Physical kit shipped to school:** Goodie bags (Cuemath branded), A4 "Crack the Code" challenge worksheets (K-2 and 3-5 versions), pencils. No archetype cards — archetype is digital only.

---

## Architecture

### Two Interfaces

**1. Presenter Mode (projector)**
- URL: `/elementary/{event-code}/present`
- Full-screen, projector-optimized (dark background, large text, high contrast)
- Facilitator controls: "Next" button, pause, skip
- Shows: questions, timers, answer reveals, live leaderboard, transitions between rounds
- Grade band toggle: K-2 or 3-5 (selected at event start)

**2. Player Mode (family phone)**
- URL: `/play/{event-code}`
- Mobile-optimized, single-column, large tap targets
- Persistent through all rounds — family registers once, stays in the game
- Shows: answer buttons, code entry field, quiz interface, archetype result
- Syncs with presenter via WebSocket (or polling fallback)

### Data Flow

```
Family scans QR → registers (parent name, email, child name, grade)
  → Round 1: 7 warm-up answers captured (FUAR-tagged)
  → Round 2: code entry validates answers, captures completion time
  → Round 3: 8 parent quiz answers captured
  → System auto-calculates archetype from Rounds 1+2 data
  → Archetype shown on phone immediately
  → QR → MathGym app (archetype pre-loaded, journey begins)
  → 48-hour follow-up email: archetype + performance summary + MathGym CTA
```

---

## Event Flow — Detailed Run-of-Show

### Pre-Event Setup (5 min)
- Facilitator opens presenter URL on laptop connected to projector
- Selects grade band (K-2 or 3-5)
- Projector shows welcome screen with large QR code
- Families scan QR as they arrive, register on phones
- A4 challenge worksheets distributed face-down on tables
- Goodie bags at check-in or on tables

### Round 1 — Warm-Up Puzzles (10 min)

**Purpose:** Build energy, teach the format, capture initial FUAR data.

**Format:** 7 questions shown on projector one at a time. Phone shows 4 answer buttons (A/B/C/D). Family discusses, taps answer. Timer: 45 seconds per question.

**Question rotation to involve both kids and parents:**

| Q# | Label on Projector | Difficulty | Who Leads |
|----|-------------------|-----------|-----------|
| 1 | "Kids First!" | Easy (K-2 level) | Child tells parent what to tap |
| 2 | "Kids First!" | Medium (3-5 level) | Older kids lead |
| 3 | "Parents' Turn!" | Tricky (adult) | Parent leads |
| 4 | "Family Team!" | Visual pattern | Both discuss |
| 5 | "Kids First!" | Easy | Child leads |
| 6 | "Parents' Turn!" | Tricky | Parent leads |
| 7 | "Family Team!" | Fun/surprising | Both |

Note: For K-2 sessions, Q2 becomes easier (still "Kids First!" but K-2 appropriate). For 3-5 sessions, Q1 becomes slightly harder. The set is grade-band specific.

**After each question:**
1. Timer expires or all answers in → answer reveal animation
2. "Did you know?" fun fact (one line)
3. Live leaderboard flashes (top 5 families by score)
4. Next question

**FUAR tagging:** Each question is tagged to a FUAR dimension. The system records which dimensions the family got right.

**Scoring:** +100 points base for correct answer. Speed bonus: +50 if answered in first 15 sec, +25 if in first 30 sec. Wrong = 0 (no negatives — no failure state).

### Round 2 — Family Math Challenge (15 min)

**Purpose:** Hands-on collaborative activity. Parent and child must both contribute. Competitive.

**Format:** "Crack the Code" — printed A4 worksheet.

**A4 Worksheet Design:**
- Landscape orientation
- Fold line down the center (or clear visual divider)
- LEFT SIDE: "Student Zone" — 3 puzzles, age-appropriate, visual
- RIGHT SIDE: "Parent Zone" — 3 puzzles, adult-level, word/number problems
- Parent and child sit side by side, each has their section facing them
- Each puzzle's answer produces one digit of a 6-digit code
- BOTTOM CENTER: "Your Secret Code: _ _ _ _ _ _" (digits from both sides)

**K-2 Worksheet — Student Zone puzzles:**
1. Pattern completion (visual: what comes next in the sequence?) → digit
2. Counting/grouping (count objects arranged in groups) → digit
3. Shape puzzle (which shape completes the picture?) → digit

**K-2 Worksheet — Parent Zone puzzles:**
4. Percentage/fraction word problem → digit
5. Logic deduction ("If A costs more than B, and C costs less than A but more than B...") → digit
6. Estimation ("Approximately how many jelly beans in this jar?") → digit

**3-5 Worksheet — Student Zone puzzles:**
1. Number pattern (find the rule, predict next number) → digit
2. Multi-step word problem (real-world: pizza party budget) → digit
3. Spatial reasoning (fold this shape — what does it look like?) → digit

**3-5 Worksheet — Parent Zone puzzles:**
4. Compound percentage problem → digit
5. Probability/combinatorics → digit
6. Data interpretation (read a chart, answer a question) → digit

**How it works:**
1. Projector shows: "CHALLENGE TIME! Flip your worksheet. You have 15 minutes. Both sides must be solved to crack the code!"
2. Timer counts down on projector (large, visible)
3. Families work simultaneously — child on left, parent on right
4. When they think they have all 6 digits, they enter the code on their phone (game board shows "Enter Code" button)
5. If correct: confetti animation on phone + family name appears on projector leaderboard with completion time
6. If wrong: phone shows "Not quite — double check!" (can retry unlimited)
7. Leaderboard updates live on projector as families crack it

**Bonus (optional, last 2 min):** The worksheet has a fold-along-lines instruction. Once code is cracked, fold the paper to reveal a hidden Cuemath logo or math joke. Small tactile reward.

**Scoring:** +500 points for cracking the code. Time bonus: +200 if in first 5 min, +100 if in first 10 min, +50 after. This goes on the cumulative leaderboard.

### Round 3 — Parent Pop Quiz (8 min)

**Purpose:** Parents-only competitive quiz. Energy peak. Kids become the audience.

**Format:** 8 rapid-fire questions on projector + phone. Parents tap answers. 30 seconds per question.

**Questions designed to be:** Fun, surprising, "I should know this but..." — percentages, mental math, real-world estimation, logic. NOT obscure math — things every parent encounters (tips, discounts, cooking ratios, distance/time).

**Example questions:**
1. "You're tipping 20% on a $85 dinner. How much is the tip?" (A: $15, B: $17, C: $18.50, D: $20)
2. "A store has 30% off, then an extra 20% off that. What's the total discount?" (A: 50%, B: 44%, C: 56%, D: 36%)
3. "Your recipe serves 4. You need to serve 10. The recipe calls for 2/3 cup of sugar. How much do you need?" (A: 1 cup, B: 1⅓ cups, C: 1⅔ cups, D: 2 cups)
4. "A car travels 45 miles in 40 minutes. What's the speed in mph?" (A: 60, B: 67.5, C: 72, D: 55)

**Student involvement:**
- Kids watch the projector — answer reveals are dramatic ("Only 31% of parents got this right!")
- FINAL QUESTION (Q8): "Hand your phone to your kid!" — one age-appropriate question that the child answers. The projector labels it "KIDS TAKE OVER!" Big moment. Cheering.

**After each question:** Answer reveal + explanation + leaderboard update.

**Scoring:** Same as Round 1 (+100 base, speed bonus). Cumulative with all rounds.

### Round 4 — Archetype Reveal + MathGym (5 min)

**Purpose:** Personalized result. Digital archetype. Transition to MathGym app.

**How archetype is calculated:**
- Round 1: 7 questions tagged to FUAR dimensions → which dimensions the child got right
- Round 2: 3 student-side puzzles tagged to FUAR dimensions → which they solved
- Combined: highest FUAR dimension = archetype
- For K-2: 4 archetypes (one per FUAR dimension: Speed Spark, Deep Thinker, Problem Solver, Pattern Seeker)
- For 3-5: 8 archetypes (FUAR × Explorer/Builder)

**Event flow:**
1. Projector: "Your results are in!" — dramatic pause
2. Projector cycles through each archetype with animation, description, fun graphic
3. Phone shows: "Your child's Math Archetype: **Speed Spark!**" with description
4. Projector: Final leaderboard — top 3 families announced. Small prizes from goodie bag (optional).
5. Projector: "Take your math superpower home!" — large QR code for MathGym app
6. Phone shows: "Download MathGym to continue your math journey" with app store links
7. MathGym deep link pre-loads the child's archetype so onboarding is personalized

**No physical archetype cards.** The archetype lives on the phone screen (shareable — "Share your archetype" button for social) and in the MathGym app.

---

## Post-Event Conversion Funnel

### Immediate (event end)
- Family has MathGym app with archetype pre-loaded
- App onboarding: "Welcome, Speed Spark! Start your first Daily Workout"

### 48-Hour Email
- Subject: "[Child Name]'s Math Night Results — [School Name]"
- Contains: Archetype graphic, Round 1 performance (e.g., "strong in Application, developing Fluency"), Round 2 completion rank, fun stats
- CTA: "Your child's first week on MathGym includes a personalized MathFit diagnostic. After 3 sessions, you'll get a detailed report."

### Day 3-5: MathGym In-App Diagnostic
- After 3 daily workouts, the app generates a mini-FUAR report
- Push notification to parent: "Your child's MathFit report is ready"
- This report is the REAL conversion lever — it shows gaps, not just an archetype

### Day 5-7: BD Rep Follow-Up
- Rep has: archetype, Round 1/2/3 data, MathGym engagement data
- "I see [child name] has been doing daily workouts — here's what we noticed about their Fluency..."
- Trial booking

---

## Physical Kit Contents (shipped to school)

| Item | Quantity | Notes |
|------|----------|-------|
| A4 Challenge Worksheets (K-2) | 60 | Landscape, fold-in-half design, branded |
| A4 Challenge Worksheets (3-5) | 60 | Landscape, fold-in-half design, branded |
| Pencils (Cuemath branded) | 120 | One per family |
| Goodie bags | 120 | Cuemath branded, contents TBD (stickers, mini puzzle book, pencil, MathGym card) |
| Facilitator Guide (laminated) | 1 | Step-by-step: plug in laptop, open URL, click Next |
| Event QR Code poster (A3) | 2 | For check-in tables |

No archetype cards. No printed scoring sheets.

---

## Technical Implementation

### New Routes in College-Ready App

| Route | Purpose |
|-------|---------|
| `/elementary/` | Event code entry page |
| `/elementary/{code}/present` | Presenter mode (projector) |
| `/elementary/{code}/present/admin` | Facilitator controls (next, pause, grade-band select) |
| `/play/{code}` | Player mode (family phone) |
| `/play/{code}/register` | Family registration |
| `/play/{code}/game` | Live game board (answers, code entry, quiz) |
| `/play/{code}/result` | Archetype result + MathGym CTA |
| `/elementary/{code}/leaderboard` | Standalone leaderboard (optional second screen) |

### Database Schema (new tables)

**elementary_events**
- id, event_code, school_name, event_date, grade_band, status, created_at

**elementary_families**
- id, event_id, parent_name, parent_email, child_name, child_grade, archetype, total_score, round2_completion_time, created_at

**elementary_answers**
- id, family_id, round (1/2/3), question_number, answer, correct (bool), time_taken_ms, fuar_dimension

### Real-Time Sync

**Option A (recommended for simplicity): Polling**
- Player phone polls `/api/elementary/{code}/state` every 2 seconds
- Returns: current_round, current_question, timer_remaining, leaderboard_top5
- Facilitator advances → state updates → phones pick it up within 2 seconds

**Option B (ideal but more complex): WebSocket**
- Server pushes state changes to all connected phones
- Instant sync, better UX
- More complex to implement, especially on Render free tier

Recommend starting with polling (simpler, works on free Render), upgrade to WebSocket later if needed.

### Question Bank Structure

```json
{
  "grade_band": "k2",
  "round1": [
    {
      "id": 1,
      "label": "Kids First!",
      "question_text": "What comes next? 2, 4, 6, __",
      "question_image": null,
      "options": ["7", "8", "9", "10"],
      "correct": 1,
      "fuar": "F",
      "fun_fact": "This is called counting by 2s — you're already doing algebra!"
    }
  ],
  "round2_code": "483712",
  "round2_student_puzzles": [...],
  "round2_parent_puzzles": [...],
  "round3": [
    {
      "id": 1,
      "question_text": "20% tip on an $85 dinner?",
      "options": ["$15", "$17", "$18.50", "$20"],
      "correct": 1,
      "fun_fact": "Only 34% of adults get tip calculations right on the first try!"
    }
  ]
}
```

### Archetype Calculation

```
For each family:
  fuar_scores = {F: 0, U: 0, A: 0, R: 0}

  For each Round 1 answer (correct only):
    fuar_scores[question.fuar] += 1

  For each Round 2 student puzzle (correct based on code digits):
    fuar_scores[puzzle.fuar] += 2  (weighted higher — hands-on)

  primary_dimension = max(fuar_scores)

  K-2: archetype = FUAR_TO_ARCHETYPE_4[primary_dimension]
  3-5:
    explorer_builder = determine_style(round1_answers)  # based on approach patterns
    archetype = FUAR_TO_ARCHETYPE_8[primary_dimension][explorer_builder]
```

**K-2 Archetypes (4):**
| FUAR | Archetype | Description |
|------|-----------|-------------|
| F | Speed Spark | Lightning-fast with numbers |
| U | Deep Thinker | Understands the "why" behind math |
| A | Problem Solver | Uses math in the real world |
| R | Pattern Seeker | Spots patterns others miss |

**3-5 Archetypes (8):**
Same as existing archetype system (FUAR × Explorer/Builder).

---

## Build Plan

### Phase 1: Core Platform (Days 1-3)
- [ ] Presenter mode: full-screen projector view with question display, timer, transitions
- [ ] Player mode: mobile game board with registration, answer buttons
- [ ] Polling-based sync between presenter and players
- [ ] Live leaderboard (top 5, updates after each question)
- [ ] Round 1 complete flow: 7 questions, answer reveal, scoring

### Phase 2: Challenge + Quiz (Days 3-5)
- [ ] Round 2: code entry interface on phone, validation, completion tracking
- [ ] Round 3: parent quiz flow (reuses Round 1 mechanics)
- [ ] Cumulative scoring across all rounds
- [ ] Archetype calculation and reveal screen

### Phase 3: Post-Event (Days 5-6)
- [ ] Archetype result page with MathGym deep link
- [ ] 48-hour email template with performance data
- [ ] Event analytics dashboard (facilitator/admin view)
- [ ] Share card ("My child is a Speed Spark!")

### Phase 4: Content + Design (parallel)
- [ ] Question bank: 7 warm-up + 8 parent quiz per grade band (14 + 16 = 30 questions)
- [ ] A4 worksheet design: K-2 and 3-5 versions (Vignelli task)
- [ ] Presenter slide design: backgrounds, animations, transitions
- [ ] MathGym onboarding integration spec

---

## Open Questions

1. **Goodie bag contents** — what goes in them? Stickers, mini puzzle book, Cuemath pencil, MathGym download card?
2. **MathGym deep link** — does MathGym currently support deep linking with pre-loaded archetype? If not, this is a product dependency.
3. **WiFi at schools** — can we assume WiFi? If not, the phone-based game breaks. Fallback: facilitator's phone as hotspot? Or offline worksheet-only mode?
4. **Question content creation** — who writes the actual math puzzles? Need grade-appropriate, FUAR-tagged, fun questions. Rigved/Joyita or Edison?
5. **A4 worksheet printing** — printed by Cuemath and shipped, or PDF sent to school for local printing?
6. **MathGym onboarding diagnostic** — does the 3-day diagnostic flow exist in MathGym? If not, this is the biggest product dependency for conversion.
