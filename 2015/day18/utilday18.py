import sys
import time
import os
import re

from pprint import pprint, pformat
from typing import List, Tuple, Sequence, Dict, Set

# Windows git bash doesn't line buffer
sys.stdout.reconfigure(line_buffering=True) # type: ignore

class Input(object):
    def __init__(self, line: str):
        self.line = line
        self.extra_parsing()

    def extra_parsing(self):
        pass

    @staticmethod
    def from_list(line: str, sep, convert=str):
        return list(map(convert, line.split(sep)))

    def __str__(self):
        return f"<Input {pformat(self.__dict__)}>"

    __repr__ = __str__

class Grid:
    def __init__(self, inputs: Sequence[Input]):
        self.grid = [list(i.line) for i in inputs]
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])

    def __getitem__(self, key):
        return self.grid[key]

    def __str__(self):
        return '\n'.join([''.join(row) for row in self.grid])

    def for_neighbors(self, func, row, col):
        for dr in range(-1, 2):
            n_row = row + dr
            if not (0 <= n_row < self.rows):
                continue
            for dc in range(-1, 2):
                if dr == 0 and dc == 0:
                    # Skip self
                    continue
                n_col = col + dc
                if not (0 <= n_col < self.cols):
                    continue
                neighbor = self[n_row][n_col]
                func(neighbor)

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

class AdventOfCode:
    input_class = Input
    @classmethod
    def load_input(cls, filename):
        try:
            with open(filename,'r') as f:
                lines = [line.strip() for line in f.readlines()]
        except:
            print("No input file", filename)
            return None
        return [cls.input_class(line) for line in lines]

    def load_test_inputs(self, example, input):
        script_dir = os.path.dirname(sys.argv[0])
        if len(script_dir) > 0:
            script_dir += '/'

        if example is None:
            self.inputs_example = None
        else:
            self.inputs_example = self.load_input(script_dir + example)
        self.inputs_mine = self.load_input(script_dir + input)
        self.args_example = ()
        self.args_input = ()

    def set_test_args(self, example, input):
        self.args_example = (example,)
        self.args_input = (input,)

    def run_part(self, part_func, example_answer=None):
        for inputs, args, expect in [(self.inputs_example, self.args_example, example_answer),
                               (self.inputs_mine, self.args_input, None)]:
            if inputs is None:
                continue
            assert(inputs is not None)
            answer = part_func(inputs, *args)
            print(f"{part_func.__name__} result {answer}")
            if expect is not None:
                if expect != answer:
                    print(f"{part_func.__name__} got {answer}, but expect {expect}")
                assert(expect == answer)

    @classmethod
    def run_tests(cls):
        with TimeBlock():
            aoc = cls()
            for method in dir(aoc):
                if method.startswith("test_"):
                    test_func = getattr(aoc, method)
                    test_func()
