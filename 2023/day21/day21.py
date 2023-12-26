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

moves = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]

def part1(input):
    total = 0
    for y, row in enumerate(input):
        start = list(re.finditer('S', row))
        if len(start):
            start_pos = (start[0].start(), y)
            # print('start', start_pos)
            # print('map size', len(input[0]), len(input))
            break
    visited = set()
    odd_steps = []
    even_steps = []
    q = [start_pos]
    if len(input) < 20:
        total_steps = 6
    else:
        total_steps = 64

    for step in range(total_steps + 1):
        next_q = set()
        while len(q):
            pos = q.pop(0)
            visited.add(pos)
            x, y = pos
            if step & 1:
                odd_steps.append(pos)
            else:
                even_steps.append(pos)
            for dx, dy in moves:
                next_x = x + dx
                next_y = y + dy
                if next_x >= len(input[0]) or next_x < 0:
                    continue
                if next_y >= len(input) or next_y < 0:
                    continue
                if input[next_y][next_x] == '#':
                    continue
                next_pos = (next_x, next_y)
                if next_pos in visited:
                    continue
                next_q.add(next_pos)
        q.extend(next_q)
        # print('step', step)
        # pprint(q)
    # print(odd_steps)
    total = len(even_steps)


    return total

def get_direction(x, y):
    d = ''
    if y < 0:
        d += 'N'
    elif y > 0:
        d += 'S'
    if x < 0:
        d += 'W'
    elif x > 0:
        d += 'E'
    return d

def create_map_block(step, pos, next_mod):
    map_block = Input()
    map_block.created = step
    map_block.pos = pos
    map_block.external_steps = {step - map_block.created: set((next_mod,))}
    map_block.step_actions = {}
    map_block.odd_steps = {}
    map_block.even_steps = {}
    return map_block

def part2(input):
    total = 0
    for y, row in enumerate(input):
        start = list(re.finditer('S', row))
        if len(start):
            start_pos = (start[0].start(), y)
            # print('start', start_pos)
            # print('map size', len(input[0]), len(input))
            break
    if len(input) < 20:
        total_step_list = (6, 10, 50, 100, 500, 1000, 5000)
        # total_step_list = (100,)
    else:
        total_step_list = (26501365,)
        # total_step_list = (1000,)

    for total_steps in total_step_list:
        # total_steps += 1
        visited = set()
        map_blocks = {}
        odd_steps = []
        even_steps = []
        final_even_count = 0
        final_odd_count = 0
        last_maps = set()
        active_maps = set()
        final_maps = set()
        all_finished_maps = set()
        external_start_history = []
        found_steady_state = False

        map_block = create_map_block(0, start_pos, start_pos)
        map_blocks[(0, 0)] = map_block
        q = [start_pos]
        for step in range(total_steps + 1):
            next_q = set()
            next_q_external = set()
            while len(q):
                pos = q.pop(0)
                visited.add(pos)
                x, y = pos
                map_x, mod_x = divmod(x, len(input[0]))
                map_y, mod_y = divmod(y, len(input))
                map_pos = (map_x, map_y)
                active_maps.add(map_pos)
                map_block = map_blocks[map_pos]
                map_step = step - map_block.created
                if map_step not in map_block.step_actions:
                    map_block.step_actions[map_step] = set()
                map_block.step_actions[map_step].add((mod_x, mod_y))

                if step & 1:
                    odd_steps.append(pos)
                else:
                    even_steps.append(pos)
                if map_step & 1:
                    map_block.odd_steps[map_step] = map_block.odd_steps.get(map_step, map_block.odd_steps.get(map_step - 2, 0)) + 1
                else:
                    map_block.even_steps[map_step] = map_block.even_steps.get(map_step, map_block.even_steps.get(map_step - 2, 0)) + 1
                for dx, dy in moves:
                    next_x = x + dx
                    next_y = y + dy
                    next_pos = (next_x, next_y)
                    next_map_x, next_mod_x = divmod(next_x, len(input[0]))
                    next_map_y, next_mod_y = divmod(next_y, len(input))
                    if input[next_mod_y][next_mod_x] == '#':
                        continue
                    if next_pos in visited:
                        continue
                    next_map = (next_map_x, next_map_y)
                    next_mod = (next_mod_x, next_mod_y)
                    if next_map in map_blocks:
                        is_external = next_map != map_pos
                        if (is_external):
                            next_q_external.add(next_pos)
                        else:
                            next_q.add(next_pos)
                    else:
                        # print(f'{step} new map block {str(pos):10} {str(next_pos):10} map {str(next_map):10} {str(next_mod):10}')
                        next_map_block = create_map_block(step + 1, next_map, next_mod)
                        # next_map_block.interval = next_map_block.created - map_block.created
                        next_map_block.interval = len(input)
                        map_blocks[next_map] = next_map_block
                        next_q.add(next_pos)
            next_q_external -= next_q
            q.extend(next_q)
            q.extend(next_q_external)
            # map_block.step_actions[step - map_block.created] = next_q.union(next_q_external)
            for next_pos in next_q_external:
                next_x, next_y = next_pos
                next_map_x, next_mod_x = divmod(next_x, len(input[0]))
                next_map_y, next_mod_y = divmod(next_y, len(input))
                next_map = (next_map_x, next_map_y)
                next_mod = (next_mod_x, next_mod_y)
                map_block = map_blocks[next_map]
                step_key = step - map_block.created + 1
                if step_key not in map_block.external_steps:
                    map_block.external_steps[step_key] = set()
                map_block.external_steps[step_key].add(next_mod)
            # print('step', step)
            finished_maps = last_maps - active_maps
            if len(finished_maps):
                # print(step, 'finished', finished_maps)
                for map_pos in finished_maps:
                    map_block = map_blocks[map_pos]
                    map_block.finished = step - map_block.created - 1
                final_maps = final_maps.union(finished_maps)
                all_finished_maps = all_finished_maps.union(final_maps)
                for map_pos in finished_maps:
                    map_x, map_y = map_pos
                    map_block = map_blocks[map_pos]
                    if map_y == 0 and map_x > 0:
                        # print(step, 'check for steady state', final_maps)
                        final_external_positions = ([
                            (p,
                            tuple([
                                (k, tuple(sorted(m.external_steps[k]))) for k in sorted(m.external_steps.keys())
                            ])
                            )
                            for p, m in [((p, map_blocks[p].created), map_blocks[p]) for p in final_maps]
                        ])
                        # pprint((final_external_positions))

                        final_external_start_and_count = set([(v, p[1], [v for p, v in final_external_positions].count(v)) for p, v in final_external_positions])
                        # pprint(final_external_start_and_count)
                        # print('len list', len(final_external_positions), 'len set', len(final_external_start_and_count))
                        external_start_history.append(len(final_external_start_and_count))
                        if len(external_start_history) > 2:
                            if [len(final_external_start_and_count) == l for l in external_start_history].count(False) == 0:
                                # print('found steady state')
                                found_steady_state = True
                                break

                            external_start_history.pop(0)

                        final_maps = set()
            if found_steady_state:
                break

            last_maps = active_maps
            active_maps = set()
            # pprint(q)
        if step != total_steps:
            steps_left = total_steps - step
            # print("do more", steps_left)
            final_map_dict = {}
            for map_pos in final_maps:
                final_map_dict[get_direction(*map_pos)] = map_blocks[map_pos]
            final_even_count = 0
            final_odd_count = 0
            for map_pos in all_finished_maps:
                map_block = map_blocks[map_pos]
                odd_key = max(map_block.odd_steps.keys())
                even_key = max(map_block.even_steps.keys())
                odd_count = map_block.odd_steps[odd_key]
                even_count = map_block.even_steps[even_key]
                if map_block.created & 1:
                    final_even_count += odd_count
                    final_odd_count += even_count
                else:
                    final_even_count += even_count
                    final_odd_count += odd_count
                # final_even_count += map_even_steps
                # print('finished', map_pos, map_block, odd_key, even_key)

            # print('steps', total_steps, 'finished even', final_even_count)

            for direction, map_block in final_map_dict.items():
                steps_left_from_created = total_steps - map_block.created
                current_step = map_block.created + map_block.interval
                odd_key = max(map_block.odd_steps.keys())
                even_key = max(map_block.even_steps.keys())
                odd_count = map_block.odd_steps[odd_key]
                even_count = map_block.even_steps[even_key]
                # print(direction, map_block.pos, map_block.created, steps_left_from_created)
                do_corner = len(direction) == 2
                corner_count = sum(map(abs, map_block.pos)) - 1

                while current_step <= total_steps:
                    if current_step & 1:
                        map_evenness = "odd"
                        map_odd_steps = map_block.even_steps
                        map_even_steps = map_block.odd_steps
                        max_odd_count = even_count
                        max_even_count = odd_count
                    else:
                        map_evenness = "even"
                        map_even_steps = map_block.even_steps
                        map_odd_steps = map_block.odd_steps
                        max_even_count = even_count
                        max_odd_count = odd_count

                    even_to_add = 0
                    odd_to_add = 0
                    if current_step + map_block.finished < total_steps:
                        even_to_add += max_even_count
                        odd_to_add += max_odd_count
                    else:
                        sub_step = total_steps - current_step
                        if sub_step not in map_even_steps.keys():
                            sub_step -= 1
                        if sub_step >= 0:
                            even_to_add = map_even_steps[sub_step]
                        sub_step = total_steps - current_step
                        if sub_step not in map_odd_steps.keys():
                            sub_step -= 1
                        if sub_step >= 0:
                            odd_to_add = map_odd_steps[sub_step]
                    if do_corner:
                        corner_count += 1
                        even_to_add *= corner_count
                        odd_to_add *= corner_count
                    final_even_count += even_to_add
                    final_odd_count += odd_to_add
                    # print("adding", current_step, map_evenness, '+even', even_to_add, "+odd", odd_to_add, do_corner, corner_count)
                    current_step += map_block.interval

        if total_steps & 1:
            evenness = 'odd'
        else:
            evenness = 'even'
        if final_even_count:
            if evenness == 'even':
                total = final_even_count
            else:
                total = final_odd_count
            print('steps', total_steps, 'final extrapolated', evenness, total)
        else:
            if evenness == 'even':
                total = len(even_steps)
            else:
                total = len(odd_steps)
            print('steps', total_steps, 'final', evenness, total)
    # print(odd_steps)
    # pprint(map_blocks)
    return total

class AdventOfCode(unittest.TestCase):
    def setUp(self) -> None:
        script_dir = os.path.dirname(sys.argv[0])
        if len(script_dir) > 0:
            script_dir += '/'

        self.input_set = [
            load_input(script_dir + "example1.txt", 16, 16733044),
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
