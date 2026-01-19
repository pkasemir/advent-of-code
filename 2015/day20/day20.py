#!/usr/bin/env python3
from utilday20 import *

class TodaysInput(Input):
    def extra_parsing(self):
        pass

import math
import sympy
def get_divisors(n):
    divs = []
    # Iterate from 1 up to the square root of n (inclusive)
    for i in range(1, int(math.isqrt(n)) + 1): # Use math.isqrt for better precision
        if n % i == 0:
            divs.append(i)
            # If the divisors are not a pair of the same number (e.g., sqrt of a perfect square)
            if i * i != n:
                divs.append(n // i)
    # Sort the list to have divisors in order
    divs.sort()
    return divs

def part1(inputs: List[TodaysInput], presents):
    # print(presents)
    house = 1
    best = 0
    while True:
        # print(house)
        divisors = sympy.divisors(house)
        house_presents = sum(divisors) * 10
        elves = len(divisors)

        if house_presents > best:
            # print(f'House {house} got {house_presents} presents from {elves} elves')
            best = house_presents
        if house_presents >= presents:
            return house
        house += 1

def part2(inputs: List[TodaysInput], presents):
    # print(presents)
    house = 1
    best = 0
    while True:
        # print(house)
        divisors = sympy.divisors(house)
        divisors = [d for d in divisors if house // d <= 50]
        house_presents = sum(divisors) * 11
        elves = len(divisors)

        if house_presents > best:
            # print(f'House {house} got {house_presents} presents from {elves} elves')
            best = house_presents
        if house_presents >= presents:
            return house
        house += 1
        # if house > 201:
        #     break

class TodaysAdventOfCode(AdventOfCode):
    input_class = TodaysInput
    def test_part1(self):
        self.set_test_args(None, 29000000)
        self.run_part(part1, -1)

    def test_part2(self):
        self.set_test_args(None, 29000000)
        self.run_part(part2, -1)

TodaysAdventOfCode.run_tests()
