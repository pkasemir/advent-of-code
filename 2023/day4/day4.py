import unittest
import sys
import os
import re

class Input(object):
    pass

def convert_input(line):
    input = Input()
    input.line = line
    input.count = 1
    _, numbers = line.split(':')
    winning, mine = numbers.split('|')
    input.winning = list(map(int, winning.split()))
    input.mine = list(map(int, mine.split()))
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

def part1(input):
    total = 0
    for card in input:
        points = None
        for num in card.mine:
            if num in card.winning:
                # print("win", num)
                if not points:
                    points = 1
                else:
                    points <<= 1
        if points:
            total += points
    return total
    
def part2(input):
    total = 0
    for card_idx, card in enumerate(input):
        wins = 0
        for num in card.mine:
            if num in card.winning:
                wins += 1
        # print("card", card_idx + 1, wins, card.count)
        for idx in range(wins):
            input[idx + card_idx + 1].count += card.count
        total += card.count
    return total

class AdventOfCode(unittest.TestCase):
    def setUp(self) -> None:
        script_dir = os.path.dirname(sys.argv[0])
        if len(script_dir) > 0:
            script_dir += '/'

        self.input_set = [
            load_input(script_dir + "example1.txt", 13, 30),
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
