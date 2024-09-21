"""Day 01: No Time for a Taxicab.

Coordinate rotation on day 1! This couuld be an interesting year.

"""

import os
from typing import List, Tuple
from textwrap import dedent

from common import cartesian


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> List[Tuple[str, int]]:
    cartesian_map = {"R": cartesian.RIGHT, "L": cartesian.LEFT}
    return [
        (cartesian_map[element[0]], int(element[1:])) for element in data.split(", ")
    ]


def part1(instructions):
    heading = cartesian.UP
    pos = (0, 0)

    turns = {cartesian.RIGHT: cartesian.RIGHT_TURN, cartesian.LEFT: cartesian.LEFT_TURN}
    for direction, steps in instructions:
        heading = turns[direction][heading]
        pos = (pos[0] + heading[0] * steps, pos[1] + heading[1] * steps)

    return sum((abs(p) for p in pos))


def part2(instructions):
    heading = cartesian.UP
    pos = (0, 0)
    visited = {pos}

    turns = {cartesian.RIGHT: cartesian.RIGHT_TURN, cartesian.LEFT: cartesian.LEFT_TURN}
    for direction, steps in instructions:
        heading = turns[direction][heading]
        for _ in range(steps):
            pos = (pos[0] + heading[0], pos[1] + heading[1])
            if pos in visited:
                return sum((abs(p) for p in pos))
            visited.add(pos)

    assert False, "Shouldn't get here"


def test_part1():
    data = dedent(
        """
        R5, L5, R5, R3
        """
    ).strip()

    assert part1(parse(data)) == 12


def test_part2():
    data = dedent(
        """
        R8, R4, R4, R8
        """
    ).strip()

    assert part2(parse(data)) == 4


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
