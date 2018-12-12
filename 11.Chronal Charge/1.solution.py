class Grid(object):
    def __init__(self, serial_number):
        self._serial_number = serial_number
        self._power_levels = self._make_power_levels()
        self._power_sums = self._make_power_sums()

    def _make_power_levels(self):
        return [[self._derive_power_level(x,y) for x in range(300)] for y in range(300)]

    def _make_power_sums(self):
        return [[self._derive_power_sum(x,y) for x in range(300 - 2)] for y in range(300 - 2)]

    def _derive_power_level(self, x, y):
        # Convert from indexes to coordinates
        x, y = x+1, y+1
        rack_id = x + 10
        power_level = (rack_id * y + self._serial_number) * rack_id
        return (int(power_level / 100) % 10) - 5

    def _derive_power_sum(self, x, y):
        grid = [[(x, y) for x in range(x, x+3)] for y in range(y, y+3)]
        grid = [item for sublist in grid for item in sublist]
        return sum([self._power_levels[y][x] for (x, y) in grid])

    def power_level(self, x, y):
        return self._power_levels[y-1][x-1]

    def max(self):
        peak_x = peak_y = peak_value = None
        for y in range(300 - 2):
            for x in range(300 - 2):
                if peak_value is None or self._power_sums[y][x] > peak_value:
                    peak_value = self._power_sums[y][x]
                    peak_x = x
                    peak_y = y

        return (peak_x+1, peak_y+1, peak_value)




# Power Level tests
# Expect 4 -5 0 4
print(Grid(8).power_level(3, 5))
print(Grid(57).power_level(122, 79))
print(Grid(39).power_level(217, 196))
print(Grid(71).power_level(101, 153))

# Power Sum Tests
# Expect (33,45,29), (21,61,30)
print(Grid(18).max())
print(Grid(42).max())

with open("input_file.txt") as file:
    serial_number = int(file.read())
print(Grid(serial_number).max())