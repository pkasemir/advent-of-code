#!/usr/bin/env python3
from utilday14 import *

class TodaysInput(Input):
    def extra_parsing(self):
        m = re.match('(.*) can fly (.*) km/s for (.*) seconds, but then must rest for (.*) seconds.', self.line)
        assert(m)
        self.name, speed, length, rest = m.groups()
        self.speed = int(speed)
        self.length = int(length)
        self.rest = int(rest)
        self.cycle_distance = self.speed * self.length
        self.cycle_time = self.length + self.rest

        self.points = 0
        self.distance = 0
        self.rest_left = 0
        self.fly_left = self.length

    def next_second(self):
        if self.rest_left > 0:
            self.rest_left -= 1
            if self.rest_left == 0:
                self.fly_left = self.length
        elif self.fly_left > 0:
            self.fly_left -= 1
            self.distance += self.speed
            if self.fly_left == 0:
                self.rest_left = self.rest
        # print(self.name, self.fly_left, self.rest_left, self.distance)
        return self.distance

def calculate_distance(deer: TodaysInput, seconds):
    distance = 0
    full_cycles = seconds // deer.cycle_time
    distance = full_cycles * deer.cycle_distance
    seconds -= full_cycles * deer.cycle_time
    distance += min(deer.speed * seconds, deer.cycle_distance)
    return distance

def part1(inputs: List[TodaysInput], seconds):
    total = 0
    # print('seconds', seconds)
    distances = [calculate_distance(i, seconds) for i in inputs]
    total = max(distances)
    return total

def part2(inputs: List[TodaysInput], seconds):
    total = 0
    # print('seconds', seconds)
    for s in range(1, seconds + 1):
        # print(s)
        farthest_deer = inputs[0]
        for deer in inputs:
            distance = deer.next_second()
            if distance >= farthest_deer.distance:
                farthest_deer = deer
        farthest_deer.points += 1
        # print(s, " ".join([f'{d.name}:{d.points}' for d in inputs]))

    fastest_deer = inputs[0]
    for deer in inputs:
        if deer.points > fastest_deer.points:
            fastest_deer = deer
    total = fastest_deer.points
    return total

class TodaysAdventOfCode(AdventOfCode):
    input_class = TodaysInput
    def test_part1(self):
        self.load_test_inputs("example1.txt", "input1.txt")
        self.set_test_args(1000, 2503)
        self.run_part(part1, 1120)

    def test_part2(self):
        self.load_test_inputs("example1.txt", "input1.txt")
        self.set_test_args(1000, 2503)
        self.run_part(part2, 689)

TodaysAdventOfCode.run_tests()
