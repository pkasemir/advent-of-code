#!/usr/bin/env python3
import unittest
import sys
import time
import os
import re
import bisect

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
        for name in ['supports', 'supported_by']:
            d[name] = [b.name for b in d[name]]
        return f"<Input {pformat(d)}>"

    __repr__ = __str__

def convert_input(line):
    input = Input()
    input.line = line
    pts = line.split('~')
    pts = [list(map(int, p.split(','))) for p in pts]
    input.p1, input.p2 = pts
    # print(input)
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

def brick_in_point(brick, x, y, z):
    if x < brick.p1[0] or x > brick.p2[0]:
        return False
    if y < brick.p1[1] or y > brick.p2[1]:
        return False
    if z < brick.p1[2] or z > brick.p2[2]:
        return False
    return True

def get_brick_name(idx):
    return chr(ord('A') + idx % 26)

def print_bricks(input):
    max_x = max([get_brick_min_max(b, max, 0) for b in input])
    max_y = max([get_brick_min_max(b, max, 1) for b in input])
    max_z = max([get_brick_min_max(b, max, 2) for b in input])
    for idx in [0,1]:
        c = "xy"[idx]
        print()
        print(c, ', z')
        if idx == 0:
            get_x = lambda a, b: a
            get_y = lambda a, b: b
        else:
            get_x = lambda a, b: b
            get_y = lambda a, b: a
        idx_other = 1 - idx
        max_xy = [max_x, max_y][idx]
        max_xy_other = [max_x, max_y][idx_other]

        for z in range(max_z, -1, -1):
            line = []
            for xy in range(max_xy + 1):
                vals = []
                for xy_other in range(max_xy_other + 1):
                    vals.extend([n for n, b in enumerate(input) if brick_in_point(b, get_x(xy, xy_other), get_y(xy, xy_other), z)])
                # print(c, xy, z, vals)
                vals = set(vals)
                if len(vals) == 0:
                    line.append('.')
                elif len(vals) == 1:
                    line.append(input[vals.pop()].name)
                else:
                    line.append('?')
            print("".join(line), z)

def get_brick_min_max(brick, func, idx):
    return func(brick.p1[idx], brick.p2[idx])

def check_overlap_bricks(input):
    for idx, b1 in enumerate(input):
        for check_idx in range(idx - 1, -1, -1):
            b2 = input[check_idx]
            matches = True
            for axis in range(3):
                center_sep = abs(b1.center[axis] - b2.center[axis])
                center_dist = b1.center_dist[axis] + b2.center_dist[axis]
                if center_sep >= center_dist:
                    matches = False
                    break
            if not matches:
                continue
            raise Exception("Found overlapping blocks")

def land_bricks(input):
    landed = []
    check_overlap_bricks(input)
    for idx, b1 in enumerate(input):
        top_height = None
        for check_idx in range(len(landed) - 1, -1, -1):
            b2 = landed[check_idx]
            matches = True
            for axis in range(2):
                center_sep = abs(b1.center[axis] - b2.center[axis])
                center_dist = b1.center_dist[axis] + b2.center_dist[axis]
                if center_sep >= center_dist:
                    matches = False
                    break
            if not matches:
                continue

            if top_height is None:
                top_height = b2.p2[2]
            elif top_height != b2.p2[2]:
                break
            b2.supports.append(b1)
            b1.supported_by.append(b2)
            # print(b1.name, b1.line, b2.name, b2.line)
        if top_height is None:
            top_height = 0
        drop = b1.p1[2] - (top_height + 1)
        # print('drop', drop)
        if drop > 0:
            for arr in [b1.p1, b1.p2, b1.center]:
                arr[2] -= drop
        bisect.insort(landed, b1, key=lambda b: b.p2[2])
    input[:] = landed
    check_overlap_bricks(input)

def sort_bricks(input):
    input.sort(key=lambda b: max(b.p1[2], b.p2[2]))
    max_x = max([get_brick_min_max(b, max, 0) for b in input])
    max_y = max([get_brick_min_max(b, max, 1) for b in input])
    max_z = max([get_brick_min_max(b, max, 2) for b in input])
    # print(max_x, max_y, max_z)
    # placed_bricks = []
    for idx, brick in enumerate(input):
        brick.name = get_brick_name(idx)
        p1 = [get_brick_min_max(brick, min, i) for i in range(3)]
        p2 = [get_brick_min_max(brick, max, i) for i in range(3)]
        brick.p1, brick.p2 = (p1, p2)
        brick.center_dist = [(b - a + 1) / 2 for a, b in zip(p1, p2)]
        brick.center = [a + d for a, d in zip(p1, brick.center_dist)]
        # print(brick)
        brick.supports = []
        brick.supported_by = []

def part1(input):
    total = 0
    sort_bricks(input)
    # print_bricks(input)
    land_bricks(input)
    # print_bricks(input)

    for brick in input:
        can_disintegrate = True
        for b2 in brick.supports:
            if len(b2.supported_by) == 1:
                can_disintegrate = False
                assert(b2.supported_by == [brick])
                break
        if can_disintegrate:
            # print('disintegrate', brick.name, brick)
            total += 1

    return total

def count_fall(brick):
    # print('check', brick.name)
    for b in brick.supports:
        b.fall_supported_by = [b2 for b2 in b.fall_supported_by if b2 != brick]
        if len(b.fall_supported_by) == 0:
            count_fall(b)

def prepare_fall(input):
    for brick in input:
        brick.fall_supported_by = list(brick.supported_by)

def part2(input):
    total = 0
    sort_bricks(input)
    land_bricks(input)
    for brick in input:
        prepare_fall(input)
        count_fall(brick)
        for b in input:
            # print(brick.name, b.name, [b2.name for b2 in b.fall_supported_by])
            if len(b.fall_supported_by) == 0 and b.p1[2] > 1:
                total += 1
    return total

class AdventOfCode(unittest.TestCase):
    def setUp(self) -> None:
        script_dir = os.path.dirname(sys.argv[0])
        if len(script_dir) > 0:
            script_dir += '/'

        self.input_set = [
            load_input(script_dir + "example1.txt", 5, 7),
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
