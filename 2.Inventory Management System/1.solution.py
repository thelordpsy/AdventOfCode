def histogram(line):
    data = {}
    for element in line:
        if element not in data:
            data[element] = 1
        else:
            data[element] = data[element] + 1

    return set(data.values())


sum_2 = 0
sum_3 = 0

with open("input_file.txt", "r") as file:
    for line in file:
        counts = histogram(line.strip())
        if 2 in counts:
            sum_2 += 1
        if 3 in counts:
            sum_3 += 1

print(sum_2 * sum_3)