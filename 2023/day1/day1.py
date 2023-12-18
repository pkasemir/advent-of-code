#!/usr/bin/env python3
import re

def append_input(inputs, filename, solution=None):
    try:
        with open(filename,'r') as f:
            inputs.append((f.read(), solution))
    except:
        print("No input file", filename)

inputs = []

append_input(inputs, "example1.txt", 142)
append_input(inputs, "input1.txt")

def convert(line):
    digits = re.sub("[^0-9]", "", line)
    digits = digits[0] + digits[-1]
    return int(digits)


for input, solution in inputs:
    # print(input, solution)
    lines = input.splitlines()
    # print(lines)
    vals = [convert(line) for line in lines]
    total = sum(vals)
    # print(vals)
    print(sum(vals))
    if solution is not None:
        print("solution", solution, "matches" if solution == total else "not right", total)



inputs = []

append_input(inputs, "example2.txt", 281)
append_input(inputs, "input2.txt")

numbers = "zero one two three four five six seven eight nine".split()
numbers_rev = [n[::-1] for n in numbers]
numbers_re = "|".join(numbers)
numbers_rev_re = "|".join(numbers_rev)

numbers_dict = {n: i for i,n in enumerate(numbers)}
numbers_rev_dict = {n: i for i,n in enumerate(numbers_rev)}
for i in range(10):
    numbers_dict[str(i)] = i
    numbers_rev_dict[str(i)] = i

def convert(line):
    output = ""
    skip = 0
    m1 = re.search("[0-9]|"+numbers_re, line)
    # print(m1)
    m2 = re.search("[0-9]|"+numbers_rev_re, line[::-1])
    # print(m2)
    val = numbers_dict[m1.group()] *10 + numbers_rev_dict[m2.group()]
    # print(val)
    return val

for input, solution in inputs:
    # print(input, solution)
    lines = input.splitlines()
    # print(lines)
    vals = [convert(line) for line in lines]
    total = sum(vals)
    # print(vals)
    print(sum(vals))
    if solution is not None:
        print("solution", solution, "matches" if solution == total else "not right", total)
