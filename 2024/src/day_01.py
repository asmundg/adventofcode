"""Day 1: Historian Hysteria

Welcome to AoC 2024!

I'm immediately happy with my usual choice of Python, since we have
some nice primitives for list processing. Comprehensions are great!

"""

import os
from textwrap import dedent
from typing import TypeAlias

List: TypeAlias = tuple[int, ...]


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> tuple[List, List]:
    a, b = zip(*((int(a), int(b)) for a, b in [line.split() for line in data.split("\n")]))
    return a, b


def part1(list_a: List, list_b: List) -> int:
    return sum([abs(a - b) for a, b in zip(sorted(list_a), sorted(list_b))])


def part2(list_a: List, list_b: List) -> int:
    return sum([a * list_b.count(a) for a in list_a])


def test_part1() -> None:
    data = dedent("""
    3   4
    4   3
    2   5
    1   3
    3   9
    3   3
    """).strip()
    assert part1(*parse(data)) == 11


def test_part2() -> None:
    data = dedent("""
    3   4
    4   3
    2   5
    1   3
    3   9
    3   3
    """).strip()
    assert part2(*parse(data)) == 31


if __name__ == "__main__":
    print(part1(*parse(read_data())))
    print(part2(*parse(read_data())))
