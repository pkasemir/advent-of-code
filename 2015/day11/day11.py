#!/usr/bin/env python3
from utilday11 import *

class TodaysInput(Input):
    def extra_parsing(self):
        pass

class Password(str):
    start_val = ord('a')
    end_val = ord('z')
    invalid_chars = "iol"
    invalid_vals = tuple(map(ord, invalid_chars))

    def next(self):
        is_valid = False
        r_vals = list(map(ord, reversed(self)))
        while not is_valid:
            # print("".join(map(chr, reversed(r_vals))))

            to_add = 1
            for i, c in enumerate(r_vals):
                # print(chr(c))
                c += to_add
                if c in self.invalid_vals:
                    c += 1
                    r_vals[:i] = [self.start_val] * i

                if c > self.end_val:
                    c = self.start_val
                    to_add = 1
                else:
                    to_add = 0

                r_vals[i] = c
            if to_add == 1:
                r_vals.append(self.start_val)

            # Check for increasing
            last = self.end_val
            increasing_count = 1
            for v in reversed(r_vals):
                if v - last == 1:
                    increasing_count += 1
                    if increasing_count >= 3:
                        is_valid = True
                        break
                else:
                    increasing_count = 1
                last = v

            # check for pairs
            if is_valid:
                last = None
                pair_count = 0
                for v in r_vals:
                    if v == last:
                        last = None
                        pair_count += 1
                        if pair_count >= 2:
                            break
                    else:
                        last = v
                is_valid = pair_count >= 2

        return Password("".join(map(chr, reversed(r_vals))))

def part1(inputs: List[TodaysInput]):
    total = 0
    for input in inputs:
        # print(input)
        p = Password(input.line)
        total = p.next()
        # print(p, total)

    return total

def part2(inputs: List[TodaysInput]):
    total = 0
    for input in inputs:
        p = Password(input.line)
        total = p.next().next()
    return total

class TodaysAdventOfCode(AdventOfCode):
    input_class = TodaysInput
    def test_part1(self):
        self.load_test_inputs("example1.txt", "input1.txt")
        self.run_part(part1, 'ghjaabcc')

    def test_part2(self):
        self.load_test_inputs(None, "input1.txt")
        self.run_part(part2, -1)

TodaysAdventOfCode.run_tests()
