"""Supplemental Grade 8 questions to reach 3x test variety."""
import sqlite3, os
DB_PATH = os.environ.get('DATABASE_PATH', 'college_ready.db')

QUESTIONS = [
    # ── LINEAR_8 (28 questions) ───────────────────────────────────────────────
    # F — linear_8
    ("grade_8", "linear_8", "F", 1,
     "What is the slope of the line y = 3x − 7?",
     "multiple_choice", "−7", "7", "3", "−3", "C",
     "In slope-intercept form y = mx + b, the slope is m = 3.", "linear_8"),

    ("grade_8", "linear_8", "F", 1,
     "What is the y-intercept of the line y = −2x + 5?",
     "multiple_choice", "−2", "2", "−5", "5", "D",
     "In y = mx + b, b = 5 is the y-intercept.", "linear_8"),

    ("grade_8", "linear_8", "F", 2,
     "A line passes through (0, 4) and (2, 10). What is its slope?",
     "multiple_choice", "2", "3", "5", "6", "B",
     "slope = (10 − 4)/(2 − 0) = 6/2 = 3.", "linear_8"),

    ("grade_8", "linear_8", "F", 2,
     "Which equation represents a line with slope −½ and y-intercept 6?",
     "multiple_choice", "y = 6x − ½", "y = −½x − 6", "y = −½x + 6", "y = ½x + 6", "C",
     "Slope-intercept form: y = (−½)x + 6.", "linear_8"),

    ("grade_8", "linear_8", "F", 3,
     "Two lines: y = 2x + 1 and y = 2x − 5. Which statement is true?",
     "multiple_choice", "They intersect at one point", "They are the same line", "They are parallel", "They are perpendicular", "C",
     "Both lines have slope 2 but different y-intercepts, so they are parallel.", "linear_8"),

    ("grade_8", "linear_8", "F", 4,
     "What is the slope of a line that passes through (−3, 1) and (5, 5)?",
     "multiple_choice", "½", "1", "2", "⅓", "A",
     "slope = (5 − 1)/(5 − (−3)) = 4/8 = ½.", "linear_8"),

    ("grade_8", "linear_8", "F", 3,
     "Solve the system: y = x + 3 and y = −x + 7.",
     "multiple_choice", "(1, 4)", "(2, 5)", "(3, 6)", "(4, 3)", "B",
     "Setting equal: x + 3 = −x + 7 → 2x = 4 → x = 2, y = 5.", "linear_8"),

    # U — linear_8
    ("grade_8", "linear_8", "U", 2,
     "A line has slope 0. Which best describes it?",
     "multiple_choice", "Vertical line", "Diagonal line going up", "Horizontal line", "Line through the origin", "C",
     "A slope of 0 means no rise, so the line is horizontal.", "linear_8"),

    ("grade_8", "linear_8", "U", 2,
     "Table: x = 0, 1, 2, 3 and y = 5, 8, 11, 14. What is the rate of change?",
     "multiple_choice", "2", "3", "4", "5", "B",
     "The y-value increases by 3 for each increase of 1 in x, so the rate of change is 3.", "linear_8"),

    ("grade_8", "linear_8", "U", 3,
     "A system of two linear equations has no solution. What does that mean graphically?",
     "multiple_choice", "The lines cross once", "The lines are the same", "The lines are parallel", "The lines cross at the origin", "C",
     "No solution means the lines never intersect — they are parallel.", "linear_8"),

    ("grade_8", "linear_8", "U", 4,
     "Line A: slope 2, y-intercept 3. Line B: slope −3, y-intercept 8. At what x value do they intersect?",
     "multiple_choice", "x = 0", "x = 1", "x = 2", "x = 3", "B",
     "2x + 3 = −3x + 8 → 5x = 5 → x = 1.", "linear_8"),

    # A — linear_8
    ("grade_8", "linear_8", "A", 2,
     "A plumber charges a $50 flat fee plus $25 per hour. Which equation gives the total cost C for h hours?",
     "multiple_choice", "C = 25h", "C = 50h + 25", "C = 25h + 50", "C = 75h", "C",
     "Flat fee = 50, hourly rate = 25, so C = 25h + 50.", "linear_8"),

    ("grade_8", "linear_8", "A", 3,
     "Maya saves $15 per week and already has $40. Jaylen saves $10 per week and has $90. After how many weeks will they have the same amount?",
     "multiple_choice", "8", "9", "10", "11", "C",
     "15w + 40 = 10w + 90 → 5w = 50 → w = 10.", "linear_8"),

    ("grade_8", "linear_8", "A", 4,
     "A car rental costs $30 per day plus $0.20 per mile. If d = 2 days and m = 50 miles, what is the total cost?",
     "multiple_choice", "$60", "$70", "$80", "$90", "B",
     "T = 30(2) + 0.20(50) = 60 + 10 = $70.", "linear_8"),

    ("grade_8", "linear_8", "A", 4,
     "Two friends start at the same point. Friend A walks at 4 mph; Friend B walks at 6 mph in the opposite direction. After t hours their distance apart is 20 miles. Find t.",
     "multiple_choice", "1.5 hr", "2 hr", "2.5 hr", "3 hr", "B",
     "Distance apart = (4 + 6)t = 10t = 20, so t = 2 hours.", "linear_8"),

    ("grade_8", "linear_8", "A", 5,
     "A cell phone plan charges $0.10 per text. A second plan charges $5 per month plus $0.05 per text. For how many texts per month are the costs equal?",
     "multiple_choice", "50", "75", "100", "150", "C",
     "0.10t = 5 + 0.05t → 0.05t = 5 → t = 100 texts.", "linear_8"),

    # R — linear_8
    ("grade_8", "linear_8", "R", 3,
     "Line p has slope 3. Line q is perpendicular to p. What is the slope of q?",
     "multiple_choice", "3", "−3", "1/3", "−1/3", "D",
     "Perpendicular slopes are negative reciprocals: −1/3.", "linear_8"),

    ("grade_8", "linear_8", "R", 3,
     "Which equation is equivalent to 4x − 2y = 8 written in slope-intercept form?",
     "multiple_choice", "y = 2x − 4", "y = −2x + 4", "y = 4x − 8", "y = 2x + 4", "A",
     "−2y = −4x + 8 → y = 2x − 4.", "linear_8"),

    ("grade_8", "linear_8", "R", 4,
     "If a system of two linear equations has infinitely many solutions, which must be true?",
     "multiple_choice", "The slopes are opposite", "The lines are parallel", "Both equations represent the same line", "The y-intercepts differ", "C",
     "Infinitely many solutions means every point on one line is on the other — they are the same line.", "linear_8"),

    ("grade_8", "linear_8", "R", 4,
     "Which system has exactly one solution? System I: y = 2x + 1 and y = 2x − 3. System II: y = x + 4 and y = −x + 2. System III: 2y = 4x + 6 and y = 2x + 3.",
     "multiple_choice", "I only", "II only", "III only", "I and III", "B",
     "System I: parallel (no solution). System III: same line (infinite solutions). System II: slopes 1 and −1 differ, one intersection.", "linear_8"),

    ("grade_8", "linear_8", "R", 5,
     "A line passes through (0, 3) and has slope −2. What is the x-intercept of the line?",
     "multiple_choice", "1", "3/2", "2", "3", "B",
     "y = −2x + 3. Set y = 0: 2x = 3 → x = 3/2.", "linear_8"),

    ("grade_8", "linear_8", "R", 5,
     "The graph of 3x + 2y = 12 forms a triangle with the coordinate axes. What is the area of that triangle?",
     "multiple_choice", "6 sq units", "8 sq units", "12 sq units", "24 sq units", "C",
     "x-intercept: y=0 → x=4. y-intercept: x=0 → y=6. Area = ½(4)(6) = 12 sq units.", "linear_8"),

    # ── FUNCTIONS_8 (22 questions) ────────────────────────────────────────────
    # F — functions_8
    ("grade_8", "functions_8", "F", 1,
     "Which set of ordered pairs IS a function? A: {(1,2),(2,3),(1,4)} B: {(1,2),(2,3),(3,4)} C: {(1,1),(1,2),(1,3)} D: {(2,1),(2,2),(2,3)}",
     "multiple_choice", "A", "B", "C", "D", "B",
     "A function has exactly one output for each input. Only set B has no repeated x-values.", "functions_8"),

    ("grade_8", "functions_8", "F", 1,
     "If f(x) = 5x − 3, what is f(4)?",
     "multiple_choice", "17", "19", "20", "23", "A",
     "f(4) = 5(4) − 3 = 20 − 3 = 17.", "functions_8"),

    ("grade_8", "functions_8", "F", 2,
     "Which table represents a linear function? A: x=1,2,3 y=1,4,9. B: x=1,2,3 y=3,5,7. C: x=1,2,3 y=2,4,8. D: x=1,2,3 y=1,3,6.",
     "multiple_choice", "A", "B", "C", "D", "B",
     "Table B has a constant rate of change (+2), so it is linear.", "functions_8"),

    ("grade_8", "functions_8", "F", 2,
     "The function y = x² is best described as:",
     "multiple_choice", "Linear", "Nonlinear", "Constant", "Undefined", "B",
     "y = x² curves — the rate of change is not constant, so it is nonlinear.", "functions_8"),

    ("grade_8", "functions_8", "F", 3,
     "Which mapping diagram represents a function? A: 1→3 and 1→5. B: 2→4 and 3→4. C: 4→5 and 4→6. D: 5→7 and 5→8.",
     "multiple_choice", "A", "B", "C", "D", "B",
     "Only B has no input mapped to more than one output.", "functions_8"),

    # U — functions_8
    ("grade_8", "functions_8", "U", 2,
     "A function has a constant rate of change of 4. If f(0) = −1, what is f(3)?",
     "multiple_choice", "7", "11", "12", "13", "B",
     "f(3) = −1 + 4(3) = −1 + 12 = 11.", "functions_8"),

    ("grade_8", "functions_8", "U", 3,
     "Two functions: f(x) = 3x + 2 and g(x) with g(0)=5, g(1)=8, g(2)=11. Which has the greater initial value (y-intercept)?",
     "multiple_choice", "f(x)", "g(x)", "They are equal", "Cannot be determined", "B",
     "f(0) = 2 and g(0) = 5. g(x) has the greater initial value.", "functions_8"),

    ("grade_8", "functions_8", "U", 3,
     "Function A: slope 5, y-intercept 1. Function B passes through (0, 3) and (2, 9). Which has the greater rate of change?",
     "multiple_choice", "Function A", "Function B", "Equal rates", "Cannot be determined", "A",
     "Function A slope = 5. Function B slope = (9−3)/(2−0) = 3. Function A has the greater rate of change.", "functions_8"),

    ("grade_8", "functions_8", "U", 4,
     "Which statement correctly distinguishes a linear from a nonlinear function?",
     "multiple_choice",
     "A linear function always passes through the origin",
     "A linear function has a constant rate of change",
     "A nonlinear function has a negative slope",
     "A linear function is always increasing", "B",
     "The defining property of a linear function is a constant rate of change.", "functions_8"),

    ("grade_8", "functions_8", "U", 4,
     "For f(x) = x² and g(x) = 2x, which has the greater value at x = 4?",
     "multiple_choice", "f(x)", "g(x)", "They are equal", "Cannot be determined", "A",
     "f(4) = 16, g(4) = 8. f(x) is greater at x = 4.", "functions_8"),

    # A — functions_8
    ("grade_8", "functions_8", "A", 2,
     "A phone battery drains at a constant rate. At hour 2 it has 80% charge; at hour 5 it has 50% charge. What is the rate of change per hour?",
     "multiple_choice", "−5%", "−10%", "−15%", "−20%", "B",
     "Rate = (50 − 80)/(5 − 2) = −30/3 = −10% per hour.", "functions_8"),

    ("grade_8", "functions_8", "A", 3,
     "A pool holds 12,000 gallons and drains at 400 gallons per hour. How many hours until it is empty?",
     "multiple_choice", "20 hr", "24 hr", "28 hr", "30 hr", "D",
     "G(h) = 12000 − 400h = 0 → h = 30 hours.", "functions_8"),

    ("grade_8", "functions_8", "A", 4,
     "Carlos's savings: f(x) = 20x + 60. Priya's savings: g(x) = 30x + 10. After how many weeks will they have saved the same amount?",
     "multiple_choice", "3", "4", "5", "6", "C",
     "20x + 60 = 30x + 10 → 50 = 10x → x = 5 weeks.", "functions_8"),

    ("grade_8", "functions_8", "A", 4,
     "A ball dropped from 100 m bounces to half the previous height each time. What is the height after 3 bounces, and is the function linear or nonlinear?",
     "multiple_choice", "Linear; 12.5 m", "Nonlinear; 12.5 m", "Linear; 25 m", "Nonlinear; 25 m", "B",
     "Height = 100(½)³ = 12.5 m. Exponential decay is nonlinear.", "functions_8"),

    ("grade_8", "functions_8", "A", 5,
     "Two linear functions: f(x) = 4x + 1 and g(x) = −x + 16. For what x value is f(x) greater than g(x)?",
     "multiple_choice", "x > 2", "x > 3", "x > 4", "x > 5", "B",
     "4x + 1 > −x + 16 → 5x > 15 → x > 3.", "functions_8"),

    # R — functions_8
    ("grade_8", "functions_8", "R", 3,
     "If f(x) = 2x + k and f(3) = 11, what is k?",
     "multiple_choice", "3", "5", "7", "9", "B",
     "f(3) = 6 + k = 11 → k = 5.", "functions_8"),

    ("grade_8", "functions_8", "R", 3,
     "A function table shows x = 1, 2, 3, 4 and y = 4, 7, 12, 19. Is this function linear?",
     "multiple_choice", "Yes, constant rate of 3", "No, rate of change varies", "Yes, constant rate of 4", "No, y-intercept is missing", "B",
     "Differences in y: 3, 5, 7 — not constant. The function is nonlinear.", "functions_8"),

    ("grade_8", "functions_8", "R", 4,
     "A function g has g(2) = 7 and g(6) = 15. Assuming g is linear, what is g(10)?",
     "multiple_choice", "21", "23", "25", "27", "B",
     "Rate = (15−7)/(6−2) = 2. g(10) = 15 + 2(4) = 23.", "functions_8"),

    # ── GEOMETRY_8 (30 questions) ─────────────────────────────────────────────
    # F — geometry_8
    ("grade_8", "geometry_8", "F", 1,
     "A right triangle has legs of 6 cm and 8 cm. What is the length of the hypotenuse?",
     "multiple_choice", "10 cm", "12 cm", "14 cm", "√28 cm", "A",
     "c² = 6² + 8² = 36 + 64 = 100, so c = 10 cm.", "geometry_8"),

    ("grade_8", "geometry_8", "F", 1,
     "What is the volume of a cone with radius 3 cm and height 4 cm? (Use π ≈ 3.14)",
     "multiple_choice", "12.56 cm³", "37.68 cm³", "50.24 cm³", "75.36 cm³", "B",
     "V = ⅓πr²h = ⅓(3.14)(9)(4) = 37.68 cm³.", "geometry_8"),

    ("grade_8", "geometry_8", "F", 1,
     "A point P(3, −2) is reflected over the x-axis. What are the new coordinates?",
     "multiple_choice", "(−3, −2)", "(3, 2)", "(−3, 2)", "(2, 3)", "B",
     "Reflection over x-axis: (x, y) → (x, −y). P' = (3, 2).", "geometry_8"),

    ("grade_8", "geometry_8", "F", 1,
     "A point (5, −3) is reflected over the y-axis. What are the new coordinates?",
     "multiple_choice", "(−5, 3)", "(5, 3)", "(−5, −3)", "(3, −5)", "C",
     "Reflection over y-axis: (x, y) → (−x, y). Result: (−5, −3).", "geometry_8"),

    ("grade_8", "geometry_8", "F", 2,
     "A triangle is translated 4 units right and 3 units down. Which rule describes this?",
     "multiple_choice", "(x, y) → (x − 4, y + 3)", "(x, y) → (x + 4, y − 3)", "(x, y) → (x + 3, y − 4)", "(x, y) → (x − 3, y + 4)", "B",
     "Right means +x, down means −y: (x+4, y−3).", "geometry_8"),

    ("grade_8", "geometry_8", "F", 2,
     "A right triangle has hypotenuse 13 and one leg 5. What is the other leg?",
     "multiple_choice", "8", "10", "11", "12", "D",
     "leg² = 13² − 5² = 169 − 25 = 144, leg = 12.", "geometry_8"),

    ("grade_8", "geometry_8", "F", 2,
     "A square room has area 196 ft². What is the side length?",
     "multiple_choice", "12 ft", "13 ft", "14 ft", "15 ft", "C",
     "Side = √196 = 14 ft.", "geometry_8"),

    ("grade_8", "geometry_8", "F", 3,
     "What is the volume of a sphere with radius 3 cm? (Use π ≈ 3.14)",
     "multiple_choice", "28.26 cm³", "56.52 cm³", "113.04 cm³", "339.12 cm³", "C",
     "V = (4/3)πr³ = (4/3)(3.14)(27) = 113.04 cm³.", "geometry_8"),

    # U — geometry_8
    ("grade_8", "geometry_8", "U", 2,
     "Two triangles are congruent. Which transformation(s) could map one onto the other?",
     "multiple_choice", "Only dilation", "Only rotation", "Only reflection", "Any combination of reflection, rotation, and translation", "D",
     "Rigid motions (reflections, rotations, translations) preserve shape and size, establishing congruence.", "geometry_8"),

    ("grade_8", "geometry_8", "U", 2,
     "A figure is dilated by a scale factor of 2. How does this affect the area?",
     "multiple_choice", "Area doubles", "Area triples", "Area quadruples", "Area stays the same", "C",
     "When linear dimensions scale by k, area scales by k². Scale factor 2 → area × 4.", "geometry_8"),

    ("grade_8", "geometry_8", "U", 3,
     "Triangle ABC ~ Triangle DEF. AB = 6, BC = 9, and DE = 4. What is EF?",
     "multiple_choice", "3", "6", "8", "12", "B",
     "Scale factor = DE/AB = 4/6 = 2/3. EF = 9 × (2/3) = 6.", "geometry_8"),

    ("grade_8", "geometry_8", "U", 3,
     "A point Q(2, 5) is rotated 90° clockwise about the origin. What are the new coordinates?",
     "multiple_choice", "(−5, 2)", "(5, −2)", "(−2, −5)", "(2, −5)", "B",
     "90° clockwise: (x, y) → (y, −x). Q' = (5, −2).", "geometry_8"),

    ("grade_8", "geometry_8", "U", 3,
     "Which transformation always preserves both size and shape?",
     "multiple_choice", "Dilation", "Translation", "Stretch", "Shear", "B",
     "Translations are rigid motions — they preserve both size and shape.", "geometry_8"),

    ("grade_8", "geometry_8", "U", 4,
     "The Pythagorean theorem applies only to which type of triangle?",
     "multiple_choice", "Isosceles", "Equilateral", "Right", "Obtuse", "C",
     "The Pythagorean theorem (a² + b² = c²) applies only to right triangles.", "geometry_8"),

    ("grade_8", "geometry_8", "U", 4,
     "A rectangular prism has dimensions 4 × 3 × 2. A similar prism has dimensions 8 × 6 × 4. What is the ratio of their volumes?",
     "multiple_choice", "2:1", "4:1", "6:1", "8:1", "D",
     "Scale factor = 2. Volume ratio = 2³ = 8, so 8:1.", "geometry_8"),

    # A — geometry_8
    ("grade_8", "geometry_8", "A", 2,
     "A ladder 10 ft long leans against a wall. The base is 6 ft from the wall. How high does the ladder reach?",
     "multiple_choice", "6 ft", "7 ft", "8 ft", "9 ft", "C",
     "h² = 10² − 6² = 100 − 36 = 64, h = 8 ft.", "geometry_8"),

    ("grade_8", "geometry_8", "A", 2,
     "If triangle ABC is congruent to triangle DEF and AB = 7 cm, what is DE?",
     "multiple_choice", "3.5 cm", "7 cm", "14 cm", "Cannot determine", "B",
     "Congruent triangles have equal corresponding sides. AB corresponds to DE, so DE = 7 cm.", "geometry_8"),

    ("grade_8", "geometry_8", "A", 3,
     "A city block is a rectangle 300 m × 400 m. A pedestrian walks diagonally across. How far do they walk?",
     "multiple_choice", "350 m", "450 m", "500 m", "600 m", "C",
     "Diagonal = √(300² + 400²) = √250000 = 500 m.", "geometry_8"),

    ("grade_8", "geometry_8", "A", 3,
     "A cylindrical water tank has radius 5 m and height 10 m. What is its volume? (Use π ≈ 3.14)",
     "multiple_choice", "314 m³", "628 m³", "785 m³", "1570 m³", "C",
     "V = πr²h = 3.14 × 25 × 10 = 785 m³.", "geometry_8"),

    ("grade_8", "geometry_8", "A", 4,
     "A triangular garden has a right angle. The two legs are 7 m and 24 m. What is the perimeter?",
     "multiple_choice", "52 m", "54 m", "56 m", "58 m", "C",
     "Hypotenuse = √(49 + 576) = √625 = 25 m. Perimeter = 7 + 24 + 25 = 56 m.", "geometry_8"),

    ("grade_8", "geometry_8", "A", 4,
     "A cone-shaped paper cup has radius 3 cm and height 9 cm. What is its volume? (Use π ≈ 3.14)",
     "multiple_choice", "56.52 cm³", "84.78 cm³", "169.56 cm³", "254.34 cm³", "B",
     "V = ⅓πr²h = ⅓(3.14)(9)(9) = 84.78 cm³.", "geometry_8"),

    # R — geometry_8
    ("grade_8", "geometry_8", "R", 3,
     "After a rotation of 180° about the origin, point (−3, 4) maps to which coordinates?",
     "multiple_choice", "(3, −4)", "(−3, −4)", "(4, −3)", "(−4, 3)", "A",
     "180° rotation: (x, y) → (−x, −y). (−3, 4) → (3, −4).", "geometry_8"),

    ("grade_8", "geometry_8", "R", 4,
     "Triangle PQR has vertices P(0,0), Q(4,0), R(0,3). After dilation by factor 3 centered at the origin, what is the area of the image?",
     "multiple_choice", "18 sq units", "36 sq units", "54 sq units", "108 sq units", "C",
     "Original area = ½(4)(3) = 6. Dilation by 3 multiplies area by 9. New area = 54.", "geometry_8"),

    ("grade_8", "geometry_8", "R", 4,
     "Two similar figures have areas of 16 cm² and 36 cm². What is the ratio of their corresponding side lengths?",
     "multiple_choice", "2:3", "4:6", "4:9", "8:12", "A",
     "Area ratio = 16:36 = 4:9. Side length ratio = √4:√9 = 2:3.", "geometry_8"),

    ("grade_8", "geometry_8", "R", 5,
     "A square has side length s. A diagonal is drawn. What is the length of the diagonal in terms of s?",
     "multiple_choice", "s√2", "s√3", "2s", "s²", "A",
     "d² = s² + s² = 2s², so d = s√2.", "geometry_8"),

    ("grade_8", "geometry_8", "R", 5,
     "A sphere has volume 36π cm³. What is its radius?",
     "multiple_choice", "2 cm", "3 cm", "4 cm", "6 cm", "B",
     "V = (4/3)πr³ = 36π → r³ = 27 → r = 3 cm.", "geometry_8"),

    # ── NUMBER_SYSTEM_8 (20 questions) ────────────────────────────────────────
    # F — number_system_8
    ("grade_8", "number_system_8", "F", 1,
     "Which of the following is irrational? A: √16  B: 0.333…  C: √7  D: ¾",
     "multiple_choice", "A", "B", "C", "D", "C",
     "√7 ≈ 2.6457… is non-terminating and non-repeating, so it is irrational.", "number_system_8"),

    ("grade_8", "number_system_8", "F", 1,
     "What is ∛64?",
     "multiple_choice", "4", "6", "8", "16", "A",
     "4³ = 64, so ∛64 = 4.", "number_system_8"),

    ("grade_8", "number_system_8", "F", 2,
     "Express 0.000047 in scientific notation.",
     "multiple_choice", "4.7 × 10⁻⁵", "4.7 × 10⁻⁴", "47 × 10⁻⁶", "0.47 × 10⁻⁴", "A",
     "Move decimal 5 places right: 4.7 × 10⁻⁵.", "number_system_8"),

    ("grade_8", "number_system_8", "F", 2,
     "Which is larger: √50 or 7?",
     "multiple_choice", "√50", "7", "They are equal", "Cannot be compared", "A",
     "√50 ≈ 7.07, which is greater than 7.", "number_system_8"),

    ("grade_8", "number_system_8", "F", 2,
     "Which of the following is rational? A: √5  B: π  C: √49  D: 0.101001000…",
     "multiple_choice", "A", "B", "C", "D", "C",
     "√49 = 7, an integer, which is rational.", "number_system_8"),

    ("grade_8", "number_system_8", "F", 3,
     "Simplify: (3 × 10⁴) × (2 × 10³).",
     "multiple_choice", "6 × 10⁷", "5 × 10⁷", "6 × 10¹²", "6 × 10⁶", "A",
     "(3 × 2) × 10^(4+3) = 6 × 10⁷.", "number_system_8"),

    ("grade_8", "number_system_8", "F", 3,
     "Between which two consecutive integers does √45 lie?",
     "multiple_choice", "5 and 6", "6 and 7", "7 and 8", "4 and 5", "B",
     "6² = 36 < 45 < 49 = 7², so √45 is between 6 and 7.", "number_system_8"),

    # U — number_system_8
    ("grade_8", "number_system_8", "U", 2,
     "Which statement about irrational numbers is TRUE?",
     "multiple_choice",
     "They can be written as a fraction p/q",
     "Their decimal expansions terminate",
     "Their decimal expansions are non-terminating and non-repeating",
     "They are always negative", "C",
     "Irrational numbers have infinite, non-repeating decimal expansions.", "number_system_8"),

    ("grade_8", "number_system_8", "U", 3,
     "A number in scientific notation is 3.6 × 10⁻³. Which standard form is correct?",
     "multiple_choice", "3600", "0.36", "0.0036", "36000", "C",
     "10⁻³ moves decimal 3 places left: 3.6 → 0.0036.", "number_system_8"),

    ("grade_8", "number_system_8", "U", 3,
     "Which correctly converts 6.2 × 10⁵ to standard form?",
     "multiple_choice", "62,000", "620,000", "6,200,000", "0.000062", "B",
     "Move decimal 5 places right: 620,000.", "number_system_8"),

    ("grade_8", "number_system_8", "U", 3,
     "Which best explains why √2 is irrational?",
     "multiple_choice",
     "It is less than 2",
     "It cannot be expressed as a ratio of two integers",
     "It is between 1 and 2",
     "It has a square root", "B",
     "A number is irrational when it cannot be written as p/q for integers p and q.", "number_system_8"),

    ("grade_8", "number_system_8", "U", 4,
     "Of the following — π, −4, √9, and 0.1212… — which set includes ONLY rational numbers?",
     "multiple_choice", "π and −4", "−4 and √9 and 0.1212…", "π and √9", "All four", "B",
     "−4 is an integer; √9 = 3 is an integer; 0.1212… = 4/33 repeats. π is irrational.", "number_system_8"),

    # A — number_system_8
    ("grade_8", "number_system_8", "A", 2,
     "Earth's mass is approximately 5.97 × 10²⁴ kg. The Moon's mass is 7.34 × 10²² kg. About how many times more massive is Earth?",
     "multiple_choice", "About 8 times", "About 80 times", "About 800 times", "About 8000 times", "B",
     "5.97 × 10²⁴ ÷ 7.34 × 10²² ≈ 0.813 × 10² ≈ 81 ≈ 80.", "number_system_8"),

    ("grade_8", "number_system_8", "A", 3,
     "A red blood cell is about 8 × 10⁻⁶ m in diameter. A human hair is about 7 × 10⁻⁵ m wide. About how many red blood cells fit across a hair?",
     "multiple_choice", "About 8", "About 9", "About 87", "About 875", "B",
     "7 × 10⁻⁵ ÷ 8 × 10⁻⁶ = (7/8) × 10 = 8.75 ≈ 9 cells.", "number_system_8"),

    ("grade_8", "number_system_8", "A", 3,
     "The diameter of a virus is 3 × 10⁻⁷ m. The diameter of a bacterium is 2 × 10⁻⁶ m. About how many times larger is the bacterium?",
     "multiple_choice", "About 6.7 times", "About 3 times", "About 20 times", "About 0.15 times", "A",
     "2 × 10⁻⁶ ÷ 3 × 10⁻⁷ = (2/3) × 10 ≈ 6.7 times.", "number_system_8"),

    ("grade_8", "number_system_8", "A", 4,
     "A computer performs 2.5 × 10⁹ operations per second. How many operations occur in 4 × 10² seconds?",
     "multiple_choice", "1 × 10¹²", "1 × 10¹¹", "6.5 × 10¹¹", "1 × 10⁹", "A",
     "2.5 × 10⁹ × 4 × 10² = 10 × 10¹¹ = 1 × 10¹².", "number_system_8"),

    # R — number_system_8
    ("grade_8", "number_system_8", "R", 3,
     "Is the sum of a rational number and an irrational number always rational, always irrational, or sometimes either?",
     "multiple_choice", "Always rational", "Always irrational", "Sometimes rational, sometimes irrational", "Always zero", "B",
     "Rational + irrational is always irrational. If the sum were rational, subtracting the rational addend would make the irrational rational — a contradiction.", "number_system_8"),

    ("grade_8", "number_system_8", "R", 3,
     "Is the product of two irrational numbers always irrational?",
     "multiple_choice", "Yes, always", "No, not always", "Only if both are square roots", "Only if they are different numbers", "B",
     "Example: √2 × √2 = 2, which is rational. So the product of two irrationals is not always irrational.", "number_system_8"),

    ("grade_8", "number_system_8", "R", 4,
     "Arrange from least to greatest: √3, 1.7, 7/4, √2.",
     "multiple_choice", "√2, √3, 1.7, 7/4", "√2, 1.7, 7/4, √3", "1.7, √2, 7/4, √3", "√2, 1.7, √3, 7/4", "B",
     "√2≈1.414, 1.7, 7/4=1.75, √3≈1.732. Order: √2 < 1.7 < 7/4 < √3.", "number_system_8"),

    ("grade_8", "number_system_8", "R", 5,
     "If n² = 50 and n > 0, between which two consecutive integers does n lie?",
     "multiple_choice", "6 and 7", "7 and 8", "5 and 6", "4 and 5", "B",
     "7² = 49 < 50 < 64 = 8², so √50 is between 7 and 8.", "number_system_8"),

    # ── DATA_8 (16 questions) ─────────────────────────────────────────────────
    # F — data_8
    ("grade_8", "data_8", "F", 1,
     "A scatter plot shows hours studied on the x-axis and test score on the y-axis. Points trend upward. What type of association is this?",
     "multiple_choice", "Negative linear", "No association", "Positive linear", "Non-linear", "C",
     "Points trending upward from left to right show a positive linear association.", "data_8"),

    ("grade_8", "data_8", "F", 1,
     "In a scatter plot, a data point that is far from the rest of the points is called a(n):",
     "multiple_choice", "Cluster", "Outlier", "Line of best fit", "Residual", "B",
     "A data point far from the general pattern is called an outlier.", "data_8"),

    ("grade_8", "data_8", "F", 2,
     "A line of best fit passes through (0, 20) and (5, 45). What is the slope of the line?",
     "multiple_choice", "4", "5", "6", "7", "B",
     "Slope = (45 − 20)/(5 − 0) = 25/5 = 5.", "data_8"),

    ("grade_8", "data_8", "F", 2,
     "In a two-way table, 30 out of 75 students chose Math. What fraction chose Math?",
     "multiple_choice", "2/5", "1/3", "5/12", "2/3", "A",
     "30/75 = 2/5.", "data_8"),

    ("grade_8", "data_8", "F", 3,
     "The equation of a line of best fit is y = 3x + 10. Predict y when x = 8.",
     "multiple_choice", "24", "30", "34", "38", "C",
     "y = 3(8) + 10 = 24 + 10 = 34.", "data_8"),

    # U — data_8
    ("grade_8", "data_8", "U", 2,
     "A scatter plot shows hours of TV watched vs. GPA. Points trend downward. What does this suggest?",
     "multiple_choice", "More TV is associated with higher GPA", "More TV is associated with lower GPA", "TV watching has no effect on GPA", "GPA causes more TV watching", "B",
     "A downward trend shows a negative association.", "data_8"),

    ("grade_8", "data_8", "U", 2,
     "A scatter plot has a correlation close to 0. What does this mean?",
     "multiple_choice", "Perfect positive correlation", "Strong negative correlation", "Little or no linear association", "A curved relationship", "C",
     "A correlation near 0 means there is little or no linear relationship between the variables.", "data_8"),

    ("grade_8", "data_8", "U", 3,
     "40 boys were surveyed; 25 like soccer. 60 girls were surveyed; 30 like soccer. Which gender has a higher relative frequency of liking soccer?",
     "multiple_choice", "Boys", "Girls", "Equal", "Cannot determine", "A",
     "Boys: 25/40 = 62.5%. Girls: 30/60 = 50%. Boys have the higher relative frequency.", "data_8"),

    ("grade_8", "data_8", "U", 3,
     "What does a cluster in a scatter plot indicate?",
     "multiple_choice", "An outlier in the data", "A group of data points with similar values", "A negative association", "A perfect correlation", "B",
     "A cluster shows data points concentrated in a region with similar x and y values.", "data_8"),

    ("grade_8", "data_8", "U", 4,
     "A line of best fit for shoe size (x) and height (y) is y = 2.5x + 140. What does the slope 2.5 represent?",
     "multiple_choice", "The shoe size when height is 0", "The height when shoe size is 0", "The predicted increase in height (cm) per one shoe size increase", "The average height", "C",
     "Slope = rate of change: for each 1-unit increase in shoe size, height increases by 2.5 cm.", "data_8"),

    # A — data_8
    ("grade_8", "data_8", "A", 2,
     "A line of best fit is y = −4x + 100, where x is years since 2000 and y is number of landlines (thousands). Predict landlines in 2015.",
     "multiple_choice", "30", "35", "40", "45", "C",
     "x = 15: y = −4(15) + 100 = −60 + 100 = 40.", "data_8"),

    ("grade_8", "data_8", "A", 3,
     "Survey: 50 students prefer dogs; 30 prefer cats; 20 prefer fish (100 total). What is the probability a randomly selected student prefers cats?",
     "multiple_choice", "1/5", "3/10", "1/3", "2/5", "B",
     "30/100 = 3/10.", "data_8"),

    ("grade_8", "data_8", "A", 3,
     "Two-way table: 90 play sports, 70 play an instrument, 30 do both, out of 200 students. How many do neither?",
     "multiple_choice", "50", "60", "70", "80", "C",
     "Sports or instruments = 90 + 70 − 30 = 130. Neither = 200 − 130 = 70.", "data_8"),

    ("grade_8", "data_8", "A", 4,
     "A two-way table: 60 students prefer comedy; 40 prefer action. 30 comedy fans are female; 25 action fans are female. What fraction of all surveyed students are female?",
     "multiple_choice", "11/20", "11/40", "11/100", "55/200", "A",
     "Total female = 30 + 25 = 55. Total students = 100. Fraction = 55/100 = 11/20.", "data_8"),

    # R — data_8
    ("grade_8", "data_8", "R", 4,
     "The line of best fit for a data set is y = 2x + 5. A data point (6, 20) is plotted. What is the residual for this point?",
     "multiple_choice", "−3", "3", "7", "−7", "B",
     "Predicted: 2(6) + 5 = 17. Residual = actual − predicted = 20 − 17 = 3.", "data_8"),

    ("grade_8", "data_8", "R", 4,
     "A line of best fit is y = 1.5x + 4 where x is temperature (°F). Predict sales when x = 50. Why should this be done with caution?",
     "multiple_choice", "The equation has a negative slope", "x = 50 may be far outside the observed data range (extrapolation)", "The y-intercept is too small", "The slope is not an integer", "B",
     "Predicting far beyond the observed data range is extrapolation, which is unreliable.", "data_8"),

    ("grade_8", "data_8", "R", 5,
     "A researcher claims 'ice cream sales cause drowning' because both increase in summer. What error in reasoning is this?",
     "multiple_choice", "Incorrect scatter plot", "Confusing correlation with causation", "Extrapolation error", "Sampling error", "B",
     "Both variables are caused by a third factor (summer heat). Correlation does not imply causation.", "data_8"),

    ("grade_8", "data_8", "R", 5,
     "A line of best fit is y = −4x + 100. At what x value does the model predict zero sales?",
     "multiple_choice", "10", "15", "20", "25", "D",
     "Set y = 0: −4x + 100 = 0 → 4x = 100 → x = 25.", "data_8"),

    # ── 12 additional questions to reach 116 total ─────────────────────────────

    # linear_8 — 3 more
    ("grade_8", "linear_8", "F", 2,
     "Write the equation of the line with slope 4 that passes through the point (0, −3).",
     "multiple_choice", "y = 4x + 3", "y = −3x + 4", "y = 4x − 3", "y = 3x + 4", "C",
     "Slope-intercept form: y = mx + b = 4x + (−3) = 4x − 3.", "linear_8"),

    ("grade_8", "linear_8", "U", 3,
     "A table shows: x = −2, 0, 2, 4 and y = 9, 5, 1, −3. What is the equation of the linear function?",
     "multiple_choice", "y = −2x + 5", "y = 2x − 5", "y = −2x − 5", "y = 2x + 5", "A",
     "Rate of change = (5 − 9)/(0 − (−2)) = −2. y-intercept = 5. Equation: y = −2x + 5.", "linear_8"),

    ("grade_8", "linear_8", "A", 3,
     "A water tank holds 500 gallons. It fills at 20 gallons per minute. How many minutes to fill it completely?",
     "multiple_choice", "20 min", "25 min", "30 min", "40 min", "B",
     "500 ÷ 20 = 25 minutes.", "linear_8"),

    # functions_8 — 3 more
    ("grade_8", "functions_8", "F", 2,
     "Given f(x) = −3x + 7, what is f(−2)?",
     "multiple_choice", "1", "11", "13", "−1", "C",
     "f(−2) = −3(−2) + 7 = 6 + 7 = 13.", "functions_8"),

    ("grade_8", "functions_8", "U", 2,
     "Which graph best represents a nonlinear function?",
     "multiple_choice", "A straight line with positive slope", "A horizontal line", "A curve that gets steeper", "A straight line with negative slope", "C",
     "A curve with changing steepness has a non-constant rate of change — the defining feature of a nonlinear function.", "functions_8"),

    ("grade_8", "functions_8", "R", 4,
     "A linear function has f(−1) = 8 and f(3) = 0. What is the equation of the function?",
     "multiple_choice", "y = −2x + 6", "y = 2x + 6", "y = −2x − 6", "y = 2x − 6", "A",
     "Slope = (0 − 8)/(3 − (−1)) = −8/4 = −2. Using (3, 0): 0 = −2(3) + b → b = 6. y = −2x + 6.", "functions_8"),

    # geometry_8 — 2 more
    ("grade_8", "geometry_8", "A", 3,
     "A television screen is rectangular with width 40 in and diagonal 50 in. What is the height of the screen?",
     "multiple_choice", "20 in", "25 in", "30 in", "35 in", "C",
     "height² = 50² − 40² = 2500 − 1600 = 900. Height = 30 in.", "geometry_8"),

    ("grade_8", "geometry_8", "U", 3,
     "A dilation with scale factor ½ maps triangle XYZ onto triangle X'Y'Z'. If XY = 10 cm, what is X'Y'?",
     "multiple_choice", "20 cm", "10 cm", "5 cm", "2.5 cm", "C",
     "X'Y' = ½ × 10 = 5 cm.", "geometry_8"),

    # number_system_8 — 2 more
    ("grade_8", "number_system_8", "F", 1,
     "What is √121?",
     "multiple_choice", "10", "11", "12", "13", "B",
     "11 × 11 = 121, so √121 = 11.", "number_system_8"),

    ("grade_8", "number_system_8", "A", 2,
     "Write 45,300,000 in scientific notation.",
     "multiple_choice", "4.53 × 10⁶", "4.53 × 10⁷", "45.3 × 10⁶", "0.453 × 10⁸", "B",
     "4.53 × 10⁷ (move decimal 7 places left).", "number_system_8"),

    # data_8 — 2 more
    ("grade_8", "data_8", "A", 2,
     "A scatter plot shows a positive association between hours of practice and points scored in a game. Which is a reasonable prediction? The line of best fit is y = 5x + 10.",
     "multiple_choice", "A player who practices 6 hours scores about 30 points", "A player who practices 6 hours scores about 40 points", "A player who practices 6 hours scores about 50 points", "A player who practices 6 hours scores about 60 points", "B",
     "y = 5(6) + 10 = 30 + 10 = 40 points.", "data_8"),

    ("grade_8", "data_8", "U", 3,
     "A two-way table shows data for 200 students: 110 are in 8th grade, 90 are in 7th grade. Of 8th graders, 66 prefer reading. What is the relative frequency of 8th graders who prefer reading?",
     "multiple_choice", "33%", "55%", "60%", "73%", "C",
     "66 out of 110 eighth graders prefer reading: 66/110 = 0.60 = 60%.", "data_8"),
]


def seed():
    conn = sqlite3.connect(DB_PATH)
    inserted = 0
    for q in QUESTIONS:
        exists = conn.execute("SELECT id FROM questions WHERE question_text = ?", (q[4],)).fetchone()
        if not exists:
            conn.execute("""INSERT INTO questions (track, sat_domain, fuar_dimension, difficulty,
                question_text, question_type, option_a, option_b, option_c, option_d,
                correct_answer, explanation, topic_tag) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""", q)
            inserted += 1
    conn.commit()
    conn.close()
    print(f"[seed] Grade 8 supplement: {inserted} new questions inserted")
    return inserted


if __name__ == "__main__":
    seed()
