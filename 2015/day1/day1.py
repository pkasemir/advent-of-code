#!/usr/bin/env python3
from utilday1 import *

class TodaysInput(Input):
    def extra_parsing(self):
        pass

def get_final_floor(line):
    floor = 0
    position = None
    for i, c in enumerate(line):
        if c == '(':
            floor += 1
        else:
            floor -= 1
        if position is None and floor == -1:
            position = i + 1

    return floor, position

def part1(inputs: List[TodaysInput]):
    total = 0
    for input in inputs:
        print(input)
    total, _ = get_final_floor(inputs[0].line)
    return total

def part2(inputs: List[TodaysInput]):
    total = 0
    _, total = get_final_floor(inputs[0].line)
    return total

class TodaysAdventOfCode(AdventOfCode):
    input_class = TodaysInput
    def test_part1(self):
        self.run_part(part1, -1)

    def test_part2(self):
        self.run_part(part2, 5)

unittest.main(verbosity=0)
