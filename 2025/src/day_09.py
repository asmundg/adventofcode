"""Day 09: Movie Theater

This feels a lot like yesterday, wrt computing all pairs. That also
makes it feel like a trap.

Turns out part 2 is actually a geometry problem and although I can see
the basic shape of how to find if a shape is contained in another
shape, there are so many edge cases that I'm going insane. This is a
good time to go batteries included. Since I'm already allowing z3, I'm
totally onboard with bringing in a geometry library to fix the thing
for me.

"""

import itertools
import os
from textwrap import dedent

import shapely

from .cartesian import Coord


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> list[Coord]:
    points: list[Coord] = []
    for line in data.split("\n"):
        x, y = [int(n) for n in line.split(",")]
        points.append((x, y))
    return points


def part1(points: list[Coord]) -> int:
    largest = 0
    for a, b in itertools.permutations(points, 2):
        largest = max(largest, sizeof(a, b))
    return largest


def sizeof(a: Coord, b: Coord) -> int:
    return (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)


def corners(a: Coord, b: Coord) -> tuple[Coord, Coord, Coord, Coord]:
    return ((a[0], a[1]), (b[0], a[1]), (b[0], b[1]), (a[0], b[1]))


def part2(points: list[Coord]) -> int:
    largest = 0
    poly = shapely.Polygon(points)
    for a, b in itertools.permutations(points, 2):
        tiles = shapely.Polygon(corners(a, b))
        if poly.contains(tiles):
            largest = max(largest, sizeof(a, b))
    return largest


def test_part1() -> None:
    data = dedent(
        """
        7,1
        11,1
        11,7
        9,7
        9,5
        2,5
        2,3
        7,3
        """
    ).strip()
    assert part1(parse(data)) == 50


def test_part2() -> None:
    data = dedent(
        """
        7,1
        11,1
        11,7
        9,7
        9,5
        2,5
        2,3
        7,3
        """
    ).strip()
    assert part2(parse(data)) == 24


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
