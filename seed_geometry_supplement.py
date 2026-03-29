"""Supplemental Geometry questions to reach 3x test variety."""
import sqlite3, os
DB_PATH = os.environ.get('DATABASE_PATH', 'college_ready.db')

QUESTIONS = [
    # (track, sat_domain, fuar_dimension, difficulty, question_text, question_type,
    #  option_a, option_b, option_c, option_d, correct_answer, explanation, topic_tag)

    # =========================================================================
    # TRIANGLES — 18 questions
    # =========================================================================

    # diff=1 F
    ("geometry", "triangles", "F", 1,
     "What is the sum of the interior angles of any triangle?",
     "multiple_choice",
     "90 degrees", "180 degrees", "270 degrees", "360 degrees",
     "B",
     "The interior angles of every triangle sum to 180 degrees.",
     "angle_relationships"),

    # diff=1 F
    ("geometry", "triangles", "F", 1,
     "A right triangle has legs of length 3 and 4. What is the length of the hypotenuse?",
     "multiple_choice",
     "5", "6", "7", "8",
     "A",
     "Pythagorean theorem: 3^2 + 4^2 = 9 + 16 = 25. Hypotenuse = sqrt(25) = 5.",
     "pythagorean_theorem"),

    # diff=2 F
    ("geometry", "triangles", "F", 2,
     "In a triangle, two angles measure 55 degrees and 75 degrees. What is the third angle?",
     "multiple_choice",
     "40 degrees", "45 degrees", "50 degrees", "60 degrees",
     "C",
     "Third angle = 180 - 55 - 75 = 50 degrees.",
     "angle_relationships"),

    # diff=2 F
    ("geometry", "triangles", "F", 2,
     "A right triangle has one leg of 8 and hypotenuse of 10. What is the other leg?",
     "multiple_choice",
     "4", "5", "6", "7",
     "C",
     "a^2 + 8^2 = 10^2. a^2 = 100 - 64 = 36. a = 6.",
     "pythagorean_theorem"),

    # diff=2 U
    ("geometry", "triangles", "U", 2,
     "Two triangles are congruent by SAS. Which information is sufficient to prove this?",
     "multiple_choice",
     "Two pairs of equal angles", "Two pairs of equal sides only", "Two pairs of equal sides with the included angle equal", "Three pairs of equal sides",
     "C",
     "SAS (Side-Angle-Side) requires two pairs of equal sides AND the angle between those sides to be equal.",
     "congruence"),

    # diff=2 U
    ("geometry", "triangles", "U", 2,
     "An isosceles triangle has two equal angles of 65 degrees each. What is the third angle?",
     "multiple_choice",
     "40 degrees", "45 degrees", "50 degrees", "55 degrees",
     "C",
     "Third angle = 180 - 65 - 65 = 50 degrees.",
     "angle_relationships"),

    # diff=3 F
    ("geometry", "triangles", "F", 3,
     "What are the side lengths of a 45-45-90 triangle with hypotenuse 10?",
     "multiple_choice",
     "5 and 5", "5sqrt(2) and 5sqrt(2)", "5 and 5sqrt(3)", "10 and 10",
     "B",
     "In a 45-45-90 triangle, legs = hypotenuse / sqrt(2) = 10 / sqrt(2) = 5sqrt(2).",
     "special_right_triangles"),

    # diff=3 F
    ("geometry", "triangles", "F", 3,
     "In a 30-60-90 triangle, the shorter leg is 6. What is the length of the hypotenuse?",
     "multiple_choice",
     "6sqrt(2)", "6sqrt(3)", "12", "18",
     "C",
     "In a 30-60-90 triangle, hypotenuse = 2 x shorter leg = 2 x 6 = 12.",
     "special_right_triangles"),

    # diff=3 U
    ("geometry", "triangles", "U", 3,
     "Triangle ABC is similar to triangle DEF with a scale factor of 3. If AB = 4, what is DE?",
     "multiple_choice",
     "4", "7", "12", "16",
     "C",
     "Scale factor 3 means DE = 3 x AB = 3 x 4 = 12.",
     "similarity"),

    # diff=3 A
    ("geometry", "triangles", "A", 3,
     "A ladder 13 feet long leans against a wall. The base is 5 feet from the wall. How high does it reach?",
     "multiple_choice",
     "10 ft", "11 ft", "12 ft", "13 ft",
     "C",
     "h^2 + 5^2 = 13^2. h^2 = 169 - 25 = 144. h = 12 ft.",
     "pythagorean_theorem"),

    # diff=3 A
    ("geometry", "triangles", "A", 3,
     "A triangle has a base of 10 cm and height of 7 cm. What is its area?",
     "multiple_choice",
     "17 sq cm", "35 sq cm", "70 sq cm", "140 sq cm",
     "B",
     "Area = (1/2) x base x height = (1/2)(10)(7) = 35 sq cm.",
     "area_triangle"),

    # diff=3 R
    ("geometry", "triangles", "R", 3,
     "An exterior angle of a triangle is 125 degrees. One non-adjacent interior angle is 70 degrees. What is the other non-adjacent interior angle?",
     "multiple_choice",
     "45 degrees", "50 degrees", "55 degrees", "60 degrees",
     "C",
     "Exterior angle theorem: exterior angle = sum of the two non-adjacent interior angles. 125 = 70 + x. x = 55 degrees.",
     "angle_relationships"),

    # diff=4 U
    ("geometry", "triangles", "U", 4,
     "Two triangles have all three pairs of angles equal. Must they be congruent?",
     "multiple_choice",
     "Yes, by SSS", "Yes, by AAA", "No, they are only similar", "No, unless the perimeters are equal",
     "C",
     "AAA (three equal angles) proves similarity, not congruence. The triangles have the same shape but may be different sizes.",
     "similarity"),

    # diff=4 A
    ("geometry", "triangles", "A", 4,
     "A 30-60-90 triangle has hypotenuse 16. What is the length of the longer leg?",
     "multiple_choice",
     "8", "8sqrt(2)", "8sqrt(3)", "16sqrt(3)",
     "C",
     "Shorter leg = 16/2 = 8. Longer leg = shorter leg x sqrt(3) = 8sqrt(3).",
     "special_right_triangles"),

    # diff=4 R
    ("geometry", "triangles", "R", 4,
     "Triangle ABC ~ Triangle DEF with AB/DE = 2/3. If the area of ABC is 12 sq units, what is the area of DEF?",
     "multiple_choice",
     "18 sq units", "24 sq units", "27 sq units", "36 sq units",
     "C",
     "Area ratio = (scale factor)^2 = (2/3)^2 = 4/9. Area of DEF = 12 x (9/4) = 27 sq units.",
     "similarity"),

    # diff=4 R
    ("geometry", "triangles", "R", 4,
     "In right triangle PQR with right angle at R, tan(P) = 3/4. If PQ = 20, what is QR?",
     "multiple_choice",
     "9", "12", "15", "16",
     "B",
     "tan(P) = opposite/adjacent = QR/PR = 3/4. This is a 3-4-5 scaled by 4: PR = 16, QR = 12, PQ = 20.",
     "pythagorean_theorem"),

    # diff=5 R
    ("geometry", "triangles", "R", 5,
     "The medians of a triangle meet at the centroid, which divides each median in a 2:1 ratio. If a median is 18 cm long, how far is the centroid from the vertex?",
     "multiple_choice",
     "6 cm", "9 cm", "12 cm", "15 cm",
     "C",
     "The centroid divides the median 2:1 from vertex. Distance from vertex = (2/3) x 18 = 12 cm.",
     "triangle_centers"),

    # diff=5 R
    ("geometry", "triangles", "R", 5,
     "Triangle XYZ has sides 7, 24, and 25. Is it a right triangle? Which angle, if any, is 90 degrees?",
     "multiple_choice",
     "No, it is not a right triangle", "Yes, the angle opposite the side of 7", "Yes, the angle opposite the side of 24", "Yes, the angle opposite the side of 25",
     "D",
     "Check: 7^2 + 24^2 = 49 + 576 = 625 = 25^2. Yes, it is a right triangle. The right angle is opposite the hypotenuse (side 25).",
     "pythagorean_theorem"),

    # =========================================================================
    # CIRCLES — 15 questions
    # =========================================================================

    # diff=1 F
    ("geometry", "circles", "F", 1,
     "What is the circumference of a circle with radius 7? (Use pi = 3.14)",
     "multiple_choice",
     "21.98", "43.96", "153.86", "176.0",
     "B",
     "C = 2*pi*r = 2 x 3.14 x 7 = 43.96.",
     "circle_basics"),

    # diff=2 F
    ("geometry", "circles", "F", 2,
     "What is the area of a circle with diameter 10? (Leave answer in terms of pi.)",
     "multiple_choice",
     "10pi", "20pi", "25pi", "100pi",
     "C",
     "Radius = 10/2 = 5. Area = pi*r^2 = pi(5)^2 = 25pi.",
     "circle_basics"),

    # diff=2 U
    ("geometry", "circles", "U", 2,
     "A central angle of 90 degrees intercepts an arc in a circle with radius 8. What is the arc length? (Leave in terms of pi.)",
     "multiple_choice",
     "2pi", "4pi", "8pi", "16pi",
     "B",
     "Arc length = (theta/360) x 2*pi*r = (90/360) x 2*pi*8 = (1/4)(16pi) = 4pi.",
     "arc_length"),

    # diff=2 U
    ("geometry", "circles", "U", 2,
     "An inscribed angle intercepts an arc of 80 degrees. What is the measure of the inscribed angle?",
     "multiple_choice",
     "20 degrees", "40 degrees", "80 degrees", "160 degrees",
     "B",
     "An inscribed angle equals half the intercepted arc: 80/2 = 40 degrees.",
     "inscribed_angles"),

    # diff=3 F
    ("geometry", "circles", "F", 3,
     "A sector has a central angle of 60 degrees in a circle with radius 6. What is the sector area? (Leave in terms of pi.)",
     "multiple_choice",
     "3pi", "6pi", "9pi", "12pi",
     "B",
     "Sector area = (60/360) x pi*r^2 = (1/6)(36pi) = 6pi.",
     "sector_area"),

    # diff=3 U
    ("geometry", "circles", "U", 3,
     "A tangent line to a circle meets the radius at the point of tangency. What angle do they form?",
     "multiple_choice",
     "45 degrees", "60 degrees", "90 degrees", "180 degrees",
     "C",
     "A tangent line is always perpendicular to the radius at the point of tangency, forming a 90-degree angle.",
     "tangent_lines"),

    # diff=3 U
    ("geometry", "circles", "U", 3,
     "Two chords in a circle intersect inside. One chord is divided into segments of 4 and 6. The other chord has one segment of 3. What is the other segment?",
     "multiple_choice",
     "6", "7", "8", "9",
     "C",
     "Intersecting chords theorem: product of segments are equal. 4 x 6 = 3 x x. 24 = 3x. x = 8.",
     "circle_theorems"),

    # diff=3 A
    ("geometry", "circles", "A", 3,
     "A circular track has a diameter of 400 meters. How far does a runner travel in one complete lap? (Round to nearest meter, pi = 3.14159)",
     "multiple_choice",
     "1,257 m", "1,047 m", "628 m", "1,414 m",
     "A",
     "Circumference = pi x d = 3.14159 x 400 = 1256.6 m, approximately 1,257 m.",
     "circle_basics"),

    # diff=3 A
    ("geometry", "circles", "A", 3,
     "A pizza has a diameter of 16 inches. It is cut into 8 equal slices. What is the area of one slice? (Leave in terms of pi.)",
     "multiple_choice",
     "2pi sq in", "4pi sq in", "8pi sq in", "16pi sq in",
     "C",
     "Total area = pi(8)^2 = 64pi. One slice = 64pi / 8 = 8pi sq in.",
     "sector_area"),

    # diff=3 R
    ("geometry", "circles", "R", 3,
     "An inscribed angle is 35 degrees. What is the measure of the central angle that intercepts the same arc?",
     "multiple_choice",
     "17.5 degrees", "35 degrees", "70 degrees", "140 degrees",
     "C",
     "The central angle equals twice the inscribed angle: 2 x 35 = 70 degrees.",
     "inscribed_angles"),

    # diff=4 U
    ("geometry", "circles", "U", 4,
     "A tangent segment from an external point to a circle has length 12. The external point is 13 units from the center. What is the radius?",
     "multiple_choice",
     "4", "5", "6", "7",
     "B",
     "Tangent-radius relationship (right angle): r^2 + 12^2 = 13^2. r^2 = 169 - 144 = 25. r = 5.",
     "tangent_lines"),

    # diff=4 A
    ("geometry", "circles", "A", 4,
     "A circular garden has radius 10 m. A path of width 2 m is built around it. What is the area of the path? (Leave in terms of pi.)",
     "multiple_choice",
     "24pi sq m", "44pi sq m", "100pi sq m", "144pi sq m",
     "B",
     "Outer radius = 12. Outer area = 144pi. Inner area = 100pi. Path = 144pi - 100pi = 44pi sq m.",
     "circle_basics"),

    # diff=4 R
    ("geometry", "circles", "R", 4,
     "In a circle, a diameter bisects a chord. The chord is 16 cm and the diameter passes through its midpoint perpendicularly. If the radius is 10 cm, how far is the center from the chord?",
     "multiple_choice",
     "4 cm", "5 cm", "6 cm", "8 cm",
     "C",
     "Half the chord = 8. Distance from center: d^2 + 8^2 = 10^2. d^2 = 100 - 64 = 36. d = 6 cm.",
     "circle_theorems"),

    # diff=5 R
    ("geometry", "circles", "R", 5,
     "Two secants are drawn from an external point. One secant intercepts arcs of 80 degrees and 40 degrees (near and far). What is the measure of the angle at the external point?",
     "multiple_choice",
     "20 degrees", "30 degrees", "40 degrees", "60 degrees",
     "A",
     "Angle formed by two secants = (1/2)|far arc - near arc| = (1/2)|80 - 40| = 20 degrees.",
     "circle_theorems"),

    # diff=5 R
    ("geometry", "circles", "R", 5,
     "A chord 12 cm long is 8 cm from the center of a circle. What is the radius of the circle?",
     "multiple_choice",
     "8 cm", "10 cm", "12 cm", "14 cm",
     "B",
     "The perpendicular from center bisects the chord: half-chord = 6. r^2 = 6^2 + 8^2 = 36 + 64 = 100. r = 10 cm.",
     "circle_theorems"),

    # =========================================================================
    # TRANSFORMATIONS — 12 questions
    # =========================================================================

    # diff=1 F
    ("geometry", "transformations", "F", 1,
     "A point at (3, 5) is translated 4 units right and 2 units down. What are the new coordinates?",
     "multiple_choice",
     "(7, 3)", "(7, 7)", "(-1, 3)", "(3, 7)",
     "A",
     "Translate: (3+4, 5-2) = (7, 3).",
     "translations"),

    # diff=1 F
    ("geometry", "transformations", "F", 1,
     "A figure is reflected over the x-axis. The original point is (4, -3). What is its image?",
     "multiple_choice",
     "(-4, 3)", "(4, 3)", "(-4, -3)", "(3, 4)",
     "B",
     "Reflection over x-axis: (x, y) -> (x, -y). Image: (4, -(-3)) = (4, 3).",
     "reflections"),

    # diff=2 F
    ("geometry", "transformations", "F", 2,
     "Point P(2, 3) is rotated 90 degrees counterclockwise about the origin. What are the new coordinates?",
     "multiple_choice",
     "(-3, 2)", "(3, -2)", "(-2, -3)", "(3, 2)",
     "A",
     "90 degrees CCW rotation: (x, y) -> (-y, x). P(2, 3) -> (-3, 2).",
     "rotations"),

    # diff=2 U
    ("geometry", "transformations", "U", 2,
     "A shape is reflected over the y-axis. Original point is (-5, 2). What is the image?",
     "multiple_choice",
     "(5, 2)", "(-5, -2)", "(5, -2)", "(-5, 2)",
     "A",
     "Reflection over y-axis: (x, y) -> (-x, y). Image: (-(-5), 2) = (5, 2).",
     "reflections"),

    # diff=2 U
    ("geometry", "transformations", "U", 2,
     "Which transformation preserves both shape and size of a figure?",
     "multiple_choice",
     "Dilation by factor 2", "Reflection", "Stretch", "Shear",
     "B",
     "Reflections are rigid motions (isometries) that preserve both shape and size.",
     "transformation_properties"),

    # diff=3 F
    ("geometry", "transformations", "F", 3,
     "A point at (1, -4) is rotated 180 degrees about the origin. What is the image?",
     "multiple_choice",
     "(-4, -1)", "(-1, 4)", "(4, 1)", "(1, 4)",
     "B",
     "180-degree rotation: (x, y) -> (-x, -y). Image: (-1, 4).",
     "rotations"),

    # diff=3 U
    ("geometry", "transformations", "U", 3,
     "Triangle A is mapped onto Triangle B by a dilation with scale factor 1/2. Triangle B has side 6. What is the corresponding side in Triangle A?",
     "multiple_choice",
     "3", "6", "9", "12",
     "D",
     "Scale factor 1/2 means B sides = (1/2) x A sides. So A side = 6 / (1/2) = 12.",
     "dilations"),

    # diff=3 A
    ("geometry", "transformations", "A", 3,
     "A logo at the origin is enlarged by a scale factor of 3. A point at (2, -1) maps to which image point?",
     "multiple_choice",
     "(5, 2)", "(6, -3)", "(3, -3)", "(2, -3)",
     "B",
     "Dilation from origin by factor 3: (x, y) -> (3x, 3y). Image: (6, -3).",
     "dilations"),

    # diff=3 A
    ("geometry", "transformations", "A", 3,
     "Segment AB has endpoints A(1, 2) and B(5, 6). After a translation of (x-3, y+1), where is A'?",
     "multiple_choice",
     "(-2, 3)", "(4, 1)", "(-2, 1)", "(4, 3)",
     "A",
     "A(1, 2) translated by (-3, +1): (1-3, 2+1) = (-2, 3).",
     "translations"),

    # diff=3 R
    ("geometry", "transformations", "R", 3,
     "Triangle PQR is reflected over the line y = x. What is the image of point P(4, 1)?",
     "multiple_choice",
     "(1, 4)", "(4, -1)", "(-1, 4)", "(-4, 1)",
     "A",
     "Reflection over y = x: (x, y) -> (y, x). P(4, 1) -> (1, 4).",
     "reflections"),

    # diff=4 R
    ("geometry", "transformations", "R", 4,
     "A composition of two reflections over parallel lines that are 5 units apart is equivalent to which single transformation?",
     "multiple_choice",
     "A rotation of 90 degrees", "A translation of 10 units", "A reflection", "A dilation by 2",
     "B",
     "Reflection over two parallel lines equals a translation of twice the distance between them: 2 x 5 = 10 units.",
     "transformation_properties"),

    # diff=5 R
    ("geometry", "transformations", "R", 5,
     "Point A(3, -2) is rotated 270 degrees counterclockwise about the origin. What is its image?",
     "multiple_choice",
     "(2, 3)", "(-2, -3)", "(-3, 2)", "(2, -3)",
     "B",
     "270 degrees CCW equals 90 degrees CW. Rule for 90 CW: (x, y) -> (y, -x). A(3, -2) -> (-2, -(3)) = (-2, -3).",
     "rotations"),

    # =========================================================================
    # AREA & VOLUME — 15 questions
    # =========================================================================

    # diff=1 F
    ("geometry", "area_volume", "F", 1,
     "What is the area of a rectangle with length 9 and width 5?",
     "multiple_choice",
     "28", "35", "40", "45",
     "D",
     "Area = length x width = 9 x 5 = 45.",
     "area_polygons"),

    # diff=1 F
    ("geometry", "area_volume", "F", 1,
     "What is the volume of a rectangular box with length 4, width 3, and height 6?",
     "multiple_choice",
     "36", "48", "72", "84",
     "C",
     "Volume = l x w x h = 4 x 3 x 6 = 72.",
     "volume"),

    # diff=2 F
    ("geometry", "area_volume", "F", 2,
     "A parallelogram has base 12 and height 5. What is its area?",
     "multiple_choice",
     "30", "34", "60", "120",
     "C",
     "Area of parallelogram = base x height = 12 x 5 = 60.",
     "area_polygons"),

    # diff=2 F
    ("geometry", "area_volume", "F", 2,
     "A cylinder has radius 3 and height 10. What is its volume? (Leave in terms of pi.)",
     "multiple_choice",
     "30pi", "60pi", "90pi", "120pi",
     "C",
     "Volume = pi*r^2*h = pi(9)(10) = 90pi.",
     "volume"),

    # diff=2 U
    ("geometry", "area_volume", "U", 2,
     "A trapezoid has parallel sides of 8 and 14 and a height of 5. What is its area?",
     "multiple_choice",
     "55", "85", "110", "140",
     "A",
     "Area = (1/2)(b1 + b2)(h) = (1/2)(8 + 14)(5) = (1/2)(22)(5) = 55.",
     "area_polygons"),

    # diff=3 F
    ("geometry", "area_volume", "F", 3,
     "A cone has radius 4 and height 9. What is its volume? (Leave in terms of pi.)",
     "multiple_choice",
     "12pi", "36pi", "48pi", "144pi",
     "C",
     "Volume = (1/3)*pi*r^2*h = (1/3)*pi(16)(9) = 48pi.",
     "volume"),

    # diff=3 U
    ("geometry", "area_volume", "U", 3,
     "A sphere has radius 6. What is its surface area? (Leave in terms of pi.)",
     "multiple_choice",
     "36pi", "72pi", "144pi", "288pi",
     "C",
     "Surface area of sphere = 4*pi*r^2 = 4*pi*(36) = 144pi.",
     "surface_area"),

    # diff=3 A
    ("geometry", "area_volume", "A", 3,
     "A room is 15 ft long, 12 ft wide, and 9 ft tall. What is the total surface area of the four walls (no ceiling or floor)?",
     "multiple_choice",
     "378 sq ft", "486 sq ft", "540 sq ft", "648 sq ft",
     "B",
     "Two walls 15x9: 2 x 135 = 270. Two walls 12x9: 2 x 108 = 216. Total = 270 + 216 = 486 sq ft.",
     "surface_area"),

    # diff=3 A
    ("geometry", "area_volume", "A", 3,
     "A swimming pool is 25 m long, 10 m wide, and 2 m deep. How many cubic meters of water does it hold?",
     "multiple_choice",
     "250", "375", "500", "750",
     "C",
     "Volume = 25 x 10 x 2 = 500 cubic meters.",
     "volume"),

    # diff=3 R
    ("geometry", "area_volume", "R", 3,
     "If all sides of a square are doubled, by what factor does the area increase?",
     "multiple_choice",
     "2", "4", "6", "8",
     "B",
     "Original area: s^2. New area: (2s)^2 = 4s^2. Area increases by a factor of 4.",
     "area_polygons"),

    # diff=4 A
    ("geometry", "area_volume", "A", 4,
     "A pyramid has a rectangular base 6 m by 4 m and height 9 m. What is its volume?",
     "multiple_choice",
     "36 cu m", "54 cu m", "72 cu m", "108 cu m",
     "C",
     "Volume = (1/3) x base area x height = (1/3)(6 x 4)(9) = (1/3)(24)(9) = 72 cu m.",
     "volume"),

    # diff=4 U
    ("geometry", "area_volume", "U", 4,
     "A sphere's radius is tripled. By what factor does its volume increase?",
     "multiple_choice",
     "3", "6", "9", "27",
     "D",
     "Volume of sphere = (4/3)*pi*r^3. New volume with 3r: (4/3)*pi*(3r)^3 = 27*(4/3)*pi*r^3. Factor = 27.",
     "volume"),

    # diff=4 R
    ("geometry", "area_volume", "R", 4,
     "A composite figure is made of a rectangle 8 x 5 with a semicircle of diameter 8 on top. What is the total area? (Leave in terms of pi.)",
     "multiple_choice",
     "40 + 8pi", "40 + 16pi", "40 + 32pi", "40 + 4pi",
     "A",
     "Rectangle: 8 x 5 = 40. Semicircle radius = 4: area = (1/2)*pi*(4)^2 = 8pi. Total = 40 + 8pi.",
     "area_polygons"),

    # diff=5 R
    ("geometry", "area_volume", "R", 5,
     "A cylinder has the same radius and height h. When h is doubled and r is halved, how does the volume change?",
     "multiple_choice",
     "Doubles", "Stays the same", "Decreases by half", "Decreases to 1/4",
     "C",
     "Original: pi*r^2*h. New: pi*(r/2)^2*(2h) = pi*(r^2/4)*(2h) = (1/2)*pi*r^2*h. Volume is halved.",
     "volume"),

    # diff=5 A
    ("geometry", "area_volume", "A", 5,
     "A metal sphere of radius 3 cm is melted and recast as a cylinder with radius 3 cm. What is the height of the cylinder? (Leave answer in simplest form.)",
     "multiple_choice",
     "2 cm", "3 cm", "4 cm", "6 cm",
     "C",
     "Sphere volume: (4/3)*pi*(3)^3 = 36pi. Cylinder: pi*(3)^2*h = 9*pi*h = 36pi. h = 4 cm.",
     "volume"),

    # =========================================================================
    # COORDINATE GEOMETRY — 15 questions
    # =========================================================================

    # diff=1 F
    ("geometry", "coordinate", "F", 1,
     "What is the distance between points (0, 0) and (6, 8)?",
     "multiple_choice",
     "8", "10", "12", "14",
     "B",
     "Distance = sqrt((6-0)^2 + (8-0)^2) = sqrt(36 + 64) = sqrt(100) = 10.",
     "distance_midpoint"),

    # diff=1 F
    ("geometry", "coordinate", "F", 1,
     "What is the midpoint of the segment joining (2, 4) and (8, 10)?",
     "multiple_choice",
     "(4, 6)", "(5, 7)", "(6, 7)", "(5, 6)",
     "B",
     "Midpoint = ((2+8)/2, (4+10)/2) = (5, 7).",
     "distance_midpoint"),

    # diff=2 F
    ("geometry", "coordinate", "F", 2,
     "Find the distance between (-3, 1) and (1, 4).",
     "multiple_choice",
     "3", "4", "5", "6",
     "C",
     "Distance = sqrt((1-(-3))^2 + (4-1)^2) = sqrt(16 + 9) = sqrt(25) = 5.",
     "distance_midpoint"),

    # diff=2 U
    ("geometry", "coordinate", "U", 2,
     "A rectangle has vertices at (0,0), (5,0), (5,3), and (0,3). What is its perimeter?",
     "multiple_choice",
     "8", "15", "16", "30",
     "C",
     "Length = 5, width = 3. Perimeter = 2(5 + 3) = 16.",
     "coordinate_polygons"),

    # diff=2 U
    ("geometry", "coordinate", "U", 2,
     "Point M(4, 5) is the midpoint of segment AB. A has coordinates (1, 2). What are B's coordinates?",
     "multiple_choice",
     "(7, 8)", "(5, 6)", "(3, 4)", "(6, 7)",
     "A",
     "Midpoint formula: ((1+Bx)/2, (2+By)/2) = (4, 5). Bx = 7, By = 8. B = (7, 8).",
     "distance_midpoint"),

    # diff=3 F
    ("geometry", "coordinate", "F", 3,
     "What is the slope of the line segment from (-2, 3) to (4, -1)?",
     "multiple_choice",
     "-2/3", "2/3", "-3/2", "3/2",
     "A",
     "Slope = (-1-3)/(4-(-2)) = -4/6 = -2/3.",
     "coordinate_polygons"),

    # diff=3 U
    ("geometry", "coordinate", "U", 3,
     "A right angle in a coordinate figure is confirmed when two line segments are perpendicular. Segment 1 has slope 2/3. What slope does segment 2 need?",
     "multiple_choice",
     "2/3", "-2/3", "3/2", "-3/2",
     "D",
     "Perpendicular slopes are negative reciprocals: -1/(2/3) = -3/2.",
     "coordinate_polygons"),

    # diff=3 A
    ("geometry", "coordinate", "A", 3,
     "A circle has center (3, -1) and passes through (7, -1). What is its equation?",
     "multiple_choice",
     "(x-3)^2 + (y+1)^2 = 4", "(x-3)^2 + (y+1)^2 = 16", "(x+3)^2 + (y-1)^2 = 16", "(x-3)^2 + (y-1)^2 = 16",
     "B",
     "Radius = distance from center to point = |7 - 3| = 4. Equation: (x-3)^2 + (y+1)^2 = 16.",
     "coordinate_circles"),

    # diff=3 A
    ("geometry", "coordinate", "A", 3,
     "Three vertices of a parallelogram are (0,0), (4,0), and (5,3). What is the fourth vertex?",
     "multiple_choice",
     "(1, 3)", "(5, 0)", "(3, 4)", "(9, 3)",
     "A",
     "For a parallelogram, opposite sides are parallel and equal. Fourth vertex = (0+5-4, 0+3-0) = (1, 3).",
     "coordinate_polygons"),

    # diff=3 R
    ("geometry", "coordinate", "R", 3,
     "Is the triangle with vertices A(0,0), B(4,0), and C(2,4) isosceles?",
     "multiple_choice",
     "No, all sides are different lengths", "Yes, AB = BC", "Yes, AC = BC", "Yes, AB = AC",
     "C",
     "AB = 4. AC = sqrt(4+16) = sqrt(20). BC = sqrt(4+16) = sqrt(20). Since AC = BC, the triangle is isosceles.",
     "coordinate_polygons"),

    # diff=4 A
    ("geometry", "coordinate", "A", 4,
     "Find the area of the triangle with vertices (0,0), (6,0), and (4,5).",
     "multiple_choice",
     "12", "15", "20", "25",
     "B",
     "Area = (1/2)|base x height| = (1/2)(6)(5) = 15. (Base along x-axis = 6, height = 5.)",
     "coordinate_polygons"),

    # diff=4 U
    ("geometry", "coordinate", "U", 4,
     "A square has vertices at (1,1), (4,1), (4,4), and (1,4). What is the equation of its diagonal from (1,1) to (4,4)?",
     "multiple_choice",
     "y = x + 1", "y = x", "y = x - 1", "y = 2x - 1",
     "B",
     "Slope = (4-1)/(4-1) = 1. Through (1,1): y - 1 = 1(x - 1), y = x.",
     "coordinate_polygons"),

    # diff=4 R
    ("geometry", "coordinate", "R", 4,
     "The center of a circle is (2, 3) and its radius is 5. Which point does NOT lie on the circle?",
     "multiple_choice",
     "(2, 8)", "(7, 3)", "(2, -2)", "(4, 7)",
     "D",
     "Check each point using (x-2)^2+(y-3)^2=25. (2,8): 0+25=25 yes. (7,3): 25+0=25 yes. (2,-2): 0+25=25 yes. (4,7): (2)^2+(4)^2=4+16=20, not 25. So (4,7) does NOT lie on the circle.",
     "coordinate_circles"),

    # diff=5 R
    ("geometry", "coordinate", "R", 5,
     "A circle has equation x^2 + y^2 - 6x + 4y - 12 = 0. What are the center and radius?",
     "multiple_choice",
     "Center (3, -2), radius 5", "Center (-3, 2), radius 5", "Center (3, -2), radius 25", "Center (6, -4), radius 5",
     "A",
     "Complete the square: (x^2-6x+9) + (y^2+4y+4) = 12+9+4 = 25. (x-3)^2 + (y+2)^2 = 25. Center (3,-2), radius 5.",
     "coordinate_circles"),

    # diff=5 R
    ("geometry", "coordinate", "R", 5,
     "What is the perimeter of the quadrilateral with vertices A(0,0), B(4,3), C(8,0), and D(4,-3)?",
     "multiple_choice",
     "16", "18", "20", "24",
     "C",
     "AB = sqrt(16+9)=5. BC = sqrt(16+9)=5. CD = sqrt(16+9)=5. DA = sqrt(16+9)=5. Perimeter = 20.",
     "distance_midpoint"),

    # =========================================================================
    # PROOFS & ANGLE RELATIONSHIPS — 15 questions
    # =========================================================================

    # diff=1 F
    ("geometry", "proofs", "F", 1,
     "Two lines intersect. One angle is 40 degrees. What is the measure of its vertical angle?",
     "multiple_choice",
     "40 degrees", "50 degrees", "140 degrees", "180 degrees",
     "A",
     "Vertical angles are congruent. The vertical angle also measures 40 degrees.",
     "angle_relationships"),

    # diff=1 F
    ("geometry", "proofs", "F", 1,
     "Two supplementary angles have measures x and 2x. What is x?",
     "multiple_choice",
     "30 degrees", "45 degrees", "60 degrees", "90 degrees",
     "C",
     "Supplementary angles sum to 180 degrees: x + 2x = 180. 3x = 180. x = 60 degrees.",
     "angle_relationships"),

    # diff=2 F
    ("geometry", "proofs", "F", 2,
     "A transversal crosses two parallel lines. One alternate interior angle is 65 degrees. What is the other alternate interior angle?",
     "multiple_choice",
     "25 degrees", "65 degrees", "115 degrees", "130 degrees",
     "B",
     "Alternate interior angles are congruent when lines are parallel. Both measure 65 degrees.",
     "parallel_lines"),

    # diff=2 U
    ("geometry", "proofs", "U", 2,
     "Two angles are complementary. One angle is 3 times the other. What is the larger angle?",
     "multiple_choice",
     "22.5 degrees", "45 degrees", "60 degrees", "67.5 degrees",
     "D",
     "Complementary: x + 3x = 90. 4x = 90. x = 22.5. Larger angle = 3(22.5) = 67.5 degrees.",
     "angle_relationships"),

    # diff=2 U
    ("geometry", "proofs", "U", 2,
     "A transversal cuts two parallel lines. A co-interior (same-side interior) angle is 110 degrees. What is the other co-interior angle?",
     "multiple_choice",
     "55 degrees", "70 degrees", "80 degrees", "110 degrees",
     "B",
     "Co-interior (same-side interior) angles are supplementary: 110 + x = 180. x = 70 degrees.",
     "parallel_lines"),

    # diff=3 F
    ("geometry", "proofs", "F", 3,
     "The exterior angle of a triangle measures 130 degrees. One non-adjacent interior angle is 80 degrees. What is the other?",
     "multiple_choice",
     "40 degrees", "50 degrees", "60 degrees", "70 degrees",
     "B",
     "Exterior angle = sum of non-adjacent interior angles: 130 = 80 + x. x = 50 degrees.",
     "angle_relationships"),

    # diff=3 U
    ("geometry", "proofs", "U", 3,
     "In the proof that base angles of an isosceles triangle are equal, which congruence theorem is used when you draw the median?",
     "multiple_choice",
     "SSS", "ASA", "AAS", "SAS",
     "A",
     "Drawing the median creates two triangles sharing the median side. With two equal legs and the shared median, SSS applies.",
     "congruence_proofs"),

    # diff=3 A
    ("geometry", "proofs", "A", 3,
     "Two parallel lines are cut by a transversal. Corresponding angles are (3x + 10) degrees and (5x - 30) degrees. Find x.",
     "multiple_choice",
     "15", "20", "25", "30",
     "B",
     "Corresponding angles are equal: 3x + 10 = 5x - 30. 40 = 2x. x = 20.",
     "parallel_lines"),

    # diff=3 A
    ("geometry", "proofs", "A", 3,
     "In a polygon with 6 sides (hexagon), what is the sum of the interior angles?",
     "multiple_choice",
     "540 degrees", "720 degrees", "900 degrees", "1080 degrees",
     "B",
     "Sum of interior angles = (n - 2) x 180 = (6 - 2) x 180 = 4 x 180 = 720 degrees.",
     "polygon_angles"),

    # diff=3 R
    ("geometry", "proofs", "R", 3,
     "If two lines are cut by a transversal and the co-interior angles are supplementary, what can you conclude?",
     "multiple_choice",
     "The lines are perpendicular", "The lines are parallel", "The lines intersect at 45 degrees", "The transversal is perpendicular to both",
     "B",
     "When co-interior (same-side interior) angles are supplementary, it is the converse of the parallel lines theorem — the lines are parallel.",
     "parallel_lines"),

    # diff=4 U
    ("geometry", "proofs", "U", 4,
     "In quadrilateral ABCD, the diagonals bisect each other. What type of quadrilateral must it be?",
     "multiple_choice",
     "Rectangle", "Rhombus", "Parallelogram", "Trapezoid",
     "C",
     "The diagonals of a parallelogram always bisect each other. This is also a defining property of parallelograms.",
     "quadrilateral_properties"),

    # diff=4 A
    ("geometry", "proofs", "A", 4,
     "Each interior angle of a regular polygon measures 150 degrees. How many sides does it have?",
     "multiple_choice",
     "10", "11", "12", "15",
     "C",
     "Interior angle = (n-2)*180/n = 150. (n-2)*180 = 150n. 180n - 360 = 150n. 30n = 360. n = 12.",
     "polygon_angles"),

    # diff=4 R
    ("geometry", "proofs", "R", 4,
     "Two lines intersect. One of the four angles formed measures (4x + 15) degrees and the angle directly across is (7x - 30) degrees. Find the measure of the angle.",
     "multiple_choice",
     "55 degrees", "75 degrees", "95 degrees", "115 degrees",
     "B",
     "Vertical angles are equal: 4x + 15 = 7x - 30. 45 = 3x. x = 15. Angle = 4(15) + 15 = 75 degrees.",
     "angle_relationships"),

    # diff=5 R
    ("geometry", "proofs", "R", 5,
     "A polygon has an exterior angle sum of 360 degrees regardless of the number of sides. An exterior angle of a regular decagon (10 sides) is how many degrees?",
     "multiple_choice",
     "30 degrees", "36 degrees", "40 degrees", "45 degrees",
     "B",
     "Exterior angle of regular polygon = 360/n = 360/10 = 36 degrees.",
     "polygon_angles"),

    # diff=5 R
    ("geometry", "proofs", "R", 5,
     "In a proof of triangle congruence, you know two triangles share a side. Along with two pairs of equal angles, which theorem applies?",
     "multiple_choice",
     "SSS", "SAS", "AAS", "HL",
     "C",
     "Two pairs of equal angles plus a non-included side (the shared side is not between the known angles) satisfies AAS (Angle-Angle-Side).",
     "congruence_proofs"),
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
    print(f"[seed] supplement: {inserted} new questions inserted")
    return inserted

if __name__ == "__main__":
    seed()
