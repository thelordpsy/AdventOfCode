class Room(object):
    def __init__(self, x, y):
        self._x = x
        self._y = y

        self.E = None
        self.W = None
        self.N = None
        self.S = None


class RoomMap(object):
    def __init__(self, text):
        self._min_x = 0
        self._min_y = 0
        self._max_x = 0
        self._max_y = 0

        self._value = None
        self._rooms = {}
        self._start = Room(0, 0)
        self.add_rooms(text)
        self.convert_to_array()

    def add_rooms(self, text):
        x, y = (0, 0)
        room_stack = []

        current = self._start
        for char in text:
            if char == "E":
                x += 1
                self._max_x = max(x, self._max_x)
                room = self.get_room(x, y)
                current.E = room
                room.W = current
                current = room

            elif char == "W":
                self._min_x = min(x, self._min_x)
                x -= 1
                room = self.get_room(x, y)
                current.W = room
                room.E = current
                current = room

            elif char == "N":
                self._min_y = min(y, self._min_y)
                y -= 1
                room = self.get_room(x, y)
                current.N = room
                room.S = current
                current = room

            elif char == "S":
                y += 1
                self._max_y = max(y, self._max_y)
                room = self.get_room(x, y)
                current.S = room
                room.N = current
                current = room

            elif char == "(":
                room_stack.append(current)

            elif char == "|":
                current = room_stack[-1]
                x, y = current._x, current._y

            elif char == ")":
                current = room_stack.pop()
                x, y = current._x, current._y

    def get_room(self, x, y):
        if y not in self._rooms:
            self._rooms[y] = {}

        if x not in self._rooms[y]:
            self._rooms[y][x] = Room(x, y)

        return self._rooms[y][x]

    def convert_to_array(self):
        print(self._min_x, self._max_x)
        print(self._min_y, self._max_y)
        self._room_map = []
        for y in range(self._min_y, self._max_y + 1):
            line = []
            for x in range(self._min_x, self._max_x + 1):
                line.append(self.get_room(x, y))
            self._room_map.append(line)

    def print(self):
        for y in range(len(self._room_map)):
            line = ""
            for x in range(len(self._room_map[y])):
                line += "X"
            print(line)



with open("input_file.txt", "r") as file:
    regex = file.read()
important_part = regex[1:-1]
room_map = RoomMap(important_part)
room_map.print()