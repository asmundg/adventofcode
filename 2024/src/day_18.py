"""Day 18: RAM Run

Straight forward BFS today. We trivially solve part 2 by reusing part
1 and just decrementing the number of walls we drop in until we can
find a solution (it's much faster if we start from the end, since
steps to failed search should be shorter than steps to goal, unless
the input is particularly evil).
"""

import os
from textwrap import dedent

from common import cartesian
from common.cartesian import Coord


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> list[Coord]:
    coords: list[Coord] = []
    for line in data.split("\n"):
        a, b = line.split(",")
        coords.append((int(a), int(b)))
    return coords


def part1(corrupted: list[Coord], n_bytes: int, max_y: int, max_x: int) -> int:
    visited: set[Coord] = set()
    search: list[tuple[Coord, int]] = [((0, 0), 0)]
    current_corrupted = set(corrupted[:n_bytes])
    while search:
        node, steps = search.pop(0)
        if node in visited:
            continue

        if node == (max_y, max_x):
            return steps

        visited.add(node)
        for neighbor in cartesian.neighbors(node):
            if neighbor in current_corrupted:
                continue

            if 0 <= neighbor[0] <= max_y and 0 <= neighbor[1] <= max_x:
                search.append((neighbor, steps + 1))

    return -1


def part2(corrupted: list[Coord], max_y: int, max_x: int) -> str:
    for n in range(len(corrupted), 0, -1):
        if part1(corrupted, n, max_y, max_x) >= 1:
            return str(corrupted[n][0]) + "," + str(corrupted[n][1])
    raise Exception("No solution found")


def test_part1() -> None:
    data = dedent("""
    5,4
    4,2
    4,5
    3,0
    2,1
    6,3
    2,4
    1,5
    0,6
    3,3
    2,6
    5,1
    1,2
    5,5
    2,5
    6,5
    1,4
    0,4
    6,4
    1,1
    6,1
    1,0
    0,5
    1,6
    2,0
    """).strip()
    assert part1(parse(data), 12, 6, 6) == 22


def test_part2() -> None:
    data = dedent("""
    5,4
    4,2
    4,5
    3,0
    2,1
    6,3
    2,4
    1,5
    0,6
    3,3
    2,6
    5,1
    1,2
    5,5
    2,5
    6,5
    1,4
    0,4
    6,4
    1,1
    6,1
    1,0
    0,5
    1,6
    2,0
    """).strip()
    assert part2(parse(data), 6, 6) == "6,1"


if __name__ == "__main__":
    print(part1(parse(read_data()), 1024, 70, 70))
    print(part2(parse(read_data()), 70, 70))
