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

class DB:
    def __init__(self, inputs: List[Input]):
        self.ranges = []
        self.ids = []
        on_ranges = True
        for input in inputs:
            if on_ranges:
                if input.line == '':
                    on_ranges = False
                    continue
                self.ranges.append(list(map(int, input.line.split('-'))))
            else:
                self.ids.append(int(input.line))

    def is_fresh(self, num):
        for low, high in self.ranges:
            if low <= num <= high:
                return True
        return False

    def count_fresh(self):
        return sum([1 for n in self.ids if self.is_fresh(n)])

    def count_fresh2(self):
        m_ranges = []
        sorted_ranges = sorted(self.ranges, key=lambda r: r[0])
        for low, high in sorted_ranges:
            # print(low, high)
            if len(m_ranges) > 0:
                m_low, m_high = m_ranges[-1]
                # check if new range in or adjacent to merged range
                if m_low <= low <= (m_high + 1):
                    m_ranges[-1][1] = max(high, m_high)
                    continue
            # must be the last one
            m_ranges.append([low, high])
        # pprint(m_ranges)
        total = 0
        for low, high in m_ranges:
            total += high - low + 1
        return total



def part1(inputs: List[Input]):
    total = 0
    db = DB(inputs)
    # pprint(db.ranges)
    # pprint(db.ids)
    total = db.count_fresh()
    return total

def part2(inputs: List[Input]):
    total = 0
    db = DB(inputs)
    total = db.count_fresh2()
    # return 14
    return total

class AdventOfCode(unittest.TestCase):
    def setUp(self) -> None:
        script_dir = os.path.dirname(sys.argv[0])
        if len(script_dir) > 0:
            script_dir += '/'

        self.input_set = [
            load_input(script_dir + "example1.txt", 3, 14),
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
