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
        self.batteries = list(map(int, line))

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

def get_joltage(batteries, length):
    n_batteries = len(batteries)
    joltage = []
    for i, b in enumerate(batteries):
        start = max(0, length - n_batteries + i)
        # print(i, b, start)
        for j in range(start, length):
            if j >= len(joltage):
                joltage.append(b)
                break
            if joltage[j] < b:
                joltage[j] = b
                for k in range(j + 1, len(joltage)):
                    joltage[k] = 0

                # print('found', i, j, b, joltage)
                break
    return joltage

def get_total(inputs: List[Input], length):
    total = 0
    for input in inputs:
        # print(input.line)
        joltage = get_joltage(input.batteries, length)
        # print(joltage)
        joltage = int(''.join(map(str, joltage)))
        total += joltage
    return total

def part1(inputs: List[Input]):
    total = 0
    total = get_total(inputs, 2)
    return total

def part2(inputs: List[Input]):
    total = 0
    total = get_total(inputs, 12)
    return total

class AdventOfCode(unittest.TestCase):
    def setUp(self) -> None:
        script_dir = os.path.dirname(sys.argv[0])
        if len(script_dir) > 0:
            script_dir += '/'

        self.input_set = [
            load_input(script_dir + "example1.txt", 357, 3121910778619),
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
