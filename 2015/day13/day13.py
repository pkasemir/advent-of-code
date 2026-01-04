#!/usr/bin/env python3
from utilday13 import *

class TodaysInput(Input):
    def extra_parsing(self):
        m = re.match('(.+) would ([^ ]+) ([0-9]+) happiness units by sitting next to (.+).', self.line)
        assert(m)
        self.p1, adjective, value, self.p2 = m.groups()
        mult = 1 if adjective == 'gain' else -1
        self.happiness = mult * int(value)

def inputs_to_dict(inputs: List[TodaysInput]):
    people = {}
    for input in inputs:
        if input.p1 not in people:
            people[input.p1] = {}
        people[input.p1][input.p2] = input.happiness
    return people

def find_happiness(people, seated=(), remove_worst=False):
    if len(seated) == len(people):
        looped = (*seated, seated[0])
        worst = 1e10
        happiness = 0
        for n in range(len(looped) - 1):
            p1, p2 = looped[n:n+2]
            relation = people[p1][p2] + people[p2][p1]
            worst = min(worst, relation)
            happiness += relation
        # print(seated, happiness, worst)
        if remove_worst:
            happiness -= worst
        return happiness

    happiness = 0
    for person, reactions in people.items():
        if person in seated:
            continue
        next_seated = (*seated, person)
        happiness = max(happiness, find_happiness(people, next_seated, remove_worst=remove_worst))

    return happiness

def part1(inputs: List[TodaysInput]):
    total = 0
    people = inputs_to_dict(inputs)
    # pprint(people)
    total = find_happiness(people)
    return total

def part2(inputs: List[TodaysInput]):
    total = 0
    people = inputs_to_dict(inputs)
    # pprint(people)
    total = find_happiness(people, remove_worst=True)
    return total

class TodaysAdventOfCode(AdventOfCode):
    input_class = TodaysInput
    def test_part1(self):
        self.load_test_inputs("example1.txt", "input1.txt")
        self.run_part(part1, 330)

    def test_part2(self):
        self.load_test_inputs(None, "input1.txt")
        self.run_part(part2, -1)

TodaysAdventOfCode.run_tests()
