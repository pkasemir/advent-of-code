#!/usr/bin/env python3
from utilday9 import *

class TodaysInput(Input):
    def extra_parsing(self):
        self.coords = self.from_list(self.line, ',', int)
        delattr(self, 'line')

class Rectangle:
    def __init__(self, a:TodaysInput, b:TodaysInput):
        self.a = a
        self.b = b
        self.area = (abs(a.coords[0] - b.coords[0]) + 1) * (abs(a.coords[1] - b.coords[1]) + 1)

        self.ax = min(a.coords[0], b.coords[0])
        self.bx = max(a.coords[0], b.coords[0])
        self.ay = min(a.coords[1], b.coords[1])
        self.by = max(a.coords[1], b.coords[1])

    def __str__(self):
        return f'{self.a.coords}/{self.b.coords} A:{self.area} sorted {([self.ax, self.ay], [self.bx, self.by])}'
    __repr__ = __str__

def get_largest_area(inputs: List[TodaysInput]):
    area = 0
    for i, a in enumerate(inputs):
        for j in range(i + 1, len(inputs)):
            b = inputs[j]
            r = Rectangle(a, b)
            # print(r)
            area = max(area, r.area)

    return area

class OutsideLine:
    def __init__(self, ax, ay, bx, by):
        self.ax = min(ax, bx)
        self.bx = max(ax, bx)
        self.ay = min(ay, by)
        self.by = max(ay, by)
        self.same_x = ax == bx

    def __str__(self):
        return f'{((self.ax, self.ay),(self.bx, self.by))}'
    __repr__ = __str__

    def includes_outside(self, r: Rectangle):
        # print('inc', r, self)

        if self.same_x:
            # Line on same x
            if r.ax <= self.ax <= r.bx:
                if self.ay <= r.ay <= self.by or self.ay <= r.by <= self.by:
                    # print('intesect', r, self)
                    return True
        else:
            # Line on same y
            if r.ay <= self.ay <= r.by:
                if self.ax <= r.ax <= self.bx or self.ax <= r.bx <= self.bx:
                    # print('intesect', r, self)
                    return True
        return False

class LineGrid(Grid):
    def __init__(self, lines):
        rows = 0
        cols = 0

        for l in lines:
            cols = max(cols, l.ax, l.bx)
            rows = max(rows, l.ay, l.by)
        cols += 2
        rows += 2

        if cols < 100:
            inputs = [Input('.' * cols) for _ in range(rows)]
        else:
            inputs = [Input('')]
        super().__init__(inputs)

        if cols < 100:
            for l in lines:
                self.draw_line(l)


    def draw_line(self, line):
        ax = min(line.ax, line.bx)
        bx = max(line.ax, line.bx)
        ay = min(line.ay, line.by)
        by = max(line.ay, line.by)
        for x in range(ax, bx + 1):
            for y in range(ay, by + 1):
                c = self[y][x]
                if c == '.':
                    c = '1'
                else:
                    c = chr(ord(c) + 1)
                self[y][x] = c


    def __str__(self):
        header = f'{self.rows}x{self.cols}\n'
        return header + super().__str__()

class Line:
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'

    def __init__(self, a: TodaysInput, b: TodaysInput):
        self.a = a
        self.b = b
        self.prev:Line = None
        self.nex:Line = None

        # For line drawing
        self.ax = min(a.coords[0], b.coords[0])
        self.bx = max(a.coords[0], b.coords[0])
        self.ay = min(a.coords[1], b.coords[1])
        self.by = max(a.coords[1], b.coords[1])
        self.direction = self.get_direction()
        self.turn = 'UNK'
        self.outside = (0, 0)

    def __str__(self):
        return f'{self.a.coords}, {self.b.coords} {self.turn} out:{self.outside}' # {self.direction} {self.turn}'
    __repr__ = __str__

    def get_direction(self):
        ax, ay = self.a.coords
        bx, by = self.b.coords
        if ax == bx:
            if by > ay:
                return self.UP
            else:
                return self.DOWN
        else:
            if bx > ax:
                return self.RIGHT
            else:
                return self.LEFT

    turns = {
        (UP, LEFT): RIGHT,
        (UP, RIGHT): LEFT,
        (DOWN, RIGHT): RIGHT,
        (DOWN, LEFT): LEFT,
        (RIGHT, UP): RIGHT,
        (RIGHT, DOWN): LEFT,
        (LEFT, UP): LEFT,
        (LEFT, DOWN): RIGHT,
    }
    def get_turn(self, prev:'Line'):
        return self.turns[(prev.direction, self.direction)]

    def set_turn(self, prev:'Line'):
        self.prev = prev
        prev.nex = self
        prev.turn = self.get_turn(prev)

    directions = {
        UP: (0, 1),
        DOWN: (0, -1),
        LEFT: (-1, 0),
        RIGHT: (1, 0),
    }
    num_to_dir = (RIGHT, UP, LEFT, DOWN)
    dir_to_num = {d: i for i, d in enumerate(num_to_dir)}

    @classmethod
    def rotate_dir_cw(cls, num, d):
        dir_num = cls.dir_to_num[d]
        next_dir = (dir_num + num) % 4
        return cls.directions[cls.num_to_dir[next_dir]]

    def get_outside_line(self, is_right):
        ax, ay = self.a.coords
        bx, by = self.b.coords
        rotate_count = -1 if is_right else 1
        long_turn = self.RIGHT if is_right else self.LEFT
        dx, dy = self.rotate_dir_cw(rotate_count, self.direction)
        ax += dx
        ay += dy
        bx += dx
        by += dy

        # print(self, 'long_turn', long_turn)
        dx, dy = self.directions[self.direction]
        if self.prev.turn == long_turn:
            # print('add to beginning')
            ax -= dx
            ay -= dy
        else:
            # print('take from beginning')
            ax += dx
            ay += dy

        if self.turn == long_turn:
            # print('add to end')
            bx += dx
            by += dy
        else:
            # print('take from end')
            bx -= dx
            by -= dy
        return OutsideLine(ax, ay, bx, by)

def get_largest_area_inside(inputs: List[TodaysInput]):
    area = 0
    lines:List[Line] = []

    last = None
    for i, a in enumerate(inputs):
        if last is not None:
            l = Line(last, a)
            if len(lines) > 0:
                l.set_turn(lines[-1])
            lines.append(l)

        last = a
    l = Line(inputs[-1], inputs[0])
    l.set_turn(lines[-1])
    lines[0].set_turn(l)
    lines.append(l)
    rights = sum(map(lambda l: 1 if l.turn == l.RIGHT else -1, lines))
    # pprint(lines)
    outside_lines = [l.get_outside_line(rights > 0) for l in lines]
    # pprint(outside_lines)
    # print(LineGrid(lines))
    # print()
    # outside_grid = LineGrid(outside_lines)
    # print(outside_grid)

    for i, a in enumerate(inputs):
        for j in range(i + 1, len(inputs)):
            b = inputs[j]
            r = Rectangle(a, b)
            if r.area <= area:
                continue
            # print(r)
            # print(outside_grid)
            is_outside = False
            for l in outside_lines:
                if l.includes_outside(r):
                    is_outside = True
                    break
            if not is_outside:
                area = max(area, r.area)

    return area

def part1(inputs: List[TodaysInput]):
    total = 0
    total = get_largest_area(inputs)
    return total

def part2(inputs: List[TodaysInput]):
    total = 0
    total = get_largest_area_inside(inputs)
    return total

class TodaysAdventOfCode(AdventOfCode):
    input_class = TodaysInput
    def test_part1(self):
        self.run_part(part1, 50)

    def test_part2(self):
        self.run_part(part2, 24)

unittest.main(verbosity=0)
