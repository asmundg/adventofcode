"""Day 10: Hoof It

Relatively straight forward path search. We need to start walking
along all step 1 inclines from each node, starting at each start. If
we track the path taken along with the current node, we count both
destinations found (part 1) and the number of unique paths taken (part
2). Especially when we use sets, which will nicely deduplicate for us.
"""

import os
from dataclasses import dataclass
from textwrap import dedent

from common import cartesian
from common.cartesian import Coord, Path


@dataclass(frozen=True)
class Data:
    map: dict[Coord, int]
    starts: set[Coord]


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> Data:
    map: dict[Coord, int] = dict()
    starts: set[Coord] = set()

    for y, line in enumerate(data.split("\n")):
        for x, char in enumerate(line):
            if char == "0":
                starts.add((y, x))
            map[(y, x)] = int(char)
    return Data(map, starts)


def walk(data: Data, start: Coord) -> set[Path]:
    found_paths: set[Path] = set()
    search: set[tuple[Coord, Path]] = {(start, tuple())}
    while search:
        node, path = search.pop()
        if data.map[node] == 9:
            found_paths.add((path + (node,)))
        for neighbor in cartesian.neighbors(node):
            if neighbor in data.map and data.map[neighbor] == data.map[node] + 1:
                search.add((neighbor, path + (neighbor,)))

    return found_paths


def part1(data: Data) -> int:
    return sum(len(set([path[-1] for path in walk(data, start)])) for start in data.starts)


def part2(data: Data) -> int:
    return sum(len(walk(data, start)) for start in data.starts)


def test_part1() -> None:
    data = dedent("""
    89010123
    78121874
    87430965
    96549874
    45678903
    32019012
    01329801
    10456732
    """).strip()
    assert part1(parse(data)) == 36


def test_part2() -> None:
    data = dedent("""
    89010123
    78121874
    87430965
    96549874
    45678903
    32019012
    01329801
    10456732
    """).strip()
    assert part2(parse(data)) == 81


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
