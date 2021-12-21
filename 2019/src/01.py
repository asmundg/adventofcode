import math
import os


def read_data(fname):
    with open(fname, encoding="utf-8") as handle:
        return parse(handle.readlines())


def parse(lines):
    return [int(line.strip()) for line in lines]


def solve(lines):
    print(sum(fuel(mass) for mass in lines))


def fuel(mass):
    return math.floor(mass / 3) - 2


def realistic_fuel(mass):
    total = 0
    while True:
        mass = fuel(mass)
        if mass <= 0:
            return total
        total += mass


def solve2(lines):
    print(sum(realistic_fuel(mass) for mass in lines))


def test_fuel():
    assert fuel(12) == 2
    assert fuel(14) == 2
    assert fuel(1969) == 654
    assert fuel(100756) == 33583


def test_realistic_fuel():
    assert realistic_fuel(14) == 2
    assert realistic_fuel(1969) == 966
    assert realistic_fuel(100756) == 50346


solve(read_data(os.path.join(os.path.dirname(__file__), "input/01.input")))
solve2(read_data(os.path.join(os.path.dirname(__file__), "input/01.input")))
