#!/usr/bin/env python3
from utilday10 import *
import sympy as sp

class TodaysInput(Input):
    def extra_parsing(self):
        m = re.match(r'\[(.*)\] (.*) {(.*)}', self.line)
        self.lights = m.group(1)
        self.lights_int = sum([1 << i for i, l in enumerate(self.lights) if l == '#'])
        self.buttons = [self.from_list(b[1:-1], ',', int) for b in m.group(2).split()]
        self.buttons_int = [self.buttons_to_int(lights) for lights in self.buttons]
        self.joltage = self.from_list(m.group(3), ',', int)

    def buttons_to_int(self, lights):
        return sum([1 << l for l in lights])

    def press_button(self, button, state):
        new_state = state ^ self.buttons_int[button]
        # print('pressed', button, self.buttons[button], hex(state), '->', hex(new_state))
        return new_state

    def get_button_presses(self):
        total = len(self.buttons) + 1
        for i in range(1 << len(self.buttons)):
            # print(i, int.bit_count(i))
            if int.bit_count(i) >= total:
                continue
            state = 0
            presses = 0
            for b in range(len(self.buttons)):
                if i & (1 << b):
                    presses += 1
                    state = self.press_button(b, state)
                    if state == self.lights_int:
                        # print('found on state after', presses)
                        total = min(total, presses)
                        break
        return total

    def press_button_joltage(self, button, state, presses, times=1):
        self.press_count += 1
        new_state = list(state)
        for j in self.buttons[button]:
            new_state[j] += times
        presses[button] += times
        # print(presses, 'pressed', times, 'times', button, self.buttons[button], state, '->', new_state)
        # print(self.going_up)
        return new_state

    def joltage_too_large(self, state):
        for j, s in zip(self.joltage, state):
            if s > j:
                return True
        return False

    def get_button_presses_joltage(self):
        # This function takes a long time to run, there is probably a better way to
        # do it, as this took almost 5 minutes to solve the full set.
        symbols = sp.symbols(f'b0:{len(self.buttons)}')
        # print(symbols)
        # print(self)
        eqs = []
        b = symbols
        for i in range(len(self.joltage)):
            eqs.append([1 if i in b else 0 for b in self.buttons])
        eqs = sp.Matrix(eqs)
        ans = sp.Matrix(self.joltage)
        solutions = list(sp.linsolve((eqs, ans), *symbols))
        s:List[sp.Add] = solutions[0]
        # print(b, len(b), len(s))
        # print(solutions[0])
        free = [b[i] for i in range(len(b)) if s[i] == b[i]]
        if len(free) == 0:
            print('single solution', sum(s))
            return sum(s)
        # print('free', free)
        free_max = []
        for button_num, button in enumerate(b):
            if button in free:
                free_max.append(min([self.joltage[j] for j in self.buttons[button_num]]))

        print('free_max', free_max, flush=True)
        try_free = [0] * len(free)
        total = None

        # Speeds this up by about 3 times, but gives bad answer (s_cache gives real answer + 2 )
        # s_cache = s
        # for f, v in zip(free[1:], try_free[1:]):
        #     s_cache = [e.subs(f, v) for e in s_cache]
        calculations = 0
        while True:
            cur = s
            for f, v in zip(free, try_free):
                cur = [e.subs(f, v) for e in cur]
            # cur = [e.subs(free[0], try_free[0]) for e in s_cache]
            calculations+= 1
            # print(cur, total)
            if not any(r < 0 or not r.is_Integer for r in cur):
                if total is None:
                    total = sum(cur)
                else:
                    total = min(total, sum(cur))

            for i in range(len(free)):
                try_free[i] += 1
                if try_free[i] > free_max[i]:
                    try_free[i] = 0
                    if i + 1 == len(free):
                        print('total', total, 'calculations', calculations, flush=True)
                        return total

                    # s_cache = s
                    # for f, v in zip(free[1:], try_free[1:]):
                    #     s_cache = [e.subs(f, v) for e in s_cache]
                    continue
                break

def part1(inputs: List[TodaysInput]):
    total = 0
    for input in inputs:
        # print(input)
        total += input.get_button_presses()
    return total

def part2(inputs: List[TodaysInput]):
    total = 0
    for i, input in enumerate(inputs):
        with TimeBlock():
            # print(input)
            print('working on', i)
            total += input.get_button_presses_joltage()
    return total

class TodaysAdventOfCode(AdventOfCode):
    input_class = TodaysInput
    def test_part1(self):
        self.run_part(part1, 7)

    def test_part2(self):
        self.run_part(part2, 33)

unittest.main(verbosity=0)
