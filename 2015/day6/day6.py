#!/usr/bin/env python3
from utilday6 import *

class TodaysInput(Input):
    def extra_parsing(self):
        m = re.match('(.*) ([0-9]+,[0-9]+) through ([0-9]+,[0-9]+)$', self.line)
        self.action = m.group(1)
        self.start = self.from_list(m.group(2), ',', int)
        self.end = self.from_list(m.group(3), ',', int)

actions1 = {
    "turn on": lambda x: 1,
    "turn off": lambda x: 0,
    "toggle": lambda x: x ^ 1,
}

actions2 = {
    "turn on": lambda x: x + 1,
    "turn off": lambda x: x - 1,
    "toggle": lambda x: x + 2,
}

def get_lights_lit(inputs: List[TodaysInput], actions):
    lights = [[0] * 1000 for _ in range(1000)]
    for input in inputs:
        action = actions[input.action]
        # print(input)
        # assume start is always less than end
        xs, ys = input.start
        xe, ye = input.end
        x = xs
        while x <= xe:
            y = ys
            while y <= ye:
                # print(input.action, x, y, lights[y][x], '->', action(lights[y][x]))
                lights[y][x] = max(0, action(lights[y][x]))
                y += 1
            x += 1
    return sum(map(sum, lights))

def part1(inputs: List[TodaysInput]):
    total = 0
    total = get_lights_lit(inputs, actions1)
    return total

def part2(inputs: List[TodaysInput]):
    total = 0
    total = get_lights_lit(inputs, actions2)
    return total

class TodaysAdventOfCode(AdventOfCode):
    input_class = TodaysInput
    def test_part1(self):
        self.load_test_inputs("example1.txt", "input1.txt")
        self.run_part(part1, 1000000 - 1000 - 4)

    def test_part2(self):
        self.load_test_inputs("example1.txt", "input1.txt")
        self.run_part(part2, 1001996)

unittest.main(verbosity=0)
