# Resorted to heuristically cutting the search when we see constantly decreasing values.  I'm convinced that there's a reasonable time way to do an exhaustive search though.

class Grid(object):
    def __init__(self, serial_number, grid_size=300):
        self._grid_size = grid_size
        self._serial_number = serial_number
        self._power_levels = self._make_power_levels()

    def _make_power_levels(self):
        return [[self._derive_power_level(x,y) for x in range(self._grid_size)] for y in range(self._grid_size)]

    def _power_sum_grid_width(self, power_grid_size):
        return self._grid_size - (power_grid_size - 1)

    def _make_power_sums(self, power_grid_size):
        grid = [[0 for x in range(self._power_sum_grid_width(power_grid_size))] for y in range(self._power_sum_grid_width(power_grid_size))]

        for y in range(self._power_sum_grid_width(power_grid_size)):
            for x in range(self._power_sum_grid_width(power_grid_size)):
                if x == 0:
                    grid[y][x] = self._derive_power_sum_basic(x, y, power_grid_size)
                    continue

                new_val = grid[y][x-1]
                new_val -= sum([self._power_levels[old_y][x-1] for old_y in range(y, y+power_grid_size)])
                new_val += sum([self._power_levels[old_y][x-1+power_grid_size] for old_y in range(y, y+power_grid_size)])
                grid[y][x] = new_val

        return grid

    def _derive_power_level(self, x, y):
        # Convert from indexes to coordinates
        x, y = x+1, y+1
        rack_id = x + 10
        power_level = (rack_id * y + self._serial_number) * rack_id
        return (int(power_level / 100) % 10) - 5

    def _derive_power_sum_basic(self, x, y, power_grid_size):
        grid = [[(x, y) for x in range(x, x+power_grid_size)] for y in range(y, y+power_grid_size)]
        grid = [item for sublist in grid for item in sublist]
        return sum([self._power_levels[y][x] for (x, y) in grid])

    def power_level(self, x, y):
        return self._power_levels[y-1][x-1]

    def max(self, power_grid_size):
        power_sums = self._make_power_sums(power_grid_size)
        peak_x = peak_y = peak_value = None
        for y in range(self._power_sum_grid_width(power_grid_size)):
            for x in range(self._power_sum_grid_width(power_grid_size)):
                if peak_value is None or power_sums[y][x] > peak_value:
                    peak_value = power_sums[y][x]
                    peak_x = x
                    peak_y = y

        return (peak_x+1, peak_y+1, peak_value)

    def global_max(self):
        last_5 = [-1000] * 5

        global_max_x = global_max_y = None
        global_max_size = global_max_power = None
        for i in range(self._grid_size):
            peak_x, peak_y, peak_value = self.max(i+1)
            #print("Progress: ", peak_x, peak_y, i+1, peak_value)
            del last_5[0]
            last_5.append(peak_value)
            if all(last_5[i] > last_5[i+1] for i in range(len(last_5)-1)):
                return (global_max_x, global_max_y, global_max_size, global_max_power)

            if global_max_power is None or peak_value > global_max_power:
                global_max_power = peak_value
                global_max_x = peak_x
                global_max_y = peak_y
                global_max_size = i+1

        return (global_max_x, global_max_y, global_max_size, global_max_power)





# Power Level tests
# Expect 4 -5 0 4
print(Grid(8).power_level(3, 5))
print(Grid(57).power_level(122, 79))
print(Grid(39).power_level(217, 196))
print(Grid(71).power_level(101, 153))

# Power Sum Tests
# Expect (33,45,29), (21,61,30)
print(Grid(18).max(3))
print(Grid(42).max(3))

# Global Max Tests
# Expect (90,269,16,113), (232,251,12,119)
print(Grid(18).global_max())
print(Grid(42).global_max())

with open("input_file.txt") as file:
    serial_number = int(file.read())
print(Grid(serial_number).global_max())