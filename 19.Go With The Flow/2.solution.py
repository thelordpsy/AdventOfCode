import copy
import math

class Instruction(object):
    def __init__(self, line):
        parts = line.split()
        self._op = parts[0]
        self._args = [int(part) for part in parts[1:]]

    @property
    def op(self):
        return self._op
    
    @property
    def args(self):
        return self._args

    def __str__(self):
        return "{} {}".format(self.op, " ".join([str(arg) for arg in self.args]))

    def __repr__(self):
        return str(self)
    

class Machine(object):
    def __init__(self):
        self._ip = 0
        self._ip_register = None
        self._instructions = []
        self._registers = [0] * 6
        self._opcodes = {
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

    def set_ip_register(self, register):
        self._ip_register = register

    def add_instruction(self, instruction):
        self._instructions.append(instruction)

    def set_registers(self, values):
        assert(len(values) == 6)
        self._registers = copy.deepcopy(values)

    def state(self):
        return "{} IP={}".format(self._registers, self._ip)

    def execute(self):
        self._registers[self._ip_register] = self._ip
        # state = self.state()
        instruction = self._instructions[self._ip]
        # state += " " + str(instruction)
        self._opcodes[instruction.op](*instruction.args)
        # state += " " + str(self._registers)
        # print(state)
        self._ip = self._registers[self._ip_register] + 1
        return self._ip >= 0 and self._ip < len(self._instructions)

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
with open("input_file.txt", "r") as file:
    m.set_ip_register(int(file.readline()[len("#ip ")]))
    for line in file:
        m.add_instruction(Instruction(line))

m.set_registers([1,0,0,0,0,0])
while m._ip != 1:
    m.execute()

target = 10551377
total = 0
for i in range(1, int(math.sqrt(target)) + 1):
    if target / i == int(target/i):
        total += (i + target/i)

print(int(total))