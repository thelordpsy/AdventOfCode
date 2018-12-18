import copy

class Machine(object):
    def __init__(self):
        self._registers = [0, 0, 0, 0]
        self._opcode_discovery = {}
        self._resolved_opcodes = {}
        self._str_to_op = {
            "addr": self.addr,
            "addi": self.addi,
            "mulr": self.mulr,
            "muli": self.muli,
            "banr": self.banr,
            "bani": self.bani,
            "borr": self.borr,
            "bori": self.bori,
            "setr": self.setr,
            "seti": self.seti,
            "gtir": self.gtir,
            "gtri": self.gtri,
            "gtrr": self.gtrr,
            "eqir": self.eqir,
            "eqri": self.eqri,
            "eqrr": self.eqrr
        }

    def set_registers(self, values):
        self._registers = copy.deepcopy(values)

    def get_registers(self):
        return copy.deepcopy(self._registers)

    def test_opcode(self, starting_value, operation, ending_value):
        index, a, b, c = operation

        possible_ops = []
        for name, function in self._str_to_op.items():
            self.set_registers(starting_value)
            function(a, b, c)
            if ending_value == self._registers:
                possible_ops.append(name)

        self._assign_result(index, possible_ops)
        return len(possible_ops)

    def resolve_opcodes(self):
        found_entry = True
        while found_entry:
            found_entry = False
            for key, value in self._opcode_discovery.items():
                if len(value) == 1:
                    self._resolved_opcodes[key] = list(value)[0]
                    found_entry = True

            for key, value in self._resolved_opcodes.items():
                for disc_key in self._opcode_discovery:
                    if value in self._opcode_discovery[disc_key]:
                        self._opcode_discovery[disc_key].remove(value)

        for key in self._resolved_opcodes.keys():
            self._resolved_opcodes[key] = self._str_to_op[self._resolved_opcodes[key]]


    def _print_resolved(self):
        print("Resolved Opcodes")
        for key in sorted(self._resolved_opcodes):
            print("{}: {}".format(key, self._resolved_opcodes[key]))

    def _print_discovery(self):
        print("Discovery Queue")
        for key in sorted(self._opcode_discovery):
            print("{}: {}".format(key, self._opcode_discovery[key]))

    def _assign_result(self, index, ops):
        if index not in self._opcode_discovery:
            self._opcode_discovery[index] = set(ops)
        else:
            self._opcode_discovery[index] &= set(ops)

    def addr(self, a, b, c):
        self._registers[c] = self._registers[a] + self._registers[b]

    def addi(self, a, b, c):
        self._registers[c] = self._registers[a] + b

    def mulr(self, a, b, c):
        self._registers[c] = self._registers[a] * self._registers[b]

    def muli(self, a, b, c):
        self._registers[c] = self._registers[a] * b

    def banr(self, a, b, c):
        self._registers[c] = self._registers[a] & self._registers[b]

    def bani(self, a, b, c):
        self._registers[c] = self._registers[a] & b

    def borr(self, a, b, c):
        self._registers[c] = self._registers[a] | self._registers[b]

    def bori(self, a, b, c):
        self._registers[c] = self._registers[a] | b

    def setr(self, a, b, c):
        self._registers[c] = self._registers[a]

    def seti(self, a, b, c):
        self._registers[c] = a

    def gtir(self, a, b, c):
        self._registers[c] = int(a > self._registers[b])

    def gtri(self, a, b, c):
        self._registers[c] = int(self._registers[a] > b)

    def gtrr(self, a, b, c):
        self._registers[c] = int(self._registers[a] > self._registers[b])

    def eqir(self, a, b, c):
        self._registers[c] = int(a == self._registers[b])

    def eqri(self, a, b, c):
        self._registers[c] = int(self._registers[a] == b)

    def eqrr(self, a, b, c):
        self._registers[c] = int(self._registers[a] == self._registers[b])

    def execute(self, operation, a, b, c):
        self._resolved_opcodes[operation](a, b, c)

m = Machine()
with open("input_file.txt", "r") as file:
    count = 0

    line = file.readline()
    while line.startswith("Before: "):
        starting_registers = [int(entry) for entry in line.strip()[len("Before: ["):-1].split(", ")]
        operations = [int(entry) for entry in file.readline().strip().split(" ")]
        ending_registers = [int(entry) for entry in file.readline().strip()[len("After:  ["):-1].split(", ")]

        if m.test_opcode(starting_registers, operations, ending_registers) >= 3:
            count += 1

        file.readline()
        line = file.readline()
    line = file.readline()

    m.resolve_opcodes()
    m.set_registers([0,0,0,0])

    for line in file.readlines():
        operations = [int(entry) for entry in line.strip().split(" ")]
        m.execute(*operations)
    print(m.get_registers())