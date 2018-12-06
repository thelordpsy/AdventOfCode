class Coordinate(object):
    def __init__(self, line):
        self._x, self._y = [int(word.strip()) for word in line.split(",")]
        self._area = 0
        self._disqualified = False

    def distance(self, x, y):
        return abs(self._x - x) + abs(self._y - y)

    def __str__(self):
        return "({})".format(self.__repr__())

    def __repr__(self):
        return "{}, {}".format(self._x, self._y)

def distance_sum(coordinates, x, y):
    return sum([coordinates[i].distance(x, y) for i in range(len(coordinates))])

with open("input_file.txt", "r") as file:
    coordinates = [Coordinate(line) for line in file]


min_x = min([coord._x for coord in coordinates])
max_x = max([coord._x for coord in coordinates])
x_extent = (max_x - min_x)

min_y = min([coord._y for coord in coordinates])
max_y = max([coord._y for coord in coordinates])
y_extent = (max_y - min_y)

area = 0
for y_index in range(y_extent):
    for x_index in range(x_extent):
        y_coord = y_index + min_y
        x_coord = x_index + min_x

        if distance_sum(coordinates, x_coord, y_coord) < 10000:
            area += 1
            if x_index == 0 or x_index == x_extent - 1 or y_index == 0 or y_index == y_extent - 1:
                print("WARNING-  EXTENTS NOT LARGE ENOUGH!  Border node ({}, {}) is within region!".format(x_coord, y_coord))


print(area)