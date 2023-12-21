#!/usr/bin/env python3
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
    row = []
    for c in line:
        input = Input()
        input.c = c
        input.energized = False
        input.rays = []
        row.append(input)

    return row

def load_input(filename, solution_p1=None, solution_p2=None):
    try:
        with open(filename,'r') as f:
            lines = [line.strip() for line in f.readlines()]
    except:
        print("No input file", filename)
        return None
    inputs = [convert_input(line) for line in lines]
    return (inputs, solution_p1, solution_p2)

ray_to_tile_char = {
    (-1, 0): '<',
    (1, 0): '>',
    (0, -1): '^',
    (0, 1): 'v',
}

def get_tile_char(tile):
    if tile.c != '.':
        return tile.c
    if len(tile.rays) == 0:
        return '.'
    if len(tile.rays) > 1:
        return f'{len(tile.rays)}'
    return ray_to_tile_char[tile.rays[0]]


def print_contraption(input):
    for row in input:
        row = "".join([get_tile_char(tile) for tile in row])
        print(row)

def process_light_step(input, pos, direction):
    next_x = pos[0] + direction[0]
    next_y = pos[1] + direction[1]
    if next_x < 0 or next_x >= len(input[0]):
        return
    if next_y < 0 or next_y >= len(input):
        return
    tile = input[next_y][next_x]
    if direction in tile.rays:
        return
    tile.rays.append(direction)
    tile.energized = True
    if tile.c == '|':
        if direction[0] != 0:
            process_light_step(input, (next_x, next_y), (0, -1))
            process_light_step(input, (next_x, next_y), (0, 1))
            return
    if tile.c == '-':
        if direction[1] != 0:
            process_light_step(input, (next_x, next_y), (-1, 0))
            process_light_step(input, (next_x, next_y), (1, 0))
            return
    if tile.c == '\\':
        direction = (direction[1], direction[0])
    elif tile.c == '/':
        direction = (-direction[1], -direction[0])
    process_light_step(input, (next_x, next_y), direction)

def count_energized(input):
    total = 0
    for row in input:
        total += sum([1 for tile in row if tile.energized])
    return total

def part1(input):
    total = 0
    pos = (-1, 0)
    direction = (1, 0)
    sys.setrecursionlimit(100000)
    # print_contraption(input)
    process_light_step(input, pos, direction)
    # print()
    # print_contraption(input)
    # print(input[0])

    total = count_energized(input)
    return total

def clear_rays(input):
    for row in input:
        for tile in row:
            tile.energized = False
            tile.rays = []

def part2(input):
    total = 0
    sys.setrecursionlimit(100000)
    for y in range(len(input)):
        for x, dx in ((-1, 1), (len(input[0]), -1)):
            clear_rays(input)
            pos = (x, y)
            direction = (dx, 0)
            process_light_step(input, pos, direction)
            energized = count_energized(input)
            if energized > total:
                total = energized
                best_pos = pos
                best_direction = direction
    for x in range(len(input[0])):
        for y, dy in ((-1, 1), (len(input), -1)):
            clear_rays(input)
            pos = (x, y)
            direction = (0, dy)
            process_light_step(input, pos, direction)
            energized = count_energized(input)
            if energized > total:
                total = energized
                best_pos = pos
                best_direction = direction
    clear_rays(input)
    # try_input = tuple(map(tuple, input))
    process_light_step(input, best_pos, best_direction)
    # print_contraption(input)
    return total

class AdventOfCode(unittest.TestCase):
    def setUp(self) -> None:
        script_dir = os.path.dirname(sys.argv[0])
        if len(script_dir) > 0:
            script_dir += '/'

        self.input_set = [
            load_input(script_dir + "example1.txt", 46, 51),
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
