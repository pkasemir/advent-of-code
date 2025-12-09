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
    input.mult = 1 if line[0] == 'R' else -1
    input.amount = int(line[1:])
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

def part1(inputs):
    total = 0
    dial = 50
    for input in inputs:
        dial += input.amount * input.mult
        dial %= 100
        # print(input, dial)
        if dial == 0:
            total += 1
    return total

def part2(inputs):
    total = 0
    dial = 50
    for input in inputs:
        # print(input, dial)
        old_dial = dial
        dial += input.amount * input.mult
        if input.mult == 1:
            times = dial // 100
        else:
            if dial > 0:
                times = 0
            else:
                times = (-dial) // 100
                if old_dial > 0:
                    times += 1
        # print(dial, times)
        total += times
        dial %= 100
    return total

class AdventOfCode(unittest.TestCase):
    def setUp(self) -> None:
        script_dir = os.path.dirname(sys.argv[0])
        if len(script_dir) > 0:
            script_dir += '/'

        self.input_set = [
            load_input(script_dir + "example1.txt", 3, 6),
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
