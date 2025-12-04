"""Day 04: Printing Department

Time to bring out the sets.
"""

import os
from textwrap import dedent

from . import cartesian


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> set[cartesian.Coord]:
    rolls: set[cartesian.Coord] = set()
    for x, line in enumerate(data.split("\n")):
        for y, char in enumerate(line):
            if char == "@":
                rolls.add((y, x))
    return rolls


def part1(rolls: set[cartesian.Coord]) -> int:
    return sum(sum(c in rolls for c in cartesian.neighbors(roll)) < 4 for roll in rolls)


def part2(rolls: set[cartesian.Coord]) -> int:
    start_count = len(rolls)
    while True:
        to_remove = set()
        for roll in rolls:
            if sum(c in rolls for c in cartesian.neighbors(roll)) < 4:
                to_remove.add(roll)
        rolls -= to_remove
        if not to_remove:
            break
    return start_count - len(rolls)


def test_part1() -> None:
    data = dedent(
        """
        ..@@.@@@@.
        @@@.@.@.@@
        @@@@@.@.@@
        @.@@@@..@.
        @@.@@@@.@@
        .@@@@@@@.@
        .@.@.@.@@@
        @.@@@.@@@@
        .@@@@@@@@.
        @.@.@@@.@.
        """
    ).strip()
    assert part1(parse(data)) == 13


def test_part2() -> None:
    data = dedent(
        """
        ..@@.@@@@.
        @@@.@.@.@@
        @@@@@.@.@@
        @.@@@@..@.
        @@.@@@@.@@
        .@@@@@@@.@
        .@.@.@.@@@
        @.@@@.@@@@
        .@@@@@@@@.
        @.@.@@@.@.
        """
    ).strip()
    assert part2(parse(data)) == 43


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
