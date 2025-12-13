#!/usr/bin/env python3
from utilday7 import *

import functools

class Manifold(Grid):
    def do_splits(self):
        splits = 0
        for r in range(self.rows):
            for c, value in enumerate(self[r]):
                if value == '.':
                    if r > 0 and self[r - 1][c] == '|':
                        self[r][c] = '|'
                    continue
                if value in 'S':
                    self[r + 1][c] = '|'
                    continue
                if value == '^':
                    if self[r - 1][c] == '|':
                        self[r][c + 1] = '|'
                        self[r][c - 1] = '|'
                        splits += 1
        return splits

    @functools.lru_cache
    def find_splits(self, r, c):
        for next_r in range(r, self.rows):
            # print("check row", next_r, self[next_r][c])
            if self[next_r][c] == '^':
                return self.find_splits(next_r, c - 1) + self.find_splits(next_r, c + 1)
        return 1

    def do_quantum_splits(self):
        r = 0
        for c in range (self.rows):
            if self[r][c] == 'S':
                break
        return self.find_splits(r, c)

def part1(inputs: List[Input]):
    total = 0
    manifold = Manifold(inputs)
    total = manifold.do_splits()
    # print(manifold)
    return total

def part2(inputs: List[Input]):
    total = 0
    manifold = Manifold(inputs)
    total = manifold.do_quantum_splits()
    return total

class TodaysAdventOfCode(AdventOfCode):
    def test_part1(self):
        self.run_part(part1, 21)

    def test_part2(self):
        self.run_part(part2, 40)

unittest.main(verbosity=0)
