import copy

class LumberMap(object):
    def __init__(self, file):
        self._minute = 0
        self._map = [[char for char in line.strip()] for line in file]

    @property
    def minute(self):
        return self._minute
    
    @property
    def resource_value(self):
        empty, trees, yards = self.count_nodes()
        return trees * yards
    

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


values = [lumber_map.resource_value]

consecutive_repeats = 0
while consecutive_repeats < 5:
    lumber_map.advance()
    resource_value = lumber_map.resource_value
    if resource_value in values:
        consecutive_repeats += 1
    else:
        consecutive_repeats = 0

    values.append(resource_value)

def detect_cycle(values, consecutive_repeats):
    for i in range(len(values)):
        if values[i:i+consecutive_repeats] == values[-consecutive_repeats:]:
            cycle_start = i
            cycle_length = len(values) - consecutive_repeats - i
            cycle_values = values[i:i+cycle_length]
            print("Repeating cycle starts at {}".format(cycle_start))
            print("Cycle length {}".format(cycle_length))
            print("cycle_values: {}".format(cycle_values))

            return cycle_start, cycle_length, cycle_values

cycle_start, cycle_length, cycle_values = detect_cycle(values, consecutive_repeats)

def get_expected_value(cycle_start, cycle_length, cycle_values, index):
    return cycle_values[(index - cycle_start) % cycle_length]

# Advance the simulation 100 more frames
for i in range(100):
    lumber_map.advance()
    values.append(lumber_map.resource_value)

# Verify everything from cycle start to end of array
for i in range(cycle_start, len(values)):
    if values[i] != get_expected_value(cycle_start, cycle_length, cycle_values, i):
        print("Expected {} but got {} at {}".format(get_expected_value(cycle_start, cycle_length, cycle_values, i), values[i], i))

# Print our answer
print("Value at 1000000000: {}".format(get_expected_value(cycle_start, cycle_length, cycle_values, 1000000000)))