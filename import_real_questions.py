#!/usr/bin/env python3
"""
Import real SAT/AP questions from REAL-QUESTIONS-RESEARCH.md into college_ready.db.

Parses all question blocks from the markdown file and inserts them into the
questions table, skipping any that already exist (matched by question_text).
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'college_ready.db')

# ---------------------------------------------------------------------------
# All questions parsed from REAL-QUESTIONS-RESEARCH.md
# ---------------------------------------------------------------------------

QUESTIONS = [
    # -----------------------------------------------------------------------
    # SAT QUESTIONS  (topic_tag = 'real_sat_2024')
    # -----------------------------------------------------------------------
    {
        'track': 'sat',
        'sat_domain': 'Algebra — Linear growth',
        'fuar_dimension': 'F',
        'difficulty': 1,
        'question_text': (
            "On the first day of a semester, a film club has 90 members. "
            "Each day after the first day of the semester, 10 new members join the film club. "
            "If no members leave the film club, how many total members will the film club have "
            "4 days after the first day of the semester?"
        ),
        'option_a': '400',
        'option_b': '130',
        'option_c': '94',
        'option_d': '90',
        'correct_answer': 'B',
        'explanation': 'After 4 days, 4 x 10 = 40 new members join. Total = 90 + 40 = 130.',
        'topic_tag': 'real_sat_2024',
    },
    {
        'track': 'sat',
        'sat_domain': 'Algebra — Systems of equations',
        'fuar_dimension': 'U',
        'difficulty': 1,
        'question_text': (
            "Given the system of equations:\n"
            "s + 7r = 27\n"
            "r = 3\n"
            "What is the solution (r, s) to the given system of equations?"
        ),
        'option_a': '(6, 3)',
        'option_b': '(3, 6)',
        'option_c': '(3, 27)',
        'option_d': '(27, 3)',
        'correct_answer': 'B',
        'explanation': 'Substitute r = 3 into s + 7(3) = 27, so s + 21 = 27, s = 6. Solution is (3, 6).',
        'topic_tag': 'real_sat_2024',
    },
    {
        'track': 'sat',
        'sat_domain': 'Algebra — Linear equations in context',
        'fuar_dimension': 'U',
        'difficulty': 2,
        'question_text': (
            "The equation x + y = 1,440 represents the number of minutes of daylight "
            "(between sunrise and sunset), x, and the number of minutes of non-daylight, y, "
            "on a particular day in Oak Park, Illinois. If this day has 670 minutes of daylight, "
            "how many minutes of non-daylight does it have?"
        ),
        'option_a': '670',
        'option_b': '770',
        'option_c': '1,373',
        'option_d': '1,440',
        'correct_answer': 'B',
        'explanation': '670 + y = 1,440, so y = 770.',
        'topic_tag': 'real_sat_2024',
    },
    {
        'track': 'sat',
        'sat_domain': 'Problem Solving & Data Analysis — Proportional reasoning',
        'fuar_dimension': 'A',
        'difficulty': 2,
        'question_text': (
            "Scott selected 20 employees at random from all 400 employees at a company. "
            "He found that 16 of the employees in this sample are enrolled in exactly three "
            "professional development courses this year. Based on Scott's findings, which of "
            "the following is the best estimate of the number of employees at the company who "
            "are enrolled in exactly three professional development courses this year?"
        ),
        'option_a': '4',
        'option_b': '320',
        'option_c': '380',
        'option_d': '384',
        'correct_answer': 'B',
        'explanation': '16/20 = 0.8 of the sample. 0.8 x 400 = 320.',
        'topic_tag': 'real_sat_2024',
    },
    {
        'track': 'sat',
        'sat_domain': 'Algebra — Solving linear equations',
        'fuar_dimension': 'F',
        'difficulty': 1,
        'question_text': 'If 4x - 28 = -24, what is the value of x - 7?',
        'option_a': '-24',
        'option_b': '-22',
        'option_c': '-6',
        'option_d': '-1',
        'correct_answer': 'C',
        'explanation': '4x - 28 = -24 means 4(x - 7) = -24, so x - 7 = -6.',
        'topic_tag': 'real_sat_2024',
    },
    {
        'track': 'sat',
        'sat_domain': 'Algebra — Inequalities',
        'fuar_dimension': 'U',
        'difficulty': 2,
        'question_text': (
            "For a snowstorm in a certain town, the minimum rate of snowfall recorded was "
            "0.6 inches per hour, and the maximum rate of snowfall recorded was 1.8 inches "
            "per hour. Which inequality is true for all values of s, where s represents a rate "
            "of snowfall, in inches per hour, recorded for this snowstorm?"
        ),
        'option_a': 's >= 2.4',
        'option_b': 's >= 1.8',
        'option_c': '0 <= s <= 0.6',
        'option_d': '0.6 <= s <= 1.8',
        'correct_answer': 'D',
        'explanation': 'The rate must be between the minimum (0.6) and maximum (1.8), inclusive.',
        'topic_tag': 'real_sat_2024',
    },
    {
        'track': 'sat',
        'sat_domain': 'Algebra — Ratios and proportional relationships',
        'fuar_dimension': 'U',
        'difficulty': 2,
        'question_text': (
            "At a particular track meet, the ratio of coaches to athletes is 1 to 26. "
            "If there are x coaches at the track meet, which of the following expressions "
            "represents the number of athletes at the track meet?"
        ),
        'option_a': 'x/26',
        'option_b': '26x',
        'option_c': 'x + 26',
        'option_d': '26/x',
        'correct_answer': 'B',
        'explanation': 'If coaches:athletes = 1:26, and there are x coaches, there are 26x athletes.',
        'topic_tag': 'real_sat_2024',
    },
    {
        'track': 'sat',
        'sat_domain': 'Advanced Math — Volume / polynomial functions',
        'fuar_dimension': 'A',
        'difficulty': 3,
        'question_text': (
            "A right rectangular prism has a height of 9 inches. The length of the prism's base "
            "is x inches, which is 7 inches more than the width of the prism's base. Which "
            "function V gives the volume of the prism, in cubic inches, in terms of the length "
            "of the prism's base?"
        ),
        'option_a': 'V(x) = x(x + 9)(x + 7)',
        'option_b': 'V(x) = x(x + 9)(x - 7)',
        'option_c': 'V(x) = 9x(x + 7)',
        'option_d': 'V(x) = 9x(x - 7)',
        'correct_answer': 'D',
        'explanation': 'Length = x, width = x - 7, height = 9. V = 9 * x * (x - 7).',
        'topic_tag': 'real_sat_2024',
    },
    {
        'track': 'sat',
        'sat_domain': 'Advanced Math — Polynomial factoring',
        'fuar_dimension': 'U',
        'difficulty': 2,
        'question_text': 'Which expression is equivalent to 16x^3y^2 + 14xy?',
        'option_a': '2xy(8xy + 7)',
        'option_b': '2xy(8x^2y + 7)',
        'option_c': '14xy(2x^2y + 1)',
        'option_d': '14xy(8x^2y + 1)',
        'correct_answer': 'B',
        'explanation': (
            'Factor out 2xy: 16x^3y^2 / 2xy = 8x^2y; 14xy / 2xy = 7. So 2xy(8x^2y + 7).'
        ),
        'topic_tag': 'real_sat_2024',
    },
    {
        'track': 'sat',
        'sat_domain': 'Algebra — Linear equations in context',
        'fuar_dimension': 'A',
        'difficulty': 2,
        'question_text': (
            "A veterinarian recommends that each day a certain rabbit should eat 25 calories "
            "per pound of the rabbit's weight, plus an additional 11 calories. Which equation "
            "represents this situation, where c is the total number of calories the veterinarian "
            "recommends the rabbit should eat each day if the rabbit's weight is x pounds?"
        ),
        'option_a': 'c = 25x',
        'option_b': 'c = 36x',
        'option_c': 'c = 11x + 25',
        'option_d': 'c = 25x + 11',
        'correct_answer': 'D',
        'explanation': '25 calories per pound (25x) plus 11 additional calories = 25x + 11.',
        'topic_tag': 'real_sat_2024',
    },
    {
        'track': 'sat',
        'sat_domain': 'Algebra — Slope-intercept form',
        'fuar_dimension': 'U',
        'difficulty': 2,
        'question_text': (
            "Line r in the xy-plane has a slope of 4 and passes through the point (0, 6). "
            "Which equation defines line r?"
        ),
        'option_a': 'y = -6x + 4',
        'option_b': 'y = 6x + 4',
        'option_c': 'y = 4x - 6',
        'option_d': 'y = 4x + 6',
        'correct_answer': 'D',
        'explanation': 'Slope = 4, y-intercept = 6 (passes through (0,6)). y = 4x + 6.',
        'topic_tag': 'real_sat_2024',
    },
    {
        'track': 'sat',
        'sat_domain': 'Advanced Math — Polynomial operations',
        'fuar_dimension': 'U',
        'difficulty': 3,
        'question_text': 'Which expression is equivalent to (8x^3 + 8) - (x^3 - 2)?',
        'option_a': '8x^3 + 6',
        'option_b': '7x^3 + 10',
        'option_c': '8x^3 + 10',
        'option_d': '7x^3 + 6',
        'correct_answer': 'B',
        'explanation': '(8x^3 + 8) - (x^3 - 2) = 8x^3 + 8 - x^3 + 2 = 7x^3 + 10.',
        'topic_tag': 'real_sat_2024',
    },
    {
        'track': 'sat',
        'sat_domain': 'Geometry — Similar figures / area scaling',
        'fuar_dimension': 'A',
        'difficulty': 3,
        'question_text': (
            "Rectangles ABCD and EFGH are similar. The length of each side of EFGH is 6 times "
            "the length of the corresponding side of ABCD. The area of ABCD is 54 square units. "
            "What is the area, in square units, of EFGH?"
        ),
        'option_a': '9',
        'option_b': '36',
        'option_c': '324',
        'option_d': '1,944',
        'correct_answer': 'D',
        'explanation': 'When sides scale by factor 6, area scales by 6^2 = 36. Area = 54 x 36 = 1,944.',
        'topic_tag': 'real_sat_2024',
    },
    {
        'track': 'sat',
        'sat_domain': 'Advanced Math — Rational expressions',
        'fuar_dimension': 'U',
        'difficulty': 3,
        'question_text': (
            "Which expression is equivalent to (42a/k) + 42ak, where k > 0?"
        ),
        'option_a': '84a/k',
        'option_b': '84ak^2/k',
        'option_c': '42a(k + 1)/k',
        'option_d': '42a(k^2 + 1)/k',
        'correct_answer': 'D',
        'explanation': '(42a/k) + 42ak = (42a + 42ak^2)/k = 42a(1 + k^2)/k.',
        'topic_tag': 'real_sat_2024',
    },
    {
        'track': 'sat',
        'sat_domain': 'Advanced Math — Quadratic equations / discriminant',
        'fuar_dimension': 'A',
        'difficulty': 4,
        'question_text': 'Which quadratic equation has no real solutions?',
        'option_a': 'x^2 + 14x - 49 = 0',
        'option_b': 'x^2 - 14x + 49 = 0',
        'option_c': '5x^2 - 14x - 49 = 0',
        'option_d': '5x^2 - 14x + 49 = 0',
        'correct_answer': 'D',
        'explanation': (
            'Discriminant = b^2 - 4ac. For D: (-14)^2 - 4(5)(49) = 196 - 980 = -784 < 0. '
            'No real solutions.'
        ),
        'topic_tag': 'real_sat_2024',
    },
    {
        'track': 'sat',
        'sat_domain': 'Advanced Math — Exponential growth modeling',
        'fuar_dimension': 'R',
        'difficulty': 4,
        'question_text': (
            "P(t) = 260(1.04)^((6/4)t). The function P models the population, in thousands, "
            "of a certain city t years after 2003. According to the model, the population is "
            "predicted to increase by 4% every n months. What is the value of n?"
        ),
        'option_a': '8',
        'option_b': '12',
        'option_c': '18',
        'option_d': '72',
        'correct_answer': 'A',
        'explanation': (
            'The exponent (6/4)t = 1 when t = 2/3 years = 8 months. '
            'So the population grows by 4% every 8 months.'
        ),
        'topic_tag': 'real_sat_2024',
    },

    # -----------------------------------------------------------------------
    # AP CALCULUS AB QUESTIONS  (topic_tag = 'real_ap_calc_2016')
    # -----------------------------------------------------------------------
    {
        'track': 'ap_calc_ab',
        'sat_domain': 'Limits — L\'Hopital\'s Rule',
        'fuar_dimension': 'A',
        'difficulty': 3,
        'question_text': (
            "lim(x->pi) [cos(x) + sin(2x) + 1] / [x^2 - pi^2] is"
        ),
        'option_a': '1/(2pi)',
        'option_b': '1/pi',
        'option_c': '1',
        'option_d': 'nonexistent',
        'correct_answer': 'B',
        'explanation': (
            "Direct substitution gives 0/0. Apply L'Hopital's Rule: "
            "[-sin(x) + 2cos(2x)] / [2x]. At x = pi: [0 + 2] / [2pi] = 1/pi."
        ),
        'topic_tag': 'real_ap_calc_2016',
    },
    {
        'track': 'ap_calc_ab',
        'sat_domain': 'Limits — Limits at infinity',
        'fuar_dimension': 'U',
        'difficulty': 3,
        'question_text': (
            "lim(x->infinity) sqrt(9x^4 + 1) / (x^2 - 3x + 5) is"
        ),
        'option_a': '1',
        'option_b': '3',
        'option_c': '9',
        'option_d': 'nonexistent',
        'correct_answer': 'B',
        'explanation': (
            'For large x, sqrt(9x^4 + 1) approaches 3x^2 and x^2 - 3x + 5 approaches x^2. '
            'The limit is 3.'
        ),
        'topic_tag': 'real_ap_calc_2016',
    },
    {
        'track': 'ap_calc_ab',
        'sat_domain': 'Derivatives — Related rates',
        'fuar_dimension': 'A',
        'difficulty': 4,
        'question_text': (
            "An ice sculpture in the form of a sphere melts in such a way that it maintains its "
            "spherical shape. The volume of the sphere is decreasing at a constant rate of 2pi "
            "cubic meters per hour. At what rate, in square meters per hour, is the surface area "
            "of the sphere decreasing at the moment when the radius is 5 meters? "
            "(Note: For a sphere of radius r, the surface area is 4pi*r^2 and the volume is "
            "(4/3)pi*r^3.)"
        ),
        'option_a': '4pi/5',
        'option_b': '40pi',
        'option_c': '80pi^2',
        'option_d': '100pi',
        'correct_answer': 'A',
        'explanation': (
            'dV/dt = 4pi*r^2 * dr/dt = -2pi. At r=5: 100pi * dr/dt = -2pi, so dr/dt = -1/50. '
            'dA/dt = 8pi*r * dr/dt = 8pi(5)(-1/50) = -4pi/5. Rate = 4pi/5.'
        ),
        'topic_tag': 'real_ap_calc_2016',
    },
    {
        'track': 'ap_calc_ab',
        'sat_domain': 'Derivatives — Piecewise functions / differentiability',
        'fuar_dimension': 'A',
        'difficulty': 3,
        'question_text': (
            "Let f be the piecewise-linear function defined as:\n"
            "f(x) = 2x - 2 for x < 3\n"
            "f(x) = 2x - 4 for x >= 3\n\n"
            "Which of the following statements are true?\n\n"
            "I. lim(h->0-) [f(3+h) - f(3)] / h = 2\n"
            "II. lim(h->0+) [f(3+h) - f(3)] / h = 2\n"
            "III. f'(3) = 2"
        ),
        'option_a': 'None',
        'option_b': 'II only',
        'option_c': 'I and II only',
        'option_d': 'I, II, and III',
        'correct_answer': 'B',
        'explanation': (
            'f(3) = 2(3) - 4 = 2. From the right (x >= 3): slope is 2, so right derivative = 2. '
            'From the left (x < 3): f approaches 2(3) - 2 = 4, but f(3) = 2, so there is a jump '
            'discontinuity. The left-hand limit of the difference quotient does not equal 2. '
            'Only statement II is true.'
        ),
        'topic_tag': 'real_ap_calc_2016',
    },
    {
        'track': 'ap_calc_ab',
        'sat_domain': 'Integration — Fundamental Theorem of Calculus',
        'fuar_dimension': 'A',
        'difficulty': 4,
        'question_text': (
            "If f(x) = integral from 1 to x^3 of 1/(1 + ln(t)) dt for x >= 1, then f'(2) ="
        ),
        'option_a': '1/(1 + ln 2)',
        'option_b': '12/(1 + ln 2)',
        'option_c': '1/(1 + ln 8)',
        'option_d': '12/(1 + ln 8)',
        'correct_answer': 'D',
        'explanation': (
            'By Chain Rule + FTC: f\'(x) = [1/(1 + ln(x^3))] * 3x^2. '
            'At x=2: f\'(2) = [1/(1 + ln 8)] * 12 = 12/(1 + ln 8).'
        ),
        'topic_tag': 'real_ap_calc_2016',
    },
    {
        'track': 'ap_calc_ab',
        'sat_domain': 'Integration — Riemann sums',
        'fuar_dimension': 'R',
        'difficulty': 4,
        'question_text': (
            "Which of the following limits is equal to the integral from 3 to 5 of x^4 dx?"
        ),
        'option_a': 'lim(n->inf) sum(k=1 to n) (3 + k/n)^4 * (1/n)',
        'option_b': 'lim(n->inf) sum(k=1 to n) (3 + k/n)^4 * (2/n)',
        'option_c': 'lim(n->inf) sum(k=1 to n) (3 + 2k/n)^4 * (1/n)',
        'option_d': 'lim(n->inf) sum(k=1 to n) (3 + 2k/n)^4 * (2/n)',
        'correct_answer': 'D',
        'explanation': (
            'Interval [3,5] has width 2. Delta x = 2/n. x_k = 3 + k*(2/n). '
            'Riemann sum = sum of (3 + 2k/n)^4 * (2/n).'
        ),
        'topic_tag': 'real_ap_calc_2016',
    },
    {
        'track': 'ap_calc_ab',
        'sat_domain': 'Differential Equations — Exponential growth/decay',
        'fuar_dimension': 'A',
        'difficulty': 4,
        'question_text': (
            "Let y = f(t) be a solution to the differential equation dy/dt = ky, where k is a "
            "constant. Values of f for selected values of t are given:\n"
            "t = 0: f(t) = 4\n"
            "t = 2: f(t) = 12\n"
            "Which of the following is an expression for f(t)?"
        ),
        'option_a': '4e^((t/2) ln 3)',
        'option_b': 'e^((t/2) ln 9) + 3',
        'option_c': '2t^2 + 4',
        'option_d': '4t + 4',
        'correct_answer': 'A',
        'explanation': (
            'For dy/dt = ky, the solution is f(t) = f(0)e^(kt). f(0) = 4, '
            'f(2) = 4e^(2k) = 12, so e^(2k) = 3, k = (ln 3)/2. '
            'Thus f(t) = 4e^((t/2) ln 3).'
        ),
        'topic_tag': 'real_ap_calc_2016',
    },
    {
        'track': 'ap_calc_ab',
        'sat_domain': 'Derivatives — Interpretation in context',
        'fuar_dimension': 'U',
        'difficulty': 2,
        'question_text': (
            "The temperature of a room, in degrees Fahrenheit, is modeled by H, a differentiable "
            "function of the number of minutes after the thermostat is adjusted. Of the following, "
            "which is the best interpretation of H'(5) = 2?"
        ),
        'option_a': 'The temperature of the room is 2 degrees Fahrenheit, 5 minutes after the thermostat is adjusted.',
        'option_b': 'The temperature of the room increases by 2 degrees Fahrenheit during the first 5 minutes after the thermostat is adjusted.',
        'option_c': 'The temperature of the room is increasing at a constant rate of 2/5 degree Fahrenheit per minute.',
        'option_d': 'The temperature of the room is increasing at a rate of 2 degrees Fahrenheit per minute, 5 minutes after the thermostat is adjusted.',
        'correct_answer': 'D',
        'explanation': (
            "H'(5) = 2 means the instantaneous rate of change of temperature at t = 5 minutes "
            "is 2 degrees F per minute."
        ),
        'topic_tag': 'real_ap_calc_2016',
    },
    {
        'track': 'ap_calc_ab',
        'sat_domain': 'Theorems — Mean Value Theorem / Rolle\'s Theorem',
        'fuar_dimension': 'R',
        'difficulty': 4,
        'question_text': (
            "A function f is continuous on the closed interval [2, 5] with f(2) = 17 and f(5) = 17. "
            "Which of the following additional conditions guarantees that there is a number c in "
            "the open interval (2, 5) such that f'(c) = 0?"
        ),
        'option_a': 'No additional conditions are necessary.',
        'option_b': 'f has a relative extremum on the open interval (2, 5).',
        'option_c': 'f is differentiable on the open interval (2, 5).',
        'option_d': 'The integral from 2 to 5 of f(x) dx exists.',
        'correct_answer': 'C',
        'explanation': (
            "By Rolle's Theorem (a special case of MVT), if f is continuous on [2,5], "
            "differentiable on (2,5), and f(2) = f(5), then there exists c in (2,5) where f'(c) = 0."
        ),
        'topic_tag': 'real_ap_calc_2016',
    },

    # -----------------------------------------------------------------------
    # AP PRECALCULUS QUESTIONS  (topic_tag = 'real_ap_precalc_2023')
    # -----------------------------------------------------------------------
    {
        'track': 'ap_precalc',
        'sat_domain': 'Polynomial Functions — Zeros and sign analysis',
        'fuar_dimension': 'A',
        'difficulty': 3,
        'question_text': (
            "A polynomial function p is given by p(x) = -x(x - 4)(x + 2). "
            "What are all intervals on which p(x) >= 0?"
        ),
        'option_a': '[-2, 4]',
        'option_b': '[-2, 0] union [4, infinity)',
        'option_c': '(-infinity, -4] union [0, 2]',
        'option_d': '(-infinity, -2] union [0, 4]',
        'correct_answer': 'D',
        'explanation': (
            'Zeros at x = -2, 0, 4. Leading coefficient is negative (from -x^3). '
            'Sign analysis: p(x) >= 0 on (-inf, -2] union [0, 4].'
        ),
        'topic_tag': 'real_ap_precalc_2023',
    },
    {
        'track': 'ap_precalc',
        'sat_domain': 'Exponential Functions — Equivalent forms',
        'fuar_dimension': 'U',
        'difficulty': 2,
        'question_text': (
            "The function f is given by f(x) = 9 * 25^x. "
            "Which of the following is an equivalent form for f(x)?"
        ),
        'option_a': 'f(x) = 3 * 5^(x/2)',
        'option_b': 'f(x) = 3 * 5^(2x)',
        'option_c': 'f(x) = 9 * 5^(x/2)',
        'option_d': 'f(x) = 9 * 5^(2x)',
        'correct_answer': 'D',
        'explanation': '25^x = (5^2)^x = 5^(2x). So f(x) = 9 * 5^(2x).',
        'topic_tag': 'real_ap_precalc_2023',
    },
    {
        'track': 'ap_precalc',
        'sat_domain': 'Polynomial Functions — End behavior',
        'fuar_dimension': 'U',
        'difficulty': 2,
        'question_text': (
            "The function f is given by f(x) = 5x^6 - 2x^3 - 3. "
            "Which of the following describes the end behavior of f?"
        ),
        'option_a': 'lim(x->-inf) f(x) = -inf and lim(x->inf) f(x) = -inf',
        'option_b': 'lim(x->-inf) f(x) = inf and lim(x->inf) f(x) = inf',
        'option_c': 'lim(x->-inf) f(x) = -inf and lim(x->inf) f(x) = inf',
        'option_d': 'lim(x->-inf) f(x) = inf and lim(x->inf) f(x) = -inf',
        'correct_answer': 'B',
        'explanation': (
            'Leading term is 5x^6. Even degree with positive leading coefficient means '
            'both ends go to +infinity.'
        ),
        'topic_tag': 'real_ap_precalc_2023',
    },
    {
        'track': 'ap_precalc',
        'sat_domain': 'Logarithmic Functions — Properties of logarithms',
        'fuar_dimension': 'F',
        'difficulty': 2,
        'question_text': (
            "Let x and y be positive constants. Which of the following is equivalent to "
            "2ln(x) - 3ln(y)?"
        ),
        'option_a': 'ln(x^2 / y^3)',
        'option_b': 'ln(x^2 * y^3)',
        'option_c': 'ln(2x - 3y)',
        'option_d': 'ln(2x / 3y)',
        'correct_answer': 'A',
        'explanation': '2ln(x) - 3ln(y) = ln(x^2) - ln(y^3) = ln(x^2 / y^3).',
        'topic_tag': 'real_ap_precalc_2023',
    },
    {
        'track': 'ap_precalc',
        'sat_domain': 'Polynomial Functions — Zeros of polynomials',
        'fuar_dimension': 'A',
        'difficulty': 3,
        'question_text': (
            "The polynomial function p is given by p(x) = (x + 3)(x^2 - 2x - 15). "
            "Which of the following describes the zeros of p?"
        ),
        'option_a': 'p has exactly two distinct real zeros.',
        'option_b': 'p has exactly three distinct real zeros.',
        'option_c': 'p has exactly one distinct real zero and no non-real zeros.',
        'option_d': 'p has exactly one distinct real zero and two non-real zeros.',
        'correct_answer': 'A',
        'explanation': (
            'Factor x^2 - 2x - 15 = (x - 5)(x + 3). So p(x) = (x + 3)^2(x - 5). '
            'Two distinct real zeros: x = -3 (multiplicity 2) and x = 5.'
        ),
        'topic_tag': 'real_ap_precalc_2023',
    },
    {
        'track': 'ap_precalc',
        'sat_domain': 'Rational Functions — Vertical asymptotes',
        'fuar_dimension': 'U',
        'difficulty': 3,
        'question_text': (
            "In the xy-plane, the graph of a rational function f has a vertical asymptote at "
            "x = -5. Which of the following could be an expression for f(x)?"
        ),
        'option_a': '(x - 5)(x + 5) / [2(x - 5)]',
        'option_b': '(x - 4)(x + 5) / [(x - 1)(x + 5)]',
        'option_c': '(x + 1)(x + 5) / [(x - 5)(x + 2)]',
        'option_d': '(x - 5)(x - 3) / [(x - 3)(x + 5)]',
        'correct_answer': 'D',
        'explanation': (
            'A vertical asymptote at x = -5 requires (x + 5) in the denominator but NOT '
            'canceled by the numerator. In D: denominator has (x + 5), numerator has '
            '(x - 5)(x - 3) which does not cancel (x + 5), giving a vertical asymptote at x = -5.'
        ),
        'topic_tag': 'real_ap_precalc_2023',
    },
    {
        'track': 'ap_precalc',
        'sat_domain': 'Exponential Functions — Growth vs decay from table',
        'fuar_dimension': 'U',
        'difficulty': 2,
        'question_text': (
            "The exponential function f is defined by f(x) = ab^x, where a and b are positive "
            "constants. The table gives values of f(x) at selected values of x:\n"
            "x: 0, 1, 2, 3, 4\n"
            "f(x): 3/4, 3/2, 3, 6, 12\n\n"
            "Which of the following statements is true?"
        ),
        'option_a': 'f demonstrates exponential decay because a > 0 and 0 < b < 1.',
        'option_b': 'f demonstrates exponential decay because a > 0 and b > 1.',
        'option_c': 'f demonstrates exponential growth because a > 0 and 0 < b < 1.',
        'option_d': 'f demonstrates exponential growth because a > 0 and b > 1.',
        'correct_answer': 'D',
        'explanation': (
            'f(0) = a = 3/4 > 0. Each successive value doubles: 3/4, 3/2, 3, 6, 12. '
            'So b = 2 > 1. Exponential growth with a > 0 and b > 1.'
        ),
        'topic_tag': 'real_ap_precalc_2023',
    },
    {
        'track': 'ap_precalc',
        'sat_domain': 'Functions — Composition of functions',
        'fuar_dimension': 'A',
        'difficulty': 3,
        'question_text': (
            "The function f is given by f(x) = x^2 + 1, and the function g is given by "
            "g(x) = (x - 3)/x. Which of the following is an expression for f(g(x))?"
        ),
        'option_a': '(x^3 - 3x^2 + x - 3) / x',
        'option_b': '(x^2 - 2) / (x^2 + 1)',
        'option_c': '(x^2 - 6x + 9) / x^2 + 1',
        'option_d': '(x^2 - 8) / x^2',
        'correct_answer': 'C',
        'explanation': (
            'f(g(x)) = [g(x)]^2 + 1 = [(x-3)/x]^2 + 1 = (x^2 - 6x + 9)/x^2 + 1.'
        ),
        'topic_tag': 'real_ap_precalc_2023',
    },

    # -----------------------------------------------------------------------
    # AP STATISTICS QUESTIONS  (topic_tag = 'real_ap_stats_ced')
    # -----------------------------------------------------------------------
    {
        'track': 'ap_stats',
        'sat_domain': 'Experimental Design — Randomization',
        'fuar_dimension': 'U',
        'difficulty': 2,
        'question_text': (
            "A researcher wants to determine whether a new fertilizer increases crop yield. "
            "She has 40 identical plots of land available. Which of the following is the best "
            "way to design this experiment?"
        ),
        'option_a': 'Apply the fertilizer to all 40 plots and compare the yield to the previous year\'s yield.',
        'option_b': 'Let each farmer choose whether to use the fertilizer, then compare yields.',
        'option_c': 'Randomly assign 20 plots to receive the fertilizer and 20 plots to receive no fertilizer, then compare yields.',
        'option_d': 'Apply the fertilizer to the 20 plots with the poorest soil and no fertilizer to the other 20, then compare yields.',
        'correct_answer': 'C',
        'explanation': (
            'Random assignment to treatment and control groups is the hallmark of a '
            'well-designed experiment, controlling for confounding variables.'
        ),
        'topic_tag': 'real_ap_stats_ced',
    },
    {
        'track': 'ap_stats',
        'sat_domain': 'Inference — Confidence intervals',
        'fuar_dimension': 'U',
        'difficulty': 3,
        'question_text': (
            "A 95% confidence interval for the mean weight of all packages shipped by a company "
            "is (2.1, 3.7) pounds. Which of the following is a correct interpretation of this interval?"
        ),
        'option_a': '95% of all packages weigh between 2.1 and 3.7 pounds.',
        'option_b': 'There is a 95% probability that the true mean weight is between 2.1 and 3.7 pounds.',
        'option_c': 'We are 95% confident that the true mean weight of all packages is between 2.1 and 3.7 pounds.',
        'option_d': 'If we took 100 samples, exactly 95 of them would have a mean between 2.1 and 3.7 pounds.',
        'correct_answer': 'C',
        'explanation': (
            'The correct interpretation is about confidence in the interval capturing the true '
            'parameter, not about probability of the parameter or individual observations.'
        ),
        'topic_tag': 'real_ap_stats_ced',
    },
    {
        'track': 'ap_stats',
        'sat_domain': 'Probability — Independence',
        'fuar_dimension': 'F',
        'difficulty': 2,
        'question_text': (
            "Events A and B are independent. P(A) = 0.3 and P(B) = 0.5. What is P(A and B)?"
        ),
        'option_a': '0.15',
        'option_b': '0.20',
        'option_c': '0.65',
        'option_d': '0.80',
        'correct_answer': 'A',
        'explanation': 'For independent events, P(A and B) = P(A) * P(B) = 0.3 * 0.5 = 0.15.',
        'topic_tag': 'real_ap_stats_ced',
    },
    {
        'track': 'ap_stats',
        'sat_domain': 'Inference — Hypothesis testing (p-value interpretation)',
        'fuar_dimension': 'U',
        'difficulty': 3,
        'question_text': (
            "A researcher conducts a hypothesis test and obtains a p-value of 0.03. "
            "Which of the following is a correct interpretation of this p-value?"
        ),
        'option_a': 'There is a 3% chance that the null hypothesis is true.',
        'option_b': 'There is a 3% chance that the alternative hypothesis is true.',
        'option_c': 'If the null hypothesis were true, there is a 3% probability of obtaining a test statistic as extreme as or more extreme than the one observed.',
        'option_d': '3% of the population supports the alternative hypothesis.',
        'correct_answer': 'C',
        'explanation': (
            'The p-value is the probability of observing the data (or more extreme) assuming '
            'the null hypothesis is true. It is NOT the probability that H0 is true.'
        ),
        'topic_tag': 'real_ap_stats_ced',
    },
    {
        'track': 'ap_stats',
        'sat_domain': 'Sampling — Bias',
        'fuar_dimension': 'U',
        'difficulty': 2,
        'question_text': (
            "A school newspaper wants to estimate the proportion of students who support a new "
            "dress code. They survey all students in the cafeteria during lunch on a Tuesday. "
            "Which type of bias is most likely present?"
        ),
        'option_a': 'Response bias',
        'option_b': 'Undercoverage bias',
        'option_c': 'Nonresponse bias',
        'option_d': 'Measurement bias',
        'correct_answer': 'B',
        'explanation': (
            'Not all students eat in the cafeteria, so students who bring lunch from home, '
            'eat off campus, or have a different lunch period are excluded. This is undercoverage.'
        ),
        'topic_tag': 'real_ap_stats_ced',
    },
    {
        'track': 'ap_stats',
        'sat_domain': 'Descriptive Statistics — Normal distribution',
        'fuar_dimension': 'A',
        'difficulty': 3,
        'question_text': (
            "The weights of apples in an orchard are approximately normally distributed with a "
            "mean of 150 grams and a standard deviation of 20 grams. What proportion of apples "
            "weigh more than 190 grams?"
        ),
        'option_a': '0.0228',
        'option_b': '0.0456',
        'option_c': '0.4772',
        'option_d': '0.9772',
        'correct_answer': 'A',
        'explanation': 'z = (190 - 150)/20 = 2.0. P(Z > 2.0) = 1 - 0.9772 = 0.0228.',
        'topic_tag': 'real_ap_stats_ced',
    },
]


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=5000")
    c = conn.cursor()

    # Fetch existing question texts to avoid duplicates
    c.execute("SELECT question_text FROM questions")
    existing_texts = {row[0] for row in c.fetchall()}

    inserted = 0
    skipped = 0
    ids_inserted = []
    counts_by_track = {}

    for q in QUESTIONS:
        if q['question_text'] in existing_texts:
            skipped += 1
            continue

        c.execute(
            """
            INSERT INTO questions
                (track, sat_domain, fuar_dimension, difficulty, question_text,
                 question_type, option_a, option_b, option_c, option_d,
                 correct_answer, explanation, topic_tag)
            VALUES (?, ?, ?, ?, ?, 'multiple_choice', ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                q['track'], q['sat_domain'], q['fuar_dimension'], q['difficulty'],
                q['question_text'], q['option_a'], q['option_b'], q['option_c'],
                q['option_d'], q['correct_answer'], q['explanation'], q['topic_tag'],
            ),
        )
        row_id = c.lastrowid
        ids_inserted.append(row_id)
        existing_texts.add(q['question_text'])
        inserted += 1
        counts_by_track[q['track']] = counts_by_track.get(q['track'], 0) + 1

    conn.commit()
    conn.close()

    print(f"\n=== Import Complete ===")
    print(f"Inserted: {inserted} questions")
    print(f"Skipped (already exist): {skipped} questions")
    print(f"\nInserted by track:")
    for track, count in sorted(counts_by_track.items()):
        print(f"  {track}: {count}")

    if ids_inserted:
        print(f"\nNew question IDs: {ids_inserted[0]} – {ids_inserted[-1]}")

    return ids_inserted


if __name__ == '__main__':
    main()
