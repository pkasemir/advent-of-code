#!/usr/bin/env python3
from utilday12 import *

import json

class TodaysInput(Input):
    def extra_parsing(self):
        self.json = json.loads(self.line)

def count_numbers(json, ignore_red=False):
    total = 0
    if isinstance(json, list):
        for subjson in json:
            total += count_numbers(subjson, ignore_red=ignore_red)
    elif isinstance(json, dict):
        ignore = False
        if ignore_red:
            for subjson in json.values():
                if subjson == 'red':
                    ignore = True
                    break
        if not ignore:
            for subjson in json.values():
                total += count_numbers(subjson, ignore_red=ignore_red)
    elif isinstance(json, int):
        total = json

    return total

def part1(inputs: List[TodaysInput]):
    total = 0
    for input in inputs:
        # print(input)
        total += count_numbers(input.json)
    return total

def part2(inputs: List[TodaysInput]):
    total = 0
    total += count_numbers(inputs[0].json, ignore_red=True)
    return total

class TodaysAdventOfCode(AdventOfCode):
    input_class = TodaysInput
    def test_part1(self):
        self.load_test_inputs("example1.txt", "input1.txt")
        self.run_part(part1, 2*(6+3))

    def test_part2(self):
        self.load_test_inputs("example2.txt", "input1.txt")
        self.run_part(part2, 4)

TodaysAdventOfCode.run_tests()
