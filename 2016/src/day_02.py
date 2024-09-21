"""Day 02: Bathroom Security.

More fun with coordinates. Clamping to the allowed coordinates can
conventiently reuse the data structure telling us which keys the
positions correspond to.

"""

import os
from typing import List
from textwrap import dedent

from common import cartesian


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> List[List[cartesian.Coord]]:
    cartesian_map = {
        "U": cartesian.UP,
        "R": cartesian.RIGHT,
        "D": cartesian.DOWN,
        "L": cartesian.LEFT,
    }

    res = []
    for line in data.split("\n"):
        res.append([cartesian_map[char] for char in line])
    return res


PART1_KEYPAD = {
    (-1, -1): "1",
    (-1, 0): "2",
    (-1, 1): "3",
    (0, -1): "4",
    (0, 0): "5",
    (0, 1): "6",
    (1, -1): "7",
    (1, 0): "8",
    (1, 1): "9",
}

PART2_KEYPAD = {
    (-2, 0): "1",
    (-1, -1): "2",
    (-1, 0): "3",
    (-1, 1): "4",
    (0, -2): "5",
    (0, -1): "6",
    (0, 0): "7",
    (0, 1): "8",
    (0, 2): "9",
    (1, -1): "A",
    (1, 0): "B",
    (1, 1): "C",
    (2, 0): "D",
}


def solve(instructions, keypad, start):
    pos = start
    keys = []

    for instruction in instructions:
        for move in instruction:
            new_pos = cartesian.move(pos, move)
            pos = new_pos if new_pos in keypad else pos
        keys.append(pos)

    return "".join([keypad[pos] for pos in keys])


def part1(instructions):
    return solve(instructions, PART1_KEYPAD, (0, 0))


def part2(instructions):
    return solve(instructions, PART2_KEYPAD, (0, -2))


def test_part1():
    data = dedent(
        """
        ULL
        RRDDD
        LURDL
        UUUUD
        """
    ).strip()

    assert part1(parse(data)) == "1985"


def test_part2():
    data = dedent(
        """
        ULL
        RRDDD
        LURDL
        UUUUD
        """
    ).strip()

    assert part2(parse(data)) == "5DB3"


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
