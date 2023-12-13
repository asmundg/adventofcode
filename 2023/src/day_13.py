"""Day 13: Point of Incidence

Mirroring the rows and columns is pretty simple with slicing. To find
the single smudged point in part 2, we need to find the mirror point
that produces a single char diff.
"""

import os
from textwrap import dedent

from typing import List, Tuple, TypeAlias

Coord: TypeAlias = Tuple[int, int]
Data: TypeAlias = List[List[str]]


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> Data:
    parts: Data = []
    for part in data.split("\n\n"):
        parts.append(part.split("\n"))
    return parts


def part1(data: str) -> int:
    parts = parse(data)
    total = 0
    for part in parts:
        max_y = len(part)
        max_x = len(part[0])

        # check for mirrored rows
        cols = ["".join([part[y][x] for y in range(max_y)]) for x in range(max_x)]
        for x in range(max_x - 1):
            for a, b in zip(cols[x::-1], cols[x + 1 :]):
                if a != b:
                    break
            else:
                total += x + 1

        # check for mirrored rows
        for y in range(max_y - 1):
            for a, b in zip(part[y::-1], part[y + 1 :]):
                if a != b:
                    break
            else:
                total += (y + 1) * 100

    return total


def n_diff(a: str, b: str) -> int:
    return len([(a, b) for a, b in zip(a, b) if a != b])


def part2(data: str) -> int:
    parts = parse(data)
    total = 0
    for part in parts:
        max_y = len(part)
        max_x = len(part[0])

        # check for mirrored cols
        cols = ["".join([part[y][x] for y in range(max_y)]) for x in range(max_x)]
        for x in range(max_x - 1):
            diff = [(a, b) for a, b in zip(cols[x::-1], cols[x + 1 :]) if a != b]
            if len(diff) == 1 and n_diff(diff[0][0], diff[0][1]) == 1:
                total += x + 1
                break

        # check for mirrored rows
        for y in range(max_y - 1):
            diff = [(a, b) for a, b in zip(part[y::-1], part[y + 1 :]) if a != b]
            if len(diff) == 1 and n_diff(diff[0][0], diff[0][1]) == 1:
                total += (y + 1) * 100
                break

    return total


def test_part1():
    data = dedent(
        """
        #.##..##.
        ..#.##.#.
        ##......#
        ##......#
        ..#.##.#.
        ..##..##.
        #.#.##.#.

        #...##..#
        #....#..#
        ..##..###
        #####.##.
        #####.##.
        ..##..###
        #....#..#
        """
    ).strip()

    assert (part1(data)) == 405


def test_part2():
    data = dedent(
        """
        #.##..##.
        ..#.##.#.
        ##......#
        ##......#
        ..#.##.#.
        ..##..##.
        #.#.##.#.

        #...##..#
        #....#..#
        ..##..###
        #####.##.
        #####.##.
        ..##..###
        #....#..#
        """
    ).strip()

    assert (part2(data)) == 400


if __name__ == "__main__":
    print(part1(read_data()))
    print(part2(read_data()))
