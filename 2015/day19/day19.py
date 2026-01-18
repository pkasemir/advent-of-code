#!/usr/bin/env python3
from utilday19 import *

class TodaysInput(Input):
    def extra_parsing(self):
        pass

def to_element_list(molecule:str):
    elements = []
    i = 0
    while i < len(molecule):
        if i + 1 >= len(molecule):
            elements.append(molecule[i])
            break
        if molecule[i + 1].islower():
            elements.append(molecule[i:i+2])
            i += 1
        else:
            elements.append(molecule[i])
        i += 1
    return elements

def get_replacements(inputs: List[TodaysInput], reverse=False):
    replacements = {}
    for input in inputs:
        s = input.line.split(' => ')
        if len(s) == 1:
            break
        if reverse:
            replacements[tuple(to_element_list(s[1]))] = s[0]
        else:
            replacements.setdefault(s[0], []).append(to_element_list(s[1]))

        # print(input)
    return replacements

def get_possible_molecules(molecule, replacements):
    molecules = set()
    for i, element in enumerate(molecule):
        if element not in replacements:
            continue
        for r in replacements[element]:
            my_molecule = do_replacement(molecule, slice(i, i+1), r)
            # print(element, r, my_molecule)
            molecules.add(tuple(my_molecule))
    # pprint(molecules)
    return molecules

def part1(inputs: List[TodaysInput]):
    total = 0
    replacements = get_replacements(inputs)
    molecule = to_element_list(inputs[-1].line)
    # pprint(replacements)
    # print(molecule)
    total = len(get_possible_molecules(molecule, replacements))

    return total

def do_replacement(parent, p_slice:slice, replace):
    replacement = (*parent[:p_slice.start], *replace, *parent[p_slice.stop:])
    return replacement

# parse using a modified CYK algorithm
def parse_grammar(inputs: List[TodaysInput]):
    replacements = get_replacements(inputs, reverse=True)
    molecule = to_element_list(inputs[-1].line)
    # pprint(replacements)

    # Expand the replacement to get minimal production rules Ra => Rb Rc
    min_replacements = {}
    for prod, input in replacements.items():
        while len(prod) > 2:
            new_prod = (prod[1], prod[2])
            # Add reduction rule with x prefix so we don't count it as a real step
            new_input = 'x' + prod[1] + prod[2]
            min_replacements[new_prod] = new_input
            prod = (prod[0], new_input, *prod[3:])

        min_replacements[prod] = input
    # pprint(min_replacements)

    # Run CYK algorithm
    P = [[set([e]) for e in molecule]]
    back = [[{} for e in molecule]]
    for l in range(1, len(molecule)):
        layer = []
        P.append(layer)
        b_layer = []
        back.append(b_layer)
        for s in range(len(molecule) - l):
            span = set()
            layer.append(span)
            b_span = {}
            b_layer.append(b_span)
            for p in range(l):
                for e1 in  P[p][s]:
                    for e2 in P[l-p - 1][s+p +1]:
                        if (e1, e2) in min_replacements:
                            e_from = min_replacements[(e1, e2)]
                            span.add(e_from)
                            b_span.setdefault(e_from, []).append((p, e1, e2))

    # for l in P:
    #     print(l)
    # print()
    # for l in back:
    #     print(l)

    def get_backtrace(e, l, s):
        # print('backtrace', e, 'l', l, 's', s)
        for p, b, c in back[l][s].get(e, []):
            # print('e', e, 'p', p, 's', s, 'b', b, 'c', c)
            b1, s1 = get_backtrace(b, p, s)
            b2, s2 = get_backtrace(c, l-p - 1, s+p +1)

            if e[0] == 'x':
                my_steps = 0
            else:
                my_steps = 1
            return b1 + b2, my_steps + s1 + s2
        return e.replace('x', ''), 0

    final_element = list(back[-1][0].keys())[0]
    reproduce, steps = get_backtrace(final_element, len(back) - 1, 0)
    assert(reproduce == "".join(molecule))
    if final_element != 'e':
        # Account for example style inputs with e => O
        steps += 1
    return steps

def part2(inputs: List[TodaysInput]):
    total = 0
    total = parse_grammar(inputs)
    return total

class TodaysAdventOfCode(AdventOfCode):
    input_class = TodaysInput
    def test_part1(self):
        self.load_test_inputs("example1.txt", "input1.txt")
        self.run_part(part1, 4)

    def test_part2(self):
        self.load_test_inputs("example1.txt", "input1.txt")
        self.run_part(part2, 3)

TodaysAdventOfCode.run_tests()
