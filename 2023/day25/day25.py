#!/usr/bin/env python3
import unittest
import sys
import time
import os
import re
import graphviz

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
    input.key, vals = line.split(':')
    input.vals = vals.split()
    return input

def load_input(filename, solution_p1=None, solution_p2=None):
    try:
        with open(filename,'r') as f:
            lines = [line.strip() for line in f.readlines()]
    except:
        print("No input file", filename)
        return None
    inputs = [convert_input(line) for line in lines]
    return (inputs, solution_p1, solution_p2)

def to_graph(input):
    graph = {}

    for line in input:
        graph[line.key] = graph.get(line.key, set())
        graph[line.key].update(set(line.vals))
        for key in line.vals:
            graph[key] = graph.get(key, set())
            graph[key].add(line.key)


    return graph

def plot_graph(graph):
    print('graph nodes', len(graph))
    dot = graphviz.Digraph(comment='Graph')
    for p1, edges in graph.items():
        p1 = str(p1)
        dot.node(p1, str(p1))
        for p2 in edges:
            p2 = str(p2)
            # dot.edge(p1, p2, str(steps))
            dot.edge(p1, p2)
    dot.render("day25graph")
    print(dot.source)
    exit(1)

def fill_paths(cache, path, next_edge):
    for i, edge in enumerate(path):
        key = tuple(sorted((edge, next_edge)))
        next_path = path[i:] + (next_edge,)
        if edge != key[0]:
            next_path = tuple(reversed(next_path))
        cache[key] = next_path

def find_short(graph, cache, edge1, edge2, visited=None):
    if visited is None:
        visited = set((edge1,))
    q = [(edge1, (edge1,))]
    while len(q) > 0:
        edge, path = q.pop(0)
        key = tuple(sorted((edge, edge2)))
        if key in cache:
            finish_path = cache[key]
            if edge != key[0]:
                finish_path = tuple(reversed(finish_path))
            for next_edge in finish_path[1:]:
                fill_paths(cache, path, next_edge)
                path += (next_edge,)

            return path
        for next_edge in graph[edge]:
            if next_edge in visited:
                continue
            visited.add(next_edge)
            next_path = path + (next_edge,)

            # key = tuple(sorted((path[0], next_edge)))
            # cache[key] = next_path
            fill_paths(cache, path, next_edge)
            if next_edge == edge2:
                q.clear()
                return next_path
            q.append((next_edge, next_path))

def verify_cache(graph, cache):
    for edges, path in cache.items():
        edge1, edge2 = edges
        if edge1 != path[0]:
            raise Exception("edge1 not matching")
        if edge2 != path[-1]:
            raise Exception("edge2 not matching")
        for i in range(len(path) - 1):
            if path[i+1] not in graph[path[i]]:
                raise Exception("path not right")

def traverse_graph(graph, keys:set, edge, group:set):
    q = [edge]
    while len(q):
        edge = q.pop(0)
        if edge in group:
            continue
        group.add(edge)
        keys.discard(edge)
        for next_edge in graph[edge]:
            q.append(next_edge)

def part1(input):
    total = 0
    graph = to_graph(input)
    # pprint(graph)
    # print('graph', len(graph))
    # plot_graph(graph)
    for _ in range(3):
        cache = {}
        # with TimeBlock('find all shorts') as t:
        keys = list(graph.keys())
        for i, edge1 in enumerate(keys):
            for edge2 in keys[i+1:]:
                path = find_short(graph, cache, edge1, edge2)
    #         break
        # pprint(cache)
        # print('cache', len(cache))
        # with TimeBlock('verify') as t:
        verify_cache(graph, cache)
        link_counts = {}
        # with TimeBlock("count links") as t:
        for path in cache.values():
            for i in range(len(path) - 1):
                key = tuple(sorted((path[i], path[i + 1])))
                count = link_counts.get(key, 0) + 1
                link_counts[key] = count
        # pprint(link_counts)

        sorted_counts = sorted([(k, v) for k, v in link_counts.items()], key=lambda x: x[1])
        # pprint(sorted_counts)
        # print('sorted counts', len(sorted_counts))
        # print('link_counts', len(link_counts))
        (link1, link2), _ = sorted_counts[-1]
        graph[link1].remove(link2)
        graph[link2].remove(link1)

    groups = []

    keys = set(graph.keys())
    while len(keys) > 0:
        edge = keys.pop()
        groups.append(set())
        traverse_graph(graph, keys, edge, groups[-1])
    # pprint(groups)

    total = len(groups[0]) * len(groups[1])
    return total

def part2(input):
    total = 0
    return total

class AdventOfCode(unittest.TestCase):
    def setUp(self) -> None:
        script_dir = os.path.dirname(sys.argv[0])
        if len(script_dir) > 0:
            script_dir += '/'

        self.input_set = [
            load_input(script_dir + "example1.txt", 54, -1),
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
