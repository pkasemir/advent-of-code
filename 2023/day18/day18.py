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
    input = Input()
    input.line = line
    input.direction, input.moves, input.color = line.split()
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

direction_to_tuple = {
    'U' : (0, -1),
    'D' : (0, 1),
    'L' : (-1, 0),
    'R' : (1, 0),
}

def print_terrain(terrain):
    for y, row in enumerate(terrain):
        row = [' ' if c == ' ' else '#' for c in row]
        print(f'{y:9}', "".join(row))
x_offset = 10

def count_outside(terrain):
    visited = set()
    q = []
    for y in range(len(terrain)):
        for x in [0, len(terrain[0]) - 1]:
            q.append((x, y))
    # print_terrain(terrain)
    for x in range(len(terrain[0])):
        for y in [0, len(terrain) - 1]:
            q.append((x, y))
    while len(q) > 0:
        x, y = q.pop()
        if x < 0 or x >= len(terrain[0]):
            continue
        if y < 0 or y >= len(terrain):
            continue
        if terrain[y][x] != '.':
            continue
        pos = (x, y)
        if pos in visited:
            continue
        visited.add(pos)
        # print('add', pos)
        terrain[y][x] = ' '
        for dx, dy in direction_to_tuple.values():
            next_x = x + dx
            next_y = y + dy
            q.append((next_x, next_y))

    return len(terrain) * len(terrain[0]) - len(visited)

def part1(input):
    total = 0
    terrain = [["S"]]
    x = y = 0
    for instruction in input:
        dx, dy = direction_to_tuple[instruction.direction]
        for val in range(int(instruction.moves)):
            x += dx
            y += dy
            if x < 0:
                insert_x_action = lambda row: row.insert(0, '.')
            elif x >= len(terrain[0]):
                insert_x_action = lambda row: row.append('.')
            else:
                insert_x_action = None

            if y < 0:
                insert_y_action = lambda terrain, row: terrain.insert(0, row)
            elif y >= len(terrain):
                insert_y_action = lambda terrain, row: terrain.append(row)
            else:
                insert_y_action = None

            if insert_x_action is not None:
                for row in terrain:
                    insert_x_action(row)
                if x < 0:
                    x += 1

            if insert_y_action is not None:
                insert_y_action(terrain, ['.' for _ in terrain[0]])
                if y < 0:
                    y += 1
            terrain[y][x] = '#'

    total = count_outside(terrain)
    # print_terrain(terrain)

    return total

def pair_wise(l):
    l_iter = iter(l)
    return zip(l_iter, l_iter)

def handle_corners(old_corners, current_corners):
    total = 0
    columns = {}
    to_split = []
    for corner1, corner2 in pair_wise(current_corners):
        # print('pair',corner1, corner2)
        found = False
        for old_pair in old_corners:
            is_split = False
            if old_pair.x[0] in [corner1[1], corner2[1]]:
                found = True
            elif old_pair.x[1] in [corner1[1], corner2[1]]:
                found = True
            elif corner1[1] > old_pair.x[0] and corner1[1] < old_pair.x[1]:
                # print("need to split")
                found = True
                is_split = True
                to_split.append((corner1, corner2))
            else:
                continue
            # print('found')
            pair_corners = columns.get(old_pair, [])
            pair_corners.extend([corner1, corner2])
            columns[old_pair] = pair_corners
        if not found:
            old_corner = Input()
            old_corner.y = corner1[2]
            old_corner.x = [corner1[1], corner2[1]]

            old_corners.append(old_corner)
            # print('adding to old', id(old_corner))
            old_corners.sort(key=lambda c: c.x)
            # pprint(old_corners)
    # pprint(columns)
    for old_pair, pair_corners in columns.items():
        # print('paired', old_pair, pair_corners)
        height = pair_corners[0][2] - old_pair.y + 1
        width = old_pair.x[1] - old_pair.x[0] + 1
        # print("calc y", height, width)
        area = height * width
        # print('area', area)
        total += area
        if print_part2_terrain:
            for x in range(width):
                x += old_pair.x[0] - x_offset# - min_x
                for y in range(height):
                    y += old_pair.y # - min_y
                    part2_terrain[y][x] = '#'
        # total += area
        # next1, next2 = (old1, old2)
        original_x = list(old_pair.x)
        split_non_overlap = 0
        for corner1, corner2 in pair_wise(pair_corners):
            is_split = (corner1, corner2) in to_split
            if is_split:
                split_non_overlap += corner2[1] - corner1[1] - 1
                # print("Calculate for split",  (corner1, corner2), split_non_overlap)
            else:
                if old_pair.x[0] in [corner1[1], corner2[1]]:
                    # print('update next1')
                    old_pair.y = corner1[2]
                    if old_pair.x[0] == corner1[1]:
                        old_pair.x[0] = corner2[1]
                    else:
                        old_pair.x[0] = corner1[1]
                if old_pair.x[1] in [corner1[1], corner2[1]]:
                    # print('update next2')
                    old_pair.y = corner1[2]
                    if old_pair.x[1] == corner1[1]:
                        old_pair.x[1] = corner2[1]
                    else:
                        old_pair.x[1] = corner1[1]
        if old_pair.x[0] < old_pair.x[1]:
            overlap = min(old_pair.x[1], original_x[1]) - max(old_pair.x[0], original_x[0]) + 1 - split_non_overlap
            # print('overlap', overlap)
            total -= overlap

    # Remove ended section
    old_corners[:] = [corner for corner in old_corners if corner.x[0] < corner.x[1]]
    old_corners.sort(key=lambda c: c.x)
    # pprint(old_corners)
    new_corners = []
    for old_pair in old_corners:
        # print("look for merge", old_pair)
        merged = False
        for new_pair in new_corners:
            if old_pair.x[0] > new_pair.x[0] and old_pair.x[0] < new_pair.x[1]:
                # print("should merge")
                new_pair.x[1] = old_pair.x[1]
                merged = True
                break
        if not merged:
            new_corners.append(old_pair)
    old_corners[:] = new_corners
    old_corners.sort(key=lambda c: c.x)
    # print("merged", old_corners)
    for corner1, corner2 in to_split:
        # print("Splitting", corner1, corner2)
        for old_pair in old_corners:
            # print(old_pair)
            if corner1[1] > old_pair.x[0] and corner1[1] < old_pair.x[1]:
                # print('found split pair')

                split_corner = Input()
                split_corner.y = corner1[2]
                split_corner.x = [corner2[1], old_pair.x[1]]

                old_corners.append(split_corner)
                old_pair.x[1] = corner1[1]
                old_pair.y = corner1[2]
                break
        old_corners.sort(key=lambda c: c.x)
        # pprint(old_corners)


    # print()
    return total

def part2(input):
    total = 0
    direction_int_to_c = "RDLU"
    corners = []
    x = y = 0
    for instruction in input:
        # pprint(instruction)
        # print (instruction.color, instruction.color[2:-2])
        instruction.moves = int(instruction.color[2:-2], 16)
        direction = int(instruction.color[-2:-1])
        instruction.direction = direction_int_to_c[direction]
        # print(direction, moves)


    for idx, instruction in enumerate(input):
        dx, dy = direction_to_tuple[instruction.direction]
        moves = int(instruction.moves)
        corners.append(((idx + 1) % len(input), x, y))
        x += dx * moves
        y += dy * moves
    corners = sorted(corners, key=lambda pos: (pos[1], pos[2]))
    global min_x
    min_x, max_x = (corners[0][1], corners[-1][1])
    corners = sorted(corners, key=lambda pos: (pos[2], pos[1]))
    global min_y
    min_y, max_y = (corners[0][2], corners[-1][2])
    global print_part2_terrain
    print_part2_terrain = corners[-1][2] < 1000
    if print_part2_terrain:
        global part2_terrain
        part2_terrain = [list(" "* (max_x - min_x + 1)) for _ in range(max_y - min_y + 1)]


    # print('min x,y', min_x, min_y)
    for i, (idx, x, y) in enumerate(corners):
        corners[i] = (idx, x - min_x + x_offset, y - min_y)

    # pprint(corners)

    current_corners = []
    old_corners = []
    last_y = None
    for corner in corners:
        idx, x, y = corner
        if last_y is None or last_y != y:
            # print(current_corners)
            total += handle_corners(old_corners, current_corners)

            current_corners = [corner]
            last_y = y

            continue
        current_corners.append(corner)
    if len(current_corners) > 0:
        total += handle_corners(old_corners, current_corners)
    # if print_part2_terrain:
    #     print('part2_terrain')
    #     print_terrain(part2_terrain)
    return total

class AdventOfCode(unittest.TestCase):
    def setUp(self) -> None:
        script_dir = os.path.dirname(sys.argv[0])
        if len(script_dir) > 0:
            script_dir += '/'


        self.input_set = [
            # load_input(script_dir + "example2.txt", 146, 146),
            load_input(script_dir + "example1.txt", 62, 952408144115),
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
