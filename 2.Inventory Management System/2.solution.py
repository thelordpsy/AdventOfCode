def single_difference(left, right):
    difference_count = 0
    for i in range(len(left)):
        if left[i] != right[i]:
            difference_count += 1
            if difference_count > 1:
                return False

    if difference_count == 1:
        return True

    assert("Duplicate string found?")

def morph(left, right):
    output = ""
    for i in range(len(left)):
        if left[i] == right[i]:
            output += left[i]
    return output


with open("input_file.txt", "r") as file:
    lines = [line.strip() for line in file.readlines()]

for i in range(len(lines)):
    for j in range(len(lines) - i - 1):
        if single_difference(lines[i], lines[i+j]):
            print(morph(lines[i], lines[i+j]))