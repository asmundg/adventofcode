"""Day 12: Christmas Tree Farm

Wtf. This looks like a tiling problem initially, but there are no
fixed positions? permutations seem like they would grow out of bounds
extremely quickly if we try all sequences, but shapes can be placed
anywhere not occupied.

There might be some constraints re "growing outwards" and leaving
minimal open space. But then there's the count requirement. As a
bonus, there seems to be a prime in each count requirement, so we
can't subdivide the problem space either (even if there was some kind
of magical perfect alignment at the boundary).

It might be possible to grow bigger tiles out of ideal combinations of
the smaller tiles. This would let us precompute the size of optimal
placements, which we can just multiply up to get _near_ the target
configuration, then manually place the remainders.

There is a vastly simpler hack we can try though. Manually looking at
the tiles makes it look like any combination of packing will leave
slightly more than 1 empty space. This means we can try just
multiplying the tile sizes (how much space they actually use) with the
number of occurrences per tile, plus a waste factor (1.5 in this
case). If this is less than or equal to available space, it should
(might?) work.

Unclear if this is a globally correct solution, but it works!
"""

import os
from dataclasses import dataclass
from textwrap import dedent

from .cartesian import Coord


@dataclass(frozen=True)
class Problem:
    tiles: list[set[Coord]]
    sizes: list[Coord]
    counts: list[list[int]]


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> Problem:
    parts = data.split("\n\n")
    tiles: list[set[Coord]] = []
    for t in parts[:-1]:
        tiles.append(set())
        for y, line in enumerate(t.split("\n")[1:]):
            for x, char in enumerate(line):
                if char == "#":
                    tiles[-1].add((y, x))

    sizes: list[Coord] = []
    counts: list[list[int]] = []
    for t in parts[-1].split("\n"):
        tree = t.split()
        y, x = tree[0][:-1].split("x")
        sizes.append((int(y), int(x)))
        counts.append([int(n) for n in tree[1:]])

    return Problem(tiles, sizes, counts)


def part1(problem: Problem) -> int:
    lens = [len(tile) for tile in problem.tiles]
    return len(
        [
            1
            for ci, count in enumerate(problem.counts)
            if (sum(psize * count[pi] for pi, psize in enumerate(lens)) + sum(count) * 1.5)
            <= problem.sizes[ci][0] * problem.sizes[ci][1]
        ]
    )


def test_part1() -> None:
    data = dedent(
        """
        0:
        ###
        ##.
        ##.
        
        1:
        ###
        ##.
        .##
        
        2:
        .##
        ###
        ##.
        
        3:
        ##.
        ###
        ##.
        
        4:
        ###
        #..
        ###
        
        5:
        ###
        .#.
        ###
        
        4x4: 0 0 0 0 2 0
        12x5: 1 0 1 0 2 2
        12x5: 1 0 1 0 3 2
        """
    ).strip()
    assert part1(parse(data)) == 2


if __name__ == "__main__":
    print(part1(parse(read_data())))
