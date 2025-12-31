#!/usr/bin/env python3
from utilday10 import *

class TodaysInput(Input):
    def extra_parsing(self):
        pass

def look_and_say(look):
    last = look[0]
    say = ''
    count = 1
    for c in look[1:]:
        if last == c:
            count += 1
        else:
            say += f'{count}{last}'
            count = 1
        last = c

    say += f'{count}{last}'
    return say

def part1(inputs: List[TodaysInput]):
    total = 0
    iterations = 5 if inputs[0].line == '1' else 40
    for input in inputs:
        say = input.line
        for _ in range(iterations):
            say = look_and_say(say)
            # print(say)
    total = len(say)
    return total

def part2(inputs: List[TodaysInput]):
    total = 0
    iterations = 50
    for input in inputs:
        say = input.line
        for _ in range(iterations):
            say = look_and_say(say)
            # print(say)
    total = len(say)
    return total

class TodaysAdventOfCode(AdventOfCode):
    input_class = TodaysInput
    def test_part1(self):
        self.load_test_inputs("example1.txt", "input1.txt")
        self.run_part(part1, 6)

    def test_part2(self):
        self.load_test_inputs(None, "input1.txt")
        self.run_part(part2, -1)

TodaysAdventOfCode.run_tests()
