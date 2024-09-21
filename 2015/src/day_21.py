"""Day 21: RPG Simulator 20XX

Mechanical problem. As usual, I forgot to create a copy of the boss
for each combat, with weird results. Non-FP ftw!

"""

from dataclasses import dataclass
import itertools
import os


@dataclass(frozen=True)
class Character:
    hp: int
    dmg: int
    armor: int


@dataclass(frozen=True)
class Item:
    name: str
    cost: int
    dmg: int
    armor: int


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> Character:
    hp, dmg, armor = [int(line.split(": ")[1]) for line in data.split("\n")]
    return Character(hp=hp, dmg=dmg, armor=armor)


def combat(you: Character, boss: Character) -> bool:
    boss_hp = boss.hp
    you_hp = you.hp

    while True:
        boss_hp -= max(you.dmg - boss.armor, 1)
        if boss_hp <= 0:
            return True
        you_hp -= max(boss.dmg - you.armor, 1)
        if you_hp <= 0:
            return False


def part1(src: str):
    boss = parse(src)

    weapons = [
        Item(name="dagger", cost=8, dmg=4, armor=0),
        Item(name="shortsword", cost=10, dmg=5, armor=0),
        Item(name="warhammer", cost=25, dmg=6, armor=0),
        Item(name="longsword", cost=40, dmg=7, armor=0),
        Item(name="greataxe", cost=74, dmg=8, armor=0),
    ]

    armors = [
        Item(name="none", cost=0, dmg=0, armor=0),
        Item(name="leather", cost=13, dmg=0, armor=1),
        Item(name="chainmail", cost=31, dmg=0, armor=2),
        Item(name="splintmail", cost=53, dmg=0, armor=3),
        Item(name="bandedmail", cost=75, dmg=0, armor=4),
        Item(name="platemail", cost=102, dmg=0, armor=5),
    ]

    rings = [
        Item(name="none", cost=0, dmg=0, armor=0),
        Item(name="none", cost=0, dmg=0, armor=0),
        Item(name="dmg + 1", cost=25, dmg=1, armor=0),
        Item(name="dmg + 2", cost=50, dmg=2, armor=0),
        Item(name="dmg + 3", cost=100, dmg=3, armor=0),
        Item(name="defense +1", cost=20, dmg=0, armor=1),
        Item(name="defense +2", cost=40, dmg=0, armor=2),
        Item(name="defense +3", cost=80, dmg=0, armor=3),
    ]

    best = -1
    worst = 0
    for weapon in weapons:
        for armor in armors:
            for ring_l, ring_r in itertools.combinations(rings, 2):
                cost = weapon.cost + armor.cost + ring_l.cost + ring_r.cost
                if combat(
                    you=Character(
                        hp=100,
                        dmg=weapon.dmg + ring_l.dmg + ring_r.dmg,
                        armor=armor.armor + ring_l.armor + ring_r.armor,
                    ),
                    boss=boss,
                ):
                    if best < 0 or cost < best:
                        best = cost
                else:
                    if cost > worst:
                        worst = cost

    return best, worst


def test_combat():
    assert combat(
        you=Character(hp=8, dmg=5, armor=5), boss=Character(hp=12, dmg=7, armor=2)
    )


if __name__ == "__main__":
    print(part1(read_data()))
