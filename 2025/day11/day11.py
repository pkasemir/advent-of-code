#!/usr/bin/env python3
from utilday11 import *

import functools

class TodaysInput(Input):
    def extra_parsing(self):
        self.machine, self.outputs = self.line.split(':')
        self.outputs = self.outputs.split()

@functools.lru_cache
def count_paths_to(cur, last):
    global machines
    if cur == last:
        return 1
    if cur == 'out':
        return 0
    count = 0
    for n in machines[cur]:
        count += count_paths_to(n, last)
    return count

def part1(inputs: List[TodaysInput]):
    count_paths_to.cache_clear()
    total = 0
    global machines
    machines = {i.machine:i.outputs for i in inputs}
    # pprint(machines)
    total = count_paths_to('you', 'out')
    return total

def part2(inputs: List[TodaysInput]):
    count_paths_to.cache_clear()
    total = 0
    global machines
    machines = {i.machine:i.outputs for i in inputs}
    # pprint(machines)
    first, second = 'fft', 'dac'
    total = count_paths_to(first, second)
    if total == 0:
        first, second = 'dac', 'fft'
        total = count_paths_to(first, second)

    total *= count_paths_to('svr', first)
    total *= count_paths_to(second, 'out')
    return total

class TodaysAdventOfCode(AdventOfCode):
    input_class = TodaysInput
    def test_part1(self):
        self.run_part(part1, 5)

    def test_part2(self):
        self.load_test_inputs("example2.txt", "input1.txt")
        self.run_part(part2, 2)

unittest.main(verbosity=0)
