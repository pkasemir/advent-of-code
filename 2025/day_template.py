#!/usr/bin/env python3
from util_template import *

def part1(inputs: List[Input]):
    total = 0
    for input in inputs:
        print(input)
    return total

def part2(inputs: List[Input]):
    total = 0
    return total

class TodaysAdventOfCode(AdventOfCode):
    def test_part1(self):
        self.run_part(part1, -1)

    def test_part2(self):
        self.run_part(part2, -1)

unittest.main(verbosity=0)
