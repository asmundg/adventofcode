"""Day 24: Air Duct Spelunking

It's TSP with a twist! I think this should be doable by finding all
pairwise distances and then testing all permutations (max 10!, which
should be completely feasible, especially since we can prune the
search tree).

Part 2 works perfectly for this approach, since it just requires
adding the final cost from last wire back to 0 to each permutation.

"""

import itertools
import os
from textwrap import dedent

from common import cartesian


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> dict[cartesian.Coord, str]:
    ducts: dict[cartesian.Coord, str] = {}
    for y, line in enumerate(data.split("\n")):
        for x, char in enumerate(line):
            ducts[(y, x)] = char
    return ducts


def bfs_distance(ducts: dict[cartesian.Coord, str], start: cartesian.Coord, goal: cartesian.Coord) -> int:
    visited: set[cartesian.Coord] = {start}
    search: list[tuple[cartesian.Coord, int]] = [(start, 0)]
    while search:
        pos, cost = search.pop(0)
        if pos == goal:
            return cost

        for neigh in cartesian.neighbors(pos):
            if ducts.get(neigh, "#") != "#" and neigh not in visited:
                search.append((neigh, cost + 1))
                visited.add(neigh)

    raise Exception("oops")


def part1(ducts: dict[cartesian.Coord, str], must_return: bool = False) -> int:
    wires = {num: pos for pos, num in ducts.items() if num.isdigit()}

    pairs = {
        pair: bfs_distance(ducts, wires[pair[0]], wires[pair[1]])
        for pair in itertools.permutations((key for key in wires.keys()), 2)
    }
    best = float("inf")
    for sequence in itertools.permutations((key for key in wires.keys() if key != "0"), len(wires.keys()) - 1):
        cost = sum(
            pairs[pair]
            for pair in (
                zip("0" + "".join(sequence), "".join(sequence) + "0")
                if must_return
                else zip("0" + "".join(sequence[:-1]), sequence)
            )
        )
        best = min(best, cost)
    return int(best)


def test_part1() -> None:
    data = dedent("""
    ###########
    #0.1.....2#
    #.#######.#
    #4.......3#
    ###########
    """).strip()
    assert part1(parse(data)) == 14


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part1(parse(read_data()), must_return=True))
