import unittest
import sys
import os
import re

from pprint import pprint, pformat

class Input(object):
    def __str__(self):
        return f"<Input {pformat(self.__dict__)}>"

    __repr__ = __str__

def convert_input(line):
    input = Input()
    input.vals = list(map(int, line.split()))
    return input

def load_input(filename, solution_p1=None, solution_p2=None):
    try:
        with open(filename,'r') as f:
            lines = [line.strip() for line in f.readlines()]
    except:
        print("No input file", filename)
        return None
    inputs = [convert_input(line) for line in lines]
    return (inputs, solution_p1, solution_p2)

def derive(vals):
    val = None
    result = []
    for val2 in vals:
        if val is not None:
            result.append(val2 - val)
        val = val2
    return result

def find_next(vals):
    for val in vals:
        if val != 0:
            derived = derive(vals)
            return vals[-1] + find_next(derived)
    return 0

def part1(input):
    total = 0
    for history in input:
        total += find_next(history.vals)

    return total

def find_prev(vals):
    for val in vals:
        if val != 0:
            derived = derive(vals)
            return vals[0] - find_prev(derived)
    return 0

def part2(input):
    total = 0
    for history in input:
        total += find_prev(history.vals)
    return total

class AdventOfCode(unittest.TestCase):
    def setUp(self) -> None:
        script_dir = os.path.dirname(sys.argv[0])
        if len(script_dir) > 0:
            script_dir += '/'

        self.input_set = [
            load_input(script_dir + "example1.txt", 114, 2),
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
