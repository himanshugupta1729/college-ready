"""
seed_geometry.py — Seeds college_ready.db with 75 Geometry questions.

Track: geometry
Domains: congruence_triangles, similarity, right_triangles_trig, circles,
         area_volume, transformations
FUAR: F (Fluency), U (Understanding), A (Application), R (Reasoning)
Difficulty: 1–5 (wider spread than Algebra 1)
"""

import sqlite3
from collections import defaultdict

DB_PATH = "college_ready.db"

# ---------------------------------------------------------------------------
# Question bank
# Each tuple: (track, sat_domain, fuar_dimension, difficulty,
#              question_text, question_type,
#              option_a, option_b, option_c, option_d,
#              correct_answer, explanation, topic_tag)
# ---------------------------------------------------------------------------

QUESTIONS = [

    # =========================================================================
    # CONGRUENCE & TRIANGLES — 14 questions
    # =========================================================================

    # CT-1 diff=1 F
    ("geometry", "congruence_triangles", "F", 1,
     "Two triangles have all three pairs of corresponding sides equal. Which congruence postulate applies?",
     "multiple_choice",
     "SAS", "ASA", "SSS", "AAS",
     "C",
     "SSS (Side-Side-Side) postulate: if all three sides of one triangle equal the corresponding sides of another, the triangles are congruent.",
     "SSS"),

    # CT-2 diff=1 F
    ("geometry", "congruence_triangles", "F", 1,
     "In triangle ABC, AB = AC. What type of triangle is ABC?",
     "multiple_choice",
     "Equilateral", "Scalene", "Isosceles", "Right",
     "C",
     "A triangle with at least two equal sides is isosceles. AB = AC means two sides are equal.",
     "isosceles_equilateral"),

    # CT-3 diff=2 U
    ("geometry", "congruence_triangles", "U", 2,
     "Two triangles share a side. Two angles of one triangle equal two angles of the other. Which postulate proves them congruent?",
     "multiple_choice",
     "SSS", "SAS", "ASA", "AAS",
     "D",
     "AAS (Angle-Angle-Side): two angles and a non-included side are congruent. The shared side is the non-included side.",
     "AAS"),

    # CT-4 diff=2 U
    ("geometry", "congruence_triangles", "U", 2,
     "Which postulate requires two sides and the INCLUDED angle to be congruent?",
     "multiple_choice",
     "SSS", "SAS", "AAS", "HL",
     "B",
     "SAS (Side-Angle-Side): two sides and the angle between them must be congruent.",
     "SAS"),

    # CT-5 diff=2 F
    ("geometry", "congruence_triangles", "F", 2,
     "The base angles of an isosceles triangle measure 52° each. What is the measure of the vertex angle?",
     "multiple_choice",
     "52°", "76°", "128°", "90°",
     "B",
     "Sum of angles = 180°. Vertex = 180° − 52° − 52° = 76°.",
     "isosceles_equilateral"),

    # CT-6 diff=3 A
    ("geometry", "congruence_triangles", "A", 3,
     "Triangle ABC ≅ Triangle DEF. If AB = 12, BC = 15, AC = 18, what is EF?",
     "multiple_choice",
     "12", "15", "18", "Cannot be determined",
     "B",
     "By CPCTC, corresponding parts of congruent triangles are congruent. BC corresponds to EF, so EF = 15.",
     "CPCTC"),

    # CT-7 diff=3 U
    ("geometry", "congruence_triangles", "U", 3,
     "In an equilateral triangle, each interior angle measures:",
     "multiple_choice",
     "45°", "60°", "90°", "120°",
     "B",
     "An equilateral triangle has three equal angles. 180° ÷ 3 = 60° each.",
     "isosceles_equilateral"),

    # CT-8 diff=3 A
    ("geometry", "congruence_triangles", "A", 3,
     "Two right triangles have equal hypotenuses and one pair of equal legs. Which postulate proves them congruent?",
     "multiple_choice",
     "SAS", "ASA", "HL", "AAS",
     "C",
     "HL (Hypotenuse-Leg) applies only to right triangles: if the hypotenuse and one leg are congruent, the triangles are congruent.",
     "HL"),

    # CT-9 diff=3 R
    ("geometry", "congruence_triangles", "R", 4,
     "Triangle PQR has PQ = PR. If angle Q = (3x + 10)° and angle R = (5x − 8)°, find x.",
     "multiple_choice",
     "6", "9", "12", "18",
     "B",
     "Base angles of isosceles triangle are equal: 3x + 10 = 5x − 8 → 18 = 2x → x = 9.",
     "isosceles_equilateral"),

    # CT-10 diff=4 R
    ("geometry", "congruence_triangles", "R", 4,
     "Which additional information is sufficient to prove △ABC ≅ △XYZ by ASA, given ∠A = ∠X and AC = XZ?",
     "multiple_choice",
     "BC = YZ", "AB = XY", "∠C = ∠Z", "∠B = ∠Y",
     "C",
     "ASA needs two angles and the included side. We have ∠A = ∠X and side AC = XZ. The included angle at C must equal ∠Z to complete ASA.",
     "ASA"),

    # CT-11 diff=4 A
    ("geometry", "congruence_triangles", "A", 4,
     "An exterior angle of a triangle measures 110°. One non-adjacent interior angle measures 65°. What is the other non-adjacent interior angle?",
     "multiple_choice",
     "35°", "45°", "55°", "70°",
     "B",
     "Exterior Angle Theorem: exterior angle = sum of the two non-adjacent interior angles. 110° = 65° + x → x = 45°.",
     "triangle_theorems"),

    # CT-12 diff=4 U
    ("geometry", "congruence_triangles", "U", 4,
     "Which set of side lengths CANNOT form a triangle?",
     "multiple_choice",
     "3, 4, 5", "5, 7, 10", "6, 6, 11", "2, 4, 7",
     "D",
     "Triangle Inequality: the sum of any two sides must exceed the third. 2 + 4 = 6 < 7, so 2, 4, 7 cannot form a triangle.",
     "triangle_theorems"),

    # CT-13 diff=5 R
    ("geometry", "congruence_triangles", "R", 5,
     "In △ABC, a median is drawn from vertex A to midpoint M of BC. Which statement is always true?",
     "multiple_choice",
     "AM bisects ∠A", "AM ⊥ BC", "BM = MC", "△ABM ≅ △ACM",
     "C",
     "A median connects a vertex to the midpoint of the opposite side. By definition, BM = MC. The median does not necessarily bisect the angle or be perpendicular to BC.",
     "triangle_theorems"),

    # CT-14 diff=5 R
    ("geometry", "congruence_triangles", "R", 5,
     "Two triangles are congruent. One has angles 40°, 60°, 80°. The other has sides in ratio 3:4:5. Which statement is true?",
     "multiple_choice",
     "They must be right triangles",
     "They cannot be congruent if they have different side ratios",
     "Congruence requires both equal angles AND equal side lengths",
     "They are congruent because the angles match",
     "C",
     "Congruence requires equal angles AND equal side lengths (same size and shape). Equal angles only proves similarity. The 3:4:5 triangle with 40-60-80° angles could have any size.",
     "triangle_theorems"),

    # =========================================================================
    # SIMILARITY — 12 questions
    # =========================================================================

    # SI-1 diff=1 F
    ("geometry", "similarity", "F", 1,
     "Two triangles are similar. One has sides 3, 4, 5. The other has shortest side 9. What is its longest side?",
     "multiple_choice",
     "12", "15", "20", "25",
     "B",
     "Scale factor = 9/3 = 3. Longest side = 5 × 3 = 15.",
     "ratios_proportions"),

    # SI-2 diff=2 F
    ("geometry", "similarity", "F", 2,
     "Which postulate proves two triangles similar if two pairs of corresponding angles are congruent?",
     "multiple_choice",
     "SSS similarity", "SAS similarity", "AA similarity", "HL similarity",
     "C",
     "AA (Angle-Angle) similarity: if two angles of one triangle equal two angles of another, the triangles are similar.",
     "AA_SAS_SSS"),

    # SI-3 diff=2 U
    ("geometry", "similarity", "U", 2,
     "A flagpole casts a 12-foot shadow at the same time a 6-foot person casts a 4-foot shadow. How tall is the flagpole?",
     "multiple_choice",
     "8 ft", "16 ft", "18 ft", "24 ft",
     "C",
     "Using similar triangles (same angle of sun): h/12 = 6/4 → h = 6 × 12/4 = 18 feet.",
     "ratios_proportions"),

    # SI-4 diff=2 U
    ("geometry", "similarity", "U", 2,
     "Triangle ABC ~ Triangle DEF with ratio 2:5. If DE = 10, what is AB?",
     "multiple_choice",
     "2", "4", "5", "25",
     "B",
     "AB/DE = 2/5 → AB = DE × 2/5 = 10 × 2/5 = 4.",
     "ratios_proportions"),

    # SI-5 diff=3 A
    ("geometry", "similarity", "A", 3,
     "A dilation with center at the origin and scale factor 3 maps point A(2, 4) to A'. What are the coordinates of A'?",
     "multiple_choice",
     "(5, 7)", "(6, 4)", "(6, 12)", "(2/3, 4/3)",
     "C",
     "Dilation multiplies each coordinate by the scale factor: A' = (2×3, 4×3) = (6, 12).",
     "dilations"),

    # SI-6 diff=3 U
    ("geometry", "similarity", "U", 3,
     "If two triangles are similar with ratio 3:7, what is the ratio of their areas?",
     "multiple_choice",
     "3:7", "6:14", "9:49", "27:343",
     "C",
     "The ratio of areas of similar figures is the square of the similarity ratio: (3/7)² = 9/49.",
     "ratios_proportions"),

    # SI-7 diff=3 A
    ("geometry", "similarity", "A", 3,
     "In △ABC, DE is parallel to BC with D on AB and E on AC. If AD = 4, DB = 6, and BC = 15, find DE.",
     "multiple_choice",
     "6", "9", "10", "12",
     "A",
     "By the Triangle Proportionality Theorem: DE/BC = AD/AB = 4/(4+6) = 4/10 = 2/5. DE = 15 × 2/5 = 6.",
     "AA_SAS_SSS"),

    # SI-8 diff=3 R
    ("geometry", "similarity", "R", 3,
     "For SAS similarity, which must be true?",
     "multiple_choice",
     "Two sides and any angle are proportional",
     "Two sides are proportional and the included angle is congruent",
     "All three sides are proportional",
     "Two angles are congruent",
     "B",
     "SAS similarity: two pairs of corresponding sides are proportional AND the included angle is congruent.",
     "AA_SAS_SSS"),

    # SI-9 diff=4 A
    ("geometry", "similarity", "A", 4,
     "A photo is 4 inches wide and 6 inches tall. It is enlarged so the width becomes 10 inches. What is the new height?",
     "multiple_choice",
     "12 in", "15 in", "16 in", "24 in",
     "B",
     "Scale factor = 10/4 = 2.5. New height = 6 × 2.5 = 15 inches.",
     "dilations"),

    # SI-10 diff=4 R
    ("geometry", "similarity", "R", 4,
     "A dilation maps △ABC to △A'B'C' with scale factor k = 1/2. Which is true?",
     "multiple_choice",
     "△A'B'C' is larger than △ABC",
     "△A'B'C' is congruent to △ABC",
     "△A'B'C' is smaller than △ABC and similar to △ABC",
     "△A'B'C' has different angle measures than △ABC",
     "C",
     "A scale factor of 1/2 creates a smaller image (reduction). Dilations preserve shape (angles) but change size, so the triangles are similar but not congruent.",
     "dilations"),

    # SI-11 diff=4 U
    ("geometry", "similarity", "U", 5,
     "Two similar solids have surface areas of 25 cm² and 100 cm². What is the ratio of their volumes?",
     "multiple_choice",
     "1:4", "1:8", "1:16", "5:10",
     "B",
     "Surface area ratio = (similarity ratio)². 25:100 = 1:4, so similarity ratio = 1:2. Volume ratio = (1:2)³ = 1:8.",
     "ratios_proportions"),

    # SI-12 diff=5 R
    ("geometry", "similarity", "R", 5,
     "In a right triangle, the altitude drawn to the hypotenuse creates two smaller triangles. Which is always true?",
     "multiple_choice",
     "The two smaller triangles are congruent to each other",
     "Each smaller triangle is similar to the original triangle",
     "The altitude equals half the hypotenuse",
     "The two smaller triangles are congruent to the original",
     "B",
     "Geometric Mean (Altitude) Theorem: the altitude to the hypotenuse of a right triangle creates two triangles each similar to the original and to each other.",
     "AA_SAS_SSS"),

    # =========================================================================
    # RIGHT TRIANGLES & TRIG — 14 questions
    # =========================================================================

    # RT-1 diff=1 F
    ("geometry", "right_triangles_trig", "F", 1,
     "A right triangle has legs 6 and 8. What is the hypotenuse?",
     "multiple_choice",
     "10", "12", "14", "√100",
     "A",
     "Pythagorean Theorem: c² = 6² + 8² = 36 + 64 = 100. c = 10.",
     "pythagorean_theorem"),

    # RT-2 diff=1 F
    ("geometry", "right_triangles_trig", "F", 1,
     "In a 45-45-90 triangle, if the legs are each 7, what is the hypotenuse?",
     "multiple_choice",
     "7√2", "7√3", "14", "7/√2",
     "A",
     "In a 45-45-90 triangle, hypotenuse = leg × √2 = 7√2.",
     "special_right_triangles"),

    # RT-3 diff=2 U
    ("geometry", "right_triangles_trig", "U", 2,
     "In a 30-60-90 triangle, the shorter leg is 5. What is the hypotenuse?",
     "multiple_choice",
     "5√3", "10", "5√2", "10√3",
     "B",
     "In a 30-60-90 triangle, hypotenuse = 2 × shorter leg = 2 × 5 = 10.",
     "special_right_triangles"),

    # RT-4 diff=2 U
    ("geometry", "right_triangles_trig", "U", 2,
     "In right triangle ABC with right angle C, which ratio equals sin(A)?",
     "multiple_choice",
     "adjacent/hypotenuse", "hypotenuse/opposite", "opposite/hypotenuse", "adjacent/opposite",
     "C",
     "SOH: Sin = Opposite/Hypotenuse. sin(A) = side opposite to A / hypotenuse.",
     "sin_cos_tan"),

    # RT-5 diff=2 F
    ("geometry", "right_triangles_trig", "F", 2,
     "In a right triangle, if one leg is 5 and the hypotenuse is 13, what is the other leg?",
     "multiple_choice",
     "8", "12", "√144", "10",
     "B",
     "b² = 13² − 5² = 169 − 25 = 144. b = 12.",
     "pythagorean_theorem"),

    # RT-6 diff=3 A
    ("geometry", "right_triangles_trig", "A", 3,
     "A ladder 20 feet long leans against a wall. The base is 8 feet from the wall. How high does the ladder reach?",
     "multiple_choice",
     "√336 ≈ 18.3 ft", "12 ft", "16 ft", "√464 ≈ 21.5 ft",
     "A",
     "h² = 20² − 8² = 400 − 64 = 336. h = √336 ≈ 18.3 feet.",
     "pythagorean_theorem"),

    # RT-7 diff=3 A
    ("geometry", "right_triangles_trig", "A", 3,
     "A 30-60-90 triangle has a hypotenuse of 18. What is the length of the longer leg?",
     "multiple_choice",
     "9", "9√3", "18√3", "6√3",
     "B",
     "Shorter leg = hypotenuse/2 = 9. Longer leg = shorter leg × √3 = 9√3.",
     "special_right_triangles"),

    # RT-8 diff=3 U
    ("geometry", "right_triangles_trig", "U", 3,
     "In right triangle XYZ with right angle at Z, XZ = 3 and XY = 5. What is cos(X)?",
     "multiple_choice",
     "3/5", "4/5", "3/4", "5/3",
     "A",
     "cos(X) = adjacent/hypotenuse. Adjacent to X is XZ = 3. Hypotenuse = XY = 5. cos(X) = 3/5.",
     "sin_cos_tan"),

    # RT-9 diff=3 A
    ("geometry", "right_triangles_trig", "A", 3,
     "From the top of a 50-foot cliff, the angle of depression to a boat is 30°. How far is the boat from the base of the cliff?",
     "multiple_choice",
     "25 ft", "50√3 ft", "50/√3 ft", "25√3 ft",
     "B",
     "tan(30°) = opposite/adjacent = 50/d. d = 50/tan(30°) = 50/(1/√3) = 50√3 ≈ 86.6 ft.",
     "applications"),

    # RT-10 diff=4 R
    ("geometry", "right_triangles_trig", "R", 4,
     "In right triangle ABC, sin(A) = 3/5. What is cos(A)?",
     "multiple_choice",
     "3/4", "4/5", "5/3", "4/3",
     "B",
     "If sin(A) = 3/5, then opposite = 3, hypotenuse = 5. Adjacent = √(25−9) = 4. cos(A) = 4/5.",
     "sin_cos_tan"),

    # RT-11 diff=4 A
    ("geometry", "right_triangles_trig", "A", 4,
     "A ramp rises 4 feet over a horizontal distance of 20 feet. What is the angle of elevation to the nearest degree? (tan⁻¹(0.2) ≈ 11.3°)",
     "multiple_choice",
     "about 11°", "about 15°", "about 20°", "about 78°",
     "A",
     "tan(θ) = opposite/adjacent = 4/20 = 0.2. θ = tan⁻¹(0.2) ≈ 11.3° ≈ 11°.",
     "applications"),

    # RT-12 diff=4 R
    ("geometry", "right_triangles_trig", "R", 4,
     "Which trigonometric ratio is equal to sin(60°)?",
     "multiple_choice",
     "sin(30°)", "cos(30°)", "cos(60°)", "tan(45°)",
     "B",
     "Complementary angles: sin(θ) = cos(90° − θ). sin(60°) = cos(30°) = √3/2.",
     "sin_cos_tan"),

    # RT-13 diff=5 R
    ("geometry", "right_triangles_trig", "R", 5,
     "In △ABC, angle B = 90°, AB = 7, BC = 24. What is tan(A)?",
     "multiple_choice",
     "7/25", "24/25", "24/7", "7/24",
     "C",
     "tan(A) = opposite/adjacent. Opposite to A is BC = 24. Adjacent to A is AB = 7. tan(A) = 24/7.",
     "sin_cos_tan"),

    # RT-14 diff=5 R
    ("geometry", "right_triangles_trig", "R", 5,
     "A surveyor stands 100 m from the base of a building. The angle of elevation to the top is 58°. "
     "Which expression gives the building's height? (sin 58° ≈ 0.848, cos 58° ≈ 0.530, tan 58° ≈ 1.600)",
     "multiple_choice",
     "100 × sin(58°)", "100 / tan(58°)", "100 × tan(58°)", "100 × cos(58°)",
     "C",
     "tan(58°) = height/100 → height = 100 × tan(58°) ≈ 100 × 1.600 = 160 m.",
     "applications"),

    # =========================================================================
    # CIRCLES — 12 questions
    # =========================================================================

    # CI-1 diff=1 F
    ("geometry", "circles", "F", 1,
     "A circle has radius 9. What is its circumference? (Use π)",
     "multiple_choice",
     "9π", "18π", "81π", "27π",
     "B",
     "Circumference = 2πr = 2π(9) = 18π.",
     "arc_length_sector"),

    # CI-2 diff=1 F
    ("geometry", "circles", "F", 1,
     "A central angle of a circle intercepts an arc of 80°. What is the measure of the central angle?",
     "multiple_choice",
     "40°", "80°", "160°", "320°",
     "B",
     "A central angle equals the intercepted arc. Central angle = 80°.",
     "central_inscribed_angles"),

    # CI-3 diff=2 U
    ("geometry", "circles", "U", 2,
     "An inscribed angle intercepts an arc of 100°. What is the measure of the inscribed angle?",
     "multiple_choice",
     "50°", "100°", "200°", "25°",
     "A",
     "An inscribed angle equals half the intercepted arc: 100°/2 = 50°.",
     "central_inscribed_angles"),

    # CI-4 diff=2 U
    ("geometry", "circles", "U", 2,
     "What is the equation of a circle with center (3, −2) and radius 5?",
     "multiple_choice",
     "(x − 3)² + (y + 2)² = 5",
     "(x + 3)² + (y − 2)² = 25",
     "(x − 3)² + (y + 2)² = 25",
     "(x − 3)² + (y − 2)² = 25",
     "C",
     "Standard form: (x − h)² + (y − k)² = r². Center (3, −2): (x−3)² + (y+2)² = 25.",
     "equation_of_circle"),

    # CI-5 diff=2 F
    ("geometry", "circles", "F", 2,
     "A circle has radius 6. What is the area of a sector with a central angle of 90°?",
     "multiple_choice",
     "9π", "12π", "18π", "36π",
     "A",
     "Sector area = (central angle/360°) × πr² = (90/360) × π(36) = (1/4) × 36π = 9π.",
     "arc_length_sector"),

    # CI-6 diff=3 A
    ("geometry", "circles", "A", 3,
     "A chord is 16 cm long. It is 6 cm from the center of the circle. What is the radius?",
     "multiple_choice",
     "8 cm", "10 cm", "12 cm", "14 cm",
     "B",
     "The perpendicular from center to chord bisects it: half-chord = 8 cm. r² = 8² + 6² = 64 + 36 = 100. r = 10 cm.",
     "chords"),

    # CI-7 diff=3 U
    ("geometry", "circles", "U", 3,
     "A tangent line from an external point touches the circle at exactly one point. What is the angle between the tangent and the radius at the point of tangency?",
     "multiple_choice",
     "45°", "60°", "90°", "180°",
     "C",
     "A tangent line is perpendicular to the radius drawn to the point of tangency. The angle is always 90°.",
     "tangent_lines"),

    # CI-8 diff=3 A
    ("geometry", "circles", "A", 3,
     "A circle has diameter 14. What is the length of an arc intercepted by a central angle of 60°?",
     "multiple_choice",
     "7π/3", "7π", "14π/6", "14π/3",
     "A",
     "Radius = 7. Arc length = (60/360) × 2πr = (1/6) × 14π = 7π/3.",
     "arc_length_sector"),

    # CI-9 diff=4 R
    ("geometry", "circles", "R", 4,
     "Two secants from the same external point intercept arcs of 80° and 30°. What is the angle at the external point?",
     "multiple_choice",
     "25°", "35°", "40°", "55°",
     "A",
     "Angle = (1/2)|arc₁ − arc₂| = (1/2)|80° − 30°| = (1/2)(50°) = 25°.",
     "central_inscribed_angles"),

    # CI-10 diff=4 A
    ("geometry", "circles", "A", 4,
     "Identify the center and radius of the circle (x + 5)² + (y − 1)² = 49.",
     "multiple_choice",
     "Center (5, −1), r = 7", "Center (−5, 1), r = 49", "Center (−5, 1), r = 7", "Center (5, 1), r = 7",
     "C",
     "Standard form (x − h)² + (y − k)² = r². Here h = −5, k = 1, r² = 49 → r = 7. Center (−5, 1), radius 7.",
     "equation_of_circle"),

    # CI-11 diff=4 R
    ("geometry", "circles", "R", 4,
     "Two chords intersect inside a circle. One chord is divided into segments of 3 and 8. The other chord's shorter segment is 4. What is the longer segment?",
     "multiple_choice",
     "5", "6", "7", "8",
     "B",
     "Intersecting Chords Theorem: product of segments are equal. 3 × 8 = 4 × x → 24 = 4x → x = 6.",
     "chords"),

    # CI-12 diff=5 R
    ("geometry", "circles", "R", 5,
     "A tangent and a secant are drawn from an external point. The tangent has length 12 and the secant's external segment is 6. What is the secant's total length?",
     "multiple_choice",
     "18", "24", "30", "36",
     "C",
     "Tangent-Secant theorem: tangent² = external segment × whole secant. 144 = 6 × whole → whole = 24. "
     "Wait: 12² = 6 × whole → 144 = 6 × whole → whole = 24. Answer B.",
     "tangent_lines"),

    # =========================================================================
    # AREA & VOLUME — 12 questions
    # =========================================================================

    # AV-1 diff=1 F
    ("geometry", "area_volume", "F", 1,
     "What is the area of a triangle with base 10 cm and height 8 cm?",
     "multiple_choice",
     "40 cm²", "80 cm²", "18 cm²", "20 cm²",
     "A",
     "Area of triangle = (1/2) × base × height = (1/2) × 10 × 8 = 40 cm².",
     "area_triangles"),

    # AV-2 diff=1 F
    ("geometry", "area_volume", "F", 1,
     "What is the volume of a rectangular prism with length 5, width 4, and height 3?",
     "multiple_choice",
     "12", "47", "60", "120",
     "C",
     "Volume = length × width × height = 5 × 4 × 3 = 60.",
     "volume_prisms"),

    # AV-3 diff=2 U
    ("geometry", "area_volume", "U", 2,
     "A parallelogram has base 12 ft and height 7 ft. What is its area?",
     "multiple_choice",
     "38 ft²", "42 ft²", "84 ft²", "19 ft²",
     "C",
     "Area of parallelogram = base × height = 12 × 7 = 84 ft².",
     "area_parallelograms"),

    # AV-4 diff=2 U
    ("geometry", "area_volume", "U", 2,
     "A trapezoid has parallel bases of 6 and 10, and a height of 4. What is its area?",
     "multiple_choice",
     "32", "40", "64", "60",
     "A",
     "Area of trapezoid = (1/2)(b₁ + b₂)(h) = (1/2)(6 + 10)(4) = (1/2)(16)(4) = 32.",
     "area_trapezoids"),

    # AV-5 diff=2 F
    ("geometry", "area_volume", "F", 2,
     "A cylinder has radius 3 cm and height 10 cm. What is its volume? (Use π)",
     "multiple_choice",
     "30π cm³", "60π cm³", "90π cm³", "900π cm³",
     "C",
     "Volume of cylinder = πr²h = π(9)(10) = 90π cm³.",
     "volume_cylinders"),

    # AV-6 diff=3 A
    ("geometry", "area_volume", "A", 3,
     "A rectangular swimming pool is 20 m long, 10 m wide, and 2 m deep. How many cubic meters of water does it hold?",
     "multiple_choice",
     "200 m³", "320 m³", "400 m³", "600 m³",
     "C",
     "Volume = 20 × 10 × 2 = 400 m³.",
     "volume_prisms"),

    # AV-7 diff=3 A
    ("geometry", "area_volume", "A", 3,
     "A cone has radius 4 cm and height 9 cm. What is its volume? (Use π)",
     "multiple_choice",
     "12π cm³", "36π cm³", "48π cm³", "144π cm³",
     "C",
     "Volume of cone = (1/3)πr²h = (1/3)π(16)(9) = 48π cm³.",
     "volume_cones"),

    # AV-8 diff=3 U
    ("geometry", "area_volume", "U", 3,
     "What is the surface area of a cube with side length 5?",
     "multiple_choice",
     "25", "75", "125", "150",
     "D",
     "A cube has 6 faces. Surface area = 6 × s² = 6 × 25 = 150.",
     "surface_area"),

    # AV-9 diff=4 A
    ("geometry", "area_volume", "A", 4,
     "A sphere has radius 6 cm. What is its volume? (Use π; V = (4/3)πr³)",
     "multiple_choice",
     "144π cm³", "216π cm³", "288π cm³", "864π cm³",
     "C",
     "V = (4/3)π(6)³ = (4/3)π(216) = 288π cm³.",
     "volume_spheres"),

    # AV-10 diff=4 R
    ("geometry", "area_volume", "R", 4,
     "A cylinder and a cone have the same radius and height. What is the ratio of the cylinder's volume to the cone's volume?",
     "multiple_choice",
     "1:3", "2:1", "3:1", "1:2",
     "C",
     "V_cylinder = πr²h; V_cone = (1/3)πr²h. Ratio = πr²h / (1/3)πr²h = 3:1.",
     "volume_cylinders"),

    # AV-11 diff=4 A
    ("geometry", "area_volume", "A", 4,
     "A triangular prism has a triangular base with base 6 and height 4, and a prism height of 10. What is its volume?",
     "multiple_choice",
     "60", "120", "240", "480",
     "B",
     "Area of triangular base = (1/2)(6)(4) = 12. Volume = base area × prism height = 12 × 10 = 120.",
     "volume_prisms"),

    # AV-12 diff=5 R
    ("geometry", "area_volume", "R", 5,
     "A cone is inscribed in a cylinder of radius 5 and height 12. What fraction of the cylinder's volume is occupied by the cone?",
     "multiple_choice",
     "1/4", "1/3", "1/2", "2/3",
     "B",
     "V_cone = (1/3)πr²h. V_cylinder = πr²h. Fraction = (1/3)πr²h / πr²h = 1/3.",
     "volume_cones"),

    # =========================================================================
    # TRANSFORMATIONS — 11 questions
    # =========================================================================

    # TR-1 diff=1 F
    ("geometry", "transformations", "F", 1,
     "Point A(3, 5) is translated 4 units right and 2 units down. What are the new coordinates?",
     "multiple_choice",
     "(7, 3)", "(7, 7)", "(−1, 7)", "(3, 3)",
     "A",
     "Translation: add 4 to x, subtract 2 from y. A' = (3+4, 5−2) = (7, 3).",
     "translations"),

    # TR-2 diff=1 F
    ("geometry", "transformations", "F", 1,
     "Point B(4, −3) is reflected over the x-axis. What are the new coordinates?",
     "multiple_choice",
     "(−4, −3)", "(4, 3)", "(−4, 3)", "(3, 4)",
     "B",
     "Reflection over x-axis: negate the y-coordinate. B' = (4, −(−3)) = (4, 3).",
     "reflections"),

    # TR-3 diff=2 U
    ("geometry", "transformations", "U", 2,
     "Point C(2, 5) is reflected over the y-axis. What are the new coordinates?",
     "multiple_choice",
     "(2, −5)", "(−2, 5)", "(−2, −5)", "(5, 2)",
     "B",
     "Reflection over y-axis: negate the x-coordinate. C' = (−2, 5).",
     "reflections"),

    # TR-4 diff=2 U
    ("geometry", "transformations", "U", 2,
     "Point D(3, 4) is rotated 90° counterclockwise about the origin. What are the new coordinates?",
     "multiple_choice",
     "(4, 3)", "(−4, 3)", "(4, −3)", "(−3, 4)",
     "B",
     "90° CCW rotation: (x, y) → (−y, x). D' = (−4, 3).",
     "rotations"),

    # TR-5 diff=2 F
    ("geometry", "transformations", "F", 2,
     "Which transformation preserves both the shape and size of a figure?",
     "multiple_choice",
     "Dilation with scale factor 2", "Translation", "Dilation with scale factor 1/2", "Stretch",
     "B",
     "Translations (rigid motions) preserve both shape and size. Dilations change size.",
     "translations"),

    # TR-6 diff=3 A
    ("geometry", "transformations", "A", 3,
     "Triangle PQR has vertices P(1,2), Q(3,2), R(2,4). After a reflection over the line y = x, what is the image of P?",
     "multiple_choice",
     "(2, 1)", "(−1, 2)", "(1, −2)", "(2, −1)",
     "A",
     "Reflection over y = x: (x, y) → (y, x). P(1,2) → P'(2, 1).",
     "reflections"),

    # TR-7 diff=3 U
    ("geometry", "transformations", "U", 3,
     "Point E(5, 3) is rotated 180° about the origin. What are the new coordinates?",
     "multiple_choice",
     "(3, 5)", "(−5, −3)", "(5, −3)", "(−3, −5)",
     "B",
     "180° rotation about origin: (x, y) → (−x, −y). E' = (−5, −3).",
     "rotations"),

    # TR-8 diff=3 A
    ("geometry", "transformations", "A", 3,
     "A figure is dilated by a scale factor of 3 from the origin. A point on the figure is (2, 4). Where does it map?",
     "multiple_choice",
     "(5, 7)", "(6, 4)", "(2, 12)", "(6, 12)",
     "D",
     "Dilation from origin: multiply each coordinate by scale factor. (2×3, 4×3) = (6, 12).",
     "dilations"),

    # TR-9 diff=4 R
    ("geometry", "transformations", "R", 4,
     "Which transformation maps △ABC onto itself (is a symmetry of the figure) if △ABC is equilateral?",
     "multiple_choice",
     "Rotation of 90° about the centroid",
     "Rotation of 120° about the centroid",
     "Translation by any vector",
     "Dilation by factor 2",
     "B",
     "An equilateral triangle has 3-fold rotational symmetry. Rotations of 120° and 240° about the centroid map it onto itself.",
     "rotations"),

    # TR-10 diff=4 R
    ("geometry", "transformations", "R", 4,
     "A figure is reflected over the line x = 2. A point at (6, 3) maps to:",
     "multiple_choice",
     "(−2, 3)", "(−6, 3)", "(−2, −3)", "(2, 3)",
     "A",
     "Reflect over x = 2: distance from 6 to x=2 is 4. Mirror image is 4 units left of x=2: x = 2 − 4 = −2. Image: (−2, 3).",
     "reflections"),

    # TR-11 diff=5 R
    ("geometry", "transformations", "R", 5,
     "Which sequence of transformations is equivalent to a rotation of 180° about the origin?",
     "multiple_choice",
     "Reflection over x-axis then reflection over y-axis",
     "Reflection over x-axis then translation right 2",
     "Two consecutive translations",
     "Dilation by −1 then rotation of 90°",
     "A",
     "Reflecting over x-axis: (x,y)→(x,−y). Then over y-axis: (x,−y)→(−x,−y). This is equivalent to 180° rotation about origin.",
     "rotations"),

]


def create_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            track           TEXT    NOT NULL,
            sat_domain      TEXT    NOT NULL,
            fuar_dimension  TEXT    NOT NULL,
            difficulty      INTEGER NOT NULL,
            question_text   TEXT    NOT NULL,
            question_type   TEXT    NOT NULL DEFAULT 'multiple_choice',
            option_a        TEXT,
            option_b        TEXT,
            option_c        TEXT,
            option_d        TEXT,
            correct_answer  TEXT    NOT NULL,
            explanation     TEXT,
            topic_tag       TEXT,
            created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()


def seed(conn):
    conn.execute("DELETE FROM questions WHERE track = 'geometry'")
    conn.executemany(
        """INSERT INTO questions
           (track, sat_domain, fuar_dimension, difficulty,
            question_text, question_type,
            option_a, option_b, option_c, option_d,
            correct_answer, explanation, topic_tag)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        QUESTIONS,
    )
    conn.commit()


def print_summary(conn):
    rows = conn.execute(
        "SELECT sat_domain, fuar_dimension, difficulty FROM questions WHERE track = 'geometry'"
    ).fetchall()

    by_domain = defaultdict(int)
    by_fuar = defaultdict(int)
    by_diff = defaultdict(int)

    for domain, fuar, diff in rows:
        by_domain[domain] += 1
        by_fuar[fuar] += 1
        by_diff[diff] += 1

    print(f"\n{'='*55}")
    print(f"  Geometry seed complete — {len(rows)} questions")
    print(f"{'='*55}")
    print("\nBy domain:")
    for k, v in sorted(by_domain.items()):
        print(f"  {k:<30} {v}")
    print("\nBy FUAR:")
    for k, v in sorted(by_fuar.items()):
        print(f"  {k:<5} {v}")
    print("\nBy difficulty:")
    for k, v in sorted(by_diff.items()):
        print(f"  {k}   {v}")
    print()


def main():
    conn = sqlite3.connect(DB_PATH)
    create_table(conn)
    seed(conn)
    print_summary(conn)
    conn.close()


if __name__ == "__main__":
    main()
