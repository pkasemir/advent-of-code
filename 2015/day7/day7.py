#!/usr/bin/env python3
from utilday7 import *

class TodaysInput(Input):
    def extra_parsing(self):
        m = re.match('([^ ]+) ?([^ ]+)? ?([^ ]+)? -> (.*)', self.line)
        assert(m)
        i0, i1, i2, self.output = m.groups()
        if i0 == 'NOT':
            self.gate = i0
            self.inputs = [i1]
        elif i2 is not None:
            self.gate = i1
            if self.gate in ['AND', 'OR']:
                pass
            elif self.gate in ['LSHIFT', 'RSHIFT']:
                i2 = int(i2)
            else:
                assert(False)
            self.inputs = [i0, i2]
        elif i1 is not None:
            assert(False)
        else:
            self.gate = 'WIRE'
            self.inputs = [i0]

        for i in range(len(self.inputs)):
            try:
                self.inputs[i] = int(self.inputs[i])
            except:
                pass

        self.value = None

actions = {
    'AND': lambda x: x[0] & x[1],
    'OR': lambda x: x[0] | x[1],
    'LSHIFT': lambda x: x[0] << x[1],
    'RSHIFT': lambda x: x[0] >> x[1],
    'NOT': lambda x: (~x[0]) & 0xffff,
    'WIRE': lambda x: x[0],
}

def get_wire_value(circuit, wire):
    item: TodaysInput = circuit[wire]
    if item.value is not None:
        return item.value
    inputs = [i if isinstance(i, int) else get_wire_value(circuit, i) for i in item.inputs]
    item.value =  actions[item.gate](inputs)
    # print(item.output, item.value)
    return item.value

def part1(inputs: List[TodaysInput]):
    wire = 'i' if len(inputs) < 10 else 'a'
    circuit = {i.output: i for i in inputs}
    total = get_wire_value(circuit, wire)
    return total

def part2(inputs: List[TodaysInput]):
    wire = 'a'
    circuit = {i.output: i for i in inputs}
    a_value = get_wire_value(circuit, wire)
    for input in inputs:
        input.value = None
        if input.output == 'b':
            input.inputs = [a_value]
    total = get_wire_value(circuit, wire)
    return total

class TodaysAdventOfCode(AdventOfCode):
    input_class = TodaysInput
    def test_part1(self):
        self.load_test_inputs("example1.txt", "input1.txt")
        self.run_part(part1, 65079) # i output

    def test_part2(self):
        self.load_test_inputs(None, "input1.txt")
        self.run_part(part2, -1)

unittest.main(verbosity=0)
