#!/usr/bin/env python3
from utilday23 import *

class TodaysInput(Input):
    def extra_parsing(self):
        p = self.line.replace(',', '').split()
        self.instruction = p[0]
        self.register = p[1]
        self.offset = 0
        if self.instruction[0] == 'j':
            self.offset = int(p[-1])

class Computer:
    def __init__(self, instructions: List[TodaysInput]) -> None:
        self.instructions = instructions
        self.pc = 0
        self.registers = dict(a=0, b=0)

    def ins_hlf(self, r, offset):
        self.registers[r] >>= 1
        return 1

    def ins_tpl(self, r, offset):
        self.registers[r] *= 3
        return 1

    def ins_inc(self, r, offset):
        self.registers[r] += 1
        return 1

    def ins_jmp(self, r, offset):
        return offset

    def ins_jie(self, r, offset):
        if self.registers[r] & 1 == 0:
            return offset
        return 1

    def ins_jio(self, r, offset):
        if self.registers[r] == 1:
            return offset
        return 1

    def run(self):
        while 0 <= self.pc < len(self.instructions):
            instruction = self.instructions[self.pc]
            # print(self.pc, instruction.line)
            ins_func = getattr(self, 'ins_' + instruction.instruction)
            self.pc += ins_func(instruction.register, instruction.offset)
            # print(self.pc, self.registers)

def part1(inputs: List[TodaysInput]):
    cpu = Computer(inputs)
    cpu.run()
    return cpu.registers['b']

def part2(inputs: List[TodaysInput]):
    cpu = Computer(inputs)
    cpu.registers['a'] = 1
    cpu.run()
    return cpu.registers['b']

class TodaysAdventOfCode(AdventOfCode):
    input_class = TodaysInput
    def test_part1(self):
        self.load_test_inputs("example1.txt", "input1.txt")
        self.run_part(part1, 0)

    def test_part2(self):
        self.load_test_inputs(None, "input1.txt")
        self.run_part(part2, -1)

TodaysAdventOfCode.run_tests()
