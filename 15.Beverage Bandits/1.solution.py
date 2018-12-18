import subprocess

class Unit(object):
    pass

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

    def _move_unit(self, unit_position):
        x, y = unit_position
        unit = self._unit_layer[y][x]

        potential_targets = self._gather_units(unit_type=unit.target_type)
        if len(potential_targets) == 0:
            self._complete_game()

        movement_options = self._generate_adjacency_list(unit_position)
        for opt_x, opt_y, in movement_options:
            if self._unit_layer[opt_y][opt_x] != None and type(self._unit_layer[opt_y][opt_x] == unit.target_type):
                return (x, y) # No need to move, we're adjacent to an enemy

        movement_targets = self._generate_movement_target_grid(potential_targets)
        player_distance_graph = self._make_distance_graph(unit_position)

        movement_targets = [target_position for target_position in movement_targets if player_distance_graph[target_position[1]][target_position[0]]]
        if len(movement_targets) == 0:
            return (x, y) # Nowhere to move

        min_distance = min([player_distance_graph[y][x] for x, y in movement_targets])
        movement_targets = [(x,y) for x,y in movement_targets if player_distance_graph[y][x] == min_distance]
        min_y = min([y for x,y in movement_targets])
        movement_targets = [(x,y) for x,y in movement_targets if y == min_y]
        min_x = min([x for x,y in movement_targets])
        movement_targets = [(x,y) for x,y in movement_targets if x == min_x]

        movement_target = movement_targets[0]
        reverse_distance_graph = self._make_distance_graph(movement_target)
        
        movement_options = [(x, y) for x, y in movement_options if type(reverse_distance_graph[y][x]) == int]
        movement_options = [(x, y, reverse_distance_graph[y][x]) for x, y in movement_options]
        min_value = min([value for x, y, value in movement_options])
        movement_options = [(x, y) for x, y, value in movement_options if value == min_value]
        min_y = min([y for x, y in movement_options])
        movement_options = [(x, y) for x, y in movement_options if y == min_y]
        min_x = min([x for x, y in movement_options])
        movement_options = [(x, y) for x, y in movement_options if x == min_x]

        self._unit_layer[y][x] = None
        x, y = movement_options[0]
        self._unit_layer[y][x] = unit
        return (x, y)

    def _perform_attack(self, unit_position):
        x, y = unit_position
        attacking_unit = self._unit_layer[y][x]

        target_options = self._generate_adjacency_list(unit_position)
        target_options = [option for option in target_options if self._has_unit(option)]
        target_options = [(x,y) for x,y in target_options if type(self._unit_layer[y][x]) == attacking_unit.target_type]

        if len(target_options) == 0:
            return


        target_options = [(x,y,self._unit_layer[y][x].health) for x,y in target_options]
        min_health = min([health for x,y,health in target_options])
        target_options = [(x,y) for x,y,health in target_options if health == min_health]
        min_y = min([y for x, y in target_options])
        target_options = [(x, y) for x, y in target_options if y == min_y]
        min_x = min([x for x, y in target_options])
        target_options = [(x, y) for x, y in target_options if x == min_x]

        target_x, target_y = target_options[0]
        enemy_unit = self._unit_layer[target_y][target_x]
        enemy_unit.health -= attacking_unit.power
        if enemy_unit.health <= 0:
            self._unit_layer[target_y][target_x] = None

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
        health_sum = sum([self._unit_layer[y][x].health for x, y in self._gather_units()])
        print(health_sum * self._round_id)
        exit(0)


    def print(self):
        subprocess.call("cls", shell=True)
        for y in range(len(self._map_layer)):
            line = ""
            for x in range(len(self._map_layer[y])):
                if self._unit_layer[y][x] is not None:
                    line += self._unit_layer[y][x].char
                else:
                    line += self._map_layer[y][x]
            print(line)

    def _print_graph(self, graph):
        for line in graph:
            print(line)




sim = GameSimulation()
with open("input_file.txt", "r") as file:
    sim.load(file)

while True:
    sim.tick()