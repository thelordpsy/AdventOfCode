import copy

class LumberMap(object):
    def __init__(self, file):
        self._minute = 0
        self._map = [[char for char in line.strip()] for line in file]

    @property
    def minute(self):
        return self._minute
    

    def print(self):
        for line in self._map:
            print("".join(line))

    def advance(self):
        self._minute += 1
        new_map = copy.deepcopy(self._map)
        for y in range(len(self._map)):
            for x in range(len(self._map)):
                new_map[y][x] = self._advance_node(x, y)
        self._map = new_map

    def count_nodes(self):
        empty = trees = yards = 0
        for line in self._map:
            for char in line:
                if char == ".":
                    empty += 1
                elif char == "|":
                    trees += 1
                elif char == "#":
                    yards += 1
        return empty, trees, yards


    def _advance_node(self, x, y):
        element = self._element_at(x, y)
        adjacent_empties, adjacent_trees, adjacent_yards = self._count_adjacent(x, y)
        if element == "." and adjacent_trees >= 3:
            return "|"
        elif element == "|" and adjacent_yards >= 3:
            return "#"
        elif element == "#" and (adjacent_yards < 1 or adjacent_trees < 1):
            return "."
        else:
            return element

    def _count_adjacent(self, x, y):
        grid = [(x-1,y-1), (x,y-1), (x+1,y-1), 
                (x-1,y),            (x+1,y),
                (x-1,y+1), (x,y+1), (x+1,y+1)]

        count_empty = 0
        count_tree = 0
        count_yard = 0

        for position in grid:
            if self._element_at(*position) == ".":
                count_empty += 1
            elif self._element_at(*position) == "|":
                count_tree += 1
            elif self._element_at(*position) == "#":
                count_yard += 1

        return count_empty, count_tree, count_yard

    def _element_at(self, x, y):
        if y < 0 or y >= len(self._map):
            return None

        if x < 0 or x >= len(self._map[y]):
            return None

        return self._map[y][x]

        # An open acre will become filled with trees if three or more adjacent acres contained trees. Otherwise, nothing happens.
        # An acre filled with trees will become a lumberyard if three or more adjacent acres were lumberyards. Otherwise, nothing happens.
        # An acre containing a lumberyard will remain a lumberyard if it was adjacent to at least one other lumberyard and at least one acre containing trees. Otherwise, it becomes open.

with open("input_file.txt", "r") as file:
    lumber_map = LumberMap(file)

for i in range(10):
    lumber_map.advance()

print("Minutes: {}".format(lumber_map.minute))
lumber_map.print()
empty, trees, yards = lumber_map.count_nodes()
print("[Trees: {}] [Yards: {}]".format(trees, yards))
print("Resource Value: {}".format(trees * yards))