#!/usr/bin/env python3
import sympy as sym
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
    pos, vel = line.split('@')
    input.pos = list(map(int, pos.split(',')))
    input.vel = list(map(int, vel.split(',')))
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

def solve_x(a, b):
    xc1, yc1, zc1 = a.pos
    xd1, yd1, zd1 = a.vel

    xc2, yc2, zc2 = b.pos
    xd2, yd2, zd2 = b.vel

    den = yd1/xd1 - yd2/xd2
    if den == 0:
        return None
    num = yc2 - yc1 - yd2*xc2/xd2 + yd1*xc1/xd1

    return num/den

def solve_t_from_x(hail, x):
    if x is None:
        return None
    return (x - hail.pos[0])/hail.vel[0]

def solve_y_from_t(hail, t):
    if t is None:
        return None
    return hail.pos[1] + hail.vel[1]*t

def in_range(r, val):
    return val >= r[0] and val <= r[1]

def part1(input):
    total = 0
    if len(input) < 10:
        area = (7, 27)
    else:
        area = (200000000000000, 400000000000000)
    for i, hail1 in enumerate(input):
        for hail2 in input[i + 1:]:
            x = solve_x(hail1, hail2)
            t1 = solve_t_from_x(hail1, x)
            t2 = solve_t_from_x(hail2, x)
            y1 = solve_y_from_t(hail1, t1)
            y2 = solve_y_from_t(hail2, t2)
            # if x is not None:
            #     assert(abs(y1 - y2) < 0.00000001)
            # print(hail1, hail2, 'x', x, 'y', y1, y2, 't', t1, t2)
            if x is None:
                # print("Parallel", hail1, hail2)
                continue
            if t1 < 0 or t2 < 0:
                # print("in the past", t1, t2)
                continue
            if not in_range(area, x) or not in_range(area, y1):
                # print("outside area")
                continue
            # print("ADD IT!!!")
            total += 1


    return total

def part2(input):
    total = 0
    sym.init_printing()

    stone_pos = sym.symbols('xcr,ycr,zcr')
    stone_vel = sym.symbols('xdr,ydr,zdr')
    eqs = []
    for i, hail1 in enumerate(input):
        t = sym.symbols(f't{i}')
        for ax in range(3):
            eq = hail1.pos[ax] + (hail1.vel[ax] - stone_vel[ax]) * t - stone_pos[ax]
            # print(eq)
            eqs.append(eq)
        # Solving all inputs takes too long, solving the first few gives a single solution
        if i > 6:
            break

    ans = sym.solve(eqs)
    # print(ans)
    total = int(sum([ans[0][s] for s in stone_pos]))

    return total

class AdventOfCode(unittest.TestCase):
    def setUp(self) -> None:
        script_dir = os.path.dirname(sys.argv[0])
        if len(script_dir) > 0:
            script_dir += '/'

        self.input_set = [
            load_input(script_dir + "example1.txt", 2, 47),
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
