#!/usr/bin/env python3
from utilday24 import *

class TodaysInput(Input):
    def extra_parsing(self):
        self.value = int(self.line)

def present_combos(presents, g1_weight):
    for g1_size in range(1, len(presents)):
        indexes = list(range(g1_size))
        while True:
            if indexes[-1] >= len(presents):
                indexes.pop(-1)
                if len(indexes) == 0:
                    break
                indexes[-1] += 1
                continue

            if len(indexes) != g1_size:
                indexes.append(indexes[-1] + 1)
                continue

            ranges = tuple(presents[i] for i in indexes)
            if sum(ranges) == g1_weight:
                others = tuple(presents[i] for i in range(len(presents)) if i not in indexes)
                yield ranges, others
            indexes[-1] += 1

def get_qe(inputs: List[TodaysInput], groups):
    presents = tuple(sorted((p.value for p in inputs), reverse=True))
    all_weight = sum(presents)
    group_weight = all_weight // groups
    assert(group_weight * groups == all_weight)
    min_group = [100] * len(presents)
    min_qe = 1e100
    for g1, others in present_combos(presents, group_weight):
        if len(min_group) < len(g1):
            break
        # print(g1, others)
        qe = 1
        for p in g1:
            qe *= p
        if qe >= min_qe:
            continue
        for g2, g3 in present_combos(others, group_weight):
            if groups == 4:
                found = False
                for g3, g4 in present_combos(g3, group_weight):
                    final_groups = (g2, g3, g4)
                    found = True
            else:
                final_groups = (g2, g3)
                found = True
            if not found:
                continue
            min_group = g1
            min_qe = qe
            # print(g1, qe, *final_groups)
            break
            # print(sum(g1), sum(g2), sum(g3))
    return min_qe

def part1(inputs: List[TodaysInput]):
    total = get_qe(inputs, 3)
    return total

def part2(inputs: List[TodaysInput]):
    total = get_qe(inputs, 4)
    return total

class TodaysAdventOfCode(AdventOfCode):
    input_class = TodaysInput
    def test_part1(self):
        self.load_test_inputs("example1.txt", "input1.txt")
        self.run_part(part1, 99)

    def test_part2(self):
        self.load_test_inputs("example1.txt", "input1.txt")
        self.run_part(part2, 44)

TodaysAdventOfCode.run_tests()
