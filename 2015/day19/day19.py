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

def get_replacements(inputs: List[TodaysInput], conv=to_element_list):
    replacements = {}
    for input in inputs:
        s = input.line.split(' => ')
        if len(s) == 1:
            break
        replacements.setdefault(s[0], []).append(conv(s[1]))

        # print(input)
    return replacements

def get_possible_molecules(molecule, replacements):
    molecules = set()
    for i, element in enumerate(molecule):
        if element not in replacements:
            continue
        for r in replacements[element]:
            # my_molecule = molecule[:i]
            # my_molecule.extend(r)
            # my_molecule.extend(molecule[i+1:])
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

# from pyvis.network import Network

def find_indexes_of(pattern, parent):
    for i in range(len(parent) - len(pattern), -1, -1):
        match = True
        for pat, par in zip(pattern, parent[i:]):
            if pat != par:
                match = False
                break
        if match:
            yield i

def do_replacement(parent, p_slice:slice, replace):
    # replacement = parent[:p_slice.start]
    # replacement.extend(replace)
    # replacement.extend(parent[p_slice.stop:])
    replacement = (*parent[:p_slice.start], *replace, *parent[p_slice.stop:])
    return replacement

def recurse_replace(r_replacements, cur_molecule, step=0, my_best_replace = 1e10):
    step += 1
    if step >= my_best_replace:
        return my_best_replace
    for r_molecule, to_element in r_replacements:
        # print(step, r_molecule, to_element)
        if to_element == 'e':
            if r_molecule == cur_molecule:
                print('Found e from', cur_molecule, step)
                return step
            continue

        for i in find_indexes_of(r_molecule, cur_molecule):
            next_molecule = do_replacement(cur_molecule, slice(i, i + len(r_molecule)), to_element)
            # print('next', cur_molecule)
            # print('   ', i, r_molecule, to_element, next_molecule)
            print('step', step, 'i', i, r_molecule, to_element, len(next_molecule))
            # input()
            replace_count = recurse_replace(r_replacements, next_molecule, step, my_best_replace)
            my_best_replace = min(my_best_replace, replace_count)
    return my_best_replace

import bisect

def get_fastest_reverse(r_replacements, cur_molecule):
    # use breadth first search
    # print(replacements)
    q = [(0, cur_molecule)]
    running = True
    last_step = 0
    last_time = time.time() + 1
    while running:
        step, cur_molecule = q.pop(0)
        # print(step, cur_molecule)
        # print('step', step, 'len(cur_molecule)', len(cur_molecule))
        # input()
        step += 1
        # if step > last_step:
        #     last_step = step
        #     print('step', step, len(q))
        if last_time < time.time():
            last_time = time.time() + 1
            print('step', step, len(q))
            # break
        # next_molecules = get_possible_molecules(cur_molecule, replacements)
        # # pprint(next_molecules)
        # for m in next_molecules:
        #     if m == molecule:
        #         total = step
        #         running = False
        #         break
        #     if len(m) <= len(molecule):

        for r_molecule, to_element in r_replacements:
            # print(step, r_molecule, to_element)
            if to_element == 'e':
                if r_molecule == cur_molecule:
                    print('Found e from', cur_molecule, step)
                    return step
                continue

            for i in find_indexes_of(r_molecule, cur_molecule):
                next_molecule = do_replacement(cur_molecule, slice(i, i + len(r_molecule)), to_element)
                # print('next', cur_molecule)
                # print('   ', i, r_molecule, to_element, next_molecule)
                # print('step', step, 'i', i, r_molecule, to_element, len(next_molecule))
                # input()
                # replace_count = recurse_replace(r_replacements, next_molecule, step, my_best_replace)
                # my_best_replace = min(my_best_replace, replace_count)
                # q.append((step, next_molecule))
                bisect.insort(q, (step, next_molecule), key=lambda x: len(x[1]))

def get_fastest_reverse2(r_replacements, cur_molecule):
    step = 1
    last_molecule = cur_molecule
    while True:
        for r_molecule, to_element in r_replacements:
            # print(step, r_molecule, to_element)
            if to_element == 'e':
                if r_molecule == cur_molecule:
                    print('Found e from', cur_molecule, step)
                    return step
                continue
            for i in find_indexes_of(r_molecule, cur_molecule):
                print(step, r_molecule, to_element, i)
                cur_molecule = do_replacement(cur_molecule, slice(i, i + len(r_molecule)), to_element)
                step += 1
                if last_molecule == cur_molecule:
                    print('stale')
                    return -1
                last_molecule = cur_molecule
                break

def parse_grammar(inputs: List[TodaysInput]):
    replacements = get_replacements(inputs, str)
    molecule = inputs[-1].line
    pprint(replacements)

    for i in range(len(molecule)):
        pass

    return 0

def cheat(inputs: List[TodaysInput]):
    input1 = "\n".join(map(lambda x: x.line, inputs))
    molecule = input1.split('\n')[-1][::-1]
    reps = {m[1][::-1]: m[0][::-1]
            for m in re.findall(r'(\w+) => (\w+)', input1) if m[0] != 'e'}
    reps_e = "|".join([m[1][::-1]
            for m in re.findall(r'(\w+) => (\w+)', input1) if m[0] == 'e'])
    reps_e = f'^({reps_e})$'
    # print(reps_e)
    # rev_it = lambda x: x[::-1]
    # molecule = rev_it(inputs[-1].line)
    # # reps = {m[1][::-1]: m[0][::-1]
    # #         for m in re.findall(r'(\w+) => (\w+)', input)}
    # print('molecule', str(molecule))
    # pprint(get_replacements(inputs, str))
    # # reps = {t[::-1]: f[::-1]
    # #         for f, t in get_replacements(inputs, str).items()}
    # reps = {}
    # for f, tl in get_replacements(inputs, str).items():
    #     for t in tl:
    #         reps[rev_it(t)] = rev_it(f)

    # pprint(reps)

    def rep(x):
        return reps[x.group()]

    count = 0
    while True:
        if re.match(reps_e, molecule):
            count += 1
            break
        molecule = re.sub('|'.join(reps.keys()), rep, molecule, count=1)
        # print(molecule)
        count += 1

    # print(count)
    return count


def part2(inputs: List[TodaysInput]):
    total = 0
    total = cheat(inputs)
    return total
    # total = parse_grammar(inputs)
    # return total
    global replacements
    replacements = get_replacements(inputs)
    molecule = tuple(to_element_list(inputs[-1].line))
    ##########
    # p = list("hello world")
    # print(p)
    # print(do_replacement(p, slice(1, 2), ['E']))
    # print(do_replacement(p, slice(1, 5), ['H']))
    # print(do_replacement(p, slice(1, 5), list('eat')))
    # print(do_replacement(p, slice(1, 2), list('eat')))
    # exit()
    ##########
    # pprint(replacements)
    print('len(molecule)', len(molecule))
    r_count = 0
    r_set = set()
    e_set = set(replacements.keys())
    for r, l in replacements.items():
        e_set.update(*l)
    # net = Network()
    # net.add_nodes(e_set)
    e_count = {}
    e_dict = {}
    for r, l in replacements.items():
        for l2 in l:
            r_set.add((tuple(l2), r))
            for e in l2:
                # print(e)
                e_count.setdefault(e, 0)
                e_dict.setdefault(e, set())
                e_count[e] += 1
                e_dict[e].add(r)
                # net.add_edge(r, e)

        # print(l)
        r_count += len(l)
    # net.show('vis.html', notebook=False)
    print('r_count', r_count)
    print('len(r_set)', len(r_set))
    pprint('r_set')
    pprint(r_set)
    pprint('sorted(r_set)')
    r_replacements = sorted(sorted(r_set), key=lambda x: -len(x[0]))
    # pprint(r_replacements)
    for m, to in r_replacements:
        print(tuple(map("{:2}".format, m)), 'to', to)
    pprint('e_count')
    pprint(e_count)
    pprint('e_dict')
    pprint(e_dict)
    pprint('e_set')
    pprint(e_set)
    print(len(e_set), len(replacements))
    # use largest replacements first
    cur_molecule = tuple(molecule)
    # total = recurse_replace(r_replacements, cur_molecule)
    total = get_fastest_reverse2(r_replacements, cur_molecule)


    return total


    # use breadth first search
    # print(replacements)
    q = [(0, ['e'])]
    running = True
    last_step = 0
    last_time = time.time() + 1
    while running:
        step, cur_molecule = q.pop(0)
        # print(step, cur_molecule)
        step += 1
        # if step > last_step:
        #     last_step = step
        if last_time < time.time():
            last_time = time.time() + 1
            print('step', step, len(q))
            break
        next_molecules = get_possible_molecules(cur_molecule, replacements)
        # pprint(next_molecules)
        for m in next_molecules:
            if m == molecule:
                total = step
                running = False
                break
            if len(m) <= len(molecule):
                q.append((step, list(m)))

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
