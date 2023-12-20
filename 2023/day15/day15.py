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

def do_hash(s):
    value = 0

    for c in s:
        value += ord(c)
        value *= 17
        value &= 0xff

    return value

def part1(input):
    total = 0
    for s in input[0].line.split(','):
        total += do_hash(s)
    return total

def part2(input):
    total = 0
    boxes =[[] for _ in range(256)]
    instructions = []
    for instruction in input[0].line.split(','):
        instruction = instruction.split('=')
        if len(instruction) != 2:
            instruction = [instruction[0].replace('-', ''), None]
        instructions.append(instruction)
    for label, lens in instructions:
        if lens is not None:
            lens = int(lens)
        box_num = do_hash(label)
        box = boxes[box_num]
        found = False
        # print('lookup', label, lens)
        for idx, (box_label, box_lens) in enumerate(box):
            if box_label == label:
                found = True
                break
        if lens is not None:
            if found:
                box[idx][1] = lens
            else:
                box.append([label, lens])
        else:
            if found:
                del box[idx]
        # for idx, box in enumerate(boxes):
        #     if len(box) > 0:
        #         print("box", idx, box)

        # print(label, lens, box)
    # pprint(boxes)
    for box_num, box in enumerate(boxes):
        box_num += 1
        for lens_num, (label, lens) in enumerate(box):
            lens_num += 1
            # print(label, box_num, lens_num, lens)
            total += box_num * lens_num * lens


    return total

class AdventOfCode(unittest.TestCase):
    def setUp(self) -> None:
        script_dir = os.path.dirname(sys.argv[0])
        if len(script_dir) > 0:
            script_dir += '/'

        self.input_set = [
            load_input(script_dir + "example1.txt", 1320, 145),
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
