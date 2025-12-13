#!/usr/bin/env python3
from utilday8 import *
import sys
sys.setrecursionlimit(2000) # Sets the limit to 2000

class TodaysInput(Input):
    def extra_parsing(self):
        self.coords = self.from_list(self.line, ',', int)
        delattr(self, 'line')

class Distance:
    def __init__(self, a:TodaysInput, b:TodaysInput):
        self.a = a
        self.b = b
        pairs = list(zip(a.coords, b.coords))
        self.distances = list(map(lambda p: p[0] - p[1], pairs))
        self.distance = sum(map(lambda x: x**2,self.distances))
    def __str__(self):
        return f'{str(self.a.coords):30}/{str(self.b.coords):30} - {self.distance}'
    __repr__ = __str__

def get_distances(inputs: List[TodaysInput], first=0, distances=None):
    if distances is None:
        distances = []
    if first + 1 >= len(inputs):
        return distances
    for second in range(first + 1, len(inputs)):
        # print(second)
        d = Distance(inputs[first], inputs[second])
        distances.append(d)
    distances = get_distances(inputs, first + 1, distances)
    if first == 0:
        return sorted(distances, key=lambda d: d.distance)
    return distances

def get_circuits(inputs: List[TodaysInput], distances:List[Distance], count=None):
    circuits = {i: set((i,)) for i in inputs}
    for i, d in enumerate(distances):
        if count is not None:
            if i >= count:
                break
        # print(i, d, len(circuits))
        set_a = circuits[d.a]
        set_b = circuits[d.b]
        set_a.update(set_b)
        if len(set_a) == len(inputs):
            # print('found last item', d)
            break
        for c in circuits.keys():
            if c in set_a:
                circuits[c] = set_a

        # pprint(circuits)
        # print()
    return circuits, d

def get_circuit_sum(inputs: List[TodaysInput], distances:List[Distance], count):
    circuits, *_ = get_circuits(inputs, distances, count)

    final_circuits = []
    for c in circuits.values():
        if c in final_circuits:
            continue
        final_circuits.append(c)

    # pprint(final_circuits)
    circuit_counts = sorted([len(s) for s in final_circuits], reverse=True)
    # for s in final_circuits:
    #     print(len(s))
    # print(circuit_counts, len(circuit_counts))
    total = 1
    for i in range(3):
        total *= circuit_counts[i]

    return total

def part1(inputs: List[TodaysInput]):
    total = 0
    # for input in inputs:
    #     print(input)
    distances = get_distances(inputs)
    # pprint(distances)
    total = get_circuit_sum(inputs, distances, 10 if len(inputs) < 100 else 1000 )
    # pprint(circuits)
    return total

def part2(inputs: List[TodaysInput]):
    total = 0
    distances = get_distances(inputs)
    # pprint(distances)
    _, d = get_circuits(inputs, distances)
    total = d.a.coords[0] * d.b.coords[0]

    return total

class TodaysAdventOfCode(AdventOfCode):
    input_class = TodaysInput
    def test_part1(self):
        self.run_part(part1, 40)

    def test_part2(self):
        self.run_part(part2, 25272)

unittest.main(verbosity=0)
