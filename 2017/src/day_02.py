"""Day 02: Corruption Checksum

Part1: Sort, then subtract [0] from [-1].
Part2: Just test app pairwise permutations.
"""

import itertools
import os
from textwrap import dedent


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> list[list[int]]:
    nums = []
    for line in data.split("\n"):
        nums.append([int(n) for n in line.split()])
    return nums


def part1(sheet: list[list[int]]) -> int:
    total = 0
    for row in sheet:
        s = sorted(row)
        total += s[-1] - s[0]
    return total


def part2(sheet: list[list[int]]) -> int:
    total = 0
    for row in sheet:
        for a, b in itertools.permutations(row, 2):
            if a / b == a // b:
                total += a // b
    return total


def test_part1() -> None:
    data = dedent("""
    5 1 9 5
    7 5 3
    2 4 6 8
    """).strip()
    assert part1(parse(data)) == 18


def test_part2() -> None:
    data = dedent("""
    5 9 2 8
    9 4 7 3
    3 8 6 5
    """).strip()
    assert part2(parse(data)) == 9


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
