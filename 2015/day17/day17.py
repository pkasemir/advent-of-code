#!/usr/bin/env python3
from utilday17 import *

class TodaysInput(Input):
    def extra_parsing(self):
        self.size = int(self.line)

    def __repr__(self):
        return str(self.size)

class ComboCounter:
    def __init__(self, inputs: List[TodaysInput], liters) -> None:
        self.inputs = sorted(inputs, key=lambda x: x.size)
        self.liters = liters

        self.container_min = 100
        self.container_count = 0

    def get_combo_count(self, current=(), first=0):
        total = 0
        current_liters = sum(map(lambda x: x.size, current))
        # print(current, current_liters)
        if current_liters > self.liters:
            return 0
        if current_liters == self.liters:
            if len(current) < self.container_min:
                self.container_min = len(current)
                self.container_count = 1
            elif len(current) == self.container_min:
                self.container_count += 1
            return 1

        for i, input in enumerate(self.inputs[first:], first):
            next_current = (*current, input)
            total += self.get_combo_count(next_current, i + 1)
        return total

def part1(inputs: List[TodaysInput], liters):
    total = 0
    # print('liters', liters)
    cc = ComboCounter(inputs, liters)
    total = cc.get_combo_count()
    return total

def part2(inputs: List[TodaysInput], liters):
    total = 0
    # print('liters', liters)
    cc = ComboCounter(inputs, liters)
    cc.get_combo_count()
    total = cc.container_count
    return total

class TodaysAdventOfCode(AdventOfCode):
    input_class = TodaysInput
    def test_part1(self):
        self.load_test_inputs("example1.txt", "input1.txt")
        self.set_test_args(25, 150)
        self.run_part(part1, 4)

    def test_part2(self):
        self.load_test_inputs("example1.txt", "input1.txt")
        self.set_test_args(25, 150)
        self.run_part(part2, 3)

TodaysAdventOfCode.run_tests()
