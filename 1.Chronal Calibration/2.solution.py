current = 0
history = {}
history[current] = True

def recycle_list(lst):
    index = 0
    while True:
        yield lst[index]
        index += 1
        if index >= len(lst):
            index = 0

with open("input_file.txt", "r") as file:
    for value in recycle_list([int(line) for line in file.readlines()]):
        current = current + value
        if current in history:
            print(current)
            exit(0)
        history[current] = True