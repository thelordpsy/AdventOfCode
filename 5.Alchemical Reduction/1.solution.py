def flip_case(char):
    if char.isupper():
        return char.lower()
    return char.upper()


class PolymerStack(object):
    def __init__(self):
        self._backing = []

    def push(self, char):
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


stack = PolymerStack()
with open("input_file.txt") as file:
    char = file.read(1)
    while char:
        stack += char
        char = file.read(1)

print(len(str(stack)))