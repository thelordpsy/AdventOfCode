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



def assign(coordinates, x, y):
    result = [(i, coordinates[i].distance(x, y)) for i in range(len(coordinates))]
    result = sorted(result, key=lambda x: x[1])
    if result[0][1] == result[1][1]:
        return None

    return result[0][0]


def disqualify(coordinates, number):
    if number == None:
        return
    coordinates[number]._disqualified = True


def increment(coordinates, number):
    if number == None:
        return
    coordinates[number]._area += 1



with open("input_file.txt", "r") as file:
    coordinates = [Coordinate(line) for line in file]


min_x = min([coord._x for coord in coordinates])
max_x = max([coord._x for coord in coordinates])
x_extent = (max_x - min_x)

min_y = min([coord._y for coord in coordinates])
max_y = max([coord._y for coord in coordinates])
y_extent = (max_y - min_y)

for y_index in range(y_extent):
    for x_index in range(x_extent):
        y_coord = y_index + min_y
        x_coord = x_index + min_x
        owner = assign(coordinates, x_coord, y_coord)
        increment(coordinates, owner)
        if y_index == 0 or y_index == y_extent - 1 or x_index == 0 or x_index == x_extent - 1:
            disqualify(coordinates, owner)

print(max([coordinate._area for coordinate in coordinates if not coordinate._disqualified]))