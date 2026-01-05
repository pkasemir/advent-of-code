#!/usr/bin/env python3
from utilday16 import *

message = '''children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1'''

class TodaysInput(Input):
    def extra_parsing(self):
        p1, p2 = self.line.split(':', maxsplit=1)
        self.number = int(p1.split()[1])
        self.properties = to_dict(self.from_list(p2, ','))

def to_dict(lines):
    d = {}
    for pv in lines:
            p, v = pv.split(':')
            d[p.strip()] = int(v)
    return d

actions = {
    'cats': lambda x, y : x > y,
    'trees': lambda x, y : x > y,
    'pomeranians': lambda x, y : x < y,
    'goldfish': lambda x, y : x < y,
}
def_action = lambda x, y: x == y

def get_sue_num(inputs: List[TodaysInput], actions={}):
    total = 0
    d = to_dict(message.splitlines())
    for input in inputs:
        # print(input)
        mismatch = False
        for p, v in input.properties.items():
            action = actions.get(p, def_action)
            if not action(v, d[p]):
                mismatch = True
                break
        if not mismatch:
            total = input.number
            break
    return total

def part1(inputs: List[TodaysInput]):
    total = 0
    total = get_sue_num(inputs)
    return total

def part2(inputs: List[TodaysInput]):
    total = 0
    total = get_sue_num(inputs, actions=actions)
    return total

class TodaysAdventOfCode(AdventOfCode):
    input_class = TodaysInput
    def test_part1(self):
        self.load_test_inputs(None, "input1.txt")
        self.run_part(part1, -1)

    def test_part2(self):
        self.load_test_inputs(None, "input1.txt")
        self.run_part(part2, -1)

TodaysAdventOfCode.run_tests()
