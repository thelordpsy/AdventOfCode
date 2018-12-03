with open("input_file.txt", "r") as file:
    print(sum([int(line) for line in file.readlines()]))
