import unittest
import sys
import os
import re

from pprint import pprint

def load_input(filename, solution_p1=None, solution_p2=None):
    try:
        with open(filename,'r') as f:
            lines = [line.strip() for line in f.readlines()]
    except:
        print("No input file", filename)
        return None
    input_map = {}
    for line in lines:
        if not line:
            continue
        s = line.split(':')
        if s[0] == "seeds":
            input_map[s[0]] = list(map(int, s[1].split()))
            # print("seeds")
        elif m := re.match("([^-]+)-to-([^ ]+) map", line):
            src, dst = m.groups()
            current_map = []
            input_map[src] = {dst:current_map}
        else:
            current_map.append(list(map(int, line.split())))
            current_map.sort(key=lambda x: x[1])

    # pprint(input_map)
    return (input_map, solution_p1, solution_p2)


def lookup_location(input_map, key, value):
    next_value = None
    for next_key, range_list in input_map[key].items():
        for dst, src, count in range_list:
            # print(next_key, src, dst, count)
            if value >= src and value < src + count:
                next_value = dst + value - src
                break
        break
    if next_value is None:
        next_value = value
    # print ("found", next_key, next_value)
    if next_key == 'location':
        return next_value
    else:
        return lookup_location(input_map, next_key, next_value)


def part1(input):
    locations = []
    for seed in input['seeds']:
        # print(seed)
        locations.append(lookup_location(input, 'seed', seed))
    # print(locations)
    return(min(locations))

def lookup_location2(input_map, key, key_begin, key_count):
    values = []
    # print("lookup", key, key_begin, key_count)
    if key == 'location':
        values.append(key_begin)
        # print("location", key_begin)
        return values
    for next_key, range_list in input_map[key].items():
        for dst, src, count in range_list:
            if key_begin < src:
                # print("begin before")
                before_count = min(key_count, src - key_begin)
                values.extend(lookup_location2(input_map, next_key, key_begin, before_count))
                key_begin = src
                key_count -= before_count
                if key_count == 0:
                    return values
            int_begin = max(src, key_begin)
            int_end = min(src + count, key_begin + key_count)
            int_count = int_end - int_begin
            if int_count <= 0:
                continue
            # print("intersect", key_begin, key_count, key_begin + key_count, "with", src, count, src + count, "offset", dst - src, "gives", int_begin, int_count, int_end)

            values.extend(lookup_location2(input_map, next_key, dst + int_begin - src, int_count))
            key_begin = int_end - 1
            key_count -= int_count
            if key_count == 0:
                return values
        break
    if key_count > 0:
        # print("values after")
        values.extend(lookup_location2(input_map, next_key, key_begin, key_count))

    return values

def part2(input):
    locations = []
    seed_iter = iter(input['seeds'])
    for seed in seed_iter:
        count = next(seed_iter)
        # print(seed, count)
        locations.extend(lookup_location2(input, 'seed', seed, count))
    # print(locations)
    return(min(locations))

class AdventOfCode(unittest.TestCase):
    def setUp(self) -> None:
        script_dir = os.path.dirname(sys.argv[0])
        if len(script_dir) > 0:
            script_dir += '/'

        self.input_set = [
            load_input(script_dir + "example1.txt", 35, 46),
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
