#!/usr/bin/env python3
from utilday4 import *

import hashlib

class TodaysInput(Input):
    def extra_parsing(self):
        pass

def get_num(line, prefix = '0' * 5):
    num = 0
    while True:
        ctx = hashlib.md5(string=f'{line}{num}'.encode('utf-8'))
        result = ctx.hexdigest()
        if re.match(prefix, result):
            return num
        num += 1


def part1(inputs: List[TodaysInput]):
    total = 0
    total = get_num(inputs[0].line)
    return total

def part2(inputs: List[TodaysInput]):
    total = 0
    total = get_num(inputs[0].line, '0' * 6)
    return total

class TodaysAdventOfCode(AdventOfCode):
    input_class = TodaysInput
    def test_part1(self):
        self.run_part(part1, 609043)

    def test_part2(self):
        self.run_part(part2, 6742839)

unittest.main(verbosity=0)
