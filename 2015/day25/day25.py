#!/usr/bin/env python3
from utilday25 import *

class TodaysInput(Input):
    def extra_parsing(self):
        m = re.findall('[0-9]+', self.line)
        self.row, self.col = list(map(int, m))

def get_seq_number(row, col):
    start_row = row + col
    # Formula for 1 + 2 + 3 + 4 ...
    start_seq = start_row * (start_row + 1) // 2
    return start_seq + col

def get_code(seq):
    code = 20151125
    mult = pow(252533, seq, 33554393)
    return code * mult % 33554393

def part1(inputs: List[TodaysInput]):
    total = 0
    # for row in range(6):
    #     for col in range(6):
    #         print(f'{get_code(get_seq_number(row, col)): 10}', end='')
    #     print()

    # Algorithms written for 0 based index, but input given as 1 based index
    total = get_code(get_seq_number(inputs[0].row - 1, inputs[0].col - 1))

    return total


class TodaysAdventOfCode(AdventOfCode):
    input_class = TodaysInput
    def test_part1(self):
        self.load_test_inputs("example1.txt", "input1.txt")
        self.run_part(part1, 31663883)

TodaysAdventOfCode.run_tests()
