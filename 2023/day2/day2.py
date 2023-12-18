#!/usr/bin/env python3
import re
import os
import sys

def convert_input(line):
    m = line.split(':')
    # print(m)
    game_num = int(re.search("[0-9]+", m[0]).group())
    hands = []
    game = {"id": game_num, "hands": hands}
    for hand in m[1].split(';'):
        hands.append({})
        for cube in hand.split(","):
            # print(cube)
            count, color = cube.strip().split(' ')
            # print(count, color)
            # vals = re.match(".*([0-9]+)", hand)
            # game['hand'] = vals
            hands[-1][color] = int(count)
    power = 1
    for color in ['red', 'blue', 'green']:
        val = max([hand[color] for hand in hands if color in hand])
        # print(color, val)
        power *= val
    game['power'] = power
    # print(power)

    return game


def append_input(inputs, filename, solution=None):
    script_dir = os.path.dirname(sys.argv[0])
    if len(script_dir) > 0:
        script_dir += '/'
    filename = script_dir + filename

    try:
        with open(filename,'r') as f:
            lines = [line.strip() for line in f.readlines()]
    except:
        print("No input file", filename)
        return
    lines = [convert_input(line) for line in lines]
    inputs.append((lines, solution))

inputs = []

append_input(inputs, "example1.txt", 8)
# append_input(inputs, "input1.txt")
# print(inputs)

bag = dict(red=12, green=13, blue=14)

for input, solution in inputs:
    total = 0

    for game in input:
        valid = True
        # print(game)
        for hand in game['hands']:
            # print(hand)
            for color, count in bag.items():
                if hand.get(color, 0) > count:
                    # print("hand not valid", game['id'])
                    valid = False
                    break
            if not valid:
                break
        if valid:
            total += game['id']
    result = f"total {total}"
    if solution is not None:
        result += " " + "matches" if solution == total else "not right"

    print(result)



inputs = []

append_input(inputs, "example1.txt", 2286)
append_input(inputs, "input1.txt")

bag = dict(red=12, green=13, blue=14)

for input, solution in inputs:
    total = sum([game['power'] for game in input])

    result = f"total {total}"
    if solution is not None:
        result += " " + "matches" if solution == total else "not right"

    print(result)
