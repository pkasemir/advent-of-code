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
    return input

def load_input(filename, solution_p1=None, solution_p2=None):
    try:
        with open(filename,'r') as f:
            lines = [line.strip() for line in f.readlines()]
    except:
        print("No input file", filename)
        return None
    inputs = [convert_input(line) for line in lines]

    flows = {}
    parts= []
    lines_iter = iter(lines)
    def make_func(rule):
        rule = rule.split(":")
        rule_item = Input()
        if len(rule) == 1:
            rule_item.member = 'x'
            rule_item.threshold = 0
            rule_item.use_gt = True
            rule_item.target = rule[0]
            def always_send(part):
                return rule_item.target
            rule_item.func = always_send
            return rule_item
        rule_item.use_gt = '>' in rule[0]
        rule_item.member = rule[0][0]
        rule_item.threshold = int(rule[0][2:])
        rule_item.target = rule[1]
        def check_thresh(part):
            if rule_item.use_gt:
                if part[rule_item.member] > rule_item.threshold:
                    return rule_item.target
            else:
                if part[rule_item.member] < rule_item.threshold:
                    return rule_item.target
            return None
        rule_item.func = check_thresh
        return rule_item

    for line in lines_iter:
        if len(line) == 0:
            break
        name, rules = line.split('{')
        rules = rules.strip('}').split(',')
        rules = [make_func(r) for r in rules]
        flows[name] = rules

    for line in lines_iter:
        members = line.strip('{}').split(',')

        part = {}
        for member in members:
            k, v = member.split('=')
            part[k] = int(v)
        parts.append(part)

    inputs = (flows, parts)

    return (inputs, solution_p1, solution_p2)

def process_rules(flows, flow_name, part):
    # print(flow_name)
    rules = flows[flow_name]
    for rule in rules:
        flow_name = rule.func(part)
        if flow_name is not None:
            break
    return flow_name

starting_flow = 'in'

def process_flows(flows, part):
    flow_name = starting_flow
    while flow_name not in ['R', 'A']:
        flow_name = process_rules(flows, flow_name, part)
    return flow_name

def get_part_sum(part):
    return sum([part[k] for k in 'xmas'])

def part1(input):
    total = 0
    flows, parts = input

    for part in parts:
        flow_name = process_flows(flows, part)
        # print(flow_name)
        if flow_name == 'A':
            total += get_part_sum(part)
    return total

def get_combinations(item):
    combinations = 1
    for c in 'xmas':
        member_low, member_high = getattr(item, c)
        count = member_high - member_low + 1
        combinations *= count
    return combinations

def part2(input):
    total = 0
    flows, _ = input

    min_val = 1
    max_val = 4000
    item = Input()
    item.flow_name = starting_flow
    item.path = (item.flow_name,)
    for c in 'xmas':
        setattr(item, c, [min_val, max_val])
    q = [item]
    while len(q) > 0:
        item = q.pop(0)
        # print('Pre combinations', get_combinations(item), item.path)
        if item.flow_name in ['R', 'A']:
            # print("Finished", item.path)
            if item.flow_name == 'A':
                # print("calc", item)
                combinations = get_combinations(item)
                # print("Adding combinations", combinations, item.path)
                total += combinations
            continue
        for rule in flows[item.flow_name]:
            # print(item)
            # print(rule)
            member_low, member_high = getattr(item, rule.member)
            r1 = [member_low, rule.threshold]
            r2 = [rule.threshold, member_high]
            if rule.use_gt:
                # print('gt', getattr(item, rule.member))
                r2[0] += 1
                r_true = r2
                r_false = r1
            else:
                # print('lt', getattr(item, rule.member))
                r1[1] -= 1
                r_true = r1
                r_false = r2
            r1[1] = min(r1[1], member_high)
            r2[0] = max(r2[0], member_low)

            # print("true", r_true)
            # print('false', r_false)
            if r_true[0] <= r_true[1]:
                # print("queue up", rule.target)
                next_item = Input()
                next_item.flow_name = rule.target
                next_item.path = item.path + (next_item.flow_name,)
                for c in 'xmas':
                    setattr(next_item, c, getattr(item, c))
                setattr(next_item, rule.member, r_true)
                q.append(next_item)
            if r_false[0] > r_false[1]:
                break
            setattr(item, rule.member, r_false)

    return total

class AdventOfCode(unittest.TestCase):
    def setUp(self) -> None:
        script_dir = os.path.dirname(sys.argv[0])
        if len(script_dir) > 0:
            script_dir += '/'

        self.input_set = [
            load_input(script_dir + "example1.txt", 19114, 167409079868000),
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
