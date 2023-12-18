#!/usr/bin/env python3
import unittest
import sys
import os
import re
import math

from pprint import pprint, pformat

class Input(object):
    def __str__(self):
        return f"<Input {pformat(self.__dict__)}>"

    __repr__ = __str__

def convert_input(line):
    input = Input()
    input.line = line
    if '=' in line:
        line = re.sub("[ ()]", "", line)
        input.key, pair = line.split('=')
        input.value = pair.split(',')
    else:
        input.turns = [0 if c == 'L' else 1 for c in line]
    # print(input)
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
    total = 0
    turns = input[0].turns
    the_map = {i.key: i.value for i in input[2:]}
    # pprint (the_map)
    current = 'AAA'
    while True:
        for turn in turns:
            if current == 'ZZZ':
                break
            current = the_map[current][turn]
            total += 1
        if current == 'ZZZ':
            break
    return total

def part2(input):
    total = 0
    turns = input[0].turns
    the_map = {i.key: i.value for i in input[2:]}
    current_list = [k for k in the_map.keys() if k[2] == "A"]
    cycle_list = [None for i in current_list]

    # pprint (the_map)
    while None in cycle_list:
        for turn in turns:
            # print(total, current_list)
            foundz = False
            for idx, current in enumerate(current_list):
                if current[2] == 'Z':
                    foundz = True
                    if cycle_list[idx] is None:
                        cycle_list[idx] = total
            # if foundz:
            #     print(total, current_list, cycle_list)
            for idx, current in enumerate(current_list):
                current_list[idx] = the_map[current][turn]
            total += 1
    # print(cycle_list)

    return math.lcm(*cycle_list)

class AdventOfCode(unittest.TestCase):
    def setUp(self) -> None:
        script_dir = os.path.dirname(sys.argv[0])
        if len(script_dir) > 0:
            script_dir += '/'

        self.input_set = [
            load_input(script_dir + "example1.txt", 2, -1),
            load_input(script_dir + "example2.txt", 6, -1),
            load_input(script_dir + "example3.txt", -1, 6),
            load_input(script_dir + "input1.txt"),
        ]

    def run_part(self, part_num, part_func):
        self.assertIn(part_num, [1, 2])
        for input_set in self.input_set:
            self.assertIsNotNone(input_set)
            expect = input_set[part_num]
            if expect == -1:
                continue
            answer = part_func(input_set[0])
            print(f"Part{part_num} result", answer)
            if expect is not None:
                self.assertEqual(expect, answer)

    def test_part1(self):
        self.run_part(1, part1)

    def test_part2(self):
        self.run_part(2, part2)

unittest.main(verbosity=0)
