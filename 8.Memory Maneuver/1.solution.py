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

    def __str__(self):
        return "{}/{}".format(self._child_count, self._data_count)

def walk_tree_deep(tree, start, function):
    value = start
    for child in tree._children:
        value = walk_tree_deep(child, value, function)

    for data in tree._data:
        value = function(value, data)

    return value

with open("input_file.txt") as file:
    data = [int(entry) for entry in file.read().split(' ')]


node = TreeNode(data)
print(walk_tree_deep(node, 0, lambda x, y: x+y))