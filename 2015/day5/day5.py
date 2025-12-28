#!/usr/bin/env python3
from utilday5 import *

class TodaysInput(Input):
    def extra_parsing(self):
        pass

vowels = 'aeiou'
bads = ('ab', 'cd', 'pq', 'xy')

def is_nice1(line):
    v_count = 0
    double = False
    last_c = None
    for c in line:
        if c == last_c:
            double = True
        if c in vowels:
            v_count += 1
        last_c = c
    if not double or v_count < 3:
        return False
    for bad in bads:
        if bad in line:
            return False
    return True

def is_nice2(line):
    has_pair  = False
    has_sandwich = False
    pairs = {}

    last1_c = None
    last2_c = None
    for i, c in enumerate(line):
        if last2_c == c:
            has_sandwich = True

        if last1_c != None:
            pair = pairs.get((last1_c, c), [])
            pair.append(i)
            pairs[(last1_c, c)] = pair
            for p in pair[1:]:
                if p - pair[0] >= 2:
                    has_pair = True

        last2_c = last1_c
        last1_c = c

    return has_pair and has_sandwich

def part1(inputs: List[TodaysInput]):
    total = 0
    for input in inputs:
        if is_nice1(input.line):
            total += 1
    return total

def part2(inputs: List[TodaysInput]):
    total = 0
    for input in inputs:
        if is_nice2(input.line):
            total += 1
    return total

class TodaysAdventOfCode(AdventOfCode):
    input_class = TodaysInput
    def test_part1(self):
        self.load_test_inputs("example1.txt", "input1.txt")
        self.run_part(part1, 2)

    def test_part2(self):
        self.load_test_inputs("example2.txt", "input1.txt")
        self.run_part(part2, 2)

unittest.main(verbosity=0)
