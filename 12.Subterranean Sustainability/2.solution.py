import copy
import collections

def char_to_state(char):
    if char == "#":
        return True
    return False

def state_to_char(state):
    if state:
        return "#"
    return '.'

class PlantState(object):
    def __init__(self):
        self._state = None
        self._left_index = None

    def init_from_line(self, line):
        self._left_index = 0
        line = line[len("initial state: "):].strip()
        self._state = collections.deque([char_to_state(char) for char in line])
        self._resize_state()
        #self._print_state()

    def init_from_state(self, left_index, state):
        self._left_index = left_index
        self._state = state
        self._resize_state()
        #self._print_state()

    def derive_new_state(self, rules):
        new_state = collections.deque()
        
        state_circle = collections.deque()
        for value in self._state:
            state_circle.append(value)
            if len(state_circle) < 5:
                continue
            if len(state_circle) > 5:
                state_circle.popleft()
            new_state.append(rules.apply(state_circle))

        result = PlantState()
        result.init_from_state(self._left_index + 2, new_state)
        return result

    def evaluate(self):
        total = 0
        for i in range(len(self._state)):
            if self._state[i]:
                total += (i + self._left_index)
        return total

    def _resize_state(self):
        __EDGE_WIDTH = 4

        leftmost_true = None
        for i in range(len(self._state)):
            if self._state[i]:
                leftmost_true = i
                break

        if leftmost_true > __EDGE_WIDTH:
            left_shift_amount = leftmost_true - __EDGE_WIDTH
            for j in range(left_shift_amount):
                del self._state[i]
            self._left_index += left_shift_amount
        elif leftmost_true < __EDGE_WIDTH:
            right_shift_amount = __EDGE_WIDTH - leftmost_true
            for j in range(right_shift_amount):
                self._state.insert(0, False)
            self._left_index -= right_shift_amount

        while not self._state[-1]:
            del self._state[-1]
        [self._state.append(False) for j in range(__EDGE_WIDTH)]

    def _print_state(self):
        print("".join([state_to_char(state) for state in self._state]))

class RuleNode(object):
    def __init__(self):
        self._data = None
        self._child_true = None
        self._child_false = None

    def child(self, state):
        if state:
            if self._child_true is None:
                self._child_true = RuleNode()
            return self._child_true

        if self._child_false is None:
            self._child_false = RuleNode()
        return self._child_false

    def data(self):
        return self._data

    def set_data(self, data):
        self._data = data

    def print_children(self, path):
        if self._child_true:
            self._child_true.print_children(copy.deepcopy(path) + [True])
        if self._child_false:
            self._child_false.print_children(copy.deepcopy(path) + [False])
        if self._data is not None:
            print("{} -> {}".format("".join([state_to_char(state) for state in path]), state_to_char(self._data)))

class RuleTree(object):
    def __init__(self):
        self._root = RuleNode()

    def add_rule(self, line):
        line = line.strip()
        state = line[0:5]
        result = line[-1]

        node = self._root
        for state_entry in state:
            node = node.child(char_to_state(state_entry))
        node.set_data(char_to_state(result))

    def apply(self, states):
        node = self._root
        for state in states:
            node = node.child(state)

        assert(node.data() != None)
        return node.data()


    def print_tree(self):
        self._root.print_children([])


with open("input_file.txt", "r") as file:
    state = PlantState()
    state.init_from_line(file.readline())
    file.readline() # Throw one away
    rules = RuleTree()
    [rules.add_rule(line) for line in file.readlines()]

for i in range(1000):
    state = state.derive_new_state(rules)
one_k = state.evaluate()

for i in range(1000):
    state = state.derive_new_state(rules)
two_k = state.evaluate()

for i in range(1000):
    state = state.derive_new_state(rules)
three_k = state.evaluate()


# It should be growing linearly by now
assert(three_k - two_k == two_k - one_k)


rate_per_thousand = two_k - one_k # Rate
starting_value = one_k - rate_per_thousand

result = starting_value + (rate_per_thousand * (50000000000/1000))
print(int(result))