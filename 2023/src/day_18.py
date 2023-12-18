"""Day 18: Lavaduct Lagoon

Yay, math is apparently hard. It took me significant time to go from
'this looks like some kind of geometry problem' to 'of course the
mathematicians have already solved this'.

The most cumbersome part, after figuring out the formula, is to figure
out how to correctly trace the outside of the shape. I'm sure there is
a prettier way to do this, but tracking whether we're making an inside
our outside turn works fine to keep the coordinates aligned with the
area excavated.

"""

import os
from textwrap import dedent

from typing import List, Tuple

from common.cartesian import Coord, UP, DOWN, LEFT, RIGHT


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse1(data: str) -> List[Coord]:
    vectors: List[Coord] = [(0, 0)]

    directions = {"U": UP, "D": DOWN, "L": LEFT, "R": RIGHT}
    outer_turns = {"U": RIGHT, "D": LEFT, "L": UP, "R": DOWN}

    node = (0, 0)
    lines = data.split("\n")
    outside = True
    for a, b in zip(lines, lines[1:] + [lines[0]]):
        direction, length, _ = a.split()
        next_direction, _, _ = b.split()
        next_outside = outer_turns[direction] == directions[next_direction]
        extra = 0
        if outside and next_outside:
            extra = 1
        if not outside and not next_outside:
            extra = -1
        node = move(node, directions[direction], int(length) + extra)
        vectors.append(node)
        outside = next_outside

    return vectors


def parse2(data: str) -> List[Coord]:
    vectors: List[Coord] = [(0, 0)]

    outer_turns = {UP: RIGHT, DOWN: LEFT, LEFT: UP, RIGHT: DOWN}

    def parse_color(color: str) -> Tuple[Coord, int]:
        directions = {"0": RIGHT, "1": DOWN, "2": LEFT, "3": UP}

        color = color[2:-1]
        return (directions[color[-1]], int(color[:-1], 16))

    node = (0, 0)
    lines = data.split("\n")
    outside = True
    for a, b in zip(lines, lines[1:] + [lines[0]]):
        direction, length = parse_color(a.split()[2])
        next_direction, _ = parse_color(b.split()[2])

        next_outside = outer_turns[direction] == next_direction
        extra = 0
        if outside and next_outside:
            extra = 1
        if not outside and not next_outside:
            extra = -1
        node = move(node, direction, int(length) + extra)
        vectors.append(node)
        outside = next_outside

        vectors.append(node)

    return vectors


def move(current: Coord, direction: Coord, n: int = 1) -> Coord:
    return (
        current[0] + (direction[0] * n),
        current[1] + (direction[1] * n),
    )


def area(points: List[Coord]):
    total = 0
    for a, b in zip(points, points[1:]):
        total += (a[0] + b[0]) * (a[1] - b[1])
    return abs(total) / 2


def part1(data: str) -> int:
    return int(area(parse1(data)))


def part2(data: str) -> int:
    return int(area(parse2(data)))


def test_part1():
    data = dedent(
        """
        R 6 (#70c710)
        D 5 (#0dc571)
        L 2 (#5713f0)
        D 2 (#d2c081)
        R 2 (#59c680)
        D 2 (#411b91)
        L 5 (#8ceee2)
        U 2 (#caa173)
        L 1 (#1b58a2)
        U 2 (#caa171)
        R 2 (#7807d2)
        U 3 (#a77fa3)
        L 2 (#015232)
        U 2 (#7a21e3)
        """
    ).strip()

    assert (part1(data)) == 62


def test_part2():
    data = dedent(
        """
        R 6 (#70c710)
        D 5 (#0dc571)
        L 2 (#5713f0)
        D 2 (#d2c081)
        R 2 (#59c680)
        D 2 (#411b91)
        L 5 (#8ceee2)
        U 2 (#caa173)
        L 1 (#1b58a2)
        U 2 (#caa171)
        R 2 (#7807d2)
        U 3 (#a77fa3)
        L 2 (#015232)
        U 2 (#7a21e3)
        """
    ).strip()

    assert (part2(data)) == 952408144115


if __name__ == "__main__":
    print(part1(read_data()))
    print(part2(read_data()))
