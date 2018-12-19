import copy
import re
import subprocess


class Reservoir(object):
    def __init__(self):
        self._clay_tiles = []
        self._map = []
        self.x_min = self.x_max = self.y_min = self.y_max = None

    @property
    def x_boundary(self):
        return len(self._map[0])

    def add_clay(self, line):
        match = re.match(r"x=(\d+), y=(\d+)\.\.(\d+)", line)
        if match:
            x = int(match.group(1))
            for y in range(int(match.group(2)), int(match.group(3)) + 1):
                self._clay_tiles.append((x, y))
        else:
            match = re.match(r"y=(\d+), x=(\d+)\.\.(\d+)", line)
            assert(match)

            y = int(match.group(1))
            for x in range(int(match.group(2)), int(match.group(3)) + 1):
                self._clay_tiles.append((x, y))

    def generate_map(self):
        self.x_min = min([x for x, y in self._clay_tiles]) - 1
        self.x_max = max([x for x, y in self._clay_tiles]) + 1
        self.y_min = min([y for x, y in self._clay_tiles])
        self.y_max = max([y for x, y in self._clay_tiles])
        self._map = [["." for x in range(self.x_min, self.x_max + 1)] for y in range(self.y_min, self.y_max + 1)]
        for point in self._clay_tiles:
            x, y = point
            self._set_element(x - self.x_min, y - self.y_min, "#")

    def count_water(self):
        count = 0
        for line in self._map:
            for tile in line:
                if tile == "|" or tile == "~":
                    count += 1
        return count

    def spawn_water(self):
        iterations = 0
        position = (500, self.y_min)

        x, y = position
        x -= self.x_min
        y -= self.y_min
        # Mark this position as having water
        self._map[y][x] = "|"

        made_change = False
        check_nodes = [(x, y)]
        while check_nodes:
            iterations += 1
            if iterations % 1000 == 0:
                self.print_file(str(iterations) + ".out", check_nodes)
            if iterations > 10000:
                print("Non-terminal I assume")
                exit(0)
            x, y = check_nodes.pop()
            if iterations > 9000:
                print(self.count_water())
            made_change |= self._add_water(x, y, check_nodes)
        return made_change

    def _add_water(self, x, y, check_nodes):
        element = self._element_at_position(x, y)
        if element == "#" or element == "~":
            return False

        element_under = self._element_under_position(x, y)
        if element_under == None:
            #print("({}, {}) goes off the map".format(x, y))
            return self._set_element(x, y, "|")
        elif element_under == "." or element_under == "|":
            #print("({}, {}) flows downward".format(x, y))
            made_change = self._set_element(x, y, "|")
            check_nodes += [(x, y+1)]
            return made_change

        elif element_under == "#" or element_under == "~":
            left_x, left_bounded = self._find_left_boundary(x, y)
            right_x, right_bounded = self._find_right_boundary(x, y)

            if left_bounded and right_bounded:
                #print("({}, {}) bounded [{}-{}]".format(x, y, left_x, right_x + 1))
                made_change = False
                for sub_x in range(left_x, right_x + 1):
                    made_change |= self._set_element(sub_x, y, "~")
                if made_change:
                    check_nodes += [(x, y - 1)]
                return made_change
            else:
                #print("({}, {}) unbounded [{}-{}]".format(x, y, left_x, right_x + 1))
                made_change = False
                for sub_x in range(left_x, right_x + 1):
                    made_change |= self._set_element(sub_x, y, "|")
                if self._element_under_position(left_x, y) != "#":
                    check_nodes += [(left_x, y+1)]
                if self._element_under_position(right_x, y) != "#":
                    check_nodes += [(right_x, y+1)]
                return made_change

    def _find_left_boundary(self, x, y):
        while True:
            x -= 1
            if x < 0:
                return 0, False

            if self._element_at_position(x, y) == "#":
                return x+1, True

            if self._element_under_position(x, y) != "#" and self._element_under_position(x, y) != "~":
                return x, False

    def _find_right_boundary(self, x, y):
        while True:
            x += 1
            if x >= self.x_boundary:
                return self.x_boundary-1, False

            if self._element_at_position(x, y) == "#":
                return x-1, True

            if self._element_under_position(x, y) != "#" and self._element_under_position(x, y) != "~":
                return x, False


    def _set_element(self, x, y, element):
        if self._map[y][x] == element:
            return False
        self._map[y][x] = element
        return True

    def _element_at_position(self, x, y):
        return self._map[y][x]

    def _element_under_position(self, x, y):
        y += 1
        if y >= len(self._map):
            return None

        return self._map[y][x]


    def print(self):
        subprocess.call("cls", shell=True)
        for line in self._map:
            print("".join(line))

    def print_file(self, filename, check_nodes):
        map_copy = copy.deepcopy(self._map)
        for x, y in check_nodes:
            map_copy[y][x] = "X"

        with open(filename, "w") as file:
            for line in map_copy:
                file.write("".join(line) + "\n")



r = Reservoir()
with open("input_file.txt", "r") as file:
    for line in file:
        r.add_clay(line)

count = 0
r.generate_map()
r.spawn_water()
r.print()
print(r.count_water())
print(count)