#!/usr/bin/env python3
import re

class Input(object):
    pass

def convert_input(line):
    input = Input()
    input.line = line
    input.numbers = list(re.finditer("[0-9]+", line))
    # print(input.numbers)
    input.symbols = list(re.finditer("[^.0-9]", line))
    # print(input.symbols)
    
    return input

def append_input(inputs, filename, solution=None):
    try:
        with open(filename,'r') as f:
            lines = [line.strip() for line in f.readlines()]
    except:
        print("No input file", filename)
        return
    lines = [convert_input(line) for line in lines]
    inputs.append((lines, solution))

inputs = []

append_input(inputs, "example1.txt", 4361)
append_input(inputs, "input1.txt")
# print(inputs)


bag = dict(red=12, green=13, blue=14)

def check_y(numbers: list, symbol: re.Match, row):
    # print(" check y", numbers, symbol)
    total = 0
    found = []
    for number in numbers:
        for x_try in [v + symbol.start() for v in range(-1, 2)]:
            if x_try < 0 or x_try >= len(row.line):
                continue
            # print("try y", x_try, number.start(), number.end())
            if x_try >= number.start() and x_try < number.end():
                val = int(number.group())
                # print("found y", val)
                found.append(number)
                total += val
                # numbers.remove(number)
                break
    for number in found:
        numbers.remove(number)
    # print("check total", total)
    return total

def check_x(numbers: list, symbol: re.Match, row):
    # print(" check x", numbers, symbol)
    total = 0
    found = []
    for num_idx, number in enumerate(numbers):
        if number.end() == symbol.start() or number.start() == symbol.end():
            val = int(number.group())
            # print("found x", val)

            found.append(number)
            total += val
    for number in found:
        numbers.remove(number)
    # print("check total", total)
    return total


for input, solution in inputs:
    total = 0
    for y, row in enumerate(input):
        for symbol in row.symbols:
            # print (y, symbol)
            if y >= 1:
                total += check_y(input[y - 1].numbers, symbol, row)
            if y < len(input) - 1:
                total += check_y(input[y + 1].numbers, symbol, row)
            total += check_x(row.numbers, symbol, row)
    
    result = f"total {total}"
    if solution is not None:
        result += " " + ("matches" if solution == total else "not right")

    print(result)

inputs = []

append_input(inputs, "example1.txt", 467835)
append_input(inputs, "input1.txt")

bag = dict(red=12, green=13, blue=14)

def check_y(numbers: list, symbol: re.Match, row):
    # print(" check y", numbers, symbol)
    found = []
    for number in numbers:
        for x_try in [v + symbol.start() for v in range(-1, 2)]:
            if x_try < 0 or x_try >= len(row.line):
                continue
            # print("try y", x_try, number.start(), number.end())
            if x_try >= number.start() and x_try < number.end():
                val = int(number.group())
                # print("found y", val)
                found.append(val)
                # numbers.remove(number)
                break
    return found

def check_x(numbers: list, symbol: re.Match, row):
    # print(" check x", numbers, symbol)
    found = []
    for num_idx, number in enumerate(numbers):
        if number.end() == symbol.start() or number.start() == symbol.end():
            val = int(number.group())
            # print("found x", val)

            found.append(val)
    return found


for input, solution in inputs:
    total = 0
    for y, row in enumerate(input):
        for symbol in row.symbols:
            if symbol.group() != '*':
                continue
            # print (y, symbol)
            numbers = []
            if y >= 1:
                numbers.extend(check_y(input[y - 1].numbers, symbol, row))
            if y < len(input) - 1:
                numbers.extend(check_y(input[y + 1].numbers, symbol, row))
            numbers.extend(check_x(row.numbers, symbol, row))
            if len(numbers) == 2:
                # print("found 2 gear")
                total += numbers[0] * numbers[1]
    
    result = f"total {total}"
    if solution is not None:
        result += " " + ("matches" if solution == total else "not right")

    print(result)
