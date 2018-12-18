def advance(state, elf_1, elf_2):
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
    return state, elf_1, elf_2

def test(big_list, starting_point, small_list):
    for i in range(len(small_list)):
        if big_list[starting_point + i] != small_list[i]:
            return False
    return True


def print_answer(value):
    state = [3,7]
    elf_1 = 0
    elf_2 = 1

    last_sought = 0
    while True:
        state, elf_1, elf_2 = advance(state, elf_1, elf_2)
        while last_sought < (len(state) - 5):
            if test(state, last_sought, value):
                print("{}: {}".format(value, last_sought))
                return
            last_sought += 1
    

print_answer([5,1,5,8,9]) # 9
print_answer([0,1,2,4,5]) # 5
print_answer([9,2,5,1,0]) # 18
print_answer([5,9,4,1,4]) # 2018

# Grab a drink
with open("input_file.txt", "r") as file:
    print_answer([int(char) for char in file.read().strip()])