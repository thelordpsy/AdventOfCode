import re

class Point(object):
    __prog = re.compile(r"position=<(.+),(.+)> velocity=<(.+),(.+)>")
    def __init__(self, line):
        match = Point.__prog.match(line)
        self._position_x = int(match.group(1))
        self._position_y = int(match.group(2))

        self._velocity_x = int(match.group(3))
        self._velocity_y = int(match.group(4))

    def advance(self):
        self._position_x += self._velocity_x
        self._position_y += self._velocity_y

def has_adjacent_point(point, points):
    for comparison_point in points:
        if comparison_point is point:
            continue

        if abs(comparison_point._position_x - point._position_x) <= 1 and abs(comparison_point._position_y - point._position_y) <= 1:
           return True

    return False

def all_adjacent(points):
    for point in points:
        if not has_adjacent_point(point, points):
            return False
    return True

def has_point(points, x, y):
    for point in points:
        if point._position_x == x and point._position_y == y:
            return True
    return False

def draw(points):
    x_min = min([point._position_x for point in points])
    x_max = max([point._position_x for point in points])

    y_min = min([point._position_y for point in points])
    y_max = max([point._position_y for point in points])

    for y_val in range(y_max + 1 - y_min):
        line_str = ""
        for x_val in range(x_max + 1 - x_min):
            if has_point(points, x_val + x_min, y_val + y_min):
                line_str += "#"
            else:
                line_str += " "
        print(line_str)



with open("input_file.txt") as file:
    points = [Point(line) for line in file]

while not all_adjacent(points):
    for point in points:
        point.advance()

draw(points)