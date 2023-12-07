import unittest
import sys
import os
import re

from pprint import pprint

class Input(object):
    pass

    def __iter__(self):
        return self.values.__iter__()

def convert_input(line):
    input = Input()
    input.line = line
    input.values = list(map(int, line.split(':')[1].split()))
    input.values2 = int(line.split(':')[1].replace(' ', ''))
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

def part1(input):
    total = 1
    for t, record in zip(*input):
        options = 0
        for hold in range(t):
            left = t - hold
            distance = left * hold
            # print(hold, distance)
            if distance > record:
                options += 1
        total *= options

    return total

def part2(input):
    total = 1
    t = input[0].values2
    record = input[1].values2
    options = 0
    for hold in range(t):
        left = t - hold
        distance = left * hold
        # print(hold, distance)
        if distance > record:
            options += 1
    total *= options
    return total

class AdventOfCode(unittest.TestCase):
    def setUp(self) -> None:
        script_dir = os.path.dirname(sys.argv[0])
        if len(script_dir) > 0:
            script_dir += '/'

        self.input_set = [
            load_input(script_dir + "example1.txt", 288, 71503),
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
