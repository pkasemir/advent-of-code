#!/usr/bin/env python3
from utilday3 import *

class TodaysInput(Input):
    def extra_parsing(self):
        pass

moves = {
    '^': (0, 1),
    'v': (0, -1),
    '>': (1, 0),
    '<': (-1, 0),
}

def houses_visited(line, santas=1):
    coords = [(0, 0) for _ in range(santas)]
    houses = [set([c]) for c in coords]

    i = 0
    for c in line:
        dx, dy = moves[c]
        x, y = coords[i]
        x += dx
        y += dy
        coords[i] = (x, y)
        houses[i].add((x, y))
        i += 1
        if i >= len(houses):
            i = 0
    all_houses = set()
    for house in houses:
        all_houses = all_houses.union(house)

    return len(all_houses)

def part1(inputs: List[TodaysInput]):
    total = 0
    total = houses_visited(inputs[0].line)
    return total

def part2(inputs: List[TodaysInput]):
    total = 0
    total = houses_visited(inputs[0].line, 2)
    return total

class TodaysAdventOfCode(AdventOfCode):
    input_class = TodaysInput
    def test_part1(self):
        self.run_part(part1, 4)

    def test_part2(self):
        self.run_part(part2, 3)

unittest.main(verbosity=0)
