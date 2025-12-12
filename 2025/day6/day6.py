#!/usr/bin/env python3
import unittest
import sys
import time
import os
import re

from pprint import pprint, pformat
from typing import List

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
    def __init__(self, line: str):
        self.line = line

    def __str__(self):
        return f"<Input {pformat(self.__dict__)}>"

    __repr__ = __str__

def load_input(filename, solution_p1=None, solution_p2=None):
    try:
        with open(filename,'r') as f:
            lines = [line.rstrip('\r\n') for line in f.readlines()]
    except:
        print("No input file", filename)
        return None
    inputs = [Input(line) for line in lines]
    return (inputs, solution_p1, solution_p2)

def op_fn(op, a, b):
    if op == '+':
        return a + b
    else:
        return a * b

class WS:
    class Set:
        def __init__(self, numbers, op):
            self.numbers = numbers
            self.op = op

        def __str__(self):
            return f'{self.op} {self.numbers}'
        __repr__ = __str__

    def __init__(self, inputs: List[Input]):
        numbers = [list(map(int, i.line.split())) for i in inputs[:-1]]
        operations = inputs[-1].line.split()
        self.sets1 = [self.Set(n, op) for n, op in zip(zip(*numbers), operations)]

        # And for part 2
        longest = max([len(i.line) for i in inputs])
        equalized_lines = [i.line + (' ' * (longest - len(i.line))) for i in inputs]
        number_lines = list(map(''.join, zip(*equalized_lines)))
        self.sets2 = []
        numbers = []
        for line in number_lines:
            if line.strip() == '':
                self.sets2.append(self.Set(numbers, op))
                numbers = []
                continue

            if line[-1] != ' ':
                op = line[-1]
            numbers.append(int(line[:-1]))
        self.sets2.append(self.Set(numbers, op))

    def solve_worksheet(self, sets: List[Set]):
        total = 0
        for s in sets:
            value = s.numbers[0]
            for n in s.numbers[1:]:
                value = op_fn(s.op, value, n)
            total += value
        return total

def part1(inputs: List[Input]):
    total = 0
    ws = WS(inputs)
    # pprint(ws.sets1)
    total = ws.solve_worksheet(ws.sets1)
    return total

def part2(inputs: List[Input]):
    total = 0
    ws = WS(inputs)
    # pprint(ws.sets2)
    total = ws.solve_worksheet(ws.sets2)
    return total

class AdventOfCode(unittest.TestCase):
    def setUp(self) -> None:
        script_dir = os.path.dirname(sys.argv[0])
        if len(script_dir) > 0:
            script_dir += '/'

        self.input_set = [
            load_input(script_dir + "example1.txt", 4277556, 3263827),
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
