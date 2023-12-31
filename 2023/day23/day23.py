#!/usr/bin/env python3
import graphviz
import unittest
import sys
import time
import os
import re

from pprint import pprint, pformat

class TimeBlock:
    def __init__(self, description=None):
        self.description = description

    def __enter__(self):
        self.begin = time.time()

    def __exit__(self, exception_type, exception_value, traceback):
        end = time.time()
        if exception_type is not None:
            raise exception_value

        print(f"{'' if self.description is None else self.description + ' '}took {end - self.begin:.3f} sec")

class Input(object):
    def __str__(self):
        return f"<Input {pformat(self.__dict__)}>"

    __repr__ = __str__

def convert_input(line):
    input = Input()
    input.line = line
    return line

def load_input(filename, solution_p1=None, solution_p2=None):
    try:
        with open(filename,'r') as f:
            lines = [line.strip() for line in f.readlines()]
    except:
        print("No input file", filename)
        return None
    inputs = [convert_input(line) for line in lines]
    return (inputs, solution_p1, solution_p2)

move = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]

direction_char = {
    (-1, 0): '<',
    (1, 0): '>',
    (0, -1): '^',
    (0, 1): 'v',
}
def make_step(path, pos):
    step = Input()
    step.path = path + [pos]
    step.pos = pos
    return step

def find_longest_path(input, is_part1):
    total = 0
    cache = {}
    starting_pos = (1, 0)
    goal_y = len(input) - 1
    q = [make_step([], starting_pos)]
    final_trail_start = None
    while len(q):
        step = q.pop(-1)
        trail = []
        while True:
            next_steps = []
            key = tuple(step.path[-2:])
            # key = step.pos
            if key in cache:
                # print("get from cache", key)
                pass
                cache_path = cache[key]
                if cache_path[-1] in step.path:
                    # print('cache path double steps')
                    break
                step.path.extend(cache_path)
                step.last_trail = cache_path
                step.pos = step.path[-1]
                continue
            if step.pos == final_trail_start:
                step.path.extend(final_trail)
                step.pos = step.path[-1]
                # print('using final trail')

            x, y = step.pos
            if y == goal_y:
                # print('found path', len(step.path) - 1, step.path)
                if final_trail_start is None:
                    final_trail = step.path[-2 - len(step.last_trail):]
                    final_trail_start = final_trail[0]
                    del final_trail[0]
                # print('found path', len(step.path) - 1, final_trail_start, final_trail)
                # print('found path', len(step.path) - 1)
                total = max(len(step.path) - 1, total)
                break
            for dx, dy in move:
                next_x = x + dx
                next_y = y + dy
                next_pos = (next_x, next_y)

                if next_x >= len(input[0]) or next_x < 0:
                    continue
                if next_y >= len(input) or next_y < 0:
                    continue
                if input[next_y][next_x] == '#':
                    continue
                uphill = direction_char[(-dx, -dy)]
                if is_part1 and input[next_y][next_x] == uphill:
                    continue
                if next_pos in step.path:
                    continue
                next_steps.append(make_step(step.path, next_pos))
            if len(next_steps) == 1:
                if len(trail) == 0:
                    cache[key] = trail
                step = next_steps[0]
                step.last_trail = trail
                trail.append(step.pos)
            else:
                for s in next_steps:
                    s.last_trail = trail
                q.extend(next_steps)
                break
    # pprint(cache)
    return total

def count_turns(input):
    counts = {}
    for i in range(5):
        counts[i] = 0
    for x in range(len(input[0])):
        for y in range(len(input)):
            if input[y][x] == '#':
                continue
            count = 0
            for dx, dy in move:
                next_x = x + dx
                next_y = y + dy
                next_pos = (next_x, next_y)

                if next_x >= len(input[0]) or next_x < 0:
                    continue
                if next_y >= len(input) or next_y < 0:
                    continue
                if input[next_y][next_x] == '#':
                    continue
                count += 1
            # if count == 4:
            #     print('4 at', x, y)
            counts[count] += 1
    pprint(counts)

def find_endpoint(input, graph:dict, visited:set, pos, pos2 = None):
    x, y = pos
    graph[pos] = graph.get(pos, {})
    steps = 0
    # print('find', pos, pos2)
    while True:
        visited.add((x, y))
        # print('visit', x, y)
        choices = 0
        next_step = []
        for dx, dy in move:
            next_x = x + dx
            next_y = y + dy
            next_pos = (next_x, next_y)

            if next_x >= len(input[0]) or next_x < 0:
                continue
            if next_y >= len(input) or next_y < 0:
                continue
            if input[next_y][next_x] == '#':
                continue
            if next_pos in visited:
                continue
            if pos2 is not None and pos2 != next_pos:
                continue
            choices += 1
            next_step.append(next_pos)
        pos2 = None


        if choices != 1 or (steps > 0 and (x, y) in graph):
            break
        steps += 1
        x, y = next_step[0]
    if steps > 0:
        graph[pos][(x, y)] = steps
        graph[(x, y)] = graph.get((x, y), {})
        graph[(x, y)][pos] = steps
    visited.discard(pos)
    visited.discard((x, y))
    for next_pos in next_step:
        find_endpoint(input, graph, visited, (x, y), next_pos)


def make_graph(input):
    starting_pos = (1, 0)
    graph = {}
    find_endpoint(input, graph, set(), starting_pos)
    # pprint(graph)
    return graph

def find_longest_path2(input, graph):
    total = 0
    found_count = 0
    starting_pos = (1, 0)
    goal_y = len(input) - 1
    q = [((starting_pos,), 0)]
    while len(q):
        path, path_len = q.pop(-1)
        pos = path[-1]
        if pos[1] == goal_y:
            # print('found', pos, path_len)
            total = max(total, path_len)
            found_count += 1
        for pos2, steps in graph[pos].items():
            if pos2 in path:
                continue
            q.append((path + (pos2,), path_len + steps))
    # print("Checked all paths", found_count)
    return total

def plot_graph(graph):
    dot = graphviz.Digraph(comment='Graph')
    for p1, edges in graph.items():
        p1 = str(p1)
        dot.node(p1, str(p1))
        for p2, steps in edges.items():
            p2 = str(p2)
            # dot.edge(p1, p2, str(steps))
            dot.edge(p1, p2)
    dot.render("day23graph")
    print(dot.source)
    exit(1)

def part1(input):
    # count_turns(input)
    return find_longest_path(input, True)

def part2(input):
    graph = make_graph(input)
    # plot_graph(graph)
    # count_turns(input)
    return find_longest_path2(input, graph)

class AdventOfCode(unittest.TestCase):
    def setUp(self) -> None:
        script_dir = os.path.dirname(sys.argv[0])
        if len(script_dir) > 0:
            script_dir += '/'

        self.input_set = [
            load_input(script_dir + "example1.txt", 94, 154),
            load_input(script_dir + "input1.txt"),
        ]

    def run_part(self, part_num, part_func):
        self.assertIn(part_num, [1, 2])
        for input_set in self.input_set:
            self.assertIsNotNone(input_set)
            expect = input_set[part_num]
            answer = part_func(input_set[0])
            print(f"Part{part_num} result", answer)
            if expect is not None:
                self.assertEqual(expect, answer)

    def test_part1(self):
        self.run_part(1, part1)

    def test_part2(self):
        self.run_part(2, part2)

unittest.main(verbosity=0)
