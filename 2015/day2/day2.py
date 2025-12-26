#!/usr/bin/env python3
from utilday2 import *

class TodaysInput(Input):
    def extra_parsing(self):
        self.dims = self.from_list(self.line, 'x', int)

    def get_area(self):
        l, w, h = self.dims
        return 2 * (l * w + w * h + h *l)

    def get_smallest_side_area(self):
        s1, s2, _ = list(sorted(self.dims))
        return s1 * s2

    def get_wrapping_paper(self):
        return self.get_area() + self.get_smallest_side_area()

    def get_ribbon(self):
        volume = 1
        for d in self.dims:
            volume *= d
        s1, s2, _ = list(sorted(self.dims))
        around = 2 * (s1 + s2)
        return volume + around

def part1(inputs: List[TodaysInput]):
    total = 0
    for input in inputs:
        # print(input)
        total += input.get_wrapping_paper()
    return total

def part2(inputs: List[TodaysInput]):
    total = 0
    for input in inputs:
        # print(input)
        total += input.get_ribbon()
    return total

class TodaysAdventOfCode(AdventOfCode):
    input_class = TodaysInput
    def test_part1(self):
        self.run_part(part1, 58 + 43)

    def test_part2(self):
        self.run_part(part2, 34 + 14)

unittest.main(verbosity=0)
