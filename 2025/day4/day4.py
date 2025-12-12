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
    def __init__(self, line):
        self.line = line

    def __str__(self):
        return f"<Input {pformat(self.__dict__)}>"

    __repr__ = __str__

def load_input(filename, solution_p1=None, solution_p2=None):
    try:
        with open(filename,'r') as f:
            lines = [line.strip() for line in f.readlines()]
    except:
        print("No input file", filename)
        return None
    inputs = [Input(line) for line in lines]
    return (inputs, solution_p1, solution_p2)

class Grid:
    def __init__(self, inputs: List[Input]):
        self.g = [list(i.line) for i in inputs]
        self.rows = len(self.g)
        self.cols = len(self.g[0])

    def __str__(self):
        return '\n'.join([''.join(row) for row in self.g])

    def get_adjecent_count(self, row, col):
        count = 0
        for r_diff in range(-1, 2):
            test_row = row + r_diff
            if not (0 <= test_row < self.rows):
                continue
            for c_diff in range(-1, 2):
                if r_diff == 0 and c_diff == 0:
                    continue
                test_col = col + c_diff
                if not (0 <= test_col < self.cols):
                    continue
                if self.g[test_row][test_col] != '.':
                    count += 1
        return count

    def get_accessible(self):
        total = 0
        for row in range(self.rows):
            for col in range(self.cols):
                #  self.g[row][col] = str(row)[-1]
                if self.g[row][col] == '.':
                    continue
                count = self.get_adjecent_count(row, col)
                if count < 4:
                    self.g[row][col] = 'x' # str(count)
                    total += 1

        # print(self)
        return total

    def remove_x(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.g[row][col] == 'x':
                    self.g[row][col] = '.'

def part1(inputs: List[Input]):
    total = 0
    grid = Grid(inputs)
    total = grid.get_accessible()
    return total

def part2(inputs: List[Input]):
    total = 0
    grid = Grid(inputs)
    to_remove = None
    while to_remove != 0:
        to_remove = grid.get_accessible()
        grid.remove_x()
        total += to_remove

    return total

class AdventOfCode(unittest.TestCase):
    def setUp(self) -> None:
        script_dir = os.path.dirname(sys.argv[0])
        if len(script_dir) > 0:
            script_dir += '/'

        self.input_set = [
            load_input(script_dir + "example1.txt", 13, 43),
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
