#!/usr/bin/env python3
from utilday8 import *

class TodaysInput(Input):
    def extra_parsing(self):
        inner = self.line[1:-1]
        assert(self.line == f'"{inner}"')
        slash = None
        hex_str = None
        encoded = ''
        for c in inner:
            if hex_str is not None:
                hex_str += c
                if len(hex_str) >= 2:
                    encoded += chr(int(hex_str, 16))
                    hex_str = None
            elif slash == '\\':
                slash = None
                if c in '\\\"\'':
                    encoded += c
                    slash = None
                    continue
                else:
                    assert(c == 'x')
                    hex_str = ''
                    continue
            elif c == '\\':
                slash = c
            else:
                encoded += c
        self.encoded = encoded

    def encode(self):
        encoded = re.sub(r'([\\\'\"])', r'\\\1', self.line)
        return f'"{encoded}"'

    def char_diff1(self):
        return len(self.line) - len(self.encoded)

    def char_diff2(self):
        return len(self.encode()) - len(self.line)

def part1(inputs: List[TodaysInput]):
    total = 0
    for input in inputs:
        # print(input)
        total += input.char_diff1()
    return total

def part2(inputs: List[TodaysInput]):
    total = 0
    for input in inputs:
        total += input.char_diff2()
    return total

class TodaysAdventOfCode(AdventOfCode):
    input_class = TodaysInput
    def test_part1(self):
        self.load_test_inputs("example1.txt", "input1.txt")
        self.run_part(part1, 12)

    def test_part2(self):
        self.load_test_inputs("example1.txt", "input1.txt")
        self.run_part(part2, 19)

unittest.main(verbosity=0)
