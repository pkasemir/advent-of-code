#!/usr/bin/env python3
from utilday22 import *

import copy

class TodaysInput(Input):
    def extra_parsing(self):
        self.name, value = self.line.split(':')
        self.value:int = int(value)

class Person:
    def __init__(self, hp, damage=0, mana=0) -> None:
        self.hp = hp
        self.damage = damage
        self.mana = mana
        self.is_wizard = mana > 0

    def name(self):
        if self.is_wizard:
            return 'Player'
        else:
            return 'Boss'

    def __repr__(self) -> str:
        return f'{self.name()}: HP {self.hp}{f' mana {self.mana}' if self.is_wizard else '' }'

class Spell:
    def __init__(self, name, cost, damage=0, heal=0, armor=0, duration=0, recharge=0) -> None:
        self.name=name
        self.cost=cost
        self.damage=damage
        self.heal=heal
        self.armor=armor
        self.duration=duration
        self.recharge=recharge

    def is_effect(self):
        return self.duration > 0

    def __str__(self) -> str:
        return self.name
    __repr__ = __str__

missile = Spell('Magic Missile', 53, damage=4)
drain = Spell('Drain', 73, damage=2, heal=2)
shield = Spell('Shield', 113, armor=7, duration=6)
poison = Spell('Poison', 173, damage=3, duration=6)
recharge = Spell('Recharge ', 229, recharge=101, duration=5)

spells = [
    poison,
    shield,
    recharge,
    missile,
    drain,
]

def recurse_battle(p1:Person, p2:Person, effects:Sequence[Tuple[Spell, int]]=(), turn = 0, spent = 0, hard=False):
    global least_spent
    # print(turn, f'-- {p1.name()} turn --')
    if p1.is_wizard:
        me, boss = p1, p2
    else:
        me, boss = p2, p1

    wizard_armor = sum(s.armor for s, _ in effects)

    # print(turn, '-', me, 'armor', wizard_armor)
    # print(turn, '-', boss)
    me2 = copy.copy(me)
    boss2 = copy.copy(boss)
    if hard and p1.is_wizard:
        me2.hp -= 1
        # print(turn, f'player takes 1 damage')
        if me2.hp <= 0:
            # print('Boss wins')
            # print()
            return
    # apply effects
    for spell, duration in effects:
        duration -= 1
        # print(turn, f'{spell} in effect timer {duration}')
        me2.mana += spell.recharge
        boss2.hp -= spell.damage
        if boss2.hp <= 0:
            # print('Player wins spent mana:', spent)
            # print()
            least_spent = min(least_spent, spent)
            return

        # if duration == 0:
            # print(turn, f'{spell} wears off')

    effects = tuple([(s, d - 1) for s, d in effects if d > 1])

    # player actions
    if p1.is_wizard:
        # cast a spell
        cast_a_spell = False
        for spell in spells:
            if me2.mana < spell.cost:
                continue
            if any(s == spell for s, _ in effects):
                continue

            # print(turn, '-', me2, 'armor', wizard_armor)
            # print(turn, '-', boss2)
            # print(f'{turn} Player Cast {spell}')
            cast_a_spell = True
            spent2 = spent + spell.cost
            if spent2 >= least_spent:
                # Avoid searching deeper than we need to
                continue
            me3 = copy.copy(me2)
            boss3 = copy.copy(boss2)
            me3.mana -= spell.cost
            if spell.is_effect():
                effects2 = (*effects, (spell, spell.duration))
            else:
                effects2 = effects
                me3.hp += spell.heal
                boss3.hp -= spell.damage
                if boss3.hp <= 0:
                    # print('Player wins spent mana:', spent2)
                    least_spent = min(least_spent, spent2)
                    # print()
                    continue

            recurse_battle(boss3, me3, effects2, turn + 1, spent2, hard)
        if not cast_a_spell:
            # print(f'Boss wins, player only has {me2.mana} mana')
            # print()
            return
    else:
        damage = max(1, boss.damage - wizard_armor)
        # print(f'{turn} Boss attack {damage}')
        me2.hp -= damage
        if me2.hp <= 0:
            # print('Boss wins')
            # print()
            return
        recurse_battle(me2, boss2, effects, turn + 1, spent, hard)

def battle_arena(inputs: List[TodaysInput], hard=False):
    global least_spent
    least_spent = 1e10
    hp = 50
    mana = 500
    boss = Person(*[i.value for i in inputs])
    me = Person(hp, mana=mana)
    # boss = Person(13, 8)
    # me = Person(10, mana=250)

    # print(boss)
    # print(me)
    recurse_battle(me, boss, hard=hard)
    return least_spent

def part1(inputs: List[TodaysInput]):
    return battle_arena(inputs)

def part2(inputs: List[TodaysInput]):
    return battle_arena(inputs, hard=True)

class TodaysAdventOfCode(AdventOfCode):
    input_class = TodaysInput
    def test_part1(self):
        self.load_test_inputs(None, "input1.txt")
        self.run_part(part1, -1)

    def test_part2(self):
        self.load_test_inputs(None, "input1.txt")
        self.run_part(part2, -1)

TodaysAdventOfCode.run_tests()
