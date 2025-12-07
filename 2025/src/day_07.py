"""Day 07: Laboratories

The meaningful thing to track here is the particle/front of beam. Each
time a particle hits a splitter, that's a beam split. We can then
iterate time by moving down one line at a time and computing for all
particles. This takes care of merging when we get multiple beams
entering the same space, since we only track "is there a beam here".

This handles part 2 as well, which would scale out of control if we
tried tracing individual beams. Except now we also need to track how
many different ways we could get here. Which is a counter summing the
number of incoming paths.

"""

import os
from dataclasses import dataclass
from textwrap import dedent

from .cartesian import DOWN, LEFT, RIGHT, Coord, move


@dataclass
class Problem:
    start: Coord
    splitters: set[Coord]
    end: int


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> Problem:
    problem = Problem((0, 0), set(), 0)
    for y, line in enumerate(data.split("\n")):
        for x, char in enumerate(line):
            if char == "S":
                problem.start = (y, x)
            elif char == "^":
                problem.splitters.add((y, x))
    problem.end = y

    return problem


def solve(problem: Problem) -> tuple[int, int]:
    beams = {move(problem.start, DOWN): 1}
    total_paths = 0
    splits = 0
    while beams:
        next_beams: dict[Coord, int] = {}
        for beam, paths in beams.items():
            if beam[0] == problem.end:
                total_paths += paths
            elif move(beam, DOWN) in problem.splitters:
                splits += 1
                for next_start in (move(move(beam, DOWN), LEFT), move(move(beam, DOWN), RIGHT)):
                    next_beams[next_start] = next_beams.get(next_start, 0) + paths
            else:
                next_beams[move(beam, DOWN)] = next_beams.get(move(beam, DOWN), 0) + paths
        beams = next_beams
    return splits, total_paths


def part1(problem: Problem) -> int:
    return solve(problem)[0]


def part2(problem: Problem) -> int:
    return solve(problem)[1]


def test_part1() -> None:
    data = dedent(
        """
        .......S.......
        ...............
        .......^.......
        ...............
        ......^.^......
        ...............
        .....^.^.^.....
        ...............
        ....^.^...^....
        ...............
        ...^.^...^.^...
        ...............
        ..^...^.....^..
        ...............
        .^.^.^.^.^...^.
        ...............
        """
    ).strip()
    assert part1(parse(data)) == 21


def test_part2() -> None:
    data = dedent(
        """
        .......S.......
        ...............
        .......^.......
        ...............
        ......^.^......
        ...............
        .....^.^.^.....
        ...............
        ....^.^...^....
        ...............
        ...^.^...^.^...
        ...............
        ..^...^.....^..
        ...............
        .^.^.^.^.^...^.
        ...............
        """
    ).strip()
    assert part2(parse(data)) == 40


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
