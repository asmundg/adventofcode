"""Day 11: Cosmic Expansion

We need to find the distance between all pairs. Python has some very
useful abstractions here to produce permutations and reduce them to
the set of unique pairs.

The complicating factor is that space is expanding by a whole lot, so
physically extending the grid does not scale. Instead, we find the
number of crossed empty rows and columns, adding that number
multiplied by the expansion factor to the original distance between
the stars.

"""

from dataclasses import dataclass
import itertools
import os
from textwrap import dedent

from typing import Set, Tuple, TypeAlias

Coord: TypeAlias = Tuple[int, int]


@dataclass
class Data:
    stars: Set[Coord]
    empty_rows: Set[int]
    empty_cols: Set[int]


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> Data:
    stars = set()
    for y, line in enumerate(data.split("\n")):
        for x, char in enumerate(line):
            if char == "#":
                stars.add((y, x))

    max_y = max(c[0] for c in stars)
    max_x = max(c[1] for c in stars)

    empty_rows = set()
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if (y, x) in stars:
                break
        else:
            empty_rows.add(y)

    empty_cols = set()
    for x in range(max_x + 1):
        for y in range(max_y + 1):
            if (y, x) in stars:
                break
        else:
            empty_cols.add(x)

    return Data(stars=stars, empty_rows=empty_rows, empty_cols=empty_cols)


def distance(a: Coord, b: Coord, stars: Data, expansion):
    base = abs(a[0] - b[0]) + abs(a[1] - b[1])
    y = sum(
        expansion - 1
        for y in range(min(a[0], b[0]), max(a[0], b[0]))
        if y in stars.empty_rows
    )
    x = sum(
        expansion - 1
        for x in range(min(a[1], b[1]), max(a[1], b[1]))
        if x in stars.empty_cols
    )
    return base + y + x


def solve(stars: Data, expansion: int) -> int:
    total = 0
    unique_pairs = {tuple(sorted(p)) for p in itertools.permutations(stars.stars, 2)}
    for a, b in unique_pairs:
        total += distance(a, b, stars, expansion=expansion)
    return total


def part1(data: str) -> int:
    stars = parse(data)
    return solve(stars, expansion=2)


def part2(data: str) -> int:
    stars = parse(data)
    return solve(stars, expansion=1000000)


def test_part1():
    data = dedent(
        """
        ...#......
        .......#..
        #.........
        ..........
        ......#...
        .#........
        .........#
        ..........
        .......#..
        #...#.....
        """
    ).strip()

    assert distance((9, 0), (9, 4), parse(data), 2) == 5
    assert distance((0, 3), (8, 7), parse(data), 2) == 15
    assert distance((2, 0), (6, 9), parse(data), 2) == 17
    assert part1(data) == 374


def test_part2():
    data = dedent(
        """
        ...#......
        .......#..
        #.........
        ..........
        ......#...
        .#........
        .........#
        ..........
        .......#..
        #...#.....
        """
    ).strip()

    assert solve(parse(data), 10) == 1030
    assert solve(parse(data), 100) == 8410


if __name__ == "__main__":
    print(part1(read_data()))
    print(part2(read_data()))
