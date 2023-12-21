#!/usr/bin/env python3
import bisect
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
        d = dict(self.__dict__)
        del d['path']
        return f"<Input {pformat(d)}>"

    __repr__ = __str__

def convert_input(line):
    input = Input()
    input.line = line
    return tuple(map(int, line))

def load_input(filename, solution_p1=None, solution_p2=None):
    try:
        with open(filename,'r') as f:
            lines = [line.strip() for line in f.readlines()]
    except:
        print("No input file", filename)
        return None
    inputs = [convert_input(line) for line in lines]
    return (inputs, solution_p1, solution_p2)

direction_to_char = {
    (-1, 0): '<',
    (1, 0): '>',
    (0, -1): '^',
    (0, 1): 'v',
}

class Traverse(object):
    def __init__(self, input):
        self.input = input
        self.pos = (0, 0)
        self.direction = (1, 0)
        self.speed = 0
        self.goal_pos = (len(input[0]) - 1, len(input) - 1)
        # print("Goal", self.goal_pos)

    def print(self, path):
        city = []

        if False:
            for row in self.input:
                city.append(list(row))
                x_mult = 1
        else:
            for row in self.input:
                city.append([' ' for _ in range(len(row) * 2)])
            city[-1][-2] = '*'
            x_mult = 2
        for step in path:
            x, y = step.pos
            x *= x_mult
            direction = step.direction
            city[y][x] = direction_to_char[direction]
            if x_mult > 1:
                city[y][x + 1] = str(step.speed)


        for row in city:
            print("".join(map(str, row)))

    def walk2_add_directions(self, step):
        # print("Walk", step)
        if step is None:
            speed = 0
            total = 0
            x, y = (0, 0)
            direction = (0, 0)
            path = ()
        else:
            speed = step.speed
            total = step.total
            x, y = step.pos
            direction = step.direction
            path = step.path
            # self.print(path)

        for val in [1, -1]:
            for set_order in [lambda v: v, reversed]:
                dx, dy = tuple(set_order((val, 0)))
                next_x = x + dx
                next_y = y + dy
                next_pos = (next_x, next_y)
                next_direction = (dx, dy)
                if next_x < 0 or next_x >= len(self.input[0]):
                    continue
                if next_y < 0 or next_y >= len(self.input):
                    continue
                if direction == (-dx, -dy):
                    continue
                if direction in ((dx, dy), (0, 0)):
                    next_speed = speed + 1
                    if next_speed > self.max_move:
                        continue
                else:
                    if speed < self.min_move:
                        continue
                    next_speed = 1
                next_total = total + self.input[next_y][next_x]
                if next_pos == self.goal_pos:
                    if next_speed < self.min_move:
                        continue
                    self.found_route = next_total
                    self.found_path = path
                    return next_total

                visit_key = (next_pos, next_direction, next_speed)
                if visit_key in self.visited:
                    # print("Skip visited")
                    continue
                self.visited.add(visit_key)

                next_step = Input()
                next_step.pos = next_pos
                # if next_step.pos in visited:
                #     return path
                # visited.add(next_step.pos)
                # print('add', next_step.pos)


                next_step.direction = next_direction
                next_step.speed = next_speed
                next_step.total = next_total
                next_path = path + (next_step,)
                next_step.path = next_path
                bisect.insort(self.q, next_step, key=lambda step: step.total)
                # print("Add", next_step)
    def walk2(self):
        self.visited = set()
        self.found_route = None
        self.q = [None]
        while self.found_route is None:
            self.walk2_add_directions(self.q.pop(0))
            # pprint(self.q)
            # self.print(self.q)


        return self.found_route


def part1(input):
    total = 0
    traverse = Traverse(input)
    traverse.min_move = 1
    traverse.max_move = 3
    # traverse.print(())
    total = traverse.walk2()
    return total

def part2(input):
    total = 0
    traverse = Traverse(input)
    traverse.min_move = 4
    traverse.max_move = 10
    # traverse.print(())
    total = traverse.walk2()
    # traverse.print(traverse.found_path)
    return total

class AdventOfCode(unittest.TestCase):
    def setUp(self) -> None:
        script_dir = os.path.dirname(sys.argv[0])
        if len(script_dir) > 0:
            script_dir += '/'

        self.input_set = [
            load_input(script_dir + "example1.txt", 102, 94),
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
