#!/usr/bin/env python3
import unittest
import sys
import time
import os
import re

from pprint import pprint, pformat

class TimeBlock:
    def __init__(self, description=None):
        self.description = description

    def __enter__(self):
        self.begin = time.time()

    def __exit__(self, exception_type, exception_value, traceback):
        end = time.time()
        if exception_type is not None:
            raise exception_value

        print(f"{'' if self.description is None else self.description + ' '}took {end - self.begin:.3f} sec")

class Input(object):
    def __str__(self):
        return f"<Input {pformat(self.__dict__)}>"

    __repr__ = __str__

def convert_input(line):
    input = Input()
    input.line = line
    return list(line)

def load_input(filename, solution_p1=None, solution_p2=None):
    try:
        with open(filename,'r') as f:
            lines = [line.strip() for line in f.readlines()]
    except:
        print("No input file", filename)
        return None
    inputs = [convert_input(line) for line in lines]
    return (inputs, solution_p1, solution_p2)

def print_platform(input):
    for row in input:
        print("".join(row))

def slide_rocks(line, pos):
    next_spot = pos
    for i in range(pos, len(line)):
        if line[i] == 'O':
            line[i] = '.'
            line[next_spot] = 'O'
            next_spot += 1
        elif line[i] == '#':
            slide_rocks(line, i + 1)
            return

def tilt_platform(input, direction):
    result = [[] for _ in input]
    if direction in "NS":
        if direction == "N":
            rev_func = lambda x: x
        else:
            rev_func = reversed
        for x in range(0, len(input[0])):

            # print(x)
            line = [row[x] for row in rev_func(input)]
            slide_rocks(line, 0)
            # print(line)
            # for y, c in enumerate(rev_func(line)):
            #     input[y] = list(input[y])
            #     input[y][x] = c
            #     input[y] = tuple(input[y])
            for y, c in enumerate(rev_func(line)):
                result[y].append(c)

    else:
        if direction == "W":
            rev_func = lambda x: x
        else:
            rev_func = reversed
        for y in range(0, len(input[0])):
            # print(y)
            # print(input[y])
            line = list(rev_func(input[y]))
            slide_rocks(line, 0)
            result[y] = tuple(rev_func(line))
            # print(input[y])
    return tuple(map(tuple, result))


def calculate_load(input):
    max_load = len(input)
    total = 0
    for y, row in enumerate(input):
        load = max_load - y
        # print(y, row, load)
        total += load * sum([1 for c in row if c == 'O'])

    return total


def part1(input):
    total = 0
    input = tuple(map(tuple, input))
    # print_platform(input)
    input = tilt_platform(input, 'N')
    # print_platform(input)
    total = calculate_load(input)
    return total

def part2(input):
    total = 0
    input = tuple(map(tuple, input))
    # print_platform(input)
    cache = {}
    iterations = 1000000000
    for i in range(iterations):
        if input in cache:
            next, prev_i = cache[input]
            break

        next = input
        for direction in "NWSE":
            next = tilt_platform(next, direction)
            # print_platform(input)
        cache[input] = (next, i)
        input = next
    cycle = i - prev_i
    left = iterations - (i + 1)

    # print("found", i, prev_i, cycle, left)
    left = left % cycle
    # print("mod", left)
    for _ in range(left):
        next, prev_i = cache[next]
        # print_platform(next)
        # print("sum", calculate_load(next))



    total = calculate_load(next)
    return total

class AdventOfCode(unittest.TestCase):
    def setUp(self) -> None:
        script_dir = os.path.dirname(sys.argv[0])
        if len(script_dir) > 0:
            script_dir += '/'

        self.input_set = [
            load_input(script_dir + "example1.txt", 136, 64),
            load_input(script_dir + "input1.txt"),
        ]

    def run_part(self, part_num, part_func):
        self.assertIn(part_num, [1, 2])
        for input_set in self.input_set:
            self.assertIsNotNone(input_set)
            expect = input_set[part_num]
            answer = part_func(input_set[0])
            print(f"Part{part_num} result", answer)
            if expect is not None:
                self.assertEqual(expect, answer)

    def test_part1(self):
        self.run_part(1, part1)

    def test_part2(self):
        self.run_part(2, part2)

unittest.main(verbosity=0)
