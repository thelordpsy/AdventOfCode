import string

def flip_case(char):
    if char.isupper():
        return char.lower()
    return char.upper()


class PolymerStack(object):
    def __init__(self, to_delete=None):
        self._backing = []
        self._to_delete = to_delete

    def push(self, char):
        if self._to_delete != None and self._to_delete.lower() == char.lower():
            return

        if len(self._backing) != 0:
            if self._backing[-1] == flip_case(char):
                del self._backing[-1]
                return

        self._backing += char

    def __iadd__(self, char):
        self.push(char)
        return self

    def __str__(self):
        return "".join(self._backing)

def execute_test(to_delete):
    stack = PolymerStack(to_delete=to_delete)
    with open("input_file.txt") as file:
        char = file.read(1)
        while char:
            stack += char
            char = file.read(1)
    return len(str(stack))


best = None
for char in string.ascii_lowercase:
    this_run = execute_test(char)
    if best == None or this_run < best:
        best = this_run

print(best)