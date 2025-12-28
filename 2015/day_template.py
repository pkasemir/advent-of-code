#!/usr/bin/env python3
from util_template import *

class TodaysInput(Input):
    def extra_parsing(self):
        pass

def part1(inputs: List[TodaysInput]):
    total = 0
    for input in inputs:
        print(input)
    return total

def part2(inputs: List[TodaysInput]):
    total = 0
    return total

class TodaysAdventOfCode(AdventOfCode):
    input_class = TodaysInput
    def test_part1(self):
        self.load_test_inputs("example1.txt", "input1.txt")
        self.run_part(part1, -1)

    def test_part2(self):
        self.load_test_inputs("example1.txt", "input1.txt")
        self.run_part(part2, -1)

unittest.main(verbosity=0)
