"""Day 8: Resonant Collinearity

Another matrix walk-ish problem. This time, we're using bresenham
lines to step out from each pair of nodes.

My brain refused to correctly interpret part 2 correctly and got
confused when I read that there should be antinodes on top of each
antenna, but the example output didn't show the antinodes. Didn't help
that the text (somewhat) explicitly said "including the antinodes that
appear on every antenna".

In any case, finding every (integer) node along the line between two
nodes just requires dividing the distance from part 1 by the GCD of
the vector components, giving us the shortest path to a node in line.
"""

import itertools
import math
import os
from dataclasses import dataclass
from textwrap import dedent

from common import cartesian


@dataclass(frozen=True)
class Data:
    antennas: dict[str, set[cartesian.Coord]]
    max_y: int = 0
    max_x: int = 0


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> Data:
    antennas: dict[str, set[cartesian.Coord]] = dict()
    for y, line in enumerate(data.split("\n")):
        for x, char in enumerate(line):
            if char.isalnum():
                if char not in antennas:
                    antennas[char] = set()
                antennas[char].add((y, x))
        max_x = x
    max_y = y
    return Data(antennas, max_y=max_y, max_x=max_x)


def part1(data: Data) -> int:
    antinodes: set[cartesian.Coord] = set()
    for antenna_type in data.antennas:
        for a, b in itertools.combinations(data.antennas[antenna_type], 2):
            y_diff = b[0] - a[0]
            x_diff = b[1] - a[1]

            anti_a = (a[0] - y_diff, a[1] - x_diff)
            anti_b = (b[0] + y_diff, b[1] + x_diff)

            for node in (anti_a, anti_b):
                if 0 <= node[0] <= data.max_x and 0 <= node[1] <= data.max_y:
                    antinodes.add(node)

    return len(antinodes)


def part2(data: Data) -> int:
    antinodes: set[cartesian.Coord] = set()
    for antenna_type in data.antennas:
        for a, b in itertools.combinations(data.antennas[antenna_type], 2):
            y_diff = b[0] - a[0]
            x_diff = b[1] - a[1]

            divisor = math.gcd(y_diff, x_diff)
            y_diff //= divisor
            x_diff //= divisor

            for direction in (1, -1):
                step = 0
                while True:
                    y = a[0] + step * direction * y_diff
                    x = a[1] + step * direction * x_diff
                    if not (0 <= y <= data.max_y and 0 <= x <= data.max_x):
                        break

                    antinodes.add((a[0] + step * direction * y_diff, a[1] + step * direction * x_diff))
                    step += 1

    return len(antinodes)


def test_part1() -> None:
    data = dedent("""
    ............
    ........0...
    .....0......
    .......0....
    ....0.......
    ......A.....
    ............
    ............
    ........A...
    .........A..
    ............
    ............
    """).strip()
    assert part1(parse(data)) == 14


def test_part2() -> None:
    data = dedent("""
    ............
    ........0...
    .....0......
    .......0....
    ....0.......
    ......A.....
    ............
    ............
    ........A...
    .........A..
    ............
    ............
    """).strip()
    assert part2(parse(data)) == 34


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
