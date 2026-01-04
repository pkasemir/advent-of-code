#!/usr/bin/env python3
from utilday15 import *

class TodaysInput(Input):
    def extra_parsing(self):
        self.name, properties = self.from_list(self.line, ':')
        properties = self.from_list(properties, ',')
        self.properties = {}
        for p in properties:
            name, value = p.split()
            self.properties[name] = int(value)

p1_properties = ('capacity', 'durability', 'flavor', 'texture')
total_tablespoons = 100
def get_score(inputs: List[TodaysInput], used, check_calories):
    score = 1
    if check_calories:
        calories = 0
        for i, u in zip(inputs, used):
            calories += u * i.properties['calories']
        if calories != 500:
            return 0
    for p in p1_properties:
        p_sum = 0
        for i, u in zip(inputs, used):
            # print(p, i.name, u)
            p_sum += u * i.properties[p]
            # print(f'{p}-{i.name}: {u} * {i.properties[p]} = {u * i.properties[p]}')
        # print('p_sum', p_sum)
        if p_sum < 0:
            return 0
        score *= p_sum

    # print(used, score)
    return score


def maximize_score(inputs: List[TodaysInput], used, check_calories=False):
    # print('maximize', used)
    t_start = 0
    t_left = total_tablespoons - sum(used)
    if len(used) == len(inputs):
        return get_score(inputs, used, check_calories)
    elif len(used) == len(inputs) - 1:
        t_start = t_left
    total = 0
    for t in range(t_start, t_left + 1):
        next_used = (*used, t)
        total = max(total, maximize_score(inputs, next_used, check_calories=check_calories))

    return total

def part1(inputs: List[TodaysInput]):
    total = 0
    total = maximize_score(inputs, ())
    return total

def part2(inputs: List[TodaysInput]):
    total = 0
    total = maximize_score(inputs, (), True)
    return total

class TodaysAdventOfCode(AdventOfCode):
    input_class = TodaysInput
    def test_part1(self):
        self.load_test_inputs("example1.txt", "input1.txt")
        self.run_part(part1, 62842880)

    def test_part2(self):
        self.load_test_inputs("example1.txt", "input1.txt")
        self.run_part(part2, 57600000)

TodaysAdventOfCode.run_tests()
