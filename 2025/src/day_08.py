"""Day 08 Playground:

To avoid N^2, we want to build the distance map up front. Then we can
simply iterate through the list of pairs sorted by distance. We can
track circuits as sets of connected coordinates.
"""

import math
import operator
import os
import typing
from enum import unique
from functools import reduce
from textwrap import dedent

Coord: typing.TypeAlias = tuple[int, int, int]


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> set[Coord]:
    points: set[Coord] = set()
    for line in data.split("\n"):
        x, y, z = [int(n) for n in line.split(",")]
        points.add((x, y, z))
    return points


def ordered_pairs(points: set[Coord]) -> list[tuple[Coord, Coord]]:
    distances: dict[tuple[Coord, Coord], float] = {}
    for a in points:
        for b in points:
            if a == b or (a, b) in distances or (b, a) in distances:
                continue

            distances[(a, b)] = math.sqrt(sum((b_n - a_n) ** 2 for a_n, b_n in zip(a, b)))
    return sorted(distances, key=lambda k: distances[k])


def part1(points: set[Coord], iterations: int) -> int:
    circuits = {c: set([c]) for c in points}
    pairs = ordered_pairs(points)

    for _ in range(iterations):
        (
            a,
            b,
        ) = pairs.pop(0)

        circuits[a].update(circuits[b])
        for c in circuits[a]:
            circuits[c] = circuits[a]

    final_values = set(frozenset(s) for s in circuits.values())
    return reduce(operator.mul, [len(circuit) for circuit in sorted(final_values, key=lambda x: len(x))][-3:])


def part2(points: set[Coord]) -> int:
    circuits = {c: set([c]) for c in points}
    pairs = ordered_pairs(points)

    while True:
        (
            a,
            b,
        ) = pairs.pop(0)

        circuits[a].update(circuits[b])
        for c in circuits[a]:
            circuits[c] = circuits[a]

        if len(circuits[a]) == len(points):
            return a[0] * b[0]


def test_part1() -> None:
    data = dedent(
        """
        162,817,812
        57,618,57
        906,360,560
        592,479,940
        352,342,300
        466,668,158
        542,29,236
        431,825,988
        739,650,466
        52,470,668
        216,146,977
        819,987,18
        117,168,530
        805,96,715
        346,949,466
        970,615,88
        941,993,340
        862,61,35
        984,92,344
        425,690,689
        """
    ).strip()
    assert part1(parse(data), 10) == 40


def test_part2() -> None:
    data = dedent(
        """
        162,817,812
        57,618,57
        906,360,560
        592,479,940
        352,342,300
        466,668,158
        542,29,236
        431,825,988
        739,650,466
        52,470,668
        216,146,977
        819,987,18
        117,168,530
        805,96,715
        346,949,466
        970,615,88
        941,993,340
        862,61,35
        984,92,344
        425,690,689
        """
    ).strip()
    assert part2(parse(data)) == 25272


if __name__ == "__main__":
    print(part1(parse(read_data()), 1000))
    print(part2(parse(read_data())))
