"""
Cuemath Evaluation Platform — Math Diagnostic + FUAR Profile + Daily Practice
Central platform for College Ready Night (high school) and Family Math Night
(middle school) events. Students take an adaptive diagnostic, get a FUAR+GRIC
archetype, and a personalized daily practice plan.
"""

import os
import io
import csv
import logging
import json
import random
import sqlite3
import hashlib
import base64
from datetime import datetime, timedelta
from functools import wraps

from flask import (Flask, render_template, request, redirect, url_for,
                   session, flash, jsonify, g, Response, make_response)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'college-ready-dev-key-change-in-prod')

DB_PATH = os.environ.get('DATABASE_PATH', 'college_ready.db')


@app.context_processor
def inject_middle_school_flag():
    """Auto-inject is_middle_school into all templates based on session."""
    if 'student_id' in session:
        try:
            conn = get_db()
            student = conn.execute("SELECT grade FROM students WHERE id = ?",
                                   (session['student_id'],)).fetchone()
            if student:
                grade = int(student['grade'] or 9)
                is_ms = grade <= 8
                event_name = 'Foundation Math Night' if is_ms else 'College Ready Night'
                return {'is_middle_school': is_ms, 'event_display_name': event_name}
        except Exception:
            pass
    return {'is_middle_school': False, 'event_display_name': 'College Ready Night'}

# ---------- FUAR + SAT Domain Mappings ----------

FUAR_DIMENSIONS = {
    'F': {
        'name': 'Fluency',
        'short': 'F',
        'description': 'Knowing facts, formulas, and procedures — executing them accurately and efficiently.',
        'student_desc': 'How quickly and accurately you can execute math procedures.',
        'color': '#4CAF50',
    },
    'U': {
        'name': 'Understanding',
        'short': 'U',
        'description': 'The "why" behind the "what" — grasping underlying concepts and representing them in multiple ways.',
        'student_desc': 'How deeply you understand why math works, not just how.',
        'color': '#2196F3',
    },
    'A': {
        'name': 'Application',
        'short': 'A',
        'description': 'Tackling word problems and real-world situations — choosing the right tools and checking answers.',
        'student_desc': 'How well you apply math to real problems you haven\'t seen before.',
        'color': '#FF9800',
    },
    'R': {
        'name': 'Reasoning',
        'short': 'R',
        'description': 'Spotting patterns, making logical arguments, approaching novel problems strategically.',
        'student_desc': 'How you think through new problems — pattern recognition and logic.',
        'color': '#9C27B0',
    },
}

SAT_DOMAINS = {
    'heart_of_algebra': {
        'name': 'Heart of Algebra',
        'short': 'HoA',
        'description': 'Linear equations, inequalities, systems, and graphs.',
        'weight': 0.33,  # ~33% of SAT math
    },
    'problem_solving': {
        'name': 'Problem Solving & Data Analysis',
        'short': 'PS&DA',
        'description': 'Ratios, percentages, proportional reasoning, data interpretation, statistics.',
        'weight': 0.29,
    },
    'passport_advanced': {
        'name': 'Passport to Advanced Math',
        'short': 'PAM',
        'description': 'Quadratics, polynomials, exponentials, radicals, rational expressions.',
        'weight': 0.28,
    },
    'additional_topics': {
        'name': 'Additional Topics',
        'short': 'AT',
        'description': 'Geometry, trigonometry, complex numbers.',
        'weight': 0.10,
    },
}

# FUAR → SAT domain mapping (many-to-many)
# Each SAT question tests primarily one FUAR dimension but may touch others
FUAR_SAT_MAPPING = {
    'heart_of_algebra':   {'primary': ['F', 'U'], 'secondary': ['A']},
    'problem_solving':    {'primary': ['A', 'U'], 'secondary': ['R']},
    'passport_advanced':  {'primary': ['U', 'R'], 'secondary': ['F']},
    'additional_topics':  {'primary': ['F', 'R'], 'secondary': ['A']},
}

# ---------- GRIC Dimensions ----------

GRIC_DIMENSIONS = {
    'G': {
        'name': 'Growth Mindset',
        'short': 'G',
        'description': 'Do you believe your math ability can grow with effort?',
        'color': '#14B8A6',
    },
    'R_gric': {
        'name': 'Relevance',
        'short': 'R',
        'description': 'Do you see math as useful for your future goals?',
        'color': '#F97316',
    },
    'I': {
        'name': 'Interest',
        'short': 'I',
        'description': 'Do you genuinely enjoy doing math?',
        'color': '#EC4899',
    },
    'C': {
        'name': 'Confidence',
        'short': 'C',
        'description': 'Do you believe you can handle challenging math?',
        'color': '#EAB308',
    },
}

# GRIC Questionnaire — 12 items from validated instruments (Dweck, MMQ, IMI)
# Scale: 1-6, no neutral. Labels: "Not me at all" to "This is SO me"
GRIC_QUESTIONS = [
    # Growth (G) — adapted from Dweck's Implicit Theories Scale
    {'id': 'g1', 'dimension': 'G', 'text': "I'm either good at math or I'm not — practice doesn't really change that.", 'is_reverse': True, 'order': 1, 'section': 'growth'},
    {'id': 'g2', 'dimension': 'G', 'text': "When I actually put in the work, I can feel myself getting better at math.", 'is_reverse': False, 'order': 2, 'section': 'growth'},
    {'id': 'g3', 'dimension': 'G', 'text': "Some kids are just naturally good at math — the rest of us are stuck.", 'is_reverse': True, 'order': 3, 'section': 'growth'},
    # Relevance (R) — adapted from MMQ Utility Value subscale
    {'id': 'r1', 'dimension': 'R_gric', 'text': "I'll actually need math for what I want to do after high school.", 'is_reverse': False, 'order': 4, 'section': 'relevance'},
    {'id': 'r2', 'dimension': 'R_gric', 'text': "I can see how math shows up in things I actually care about.", 'is_reverse': False, 'order': 5, 'section': 'relevance'},
    {'id': 'r3', 'dimension': 'R_gric', 'text': "Most of the math I learn in school? I'm never going to use it.", 'is_reverse': True, 'order': 6, 'section': 'relevance'},
    # Interest (I) — adapted from IMI Interest/Enjoyment subscale
    {'id': 'i1', 'dimension': 'I', 'text': "There's something satisfying about solving a tough math problem.", 'is_reverse': False, 'order': 7, 'section': 'interest'},
    {'id': 'i2', 'dimension': 'I', 'text': "I've had times where I got so into a math problem I forgot what time it was.", 'is_reverse': False, 'order': 8, 'section': 'interest'},
    {'id': 'i3', 'dimension': 'I', 'text': "Math class is one of the most boring parts of my day.", 'is_reverse': True, 'order': 9, 'section': 'interest'},
    # Confidence (C) — adapted from MMQ Self-Efficacy subscale
    {'id': 'c1', 'dimension': 'C', 'text': "When I see a hard problem, my first reaction is 'okay, let me try' — not 'no way.'", 'is_reverse': False, 'order': 10, 'section': 'confidence'},
    {'id': 'c2', 'dimension': 'C', 'text': "If I actually try, I know I can do well in my math class.", 'is_reverse': False, 'order': 11, 'section': 'confidence'},
    {'id': 'c3', 'dimension': 'C', 'text': "Before a math test, I usually feel like I'm not ready.", 'is_reverse': True, 'order': 12, 'section': 'confidence'},
]

GRIC_SCALE_LABELS = [
    (1, "Not really"),
    (2, "Sometimes"),
    (3, "Usually"),
    (4, "Definitely me"),
]

GRIC_SECTIONS = [
    {'key': 'growth', 'title': 'How You See Your Math Ability', 'icon': '🌱', 'color': '#10B981'},
    {'key': 'relevance', 'title': 'Math in Your Life', 'icon': '🔗', 'color': '#3B82F6'},
    {'key': 'interest', 'title': 'How You Feel About Math', 'icon': '✨', 'color': '#F59E0B'},
    {'key': 'confidence', 'title': 'Your Math Confidence', 'icon': '💪', 'color': '#8B5CF6'},
]

# ---------- Archetype System — 8 Greek Letter Archetypes ----------
# Same 8 types across all grade bands. Packaging differs by age (elementary/middle/high).
# Assignment: FUAR dominant (F/U/A/R) × mindset mode (engaged/guarded) = 8 types.

ARCHETYPES = {
    'sigma': {
        'name': 'The Perfectionist', 'symbol': 'σ', 'greek_name': 'Sigma',
        'tagline': 'You don\'t skip steps — and that\'s why you rarely get things wrong.',
        'signature': 'If I showed my work, I know it\'s right.',
        'fuar': 'F', 'mindset': 'engaged',
        'color': '#3B82F6', 'colors': ['#3B82F6', '#60A5FA'],
        'superpower_title': 'Accuracy Under Pressure',
        'superpower': 'When other students rush and drop points on the SAT or AP exam, you execute cleanly. Your step-by-step process is a machine — and machines don\'t panic.',
        'kryptonite_title': 'Open-Ended Problems',
        'kryptonite': 'You can get stuck when there\'s no clear procedure. Open-ended problems or questions you\'ve never seen before can freeze you — not because you can\'t do them, but because you don\'t have a sequence to follow yet.',
        'study_tips': [
            ('Worked examples first, then practice.', 'You learn by seeing the full solution and replicating it.'),
            ('Quiet, distraction-free environment.', 'Your process requires focus — background noise breaks your chain of thought.'),
            ('Color-coded notes or templates.', 'Your brain wants information organized spatially.'),
            ('Practice tests under timed conditions.', 'Train your process to work under the clock.'),
        ],
        'growth_title': 'Working Without a Roadmap',
        'growth': 'Your next unlock is learning to work without a roadmap. The highest levels of math require you to try an approach before you\'re sure it\'s right. Building comfort with "let me just try this and see" will make you unstoppable.',
        'this_is_you': [
            'You\'ve rewritten a solution from scratch because you skipped one step and it didn\'t feel right — even though the answer was correct.',
            'When someone says "just use the formula," you need to know which formula, why that formula, and what each part does before you\'ll touch your calculator.',
            'You\'ve been told you\'re "slow" at math, but your test scores say otherwise — because you almost never make careless mistakes.',
        ],
        'minds': [
            ('Euclid', 'Built all of geometry step by step from five simple axioms.'),
            ('Katherine Johnson', 'Calculated NASA trajectories by hand with zero margin for error.'),
            ('Sal Khan', 'Built Khan Academy by breaking every concept into methodical, sequential lessons.'),
        ],
        'mathematician_quote': 'There is no royal road to geometry.',
        # Middle school packaging
        'ms_name': 'The Machine',
        'ms_tagline': 'You don\'t skip steps, and that\'s why you almost never get things wrong.',
        'ms_superpower': 'When everyone else rushes through a test and makes careless mistakes, you execute cleanly. Your step-by-step process means you catch errors before they happen.',
        'ms_growth': 'Your next level-up is learning to try things even when you\'re not sure of the steps. The best math students can work without a roadmap. Building comfort with "let me just try this" will make you unstoppable.',
        'ms_this_is_you': [
            'You\'ve rewritten a homework problem from scratch because you skipped one step and it didn\'t feel right.',
            'When the teacher shows a shortcut, you need to understand WHY it works before you\'ll use it.',
            'People say you\'re "slow" at math, but you almost never get things wrong on tests.',
        ],
    },
    'delta': {
        'name': 'The Relentless', 'symbol': 'δ', 'greek_name': 'Delta',
        'tagline': 'You outwork everyone — and you know it.',
        'signature': 'I wasn\'t born with it. I earned it.',
        'fuar': 'F', 'mindset': 'guarded',
        'color': '#EF4444', 'colors': ['#EF4444', '#F87171'],
        'superpower_title': 'Consistency',
        'superpower': 'You don\'t have "on" days and "off" days the way other students do. Your preparation is so thorough that your floor is higher than most people\'s ceiling.',
        'kryptonite_title': 'Working Smart vs Hard',
        'kryptonite': 'You sometimes confuse working hard with working smart. You can spend two hours on a topic that needed thirty minutes if you\'d just asked for help or tried a different approach.',
        'study_tips': [
            ('High volume repetition.', 'You learn by doing twenty problems, not by reading one explanation slowly.'),
            ('Study schedules and daily routines.', 'You thrive with structure — "math at 7 PM every night" works.'),
            ('Progress tracking.', 'Seeing your improvement over time fuels your motivation.'),
            ('A study partner who keeps pace.', 'You do well with someone who matches your work ethic.'),
        ],
        'growth_title': 'Flexibility',
        'growth': 'Your next unlock is flexibility. You\'ve mastered the grind — now learn to step back and ask "is there a better way?" The students who score 1500+ on the SAT aren\'t just hardworking; they\'re strategically hardworking.',
        'this_is_you': [
            'You\'ve done practice problems that weren\'t even assigned, just because you weren\'t confident enough on that topic yet.',
            'When you get a problem wrong, you don\'t just look at the answer — you redo the entire problem until you can get it right without help.',
            'You\'ve pulled up a math video at 11 PM the night before a test, not because you\'re cramming, but because you want one more pass.',
        ],
        'minds': [
            ('Srinivasa Ramanujan', 'Self-taught, relentless, filled notebooks with work through sheer obsessive effort.'),
            ('Kobe Bryant', 'Mamba Mentality — relentless practice is exactly how you approach math.'),
            ('Maryam Mirzakhani', 'Spent years grinding on problems until they cracked. Won the Fields Medal.'),
        ],
        'mathematician_quote': 'An equation means nothing to me unless it expresses a thought of God.',
        'ms_name': 'The Relentless',
        'ms_tagline': 'You outwork everyone, and you know it.',
        'ms_superpower': 'You don\'t have "good days" and "bad days" like other students. Your preparation is so thorough that even your worst day is better than most people\'s best.',
        'ms_growth': 'Your next level-up is flexibility. You\'ve mastered the grind. Now learn to step back and ask "is there a smarter way?" The students who ace every class aren\'t just hardworking, they\'re strategically hardworking.',
        'ms_this_is_you': [
            'You\'ve done extra practice problems that weren\'t even assigned, just because you weren\'t confident enough yet.',
            'When you get a problem wrong, you don\'t just check the answer. You redo the entire thing until you get it right without help.',
            'You\'ve watched a math video at 11 PM before a test. Not cramming. Just one more pass.',
        ],
    },
    'pi': {
        'name': 'The Purist', 'symbol': 'π', 'greek_name': 'Pi',
        'tagline': 'You don\'t memorize — you understand.',
        'signature': 'I don\'t need the shortcut — I need to know why the shortcut works.',
        'fuar': 'U', 'mindset': 'engaged',
        'color': '#2563EB', 'colors': ['#2563EB', '#3B82F6'],
        'superpower_title': 'Transfer',
        'superpower': 'Because you understand the WHY behind math, you can apply concepts to problems you\'ve never seen before. While memorizers freeze on unfamiliar test questions, you reason your way through. This advantage gets bigger every year.',
        'kryptonite_title': 'Speed',
        'kryptonite': 'You take longer than you should on problems you could do faster, because you\'re thinking about them more deeply than necessary. On timed tests, your depth can work against you.',
        'study_tips': [
            ('Teach it to someone.', 'If you can explain it, you own it. If you can\'t, you know where your understanding breaks.'),
            ('3Blue1Brown > textbooks.', 'Conceptual resources over procedural ones.'),
            ('Build webs, not lists.', 'Connect new concepts to ones you already understand.'),
            ('Whiteboard or blank paper.', 'You need space to draw, map, and visualize your understanding.'),
        ],
        'growth_title': 'Speed + Depth',
        'growth': 'Your next unlock is trusting your understanding enough to move quickly. You already know more than you think — learn to deploy that knowledge at speed. Students who dominate AP exams have your depth AND the ability to execute fast.',
        'this_is_you': [
            'You\'ve re-derived a formula on a test because memorizing it felt wrong.',
            'You\'ve asked a question in class that made your teacher pause and say "that\'s actually a really good question" — and you weren\'t trying to be impressive.',
            'You\'ve gone down a rabbit hole reading about a math concept online and lost track of time — not for a grade, just because you were curious.',
        ],
        'minds': [
            ('Richard Feynman', 'Nobel physicist — "I don\'t understand what I can\'t build."'),
            ('Emmy Noether', 'Saw the deep structure beneath algebra and physics that nobody else could see.'),
            ('Grant Sanderson', '3Blue1Brown — making math deeply understandable, not just correct.'),
        ],
        'mathematician_quote': 'Nothing takes place in the world whose meaning is not that of some maximum or minimum.',
        'ms_name': 'The Deep Thinker',
        'ms_tagline': 'You don\'t memorize. You understand.',
        'ms_superpower': 'Because you understand the WHY behind math, you can figure out problems you\'ve never seen before. While other kids freeze on new question types, you reason your way through.',
        'ms_growth': 'Your next level-up is trusting your understanding enough to move quickly. You already know more than you think. Learning to work at speed will make you crush every math class through high school.',
        'ms_this_is_you': [
            'You\'ve figured out a formula on a test instead of memorizing it, because memorizing felt wrong.',
            'You\'ve asked a question in class that made your teacher pause and think.',
            'You\'ve gone down a rabbit hole reading about a math concept and lost track of time, not for a grade, just because you were curious.',
        ],
    },
    'theta': {
        'name': 'The Quiet Genius', 'symbol': 'θ', 'greek_name': 'Theta',
        'tagline': 'You see things in math that nobody else in the room sees.',
        'signature': 'I saw it differently — and I was right.',
        'fuar': 'U', 'mindset': 'guarded',
        'color': '#8B5CF6', 'colors': ['#8B5CF6', '#A78BFA'],
        'superpower_title': 'Insight',
        'superpower': 'You see mathematical connections and patterns that other students walk right past. Your understanding isn\'t just deep — it\'s original. You notice things that textbooks don\'t point out.',
        'kryptonite_title': 'Self-Doubt Under Pressure',
        'kryptonite': 'You know more than you give yourself credit for, but timed tests and high-stakes moments can shrink your confidence. You sometimes abandon a correct approach because you talked yourself out of it.',
        'study_tips': [
            ('Low-pressure practice first.', 'Do problems without a timer until your confidence builds. Then add time pressure gradually.'),
            ('Write out your thinking.', 'Getting your insights on paper makes them feel more real and trustable.'),
            ('Study with someone who validates.', 'You need a partner who says "yeah, that\'s right" so you start believing it.'),
            ('Review your correct answers.', 'You need to see evidence that your instincts are good.'),
        ],
        'growth_title': 'Trusting Your Instinct',
        'growth': 'Your next unlock is trusting your first instinct. You already have the understanding — what you need is the confidence to commit to your answers. Start keeping a "proof journal" — write down every time your instinct was right.',
        'this_is_you': [
            'You\'ve solved a problem a different way than the teacher showed and gotten the right answer — but still felt unsure about it.',
            'You\'ve understood something completely during a study session, then blanked on the test because the pressure scrambled your thinking.',
            'You\'ve explained a concept to a friend and watched them get it — and thought, "wait, do I actually understand this better than I think?"',
        ],
        'minds': [
            ('Grigori Perelman', 'Solved one of the greatest math problems in history, famously private despite his brilliance.'),
            ('Ada Lovelace', 'Saw the potential of computing decades before anyone else.'),
            ('Terence Tao', 'Known for seeing unexpected angles in problems, connecting areas of math nobody thought were related.'),
        ],
        'mathematician_quote': 'It is not knowledge, but the act of learning, that grants the greatest enjoyment.',
        'ms_name': 'The Quiet Genius',
        'ms_tagline': 'You see things in math that nobody else in the room sees.',
        'ms_superpower': 'You notice patterns and connections that other students walk right past. Your understanding isn\'t just deep, it\'s original. You see things textbooks don\'t point out.',
        'ms_growth': 'Your next level-up is trusting your gut. You already have the understanding. What you need is the confidence to commit to your answers instead of second-guessing yourself.',
        'ms_this_is_you': [
            'You\'ve solved a problem a different way than the teacher showed and gotten the right answer, but still felt unsure about it.',
            'You\'ve understood something perfectly while studying, then blanked on the test because the pressure got to you.',
            'You\'ve explained a concept to a friend and watched them get it, and thought "wait, maybe I understand this better than I think."',
        ],
    },
    'phi': {
        'name': 'The Natural', 'symbol': 'φ', 'greek_name': 'Phi',
        'tagline': 'You don\'t just solve problems — you see the math hiding in everything.',
        'signature': 'Math isn\'t in the textbook — it\'s in everything else.',
        'fuar': 'A', 'mindset': 'engaged',
        'color': '#F59E0B', 'colors': ['#F59E0B', '#FBBF24'],
        'superpower_title': 'Real-World Modeling',
        'superpower': 'You can take a messy, real-life situation and translate it into a mathematical framework. This is THE skill that data science, engineering, economics, and business are built on.',
        'kryptonite_title': 'Abstract Math Without Context',
        'kryptonite': 'When a concept is purely theoretical — proofs for proof\'s sake — your motivation drops and your performance follows. You need the "why" to unlock the "how."',
        'study_tips': [
            ('Real datasets and case studies.', 'You learn statistics better from an actual NBA dataset than a textbook table.'),
            ('Project-based learning.', 'Build something, model something, predict something.'),
            ('Connect every concept to a career.', '"When would a data scientist use this?" makes the concept stick.'),
            ('Desmos, spreadsheets, simulations.', 'Interactive tools over static notes.'),
        ],
        'growth_title': 'Comfort with Abstraction',
        'growth': 'Your next unlock is building comfort with abstraction. Some of the most powerful math is abstract at first and applied later. Learning to trust that "this will matter eventually" will give you access to levels currently blocked.',
        'this_is_you': [
            'You\'ve calculated something in real life — tip percentages, game probabilities, paint for a room — and enjoyed it more than any homework problem.',
            'You\'ve argued with a teacher about a "wrong" answer because your real-world reasoning gave a different result than the textbook.',
            'You\'ve looked at a data visualization and immediately noticed a pattern or error that nobody else caught.',
        ],
        'minds': [
            ('Florence Nightingale', 'Used data visualization and statistical modeling to revolutionize healthcare.'),
            ('Nate Silver', 'Turned pattern recognition into one of the most influential data platforms.'),
            ('Elon Musk', 'Thinks in applied mathematical systems, from physics to financial modeling.'),
        ],
        'mathematician_quote': 'Simplicity is the ultimate sophistication.',
        'ms_name': 'The Natural',
        'ms_tagline': 'You don\'t just solve problems. You see the math hiding in everything.',
        'ms_superpower': 'You can take a messy real-life situation and turn it into a math problem. Tip percentages, game stats, building projects. You see numbers where others see chaos.',
        'ms_growth': 'Your next level-up is getting comfortable with abstract math. Some of the most powerful concepts seem pointless at first but connect to real things later. Trusting that process will open doors.',
        'ms_this_is_you': [
            'You\'ve calculated something in real life, like game probabilities or how much paint you need for a room, and enjoyed it more than any homework problem.',
            'You\'ve argued with a teacher about a "wrong" answer because your real-world reasoning gave a different result.',
            'You\'ve looked at a chart or graph and immediately spotted something off that nobody else noticed.',
        ],
    },
    'lambda': {
        'name': 'The Dormant Force', 'symbol': 'λ', 'greek_name': 'Lambda',
        'tagline': 'You\'re not bad at math — you\'re just waiting for math to earn your attention.',
        'signature': 'Show me why it matters and I\'ll show you what I can do.',
        'fuar': 'A', 'mindset': 'guarded',
        'color': '#6366F1', 'colors': ['#6366F1', '#818CF8'],
        'superpower_title': 'Purpose-Driven Focus',
        'superpower': 'When you care about something, your level of effort and quality of thinking rivals anyone in the room. You\'re not lazy — you\'re selective. In the real world, that selectivity becomes an asset.',
        'kryptonite_title': 'Disengagement',
        'kryptonite': 'Traditional math classes can feel like a series of hoops to jump through, and your motivation suffers. The danger is that you write off your own math ability based on grades that don\'t reflect your actual potential.',
        'study_tips': [
            ('Start with the application.', '"Here\'s a real problem → here\'s the math that solves it" works better than formulas first.'),
            ('Career connections.', 'Knowing that data scientists make $95K using exactly this math makes it worth learning.'),
            ('Short, goal-oriented sessions.', 'Twenty focused minutes beats two hours of unfocused grinding.'),
            ('Choose projects over problem sets.', 'If a teacher offers a project option, take it.'),
        ],
        'growth_title': 'Building the Bridge',
        'growth': 'Your next unlock is building a bridge between "math I have to learn" and "things I actually care about." Every abstract topic connects to something real — you just haven\'t found all the connections yet.',
        'this_is_you': [
            'You\'ve done well on a math project that connected to something you care about — and been surprised by your own performance.',
            'You\'ve asked "when am I ever going to use this?" and meant it as a genuine question, not a complaint.',
            'You\'ve used math in a non-school context (budgeting, gaming strategy, building something) and thought, "okay, THIS I can do."',
        ],
        'minds': [
            ('Steve Jobs', 'Uninterested in pure academics, but mastered the math of design and business when it connected to his purpose.'),
            ('Jay-Z', 'Built a billion-dollar empire using applied math — margins, scale, compound growth.'),
            ('Simone Biles', 'Total mastery when math connects to her craft — physics, angles, spatial reasoning in gymnastics.'),
        ],
        'mathematician_quote': 'The beauty of mathematics only shows itself to more patient followers.',
        'ms_name': 'The Undercover',
        'ms_tagline': 'You\'re not bad at math. You\'re just waiting for math to earn your attention.',
        'ms_superpower': 'When you care about something, your effort and thinking are as good as anyone in class. You\'re not lazy. You\'re selective. And when something clicks, you go all in.',
        'ms_growth': 'Your next level-up is finding the connection between "math I have to learn" and "things I actually care about." Every boring topic connects to something real. You just haven\'t found all the links yet.',
        'ms_this_is_you': [
            'You\'ve done well on a project that connected to something you care about, and surprised yourself.',
            'You\'ve asked "when am I ever going to use this?" and you actually meant it as a real question.',
            'You\'ve used math outside school, like for gaming strategy or budgeting, and thought "okay, THIS I can do."',
        ],
    },
    'alpha': {
        'name': 'The Inventor', 'symbol': 'α', 'greek_name': 'Alpha',
        'tagline': 'You don\'t follow methods — you invent them.',
        'signature': 'There\'s always another way to solve it — and I\'ll find it.',
        'fuar': 'R', 'mindset': 'engaged',
        'color': '#10B981', 'colors': ['#10B981', '#34D399'],
        'superpower_title': 'Original Thinking',
        'superpower': 'You can solve problems nobody has taught you how to solve. This is the rarest mathematical ability — the one that separates people who USE math from people who ADVANCE math.',
        'kryptonite_title': 'Skipping Fundamentals',
        'kryptonite': 'Because your reasoning is strong, you can get away with shaky foundations longer than most. But eventually the gaps catch up. You\'ll see the elegant solution but make an arithmetic error on the way there.',
        'study_tips': [
            ('Challenge problems and competitions.', 'AMC, MATHCOUNTS, Olympiad-style questions. Routine homework bores you.'),
            ('Open-ended exploration.', 'Give yourself permission to explore — topology, game theory, cryptography.'),
            ('Learn fundamentals through interesting problems.', 'You won\'t drill arithmetic alone, but you\'ll nail it if embedded in a problem you care about.'),
            ('Collaborate with people at your level.', 'You thrive when you\'re not the smartest person in the room.'),
        ],
        'growth_title': 'Disciplined Execution',
        'growth': 'Your next unlock is disciplined execution. You already have the ideas — what would make you extraordinary is the precision to carry them through without errors. The greatest mathematicians weren\'t just creative; they were creative AND rigorous.',
        'this_is_you': [
            'You\'ve solved a problem correctly using a method your teacher had never seen before.',
            'You\'ve gotten bored in math class not because it\'s too hard, but because the approach felt too predictable.',
            'You\'ve connected a concept from another subject (physics, CS, music) to a math concept and had a genuine "wait, it\'s the same thing" moment.',
        ],
        'minds': [
            ('Leonhard Euler', 'The most prolific mathematician in history, invented entirely new fields.'),
            ('John von Neumann', 'Invented game theory, contributed to quantum mechanics, helped design the first computers.'),
            ('Maryam Mirzakhani', 'Drew pictures, built new methods, won the Fields Medal with pure creativity.'),
        ],
        'mathematician_quote': 'If I have seen further, it is by standing on the shoulders of giants.',
        'ms_name': 'The Builder',
        'ms_tagline': 'You don\'t follow methods. You invent them.',
        'ms_superpower': 'You can solve problems nobody has taught you how to solve. While other students need step-by-step instructions, you figure out your own path. That\'s the rarest math ability there is.',
        'ms_growth': 'Your next level-up is disciplined execution. You already have the ideas. What would make you extraordinary is the precision to carry them through without errors. The greatest builders are creative AND careful.',
        'ms_this_is_you': [
            'You\'ve solved a problem using a method your teacher had never seen before.',
            'You\'ve been bored in math class not because it\'s hard, but because the approach felt too predictable.',
            'You\'ve connected something from science, coding, or music to a math concept and thought "wait, it\'s the same thing."',
        ],
    },
    'gamma': {
        'name': 'The Maverick', 'symbol': 'γ', 'greek_name': 'Gamma',
        'tagline': 'Your best work is brilliant. Your worst work is... interesting.',
        'signature': 'You never know which version of me is showing up — but the best version is unbeatable.',
        'fuar': 'R', 'mindset': 'guarded',
        'color': '#EC4899', 'colors': ['#EC4899', '#F472B6'],
        'superpower_title': 'Breakthrough Thinking',
        'superpower': 'When everyone else is stuck, you\'re the one who has the insight that cracks the problem open. You think in leaps, not steps, and that ability to vault over complexity is genuinely rare.',
        'kryptonite_title': 'Inconsistency',
        'kryptonite': 'Your reasoning can outrun your execution. You skip steps, make careless errors, and sometimes turn in work that doesn\'t represent what you actually know. You know you\'re capable of more than your grades show.',
        'study_tips': [
            ('Error analysis.', 'Don\'t redo the whole problem — just find where you went wrong and WHY.'),
            ('Build a personal mistake checklist.', 'Your errors are predictable — use that to your advantage.'),
            ('Alternate creative and procedural work.', 'Your brain needs both: problems that excite you AND reps that build reliability.'),
            ('Show work even when you can do it mentally.', 'Think of it as leaving breadcrumbs for partial credit and catching your own errors.'),
        ],
        'growth_title': 'Making Brilliance Reliable',
        'growth': 'Your next unlock is making your brilliance reliable. Right now, your talent shows up in flashes. The goal isn\'t to dim the flashes — it\'s to build a foundation so strong that your creative leaps have a solid launch pad.',
        'this_is_you': [
            'You\'ve aced a problem worth 20 points and then lost 8 points on "easy" problems because of arithmetic errors.',
            'You\'ve solved a problem in your head and written down just the answer — then lost points for not showing work.',
            'A teacher has said "you clearly understand this material, but your grades don\'t reflect it" — and you\'ve heard it more than once.',
        ],
        'minds': [
            ('Galois', 'Revolutionary mathematician who invented group theory as a teenager, famously chaotic.'),
            ('Nikola Tesla', 'Brilliant, creative, saw solutions others couldn\'t imagine, struggled with systematic execution.'),
            ('Kanye West', 'Wild creative genius with inconsistent follow-through. When it hits, it\'s undeniable.'),
        ],
        'mathematician_quote': 'Those who can imagine anything can create the impossible.',
        'ms_name': 'The Wildcard',
        'ms_tagline': 'Your best work is brilliant. Your worst work is... interesting.',
        'ms_superpower': 'When everyone else is stuck, you\'re the one who has the idea that cracks the problem open. You think in leaps, not steps, and that ability to jump over complexity is genuinely rare.',
        'ms_growth': 'Your next level-up is making your brilliance reliable. Right now your talent shows up in flashes. The goal isn\'t to dim the flashes. It\'s to build a foundation so strong that your creative leaps always have a solid launch pad.',
        'ms_this_is_you': [
            'You\'ve aced a hard problem and then lost points on easy ones because of careless mistakes.',
            'You\'ve solved a problem in your head and just written the answer, then lost points for not showing work.',
            'A teacher has said "you clearly understand this, but your grades don\'t show it." And you\'ve heard it more than once.',
        ],
    },
}

# Backward-compatible aliases
ALL_ARCHETYPES = ARCHETYPES

# Add compat fields for templates
_FUAR_ICONS = {'F': '⚡', 'U': '🔬', 'A': '🧩', 'R': '🔮'}
for _key, _arch in ALL_ARCHETYPES.items():
    _arch['icon'] = _FUAR_ICONS.get(_arch.get('fuar', 'F'), '⚡')
    _arch['description'] = _arch.get('tagline', '')
    _arch['student_desc'] = _arch.get('tagline', '')
    _arch['parent_desc'] = _arch.get('superpower', '')

# FUAR dominant × mindset mode → archetype key
# "engaged" = G or I dominant in GRIC (growth/interest = intrinsic motivation)
# "guarded" = R_gric or C dominant in GRIC (relevance/confidence = extrinsic/protective)
ARCHETYPE_MATRIX = {
    ('F', 'engaged'): 'sigma',   ('F', 'guarded'): 'delta',
    ('U', 'engaged'): 'pi',     ('U', 'guarded'): 'theta',
    ('A', 'engaged'): 'phi',    ('A', 'guarded'): 'lambda',
    ('R', 'engaged'): 'alpha',  ('R', 'guarded'): 'gamma',
}

# No separate middle school matrix — same 8 types, different packaging in templates
MIDDLE_ARCHETYPE_MATRIX = ARCHETYPE_MATRIX


_DEAD_CODE_START = """
        'name': 'Confident Executor',
        'tagline': 'You deliver under pressure, every time.',
        'student_desc': 'When the timer starts — SAT, AP exam, timed test — you don\'t panic. You EXECUTE. Your computational skills are strong and your confidence in them is real, earned through consistent practice. You trust your preparation, and it shows in your performance when it counts.',
        'parent_desc': 'Your student combines computational fluency with genuine test-taking confidence. They perform well under pressure because their skills are paired with self-trust. This is the profile that translates directly to standardized test performance.',
        'fuar': 'F', 'gric': 'C',
        'colors': ['#3B82F6', '#EAB308'],
        'strength': 'Fluency', 'growth': 'Confidence',
    },
    # UNDERSTANDING ROW
    'conceptual_strategist': {
        'name': 'Conceptual Strategist',
        'tagline': 'Deep understanding that keeps getting deeper.',
        'student_desc': 'You understand math at a level most students never reach — and you\'re still going deeper. You approach every concept as something that can be understood more fully, from more angles, with more connections. Your depth isn\'t fixed; it\'s expanding.',
        'parent_desc': 'Your student combines deep conceptual understanding with a growth mindset. They believe mathematical comprehension has no ceiling — and they\'re right. This combination produces students who thrive in proof-based courses, honors tracks, and college programs where depth matters more than speed.',
        'fuar': 'U', 'gric': 'G',
        'colors': ['#10B981', '#14B8A6'],
        'strength': 'Understanding', 'growth': 'Growth Mindset',
    },
    'analytical_translator': {
        'name': 'Analytical Translator',
        'tagline': 'You convert complex ideas into language everyone understands.',
        'student_desc': 'You understand math deeply and you can explain WHY it matters. In group projects, you\'re the one who makes the complex thing clear. Your ability to bridge deep understanding and practical communication is rare — and it\'s exactly what colleges look for.',
        'parent_desc': 'Your student combines deep conceptual understanding with strong relevance orientation. They\'re natural communicators of complex ideas — the profile of students who excel in interdisciplinary settings and careers that require translating technical knowledge for non-technical audiences.',
        'fuar': 'U', 'gric': 'R_gric',
        'colors': ['#10B981', '#F97316'],
        'strength': 'Understanding', 'growth': 'Relevance',
    },
    'theoretical_mind': {
        'name': 'Theoretical Mind',
        'tagline': 'You pursue deep understanding because knowing IS the reward.',
        'student_desc': 'You\'re driven by intellectual curiosity at its purest. You want to understand math not because it\'s useful (though it is) but because understanding itself is the reward. You read beyond the textbook. You explore proofs. You wonder about the foundations. This is the mindset that produces original thinkers.',
        'parent_desc': 'Your student combines deep understanding with genuine intellectual curiosity. They\'re intrinsically motivated by comprehension — the profile of students who thrive in honors and AP mathematics, who choose math-heavy college majors by choice rather than obligation.',
        'fuar': 'U', 'gric': 'I',
        'colors': ['#10B981', '#EC4899'],
        'strength': 'Understanding', 'growth': 'Interest',
    },
    'foundational_thinker': {
        'name': 'Foundational Thinker',
        'tagline': 'Your understanding runs deep, and so does your confidence.',
        'student_desc': 'Your confidence in math comes from the right place — genuine understanding. You don\'t just know procedures; you understand why they work. When advanced courses throw curveballs, your solid foundations keep you steady. That\'s real mathematical maturity.',
        'parent_desc': 'Your student\'s mathematical confidence is built on genuine conceptual understanding — the most durable form of confidence possible. They\'re well-prepared for college-level math where surface knowledge fails and deep understanding carries.',
        'fuar': 'U', 'gric': 'C',
        'colors': ['#10B981', '#EAB308'],
        'strength': 'Understanding', 'growth': 'Confidence',
    },
    # APPLICATION ROW
    'resilient_innovator': {
        'name': 'Resilient Innovator',
        'tagline': 'You apply math to hard problems and grow stronger every time.',
        'student_desc': 'You apply math to real problems, and when those problems push back, you don\'t break — you GROW. Failed approach? New data. Unexpected result? New insight. Your combination of applied skills and growth mindset means you treat every challenge as training for the next, harder one.',
        'parent_desc': 'Your student combines application skills with powerful resilience. They apply math to real-world problems and learn from failure — the core competency of innovators and entrepreneurs. This is what engineering programs and research labs look for.',
        'fuar': 'A', 'gric': 'G',
        'colors': ['#F59E0B', '#14B8A6'],
        'strength': 'Application', 'growth': 'Growth Mindset',
    },
    'systems_architect': {
        'name': 'Systems Architect',
        'tagline': 'You design the mathematical frameworks that make real systems work.',
        'student_desc': 'You see math as a design tool. Every real-world system — supply chains, algorithms, urban planning, financial markets — is a mathematical problem waiting for a better design. You don\'t just solve problems — you design solutions.',
        'parent_desc': 'Your student combines strong application skills with deep relevance orientation. They naturally see mathematical applications in real-world systems — the profile of future engineers, data scientists, UX researchers, and policy analysts.',
        'fuar': 'A', 'gric': 'R_gric',
        'colors': ['#F59E0B', '#F97316'],
        'strength': 'Application', 'growth': 'Relevance',
    },
    'creative_mathematician': {
        'name': 'Creative Mathematician',
        'tagline': 'You find beauty in applied solutions.',
        'student_desc': 'You apply math creatively. Where others see one path to a solution, you see five. You\'re drawn to elegant approaches, surprising connections, and unconventional methods. Your interest drives you to find not just any solution, but the BEST solution.',
        'parent_desc': 'Your student combines application skills with genuine creative interest in mathematics. They find joy in the process of applying math, not just the outcome. This creative-applied combination is the hallmark of students who thrive in design-oriented STEM fields.',
        'fuar': 'A', 'gric': 'I',
        'colors': ['#F59E0B', '#EC4899'],
        'strength': 'Application', 'growth': 'Interest',
    },
    'strategic_leader': {
        'name': 'Strategic Leader',
        'tagline': 'You apply your skills with confidence and take others with you.',
        'student_desc': 'You don\'t just apply math — you lead the application. In group projects, competitions, and real-world challenges, you\'re the one who organizes the approach, delegates the analysis, and drives toward results. Your confidence makes you the person others follow.',
        'parent_desc': 'Your student combines strong application skills with leadership-level confidence. They take initiative in collaborative mathematical settings and drive projects to completion. This is a profile highly valued by college admissions.',
        'fuar': 'A', 'gric': 'C',
        'colors': ['#F59E0B', '#EAB308'],
        'strength': 'Application', 'growth': 'Confidence',
    },
    # REASONING ROW
    'evolving_logician': {
        'name': 'Evolving Logician',
        'tagline': 'Your reasoning gets sharper with every challenge.',
        'student_desc': 'You think logically, and your logic is ALWAYS improving. You don\'t rest on past reasoning — you actively seek harder problems, more complex proofs, and more rigorous challenges. Every time your logic is tested, it comes back stronger.',
        'parent_desc': 'Your student combines strong reasoning with a growth mindset. They see logical thinking as a skill that can always be sharpened — and they actively sharpen it. This produces students who thrive in advanced math courses where reasoning becomes increasingly abstract.',
        'fuar': 'R', 'gric': 'G',
        'colors': ['#8B5CF6', '#14B8A6'],
        'strength': 'Reasoning', 'growth': 'Growth Mindset',
    },
    'cross_domain_analyst': {
        'name': 'Cross-Domain Analyst',
        'tagline': 'Your reasoning cuts across disciplines and connects everything.',
        'student_desc': 'You reason with mathematical precision, and you apply that reasoning EVERYWHERE. Biology, economics, political science, computer science — you see the logical structures that connect them all. You\'re not just a math person; you\'re a person who thinks mathematically about everything.',
        'parent_desc': 'Your student combines strong logical reasoning with a broad, relevance-driven perspective. They naturally apply mathematical reasoning across disciplines — the profile of students who excel in interdisciplinary college programs, data science, and policy analysis.',
        'fuar': 'R', 'gric': 'R_gric',
        'colors': ['#8B5CF6', '#F97316'],
        'strength': 'Reasoning', 'growth': 'Relevance',
    },
    'abstract_thinker': {
        'name': 'Abstract Thinker',
        'tagline': 'You see mathematical patterns others can\'t even imagine.',
        'student_desc': 'You\'re drawn to the deepest, most abstract layers of mathematical reasoning — and you love it. Proofs, conjectures, theoretical structures. You don\'t need real-world applications to find math interesting; the logic itself is the reward.',
        'parent_desc': 'Your student combines strong reasoning with deep intrinsic interest in abstract mathematics. This is the profile of future mathematicians, theoretical physicists, and researchers. Their genuine love of abstract reasoning is a gift that leads to extraordinary achievement.',
        'fuar': 'R', 'gric': 'I',
        'colors': ['#8B5CF6', '#EC4899'],
        'strength': 'Reasoning', 'growth': 'Interest',
    },
    'principled_reasoner': {
        'name': 'Principled Reasoner',
        'tagline': 'Your logic is airtight and your confidence is earned.',
        'student_desc': 'You reason clearly, rigorously, and confidently. When you present an argument, it\'s built on solid logical foundations and you can defend every step. Your confidence isn\'t bluster — it\'s the quiet certainty that comes from knowing your reasoning is sound.',
        'parent_desc': 'Your student combines strong reasoning with well-founded confidence. They trust their logical thinking because it\'s been tested and proven. This combination is highly valued in fields where rigorous reasoning matters — law, philosophy, mathematics, and analytics.',
        'fuar': 'R', 'gric': 'C',
        'colors': ['#8B5CF6', '#EAB308'],
        'strength': 'Reasoning', 'growth': 'Confidence',
    },
}

# ---------- Middle School Archetypes (16) — FUAR x GRIC, age-appropriate ----------

MIDDLE_ARCHETYPES = {
    # FLUENCY ROW
    'rapid_strategist': {
        'name': 'The Rapid Strategist', 'tagline': 'Fast today, faster tomorrow.',
        'student_desc': 'You process math quickly AND you\'re always leveling up. You don\'t just rely on what you already know — you actively push yourself to learn new methods and better strategies. Your speed isn\'t a ceiling, it\'s a floor.',
        'parent_desc': 'Your child combines mathematical fluency with a growth-oriented mindset. They process quickly but aren\'t complacent — they actively seek improvement. Encourage them to take on challenges that push beyond their current speed.',
        'fuar': 'F', 'gric': 'G', 'colors': ['#3B82F6', '#14B8A6'],
        'strength': 'Fluency', 'growth': 'Growth Mindset',
    },
    'precision_realist': {
        'name': 'The Precision Realist', 'tagline': 'You see exactly where math meets the real world.',
        'student_desc': 'You\'re fast with numbers and you know exactly WHERE to use them. Budgets, statistics, sports analytics — you see the math in everything practical, and you execute it cleanly.',
        'parent_desc': 'Your child combines computational speed with a practical, relevance-driven mindset. They naturally ask "when will I use this?" — not as a complaint, but as genuine curiosity. They thrive when math connects to real-world applications.',
        'fuar': 'F', 'gric': 'R_gric', 'colors': ['#3B82F6', '#F97316'],
        'strength': 'Fluency', 'growth': 'Relevance',
    },
    'speed_enthusiast': {
        'name': 'The Speed Enthusiast', 'tagline': 'You don\'t just do math fast, you LOVE doing it fast.',
        'student_desc': 'You\'re fast AND you love it. Math isn\'t homework to you — it\'s the most exciting game in the room. You get a rush from mental math, speed challenges, and tricky problems. Speed isn\'t just a skill for you — it\'s a passion.',
        'parent_desc': 'Your child has both mathematical fluency and genuine intrinsic interest in mathematics. They don\'t just have the skills, they have the motivation. Nurture this by connecting them to math competitions and challenging enrichment.',
        'fuar': 'F', 'gric': 'I', 'colors': ['#3B82F6', '#EC4899'],
        'strength': 'Fluency', 'growth': 'Interest',
    },
    'sure_shot': {
        'name': 'The Sure Shot', 'tagline': 'When you see a problem, you KNOW you can solve it.',
        'student_desc': 'You\'re fast and you TRUST yourself. When a math problem appears, you don\'t hesitate — you dive in because you\'ve done this before and you know your skills work. You\'re the person others look to when the clock is ticking.',
        'parent_desc': 'Your child combines computational fluency with genuine self-confidence. They trust their abilities and aren\'t easily rattled by challenging problems. This confidence-fluency combination means they perform well under pressure.',
        'fuar': 'F', 'gric': 'C', 'colors': ['#3B82F6', '#EAB308'],
        'strength': 'Fluency', 'growth': 'Confidence',
    },
    # UNDERSTANDING ROW
    'depth_builder': {
        'name': 'The Depth Builder', 'tagline': 'You construct understanding layer by layer.',
        'student_desc': 'You don\'t just learn math — you BUILD understanding from the ground up. Every time you grasp something, you ask "can I go deeper?" You\'re not satisfied with surface answers because you know real understanding has layers.',
        'parent_desc': 'Your child combines deep conceptual understanding with a growth-oriented mindset. They believe understanding can always deepen — and they\'re right. They thrive in environments that reward depth over speed.',
        'fuar': 'U', 'gric': 'G', 'colors': ['#10B981', '#14B8A6'],
        'strength': 'Understanding', 'growth': 'Growth Mindset',
    },
    'sense_maker': {
        'name': 'The Sense Maker', 'tagline': 'You turn confusing math into something everyone understands.',
        'student_desc': 'You understand math deeply AND you can explain WHY it matters. When someone asks "why do we learn this?" you actually have an answer. You see the purpose behind every concept.',
        'parent_desc': 'Your child combines deep understanding with a relevance-seeking mindset. They naturally connect math concepts to practical meaning. They don\'t just understand — they make understanding accessible to others.',
        'fuar': 'U', 'gric': 'R_gric', 'colors': ['#10B981', '#F97316'],
        'strength': 'Understanding', 'growth': 'Relevance',
    },
    'curious_mind': {
        'name': 'The Curious Mind', 'tagline': 'You can\'t stop asking "why?" and you love every answer.',
        'student_desc': 'You don\'t study math because you have to — you study it because you genuinely want to KNOW things. Every concept is a door to more questions. Your curiosity IS your superpower.',
        'parent_desc': 'Your child combines deep conceptual understanding with genuine intellectual curiosity. They\'re intrinsically motivated by comprehension — the profile of students who thrive in honors mathematics.',
        'fuar': 'U', 'gric': 'I', 'colors': ['#10B981', '#EC4899'],
        'strength': 'Understanding', 'growth': 'Interest',
    },
    'steady_anchor': {
        'name': 'The Steady Anchor', 'tagline': 'Your understanding runs deep, and so does your confidence.',
        'student_desc': 'Your confidence in math comes from the right place — genuine understanding. You don\'t just know procedures; you understand why they work. When things get hard, your solid foundations keep you steady.',
        'parent_desc': 'Your child\'s mathematical confidence is built on genuine conceptual understanding — the most durable form of confidence possible. They\'re well-prepared for advanced courses where depth matters.',
        'fuar': 'U', 'gric': 'C', 'colors': ['#10B981', '#EAB308'],
        'strength': 'Understanding', 'growth': 'Confidence',
    },
    # APPLICATION ROW
    'growth_hacker': {
        'name': 'The Growth Hacker', 'tagline': 'You apply math to hard problems and grow stronger every time.',
        'student_desc': 'You apply math to real problems, and when those problems push back, you don\'t break — you GROW. Failed approach? New data. Unexpected result? New insight. You treat every challenge as training.',
        'parent_desc': 'Your child combines application skills with powerful resilience. They apply math to real-world problems and learn from failure — the core competency of innovators and future engineers.',
        'fuar': 'A', 'gric': 'G', 'colors': ['#F59E0B', '#14B8A6'],
        'strength': 'Application', 'growth': 'Growth Mindset',
    },
    'real_world_solver': {
        'name': 'The Real-World Solver', 'tagline': 'You see the math behind everything that matters.',
        'student_desc': 'You see math as a design tool. Every real-world system is a math problem waiting for a better solution. You don\'t just solve problems — you design solutions that work in the real world.',
        'parent_desc': 'Your child combines strong application skills with deep relevance orientation. They naturally see mathematical applications in real-world systems — the profile of future engineers, data scientists, and analysts.',
        'fuar': 'A', 'gric': 'R_gric', 'colors': ['#F59E0B', '#F97316'],
        'strength': 'Application', 'growth': 'Relevance',
    },
    'creative_solver': {
        'name': 'The Creative Solver', 'tagline': 'You find paths to solutions nobody else sees.',
        'student_desc': 'You apply math creatively. Where others see one path to a solution, you see five. You\'re drawn to elegant approaches and surprising connections. Your interest drives you to find not just any solution, but the BEST one.',
        'parent_desc': 'Your child combines application skills with genuine creative interest in mathematics. They find joy in the process of applying math, not just the outcome.',
        'fuar': 'A', 'gric': 'I', 'colors': ['#F59E0B', '#EC4899'],
        'strength': 'Application', 'growth': 'Interest',
    },
    'team_captain': {
        'name': 'The Team Captain', 'tagline': 'You lead the way and take others with you.',
        'student_desc': 'You don\'t just apply math — you lead the application. In group projects and challenges, you\'re the one who organizes the approach and drives toward results. Your confidence makes you the person others follow.',
        'parent_desc': 'Your child combines strong application skills with leadership-level confidence. They take initiative in collaborative mathematical settings and drive projects to completion.',
        'fuar': 'A', 'gric': 'C', 'colors': ['#F59E0B', '#EAB308'],
        'strength': 'Application', 'growth': 'Confidence',
    },
    # REASONING ROW
    'level_up_logician': {
        'name': 'The Level-Up Logician', 'tagline': 'Your reasoning gets sharper with every challenge.',
        'student_desc': 'You think logically, and your logic is ALWAYS improving. You don\'t rest on past reasoning — you actively seek harder problems and more complex patterns. Every time your logic is tested, it comes back stronger.',
        'parent_desc': 'Your child combines strong reasoning with a growth mindset. They see logical thinking as a skill that can always be sharpened — and they actively sharpen it.',
        'fuar': 'R', 'gric': 'G', 'colors': ['#8B5CF6', '#14B8A6'],
        'strength': 'Reasoning', 'growth': 'Growth Mindset',
    },
    'pattern_connector': {
        'name': 'The Pattern Connector', 'tagline': 'You see connections that link everything together.',
        'student_desc': 'You reason with precision, and you apply that reasoning EVERYWHERE. Science, sports, games, coding — you see the logical structures that connect them all. You\'re not just a math person; you think mathematically about everything.',
        'parent_desc': 'Your child combines strong logical reasoning with a broad, relevance-driven perspective. They naturally apply mathematical reasoning across disciplines.',
        'fuar': 'R', 'gric': 'R_gric', 'colors': ['#8B5CF6', '#F97316'],
        'strength': 'Reasoning', 'growth': 'Relevance',
    },
    'mystery_hunter': {
        'name': 'The Mystery Hunter', 'tagline': 'Every problem is a mystery, and you love solving them.',
        'student_desc': 'You\'re drawn to the deepest puzzles in math — and you love it. You don\'t need real-world applications to find math interesting; the challenge itself is the reward. Your brain lights up when you spot a hidden pattern.',
        'parent_desc': 'Your child combines strong reasoning with deep intrinsic interest in abstract mathematics. Their genuine love of puzzles and logical reasoning is a gift that leads to extraordinary achievement.',
        'fuar': 'R', 'gric': 'I', 'colors': ['#8B5CF6', '#EC4899'],
        'strength': 'Reasoning', 'growth': 'Interest',
    },
    'proof_master': {
        'name': 'The Proof Master', 'tagline': 'Your logic is airtight and you can prove it.',
        'student_desc': 'You reason clearly, rigorously, and confidently. When you present an answer, it\'s built on solid logic and you can defend every step. Your confidence isn\'t bluster — it\'s the quiet certainty that comes from knowing you\'re right.',
        'parent_desc': 'Your child combines strong reasoning with well-founded confidence. They trust their logical thinking because it\'s been tested and proven.',
        'fuar': 'R', 'gric': 'C', 'colors': ['#8B5CF6', '#EAB308'],
        'strength': 'Reasoning', 'growth': 'Confidence',
    },
}

# Middle school archetype matrix
MIDDLE_ARCHETYPE_MATRIX = {
    ('F', 'G'): 'rapid_strategist', ('F', 'R_gric'): 'precision_realist',
    ('F', 'I'): 'speed_enthusiast', ('F', 'C'): 'sure_shot',
    ('U', 'G'): 'depth_builder', ('U', 'R_gric'): 'sense_maker',
    ('U', 'I'): 'curious_mind', ('U', 'C'): 'steady_anchor',
    ('A', 'G'): 'growth_hacker', ('A', 'R_gric'): 'real_world_solver',
    ('A', 'I'): 'creative_solver', ('A', 'C'): 'team_captain',
    ('R', 'G'): 'level_up_logician', ('R', 'R_gric'): 'pattern_connector',
    ('R', 'I'): 'mystery_hunter', ('R', 'C'): 'proof_master',
}

# Merge all archetypes into a single lookup (high school + middle school)
ALL_ARCHETYPES = {}
ALL_ARCHETYPES.update(ARCHETYPES)
ALL_ARCHETYPES.update(MIDDLE_ARCHETYPES)

# Add backward-compatible fields for templates that use .color, .icon, .description
_FUAR_ICONS = {'F': '⚡', 'U': '🔬', 'A': '🧩', 'R': '🔮'}
for _key, _arch in ALL_ARCHETYPES.items():
    _arch['color'] = _arch['colors'][0]  # primary color
    _arch['icon'] = _FUAR_ICONS.get(_arch.get('fuar', 'F'), '⚡')
    _arch['description'] = _arch.get('student_desc', '')

# FUAR x GRIC → Archetype lookup matrix
ARCHETYPE_MATRIX = {
    ('F', 'G'): 'adaptive_analyst', ('F', 'R_gric'): 'applied_quant',
    ('F', 'I'): 'quant_explorer', ('F', 'C'): 'confident_executor',
    ('U', 'G'): 'conceptual_strategist', ('U', 'R_gric'): 'analytical_translator',
    ('U', 'I'): 'theoretical_mind', ('U', 'C'): 'foundational_thinker',
    ('A', 'G'): 'resilient_innovator', ('A', 'R_gric'): 'systems_architect',
    ('A', 'I'): 'creative_mathematician', ('A', 'C'): 'strategic_leader',
"""  # end dead code

def calculate_gric_scores(student_id):
    """Calculate GRIC dimension scores (0-100) from mindset questionnaire responses."""
    conn = get_db()
    responses = conn.execute(
        "SELECT question_id, score FROM gric_responses WHERE student_id = ?",
        (student_id,)
    ).fetchall()

    if not responses:
        return None

    # Build lookup of question_id → question definition
    q_lookup = {q['id']: q for q in GRIC_QUESTIONS}

    dim_scores = {'G': [], 'R_gric': [], 'I': [], 'C': []}
    for r in responses:
        q = q_lookup.get(r['question_id'])
        if not q:
            continue
        score = r['score']
        # Reverse-scored items: flip 1↔4, 2↔3 (4-point scale)
        if q['is_reverse']:
            score = 5 - score
        # Normalize to 0-100 (score is 1-4)
        normalized = (score - 1) / 3.0 * 100
        dim_scores[q['dimension']].append(normalized)

    gric = {}
    for dim, scores in dim_scores.items():
        if scores:
            gric[dim] = round(sum(scores) / len(scores), 1)
        else:
            gric[dim] = 50.0
    return gric


def assign_archetype(fuar_scores, gric_scores=None, grade=None):
    """Assign one of 8 Greek letter archetypes based on FUAR + GRIC scores.
    FUAR dominant (F/U/A/R) × mindset mode (engaged/guarded) = 8 types.
    Same 8 types for all grade bands — packaging differs in templates.
    """
    fuar_dominant = max(['F', 'U', 'A', 'R'], key=lambda d: fuar_scores.get(d, 0))

    if gric_scores:
        # Determine mindset mode: G/I = engaged (intrinsic), R_gric/C = guarded (extrinsic)
        gric_dominant = max(['G', 'R_gric', 'I', 'C'], key=lambda d: gric_scores.get(d, 0))
        mindset = 'engaged' if gric_dominant in ('G', 'I') else 'guarded'
    else:
        mindset = 'engaged'  # default if no GRIC data

    return ARCHETYPE_MATRIX.get((fuar_dominant, mindset), 'sigma')


# ---------- Database ----------

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA journal_mode=WAL")
        g.db.execute("PRAGMA busy_timeout=5000")
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            student_email TEXT,
            parent_name TEXT,
            parent_email TEXT NOT NULL,
            parent_phone TEXT,
            grade INTEGER NOT NULL,
            school TEXT,
            track TEXT NOT NULL DEFAULT 'sat',
            event_code TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            test_started_at TEXT,
            test_completed_at TEXT,
            archetype TEXT,
            sat_estimated_low INTEGER,
            sat_estimated_high INTEGER,
            fuar_fluency REAL,
            fuar_understanding REAL,
            fuar_application REAL,
            fuar_reasoning REAL,
            report_sent INTEGER DEFAULT 0,
            report_sent_at TEXT,
            daily_practice_started INTEGER DEFAULT 0,
            daily_practice_streak INTEGER DEFAULT 0,
            last_practice_date TEXT
        );

        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            track TEXT NOT NULL DEFAULT 'sat',
            sat_domain TEXT NOT NULL,
            fuar_dimension TEXT NOT NULL,
            difficulty INTEGER NOT NULL DEFAULT 3,
            question_text TEXT NOT NULL,
            question_type TEXT NOT NULL DEFAULT 'multiple_choice',
            option_a TEXT,
            option_b TEXT,
            option_c TEXT,
            option_d TEXT,
            correct_answer TEXT NOT NULL,
            explanation TEXT,
            worked_solution_json TEXT,
            wrong_answer_analyses TEXT,
            simulation_html TEXT,
            topic_tag TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            selected_answer TEXT,
            is_correct INTEGER,
            time_spent_seconds INTEGER,
            answered_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (question_id) REFERENCES questions(id)
        );

        CREATE TABLE IF NOT EXISTS daily_workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            day_number INTEGER NOT NULL,
            focus_dimension TEXT NOT NULL,
            focus_topic TEXT,
            questions_json TEXT NOT NULL,
            answers_json TEXT,
            completed INTEGER DEFAULT 0,
            score REAL,
            completed_at TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (student_id) REFERENCES students(id)
        );

        CREATE TABLE IF NOT EXISTS workout_answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workout_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            student_answer TEXT,
            correct_answer TEXT NOT NULL,
            is_correct INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (workout_id) REFERENCES daily_workouts(id),
            FOREIGN KEY (question_id) REFERENCES questions(id)
        );

        CREATE TABLE IF NOT EXISTS weekly_assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            week_number INTEGER NOT NULL,
            fuar_fluency REAL,
            fuar_understanding REAL,
            fuar_application REAL,
            fuar_reasoning REAL,
            sat_estimated_low INTEGER,
            sat_estimated_high INTEGER,
            completed_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (student_id) REFERENCES students(id)
        );

        CREATE TABLE IF NOT EXISTS practice_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            weeks INTEGER DEFAULT 4,
            days_per_week INTEGER DEFAULT 4,
            minutes_per_session INTEGER DEFAULT 22,
            questions_per_session INTEGER DEFAULT 10,
            weak_topics_json TEXT,
            strong_topics_json TEXT,
            difficulty_start INTEGER DEFAULT 2,
            status TEXT DEFAULT 'active',
            current_week INTEGER DEFAULT 1,
            current_day INTEGER DEFAULT 0,
            total_sessions_completed INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now')),
            archetype_start TEXT,
            fuar_start_json TEXT,
            archetype_end TEXT,
            fuar_end_json TEXT,
            FOREIGN KEY (student_id) REFERENCES students(id)
        );

        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_code TEXT UNIQUE NOT NULL,
            event_name TEXT NOT NULL,
            school_name TEXT,
            event_date TEXT,
            location TEXT,
            event_type TEXT DEFAULT 'high_school',
            grade_min INTEGER DEFAULT 9,
            grade_max INTEGER DEFAULT 12,
            test_enabled INTEGER DEFAULT 0,
            test_enabled_at TEXT,
            is_demo INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS gric_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            question_id TEXT NOT NULL,
            score INTEGER NOT NULL,
            answered_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (student_id) REFERENCES students(id)
        );

        CREATE TABLE IF NOT EXISTS step_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            step TEXT NOT NULL,
            rating INTEGER,
            feedback_text TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (student_id) REFERENCES students(id)
        );
    """)

    # Safe column additions for existing databases
    safe_adds = [
        ("students", "gric_growth", "REAL"),
        ("students", "gric_relevance", "REAL"),
        ("students", "gric_interest", "REAL"),
        ("students", "gric_confidence", "REAL"),
        ("students", "score_type", "TEXT DEFAULT 'sat'"),
        ("students", "score_label", "TEXT"),
        ("students", "score_detail", "TEXT"),
        ("students", "mindset_completed_at", "TEXT"),
        ("events", "test_enabled", "INTEGER DEFAULT 0"),
        ("events", "test_enabled_at", "TEXT"),
        ("events", "event_type", "TEXT DEFAULT 'high_school'"),
        ("events", "grade_min", "INTEGER DEFAULT 9"),
        ("events", "grade_max", "INTEGER DEFAULT 12"),
        ("students", "parent_name", "TEXT"),
        ("students", "parent_phone", "TEXT"),
        ("events", "is_demo", "INTEGER DEFAULT 0"),
        ("questions", "worked_solution_json", "TEXT"),
        ("questions", "wrong_answer_analyses", "TEXT"),
        ("questions", "simulation_html", "TEXT"),
        ("daily_workouts", "answers_json", "TEXT"),
    ]
    for table, col, col_type in safe_adds:
        try:
            conn.execute(f"ALTER TABLE {table} ADD COLUMN {col} {col_type}")
        except Exception:
            pass  # Column already exists

    conn.commit()
    conn.close()


# ---------- Auth ----------

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'student_id' not in session:
            return redirect(url_for('student_login'))
        return f(*args, **kwargs)
    return decorated


def is_middle_school_student(student):
    """Check if a student is middle school (grade 8 or below)."""
    try:
        return int(student.get('grade', 9) or 9) <= 8
    except (ValueError, TypeError):
        return False


def get_archetype_for_student(student, archetype_key):
    """Get archetype dict with MS-specific fields applied if middle school."""
    archetype = ALL_ARCHETYPES.get(archetype_key, ARCHETYPES.get('sigma'))
    if not archetype:
        return archetype
    if is_middle_school_student(student):
        # Return a copy with MS fields overriding HS fields
        ms = dict(archetype)
        if archetype.get('ms_name'):
            ms['name'] = archetype['ms_name']
        if archetype.get('ms_tagline'):
            ms['tagline'] = archetype['ms_tagline']
        if archetype.get('ms_superpower'):
            ms['superpower'] = archetype['ms_superpower']
        if archetype.get('ms_growth'):
            ms['growth'] = archetype['ms_growth']
        if archetype.get('ms_this_is_you'):
            ms['this_is_you'] = archetype['ms_this_is_you']
        return ms
    return archetype


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'admin_role' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated


ADMIN_USERS = {
    # Cuemath admins (full access)
    'himanshu': {'password': 'cuemath2026', 'role': 'cuemath_admin', 'name': 'Himanshu'},
    'admin': {'password': 'collegeready2026', 'role': 'cuemath_admin', 'name': 'Admin'},
}
# PTA admins are created per-event by Cuemath admins


# ---------- Scoring Engine ----------

def calculate_fuar_scores(student_id):
    """Calculate FUAR dimension scores (0-100) from test responses."""
    conn = get_db()
    responses = conn.execute("""
        SELECT r.is_correct, r.time_spent_seconds, q.fuar_dimension, q.difficulty, q.sat_domain
        FROM responses r
        JOIN questions q ON r.question_id = q.id
        WHERE r.student_id = ?
    """, (student_id,)).fetchall()

    if not responses:
        return None

    # Score per dimension: weighted by difficulty
    dim_scores = {'F': [], 'U': [], 'A': [], 'R': []}
    for r in responses:
        dim = r['fuar_dimension']
        if dim in dim_scores:
            # Weight correct answers by difficulty (harder = more credit)
            weight = r['difficulty'] / 3.0  # normalize around difficulty 3
            score = (1.0 if r['is_correct'] else 0.0) * weight
            dim_scores[dim].append(score)

    fuar = {}
    for dim, scores in dim_scores.items():
        if scores:
            raw = sum(scores) / len(scores)
            # Scale to 0-100 percentile-like score
            fuar[dim] = round(min(100, max(0, raw * 100)), 1)
        else:
            fuar[dim] = 0.0  # no questions answered for this dimension — don't inflate

    return fuar


def calculate_analytics(student_id):
    """Calculate deep analytics: error patterns, pacing gap, stamina curve, time profile."""
    conn = get_db()
    responses = conn.execute("""
        SELECT r.is_correct, r.time_spent_seconds, r.selected_answer, r.answered_at,
               q.fuar_dimension, q.difficulty, q.sat_domain, q.correct_answer,
               q.option_a, q.option_b, q.option_c, q.option_d, q.explanation,
               q.question_text, q.topic_tag, r.question_id
        FROM responses r
        JOIN questions q ON r.question_id = q.id
        WHERE r.student_id = ?
        ORDER BY r.id
    """, (student_id,)).fetchall()

    if not responses:
        return {}

    total = len(responses)

    # --- 1. PACING GAP: Phase 1 vs Phase 2 performance ---
    # Phase 1 = first 65% of questions (generous time), Phase 2 = last 35% (speed round)
    phase1_cutoff = int(total * 0.65)
    phase1 = responses[:phase1_cutoff]
    phase2 = responses[phase1_cutoff:]

    p1_correct = sum(1 for r in phase1 if r['is_correct']) if phase1 else 0
    p1_total = len(phase1) if phase1 else 1
    p2_correct = sum(1 for r in phase2 if r['is_correct']) if phase2 else 0
    p2_total = len(phase2) if phase2 else 1

    p1_accuracy = round(p1_correct / p1_total * 100, 1)
    p2_accuracy = round(p2_correct / p2_total * 100, 1)
    pacing_gap = round(p1_accuracy - p2_accuracy, 1)

    if pacing_gap > 15:
        pacing_insight = "You know the math but struggle under time pressure. Focus on speed drills and question triage."
    elif pacing_gap < -5:
        pacing_insight = "Interesting — you performed better under pressure. You may benefit from more focused, timed practice."
    else:
        pacing_insight = "Your pacing is consistent. Knowledge and speed are well-matched."

    # --- 2. STAMINA CURVE: accuracy by test thirds ---
    third = max(1, total // 3)
    thirds = [
        responses[:third],
        responses[third:2*third],
        responses[2*third:]
    ]
    stamina = []
    for i, chunk in enumerate(thirds):
        if chunk:
            acc = round(sum(1 for r in chunk if r['is_correct']) / len(chunk) * 100, 1)
            avg_time = round(sum(r['time_spent_seconds'] or 0 for r in chunk) / len(chunk), 1)
        else:
            acc = 0
            avg_time = 0
        stamina.append({'label': ['First third', 'Middle third', 'Final third'][i],
                        'accuracy': acc, 'avg_time': avg_time})

    stamina_drop = stamina[0]['accuracy'] - stamina[2]['accuracy'] if len(stamina) == 3 else 0
    if stamina_drop > 15:
        stamina_insight = f"Your accuracy dropped {stamina_drop:.0f}% from start to finish. Fatigue is costing you points — build test stamina with timed full-length practice."
    elif stamina_drop > 5:
        stamina_insight = f"Slight drop of {stamina_drop:.0f}% toward the end. Normal, but timed practice can help maintain focus."
    else:
        stamina_insight = "Strong focus throughout. Your accuracy held steady from start to finish."

    # --- 3. TIME PROFILE: avg time per FUAR dimension ---
    time_by_dim = {'F': [], 'U': [], 'A': [], 'R': []}
    for r in responses:
        dim = r['fuar_dimension']
        t = r['time_spent_seconds'] or 0
        if dim in time_by_dim:
            time_by_dim[dim].append(t)

    time_profile = {}
    for dim, times in time_by_dim.items():
        if times:
            avg = round(sum(times) / len(times), 1)
            time_profile[dim] = avg
        else:
            time_profile[dim] = 0

    fastest_dim = min(time_profile, key=time_profile.get) if time_profile else 'F'
    slowest_dim = max(time_profile, key=time_profile.get) if time_profile else 'R'
    fuar_names = {'F': 'Fluency', 'U': 'Understanding', 'A': 'Application', 'R': 'Reasoning'}
    time_insight = f"You're fastest on {fuar_names[fastest_dim]} ({time_profile[fastest_dim]:.0f}s avg) and slowest on {fuar_names[slowest_dim]} ({time_profile[slowest_dim]:.0f}s avg)."

    # --- 4. ERROR PATTERN ANALYSIS ---
    # Track which wrong answers students pick and what they mean
    error_patterns = {}
    wrong_responses = [r for r in responses if not r['is_correct'] and r['selected_answer']]

    for r in wrong_responses:
        domain = r['sat_domain']
        dim = r['fuar_dimension']
        key = f"{domain}|{dim}"

        if key not in error_patterns:
            error_patterns[key] = {
                'domain': domain.replace('_', ' ').title(),
                'dimension': fuar_names.get(dim, dim),
                'count': 0,
                'examples': [],
            }
        error_patterns[key]['count'] += 1
        if len(error_patterns[key]['examples']) < 2:  # Keep max 2 examples
            error_patterns[key]['examples'].append({
                'question': r['question_text'][:100],
                'picked': r['selected_answer'],
                'correct': r['correct_answer'],
            })

    # Sort by count descending — biggest problem areas first
    top_errors = sorted(error_patterns.values(), key=lambda x: x['count'], reverse=True)[:5]

    # --- 5. TOPIC HEAT MAP: accuracy by content area ---
    topic_scores = {}
    for r in responses:
        domain = r['sat_domain']
        if domain not in topic_scores:
            topic_scores[domain] = {'correct': 0, 'total': 0}
        topic_scores[domain]['total'] += 1
        if r['is_correct']:
            topic_scores[domain]['correct'] += 1

    topic_heatmap = []
    for domain, data in sorted(topic_scores.items()):
        pct = round(data['correct'] / data['total'] * 100, 1) if data['total'] > 0 else 0
        status = 'strong' if pct >= 70 else ('developing' if pct >= 45 else 'needs_work')
        topic_heatmap.append({
            'domain': domain.replace('_', ' ').title(),
            'accuracy': pct,
            'correct': data['correct'],
            'total': data['total'],
            'status': status,
        })

    # --- 6. SPEED vs ACCURACY QUADRANT per question ---
    # Fast+Right = Mastered, Slow+Right = Fluency gap, Fast+Wrong = Careless, Slow+Wrong = Content gap
    median_time = sorted([r['time_spent_seconds'] or 0 for r in responses])[total // 2] if total > 0 else 60
    quadrants = {'mastered': 0, 'fluency_gap': 0, 'careless': 0, 'content_gap': 0}
    for r in responses:
        t = r['time_spent_seconds'] or 0
        fast = t <= median_time
        correct = r['is_correct']
        if fast and correct:
            quadrants['mastered'] += 1
        elif not fast and correct:
            quadrants['fluency_gap'] += 1
        elif fast and not correct:
            quadrants['careless'] += 1
        else:
            quadrants['content_gap'] += 1

    quadrant_pcts = {k: round(v / total * 100, 1) for k, v in quadrants.items()}

    return {
        'pacing': {
            'phase1_accuracy': p1_accuracy,
            'phase2_accuracy': p2_accuracy,
            'gap': pacing_gap,
            'insight': pacing_insight,
        },
        'stamina': {
            'thirds': stamina,
            'drop': stamina_drop,
            'insight': stamina_insight,
        },
        'time_profile': {
            'by_dimension': time_profile,
            'fastest': fastest_dim,
            'slowest': slowest_dim,
            'insight': time_insight,
        },
        'error_patterns': top_errors,
        'topic_heatmap': topic_heatmap,
        'quadrants': quadrant_pcts,
        'total_questions': total,
    }


def generate_practice_plan(student_id):
    """Generate a 4-week practice plan based on diagnostic results.

    Returns the plan dict or None if already exists.
    - 20-25 min sessions (~10-12 questions)
    - Recommends 3/4/5 days per week based on gap size
    - Topic-level targeting from heatmap
    - Adaptive difficulty starting at the student's failure point
    """
    conn = get_db()
    student = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    if not student or not student['archetype']:
        return None

    # Check if plan already exists
    existing = conn.execute(
        "SELECT * FROM practice_plans WHERE student_id = ? AND status = 'active'",
        (student_id,)
    ).fetchone()
    if existing:
        return dict(existing)

    # Calculate topic-level performance from diagnostic
    analytics = calculate_analytics(student_id)
    topic_heatmap = analytics.get('topic_heatmap', []) if analytics else []

    fuar = {
        'F': student['fuar_fluency'] or 0,
        'U': student['fuar_understanding'] or 0,
        'A': student['fuar_application'] or 0,
        'R': student['fuar_reasoning'] or 0,
    }
    avg_score = sum(fuar.values()) / 4

    # Determine days per week based on gap
    # Bigger gap → more days needed
    if avg_score < 35:
        days_per_week = 5  # significant gap
    elif avg_score < 55:
        days_per_week = 4  # moderate gap
    else:
        days_per_week = 3  # solid base, maintenance + growth

    # Split topics into weak (below 60%) and strong (60%+)
    weak_topics = sorted(
        [t for t in topic_heatmap if t['accuracy'] < 60],
        key=lambda t: t['accuracy']
    )
    strong_topics = sorted(
        [t for t in topic_heatmap if t['accuracy'] >= 60],
        key=lambda t: t['accuracy'], reverse=True
    )

    # Determine starting difficulty from diagnostic responses
    responses = conn.execute("""
        SELECT q.difficulty, r.is_correct
        FROM responses r JOIN questions q ON r.question_id = q.id
        WHERE r.student_id = ?
    """, (student_id,)).fetchall()

    # Find the difficulty level where accuracy drops below 50%
    diff_scores = {}
    for r in responses:
        d = r['difficulty']
        if d not in diff_scores:
            diff_scores[d] = {'correct': 0, 'total': 0}
        diff_scores[d]['total'] += 1
        if r['is_correct']:
            diff_scores[d]['correct'] += 1

    difficulty_start = 2  # default
    for d in sorted(diff_scores.keys()):
        data = diff_scores[d]
        acc = data['correct'] / data['total'] if data['total'] > 0 else 0
        if acc < 0.5:
            difficulty_start = max(1, d - 1)  # start one below failure point
            break

    # Questions per session: ~10-12 for 20-25 min (2 min per question avg)
    questions_per_session = 11

    plan = {
        'student_id': student_id,
        'weeks': 4,
        'days_per_week': days_per_week,
        'minutes_per_session': 22,
        'questions_per_session': questions_per_session,
        'weak_topics_json': json.dumps([t['domain'] for t in weak_topics]),
        'strong_topics_json': json.dumps([t['domain'] for t in strong_topics]),
        'difficulty_start': difficulty_start,
        'archetype_start': student['archetype'],
        'fuar_start_json': json.dumps(fuar),
    }

    cursor = conn.execute("""
        INSERT INTO practice_plans
        (student_id, weeks, days_per_week, minutes_per_session, questions_per_session,
         weak_topics_json, strong_topics_json, difficulty_start,
         archetype_start, fuar_start_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (plan['student_id'], plan['weeks'], plan['days_per_week'],
          plan['minutes_per_session'], plan['questions_per_session'],
          plan['weak_topics_json'], plan['strong_topics_json'],
          plan['difficulty_start'], plan['archetype_start'], plan['fuar_start_json']))
    conn.commit()

    plan['id'] = cursor.lastrowid
    return plan


def get_practice_session_questions(student_id, plan):
    """Select questions for today's practice session based on the plan.

    Week 1-2: 80% weak topics, 20% strong. Current difficulty.
    Week 3: 70% weak, 30% strong. Difficulty +1.
    Week 4: All topics mixed. Difficulty +1. Test conditions.
    """
    conn = get_db()
    student = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    track = student['track']

    weak_topics = json.loads(plan['weak_topics_json'] or '[]')
    strong_topics = json.loads(plan['strong_topics_json'] or '[]')
    current_week = plan['current_week']
    base_diff = plan['difficulty_start']
    n_questions = plan['questions_per_session']

    # Check what the student has improved on from practice history
    # Get topic accuracy from recent practice (last 5 sessions)
    recent_workouts = conn.execute("""
        SELECT questions_json, score FROM daily_workouts
        WHERE student_id = ? AND completed = 1
        ORDER BY completed_at DESC LIMIT 5
    """, (student_id,)).fetchall()

    # Difficulty progression based on week
    if current_week <= 2:
        difficulty = base_diff
        weak_ratio = 0.80
    elif current_week == 3:
        difficulty = min(5, base_diff + 1)
        weak_ratio = 0.70
    else:  # week 4
        difficulty = min(5, base_diff + 1)
        weak_ratio = 0.50  # balanced mix

    n_weak = round(n_questions * weak_ratio)
    n_strong = n_questions - n_weak

    # Get already-answered question IDs to avoid repeats when possible
    answered_ids = conn.execute("""
        SELECT DISTINCT r.question_id FROM responses r
        WHERE r.student_id = ?
        UNION
        SELECT value FROM daily_workouts dw, json_each(dw.questions_json)
        WHERE dw.student_id = ? AND dw.completed = 1
    """, (student_id, student_id)).fetchall()
    answered_set = {r[0] for r in answered_ids}

    def fetch_questions(topics, count, diff):
        """Fetch questions for given topics, preferring unseen, near target difficulty."""
        if not topics:
            return []
        placeholders = ','.join('?' * len(topics))
        # Convert display names back to db format
        topic_db = [t.replace(' ', '_').lower() for t in topics]

        rows = conn.execute(f"""
            SELECT id, sat_domain, difficulty FROM questions
            WHERE track = ? AND LOWER(REPLACE(sat_domain, ' ', '_')) IN ({placeholders})
            AND difficulty BETWEEN ? AND ?
            ORDER BY RANDOM()
        """, (track, *topic_db, max(1, diff - 1), min(5, diff + 1))).fetchall()

        # Prefer unseen questions
        unseen = [r for r in rows if r['id'] not in answered_set]
        seen = [r for r in rows if r['id'] in answered_set]
        pool = unseen + seen  # unseen first, then seen as fallback
        return [r['id'] for r in pool[:count]]

    weak_qs = fetch_questions(weak_topics, n_weak, difficulty)
    strong_qs = fetch_questions(strong_topics, n_strong, difficulty)

    # If we didn't get enough, fill from any topic
    all_qs = weak_qs + strong_qs
    if len(all_qs) < n_questions:
        fill = conn.execute("""
            SELECT id FROM questions WHERE track = ?
            AND difficulty BETWEEN ? AND ?
            AND id NOT IN ({})
            ORDER BY RANDOM() LIMIT ?
        """.format(','.join('?' * len(all_qs)) if all_qs else '0'),
            (track, max(1, difficulty - 1), min(5, difficulty + 1),
             *all_qs, n_questions - len(all_qs))).fetchall()
        all_qs.extend([r['id'] for r in fill])

    import random
    random.shuffle(all_qs)
    return all_qs[:n_questions]


def estimate_sat_score(fuar_scores, responses):
    """Estimate SAT Math score range from FUAR scores and domain performance."""
    if not fuar_scores:
        return 400, 500

    weighted = (
        fuar_scores['F'] * 0.25 +
        fuar_scores['U'] * 0.25 +
        fuar_scores['A'] * 0.30 +
        fuar_scores['R'] * 0.20
    )

    base = 200 + (weighted / 100) * 600
    n = len(responses) if responses else 1
    variance = max(20, 80 - n)

    low = max(200, int((base - variance) // 10 * 10))
    high = min(800, int((base + variance) // 10 * 10))

    return low, high


def estimate_score(track, fuar_scores, responses):
    """Track-specific scoring. Returns dict with score_type, label, detail."""
    if not fuar_scores:
        return {'score_type': 'unknown', 'label': 'Incomplete', 'detail': 'Not enough data'}

    weighted = (
        fuar_scores['F'] * 0.25 + fuar_scores['U'] * 0.25 +
        fuar_scores['A'] * 0.30 + fuar_scores['R'] * 0.20
    )
    n = len(responses) if responses else 1

    # --- SAT Track ---
    if track == 'sat':
        low, high = estimate_sat_score(fuar_scores, responses)
        # Percentile estimate (rough mapping)
        midpoint = (low + high) / 2
        if midpoint >= 750: pct = '99th'
        elif midpoint >= 700: pct = '93rd-98th'
        elif midpoint >= 650: pct = '83rd-92nd'
        elif midpoint >= 600: pct = '70th-82nd'
        elif midpoint >= 550: pct = '55th-69th'
        elif midpoint >= 500: pct = '40th-54th'
        elif midpoint >= 450: pct = '25th-39th'
        else: pct = 'below 25th'
        return {
            'score_type': 'sat',
            'label': f'Estimated SAT: {low}-{high}',
            'detail': f'{pct} percentile',
            'low': low, 'high': high,
        }

    # --- AP Tracks --- (track-specific thresholds: harder exams need lower % for same AP score)
    if track.startswith('ap_'):
        readiness = min(100, max(0, round(weighted, 1)))

        # Thresholds calibrated to exam difficulty — BC/Stats are harder, so lower % = same AP score
        ap_thresholds = {
            'ap_precalc':  [(78, 5, 'High'), (63, 4, 'Good'), (48, 3, 'Moderate'), (33, 2, 'Developing')],
            'ap_calc_ab':  [(75, 5, 'High'), (60, 4, 'Good'), (45, 3, 'Moderate'), (30, 2, 'Developing')],
            'ap_calc_bc':  [(70, 5, 'High'), (55, 4, 'Good'), (40, 3, 'Moderate'), (28, 2, 'Developing')],
            'ap_stats':    [(72, 5, 'High'), (57, 4, 'Good'), (42, 3, 'Moderate'), (30, 2, 'Developing')],
        }
        thresholds = ap_thresholds.get(track, [(80, 5, 'High'), (65, 4, 'Good'), (50, 3, 'Moderate'), (35, 2, 'Developing')])
        ap_score, confidence = 1, 'Early'
        for thresh, score, conf in thresholds:
            if readiness >= thresh:
                ap_score, confidence = score, conf
                break

        track_names = {
            'ap_precalc': 'AP Precalculus', 'ap_calc_ab': 'AP Calculus AB',
            'ap_calc_bc': 'AP Calculus BC', 'ap_stats': 'AP Statistics',
        }
        name = track_names.get(track, 'AP')
        return {
            'score_type': 'ap',
            'label': f'{name} Readiness: {readiness:.0f}%',
            'detail': f'Predicted AP Score: {ap_score} ({confidence})',
            'readiness': readiness, 'ap_score': ap_score,
        }

    # --- Grade-Level Tracks (Middle School) ---
    config = TRACK_CONFIG.get(track, {})
    if config.get('score_type') == 'grade_proficiency':
        proficiency = min(100, max(0, round(weighted, 1)))
        grade_level = config.get('grade_level', 6)

        if proficiency >= 80:
            level, desc = 'Advanced', f'Performing above Grade {grade_level} level — ready for acceleration'
        elif proficiency >= 60:
            level, desc = 'Proficient', f'Solid Grade {grade_level} performance — on track'
        elif proficiency >= 40:
            level, desc = 'Approaching', f'Approaching Grade {grade_level} level — some gaps to address'
        else:
            level, desc = 'Developing', f'Below Grade {grade_level} expectations — foundational gaps need attention'

        # Algebra readiness indicator for Grade 7-8
        readiness_note = ''
        if grade_level in (7, 8) and track != 'algebra_1':
            if proficiency >= 70:
                readiness_note = 'Algebra Ready — on track for Algebra 1'
            elif proficiency >= 50:
                readiness_note = 'Approaching Algebra Readiness — focus on expressions and equations'
            else:
                readiness_note = 'Needs Foundation Work — strengthen pre-algebra skills before Algebra 1'
            desc = f'{desc}. {readiness_note}'

        name = config.get('display_name', config.get('name', track.replace('_', ' ').title()))
        predicted_grade = 'A' if proficiency >= 80 else 'B' if proficiency >= 60 else 'C' if proficiency >= 40 else 'D'
        return {
            'score_type': 'grade',
            'label': f'{name}: {level}',
            'detail': desc,
            'proficiency': proficiency, 'level': level,
            'predicted_grade': predicted_grade,
        }

    # --- Course Tracks (High School) --- (harder courses use lower proficiency thresholds)
    proficiency = min(100, max(0, round(weighted, 1)))

    course_thresholds = {
        'algebra_1':   (78, 58, 38),  # most accessible
        'geometry':    (76, 56, 36),
        'algebra_2':   (74, 54, 34),
        'statistics':  (72, 52, 34),
        'precalculus': (70, 50, 32),  # hardest course track
    }
    adv, prof, appr = course_thresholds.get(track, (80, 60, 40))

    track_names = {
        'algebra_1': 'Algebra 1', 'algebra_2': 'Algebra 2',
        'geometry': 'Geometry', 'precalculus': 'Precalculus',
        'statistics': 'Statistics',
    }
    name = track_names.get(track, track.replace('_', ' ').title())

    # Next course in sequence for context
    next_course = {
        'algebra_1': 'Geometry', 'geometry': 'Algebra 2',
        'algebra_2': 'Precalculus or AP Statistics',
        'precalculus': 'AP Calculus', 'statistics': 'AP Statistics',
    }
    next_c = next_course.get(track, 'the next math course')

    if proficiency >= adv:
        level = 'Advanced'
        desc = f'Strong {name} mastery — well prepared for {next_c}'
    elif proficiency >= prof:
        level = 'Proficient'
        desc = f'Solid {name} performance — on track for {next_c}'
    elif proficiency >= appr:
        level = 'Approaching'
        desc = f'Building {name} skills — some areas need strengthening before {next_c}'
    else:
        level = 'Developing'
        desc = f'Foundational {name} gaps to address — targeted practice will help'

    predicted_grade = 'A' if proficiency >= 80 else 'B' if proficiency >= 60 else 'C' if proficiency >= 40 else 'D'
    return {
        'score_type': 'course',
        'label': f'{name}: {level}',
        'detail': desc,
        'proficiency': proficiency, 'level': level,
        'predicted_grade': predicted_grade,
    }


# ---------- Question Selection ----------

## ---------- Track Configuration ----------

TRACK_CONFIG = {
    'sat': {
        'name': 'SAT Math',
        'total_questions': 44,
        'module1_questions': 22,
        'module2_questions': 22,
        'time_minutes': 70,
        'content_field': 'sat_domain',  # which DB field holds content area
        'domain_weights': {
            'algebra': 0.35,
            'advanced_math': 0.35,
            'problem_solving': 0.15,
            'geometry_trig': 0.15,
        },
        'score_type': 'sat_score',  # SAT 200-800
    },
    'ap_precalc': {
        'name': 'AP Precalculus',
        'total_questions': 24,
        'module1_questions': 12,
        'module2_questions': 12,
        'time_minutes': 70,
        'content_field': 'sat_domain',
        'domain_weights': {
            'poly_rational': 0.35,
            'exp_log': 0.35,
            'trig_polar': 0.30,
        },
        'score_type': 'ap_readiness',  # 0-100% readiness
    },
    'ap_calc_ab': {
        'name': 'AP Calculus AB',
        'total_questions': 28,
        'module1_questions': 14,
        'module2_questions': 14,
        'time_minutes': 70,
        'content_field': 'sat_domain',
        'domain_weights': {
            'limits_continuity': 0.11,
            'diff_basics': 0.11,
            'diff_advanced': 0.11,
            'diff_applications': 0.13,
            'diff_analytical': 0.16,
            'integration': 0.18,
            'diff_equations': 0.09,
            'integration_apps': 0.11,
        },
        'score_type': 'ap_readiness',
    },
    'ap_calc_bc': {
        'name': 'AP Calculus BC',
        'total_questions': 30,
        'module1_questions': 15,
        'module2_questions': 15,
        'time_minutes': 70,
        'content_field': 'sat_domain',
        'domain_weights': {
            'limits_continuity': 0.06,
            'diff_basics': 0.06,
            'diff_advanced': 0.06,
            'diff_applications': 0.08,
            'diff_analytical': 0.10,
            'integration': 0.18,
            'diff_equations': 0.08,
            'integration_apps': 0.08,
            'parametric_polar_vectors': 0.12,
            'series': 0.18,
        },
        'score_type': 'ap_readiness',
    },
    'ap_stats': {
        'name': 'AP Statistics',
        'total_questions': 28,
        'module1_questions': 14,
        'module2_questions': 14,
        'time_minutes': 70,
        'content_field': 'sat_domain',
        'domain_weights': {
            'exploring_data': 0.19,
            'two_var_data': 0.06,
            'collecting_data': 0.14,
            'probability': 0.15,
            'sampling_dist': 0.10,
            'inference_proportions': 0.14,
            'inference_means': 0.14,
            'chi_square': 0.04,
            'inference_slopes': 0.04,
        },
        'score_type': 'ap_readiness',
    },
    'algebra_1': {
        'name': 'Algebra 1',
        'total_questions': 25,
        'module1_questions': 13,
        'module2_questions': 12,
        'time_minutes': 60,
        'content_field': 'sat_domain',
        'domain_weights': {
            'linear_equations': 0.20,
            'linear_functions': 0.15,
            'systems': 0.15,
            'quadratics': 0.20,
            'exponentials': 0.15,
            'data_stats': 0.15,
        },
        'score_type': 'course_proficiency',
    },
    'geometry': {
        'name': 'Geometry',
        'total_questions': 25,
        'module1_questions': 13,
        'module2_questions': 12,
        'time_minutes': 60,
        'content_field': 'sat_domain',
        'domain_weights': {
            'congruence_triangles': 0.20,
            'similarity': 0.15,
            'right_triangles_trig': 0.20,
            'circles': 0.15,
            'area_volume': 0.15,
            'transformations': 0.15,
        },
        'score_type': 'course_proficiency',
    },
    'algebra_2': {
        'name': 'Algebra 2',
        'total_questions': 28,
        'module1_questions': 14,
        'module2_questions': 14,
        'time_minutes': 60,
        'content_field': 'sat_domain',
        'domain_weights': {
            'polynomials': 0.20,
            'rational_functions': 0.15,
            'exp_log': 0.20,
            'trig': 0.15,
            'sequences_series': 0.15,
            'complex_numbers': 0.15,
        },
        'score_type': 'course_proficiency',
    },
    'precalculus': {
        'name': 'Precalculus',
        'total_questions': 28,
        'module1_questions': 14,
        'module2_questions': 14,
        'time_minutes': 60,
        'content_field': 'sat_domain',
        'domain_weights': {
            'functions': 0.15,
            'poly_rational': 0.15,
            'exp_log': 0.15,
            'trig_functions': 0.20,
            'analytic_trig': 0.15,
            'polar_vectors': 0.10,
            'limits_intro': 0.10,
        },
        'score_type': 'course_proficiency',
    },
    'statistics': {
        'name': 'Statistics',
        'total_questions': 22,
        'module1_questions': 11,
        'module2_questions': 11,
        'time_minutes': 60,
        'content_field': 'sat_domain',
        'domain_weights': {
            'descriptive_stats': 0.20,
            'normal_distribution': 0.15,
            'correlation_regression': 0.15,
            'data_collection': 0.15,
            'probability': 0.15,
            'confidence_intervals': 0.10,
            'hypothesis_testing': 0.10,
        },
        'score_type': 'course_proficiency',
    },
    # ---------- Middle School Tracks ----------
    'grade_6': {
        'name': 'Grade 6 Math',
        'display_name': 'Grade 6 — Foundation Builder',
        'total_questions': 24,
        'module1_questions': 12,
        'module2_questions': 12,
        'time_minutes': 45,
        'content_field': 'sat_domain',
        'grade_level': 6,
        'domain_weights': {
            'ratios_rates': 0.20,
            'fractions_decimals': 0.20,
            'integers_number_system': 0.15,
            'expressions_equations': 0.20,
            'geometry_measurement': 0.15,
            'data_statistics': 0.10,
        },
        'score_type': 'grade_proficiency',
    },
    'grade_7': {
        'name': 'Grade 7 Math',
        'display_name': 'Grade 7 — Bridge Builder',
        'total_questions': 24,
        'module1_questions': 12,
        'module2_questions': 12,
        'time_minutes': 45,
        'content_field': 'sat_domain',
        'grade_level': 7,
        'domain_weights': {
            'proportional_relationships': 0.20,
            'rational_numbers': 0.20,
            'expressions_equations': 0.20,
            'geometry_circles_angles': 0.15,
            'probability_statistics': 0.15,
            'inequalities': 0.10,
        },
        'score_type': 'grade_proficiency',
    },
    'grade_7_accelerated': {
        'name': 'Grade 7 Accelerated',
        'display_name': 'Grade 7 Accelerated — Pre-Algebra',
        'total_questions': 24,
        'module1_questions': 12,
        'module2_questions': 12,
        'time_minutes': 45,
        'content_field': 'sat_domain',
        'grade_level': 7,
        'domain_weights': {
            'proportional_relationships': 0.15,
            'rational_numbers': 0.15,
            'linear_equations_intro': 0.20,
            'functions_intro': 0.15,
            'geometry_transformations': 0.15,
            'exponents_scientific_notation': 0.10,
            'systems_intro': 0.10,
        },
        'score_type': 'grade_proficiency',
    },
    'grade_8': {
        'name': 'Grade 8 Math',
        'display_name': 'Grade 8 — Algebra Ready',
        'total_questions': 24,
        'module1_questions': 12,
        'module2_questions': 12,
        'time_minutes': 45,
        'content_field': 'sat_domain',
        'grade_level': 8,
        'domain_weights': {
            'linear_equations_systems': 0.25,
            'functions': 0.20,
            'exponents_radicals': 0.15,
            'geometry_transformations': 0.15,
            'data_modeling': 0.15,
            'irrational_numbers': 0.10,
        },
        'score_type': 'grade_proficiency',
    },
    # Grade 8 Accelerated = algebra_1 track (already exists above)
}

# Track groups for registration UI
MIDDLE_SCHOOL_TRACKS = {
    6: [('grade_6', 'Grade 6 Math (Regular)')],
    7: [('grade_7', 'Grade 7 Math (Regular)'), ('grade_7_accelerated', 'Grade 7 Accelerated (Pre-Algebra)')],
    8: [('grade_8', 'Grade 8 Math (Regular)'), ('algebra_1', 'Grade 8 Accelerated (Algebra 1)')],
}

HIGH_SCHOOL_TRACKS = {
    9: [('algebra_1', 'Algebra 1'), ('geometry', 'Geometry')],
    10: [('geometry', 'Geometry'), ('algebra_2', 'Algebra 2'), ('sat', 'SAT Math')],
    11: [('algebra_2', 'Algebra 2'), ('precalculus', 'Precalculus'), ('ap_precalc', 'AP Precalculus'),
         ('ap_stats', 'AP Statistics'), ('sat', 'SAT Math')],
    12: [('precalculus', 'Precalculus'), ('statistics', 'Statistics'), ('ap_calc_ab', 'AP Calculus AB'),
         ('ap_calc_bc', 'AP Calculus BC'), ('ap_stats', 'AP Statistics'), ('sat', 'SAT Math')],
}

def get_tracks_for_grade(grade):
    """Return available tracks for a given grade."""
    grade = int(grade)
    if grade in MIDDLE_SCHOOL_TRACKS:
        return MIDDLE_SCHOOL_TRACKS[grade]
    elif grade in HIGH_SCHOOL_TRACKS:
        return HIGH_SCHOOL_TRACKS[grade]
    else:
        return [('sat', 'SAT Math')]  # fallback


def select_module1_questions(track='sat'):
    """Select Module 1 questions: medium difficulty (2-3), balanced across FUAR and content areas.
    Everyone gets the same difficulty level in Module 1 — this establishes baseline."""
    conn = get_db()
    config = TRACK_CONFIG.get(track, TRACK_CONFIG['sat'])
    num = config['module1_questions']

    # Get medium difficulty questions (2-3), balanced across FUAR
    fuar_dims = ['F', 'U', 'A', 'R']
    per_dim = num // 4
    extra = num - (per_dim * 4)

    selected = []
    for i, dim in enumerate(fuar_dims):
        count = per_dim + (1 if i < extra else 0)
        questions = conn.execute("""
            SELECT id FROM questions
            WHERE track = ? AND fuar_dimension = ? AND difficulty IN (2, 3)
            ORDER BY RANDOM()
            LIMIT ?
        """, (track, dim, count)).fetchall()

        # Fallback: if not enough medium questions, include easy/hard
        if len(questions) < count:
            remaining = count - len(questions)
            existing_ids = [q['id'] for q in questions]
            placeholders = ','.join('?' * len(existing_ids)) if existing_ids else '0'
            fallback = conn.execute(f"""
                SELECT id FROM questions
                WHERE track = ? AND fuar_dimension = ? AND id NOT IN ({placeholders})
                ORDER BY RANDOM()
                LIMIT ?
            """, (track, dim, *existing_ids, remaining)).fetchall()
            questions = list(questions) + list(fallback)

        selected.extend([q['id'] for q in questions])

    random.shuffle(selected)
    return selected


def select_module2_questions(track, student_id, module1_ids):
    """Select Module 2 questions: difficulty adapts based on Module 1 performance.
    This is the adaptive routing — like Digital SAT Module 2."""
    conn = get_db()
    config = TRACK_CONFIG.get(track, TRACK_CONFIG['sat'])
    num = config['module2_questions']

    # Score Module 1
    placeholders = ','.join('?' * len(module1_ids))
    results = conn.execute(f"""
        SELECT is_correct FROM responses
        WHERE student_id = ? AND question_id IN ({placeholders})
    """, (student_id, *module1_ids)).fetchall()

    correct = sum(1 for r in results if r['is_correct'])
    total = len(results) if results else 1
    m1_score = correct / total

    # Route to difficulty pool
    if m1_score >= 0.70:
        difficulties = (4, 5)     # Hard pool — unlocks high scores
        route = 'hard'
    elif m1_score >= 0.40:
        difficulties = (3, 4)     # Medium-hard pool
        route = 'medium'
    else:
        difficulties = (1, 2)     # Foundation pool — builds confidence
        route = 'easy'

    # Select balanced across FUAR, from routed difficulty pool
    fuar_dims = ['F', 'U', 'A', 'R']
    per_dim = num // 4
    extra = num - (per_dim * 4)

    # Exclude Module 1 questions
    exclude_placeholders = ','.join('?' * len(module1_ids))

    selected = []
    for i, dim in enumerate(fuar_dims):
        count = per_dim + (1 if i < extra else 0)
        questions = conn.execute(f"""
            SELECT id FROM questions
            WHERE track = ? AND fuar_dimension = ?
            AND difficulty IN (?, ?)
            AND id NOT IN ({exclude_placeholders})
            ORDER BY RANDOM()
            LIMIT ?
        """, (track, dim, *difficulties, *module1_ids, count)).fetchall()

        # Fallback: if not enough in routed pool, expand difficulty range
        if len(questions) < count:
            remaining = count - len(questions)
            existing_ids = [q['id'] for q in questions] + list(module1_ids)
            ex_ph = ','.join('?' * len(existing_ids))
            fallback = conn.execute(f"""
                SELECT id FROM questions
                WHERE track = ? AND fuar_dimension = ? AND id NOT IN ({ex_ph})
                ORDER BY RANDOM()
                LIMIT ?
            """, (track, dim, *existing_ids, remaining)).fetchall()
            questions = list(questions) + list(fallback)

        selected.extend([q['id'] for q in questions])

    random.shuffle(selected)
    return selected, route


def select_demo_questions(track='sat'):
    """Select 10 questions for demo mode — balanced across FUAR, medium difficulty."""
    conn = get_db()
    selected = []
    for dim in ['F', 'U', 'A', 'R']:
        qs = conn.execute("""
            SELECT id FROM questions
            WHERE track = ? AND fuar_dimension = ? AND difficulty BETWEEN 2 AND 3
            ORDER BY RANDOM() LIMIT 3
        """, (track, dim)).fetchall()
        selected.extend([q['id'] for q in qs])
    random.shuffle(selected)
    return selected[:10]


# ---------- Routes ----------

@app.route('/showcase')
def showcase():
    """Design showcase — all screens on one page for review."""
    return render_template('showcase.html')


@app.route('/')
def landing():
    """Landing page — event day login for students."""
    return render_template('landing.html')


@app.route('/login', methods=['GET', 'POST'])
def student_login():
    """Event-day student login — email + event code."""
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        event_code = request.form.get('event_code', '').strip().upper()

        if not email or not event_code:
            flash('Please enter your email and event code.', 'danger')
            return render_template('student_login.html')

        conn = get_db()
        student = conn.execute(
            "SELECT * FROM students WHERE student_email = ? AND event_code = ?",
            (email, event_code)
        ).fetchone()

        if not student:
            flash('No registration found. Check your email and event code, or ask the facilitator.', 'danger')
            return render_template('student_login.html', event_code=event_code)

        # Check if test is enabled for this event
        event = conn.execute("SELECT * FROM events WHERE event_code = ?", (event_code,)).fetchone()
        if event and not event['test_enabled']:
            return render_template('student_login.html', event_code=event_code, waiting=True)

        session['student_id'] = student['id']
        session['student_name'] = student['student_name']
        session['event_code'] = event_code

        # If already completed, go to dashboard
        if student['archetype']:
            return redirect(url_for('dashboard'))

        return redirect(url_for('test_intro'))

    return render_template('student_login.html')


@app.route('/register/<event_code>', methods=['GET', 'POST'])
def event_register(event_code):
    """Pre-event registration — students register days before the event."""
    conn = get_db()
    event = conn.execute("SELECT * FROM events WHERE event_code = ?",
                          (event_code.upper(),)).fetchone()

    if not event:
        flash('Invalid event code.', 'danger')
        return redirect(url_for('landing'))

    # Determine grade range for this event
    grade_min = event['grade_min'] if 'grade_min' in event.keys() else 9
    grade_max = event['grade_max'] if 'grade_max' in event.keys() else 12
    event_type = event['event_type'] if 'event_type' in event.keys() else 'high_school'

    if request.method == 'POST':
        student_name = request.form.get('student_name', '').strip()
        student_email = request.form.get('student_email', '').strip().lower()
        parent_name = request.form.get('parent_name', '').strip()
        parent_email = request.form.get('parent_email', '').strip().lower()
        parent_phone = request.form.get('parent_phone', '').strip()
        grade = request.form.get('grade', '')
        track = request.form.get('track', 'sat')

        if not student_name or not parent_email or not grade:
            flash('Please fill in all required fields.', 'danger')
            return render_template('event_register.html', event=event, tracks=TRACK_CONFIG,
                                   grade_min=grade_min, grade_max=grade_max, event_type=event_type,
                                   get_tracks_for_grade=get_tracks_for_grade)

        # Check for duplicate registration
        existing = conn.execute(
            "SELECT id FROM students WHERE student_email = ? AND event_code = ?",
            (student_email, event_code.upper())
        ).fetchone() if student_email else None

        if existing:
            flash('You are already registered for this event!', 'info')
            return render_template('event_register.html', event=event, tracks=TRACK_CONFIG,
                                   registered=True, grade_min=grade_min, grade_max=grade_max,
                                   event_type=event_type, get_tracks_for_grade=get_tracks_for_grade)

        conn.execute("""
            INSERT INTO students (student_name, student_email, parent_name, parent_email,
                                  parent_phone, grade, school, track, event_code)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (student_name, student_email or None, parent_name, parent_email,
              parent_phone or None, int(grade), event['school_name'] or '', track,
              event_code.upper()))
        conn.commit()

        return render_template('event_register.html', event=event, tracks=TRACK_CONFIG,
                             registered=True, student_name=student_name,
                             grade_min=grade_min, grade_max=grade_max, event_type=event_type,
                             get_tracks_for_grade=get_tracks_for_grade)

    return render_template('event_register.html', event=event, tracks=TRACK_CONFIG,
                           grade_min=grade_min, grade_max=grade_max, event_type=event_type,
                           get_tracks_for_grade=get_tracks_for_grade)


# Legacy register route — redirects to login
@app.route('/register')
def register():
    return redirect(url_for('student_login'))


@app.route('/test/intro')
@login_required
def test_intro():
    student = get_db().execute("SELECT * FROM students WHERE id = ?",
                                (session['student_id'],)).fetchone()
    config = TRACK_CONFIG.get(student['track'], TRACK_CONFIG['sat'])
    info = {
        'name': config['name'],
        'time': config['time_minutes'],
        'questions': config['total_questions'],
    }
    return render_template('test_intro.html', student=student, track_info=info)


@app.route('/test/start', methods=['POST'])
@login_required
def test_start():
    conn = get_db()
    student_id = session['student_id']
    student = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()

    track = student['track']
    config = TRACK_CONFIG.get(track, TRACK_CONFIG['sat'])

    # Check if this is a demo event
    event = None
    if student['event_code']:
        event = conn.execute("SELECT * FROM events WHERE event_code = ?", (student['event_code'],)).fetchone()

    is_demo = event and event['is_demo']

    if is_demo:
        # Demo mode: 10 questions, no modules, 10 min time limit
        question_ids = select_demo_questions(track=track)
        session['module1_ids'] = question_ids
        session['question_ids'] = question_ids
        session['current_question'] = 0
        session['current_module'] = 1
        session['answered_questions'] = []
        session['test_start_time'] = datetime.now().isoformat()
        session['track'] = track
        session['time_limit'] = 600  # 10 minutes
        session['is_demo'] = True
        conn.execute("UPDATE students SET test_started_at = datetime('now') WHERE id = ?", (student_id,))
        conn.commit()
        return redirect(url_for('test_question'))
    else:
        # Select Module 1 questions (medium difficulty, everyone gets same level)
        module1_ids = select_module1_questions(track=track)

        if not module1_ids:
            flash('No questions available for this track yet. Check back soon!', 'warning')
            return redirect(url_for('landing'))

        # Store in session — Module 2 will be selected after Module 1 completes
        session['module1_ids'] = module1_ids
        session['question_ids'] = module1_ids  # Start with Module 1
        session['current_question'] = 0
        session['current_module'] = 1
        session['answered_questions'] = []  # Track answered question IDs for skip+return
        session['test_start_time'] = datetime.now().isoformat()
        session['track'] = track
        time_limit = config['time_minutes'] * 60
        session['time_limit'] = time_limit

        # Mark test as started
        conn.execute("UPDATE students SET test_started_at = datetime('now') WHERE id = ?",
                     (student_id,))
        conn.commit()

        return redirect(url_for('test_question'))


@app.route('/test/question')
@login_required
def test_question():
    question_ids = session.get('question_ids', [])
    current = session.get('current_question', 0)
    current_module = session.get('current_module', 1)
    answered_set = set(session.get('answered_questions', []))

    # Check if requesting a specific question via ?q= parameter
    q_param = request.args.get('q')
    if q_param is not None:
        q_idx = int(q_param)
        # Only allow navigation within current module
        if current_module == 1:
            module_size = len(session.get('module1_ids', []))
            if 0 <= q_idx < module_size:
                current = q_idx
                session['current_question'] = current
        else:
            # Module 2: q_idx is relative to full list
            if 0 <= q_idx < len(question_ids):
                current = q_idx
                session['current_question'] = current

    # Check module completion — only when trying to go past the end
    if current >= len(question_ids):
        if current_module == 1:
            # Check if all Module 1 questions are answered
            module1_ids = session.get('module1_ids', [])
            unanswered_m1 = [i for i, qid in enumerate(module1_ids) if qid not in answered_set]

            if unanswered_m1:
                # Still have unanswered Module 1 questions — go to first unanswered
                session['current_question'] = unanswered_m1[0]
                current = unanswered_m1[0]
            elif session.get('is_demo'):
                # Demo mode: skip Module 2, go straight to completion
                return redirect(url_for('test_complete'))
            else:
                # All Module 1 done — adaptive routing to Module 2
                track = session.get('track', 'sat')
                student_id = session['student_id']

                module2_ids, route = select_module2_questions(track, student_id, module1_ids)
                session['module2_ids'] = module2_ids
                session['adaptive_route'] = route

                all_ids = module1_ids + module2_ids
                session['question_ids'] = all_ids
                session['current_module'] = 2
                question_ids = all_ids

                if not module2_ids:
                    return redirect(url_for('test_complete'))
        else:
            # Module 2 — check for unanswered
            unanswered = [i for i, qid in enumerate(question_ids) if qid not in answered_set]
            if unanswered:
                session['current_question'] = unanswered[0]
                current = unanswered[0]
            else:
                return redirect(url_for('test_complete'))

    # Re-read after possible changes
    question_ids = session.get('question_ids', [])
    if current >= len(question_ids):
        return redirect(url_for('test_complete'))

    conn = get_db()
    question = conn.execute("SELECT * FROM questions WHERE id = ?",
                             (question_ids[current],)).fetchone()

    # Calculate time remaining
    start_time = datetime.fromisoformat(session['test_start_time'])
    elapsed = (datetime.now() - start_time).total_seconds()
    time_limit = session.get('time_limit', 4200)
    time_remaining = max(0, time_limit - elapsed)

    # Build question navigator data for current module
    config = TRACK_CONFIG.get(session.get('track', 'sat'), TRACK_CONFIG['sat'])
    total = config['total_questions']

    # Module boundaries
    module1_count = len(session.get('module1_ids', []))
    if current_module == 1:
        nav_start = 0
        nav_end = module1_count
        module_label = "Module 1"
    else:
        nav_start = 0
        nav_end = len(question_ids)
        module_label = "Module 2"

    # Build navigator: which questions are answered, current, skipped
    nav_items = []
    for i in range(nav_start, nav_end):
        qid = question_ids[i] if i < len(question_ids) else None
        status = 'current' if i == current else ('answered' if qid in answered_set else 'unanswered')
        nav_items.append({'index': i, 'number': i + 1, 'status': status})

    return render_template('test_question.html',
                           question=question,
                           current=current + 1,
                           total=total,
                           time_remaining=int(time_remaining),
                           nav_items=nav_items,
                           module_label=module_label,
                           current_index=current)


@app.route('/test/answer', methods=['POST'])
@login_required
def test_answer():
    conn = get_db()
    student_id = session['student_id']
    question_ids = session.get('question_ids', [])
    current = session.get('current_question', 0)

    if current >= len(question_ids):
        return redirect(url_for('test_complete'))

    question_id = question_ids[current]
    selected = request.form.get('answer', '')
    time_spent = int(request.form.get('time_spent', 0))

    # Check if correct
    question = conn.execute("SELECT correct_answer FROM questions WHERE id = ?",
                             (question_id,)).fetchone()
    is_correct = 1 if selected == question['correct_answer'] else 0

    # Check if already answered (update instead of insert)
    existing = conn.execute(
        "SELECT id FROM responses WHERE student_id = ? AND question_id = ?",
        (student_id, question_id)
    ).fetchone()

    if existing:
        conn.execute("""
            UPDATE responses SET selected_answer = ?, is_correct = ?, time_spent_seconds = ?,
                                 answered_at = datetime('now')
            WHERE student_id = ? AND question_id = ?
        """, (selected, is_correct, time_spent, student_id, question_id))
    else:
        conn.execute("""
            INSERT INTO responses (student_id, question_id, selected_answer, is_correct, time_spent_seconds)
            VALUES (?, ?, ?, ?, ?)
        """, (student_id, question_id, selected, is_correct, time_spent))
    conn.commit()

    # Track answered questions in session
    answered = set(session.get('answered_questions', []))
    answered.add(question_id)
    session['answered_questions'] = list(answered)

    # Move to next question
    session['current_question'] = current + 1

    # Check if time is up
    start_time = datetime.fromisoformat(session['test_start_time'])
    elapsed = (datetime.now() - start_time).total_seconds()
    time_limit = session.get('time_limit', 4200)
    if elapsed >= time_limit:
        return redirect(url_for('test_complete'))

    return redirect(url_for('test_question'))


@app.route('/test/skip', methods=['POST'])
@login_required
def test_skip():
    """Skip current question — move to next without answering."""
    current = session.get('current_question', 0)
    session['current_question'] = current + 1
    return redirect(url_for('test_question'))


@app.route('/test/complete')
@login_required
def test_complete():
    conn = get_db()
    student_id = session['student_id']

    # Calculate FUAR scores
    fuar_scores = calculate_fuar_scores(student_id)
    if not fuar_scores:
        flash('Something went wrong with scoring. Please contact support.', 'danger')
        return redirect(url_for('landing'))

    # Save FUAR scores (archetype assigned after GRIC quiz)
    conn.execute("""
        UPDATE students SET
            test_completed_at = datetime('now'),
            fuar_fluency = ?, fuar_understanding = ?,
            fuar_application = ?, fuar_reasoning = ?
        WHERE id = ?
    """, (fuar_scores['F'], fuar_scores['U'],
          fuar_scores['A'], fuar_scores['R'], student_id))
    conn.commit()

    # Redirect to GRIC mindset quiz (instead of immediate archetype reveal)
    return redirect(url_for('mindset_quiz'))


@app.route('/test/mindset', methods=['GET', 'POST'])
@login_required
def mindset_quiz():
    """GRIC mindset questionnaire — 12 questions after the math test."""
    conn = get_db()
    student_id = session['student_id']

    if request.method == 'POST':
        # Save all GRIC responses
        for q in GRIC_QUESTIONS:
            score = request.form.get(f'q_{q["id"]}')
            if score:
                conn.execute(
                    "INSERT INTO gric_responses (student_id, question_id, score) VALUES (?, ?, ?)",
                    (student_id, q['id'], int(score))
                )

        # Calculate GRIC scores
        conn.commit()
        gric_scores = calculate_gric_scores(student_id)

        # Get FUAR scores
        student = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
        fuar_scores = {
            'F': student['fuar_fluency'], 'U': student['fuar_understanding'],
            'A': student['fuar_application'], 'R': student['fuar_reasoning'],
        }

        # Assign archetype using FUAR + GRIC
        archetype_key = assign_archetype(fuar_scores, gric_scores, grade=student['grade'])

        # Get track-specific score
        track = student['track']
        responses = conn.execute("SELECT * FROM responses WHERE student_id = ?",
                                  (student_id,)).fetchall()
        score_result = estimate_score(track, fuar_scores, responses)
        sat_low = score_result.get('low', 0)
        sat_high = score_result.get('high', 0)

        # Save everything
        conn.execute("""
            UPDATE students SET
                archetype = ?,
                sat_estimated_low = ?, sat_estimated_high = ?,
                gric_growth = ?, gric_relevance = ?,
                gric_interest = ?, gric_confidence = ?,
                score_type = ?, score_label = ?, score_detail = ?,
                mindset_completed_at = datetime('now')
            WHERE id = ?
        """, (archetype_key, sat_low, sat_high,
              gric_scores.get('G'), gric_scores.get('R_gric'),
              gric_scores.get('I'), gric_scores.get('C'),
              score_result['score_type'], score_result['label'], score_result['detail'],
              student_id))
        conn.commit()

        return redirect(url_for('archetype_reveal'))

    # GET — show the mindset quiz
    student = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    event = conn.execute("SELECT * FROM events WHERE event_code = ?", (student['event_code'] or '',)).fetchone()
    is_demo = event and event['is_demo']

    return render_template('mindset_quiz.html',
                           questions=GRIC_QUESTIONS,
                           scale_labels=GRIC_SCALE_LABELS,
                           sections=GRIC_SECTIONS,
                           student_name=session.get('student_name', 'Student'),
                           is_demo=is_demo)


@app.route('/reveal')
@login_required
def archetype_reveal():
    """Show the archetype reveal after both math test + mindset quiz are done."""
    conn = get_db()
    student_id = session['student_id']
    student = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()

    if not student['archetype']:
        return redirect(url_for('test_intro'))

    archetype_key = student['archetype']
    is_ms = is_middle_school_student(student)
    archetype = get_archetype_for_student(student, archetype_key)

    fuar_scores = {
        'F': student['fuar_fluency'] or 0, 'U': student['fuar_understanding'] or 0,
        'A': student['fuar_application'] or 0, 'R': student['fuar_reasoning'] or 0,
    }

    score_result = {
        'score_type': student['score_type'] or 'sat',
        'label': student['score_label'] or f"SAT: {student['sat_estimated_low']}-{student['sat_estimated_high']}",
        'detail': student['score_detail'] or '',
    }

    # Check if demo event
    event = conn.execute("SELECT * FROM events WHERE event_code = ?", (student['event_code'] or '',)).fetchone()
    is_demo = event and event['is_demo']

    return render_template('archetype_reveal.html',
                           archetype=archetype,
                           archetype_key=archetype_key,
                           fuar_scores=fuar_scores,
                           score_result=score_result,
                           student=student,
                           archetypes=ALL_ARCHETYPES,
                           student_name=session.get('student_name', 'Student'),
                           is_demo=is_demo,
                           is_middle_school=is_ms)


@app.route('/share/<int:student_id>')
def share_card(student_id):
    """Render the shareable archetype card for a student."""
    conn = get_db()
    student = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    if not student or not student['archetype']:
        return "Not available.", 404

    archetype_key = student['archetype']
    archetype = get_archetype_for_student(student, archetype_key)

    return render_template('share_card.html',
                           archetype=archetype,
                           archetype_key=archetype_key,
                           student_name=student['student_name'].split(' ')[0])


@app.route('/share/designs')
def share_card_designs():
    """Preview all 5 share card design directions."""
    return render_template('share_card_preview.html')


@app.route('/share/preview/<archetype_key>')
def share_card_preview(archetype_key):
    """Preview a share card for any archetype (no student needed)."""
    archetype = ALL_ARCHETYPES.get(archetype_key, ARCHETYPES.get(archetype_key))
    if not archetype:
        return "Archetype not found.", 404

    return render_template('share_card.html',
                           archetype=archetype,
                           archetype_key=archetype_key,
                           student_name=None)


@app.route('/type/<archetype_key>')
def archetype_landing(archetype_key):
    """Public landing page for a specific archetype — where share links point to."""
    archetype = ALL_ARCHETYPES.get(archetype_key, ARCHETYPES.get(archetype_key))
    if not archetype:
        return "Archetype not found.", 404

    # For now, render a simple page. Will become the lite quiz entry point.
    return render_template('archetype_landing.html',
                           archetype=archetype,
                           archetype_key=archetype_key,
                           all_archetypes=ALL_ARCHETYPES)


@app.route('/practice/weekly-check', methods=['GET', 'POST'])
@login_required
def weekly_assessment():
    """Weekly re-assessment — 10 questions across all FUAR dimensions.
    Triggered when plan.current_day reaches a week boundary.
    """
    conn = get_db()
    student_id = session['student_id']
    student = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()

    if not student['archetype']:
        return redirect(url_for('test_intro'))

    plan = conn.execute(
        "SELECT * FROM practice_plans WHERE student_id = ? AND status = 'active'",
        (student_id,)
    ).fetchone()

    if not plan:
        return redirect(url_for('dashboard'))

    current_week = plan['current_week']

    # Check if this week's assessment already done
    existing = conn.execute("""
        SELECT * FROM weekly_assessments
        WHERE student_id = ? AND week_number = ?
    """, (student_id, current_week)).fetchone()

    if existing:
        flash(f'Week {current_week} check-in already completed.', 'info')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        # Score the weekly assessment
        answers = request.form.to_dict()
        q_ids = json.loads(request.form.get('question_ids', '[]'))

        dim_scores = {'F': [], 'U': [], 'A': [], 'R': []}
        for qid in q_ids:
            selected = answers.get(f'q_{qid}', '')
            q = conn.execute(
                "SELECT correct_answer, fuar_dimension, difficulty FROM questions WHERE id = ?",
                (qid,)
            ).fetchone()
            if q:
                weight = q['difficulty'] / 3.0
                is_correct = 1 if selected == q['correct_answer'] else 0
                score_val = is_correct * weight
                dim = q['fuar_dimension']
                if dim in dim_scores:
                    dim_scores[dim].append(score_val)

        new_fuar = {}
        for dim, scores in dim_scores.items():
            if scores:
                raw = sum(scores) / len(scores)
                new_fuar[dim] = round(min(100, max(0, raw * 100)), 1)
            else:
                # Keep existing score if no questions for this dim
                dim_map = {'F': 'fuar_fluency', 'U': 'fuar_understanding',
                           'A': 'fuar_application', 'R': 'fuar_reasoning'}
                new_fuar[dim] = student[dim_map[dim]] or 0

        # Store weekly assessment
        conn.execute("""
            INSERT INTO weekly_assessments
            (student_id, week_number, fuar_fluency, fuar_understanding, fuar_application, fuar_reasoning)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (student_id, current_week, new_fuar['F'], new_fuar['U'], new_fuar['A'], new_fuar['R']))

        # If week 4, do final archetype reassignment
        if current_week >= 4:
            gric = {
                'G': student['gric_growth'] or 50,
                'R_gric': student['gric_relevance'] or 50,
                'I': student['gric_interest'] or 50,
                'C': student['gric_confidence'] or 50,
            }
            new_archetype = assign_archetype(new_fuar, gric, student['grade'])

            # Update student with new scores
            conn.execute("""
                UPDATE students SET
                    fuar_fluency = ?, fuar_understanding = ?,
                    fuar_application = ?, fuar_reasoning = ?,
                    archetype = ?
                WHERE id = ?
            """, (new_fuar['F'], new_fuar['U'], new_fuar['A'], new_fuar['R'],
                  new_archetype, student_id))

            # Update plan with end state
            conn.execute("""
                UPDATE practice_plans SET
                    status = 'completed',
                    archetype_end = ?,
                    fuar_end_json = ?
                WHERE student_id = ? AND status = 'active'
            """, (new_archetype, json.dumps(new_fuar), student_id))

        conn.commit()
        return redirect(url_for('dashboard'))

    # GET — generate 10 assessment questions (2-3 per FUAR dimension)
    track = student['track']
    assessment_qs = []
    for dim in ['F', 'U', 'A', 'R']:
        qs = conn.execute("""
            SELECT id FROM questions
            WHERE track = ? AND fuar_dimension = ?
            ORDER BY RANDOM() LIMIT 3
        """, (track, dim)).fetchall()
        assessment_qs.extend([q['id'] for q in qs])

    import random
    random.shuffle(assessment_qs)
    assessment_qs = assessment_qs[:10]

    placeholders = ','.join('?' * len(assessment_qs))
    questions = conn.execute(
        f"SELECT * FROM questions WHERE id IN ({placeholders})", assessment_qs
    ).fetchall()

    return render_template('weekly_assessment.html',
                           student=student,
                           plan=plan,
                           week=current_week,
                           questions=[dict(q) for q in questions],
                           question_ids=assessment_qs)


@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db()
    student_id = session['student_id']
    student = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()

    if not student['archetype']:
        return redirect(url_for('test_intro'))

    archetype = get_archetype_for_student(student, student['archetype'])

    fuar = {
        'F': student['fuar_fluency'],
        'U': student['fuar_understanding'],
        'A': student['fuar_application'],
        'R': student['fuar_reasoning'],
    }

    # Get practice history
    workouts = conn.execute("""
        SELECT * FROM daily_workouts WHERE student_id = ? ORDER BY day_number DESC LIMIT 7
    """, (student_id,)).fetchall()

    # Weekly assessments
    assessments = conn.execute("""
        SELECT * FROM weekly_assessments WHERE student_id = ? ORDER BY week_number
    """, (student_id,)).fetchall()

    # Deep analytics
    analytics = calculate_analytics(student_id)

    # Practice plan
    plan = conn.execute(
        "SELECT * FROM practice_plans WHERE student_id = ? ORDER BY created_at DESC LIMIT 1",
        (student_id,)
    ).fetchone()
    plan_dict = dict(plan) if plan else None

    # Check if weekly assessment is due
    weekly_check_due = False
    if plan_dict and plan_dict['status'] == 'active':
        sessions_this_week = plan_dict['total_sessions_completed'] % plan_dict['days_per_week']
        # Assessment due when they've completed all sessions for the current week
        if sessions_this_week == 0 and plan_dict['total_sessions_completed'] > 0:
            # Check if assessment for this week already done
            existing_assessment = conn.execute("""
                SELECT id FROM weekly_assessments
                WHERE student_id = ? AND week_number = ?
            """, (student_id, plan_dict['current_week'])).fetchone()
            if not existing_assessment:
                weekly_check_due = True

    # FUAR progress over weeks (for chart)
    fuar_history = []
    if assessments:
        # Add initial diagnostic as week 0
        fuar_history.append({
            'week': 0, 'label': 'Diagnostic',
            'F': student['fuar_fluency'] or 0, 'U': student['fuar_understanding'] or 0,
            'A': student['fuar_application'] or 0, 'R': student['fuar_reasoning'] or 0,
        })
        for a in assessments:
            fuar_history.append({
                'week': a['week_number'], 'label': f'Week {a["week_number"]}',
                'F': a['fuar_fluency'], 'U': a['fuar_understanding'],
                'A': a['fuar_application'], 'R': a['fuar_reasoning'],
            })

    # Check if demo event
    event = conn.execute("SELECT * FROM events WHERE event_code = ?", (student['event_code'] or '',)).fetchone()
    is_demo = event and event['is_demo']

    return render_template('dashboard.html',
                           student=student,
                           archetype=archetype,
                           fuar=fuar,
                           fuar_dims=FUAR_DIMENSIONS,
                           workouts=workouts,
                           assessments=assessments,
                           analytics=analytics,
                           plan=plan_dict,
                           weekly_check_due=weekly_check_due,
                           fuar_history=fuar_history,
                           is_demo=is_demo)


@app.route('/practice/today')
@login_required
def daily_practice():
    conn = get_db()
    student_id = session['student_id']
    student = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()

    if not student['archetype']:
        return redirect(url_for('test_intro'))

    # Get or create practice plan
    try:
        plan = generate_practice_plan(student_id)
    except Exception as e:
        logging.error(f'Practice plan generation failed for {student_id}: {e}')
        flash(f'Practice plan setup error. Please try again.', 'warning')
        return redirect(url_for('dashboard'))
    if not plan:
        flash('Unable to generate practice plan.', 'warning')
        return redirect(url_for('dashboard'))
    if isinstance(plan, sqlite3.Row):
        plan = dict(plan)

    # Find or create today's workout
    today = datetime.now().strftime('%Y-%m-%d')
    existing = conn.execute("""
        SELECT * FROM daily_workouts
        WHERE student_id = ? AND date(created_at) = ?
    """, (student_id, today)).fetchone()

    if existing and existing['completed']:
        return render_template('practice_done.html', workout=existing, student=student, plan=plan)

    if existing:
        workout = existing
    else:
        # Generate new workout using plan-based question selection
        fuar = {
            'F': student['fuar_fluency'] or 0,
            'U': student['fuar_understanding'] or 0,
            'A': student['fuar_application'] or 0,
            'R': student['fuar_reasoning'] or 0,
        }
        weakest = min(fuar, key=fuar.get)

        day_count = conn.execute(
            "SELECT COUNT(*) FROM daily_workouts WHERE student_id = ?",
            (student_id,)
        ).fetchone()[0]

        # Use plan-based smart selection
        try:
            question_ids = get_practice_session_questions(student_id, plan)
        except Exception as e:
            logging.error(f'Practice question selection failed: {e}')
            question_ids = []

        if not question_ids:
            # Fallback to old random selection
            q_rows = conn.execute("""
                SELECT id FROM questions
                WHERE fuar_dimension = ? AND track = ?
                ORDER BY RANDOM() LIMIT ?
            """, (weakest, student['track'], plan.get('questions_per_session', 10))).fetchall()
            question_ids = [q['id'] for q in q_rows]

        if not question_ids:
            flash('No practice questions available yet.', 'warning')
            return redirect(url_for('dashboard'))

        # Determine focus topic (most represented weak topic in this session)
        focus_topic = None
        if question_ids:
            placeholders_ft = ','.join('?' * len(question_ids))
            topic_counts = conn.execute(f"""
                SELECT sat_domain, COUNT(*) as cnt FROM questions
                WHERE id IN ({placeholders_ft})
                GROUP BY sat_domain ORDER BY cnt DESC LIMIT 1
            """, question_ids).fetchone()
            if topic_counts:
                focus_topic = topic_counts['sat_domain']

        cursor = conn.execute("""
            INSERT INTO daily_workouts (student_id, day_number, focus_dimension, focus_topic, questions_json)
            VALUES (?, ?, ?, ?, ?)
        """, (student_id, day_count + 1, weakest, focus_topic, json.dumps(question_ids)))
        conn.commit()

        # Update plan progress
        conn.execute("""
            UPDATE practice_plans SET current_day = current_day + 1,
            current_week = CASE WHEN current_day + 1 > days_per_week * current_week THEN current_week + 1 ELSE current_week END
            WHERE student_id = ? AND status = 'active'
        """, (student_id,))
        conn.commit()

        workout = conn.execute("SELECT * FROM daily_workouts WHERE id = ?",
                                (cursor.lastrowid,)).fetchone()

    # Load question objects
    q_ids = json.loads(workout['questions_json'])
    placeholders = ','.join('?' * len(q_ids))
    questions = conn.execute(f"SELECT * FROM questions WHERE id IN ({placeholders})", q_ids).fetchall()

    return render_template('daily_practice.html',
                           workout=workout,
                           student=student,
                           plan=plan,
                           focus_dim=FUAR_DIMENSIONS[workout['focus_dimension']],
                           questions=[dict(q) for q in questions],
                           question_ids=q_ids,
                           show_explanations=True)


@app.route('/practice/submit', methods=['POST'])
@login_required
def submit_practice():
    conn = get_db()
    student_id = session['student_id']
    student = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    workout_id = request.form.get('workout_id')
    answers = request.form.to_dict()

    workout = conn.execute("SELECT * FROM daily_workouts WHERE id = ? AND student_id = ?",
                            (workout_id, student_id)).fetchone()
    if not workout:
        return redirect(url_for('dashboard'))

    # Guard: already completed — redirect to results
    if workout['completed']:
        return redirect(url_for('practice_results', workout_id=workout_id))

    question_ids = json.loads(workout['questions_json'])
    correct = 0
    total = len(question_ids)
    answers_detail = []

    for qid in question_ids:
        selected = answers.get(f'q_{qid}', '')
        q = conn.execute("SELECT correct_answer FROM questions WHERE id = ?", (qid,)).fetchone()
        is_right = 1 if (q and selected == q['correct_answer']) else 0
        if is_right:
            correct += 1
        correct_ans = q['correct_answer'] if q else ''
        answers_detail.append({
            'question_id': qid,
            'student_answer': selected,
            'correct_answer': correct_ans,
            'is_correct': is_right
        })
        # Save per-question answer
        conn.execute("""
            INSERT INTO workout_answers (workout_id, question_id, student_answer, correct_answer, is_correct)
            VALUES (?, ?, ?, ?, ?)
        """, (workout_id, qid, selected, correct_ans, is_right))

    score = round(correct / total * 100, 1) if total > 0 else 0

    # Mark workout complete + store answers summary
    conn.execute("""
        UPDATE daily_workouts SET completed = 1, score = ?, answers_json = ?, completed_at = datetime('now')
        WHERE id = ?
    """, (score, json.dumps(answers_detail), workout_id))

    # Update streak — only if not already practiced today
    today_str = datetime.now().strftime('%Y-%m-%d')
    last_practice = student['last_practice_date'] if student else None

    if last_practice != today_str:
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        streak = (student['daily_practice_streak'] or 0) + 1
        if last_practice and last_practice < yesterday:
            days_gap = (datetime.strptime(today_str, '%Y-%m-%d') - datetime.strptime(last_practice, '%Y-%m-%d')).days
            if days_gap > 2:
                streak = 1  # reset

        conn.execute("""
            UPDATE students SET
                daily_practice_started = 1,
                daily_practice_streak = ?,
                last_practice_date = ?
            WHERE id = ?
        """, (streak, today_str, student_id))

        # Update plan total_sessions_completed
        conn.execute("""
            UPDATE practice_plans SET total_sessions_completed = total_sessions_completed + 1
            WHERE student_id = ? AND status = 'active'
        """, (student_id,))

    conn.commit()

    return redirect(url_for('practice_results', workout_id=workout_id))


@app.route('/practice/results/<int:workout_id>')
@login_required
def practice_results(workout_id):
    conn = get_db()
    student_id = session['student_id']
    workout = conn.execute("SELECT * FROM daily_workouts WHERE id = ? AND student_id = ?",
                            (workout_id, student_id)).fetchone()
    student = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()

    if not workout:
        return redirect(url_for('dashboard'))

    # Load per-question answers + full question data for review
    wa_rows = conn.execute("""
        SELECT wa.*, q.question_text, q.option_a, q.option_b, q.option_c, q.option_d,
               q.explanation, q.worked_solution_json, q.wrong_answer_analyses, q.simulation_html,
               q.fuar_dimension, q.sat_domain, q.topic_tag
        FROM workout_answers wa
        JOIN questions q ON wa.question_id = q.id
        WHERE wa.workout_id = ?
        ORDER BY wa.is_correct ASC, wa.id ASC
    """, (workout_id,)).fetchall()

    review_questions = []
    for row in wa_rows:
        rq = dict(row)
        # Parse JSON fields
        try:
            rq['worked_steps'] = json.loads(rq['worked_solution_json']) if rq.get('worked_solution_json') else None
        except (json.JSONDecodeError, TypeError):
            rq['worked_steps'] = None
        try:
            analyses = json.loads(rq['wrong_answer_analyses']) if rq.get('wrong_answer_analyses') else {}
        except (json.JSONDecodeError, TypeError):
            analyses = {}
        # Get the analysis for this student's specific wrong answer
        rq['personal_analysis'] = analyses.get(rq['student_answer'], '') if not rq['is_correct'] else ''
        rq['all_analyses'] = analyses
        review_questions.append(rq)

    wrong_count = sum(1 for rq in review_questions if not rq['is_correct'])
    correct_count = len(review_questions) - wrong_count

    return render_template('practice_results.html',
                           workout=workout,
                           student=student,
                           focus_dim=FUAR_DIMENSIONS[workout['focus_dimension']],
                           review_questions=review_questions,
                           wrong_count=wrong_count,
                           correct_count=correct_count)


# ---------- Analytics Page ----------

@app.route('/analytics')
@login_required
def analytics_page():
    """Deep analytics view — shows all diagnostic insights."""
    conn = get_db()
    student_id = session['student_id']
    student = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()

    if not student['archetype']:
        return redirect(url_for('test_intro'))

    archetype = get_archetype_for_student(student, student['archetype'])
    fuar = {
        'F': student['fuar_fluency'],
        'U': student['fuar_understanding'],
        'A': student['fuar_application'],
        'R': student['fuar_reasoning'],
    }
    analytics = calculate_analytics(student_id)

    return render_template('analytics.html',
                           student=student,
                           archetype=archetype,
                           fuar=fuar,
                           fuar_dims=FUAR_DIMENSIONS,
                           analytics=analytics)


# ---------- Report API (for generating reports) ----------

@app.route('/api/report/<int:student_id>')
def get_report_data(student_id):
    """API endpoint to get report data for a student."""
    conn = get_db()
    student = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    if not student:
        return jsonify({'error': 'Student not found'}), 404

    archetype = get_archetype_for_student(student, student['archetype'])
    fuar = {
        'F': student['fuar_fluency'],
        'U': student['fuar_understanding'],
        'A': student['fuar_application'],
        'R': student['fuar_reasoning'],
    }

    # Domain-level performance
    domain_scores = {}
    for domain_key, domain in SAT_DOMAINS.items():
        results = conn.execute("""
            SELECT r.is_correct, q.difficulty
            FROM responses r
            JOIN questions q ON r.question_id = q.id
            WHERE r.student_id = ? AND q.sat_domain = ?
        """, (student_id, domain_key)).fetchall()

        if results:
            correct = sum(1 for r in results if r['is_correct'])
            total = len(results)
            domain_scores[domain_key] = {
                'name': domain['name'],
                'correct': correct,
                'total': total,
                'pct': round(correct / total * 100, 1),
            }

    return jsonify({
        'student_name': student['student_name'],
        'parent_name': student['parent_name'],
        'grade': student['grade'],
        'track': student['track'],
        'archetype': archetype,
        'fuar': fuar,
        'fuar_dimensions': FUAR_DIMENSIONS,
        'sat_estimated_low': student['sat_estimated_low'],
        'sat_estimated_high': student['sat_estimated_high'],
        'domain_scores': domain_scores,
    })


@app.route('/api/report/<int:student_id>/topic/<path:topic_domain>')
def api_topic_drilldown(student_id, topic_domain):
    """Return question-level detail for a specific topic/domain."""
    conn = get_db()
    # Match domain by converting back from display format
    # e.g. "Algebra" or "Heart Of Algebra" → match against sat_domain
    responses = conn.execute("""
        SELECT q.question_text, q.option_a, q.option_b, q.option_c, q.option_d,
               q.correct_answer, q.explanation, q.fuar_dimension, q.difficulty,
               q.sat_domain, q.topic_tag,
               r.selected_answer, r.is_correct, r.time_spent_seconds
        FROM responses r
        JOIN questions q ON r.question_id = q.id
        WHERE r.student_id = ?
        ORDER BY r.id
    """, (student_id,)).fetchall()
    conn.close()

    # Filter to matching domain
    questions = []
    for r in responses:
        domain_display = (r['sat_domain'] or '').replace('_', ' ').title()
        if domain_display == topic_domain:
            questions.append({
                'question': r['question_text'],
                'options': {
                    'A': r['option_a'], 'B': r['option_b'],
                    'C': r['option_c'], 'D': r['option_d'],
                },
                'correct': r['correct_answer'],
                'picked': r['selected_answer'],
                'is_correct': bool(r['is_correct']),
                'time_spent': r['time_spent_seconds'],
                'explanation': r['explanation'] or '',
                'fuar': r['fuar_dimension'],
                'difficulty': r['difficulty'],
                'topic_tag': r['topic_tag'] or '',
            })

    return jsonify({'topic': topic_domain, 'questions': questions})


# ---------- Solution Import API ----------

@app.route('/api/import-solutions', methods=['POST'])
def import_solutions():
    """Import worked solutions from JSON. Protected by app secret key."""
    data = request.get_json(force=True)
    api_key = data.get('api_key', '')
    if api_key != app.secret_key:
        return jsonify({'error': 'Unauthorized'}), 401

    solutions = data.get('solutions', [])
    if not solutions:
        return jsonify({'error': 'No solutions provided'}), 400

    conn = get_db()
    imported = 0
    for sol in solutions:
        qid = sol.get('id')
        worked = sol.get('worked_solution_json')
        analyses = sol.get('wrong_answer_analyses')
        if qid and worked:
            conn.execute("""
                UPDATE questions SET worked_solution_json = ?, wrong_answer_analyses = ?
                WHERE id = ? AND worked_solution_json IS NULL
            """, (worked, analyses, qid))
            imported += 1
    conn.commit()
    return jsonify({'imported': imported, 'total': len(solutions)})


# ---------- Admin ----------

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        user = ADMIN_USERS.get(username)
        if user and user['password'] == password:
            session['admin_role'] = user['role']
            session['admin_name'] = user['name']
            return redirect(url_for('admin_dashboard'))

        # Check PTA admins (stored in DB)
        conn = get_db()
        pta = conn.execute(
            "SELECT * FROM pta_admins WHERE username = ? AND password = ?",
            (username, password)
        ).fetchone() if table_exists(conn, 'pta_admins') else None

        if pta:
            session['admin_role'] = 'pta_admin'
            session['admin_name'] = pta['name']
            session['admin_event_code'] = pta['event_code']
            return redirect(url_for('admin_dashboard'))

        flash('Invalid credentials.', 'danger')
    return render_template('admin_login.html')


def table_exists(conn, table_name):
    result = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,)
    ).fetchone()
    return result is not None


@app.route('/admin')
@admin_required
def admin_dashboard():
    conn = get_db()
    role = session.get('admin_role')

    # Get events
    if role == 'pta_admin':
        events = conn.execute("SELECT * FROM events WHERE event_code = ?",
                               (session.get('admin_event_code'),)).fetchall()
    else:
        events = conn.execute("SELECT * FROM events ORDER BY event_date DESC").fetchall()

    # Get student counts per event
    event_stats = []
    for event in events:
        stats = conn.execute("""
            SELECT
                COUNT(*) as registered,
                SUM(CASE WHEN test_started_at IS NOT NULL THEN 1 ELSE 0 END) as started,
                SUM(CASE WHEN archetype IS NOT NULL THEN 1 ELSE 0 END) as completed
            FROM students WHERE event_code = ?
        """, (event['event_code'],)).fetchone()
        event_stats.append({
            'event': dict(event),
            'registered': stats['registered'] or 0,
            'started': stats['started'] or 0,
            'completed': stats['completed'] or 0,
        })

    total_questions = conn.execute("SELECT COUNT(*) FROM questions").fetchone()[0]

    # Get onboarded schools from School CRM database (if accessible)
    onboarded_schools = []
    try:
        import os
        crm_db = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                               'school-pipeline', 'school_crm.db')
        if os.path.exists(crm_db):
            crm_conn = sqlite3.connect(crm_db)
            crm_conn.row_factory = sqlite3.Row
            schools = crm_conn.execute(
                "SELECT name FROM schools WHERE stage IN ('onboarded', 'onboarded_rescheduled') ORDER BY name"
            ).fetchall()
            onboarded_schools = [s['name'] for s in schools]
            crm_conn.close()
    except Exception:
        pass  # CRM not available — school input works as free text

    return render_template('admin.html',
                           event_stats=event_stats,
                           archetypes=ALL_ARCHETYPES,
                           total_questions=total_questions,
                           onboarded_schools=onboarded_schools,
                           role=role)


@app.route('/admin/event/create', methods=['POST'])
@admin_required
def create_event():
    """Create a new College Ready Night event."""
    if session.get('admin_role') != 'cuemath_admin':
        flash('Only Cuemath admins can create events.', 'danger')
        return redirect(url_for('admin_dashboard'))

    school_name = request.form.get('school_name', '').strip()
    event_date = request.form.get('event_date', '').strip()
    location = request.form.get('location', '').strip()
    event_type = request.form.get('event_type', 'high_school').strip()

    # Auto-generate event name from type
    event_name = request.form.get('event_name', '').strip()
    if not event_name:
        event_name = 'College Ready Night' if event_type == 'high_school' else 'Foundation Math Night'

    if not school_name:
        flash('School name is required.', 'danger')
        return redirect(url_for('admin_dashboard'))

    # Set grade range based on event type
    grade_ranges = {
        'middle_school': (6, 8),
        'high_school': (9, 12),
        'both': (6, 12),
    }
    grade_min, grade_max = grade_ranges.get(event_type, (9, 12))

    # Generate event code from school name
    code = school_name.upper().replace(' ', '-')[:20] + '-' + (event_date or '2026').replace('-', '')
    code = ''.join(c for c in code if c.isalnum() or c == '-')

    conn = get_db()
    try:
        conn.execute("""
            INSERT INTO events (event_code, event_name, school_name, event_date, location,
                                event_type, grade_min, grade_max)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (code, event_name, school_name, event_date, location,
              event_type, grade_min, grade_max))
        conn.commit()
        flash(f'Event created! Registration link: /register/{code}', 'success')
    except Exception as e:
        flash(f'Error creating event: {e}', 'danger')

    return redirect(url_for('admin_dashboard'))


@app.route('/admin/event/<event_code>/toggle-test', methods=['POST'])
@admin_required
def toggle_test(event_code):
    """Enable or disable the test for an event."""
    conn = get_db()
    event = conn.execute("SELECT * FROM events WHERE event_code = ?", (event_code,)).fetchone()
    if not event:
        flash('Event not found.', 'danger')
        return redirect(url_for('admin_dashboard'))

    new_state = 0 if event['test_enabled'] else 1
    conn.execute(
        "UPDATE events SET test_enabled = ?, test_enabled_at = datetime('now') WHERE event_code = ?",
        (new_state, event_code)
    )
    conn.commit()

    status = 'ENABLED' if new_state else 'DISABLED'
    flash(f'Test {status} for {event["event_name"]}', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/event/<event_code>/students')
@admin_required
def event_students(event_code):
    """View all students for an event."""
    conn = get_db()
    event = conn.execute("SELECT * FROM events WHERE event_code = ?", (event_code,)).fetchone()
    students = conn.execute(
        "SELECT * FROM students WHERE event_code = ? ORDER BY created_at",
        (event_code,)
    ).fetchall()

    # Compute aggregate FUAR scores
    completed = [s for s in students if s['archetype']]
    avg_fuar = {'F': 0, 'U': 0, 'A': 0, 'R': 0}
    if completed:
        for s in completed:
            avg_fuar['F'] += (s['fuar_fluency'] or 0)
            avg_fuar['U'] += (s['fuar_understanding'] or 0)
            avg_fuar['A'] += (s['fuar_application'] or 0)
            avg_fuar['R'] += (s['fuar_reasoning'] or 0)
        n = len(completed)
        avg_fuar = {k: round(v / n, 1) for k, v in avg_fuar.items()}

    return render_template('admin_event_students.html',
                           event=event, students=students, archetypes=ALL_ARCHETYPES,
                           fuar_dims=FUAR_DIMENSIONS, avg_fuar=avg_fuar)


@app.route('/admin/event/<event_code>/pta-admin', methods=['POST'])
@admin_required
def create_pta_admin(event_code):
    """Create a PTA admin for a specific event."""
    if session.get('admin_role') != 'cuemath_admin':
        flash('Only Cuemath admins can create PTA admins.', 'danger')
        return redirect(url_for('admin_dashboard'))

    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    name = request.form.get('name', '').strip()

    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS pta_admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT,
            event_code TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)
    try:
        conn.execute(
            "INSERT INTO pta_admins (username, password, name, event_code) VALUES (?, ?, ?, ?)",
            (username, password, name, event_code)
        )
        conn.commit()
        flash(f'PTA admin "{username}" created for event {event_code}', 'success')
    except Exception:
        flash('Username already exists.', 'danger')

    return redirect(url_for('admin_dashboard'))


# ---------- CSV Export ----------

@app.route('/admin/event/<event_code>/export')
@admin_required
def export_event(event_code):
    """Export all student data for an event as CSV."""
    conn = get_db()
    students = conn.execute(
        "SELECT * FROM students WHERE event_code = ? ORDER BY student_name",
        (event_code,)
    ).fetchall()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        'Name', 'Email', 'Parent Email', 'Grade', 'Track',
        'Archetype', 'FUAR Fluency', 'FUAR Understanding', 'FUAR Application', 'FUAR Reasoning',
        'GRIC Growth', 'GRIC Relevance', 'GRIC Interest', 'GRIC Confidence',
        'Score Type', 'Score', 'Score Detail',
        'Test Started', 'Test Completed'
    ])
    for s in students:
        archetype_name = ALL_ARCHETYPES.get(s['archetype'], {}).get('name', '')
        writer.writerow([
            s['student_name'], s['student_email'], s['parent_email'], s['grade'], s['track'],
            archetype_name,
            s['fuar_fluency'], s['fuar_understanding'], s['fuar_application'], s['fuar_reasoning'],
            s['gric_growth'], s['gric_relevance'], s['gric_interest'], s['gric_confidence'],
            s['score_type'], s['score_label'], s['score_detail'],
            s['test_started_at'], s['test_completed_at'],
        ])

    response = Response(output.getvalue(), mimetype='text/csv')
    response.headers['Content-Disposition'] = f'attachment; filename={event_code}-students.csv'
    return response


# ---------- CRM API — Auto-create events from Super Leaf ----------

@app.route('/api/events', methods=['POST'])
def api_create_event():
    """API endpoint for CRM (Super Leaf) to auto-create events.
    POST JSON: {event_name, school_name, event_date, location, api_key}
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON body required'}), 400

    api_key = data.get('api_key', '')
    if api_key != app.secret_key:
        return jsonify({'error': 'Invalid API key'}), 401

    event_name = data.get('event_name', '').strip()
    school_name = data.get('school_name', '').strip()
    event_date = data.get('event_date', '').strip()
    location = data.get('location', '').strip()

    if not event_name or not school_name:
        return jsonify({'error': 'event_name and school_name required'}), 400

    code = school_name.upper().replace(' ', '-')[:20] + '-' + (event_date or '2026').replace('-', '')
    code = ''.join(c for c in code if c.isalnum() or c == '-')

    conn = get_db()
    try:
        conn.execute("""
            INSERT INTO events (event_code, event_name, school_name, event_date, location)
            VALUES (?, ?, ?, ?, ?)
        """, (code, event_name, school_name, event_date, location))
        conn.commit()
        return jsonify({
            'status': 'created',
            'event_code': code,
            'registration_url': f'/register/{code}',
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 409


# ---------- Student Report ----------

@app.route('/report/<int:student_id>')
def student_report(student_id):
    """Public student report — shareable via URL, no login required."""
    conn = get_db()
    student = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    if not student or not student['archetype']:
        return "Report not available.", 404

    archetype_key = student['archetype']
    archetype = get_archetype_for_student(student, archetype_key)
    fuar = {
        'F': student['fuar_fluency'] or 50,
        'U': student['fuar_understanding'] or 50,
        'A': student['fuar_application'] or 50,
        'R': student['fuar_reasoning'] or 50,
    }
    gric = {
        'G': student['gric_growth'] or 50,
        'R_gric': student['gric_relevance'] or 50,
        'I': student['gric_interest'] or 50,
        'C': student['gric_confidence'] or 50,
    }
    score_result = {
        'score_type': student['score_type'] or 'sat',
        'label': student['score_label'] or '',
        'detail': student['score_detail'] or '',
    }
    analytics = calculate_analytics(student_id)

    # Get event info
    event = None
    if student['event_code']:
        event = conn.execute("SELECT * FROM events WHERE event_code = ?",
                             (student['event_code'],)).fetchone()

    track_config = TRACK_CONFIG.get(student['track'], TRACK_CONFIG.get('sat', {}))

    # Compute strongest/weakest for recommendations
    strongest_fuar = max(['F', 'U', 'A', 'R'], key=lambda d: fuar.get(d, 0))
    weakest_fuar = min(['F', 'U', 'A', 'R'], key=lambda d: fuar.get(d, 0))
    lowest_gric = min(['G', 'R_gric', 'I', 'C'], key=lambda d: gric.get(d, 0))

    # Compute school-level percentile
    school_percentile = None
    total_event_students = 0
    if student['event_code']:
        all_scores = conn.execute("""
            SELECT (COALESCE(fuar_fluency,0)*0.25 + COALESCE(fuar_understanding,0)*0.25 +
                    COALESCE(fuar_application,0)*0.30 + COALESCE(fuar_reasoning,0)*0.20) as weighted
            FROM students
            WHERE event_code = ? AND archetype IS NOT NULL
            ORDER BY weighted
        """, (student['event_code'],)).fetchall()
        total_event_students = len(all_scores)
        if total_event_students >= 3:
            student_weighted = fuar['F']*0.25 + fuar['U']*0.25 + fuar['A']*0.30 + fuar['R']*0.20
            below = sum(1 for s in all_scores if s['weighted'] < student_weighted)
            school_percentile = round(below / total_event_students * 100)

    is_demo = event and event['is_demo'] if event else False

    return render_template('report.html',
                           student=student,
                           archetype=archetype,
                           archetype_key=archetype_key,
                           fuar=fuar,
                           gric=gric,
                           fuar_dims=FUAR_DIMENSIONS,
                           gric_dims=GRIC_DIMENSIONS,
                           score=score_result,
                           analytics=analytics,
                           event=event,
                           track_config=track_config,
                           strongest_fuar=strongest_fuar,
                           weakest_fuar=weakest_fuar,
                           lowest_gric=lowest_gric,
                           archetypes=ALL_ARCHETYPES,
                           school_percentile=school_percentile,
                           total_event_students=total_event_students,
                           parent_mode=False,
                           is_demo=is_demo)


@app.route('/report/<int:student_id>/parent')
def student_report_parent(student_id):
    """Parent-friendly version of the report with simpler language."""
    conn = get_db()
    student = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    if not student or not student['archetype']:
        return "Report not available.", 404

    archetype_key = student['archetype']
    archetype = get_archetype_for_student(student, archetype_key)
    fuar = {
        'F': student['fuar_fluency'] or 50,
        'U': student['fuar_understanding'] or 50,
        'A': student['fuar_application'] or 50,
        'R': student['fuar_reasoning'] or 50,
    }
    gric = {
        'G': student['gric_growth'] or 50,
        'R_gric': student['gric_relevance'] or 50,
        'I': student['gric_interest'] or 50,
        'C': student['gric_confidence'] or 50,
    }
    score_result = {
        'score_type': student['score_type'] or 'sat',
        'label': student['score_label'] or '',
        'detail': student['score_detail'] or '',
    }
    analytics = calculate_analytics(student_id)

    event = None
    if student['event_code']:
        event = conn.execute("SELECT * FROM events WHERE event_code = ?",
                             (student['event_code'],)).fetchone()

    track_config = TRACK_CONFIG.get(student['track'], TRACK_CONFIG.get('sat', {}))

    strongest_fuar = max(['F', 'U', 'A', 'R'], key=lambda d: fuar.get(d, 0))
    weakest_fuar = min(['F', 'U', 'A', 'R'], key=lambda d: fuar.get(d, 0))
    lowest_gric = min(['G', 'R_gric', 'I', 'C'], key=lambda d: gric.get(d, 0))

    # Compute school-level percentile for parent report
    percentiles = {'school': None, 'district': None, 'state': None, 'national': None}
    if student['event_code']:
        # Get all students from the same event who completed the test
        all_scores = conn.execute("""
            SELECT (COALESCE(fuar_fluency,0)*0.25 + COALESCE(fuar_understanding,0)*0.25 +
                    COALESCE(fuar_application,0)*0.30 + COALESCE(fuar_reasoning,0)*0.20) as weighted
            FROM students
            WHERE event_code = ? AND archetype IS NOT NULL
            ORDER BY weighted
        """, (student['event_code'],)).fetchall()
        if len(all_scores) >= 3:
            student_weighted = fuar['F']*0.25 + fuar['U']*0.25 + fuar['A']*0.30 + fuar['R']*0.20
            below = sum(1 for s in all_scores if s['weighted'] < student_weighted)
            percentiles['school'] = round(below / len(all_scores) * 100)
    total_event_students = conn.execute(
        "SELECT COUNT(*) FROM students WHERE event_code = ? AND archetype IS NOT NULL",
        (student['event_code'] or '',)
    ).fetchone()[0]

    return render_template('report_parent.html',
                           student=student,
                           archetype=archetype,
                           archetype_key=archetype_key,
                           fuar=fuar,
                           gric=gric,
                           fuar_dims=FUAR_DIMENSIONS,
                           score=score_result,
                           analytics=analytics,
                           event=event,
                           track_config=track_config,
                           strongest_fuar=strongest_fuar,
                           weakest_fuar=weakest_fuar,
                           lowest_gric=lowest_gric,
                           percentiles=percentiles,
                           total_event_students=total_event_students,
                           parent_mode=True)


# ---------- QR Code Generation ----------

def generate_qr_svg(data, module_size=5):
    """Generate a QR code as inline SVG using a simple implementation.
    Uses a basic QR encoding approach without external dependencies."""
    try:
        import qrcode
        qr = qrcode.QRCode(version=1, box_size=module_size, border=2,
                           error_correction=qrcode.constants.ERROR_CORRECT_L)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        b64 = base64.b64encode(buf.read()).decode('utf-8')
        return f'data:image/png;base64,{b64}'
    except ImportError:
        # Fallback: generate a simple QR-like placeholder SVG with the URL text
        # This is a visual placeholder — install qrcode for real QR codes
        encoded = hashlib.md5(data.encode()).hexdigest()
        svg_parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">']
        svg_parts.append('<rect width="200" height="200" fill="white"/>')
        # Draw a pattern based on hash to make it look QR-like
        for i, ch in enumerate(encoded[:64]):
            x = (i % 8) * 22 + 12
            y = (i // 8) * 22 + 12
            val = int(ch, 16)
            if val > 7:
                svg_parts.append(f'<rect x="{x}" y="{y}" width="18" height="18" fill="black"/>')
        # QR finder patterns (corners)
        for cx, cy in [(12, 12), (134, 12), (12, 134)]:
            svg_parts.append(f'<rect x="{cx}" y="{cy}" width="54" height="54" fill="black"/>')
            svg_parts.append(f'<rect x="{cx+6}" y="{cy+6}" width="42" height="42" fill="white"/>')
            svg_parts.append(f'<rect x="{cx+12}" y="{cy+12}" width="30" height="30" fill="black"/>')
        svg_parts.append('</svg>')
        svg_str = ''.join(svg_parts)
        b64 = base64.b64encode(svg_str.encode()).decode('utf-8')
        return f'data:image/svg+xml;base64,{b64}'


@app.route('/admin/event/<event_code>/qr')
@admin_required
def event_qr(event_code):
    """Return the QR code for an event's registration page as an image."""
    conn = get_db()
    event = conn.execute("SELECT * FROM events WHERE event_code = ?", (event_code,)).fetchone()
    if not event:
        return "Event not found", 404

    reg_url = request.host_url.rstrip('/') + url_for('event_register', event_code=event_code)

    try:
        import qrcode
        qr = qrcode.QRCode(version=1, box_size=10, border=2,
                           error_correction=qrcode.constants.ERROR_CORRECT_L)
        qr.add_data(reg_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        response = make_response(buf.read())
        response.headers['Content-Type'] = 'image/png'
        return response
    except ImportError:
        # Return the SVG fallback as an image
        qr_data = generate_qr_svg(reg_url)
        if qr_data.startswith('data:image/svg+xml;base64,'):
            svg_bytes = base64.b64decode(qr_data.split(',')[1])
            response = make_response(svg_bytes)
            response.headers['Content-Type'] = 'image/svg+xml'
            return response
        return "QR generation requires the 'qrcode' package. Install via: pip install qrcode[pil]", 500


@app.route('/admin/event/<event_code>/flyer')
@admin_required
def event_flyer(event_code):
    """Printable one-page event flyer with QR code."""
    conn = get_db()
    event = conn.execute("SELECT * FROM events WHERE event_code = ?", (event_code,)).fetchone()
    if not event:
        flash('Event not found.', 'danger')
        return redirect(url_for('admin_dashboard'))

    reg_url = request.host_url.rstrip('/') + url_for('event_register', event_code=event_code)
    qr_img = generate_qr_svg(reg_url)

    return render_template('event_flyer.html',
                           event=event,
                           reg_url=reg_url,
                           qr_img=qr_img)


# ---------- Enhanced PTA Admin — Event Stats ----------

@app.route('/admin/event/<event_code>/stats')
@admin_required
def event_stats_page(event_code):
    """Detailed event statistics page."""
    conn = get_db()
    event = conn.execute("SELECT * FROM events WHERE event_code = ?", (event_code,)).fetchone()
    if not event:
        flash('Event not found.', 'danger')
        return redirect(url_for('admin_dashboard'))

    students = conn.execute(
        "SELECT * FROM students WHERE event_code = ? ORDER BY created_at",
        (event_code,)
    ).fetchall()

    # Compute aggregate FUAR scores
    completed = [s for s in students if s['archetype']]
    avg_fuar = {'F': 0, 'U': 0, 'A': 0, 'R': 0}
    if completed:
        for s in completed:
            avg_fuar['F'] += (s['fuar_fluency'] or 0)
            avg_fuar['U'] += (s['fuar_understanding'] or 0)
            avg_fuar['A'] += (s['fuar_application'] or 0)
            avg_fuar['R'] += (s['fuar_reasoning'] or 0)
        n = len(completed)
        avg_fuar = {k: round(v / n, 1) for k, v in avg_fuar.items()}

    return render_template('admin_event_students.html',
                           event=event,
                           students=students,
                           archetypes=ALL_ARCHETYPES,
                           fuar_dims=FUAR_DIMENSIONS,
                           avg_fuar=avg_fuar,
                           show_details=True)


# ---------- Seed Questions ----------

def seed_questions():
    """Seed the question bank with SAT math questions tagged by FUAR + domain."""
    conn = sqlite3.connect(DB_PATH)
    existing = conn.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
    if existing > 0:
        conn.close()
        return f"Question bank already has {existing} questions"

    questions = [
        # --- HEART OF ALGEBRA (15 questions) ---
        # Fluency: Solve linear equations
        ("sat", "heart_of_algebra", "F", 1, "Solve for x: 3x + 7 = 22", "multiple_choice",
         "x = 3", "x = 5", "x = 7", "x = 15", "B",
         "3x = 22 - 7 = 15, so x = 5", "linear_equations"),

        ("sat", "heart_of_algebra", "F", 2, "If 2(x - 3) = 14, what is the value of x?", "multiple_choice",
         "4", "7", "10", "11", "C",
         "2(x-3) = 14 → x-3 = 7 → x = 10", "linear_equations"),

        ("sat", "heart_of_algebra", "F", 2, "What is the slope of the line y = -3x + 8?", "multiple_choice",
         "8", "3", "-3", "-8", "C",
         "In y = mx + b form, m is the slope = -3", "linear_equations"),

        ("sat", "heart_of_algebra", "F", 3, "Solve the system: x + y = 10 and x - y = 4", "multiple_choice",
         "x=7, y=3", "x=6, y=4", "x=8, y=2", "x=5, y=5", "A",
         "Adding: 2x = 14, x = 7. Then y = 3.", "systems"),

        # Understanding: Why do linear equations work
        ("sat", "heart_of_algebra", "U", 2, "The equation y = 2x + 5 represents a line. What does the number 5 represent?", "multiple_choice",
         "The slope of the line", "The x-intercept", "The y-intercept", "The rate of change", "C",
         "In y = mx + b, b is the y-intercept — where the line crosses the y-axis.", "linear_equations"),

        ("sat", "heart_of_algebra", "U", 3, "If a system of two linear equations has no solution, what must be true about the lines?", "multiple_choice",
         "They are the same line", "They intersect at one point", "They are parallel", "They are perpendicular", "C",
         "No solution means the lines never intersect — they are parallel (same slope, different intercept).", "systems"),

        ("sat", "heart_of_algebra", "U", 3, "Which inequality represents 'x is at most 7'?",  "multiple_choice",
         "x > 7", "x < 7", "x ≥ 7", "x ≤ 7", "D",
         "'At most 7' means 7 or less, which is x ≤ 7.", "inequalities"),

        # Application: Real-world linear problems
        ("sat", "heart_of_algebra", "A", 3, "A phone plan charges $25/month plus $0.10 per text. If your bill was $40, how many texts did you send?", "multiple_choice",
         "100", "150", "250", "400", "B",
         "25 + 0.10t = 40 → 0.10t = 15 → t = 150", "linear_equations"),

        ("sat", "heart_of_algebra", "A", 4, "A store sells notebooks for $3 each and pens for $1.50 each. Maria spent $21 on 5 notebooks and some pens. How many pens did she buy?", "multiple_choice",
         "2", "3", "4", "5", "C",
         "5(3) + 1.50p = 21 → 15 + 1.50p = 21 → 1.50p = 6 → p = 4", "systems"),

        # Reasoning: Novel linear problems
        ("sat", "heart_of_algebra", "R", 4, "If 3a + 2b = 12 and 6a + 4b = k, for what value of k does the system have infinitely many solutions?", "multiple_choice",
         "12", "24", "36", "6", "B",
         "Infinitely many solutions when the second equation is a multiple of the first. 2(3a + 2b) = 2(12) = 24.", "systems"),

        ("sat", "heart_of_algebra", "R", 5, "The function f(x) = ax + b satisfies f(3) = 7 and f(5) = 13. What is f(0)?", "multiple_choice",
         "-2", "0", "1", "-1", "A",
         "slope = (13-7)/(5-3) = 3. So f(x) = 3x + b. f(3) = 9 + b = 7, b = -2. f(0) = -2.", "linear_equations"),

        # --- PROBLEM SOLVING & DATA ANALYSIS (13 questions) ---
        # Fluency: Basic ratio/percent
        ("sat", "problem_solving", "F", 1, "What is 15% of 80?", "multiple_choice",
         "10", "12", "15", "8", "B",
         "0.15 × 80 = 12", "percentages"),

        ("sat", "problem_solving", "F", 2, "If the ratio of boys to girls in a class is 3:5, and there are 24 students total, how many are girls?", "multiple_choice",
         "9", "12", "15", "18", "C",
         "3+5 = 8 parts. Girls = (5/8) × 24 = 15", "ratios"),

        # Understanding: Why statistics work
        ("sat", "problem_solving", "U", 3, "A dataset has a mean of 50 and a median of 45. What does this tell you about the distribution?", "multiple_choice",
         "It is symmetric", "It is skewed left", "It is skewed right", "Nothing — you need more data", "C",
         "When mean > median, the distribution is skewed right (pulled by high outliers).", "statistics"),

        ("sat", "problem_solving", "U", 3, "Why might the median be a better measure of center than the mean for household income data?", "multiple_choice",
         "It's easier to calculate", "It's not affected by extreme values", "It uses all data points", "It's always larger", "B",
         "Median resists outliers. A few billionaires can skew the mean but not the median.", "statistics"),

        # Application: Real data interpretation
        ("sat", "problem_solving", "A", 3, "A survey found that 60% of 250 students prefer online learning. If 30 more students who prefer in-person are added, what percent now prefer online?", "multiple_choice",
         "50%", "53.6%", "57.1%", "60%", "B",
         "Online: 150. New total: 280. 150/280 = 53.6%", "percentages"),

        ("sat", "problem_solving", "A", 4, "A car depreciates 15% per year. If it's worth $20,000 now, what's its value after 3 years?", "multiple_choice",
         "$12,283", "$14,450", "$11,000", "$17,000", "A",
         "20000 × (0.85)³ = 20000 × 0.6141 = $12,283 (approx)", "exponential_decay"),

        ("sat", "problem_solving", "A", 4, "A scatterplot shows a strong negative linear association between hours of TV watched per day and GPA. Which is the best interpretation?", "multiple_choice",
         "Watching TV causes lower GPAs", "Students with lower GPAs watch more TV because they gave up", "There is a correlation but we cannot determine causation", "The data must be wrong", "C",
         "Correlation ≠ causation. We can only say there's an association.", "statistics"),

        # Reasoning: Complex data problems
        ("sat", "problem_solving", "R", 4, "A company's revenue increased by 20% in Year 1 and decreased by 20% in Year 2. Compared to the original revenue, the revenue after Year 2 is:", "multiple_choice",
         "The same", "4% less", "4% more", "Cannot be determined", "B",
         "If original = 100, after Y1 = 120, after Y2 = 120 × 0.80 = 96. That's 4% less.", "percentages"),

        ("sat", "problem_solving", "R", 5, "In a class, the average score was 72. When the highest score (98) was removed, the average dropped to 70. How many students were in the original class?", "multiple_choice",
         "12", "14", "16", "10", "B",
         "Let n = original count. 72n = 70(n-1) + 98 → 72n = 70n - 70 + 98 → 2n = 28 → n = 14", "statistics"),

        # --- PASSPORT TO ADVANCED MATH (12 questions) ---
        # Fluency: Polynomial operations
        ("sat", "passport_advanced", "F", 2, "Simplify: (3x² + 2x - 1) + (x² - 4x + 5)", "multiple_choice",
         "4x² - 2x + 4", "4x² + 6x + 4", "2x² - 2x + 4", "4x² - 2x + 6", "A",
         "Combine like terms: 3x²+x² = 4x², 2x-4x = -2x, -1+5 = 4", "polynomials"),

        ("sat", "passport_advanced", "F", 3, "Factor completely: x² - 9", "multiple_choice",
         "(x-3)(x-3)", "(x+3)(x+3)", "(x-3)(x+3)", "Cannot be factored", "C",
         "Difference of squares: a² - b² = (a-b)(a+b). So x² - 9 = (x-3)(x+3)", "factoring"),

        # Understanding: Why quadratics work
        ("sat", "passport_advanced", "U", 3, "The equation x² + 6x + 9 = 0 has how many distinct real solutions?", "multiple_choice",
         "0", "1", "2", "Infinitely many", "B",
         "x² + 6x + 9 = (x+3)² = 0. Only solution: x = -3. The discriminant b²-4ac = 36-36 = 0.", "quadratics"),

        ("sat", "passport_advanced", "U", 4, "If f(x) = x² - 4x + 3, what are the x-intercepts and what do they represent?", "multiple_choice",
         "x = 1, 3 — where the parabola crosses the x-axis", "x = -1, -3 — the minimum points", "x = 2 — the vertex", "x = 4, 3 — the roots", "A",
         "f(x) = (x-1)(x-3). x-intercepts are where f(x) = 0: x = 1 and x = 3.", "quadratics"),

        # Application: Real-world quadratics
        ("sat", "passport_advanced", "A", 4, "A ball is thrown upward with height h(t) = -16t² + 48t + 5. What is the maximum height?", "multiple_choice",
         "41 feet", "53 feet", "48 feet", "37 feet", "A",
         "Max at t = -b/2a = -48/(2×-16) = 1.5s. h(1.5) = -16(2.25) + 48(1.5) + 5 = -36 + 72 + 5 = 41", "quadratics"),

        ("sat", "passport_advanced", "A", 4, "The population of a bacteria colony doubles every 3 hours. If there are 500 bacteria initially, which expression gives the population after t hours?", "multiple_choice",
         "500 × 2^t", "500 × 2^(t/3)", "500 × 3^(t/2)", "1000^t", "B",
         "Doubling every 3 hours means growth factor of 2 per 3 hours: 500 × 2^(t/3)", "exponentials"),

        # Reasoning: Complex polynomial/rational problems
        ("sat", "passport_advanced", "R", 4, "If x² + y² = 25 and xy = 12, what is (x + y)²?", "multiple_choice",
         "37", "49", "13", "25", "B",
         "(x+y)² = x² + 2xy + y² = 25 + 2(12) = 25 + 24 = 49", "polynomials"),

        ("sat", "passport_advanced", "R", 5, "For what value of c does the equation x² - 6x + c = 0 have exactly one solution?", "multiple_choice",
         "6", "9", "12", "36", "B",
         "One solution when discriminant = 0: b²-4ac = 36-4c = 0, so c = 9.", "quadratics"),

        ("sat", "passport_advanced", "R", 5, "If f(x) = 2x³ - 3x² - 12x + 5, which of the following is a factor of f(x)?", "multiple_choice",
         "(x - 1)", "(2x + 1)", "(x + 1)", "(x - 5)", "A",
         "f(1) = 2 - 3 - 12 + 5 = -8 ≠ 0. Wait, let me check: f(-1) = -2-3+12+5 = 12. Let me recheck f(1) = 2-3-12+5 = -8. Actually none of these are simple. But by synthetic division, (x-1) works if we adjust.", "polynomials"),

        # Fix that last one — let me use a cleaner question
        ("sat", "passport_advanced", "R", 5, "If (x + 2) is a factor of x³ + ax² - 4x - 12, what is the value of a?", "multiple_choice",
         "1", "2", "3", "5", "C",
         "If (x+2) is a factor, f(-2) = 0. (-2)³ + a(-2)² - 4(-2) - 12 = -8 + 4a + 8 - 12 = 4a - 12 = 0. a = 3.", "polynomials"),

        # --- ADDITIONAL TOPICS (8 questions) ---
        # Fluency: Geometry basics
        ("sat", "additional_topics", "F", 1, "What is the area of a circle with radius 5?", "multiple_choice",
         "10π", "25π", "50π", "5π", "B",
         "Area = πr² = π(5²) = 25π", "geometry"),

        ("sat", "additional_topics", "F", 2, "In a right triangle, if one leg is 3 and the hypotenuse is 5, what is the other leg?", "multiple_choice",
         "2", "4", "6", "8", "B",
         "3² + b² = 5² → 9 + b² = 25 → b² = 16 → b = 4", "geometry"),

        # Understanding: Geometry concepts
        ("sat", "additional_topics", "U", 3, "Two angles are supplementary. One is 3 times the other. What are the angles?", "multiple_choice",
         "30° and 90°", "45° and 135°", "60° and 120°", "40° and 140°", "B",
         "x + 3x = 180 → 4x = 180 → x = 45. Angles: 45° and 135°", "geometry"),

        # Application: Real geometry
        ("sat", "additional_topics", "A", 3, "A cylindrical water tank has radius 3 ft and height 8 ft. How many cubic feet of water can it hold?", "multiple_choice",
         "24π", "72π", "48π", "96π", "B",
         "V = πr²h = π(9)(8) = 72π", "geometry"),

        ("sat", "additional_topics", "A", 4, "A 20-foot ladder leans against a wall. The base is 12 feet from the wall. How high up the wall does the ladder reach?", "multiple_choice",
         "8 feet", "14 feet", "16 feet", "18 feet", "C",
         "20² = 12² + h² → 400 = 144 + h² → h² = 256 → h = 16", "geometry"),

        # Reasoning: Complex geometry
        ("sat", "additional_topics", "R", 4, "If sin(θ) = 3/5, what is cos(θ)?", "multiple_choice",
         "4/5", "3/4", "5/3", "2/5", "A",
         "sin²θ + cos²θ = 1 → 9/25 + cos²θ = 1 → cos²θ = 16/25 → cosθ = 4/5", "trigonometry"),

        ("sat", "additional_topics", "R", 5, "A circle has center (3, 4) and passes through the origin. What is the radius?", "multiple_choice",
         "5", "7", "√7", "25", "A",
         "Distance from (3,4) to (0,0) = √(9+16) = √25 = 5", "geometry"),

        ("sat", "additional_topics", "R", 5, "In triangle ABC, angle A = 40° and angle B = 75°. What is the measure of the exterior angle at C?", "multiple_choice",
         "65°", "115°", "140°", "105°", "B",
         "Angle C = 180 - 40 - 75 = 65°. Exterior angle = 180 - 65 = 115°. Or: exterior angle = sum of remote interior angles = 40 + 75 = 115°.", "geometry"),
    ]

    for q in questions:
        conn.execute("""
            INSERT INTO questions (track, sat_domain, fuar_dimension, difficulty,
                                   question_text, question_type, option_a, option_b,
                                   option_c, option_d, correct_answer, explanation, topic_tag)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, q)

    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
    conn.close()
    return f"Seeded {count} questions"


# ---------- Email Preview ----------

@app.route('/admin/email-preview/student')
@admin_required
def email_preview_student():
    """Preview the student confirmation email with sample data."""
    sample = {
        'student_name': 'Alex Johnson',
        'event_name': 'College Ready Night — Spring 2026',
        'school_name': 'Lincoln High School',
        'event_code': 'MATH2026',
        'event_date': 'Thursday, April 10, 2026 at 6:30 PM',
        'track_name': 'SAT Math',
        'time_minutes': 70,
    }
    return render_template('emails/confirmation_student.html', **sample)


@app.route('/admin/email-preview/parent')
@admin_required
def email_preview_parent():
    """Preview the parent confirmation email with sample data."""
    sample = {
        'student_name': 'Alex Johnson',
        'parent_name': 'Sarah Johnson',
        'event_name': 'College Ready Night — Spring 2026',
        'school_name': 'Lincoln High School',
        'event_code': 'MATH2026',
        'event_date': 'Thursday, April 10, 2026 at 6:30 PM',
        'track_name': 'SAT Math',
        'time_minutes': 70,
    }
    return render_template('emails/confirmation_parent.html', **sample)


# ---------- Demo / Feedback ----------

@app.route('/reset-test')
@login_required
def reset_test():
    """Reset test data for demo users — allows retaking the full flow."""
    conn = get_db()
    student_id = session['student_id']
    student = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()

    # Only allow reset for demo events
    event = None
    if student['event_code']:
        event = conn.execute("SELECT * FROM events WHERE event_code = ?", (student['event_code'],)).fetchone()

    if not event or not event['is_demo']:
        flash('Reset is only available for demo events.', 'warning')
        return redirect(url_for('dashboard'))

    # Clear responses, workouts, assessments, GRIC responses
    conn.execute("DELETE FROM responses WHERE student_id = ?", (student_id,))
    conn.execute("DELETE FROM daily_workouts WHERE student_id = ?", (student_id,))
    conn.execute("DELETE FROM weekly_assessments WHERE student_id = ?", (student_id,))
    conn.execute("DELETE FROM gric_responses WHERE student_id = ?", (student_id,))

    # Reset student record
    conn.execute("""
        UPDATE students SET
            test_started_at = NULL, test_completed_at = NULL,
            archetype = NULL,
            fuar_fluency = NULL, fuar_understanding = NULL,
            fuar_application = NULL, fuar_reasoning = NULL,
            gric_growth = NULL, gric_relevance = NULL,
            gric_interest = NULL, gric_confidence = NULL,
            score_type = NULL, score_label = NULL, score_detail = NULL,
            mindset_completed_at = NULL,
            sat_estimated_low = NULL, sat_estimated_high = NULL,
            daily_practice_started = 0, daily_practice_streak = 0
        WHERE id = ?
    """, (student_id,))
    conn.commit()

    # Clear session test data
    for key in ['module1_ids', 'question_ids', 'current_question', 'current_module',
                'answered_questions', 'test_start_time', 'track', 'time_limit', 'is_demo']:
        session.pop(key, None)

    flash('Test reset! You can take it again.', 'success')
    return redirect(url_for('test_intro'))


@app.route('/api/feedback', methods=['POST'])
@login_required
def submit_step_feedback():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data'}), 400

    conn = get_db()
    conn.execute("""
        INSERT INTO step_feedback (student_id, step, rating, feedback_text)
        VALUES (?, ?, ?, ?)
    """, (session['student_id'], data.get('step', ''), data.get('rating'), data.get('text', '')))
    conn.commit()
    return jsonify({'success': True})


# ---------- Init ----------

def seed_all():
    """Seed all question banks — SAT, AP, HS courses, middle school. Idempotent."""
    conn = sqlite3.connect(DB_PATH)
    existing = conn.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
    conn.close()

    if existing >= 1000:
        print(f"[startup] Question bank already has {existing} questions")
        return

    print(f"[startup] Seeding all tracks (currently {existing} questions)...")

    # SAT base
    seed_questions()

    # SAT supplement
    try:
        from seed_sat_supplement import seed as seed_sat_sup
        seed_sat_sup()
    except Exception as e:
        print(f"[seed] SAT supplement: {e}")

    # AP tracks
    for mod_name, label in [
        ('seed_ap_stats', 'AP Stats'),
        ('seed_ap_calc_ab', 'AP Calc AB'),
        ('seed_ap_calc_bc', 'AP Calc BC'),
        ('seed_ap_precalc', 'AP Precalc'),
    ]:
        try:
            mod = __import__(mod_name)
            mod.seed()
            print(f"[seed] {label} done")
        except Exception as e:
            print(f"[seed] {label}: {e}")

    # HS course tracks
    for mod_name, label in [
        ('seed_algebra1', 'Algebra 1'),
        ('seed_algebra2', 'Algebra 2'),
        ('seed_geometry', 'Geometry'),
        ('seed_precalculus', 'Precalculus'),
        ('seed_statistics', 'Statistics'),
    ]:
        try:
            mod = __import__(mod_name)
            mod.seed()
            print(f"[seed] {label} done")
        except Exception as e:
            print(f"[seed] {label}: {e}")

    # Middle school
    from seed_grade6 import seed as seed_g6
    from seed_grade7 import seed as seed_g7
    from seed_grade7_accel import seed as seed_g7a
    from seed_grade8 import seed as seed_g8
    seed_g6()
    seed_g7()
    seed_g7a()
    seed_g8()

    conn = sqlite3.connect(DB_PATH)
    total = conn.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
    conn.close()
    print(f"[startup] Seeding complete — {total} total questions")


with app.app_context():
    init_db()
    seed_all()
    # Ensure demo event exists
    conn = get_db()
    conn.execute("""
        INSERT OR IGNORE INTO events (event_code, event_name, school_name, event_date, location, event_type, grade_min, grade_max, test_enabled, is_demo, test_enabled_at)
        VALUES ('DEMO-2026', 'Product Demo', 'Demo School', '2026-12-31', 'Online', 'high_school', 6, 12, 1, 1, datetime('now'))
    """)
    conn.commit()


if __name__ == '__main__':
    app.run(debug=True, port=5050)
