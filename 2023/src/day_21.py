"""Day 21: Step Counter

Part 1 is a trivial flood fill (we just need to keep track of plots
reachable on every other step, since it's impossible to move _back_ to
a plot if we have an uneven number of steps left when we're on it).

Part 2 scales out of control and we need to cheat. Fortunately, the
input is carefully crafted to have a number of steps that divide by
the grid size _and_ to have no obstacles in the starting row and
column. This means that the bounding box is perfectly regular, with
corners at the grid boundary. This means that if we can find the
number of reachable tiles one and a half tile lengths out, we can just
multiply this by some factor to get the actual result.

This means we can find the qudractic formula defining the number of
reachable slots. This isn't a true general solution and doesn't work
for the test input, since is has obstacles in the starting row and
column.

"""

import os
from textwrap import dedent
from common import cartesian
from typing import Tuple, List, Set, Dict
import z3


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str):
    coords = {}

    start = (0, 0)
    for y, line in enumerate(data.split("\n")):
        for x, char in enumerate(line):
            coords[(y, x)] = char if char != "S" else "."
            if char == "S":
                start = (y, x)

    return coords, start


def part1(data: str, steps: int) -> int:
    coords, start = parse(data)

    # BFS
    search: List[Tuple[cartesian.Coord, int]] = [(start, steps)]
    seen: Set[cartesian.Coord] = set()
    reachable: Set[cartesian.Coord] = set()
    while search:
        point, n = search.pop(0)
        if n % 2 == 0:
            reachable.add(point)
        if n == 0:
            continue

        for neigh in cartesian.neighbors(point):
            if neigh not in seen and coords.get(neigh, "") == ".":
                search.append((neigh, n - 1))
                seen.add(neigh)

    return len(reachable)


def part2(data: str, steps: int, cheat=False) -> int:
    coords, start = parse(data)
    max_y = max(coords.keys(), key=lambda c: c[0])[0]
    max_x = max(coords.keys(), key=lambda c: c[1])[1]
    assert max_y == max_x

    # BFS
    def find_reachable(steps):
        search: List[Tuple[cartesian.Coord, int]] = [(start, steps)]
        seen: Set[cartesian.Coord] = set()
        reachable: Set[cartesian.Coord] = set()
        while search:
            point, n = search.pop(0)
            if n % 2 == 0:
                reachable.add(point)
            if n == 0:
                continue

            for neigh in cartesian.neighbors(point):
                normalized = (neigh[0] % (max_y + 1), neigh[1] % (max_x + 1))
                if neigh not in seen and coords.get(normalized, "") == ".":
                    search.append((neigh, n - 1))
                    seen.add(neigh)
        return reachable

    # Enable cheat mode: Since we can trivially determine the bounding
    # box of reachable spaces, and it happens to align perfectly with
    # the grid size, the numer of reachable plots should follow a
    # quadratic equation. Which we can identify by calculating the
    # actual number for a small bounding box.
    if cheat:
        solver = z3.Solver()
        a = z3.Int("a")
        b = z3.Int("b")
        c = z3.Int("c")
        for n in range(3):
            print(max_x)
            s = max_x / 2 + (max_x + 1) * n
            reachable = len(find_reachable(s))
            print(s, reachable)
            solver.add(a * n**2 + b * n + c == reachable)

        assert solver.check() == z3.sat, solver.check()
        m = solver.model()
        sides = steps // (max_x + 1)
        return m[a].as_long() * sides**2 + m[b].as_long() * sides + m[c].as_long()
    else:
        return len(find_reachable(steps))


def test_part1():
    data = dedent(
        """
        ...........
        .....###.#.
        .###.##..#.
        ..#.#...#..
        ....#.#....
        .##..S####.
        .##..#...#.
        .......##..
        .##.#.####.
        .##..##.##.
        ...........
        """
    ).strip()

    assert part1(data, 6) == 16


def test_part2():
    data = dedent(
        """
        ...........
        .....###.#.
        .###.##..#.
        ..#.#...#..
        ....#.#....
        .##..S####.
        .##..#...#.
        .......##..
        .##.#.####.
        .##..##.##.
        ...........
        """
    ).strip()

    assert part2(data, 6) == 16
    assert part2(data, 50) == 1594
    assert part2(data, 100) == 6536
    assert part2(data, 500) == 167004


if __name__ == "__main__":
    print(part1(read_data(), 64))
    print(part2(read_data(), 26501365, cheat=True))
