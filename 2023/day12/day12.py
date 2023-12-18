#!/usr/bin/env python3
import unittest
import sys
import time
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
    input.springs, groups = line.split()
    input.groups = list(map(int, groups.split(',')))
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

def resolve_known(row):
    min_len = sum(row.groups) + len(row.groups) - 1
    left = len(row.springs) - min_len
    group1 = row.groups[0]
    next_row = Input()
    next_row.groups = row.groups[1:]
    total = 0
    for shift in range(left + 1):
        # print(f'{str(row.groups):10} {row.springs[shift:]:20} min {min_len} left {left} shift {shift}')
        if '.' in row.springs[shift: shift + group1]:
            # print('skip operational')
            continue
        if shift + group1 < len(row.springs) and '#' in row.springs[shift + group1]:
            # print('skip broken')
            continue
        if shift >= 1 and '#' in row.springs[:shift]:
            # print('skip broken before')
            break

        if len(next_row.groups) > 0:
            next_row.springs = row.springs[group1 + shift + 1:]
            total += resolve_known(next_row)
        elif "#" in row.springs[group1 + shift + 1:]:
            # print("skip broken to far ahead")
            pass
        else:
            total += 1
            # print('works')
    return total

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

def part1(input):
    total = 0
    for i, row in enumerate(input):
        # print(row.line)
        # with TimeBlock(f'Row {i}'):
        row_total = resolve_known(row)
        # print('row total', row_total)
        total += row_total
        # print('Row', i, row_total, row.springs, row.groups)
    return total


def unfold(row):
    row.groups = row.groups * 5
    row.springs = (("?" + row.springs) * 5)[1:]
    return row

def resolve_known2(cache, row):
    key = (len(row.groups), len(row.springs))
    if key in cache:
        return cache[key]
    min_len = sum(row.groups) + len(row.groups) - 1
    left = len(row.springs) - min_len
    group1 = row.groups[0]
    next_row = Input()
    next_row.groups = row.groups[1:]
    total = 0
    for shift in range(left + 1):
        # print(f'{str(row.groups):10} {row.springs[shift:]:20} min {min_len} left {left} shift {shift}')
        if '.' in row.springs[shift: shift + group1]:
            # print('skip operational')
            continue
        if shift + group1 < len(row.springs) and '#' in row.springs[shift + group1]:
            # print('skip broken')
            continue
        if shift >= 1 and '#' in row.springs[:shift]:
            # print('skip broken before')
            break

        if len(next_row.groups) > 0:
            next_row.springs = row.springs[group1 + shift + 1:]
            total += resolve_known2(cache, next_row)
        elif "#" in row.springs[group1 + shift + 1:]:
            # print("skip broken to far ahead")
            pass
        else:
            total += 1
            # print('works')

    cache[key] = total
    return total


def part2(input):
    total = 0
    for i, row in enumerate(input):
        pass
        cache = {}
        row = unfold(row)
        # with TimeBlock(f'Row {i}'):
        row_total = resolve_known2(cache, row)
        # print('row total', row_total)
        total += row_total
        # print('Row', i, 'cache', len(cache), row_total, row.springs, row.groups)
        # pprint(sorted(cache.items()))
    return total

class AdventOfCode(unittest.TestCase):
    def setUp(self) -> None:
        script_dir = os.path.dirname(sys.argv[0])
        if len(script_dir) > 0:
            script_dir += '/'

        self.input_set = [
            load_input(script_dir + "example1.txt", 21, 525152),
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
