import subprocess
import time


def minimize(value_list):
    best_option = None
    for option in value_list:
        if best_option is None:
            best_option = option
            continue

        new_x, new_y, new_z = option
        best_x, best_y, best_z = best_option

        if new_z > best_z:
            continue
        elif new_z < best_z:
            best_option = option
            continue

        if new_y > best_y:
            continue
        elif new_y < best_y:
            best_option = option
            continue

        if new_x > best_x:
            continue
        elif new_x < best_x:
            best_option = option
            continue

        assert("Should not have fully equal comparators")

    return (best_option[0], best_option[1])

def timing(name):
    def wrap_fxn(fxn):
        def run_me(self, *args, **kwargs):
            if name not in self._times:
                self._times[name] = 0

            start = time.time()
            result = fxn(self, *args, **kwargs)
            self._times[name] += time.time() - start
            return result
        return run_me
    return wrap_fxn

class Unit(object):
    def __str__(self):
        return "{}({})".format(self.char, self.health)

class Goblin(Unit):
    def __init__(self):
        self.char = "G"
        self.target_type = Elf
        self.health = 200
        self.power = 3

class Elf(Unit):
    def __init__(self):
        self.char = "E"
        self.target_type = Goblin
        self.health = 200
        self.power = 3

class GameSimulation(object):
    def __init__(self):
        self._round_id = 0
        self._map_layer = []
        self._unit_layer = []
        self._times = {}

    def load(self, file):
        for line in file:
            map_layer_line = []
            unit_layer_line = []
            for char in line:
                if char == "#":
                    map_layer_line.append("#")
                    unit_layer_line.append(None)
                elif char == ".":
                    map_layer_line.append(".")
                    unit_layer_line.append(None)
                elif char == "G":
                    map_layer_line.append(".")
                    unit_layer_line.append(Goblin())
                elif char == "E":
                    map_layer_line.append(".")
                    unit_layer_line.append(Elf())
                else:
                    assert("Bad character input")
            self._map_layer.append(map_layer_line)
            self._unit_layer.append(unit_layer_line)

    @timing("tick")
    def tick(self):
        unit_positions = self._gather_units()

        for unit_position in unit_positions:
            self._tick_unit(unit_position)
        self._round_id += 1

    def _tick_unit(self, unit_position):
        unit_x, unit_y = unit_position
        if self._unit_layer[unit_y][unit_x] == None:
            return # This unit was killed this turn

        unit_position = self._move_unit(unit_position)
        self._perform_attack(unit_position)

    @timing("\tmove_unit")
    def _move_unit(self, unit_position):
        x, y = unit_position
        unit = self._unit_layer[y][x]

        potential_targets = self._gather_units(unit_type=unit.target_type)
        if len(potential_targets) == 0:
            self._complete_game()

        if self._has_adjacent_enemy(unit_position):
            return (x, y)

        movement_targets = self._generate_movement_target_grid(potential_targets)
        movement_target = self._select_closest_point(unit_position, movement_targets, block_zero=True)
        if movement_target is None:
            return (x, y)

        movement_options = self._generate_adjacency_list(unit_position)
        movement_selection = self._select_closest_point(movement_target, movement_options, block_zero=False)
        assert(movement_selection)

        self._unit_layer[y][x] = None
        x, y = movement_selection
        self._unit_layer[y][x] = unit
        return movement_selection

    @timing("\tperform_attack")
    def _perform_attack(self, unit_position):
        x, y = unit_position
        attacking_unit = self._unit_layer[y][x]
        target = self._select_attack_target(unit_position)
        if target is None:
            return

        target_x, target_y = target
        enemy_unit = self._unit_layer[target_y][target_x]
        enemy_unit.health -= attacking_unit.power
        if enemy_unit.health <= 0:
            self._unit_layer[target_y][target_x] = None

    def _select_attack_target(self, unit_position):
        x, y = unit_position
        attacking_unit = self._unit_layer[y][x]
        target_options = self._generate_adjacency_list(unit_position)
        target_options = [option for option in target_options if self._has_unit(option)]
        target_options = [(x, y, self._unit_layer[y][x].health) for x, y in target_options if self._unit_layer[y][x] and type(self._unit_layer[y][x]) == attacking_unit.target_type]
        if len(target_options) == 0:
            return  None

        return minimize(target_options)

    def _has_adjacent_enemy(self, unit_position):
        unit_x, unit_y = unit_position
        unit = self._unit_layer[unit_y][unit_x]
        adjacent_spaces = self._generate_adjacency_list(unit_position)
        for target_x, target_y in adjacent_spaces:
            if self._space_has_unit(target_x, target_y, unit_type=unit.target_type):
                return (unit_x, unit_y)

    def _space_has_unit(self, target_x, target_y, unit_type=None):
        if self._unit_layer[target_y][target_x] is None:
            return False

        if unit_type is None:
            return True

        return type(self._unit_layer[target_y][target_x]) == unit_type

    def _select_closest_point(self, initial_position, point_list, block_zero):
        distance_graph = self._make_distance_graph(initial_position)

        def point_is_valid(x, y):
            if type(distance_graph[y][x]) is not int:
                return False
            if distance_graph[y][x] == 0 and block_zero:
                return False
            return True

        value_list = [(x, y, distance_graph[y][x]) for x, y in point_list if point_is_valid(x, y)]
        if len(value_list) == 0:
            return None

        return minimize(value_list)

    def _gather_units(self, unit_type=None):
        unit_positions = []

        for y in range(len(self._unit_layer)):
            for x in range(len(self._unit_layer[y])):
                if self._unit_layer[y][x] is not None:
                    if unit_type and type(self._unit_layer[y][x]) != unit_type:
                        continue

                    unit_positions.append((x,y))
        return unit_positions

    def _generate_adjacency_list(self, location):
        x, y = location
        adjacent_nodes = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        adjacent_nodes = [(x,y) for x,y in adjacent_nodes if x >= 0 and y >= 0 and y < len(self._map_layer) and x < len(self._map_layer[0])]
        return adjacent_nodes

    @timing("\t\tgenerate_movement_target_grid")
    def _generate_movement_target_grid(self, targets):
        movement_targets = []
        for position in targets:
            movement_targets += self._generate_adjacency_list(position)

        return [position for position in movement_targets if not self._is_wall(position) and not self._has_unit(position)]

    def _is_wall(self, position):
        x, y = position
        return self._map_layer[y][x] == "#"

    def _has_unit(self, position):
        x, y = position
        return self._unit_layer[y][x] is not None

    @timing("\t\tmake_distance_graph")
    def _make_distance_graph(self, unit_position):
        unit_x, unit_y = unit_position
        graph = []
        for y in range(len(self._map_layer)):
            graph_line = []
            for x in range(len(self._map_layer[y])):
                if self._map_layer[y][x] == "#":
                    graph_line.append(False)
                elif y == unit_y and x == unit_x:
                    graph_line.append(0)
                elif self._unit_layer[y][x] != None:
                    graph_line.append(False)
                else:
                    graph_line.append(None)
            graph.append(graph_line)

        made_changes = True
        while made_changes:
            made_changes = False
            for y in range(len(self._map_layer)):
                for x in range(len(self._map_layer[y])):
                    if graph[y][x] == False:
                        continue

                    if type(graph[y][x]) == int:
                        current_value = graph[y][x]
                    else:
                        current_value = 999999

                    if y > 0 and type(graph[y-1][x]) == int and graph[y-1][x] < current_value - 1:
                        graph[y][x] = graph[y-1][x] + 1
                        made_changes = True
                    if y < len(graph) - 1 and type(graph[y+1][x]) == int and graph[y+1][x] < current_value - 1:
                        graph[y][x] = graph[y+1][x] + 1
                        made_changes = True
                    if x > 0 and type(graph[y][x-1]) == int and graph[y][x-1] < current_value - 1:
                        graph[y][x] = graph[y][x-1] + 1
                        made_changes = True
                    if x < len(graph[0]) - 1 and type(graph[y][x+1]) == int and graph[y][x+1] < current_value - 1:
                        graph[y][x] = graph[y][x+1] + 1
                        made_changes = True
        return graph

    def _get_distance(self, unit_position, target_position):
        return 0

    def _complete_game(self):
        self.print()
        print()
        print("{} complete rounds".format(self._round_id))

        units = [self._unit_layer[y][x] for x, y in self._gather_units()]
        print("Remaining Units: {}".format(", ".join([str(unit) for unit in units])))

        health_sum = sum([unit.health for unit in units])
        print("Health Total: {}".format(health_sum))
        print("Puzzle Solution: {}".format(health_sum * self._round_id))
        exit(0)


    def print(self):
        subprocess.call("cls", shell=True)
        print("Round " + str(self._round_id))
        for y in range(len(self._map_layer)):
            line = ""
            for x in range(len(self._map_layer[y])):
                if self._unit_layer[y][x] is not None:
                    line += self._unit_layer[y][x].char
                else:
                    line += self._map_layer[y][x]

            units_portion = [str(unit) for unit in self._unit_layer[y] if unit]
            if len(units_portion) > 0:
                line += "    " + ", ".join(units_portion)

            print(line)
        self._print_timing()

    def _print_timing(self):
        for name, duration in self._times.items():
            print(name, duration)

    def _print_graph(self, graph):
        for line in graph:
            print(line)




sim = GameSimulation()
with open("input_file.txt", "r") as file:
    sim.load(file)

sim.print()
while True:
    #input()

    sim.tick()
    sim.print()