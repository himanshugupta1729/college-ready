---
type: analysis
topic: Test-Taking UX Design Brief
date: 2026-03-28
status: draft
version: 1
---

# Test-Taking UX Design Brief — College Ready Math Fit Check

## Executive Summary

This brief synthesizes UX patterns from five leading assessment/learning platforms (SAT Bluebook, Khan Academy, Duolingo, Brilliant.org, IXL) and applies them to College Ready's `test_question.html` template. The goal: an interface that feels calm, clear, and professional for high-school students (ages 14-18) taking a timed math diagnostic — reducing test anxiety while maintaining the seriousness of an assessment.

---

## Part 1: Key Design Principles for Test UX

### 1. Calm Authority
The SAT Bluebook interface succeeds because it feels like a serious tool, not a game. Clean backgrounds, restrained color, generous whitespace. Our audience is high-school students preparing for college-level math — the tone should be confident and supportive, not gamified or childish. Think "professional assessment" not "quiz app."

### 2. One Thing at a Time
Every platform studied displays one question per screen. Duolingo takes this further — nothing else competes for attention during the active exercise. The question text and answer options should dominate the viewport. Everything else (timer, progress, navigation) is peripheral.

### 3. Progressive Disclosure of Stress
The SAT Bluebook lets students hide the timer entirely, revealing it only at the 5-minute warning. This is the gold standard for time-anxiety management. Duolingo shows no timer at all for most exercises. The principle: time pressure should be felt, not seen, until it matters.

### 4. Immediate Spatial Certainty
Students should always know: Where am I? How far along? What do I do next? Khan Academy and Bluebook both solve this with a question map (numbered dots showing answered/unanswered/current). This is more useful than a progress bar alone because it shows *which* questions are done, not just a percentage.

### 5. Touch-Target Generosity
IXL and Duolingo design for touch first. Answer cards should be large (minimum 48px height, ideally 56-64px), with generous padding. A finger tap should never miss. Khan Academy's check button is full-width on mobile. Every interactive element must meet the 44px minimum.

### 6. Friction-Free Forward Motion
Duolingo's lesson flow has near-zero friction between questions — answer, see feedback, next question loads automatically. For a timed diagnostic, the transition between questions should be fast and smooth. No unnecessary confirmation dialogs. Select answer, submit, next.

### 7. Accessibility Is Non-Negotiable
WCAG 2.1 AA compliance minimum. 4.5:1 contrast ratio for all text. Keyboard navigation for all interactions. Screen reader support with proper ARIA labels. Focus indicators that are visible. Font sizes never below 16px for body text.

---

## Part 2: Platform-by-Platform Patterns

### SAT Bluebook — What They Do Well
- **Split-screen layout** for reading passages (passage left, question right) — not applicable to our MCQ format, but the concept of dedicated content zones is
- **Hideable timer** — students choose whether to see it; 5-minute auto-reveal
- **Question navigation panel** — numbered grid showing answered, unanswered, marked-for-review, and current question
- **Mark for Review** — bookmark icon to flag uncertain answers without skipping
- **Option Eliminator** — strikethrough wrong answers to narrow choices
- **Clean, muted color palette** — dark navy/white, minimal accent color
- **No gamification** — the seriousness of the interface matches the stakes

### Khan Academy — What They Do Well
- **Immediate feedback** after each answer (correct/incorrect + explanation) — not for our timed diagnostic, but the "Check" button pattern is clean
- **Hints system** with progressive reveal — not applicable to assessment mode, but the skip button with step-by-step guide is excellent for practice
- **Simplified pre/post cards** — clear expectation-setting before an exercise (how many questions, estimated time)
- **Progress shown as skill levels** rather than raw question counts

### Duolingo — What They Do Well
- **Progress bar at top** fills left-to-right with color on correct answers — simple, motivating, non-distracting
- **Micro-interactions**: satisfying chime on correct answer, celebratory animation on completion
- **Question variety in layout** (multiple choice, word bank, typing, speaking) — keeps engagement high
- **Bottom-anchored action button** (Check) — always in the same place, thumb-reachable on mobile
- **Green = correct, Red = incorrect** — universal color language for feedback
- **Lesson structure**: starts easy, builds difficulty — maintains confidence

### Brilliant.org — What They Do Well
- **Interactive problem-solving** — manipulable visuals alongside questions
- **Conversational problem flow** — feels like guided discovery, not interrogation
- **Game feel without gamification** — satisfying animations and transitions that feel polished
- **Color-coded learning paths** — clear visual progression

### IXL — What They Do Well
- **SmartScore builds quickly at start** — front-loads positive reinforcement to build self-efficacy
- **Real-time adaptive difficulty** — adjusts per-question (our Module 1 to Module 2 adaptation is similar)
- **Clean, distraction-free question display** — question text + options + submit, nothing else
- **Immediate wrong-answer explanation** — shows the concept before moving on

---

## Part 3: Audit of Current `test_question.html`

### What to Keep (Working Well)

1. **Full-viewport test shell** — The flex-column layout with fixed header/footer and scrollable body is the correct architecture. Do not change this.

2. **Option cards with letter badges** — The A/B/C/D letter squares alongside option text is clean and standard. The selected state (yellow border + light yellow background) is on-brand and clear.

3. **Keyboard shortcuts (A/B/C/D + Enter)** — This is a power-user feature that Bluebook also supports. Excellent for desktop users. Keep it.

4. **Question navigator dots in footer** — The numbered dots with answered/current states follow the Bluebook pattern. This is correct.

5. **Back-navigation prevention** — Pushing history state to prevent accidental back-button is necessary for test integrity.

6. **Skip button** — Matches Khan Academy and Bluebook patterns. Essential for timed tests.

7. **Time-spent tracking per question** — Hidden input capturing elapsed time is valuable diagnostic data. Keep it.

### What to Change

#### High Priority

**H1. Timer Anxiety Reduction**
- Current: Timer is always visible, prominent, with aggressive red pulsing animation when below 5 minutes.
- Problem: Constant visible countdown increases anxiety, especially for students who are already math-anxious. The pulsing red at 5 minutes feels punitive.
- Recommendation: Make the timer collapsible/hideable by default. Show a small clock icon that expands on hover/tap. Auto-reveal the timer at the 5-minute mark with a gentle notification (not a pulsing red alarm). Replace the `pulse-border` animation with a single subtle color transition. Use warm amber (`#F59E0B`) for the warning state instead of red (`#DC2626`).

**H2. Progress Bar Should Show Completion, Not Position**
- Current: Progress bar fills based on `(current - 1) / total`, meaning it shows *position* in the sequence.
- Problem: A student on question 10 of 30 who has answered 25 questions (jumping around) sees 30% filled, which is demoralizing and inaccurate.
- Recommendation: Fill the progress bar based on *answered questions / total questions*. This rewards effort and shows true progress. Add a subtle text label: "18 of 30 answered" next to the bar.

**H3. Question Text Size and Spacing**
- Current: Question text is 20px with 1.6 line-height. Good on desktop, slightly small on mobile for math content.
- Recommendation: Increase to 22px on desktop, 20px on mobile (via media query). Increase `margin-bottom` from 32px to 40px for more breathing room between question and options. Math notation (if rendered via KaTeX) needs additional vertical padding.

**H4. Option Card Touch Targets**
- Current: Padding is 16px 20px. The cards are adequate but tight on mobile.
- Recommendation: Increase to 20px 24px on all screens, 24px 24px on mobile (min-height 60px). Add a subtle scale transform on tap (`transform: scale(0.98)` on `:active`) for tactile feedback.

**H5. Submit Button Disabled State**
- Current: `opacity: 0.35` when disabled. This makes the button nearly invisible.
- Recommendation: Use `opacity: 0.5` with a lighter background tone. The button should be *visible but clearly inactive* — students should see where the action is, even before they select an answer.

#### Medium Priority

**M1. Add "Mark for Review" Functionality**
- Bluebook's strongest feature. Allow students to flag a question they want to revisit. Add a small bookmark/flag icon in the question header area. Flagged questions show a distinct state in the navigator dots (e.g., orange border or small flag indicator).

**M2. Add Option Elimination (Strikethrough)**
- Bluebook feature that reduces cognitive load. On right-click or long-press on an option card, allow students to strike it through (dim it, add a line-through on text). This helps with process-of-elimination thinking, which is a core test-taking strategy.

**M3. Mobile Footer Redesign**
- Current: Question navigator dots + skip + submit all in one footer row. On mobile with 30 questions, the nav dots will overflow or wrap awkwardly.
- Recommendation: On mobile (below 640px), move the question navigator into a slide-up drawer accessed via a "Question Map" button. Keep only Skip and Submit in the fixed footer. This gives the footer breathing room and keeps the primary actions thumb-reachable.

**M4. Transition Between Questions**
- Current: Full page reload on form submit.
- Recommendation: If feasible, add a subtle fade transition (CSS only, 150ms) when navigating between questions. Even with full page reloads, a CSS `animation: fadeIn 0.2s ease` on `.question-card` would smooth the experience. This matches the polish of Brilliant.org and Duolingo.

#### Low Priority (Future Enhancements)

**L1. Micro-Feedback on Selection**
- When an option is selected, add a very brief (100ms) subtle animation — the letter badge could do a quick scale-up (`1.0 -> 1.1 -> 1.0`). This is the Duolingo principle: every interaction should feel responsive.

**L2. End-of-Module Encouragement**
- When transitioning from Module 1 to Module 2 (adaptive test), show a brief interstitial: "Module 1 complete. Module 2 is calibrated to your level. Keep going." This matches Khan Academy's simplified post-exercise card and reduces the anxiety of not knowing what comes next.

**L3. Keyboard Shortcut Hints**
- Current: There is a `.keyboard-hint` class defined in CSS but it does not appear in the HTML template.
- Recommendation: Add a small hint in the footer on desktop: `Press A-D to select, Enter to submit`. Hide on mobile. This is a discoverability aid, not a crutch.

---

## Part 4: Color, Typography, and Spacing Recommendations

### Color Palette for Test Mode

The test interface should use a *restrained subset* of the brand palette. Less color = less distraction = less anxiety.

| Element | Color | Token | Notes |
|---|---|---|---|
| Background | `#FFFFFF` | white | Clean, bright, no tint |
| Top bar / Footer | `#F9FAFB` | surface-light | Slightly cooler than current `#F5F5F5` — creates a softer contrast between chrome and content |
| Question text | `#191919` | near-black | Full contrast for readability |
| Secondary text | `#6B7280` | gray-500 | Slightly bluer than current `#666666` — reads as more modern |
| Option card border | `#E5E7EB` | gray-200 | Neutral, recedes |
| Option card border (hover) | `#D1D5DB` | gray-300 | Subtle lift |
| Selected option border | `#FFBA07` | brand-yellow | On-brand, clear selection |
| Selected option background | `rgba(255, 186, 7, 0.06)` | yellow-wash | Lighter than current 0.08 — more subtle |
| Timer normal | `#374151` | gray-700 | Calm, not prominent |
| Timer warning | `#F59E0B` | amber | Warm, not alarming |
| Timer critical (under 2 min) | `#DC2626` | red | Reserve red for genuine urgency |
| Progress bar fill | `#10B981` | green | Matches "answered" navigator dots, reads as "completed" |
| Navigator: current | `#FFBA07` | brand-yellow | Stand out |
| Navigator: answered | `#10B981` | green | Completed |
| Navigator: unanswered | `#F3F4F6` | gray-100 | Recedes |
| Navigator: flagged | `#F59E0B` | amber | Attention-worthy but not alarming |

### Typography

| Element | Size (Desktop) | Size (Mobile) | Weight | Line-Height |
|---|---|---|---|---|
| Question number label | 12px | 12px | 700, uppercase | 1.0 |
| Question text | 22px | 20px | 500 | 1.65 |
| Option text | 16px | 16px | 400 | 1.5 |
| Option letter | 13px | 13px | 700 | 1.0 |
| Timer display | 18px | 16px | 700, tabular-nums | 1.0 |
| Question counter | 13px | 12px | 600 | 1.0 |
| Button text | 15px | 15px | 600 | 1.0 |
| Keyboard hints | 12px | hidden | 400 | 1.0 |

Font: Inter (already in use). No changes needed. Inter's tabular numerals are ideal for the timer.

### Spacing

| Element | Current | Recommended | Rationale |
|---|---|---|---|
| Top bar height | 60px | 56px | Slightly tighter, more Bluebook-like |
| Top bar padding | 0 28px | 0 24px | Consistent with body padding |
| Question card max-width | 680px | 720px | Slightly wider for math content with notation |
| Question body padding | 40px 24px | 48px 24px | More vertical breathing room |
| Question text margin-bottom | 32px | 40px | Clear separation from options |
| Option card padding | 16px 20px | 20px 24px | Larger touch targets |
| Option card gap | 10px | 12px | Slightly more breathing room |
| Option card border-radius | `var(--radius)` (4px) | 8px | Matches High School grade-band feel while being slightly more approachable |
| Footer padding | 16px 28px | 14px 24px | Slightly tighter to maximize question area |
| Footer question nav dot size | 28px | 32px on mobile | Easier touch targets |

### Mobile Breakpoints

```
/* Tablet and below */
@media (max-width: 768px) {
    Question text: 20px
    Option padding: 24px 24px
    Timer: 16px
    Top bar: collapse progress bar text, show only bar
    Footer: simplify navigator to drawer
}

/* Phone */
@media (max-width: 480px) {
    Question body padding: 24px 16px
    Option card: full-bleed (no horizontal margin)
    Footer: bottom-anchored, 2 buttons only (Skip + Submit)
    Navigator: drawer with grid layout
    Timer: icon-only by default, tap to expand
}
```

---

## Part 5: Layout Mockup Descriptions

### Mockup A — Desktop (1024px+)

```
+------------------------------------------------------------------+
| [4px yellow accent bar — full width]                              |
+------------------------------------------------------------------+
| Q 12 of 30  [====----progress----====]         [clock] 18:42     |
+------------------------------------------------------------------+
|                                                                    |
|                    QUESTION 12                                     |
|                                                                    |
|    If f(x) = 3x^2 - 5x + 2, what is f(-1)?                     |
|                                                                    |
|                                                                    |
|    +--[A]-- 10 ------------------------------------------------+  |
|    |                                                             |  |
|    +-------------------------------------------------------------+  |
|                                                                    |
|    +--[B]-- 6 -------------------------------------------------+  |
|    |                                                             |  |
|    +-------------------------------------------------------------+  |
|                                                                    |
|    +--[C]-- 8 -------------------------------------------------+  |
|    |                         (selected — yellow border)          |  |
|    +-------------------------------------------------------------+  |
|                                                                    |
|    +--[D]-- 4 -------------------------------------------------+  |
|    |                                                             |  |
|    +-------------------------------------------------------------+  |
|                                                                    |
+------------------------------------------------------------------+
| [1][2][3]...[12]...[30]        [Skip ->]  [Submit & Next ->]     |
|  ^answered  ^current  ^empty    Press A-D to select, Enter submit |
+------------------------------------------------------------------+
```

Key features:
- Timer is right-aligned, uses calm gray text (not boxed/bordered by default)
- Progress bar is a thin track between question counter and timer
- Question card is centered, max 720px wide
- Option cards are full-width within the card, with generous padding
- Footer has nav dots left, actions right, keyboard hint below actions
- Navigator dots use color: green (answered), yellow (current), light gray (unanswered)

### Mockup B — Mobile (480px)

```
+----------------------------------+
| [4px yellow accent bar]          |
+----------------------------------+
| Q 12/30  [====--------]   18:42 |
+----------------------------------+
|                                  |
|  QUESTION 12                     |
|                                  |
|  If f(x) = 3x^2 - 5x + 2,     |
|  what is f(-1)?                  |
|                                  |
|  +--[A]-- 10 -----------------+ |
|  |                             | |
|  +-----------------------------+ |
|                                  |
|  +--[B]-- 6 ------------------+ |
|  |                             | |
|  +-----------------------------+ |
|                                  |
|  +--[C]-- 8 ------------------+ |
|  |      (selected — yellow)    | |
|  +-----------------------------+ |
|                                  |
|  +--[D]-- 4 ------------------+ |
|  |                             | |
|  +-----------------------------+ |
|                                  |
+----------------------------------+
| [Map]    [Skip ->]  [Next ->]    |
+----------------------------------+
```

Key changes from desktop:
- Question counter condensed: "Q 12/30" instead of "Question 12 of 30"
- Timer shows time only, no border/box
- Navigator dots replaced by a "Map" button that opens a slide-up drawer
- Footer has three elements: Map button (left), Skip (center-right), Submit (right)
- Option cards go edge-to-edge with 16px padding
- No keyboard hints

### Mockup C — Question Map Drawer (Mobile)

```
+----------------------------------+
|                                  |
|  (dimmed question behind)        |
|                                  |
+==================================+
|  Question Map           [X]     |
|                                  |
|  [1] [2] [3] [4] [5] [6]       |
|  [7] [8] [9] [10][11][12]      |
|  [13][14][15][16][17][18]       |
|  [19][20][21][22][23][24]       |
|  [25][26][27][28][29][30]       |
|                                  |
|  * green = answered              |
|  * yellow = current              |
|  * gray = unanswered             |
|  * amber dot = flagged           |
|                                  |
|  18 of 30 answered               |
+----------------------------------+
```

The drawer slides up from the bottom (half-screen height), with a semi-transparent overlay behind it. Tapping a number navigates to that question. Tapping X or the overlay closes the drawer.

### Mockup D — Timer States

```
State 1: Normal (>5 min remaining)
    [clock-icon] 18:42          <- gray-700 text, no border

State 2: Collapsible (student hides timer)
    [clock-icon]                <- icon only, tap to reveal time

State 3: Warning (5 min remaining, auto-reveals)
    [clock-icon] 5:00           <- amber text, subtle amber border
    (one-time gentle pulse, then static)

State 4: Critical (<2 min)
    [clock-icon] 1:42           <- red text, red border
    (static — no pulsing animation)
```

### Mockup E — Option States

```
Default:
    +--[A]-- Option text here ---------------------------+
    |  gray border, white bg, gray letter badge          |
    +----------------------------------------------------+

Hover:
    +--[A]-- Option text here ---------------------------+
    |  darker gray border, very light gray bg            |
    +----------------------------------------------------+

Selected:
    +--[A]-- Option text here ---------------------------+
    |  yellow border, faint yellow bg, yellow letter badge|
    +----------------------------------------------------+

Eliminated (strikethrough — future feature):
    +--[A]-- O̶p̶t̶i̶o̶n̶ ̶t̶e̶x̶t̶ ̶h̶e̶r̶e̶ ---------------------------+
    |  light gray border, dimmed text, 50% opacity       |
    +----------------------------------------------------+
```

---

## Part 6: Implementation Priority

### Sprint 1 (Immediate — before next event)
- [ ] H1: Timer anxiety reduction (hideable, amber warning)
- [ ] H2: Progress bar shows answered count
- [ ] H4: Larger option card touch targets
- [ ] H5: Fix disabled button opacity
- [ ] Mobile responsive improvements (media queries)

### Sprint 2 (Next iteration)
- [ ] H3: Question text size increase
- [ ] M1: Mark for Review feature
- [ ] M3: Mobile footer redesign with question map drawer
- [ ] M4: Fade transition between questions
- [ ] L3: Keyboard shortcut hints on desktop

### Sprint 3 (Polish)
- [ ] M2: Option elimination (strikethrough)
- [ ] L1: Micro-feedback animations on selection
- [ ] L2: End-of-module encouragement interstitial
- [ ] Color palette refinement (cooler grays)

---

## Sources

Research was conducted across the following platforms and resources:

- [SAT Bluebook Digital Testing — College Board](https://bluebook.collegeboard.org/)
- [Navigating the Digital SAT Interface — Sparkl](https://sparkl.me/blog/sat/inside-the-student-experience-navigating-the-digital-sat-interface-with-confidence/)
- [Bluebook App 101 — Aara Consultancy](https://aaraconsultancy.com/bluebook-app-101-navigating-the-digital-sat-interface-in-2026/)
- [Bluebook Testing Tools — College Board](https://bluebook.collegeboard.org/students/tools)
- [Khan Academy UX/UI Case Study — Dan (Medium)](https://medium.com/@danielgordonemail/khan-academy-a-ux-ui-case-study-230640d6ee00)
- [Wonder Blocks: Khan Academy's Design System](https://www.designsystems.com/about-wonder-blocks-khan-academys-design-system-and-the-story-behind-it/)
- [Khan Academy Skip Button Update](https://support.khanacademy.org/hc/en-us/articles/26236154715789-Update-Navigate-Questions-at-Your-Own-Pace-with-the-Skip-Button)
- [The Duolingo Handbook: 9 Lessons for Product Design — Everyday UX](https://www.everydayux.net/the-duolingo-handbook-9-lessons-for-designing-world-class-products/)
- [UX Case Study: Duolingo — Usability Geek](https://usabilitygeek.com/ux-case-study-duolingo/)
- [Duolingo Micro-Interactions — Bundu (Medium)](https://medium.com/@Bundu/little-touches-big-impact-the-micro-interactions-on-duolingo-d8377876f682)
- [Duolingo Onboarding UX — UserGuiding](https://userguiding.com/blog/duolingo-onboarding-ux)
- [How Brilliant.org Motivates Learners with Animations — Rive](https://rive.app/blog/how-brilliant-org-motivates-learners-with-rive-animations)
- [Brilliant.org x ustwo](https://ustwo.com/work/brilliant/)
- [IXL Design Principles (PDF)](https://www.ixl.com/research/IXL_Design_Principles.pdf)
- [Typography Accessibility Testing — UXPin](https://www.uxpin.com/studio/blog/ultimate-guide-to-typography-accessibility-testing/)
- [WCAG Color Contrast Guidelines — WebAIM](https://webaim.org/articles/contrast/)
- [Mobile-First UX Design Best Practices 2026 — Trinery Digital](https://www.trinergydigital.com/news/mobile-first-ux-design-best-practices-in-2026)
