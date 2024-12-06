"""Day 6: Guard Gallivant

Time to break out the good old cartesian coordinate library. Having a
good representation of where we are, where we are headed and how we
are turning is massively useful and just enough typing that I feel
annoyed about having to do it on the fly.

Part 1 is just following the rules, using the rotations, until we exit
the boundaries.

Part 2 is a bit on the slow side, taking a couple of seconds to test
all possible obstacle locations and re-running part 1 on the new
obstacle set. This is where we get a big payoff for just tracking the
obstacle coordinates and not representing the entire, mostly empty
map.

In contrast to yesterday, finding a loop is exactly what we want. That
would be a fail condition on part 1, but in part 2 it signifies that
we found a valid obstacle location.

"""

import os
from dataclasses import dataclass
from textwrap import dedent

from common import cartesian
from common.cartesian import Coord


@dataclass(frozen=True)
class Data:
    things: set[Coord]
    guard: Coord
    direction: Coord
    max_y: int
    max_x: int


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> Data:
    things: set[Coord] = set()
    guard = (0, 0)
    for y, line in enumerate(data.split("\n")):
        for x, char in enumerate(line):
            if char == "#":
                things.add((y, x))
            elif char == "^":
                guard = (y, x)
    return Data(things, guard, cartesian.UP, y, x)


def walk(data: Data) -> set[tuple[Coord, Coord]]:
    visited: set[tuple[Coord, Coord]] = set()

    direction = cartesian.UP
    guard = data.guard
    while 0 <= guard[0] <= data.max_y and 0 <= guard[1] <= data.max_x:
        visited.add((guard, direction))

        while cartesian.move(guard, direction) in data.things:
            direction = cartesian.RIGHT_TURN[direction]

        guard = cartesian.move(guard, direction)
        if (guard, direction) in visited:
            raise Exception("Cycle!")

    return visited


def part1(data: Data) -> int:
    return len({v[0] for v in walk(data)})


def part2(data: Data) -> int:
    new_things: set[Coord] = set()
    tried: set[Coord] = set()

    for candidate in walk(data):
        for neighbour in [cartesian.move(*candidate), candidate[0]]:
            if (
                not (0 <= neighbour[0] <= data.max_y and 0 <= neighbour[1] <= data.max_x)
                or neighbour == data.guard
                or neighbour in tried
            ):
                continue

            tried.add(neighbour)

            try_things = set(data.things)
            try_things.add(neighbour)
            try:
                walk((Data(try_things, data.guard, data.direction, data.max_y, data.max_x)))
            except:
                new_things.add(neighbour)

    return len(new_things)


def test_part1() -> None:
    data = dedent("""
    ....#.....
    .........#
    ..........
    ..#.......
    .......#..
    ..........
    .#..^.....
    ........#.
    #.........
    ......#...
    """).strip()
    assert part1(parse(data)) == 41


def test_part2() -> None:
    data = dedent("""
    ....#.....
    .........#
    ..........
    ..#.......
    .......#..
    ..........
    .#..^.....
    ........#.
    #.........
    ......#...
    """).strip()
    assert part2(parse(data)) == 6


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
