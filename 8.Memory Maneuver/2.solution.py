def consume(data):
    entry = data[0]
    del data[0]
    return entry

class TreeNode(object):
    def __init__(self, data):
        self._child_count = consume(data)
        self._data_count = consume(data)
        self._children = [TreeNode(data) for i in range(self._child_count)]
        self._data = [consume(data) for i in range(self._data_count)]

    def evaluate(self):
        if self._child_count == 0:
            return sum(self._data)

        return sum([self._children[value - 1].evaluate() for value in self._data
                        if value != 0 and value <= self._child_count])

with open("input_file.txt") as file:
    data = [int(entry) for entry in file.read().split(' ')]

node = TreeNode(data)
print(node.evaluate())