#!/usr/bin/env python3
from utilday18 import *

class TodaysInput(Input):
    def extra_parsing(self):
        pass

class Lights(Grid):
    def toggle(self, row, col):
        c = '#' if self[row][col] == '.' else '.'
        self[row][col] = c

def count_lights(inputs: List[TodaysInput], steps, is_part2=False):
    total = 0
    # print('steps', steps)
    # for input in inputs:
    #     print(input)
    lights = Lights(inputs)
    corners = ((0, 0),
               (lights.rows - 1, 0),
               (0, lights.cols - 1),
               (lights.rows - 1, lights.cols - 1),
               )
    if is_part2:
        for row, col in corners:
            lights[row][col] = '#'
    # print(lights)
    for _ in range(steps):
        toggles = []
        for row in range(lights.rows):
            for col in range(lights.cols):
                if is_part2 and (row, col) in corners:
                    continue
                neighbors_on = 0
                def count_on(neighbor):
                    nonlocal neighbors_on
                    # print(neighbor)
                    if neighbor == '#':
                        neighbors_on += 1
                lights.for_neighbors(count_on, row, col)
                # print(neighbors_on)
                # print()
                if lights[row][col] == '#':
                    if neighbors_on not in [2, 3]:
                        toggles.append((row, col))
                else:
                    if neighbors_on == 3:
                        toggles.append((row, col))
        # pprint(toggles)
        # print()
        for row, col in toggles:
            lights.toggle(row, col)

        # print(lights)

    for row in range(lights.rows):
        for col in range(lights.cols):
            if lights[row][col] == '#':
                total += 1

    return total

def part1(inputs: List[TodaysInput], steps):
    total = 0
    total = count_lights(inputs, steps)
    return total

def part2(inputs: List[TodaysInput], steps):
    total = 0
    total = count_lights(inputs, steps, is_part2=True)
    return total

class TodaysAdventOfCode(AdventOfCode):
    input_class = TodaysInput
    def test_part1(self):
        self.load_test_inputs("example1.txt", "input1.txt")
        self.set_test_args(4, 100)
        self.run_part(part1, 4)

    def test_part2(self):
        self.load_test_inputs("example1.txt", "input1.txt")
        self.set_test_args(5, 100)
        self.run_part(part2, 17)

TodaysAdventOfCode.run_tests()
