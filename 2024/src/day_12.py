"""Day 12: Garden Groups

First day of hitting a mental wall.

The first part can be solved trivially with a flood fill and then just
counting the number of 'other' type neighbors for each node.

This breaks down for part 2 though, where we need to count groups of
straight edges. I first had the bright idea of just tracing the edge,
but this breaks down in all sort of horrible literal corner
cases. Fortunately, just line scanning over the whole world instead
works fine. For each line, horizontally and vertically, we can count
the number of contiguous edge nodes, where we find edge nodes by
comparing nodes on each side of the line and checking if one is inside
and the other is outside (and then the reverse).
"""

import itertools
import os
from dataclasses import dataclass
from textwrap import dedent
from typing import Callable

from common import cartesian
from common.cartesian import Coord


@dataclass(frozen=True)
class Data:
    plots: dict[Coord, str]
    max_y: int
    max_x: int


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> Data:
    plots: dict[Coord, str] = {}
    for y, line in enumerate(data.split("\n")):
        for x, char in enumerate(line):
            plots[(y, x)] = char

    return Data(plots, max_y=y, max_x=x)


def fill(start: cartesian.Coord, data: Data) -> set[cartesian.Coord]:
    visited: set[cartesian.Coord] = set([start])
    search: list[cartesian.Coord] = [start]
    plant_type = data.plots[start]
    while search:
        node = search.pop()
        for neighbor in cartesian.neighbors(node):
            if neighbor in visited:
                continue

            if data.plots.get(neighbor, None) == plant_type:
                visited.add(neighbor)
                search.append(neighbor)

    return visited


def get_score(plots: set[cartesian.Coord]) -> int:
    perimeter = 0
    for plot in plots:
        for neighbor in cartesian.neighbors(plot):
            if neighbor not in plots:
                perimeter += 1

    return perimeter * len(plots)


def get_score2(plots: set[cartesian.Coord]) -> int:
    edges = 0
    max_y = max(y for y, x in plots)
    max_x = max(x for y, x in plots)
    for y in range(-1, max_y + 1):
        edges += sum(
            1
            for (edge, _) in itertools.groupby((y, x) not in plots and (y + 1, x) in plots for x in range(max_x + 1))
            if edge
        )
        edges += sum(
            1
            for (edge, _) in itertools.groupby((y, x) in plots and (y + 1, x) not in plots for x in range(max_x + 1))
            if edge
        )

    for x in range(-1, max_x + 1):
        edges += sum(
            1
            for (edge, _) in itertools.groupby((y, x) not in plots and (y, x + 1) in plots for y in range(max_y + 1))
            if edge
        )
        edges += sum(
            1
            for (edge, _) in itertools.groupby((y, x) in plots and (y, x + 1) not in plots for y in range(max_y + 1))
            if edge
        )

    return edges * len(plots)


def solve(data: Data, scorefn: Callable[[set[cartesian.Coord]], int]) -> int:
    processed: set[cartesian.Coord] = set()
    total = 0

    for plot in data.plots:
        if plot not in processed:
            in_plot = fill(plot, data)
            processed.update(in_plot)
            total += scorefn(in_plot)

    return total


def part1(data: Data) -> int:
    return solve(data, get_score)


def part2(data: Data) -> int:
    return solve(data, get_score2)


def test_part1() -> None:
    data = dedent("""
    RRRRIICCFF
    RRRRIICCCF
    VVRRRCCFFF
    VVRCCCJFFF
    VVVVCJJCFE
    VVIVCCJJEE
    VVIIICJJEE
    MIIIIIJJEE
    MIIISIJEEE
    MMMISSJEEE
    """).strip()
    assert part1(parse(data)) == 1930


def test_part2_a() -> None:
    data = dedent("""
    EEEEE
    EXXXX
    EEEEE
    EXXXX
    EEEEE
    """).strip()
    assert part2(parse(data)) == 236


def test_part2_b() -> None:
    data = dedent("""
    AAAAAA
    AAABBA
    AAABBA
    ABBAAA
    ABBAAA
    AAAAAA
    """).strip()
    assert part2(parse(data)) == 368


def test_part2_c() -> None:
    data = dedent("""
    RRRRIICCFF
    RRRRIICCCF
    VVRRRCCFFF
    VVRCCCJFFF
    VVVVCJJCFE
    VVIVCCJJEE
    VVIIICJJEE
    MIIIIIJJEE
    MIIISIJEEE
    MMMISSJEEE
    """).strip()
    assert part2(parse(data)) == 1206


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
