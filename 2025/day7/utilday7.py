import unittest
import sys
import time
import os
import re

from pprint import pprint, pformat
from typing import List

class Input(object):
    def __init__(self, line: str):
        self.line = line

    def __str__(self):
        return f"<Input {pformat(self.__dict__)}>"

    __repr__ = __str__

class Grid:
    def __init__(self, inputs: List[Input]):
        self.grid = [list(i.line) for i in inputs]
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])

    def __getitem__(self, key):
        return self.grid[key]

    def __str__(self):
        return '\n'.join([''.join(row) for row in self.grid])

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

class AdventOfCode(unittest.TestCase):
    @staticmethod
    def load_input(filename):
        try:
            with open(filename,'r') as f:
                lines = [line.strip() for line in f.readlines()]
        except:
            print("No input file", filename)
            return None
        return [Input(line) for line in lines]

    def setUp(self) -> None:
        script_dir = os.path.dirname(sys.argv[0])
        if len(script_dir) > 0:
            script_dir += '/'

        self.inputs_example = self.load_input(script_dir + "example1.txt")
        self.inputs_mine = self.load_input(script_dir + "input1.txt")

    def run_part(self, part_func, example_answer=None):
        for inputs, expect in [(self.inputs_example, example_answer),
                               (self.inputs_mine, None)]:
            self.assertIsNotNone(inputs)
            answer = part_func(inputs)
            print(f"{part_func.__name__} result", answer)
            if expect is not None:
                self.assertEqual(expect, answer)