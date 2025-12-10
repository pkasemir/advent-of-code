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
    input.range_str = [r.split('-') for r in line.split(',')]
    input.range_int = [tuple(map(int, r.split('-'))) for r in line.split(',')]
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

def get_sum(a, b):
    return (b - a + 1) * (a + b) // 2

def get_half_number(num_str, go_down):
    down = -1 if go_down else 0
    if len(num_str) & 1 == 1:
        num = 10 ** (len(num_str) + down) + down
        num_str = str(num)
        # print('num is odd move to', num_str)
    else:
        num = int(num_str)
        

    length_div = 10 ** (len(num_str) // 2)
    left_int = num // length_div
    right_int = num % length_div
    # print('num left/right', num, left_int, right_int)
    if go_down:
        if left_int > right_int:
            left_int -= 1
    else:
        if left_int < right_int:
            left_int += 1
    right_int = left_int
    num = left_int * length_div + right_int
    # print('num left/right', "down" if go_down else "up", num, left_int, right_int)
    return left_int

def part1(inputs):
    total = 0

    for (a_str, b_str), (a_int, b_int) in zip(inputs[0].range_str, inputs[0].range_int):
        # print(a_str, b_str, len(b_str), b_int- a_int)
        a_num = get_half_number(a_str, False)
        b_num = get_half_number(b_str, True)
        b_str = str(b_num)
        while True:          
            length = len(str(a_num))
            length_mult = 10 ** length
            if a_num > b_num:
                # print('a is more than b')
                break
            if length < len(b_str):
                a_end = 10 ** length - 1
            else:
                a_end = b_num
            value = get_sum(a_num, a_end)
            value = value + value * length_mult
            # print('value', value)
            total += value
            a_num = length_mult
            # print('updating length to', length + 1, a_num)

    return total

def part2(inputs):
    total = 0
    all_values = set()
    for (a_str, b_str), (a_int, b_int) in zip(inputs[0].range_str, inputs[0].range_int):
        # print(f'{a_str}-{b_str}')
        for split_count in range(2, 1000):
            min_group = int('1' * split_count)
            if min_group > b_int:
                break
            # print('split_count', split_count, 'min_split', min_group)

            length = (len(a_str) + split_count - 1) // split_count
            max_length = len(b_str) // split_count
            for length in range(length, max_length + 1):
                min_str = str(10 ** (length - 1))
                min_group = int(min_str * split_count)
                a_int_cur = max(min_group, a_int)
                a_value = int(str(a_int_cur)[:length])
                a_max = 10 ** length
                a_group = int(str(a_value) * split_count)
                # print('length', length, max_length, 'min_split', min_group, 'a_int_cur', a_int_cur, 'a_value', a_value, a_group, 'a_max', a_max)
                if a_int_cur > a_group:
                    a_value += 1
                for a_value in range(a_value, a_max):
                    a_group = int(str(a_value) * split_count)
                    if a_group > b_int:
                        break
                    # print('found', a_group)
                    all_values.add(a_group)

    total = sum(all_values)
    return total

class AdventOfCode(unittest.TestCase):
    def setUp(self) -> None:
        script_dir = os.path.dirname(sys.argv[0])
        if len(script_dir) > 0:
            script_dir += '/'

        self.input_set = [
            load_input(script_dir + "example1.txt", 1227775554, 4174379265),
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
