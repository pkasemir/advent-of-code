#!/usr/bin/env python3
from utilday21 import *

class Item(Input):
    def __init__(self, name, cost, damage, armor) -> None:
        self.name = name
        self.cost = cost
        self.damage = damage
        self.armor = armor

class TodaysInput(Input):
    def extra_parsing(self):
        self.name, self.value = self.line.split(':')
        self.value = int(self.value)

shop_text = '''
Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3
'''
def load_shop():
    shop = {}
    kind = ''
    for line in shop_text.splitlines():
        if not line.strip():
            continue
        m = re.match(r'([^:]*):(.*)', line)
        if m:
            kind = m.group(1)
            props = [p for p in Input.from_list(m.group(2), ' ') if p]
            shop[kind] = []
            continue

        m = re.match(r'([^ ]*( \+.)?) (.*)', line)
        assert(m)
        name = m.group(1)
        values =  list(map(int, [v for v in Input.from_list(m.group(3), ' ') if v]))
        shop[kind].append(Item(name, *values))
    return shop

shop = load_shop()
# pprint(shop)

class Person:
    def __init__(self, name, hp, damage, armor) -> None:
        self.name = name
        self.hp = hp
        self.damage = damage
        self.armor = armor
        self.reset()

    def reset(self):
        self.current_hp = self.hp

    def __repr__(self) -> str:
        return f'{self.name}:{self.current_hp}'

def attack(person1:Person, person2:Person):
    damage = max(1, person1.damage - person2.armor)
    person2.current_hp -= damage
    # print(person1, 'attacked', person2)
    return person2.current_hp <= 0

def do_battle(person1, person2):
    while True:
        if attack(person1, person2):
            return person1
        if attack(person2, person1):
            return person2

def gen_items(category, count0, count1, start_idx=0):
    if count0 == 0:
        yield []
    if count1 > 0:
        for i, item in enumerate(shop[category][start_idx:]):
            for items in gen_items(category, 0, count1 - 1, start_idx + i + 1):
                yield [item, *items]

def battle_arena(inputs, hp):
    boss = Person('boss', *[i.value for i in inputs])
    best = 10e5
    worst = 0
    for weapons in gen_items('Weapons', 1, 1):
        for armors in gen_items('Armor', 0, 1):
            for rings in gen_items('Rings', 0, 2):
                outfit = (*weapons, *armors, *rings)
                cost = sum(i.cost for i in outfit)
                damage = sum(i.damage for i in outfit)
                armor = sum(i.armor for i in outfit)
                # print(outfit)
                # print(cost, damage, armor)
                me = Person('player', hp, damage, armor)
                boss.reset()
                if do_battle(me, boss) is me:
                    best = min(best, cost)
                else:
                    worst = max(worst, cost)
                # print()
    return f'part1 {best} part2 {worst}'

def part1(inputs: List[TodaysInput], hp):
    total = 0
    # for input in inputs:
    #     print(input)
    # print(hp)
    boss = Person('boss', *[i.value for i in inputs])
    if hp == 8:
        me = Person('player', hp, 5, 5)
        do_battle(me, boss)
    else:
        total = battle_arena(inputs, hp)
    return total

class TodaysAdventOfCode(AdventOfCode):
    input_class = TodaysInput
    def test_part1(self):
        self.load_test_inputs("example1.txt", "input1.txt")
        self.set_test_args(8, 100)
        self.run_part(part1)

TodaysAdventOfCode.run_tests()
