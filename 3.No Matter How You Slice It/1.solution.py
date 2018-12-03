import re
tile_map = [[[] for x in range(1000)] for x in range(1000)]


class Claim(object):
    __prog = re.compile(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")
    def __init__(self, line):
        match = Claim.__prog.match(line)

        self.id = int(match.group(1))
        self.x = int(match.group(2))
        self.y = int(match.group(3))
        self.w = int(match.group(4))
        self.h = int(match.group(5))

def process_claim(claim):
    for x_coord in range(claim.w):
        for y_coord in range(claim.h):
            tile_map[claim.y + y_coord][claim.x + x_coord] += [claim.id]


with open("input_file.txt", "r") as file:
    for line in file:
        process_claim(Claim(line))

    double_claims = 0
    for y_coord in range(1000):
        for x_coord in range(1000):
            if len(tile_map[y_coord][x_coord]) > 1:
                double_claims += 1

    print(double_claims)