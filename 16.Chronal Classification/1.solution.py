import copy

class Machine(object):
    def __init__(self):
        self._registers = [0, 0, 0, 0]
        self._op_list = [
                self.addr, self.addi,
                self.mulr, self.muli,
                self.banr, self.bani,
                self.borr, self.bori,
                self.setr, self.seti,
                self.gtir, self.gtri, self.gtrr,
                self.eqir, self.eqri, self.eqrr
            ]

        self._opcode_discovery = {}

    def set_registers(self, values):
        self._registers = copy.deepcopy(values)

    def get_registers(self):
        return copy.deepcopy(self._registers)

    def test_opcode(self, starting_value, operation, ending_value):
        index, a, b, c = operation

        possible_ops = []
        for function in self._op_list:
            self.set_registers(starting_value)
            function(a, b, c)
            if ending_value == self._registers:
                possible_ops.append(function)

        self._assign_result(index, possible_ops)
        return len(possible_ops)

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


m = Machine()
acts_like = m.test_opcode([3,2,1,1], [9,2,1,2], [3,2,2,1])
print(acts_like)

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

        
    print(count)