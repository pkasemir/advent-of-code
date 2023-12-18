#!/usr/bin/env python3
import unittest
import sys
import os
import re

from pprint import pprint, pformat

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

connectors = {
    '|': [(0, -1), (0, 1)],
    '-': [(-1, 0), (1, 0)],
    'L': [(0, -1), (1, 0)],
    'J': [(0, -1), (-1, 0)],
    '7': [(0, 1), (-1, 0)],
    'F': [(0, 1), (1, 0)],
    '.': [],
}

connectors_sides = {
    'L': [(0, 1), (-1, 0)],
    'J': [(0, 1), (1, 0)],
    '7': [(0, -1), (1, 0)],
    'F': [(0, -1), (-1, 0)],
}

class Tile(str):
    @classmethod
    def new(cls, *args):
        o = cls(*args)
        o.is_part_of_loop = False
        o.outside = None
        o.is_outside = False
        o.is_inside = False
        o.is_start = False
        return o

def look_connects(input, x, y, look_x, look_y):
    tile = input[look_y][look_x]
    if tile == 'S':
        return look_x, look_y, tile
    for test_x, test_y in connectors[tile]:
        calc_x = look_x + test_x
        calc_y = look_y + test_y
        if x == calc_x and y == calc_y:
            return look_x, look_y, tile
    return None


def find_connect(input, x, y):
    for look_x in [-1, 1]:
        found = look_connects(input, x, y, x + look_x, y)
        if found is not None:
            return found
    for look_y in [-1, 1]:
        found = look_connects(input, x, y, x, y + look_y)
        if found is not None:
            return found
    return None

def find_other_side(input, x, y, next_x, next_y):
    input[y][x].next_xy = next_x, next_y
    tile = input[next_y][next_x]
    tile.prev_xy = x, y
    tile.is_part_of_loop = True
    if tile == 'S':
        return next_x, next_y, tile
    for test_x, test_y in connectors[tile]:
        calc_x = next_x + test_x
        calc_y = next_y + test_y
        if not (x == calc_x and y == calc_y):
            tile = input[calc_y][calc_x]
            return calc_x, calc_y, tile
    return None

def part1(input):
    total = 0
    for y, line in enumerate(input):
        # print(row, line)
        # if 'S' in row
        m = re.search('S', line)
        # print(m)
        if m:
            x = m.start()
            break
    input = [list(map(Tile.new, line)) for line in input]
    # print("x, y", x, y)
    next_x, next_y, tile = find_connect(input, x, y)
    # print((next_x, next_y, tile))
    while tile != 'S':
        found = find_other_side(input, x, y, next_x, next_y)
        # print(found)
        x, y = next_x, next_y
        next_x, next_y, tile = found
        total += 1
    total += 1


    return total // 2

def print_loop(input):
    for line in input:
        for tile in line:
            if tile.is_part_of_loop:
                # c = str(tile) + str(tile.next_xy)
                c = str(tile)
            elif tile.is_outside:
                c = 'O'
            else:
                c = 'I'
            print(f'{c:1}', end='')
        # print("".join(["." if tile.is_part_of_loop else " " for tile in line]))
        print()

def find_first_loop_tile(input):
    first = None
    for y in range(len(input)):
        for x in range(len(input[0])):
            input[y][x].x = x
            input[y][x].y = y
            if input[y][x].is_part_of_loop:
                if first is None:
                    first = input[y][x]
    return first

def get_next_tile_diff(tile):
    x, y = tile.next_xy
    return x - tile.x, y - tile.y

def wrap_outside(input, tile):
    sides = connectors_sides.get(str(tile), None)
    dx, dy = get_next_tile_diff(tile)
    if sides is None:
        ox, oy = tile.outside[0]
        return (ox + dx, oy + dy)
    if len(tile.outside) == 0:
        return None

    s1, s2 = sides
    s1x, s1y = s1
    s2x, s2y = s2

    if tile.outside[0] == (tile.x + s1x, tile.y + s1y):
        sx, sy = s2
    elif tile.outside[0] == (tile.x + s2x, tile.y + s2y):
        sx, sy = s1
    else:
        tile.outside = []
        return tile.x - s1x - s2x, tile.y - s1y - s2y
        # px, py = tile.prev_xy
        # prev_tile = input[py][px]
        # return prev_tile.outside[-1]

    tile.outside.append(((tile.x + sx), (tile.y + sy)))
    ox, oy = tile.outside[1]
    next_ox, next_oy = ox + dx, oy + dy
    return next_ox, next_oy

def update_outside_tiles(input, tile):
    for ox, oy in tile.outside:
        if ox < 0 or oy < 0 or oy >= len(input) or ox >= len(input[0]):
            continue
        otile = input[oy][ox]
        if not otile.is_part_of_loop:
            otile.is_outside = True

def get_loop_outside(input):
    tile = find_first_loop_tile(input)
    dx, dy = get_next_tile_diff(tile)
    tile.outside = [(tile.x - dx, tile.y - dy)]
    w = wrap_outside(input, tile)
    update_outside_tiles(input, tile)
    # print("first", tile, tile.x, tile.y, tile.outside)

    while True:
        next_x, next_y = tile.next_xy
        tile = input[next_y][next_x]
        if tile.outside is not None:
            break
        tile.outside = []
        if w is not None:
            tile.outside.append(w)
        w = wrap_outside(input, tile)
        update_outside_tiles(input, tile)

        # print("loop ", tile, tile.x, tile.y, tile.outside)

def is_tile_inside(input, x, y):
    tile = input[y][x]
    if tile.is_outside or tile.is_part_of_loop:
        return False
    for dx in [-1, 1]:
        new_x = x + dx
        if new_x < 0 or new_x >= len(input[0]):
            tile.is_outside = True
            return False
        if input[y][new_x].is_outside:
            tile.is_outside = True
            return False
    for dy in [-1, 1]:
        new_y = y + dy
        if new_y < 0 or new_y >= len(input):
            tile.is_outside = True
            return False
        if input[new_y][x].is_outside:
            tile.is_outside = True
            return False
    return True

def find_inside(input):
    count = 0
    for y in range(len(input)):
        for x in range(len(input[0])):
            if is_tile_inside(input, x, y):
                count += 1
    return count


def part2(input):
    total = 0
    for y, line in enumerate(input):
        # print(row, line)
        # if 'S' in row
        m = re.search('S', line)
        # print(m)
        if m:
            x = m.start()
            break
    # print("x, y", x, y)
    input = [list(map(Tile.new, line)) for line in input]
    input[y][x].is_part_of_loop = True
    next_x, next_y, tile = find_connect(input, x, y)
    # print((next_x, next_y, tile))
    while tile != 'S':
        found = find_other_side(input, x, y, next_x, next_y)
        # print(found)
        x, y = next_x, next_y
        next_x, next_y, tile = found
    input[y][x].next_xy = next_x, next_y
    input[next_y][next_x].prev_xy = x, y
    start_connectors = [(tile.next_xy[0] - next_x, tile.next_xy[1] - next_y),
                        (x - next_x, y - next_y)]
    c1, c2 = start_connectors

    for t, t_list in connectors.items():
        if len(t_list) != 2:
            continue
        if c1 in t_list and c2 in t_list:
            new_start = Tile.new(t)
            new_start.is_part_of_loop = True
            new_start.next_xy = tile.next_xy
            new_start.prev_xy = tile.prev_xy
            new_start.is_start = True
            input[next_y][next_x] = new_start
            break

    get_loop_outside(input)
    total = find_inside(input)
    # print_loop(input)

    return total

class AdventOfCode(unittest.TestCase):
    def setUp(self) -> None:
        script_dir = os.path.dirname(sys.argv[0])
        if len(script_dir) > 0:
            script_dir += '/'

        self.input_set = [
            load_input(script_dir + "example1.txt", 4, -1),
            load_input(script_dir + "example2.txt", 8, -1),
            load_input(script_dir + "example3.txt", -1, 4),
            load_input(script_dir + "example3b.txt", -1, 4),
            load_input(script_dir + "example4.txt", -1, 8),
            load_input(script_dir + "example5.txt", -1, 10),
            load_input(script_dir + "input1.txt"),
        ]

    def run_part(self, part_num, part_func):
        self.assertIn(part_num, [1, 2])
        for input_set in self.input_set:
            self.assertIsNotNone(input_set)
            expect = input_set[part_num]
            if expect == -1:
                continue
            answer = part_func(input_set[0])
            print(f"Part{part_num} result", answer)
            if expect is not None:
                self.assertEqual(expect, answer)

    def test_part1(self):
        self.run_part(1, part1)

    def test_part2(self):
        self.run_part(2, part2)

unittest.main(verbosity=0)
