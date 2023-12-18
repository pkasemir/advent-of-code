#!/usr/bin/env python3
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

def get_empty_space(input):
    empty_cols = []
    for x in range(len(input[0])):
        empty = True
        for y in range(len(input)):
            if input[y][x] == '#':
                empty = False
                break
        if empty:
            empty_cols.append(x)
    # print(empty_cols)

    empty_rows = []
    for y, row in enumerate(input):
        if '#' not in row:
            empty_rows.append(y)
    # print(empty_rows)
    return empty_cols, empty_rows

def expand_galaxy(input):
    empty_cols, empty_rows = get_empty_space(input)
    for x in reversed(empty_cols):
        for y in range(len(input)):
            input[y].insert(x, '.')
    for y in reversed(empty_rows):
        input.insert(y, '.' * len(input[0]))
    return input

def print_galaxy(input):
    print(f"Galaxy {len(input[0])} x {len(input)}")
    for row in input:
        print("".join(row))

def get_galaxy_list(input):
    galaxies = []
    for y, row in enumerate(input):
        x_list = list(re.finditer('#', "".join(row)))
        galaxies.extend([(x.start(), y) for x in x_list])

    return galaxies

def sum_galaxy_distance(galaxies):
    pair = 0
    total = 0
    for idx1, (x1, y1) in enumerate(galaxies):
            for idx2, (x2, y2) in enumerate(galaxies[idx1 + 1:]):
                pair += 1
                distance = abs(x1 - x2) + abs(y1 - y2)
                # print(pair, idx1, (x1, y1), (x2, y2), distance)
                total += distance
    return total

def part1(input):
    total = 0
    # print_galaxy(input)
    input = expand_galaxy(input)
    # print_galaxy(input)
    galaxies = get_galaxy_list(input)
    total = sum_galaxy_distance(galaxies)
    return total

def count_empty(v1, v2, empty_list):
    if v1 == v2:
        return 0
    if v1 > v2:
        v1, v2 = v2, v1 # swap
    count = 0
    for empty in empty_list:
        if empty > v1 and empty < v2:
            count += 1
    return count

def sum_galaxy_distance2(galaxies, scaling, empty_cols, empty_rows):
    pair = 0
    total = 0
    for idx1, (x1, y1) in enumerate(galaxies):
            for idx2, (x2, y2) in enumerate(galaxies[idx1 + 1:]):
                pair += 1
                distance = abs(x1 - x2) + abs(y1 - y2)
                distance += (scaling - 1) * (count_empty(x1, x2, empty_cols))
                distance += (scaling - 1) * (count_empty(y1, y2, empty_rows))
                # print(pair, idx1, (x1, y1), (x2, y2), distance)
                total += distance
    return total

def part2(input):
    total = 0
    empty_cols, empty_rows = get_empty_space(input)
    galaxies = get_galaxy_list(input)

    total = [sum_galaxy_distance2(galaxies, scaling, empty_cols, empty_rows) for scaling in [10, 100]]

    scaling = 2
    final = sum_galaxy_distance2(galaxies, scaling, empty_cols, empty_rows)
    print(f"Part2 scaling {scaling}:", final)

    scaling = 1000000
    final = sum_galaxy_distance2(galaxies, scaling, empty_cols, empty_rows)
    print(f"Part2 scaling {scaling}:", final)
    return total

class AdventOfCode(unittest.TestCase):
    def setUp(self) -> None:
        script_dir = os.path.dirname(sys.argv[0])
        if len(script_dir) > 0:
            script_dir += '/'

        self.input_set = [
            load_input(script_dir + "example1.txt", 374, [1030, 8410]),
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
