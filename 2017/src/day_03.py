"""Day 03: Spiral Memory

I'm sure there's some mathematical formula we can use here, but we can
also just walk the graph to find the target coordinate.

For part 2, we use the same traversal logic, but actually store the
values at each position so we can look them up later.

"""

import os
from typing import Callable

import cartesian


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> int:
    return int(data)


def part1(target: int) -> int:
    pos = (0, 0)
    bounds = {cartesian.RIGHT: (0, 0), cartesian.UP: (0, 0), cartesian.LEFT: (0, 0), cartesian.DOWN: (0, 0)}
    bound_checks: dict[cartesian.Coord, Callable[[cartesian.Coord], bool]] = {
        cartesian.RIGHT: lambda pos: pos[1] > bounds[cartesian.RIGHT][1],
        cartesian.UP: lambda pos: pos[0] < bounds[cartesian.UP][0],
        cartesian.LEFT: lambda pos: pos[1] < bounds[cartesian.LEFT][1],
        cartesian.DOWN: lambda pos: pos[0] > bounds[cartesian.DOWN][0],
    }
    direction = cartesian.RIGHT
    for _ in range(1, target):
        pos = cartesian.move(pos, direction)
        if bound_checks[direction](pos):
            bounds[direction] = pos
            direction = cartesian.LEFT_TURN[direction]

    return abs(pos[0]) + abs(pos[1])


def part2(target: int) -> int:
    pos = (0, 0)
    bounds = {cartesian.RIGHT: (0, 0), cartesian.UP: (0, 0), cartesian.LEFT: (0, 0), cartesian.DOWN: (0, 0)}
    bound_checks: dict[cartesian.Coord, Callable[[cartesian.Coord], bool]] = {
        cartesian.RIGHT: lambda pos: pos[1] > bounds[cartesian.RIGHT][1],
        cartesian.UP: lambda pos: pos[0] < bounds[cartesian.UP][0],
        cartesian.LEFT: lambda pos: pos[1] < bounds[cartesian.LEFT][1],
        cartesian.DOWN: lambda pos: pos[0] > bounds[cartesian.DOWN][0],
    }

    mem = {(0, 0): 1}
    direction = cartesian.RIGHT
    while True:
        pos = cartesian.move(pos, direction)
        mem[pos] = sum(mem.get(neigh, 0) for neigh in cartesian.neighbors(pos, diagonal=True))
        if mem[pos] > target:
            return mem[pos]

        if bound_checks[direction](pos):
            bounds[direction] = pos
            direction = cartesian.LEFT_TURN[direction]


def test_part1() -> None:
    assert part1(1) == 0
    assert part1(12) == 3
    assert part1(23) == 2
    assert part1(1024) == 31


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
