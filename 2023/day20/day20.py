#!/usr/bin/env python3
import graphviz
import unittest
import sys
import time
import os
import re
import math

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
    module, outputs = line.replace(' ', '').split('->')
    input.module = module[0]
    if input.module == 'b':
        input.name = module
    else:
        input.name = module[1:]
    input.outputs = outputs.split(',')
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

broadcaster = 'broadcaster'
flipflop = '%'
conjunction = '&'

def process_broadcaster(modules, module, source, pulse):
    key = ('b', pulse)
    if False and key in module.cache:
        return module.cache[key]
    next_items = [(modules[name], module, pulse) for name in module.outputs]
    # for name in module.outputs:
    #     print(f"{module.name} -{'high' if pulse else 'low'}-> {name}") #  src {source.name}")
    module.cache[key] = next_items
    return next_items

def process_flipflop(modules, module, source, pulse):
    if pulse:
        return []
    key = ('ff', module.state)
    if False and key in module.cache:
        module.state, next_items = module.cache[key]
    else:
        module.state = (1 - module.state[0],)
        next_items =  process_broadcaster(modules, module, source, module.state[0])
        module.cache[key] = (module.state, next_items)
    return next_items

def process_conjunction(modules, module, source, pulse):
    key = ('c', source.name, module.state)
    if False and key in module.cache:
        module.state, next_items = module.cache[key]
    else:
        module.state = list(module.state)
        for i, name in enumerate(module.inputs):
            if name == source.name:
                module.state[i] = pulse
                break
        module.state = tuple(module.state)
        pulse = 1 if sum(module.state) != len(module.state) else 0
        next_items =  process_broadcaster(modules, module, source, pulse)
        module.cache[key] = (module.state, next_items)
    return next_items

def get_module_map(input):
    modules = {}
    inputs = {}
    for module in input:
        modules[module.name] = module
        for output in module.outputs:
            l = inputs.get(output, [])
            inputs[output] = l
            l.append(module.name)
    for name, vals in inputs.items():
        if name not in modules:
            endpoint = Input()
            endpoint.name = name
            endpoint.module = 'sink'
            endpoint.outputs = []
            endpoint.process = lambda *args: []
            modules[name] = endpoint
        modules[name].inputs = vals
    for module in input:
        if module.module == flipflop:
            module.process = process_flipflop
            module.state = (0,)
        elif module.module == conjunction:
            module.process = process_conjunction
            module.state = (0,) * len(module.inputs)
        else:
            module.process = process_broadcaster
            module.state = ()
        module.cache = {}
    return modules

def part1(input):
    total = 0
    button = Input()
    button.name = 'button'
    modules = get_module_map(input)
    low_pulse_count = 0
    high_pulse_count = 0
    # pprint(modules)
    for _ in range(1000):
        low_pulse_count += 1
        q = [(modules[broadcaster], button, 0)]
        while len(q):
            module, source, pulse = q.pop(0)
            # print(module)
            next_items = module.process(modules, module, source, pulse)
            q.extend(next_items)
            for _, _, pulse in next_items:
                if pulse:
                    high_pulse_count += 1
                else:
                    low_pulse_count += 1

            # print(next_items)
    # print('low', low_pulse_count, 'high', high_pulse_count)
    total = low_pulse_count * high_pulse_count

    return total

def process_print_conjunction(modules, module, source, pulse):
    next_items = process_conjunction(modules, module, source, pulse)
    if not next_items[0][2]:
        states = list(zip(module.inputs, module.state))
        distance = button_press - module.last_success
        # print(f'{distance} {button_press} {source.name} {pulse}-> {module.name} {states}')
        module.last_success = button_press
        module.distance = distance
    return next_items

def make_graph(modules):
    dot = graphviz.Digraph(comment='The Round Table')
    for module in modules.values():
        dot.node(module.name, f'{module.module} {module.name}')
        for name in module.outputs:
            dot.edge(module.name, name)
    dot.render("day20graph")
    print(dot.source)
    exit(1)


def part2(input):
    total = 0
    button = Input()
    button.name = 'button'
    modules = get_module_map(input)
    if 'rx' not in modules:
        return -1
    # make_graph(modules)
    hub_modules = []
    for module in modules.values():
        if len(module.outputs) > 4:
            # print('large module', module.name)
            modules[module.name].process = process_print_conjunction
            module.last_success = 0
            hub_modules.append(module)
    global button_press
    for i in range(1000000):
        button_press = i + 1
        q = [(modules[broadcaster], button, 0)]
        while len(q):
            module, source, pulse = q.pop(0)
            # print(module)
            next_items = module.process(modules, module, source, pulse)
            q.extend(next_items)

            # print(next_items)
        if sum([1 for module in hub_modules if module.last_success == 0]) == 0:
            break
    total = math.lcm(*[module.distance for module in hub_modules])

    return total

class AdventOfCode(unittest.TestCase):
    def setUp(self) -> None:
        script_dir = os.path.dirname(sys.argv[0])
        if len(script_dir) > 0:
            script_dir += '/'

        self.input_set = [
            load_input(script_dir + "example1.txt", 32000000, -1),
            load_input(script_dir + "example2.txt", 11687500, -1),
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
