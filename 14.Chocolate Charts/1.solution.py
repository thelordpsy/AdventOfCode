state = [3,7]
elf_1 = 0
elf_2 = 1

def advance():
    global state
    global elf_1
    global elf_2

    total = state[elf_1] + state[elf_2]
    new_values = []

    if total == 0:
        new_values.append(0)
    else:
        while total > 0:
            new_values.append(total % 10)
            total = int(total / 10)
    new_values.reverse()
    state += new_values

    elf_1 = (elf_1 + state[elf_1] + 1) % len(state)
    elf_2 = (elf_2 + state[elf_2] + 1) % len(state)


def print_answer(value):
    while len(state) < (value + 10):
        advance()
    answer = "".join([str(obj) for obj in state[value:value+10]])
    print("{}: {}".format(value, answer))

print_answer(9) # 5158916779
print_answer(5) # 0124515891
print_answer(18) # 9251071085
print_answer(2018) # 5941429882

with open("input_file.txt", "r") as file:
    print_answer(int(file.read()))