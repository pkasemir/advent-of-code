#!/usr/bin/env python3
from utilday9 import *

class TodaysInput(Input):
    def extra_parsing(self):
        m = re.match('(.*) to (.*) = (.*)', self.line)
        self.p1, self.p2, d = m.groups()
        self.distance = int(d)

def find_path(inputs: List[TodaysInput], min_max):
    global paths
    paths = {}
    for input in inputs:
        if input.p1 not in paths:
            paths[input.p1] = {}
        if input.p2 not in paths:
            paths[input.p2] = {}
        paths[input.p1][input.p2] = input.distance
        paths[input.p2][input.p1] = input.distance
        # print(input)
    # pprint(paths)
    return find_path_recurse(min_max)

def find_path_recurse(min_max, visited:tuple=(), distances:tuple=()):
    global paths

    if len(visited) == len(paths):
        # print('end',visited, distances, sum(distances))
        return sum(distances)

    if min_max is min:
        value = 1e100
    else:
        value = 0
    for p1, next_paths in paths.items():
        if len(visited) > 0:
            if p1 != visited[-1]:
                continue
            p1_visited = visited
        else:
            p1_visited = (*visited, p1)
        for p2, dist in next_paths.items():
            if p2 in visited:
                continue
            p2_distances = (*distances, dist)
            p2_visited = (*p1_visited, p2)
            # print(p1, p2, dist, p2_visited, p2_distances, sum(p2_distances))
            length = find_path_recurse(min_max, p2_visited, p2_distances)
            value = min_max(value, length)
    return value

def part1(inputs: List[TodaysInput]):
    total = 0
    total = find_path(inputs, min)
    return total

def part2(inputs: List[TodaysInput]):
    total = 0
    total = find_path(inputs, max)
    return total

class TodaysAdventOfCode(AdventOfCode):
    input_class = TodaysInput
    def test_part1(self):
        self.load_test_inputs("example1.txt", "input1.txt")
        self.run_part(part1, 605)

    def test_part2(self):
        self.load_test_inputs("example1.txt", "input1.txt")
        self.run_part(part2, 982)

unittest.main(verbosity=0)
