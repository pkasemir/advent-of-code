#!/usr/bin/env python3
import unittest
import sys
import os
import re

from pprint import pprint

class Input(object):
    pass

def convert_input(line):
    input = Input()
    input.line = line
    hand, bid = line.split()
    input.hand = (hand, int(bid))
    # print(input.hand, input.bid)
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
    category_shift = 24
    total = 0
    tr = str.maketrans("AKQJT", "EDCBA")
    for hand_obj in input:
        hand, bid = hand_obj.hand
        hand_set = set(hand)
        hand_obj.strength = int(hand.translate(tr), 16)
        hand_obj.strength += (6 - len(hand_set)) << category_shift

        if len(hand_set) == 3:
            for c in hand_set:
                count = hand.count(c)
                if count == 3:
                    # Three of a kind
                    hand_obj.strength += 1 << (category_shift - 1)
                    break
                if count == 2:
                    # Two pair
                    break

            pass
        elif len(hand_set) == 2:
            if hand.count(hand[0]) in [1, 4]:
                # Four of a kind
                hand_obj.strength += 1 << (category_shift - 1)
                pass
            else:
                # Full house
                pass
        # print(hand, bid, hand_set, f'{hand_obj.strength:x}')
    input.sort(key=lambda i: i.strength)
    for i, hand_obj in enumerate(input):
        # print(hand_obj.hand)
        total += (i + 1) * hand_obj.hand[1]

    return total

def part2(input):
    category_shift = 24
    total = 0
    tr = str.maketrans("AKQJT", "EDC1A")
    for hand_obj in input:
        hand, bid = hand_obj.hand
        hand_set = set(hand)
        hand_obj.strength = int(hand.translate(tr), 16)

        if 'J' in hand_set:
            if len(hand_set) > 1:
                hand_set.remove('J')
                joker_char = None
                card_count = 0
                for c in hand_set:
                    count = hand.count(c)
                    if count > card_count:
                        card_count = count
                        joker_char = c
                hand = hand.replace("J", joker_char)

        hand_obj.strength += (6 - len(hand_set)) << category_shift
        if len(hand_set) == 3:
            for c in hand_set:
                count = hand.count(c)
                if count == 3:
                    # Three of a kind
                    hand_obj.strength += 1 << (category_shift - 1)
                    break
                if count == 2:
                    # Two pair
                    break

            pass
        elif len(hand_set) == 2:
            if hand.count(hand[0]) in [1, 4]:
                # Four of a kind
                hand_obj.strength += 1 << (category_shift - 1)
            else:
                # Full house
                pass
        # print(hand, bid, hand_set, f'{hand_obj.strength:x}')
    input.sort(key=lambda i: i.strength)
    for i, hand_obj in enumerate(input):
        # print(hand_obj.hand)
        total += (i + 1) * hand_obj.hand[1]

    return total

class AdventOfCode(unittest.TestCase):
    def setUp(self) -> None:
        script_dir = os.path.dirname(sys.argv[0])
        if len(script_dir) > 0:
            script_dir += '/'

        self.input_set = [
            load_input(script_dir + "example1.txt", 6440, 5905),
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
