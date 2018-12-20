class Room(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.E = None
        self.W = None
        self.N = None
        self.S = None

        self.value = None

    def __str__(self):
        return "({},{})".format(self.x, self.y)

    def __repr__(self):
        return str(self)

class RoomMap(object):
    def __init__(self, text):
        self._min_x = 0
        self._min_y = 0
        self._max_x = 0
        self._max_y = 0

        self._value = None
        self._rooms = {}
        self._start = self.get_room(0, 0)
        self.add_rooms(text)
        self.convert_to_array()
        self.assign_values()

    def add_rooms(self, text):
        x, y = (0, 0)
        # print("Starting at ({},{})".format(x, y))
        room_stack = []

        current = self._start
        for char in text:
            if char == "E":
                x += 1
                self._max_x = max(x, self._max_x)
                # print("E to ({},{})".format(x, y))
                room = self.get_room(x, y)
                current.E = room
                room.W = current
                current = room

            elif char == "W":
                x -= 1
                self._min_x = min(x, self._min_x)
                # print("W to ({},{})".format(x, y))
                room = self.get_room(x, y)
                current.W = room
                room.E = current
                current = room

            elif char == "N":
                y -= 1
                self._min_y = min(y, self._min_y)
                # print("N to ({},{})".format(x, y))
                room = self.get_room(x, y)
                current.N = room
                room.S = current
                current = room

            elif char == "S":
                y += 1
                self._max_y = max(y, self._max_y)
                # print("S to ({},{})".format(x, y))
                room = self.get_room(x, y)
                current.S = room
                room.N = current
                current = room

            elif char == "(":
                room_stack.append(current)

            elif char == "|":
                current = room_stack[-1]
                x, y = current.x, current.y

            elif char == ")":
                current = room_stack.pop()
                x, y = current.x, current.y

    def get_room(self, x, y):
        if y not in self._rooms:
            self._rooms[y] = {}

        if x not in self._rooms[y]:
            self._rooms[y][x] = Room(x, y)

        return self._rooms[y][x]

    def convert_to_array(self):
        # print(self._min_x, self._max_x)
        # print(self._min_y, self._max_y)
        self._room_map = []
        for y in range(self._min_y, self._max_y + 1):
            line = []
            for x in range(self._min_x, self._max_x + 1):
                line.append(self.get_room(x, y))
            self._room_map.append(line)

    def assign_values(self):
        rooms_to_assign = [(0,0,0)]

        while rooms_to_assign:
            x, y, value = rooms_to_assign.pop(0)
            room = self.get_room(x, y)
            if room.value is None or room.value > value:
                room.value = value
                if room.N:
                    rooms_to_assign.append((room.N.x, room.N.y, value + 1))
                if room.S:
                    rooms_to_assign.append((room.S.x, room.S.y, value + 1))
                if room.E:
                    rooms_to_assign.append((room.E.x, room.E.y, value + 1))
                if room.W:
                    rooms_to_assign.append((room.W.x, room.W.y, value + 1))

    def find_peak_room(self):
        return max([room.value for line in self._room_map for room in line])

    def count(self, size):
        return len([room.value for line in self._room_map for room in line if room.value >= size])

    def print(self):
        for y in range(len(self._room_map)):
            top_line = ""
            mid_line = ""
            for x in range(len(self._room_map[y])):
                room = self._room_map[y][x]

                top_line += "#"
                if room.N:
                    upper_room = self._room_map[y-1][x]
                    assert upper_room == room.N
                    assert upper_room.S == room
                    top_line += "-"
                else:
                    top_line += "#"

                if room.W:
                    left_room = self._room_map[y][x-1]
                    assert room.W == left_room
                    assert left_room.E == room
                    mid_line += "|"
                else:
                    mid_line += "#"
                mid_line += str(room.value % 10)

            top_line += "#"
            mid_line += "#"
            print(top_line)
            print(mid_line)
        final_line = "#" * (len(self._room_map[-1]) * 2 + 1)
        print(final_line)

with open("input_file.txt", "r") as file:
    regex = file.read()
important_part = regex[1:-1]
room_map = RoomMap(important_part)
room_map.print()
print(room_map.find_peak_room())
print(room_map.count(1000))