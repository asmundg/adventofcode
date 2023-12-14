"""Day 14: Parabolic Reflector Dish

Cycle detection day! We _can_ brute force the iterations, but it takes
hours and hours. Instead, we can find the repeating cycle length and
skip to the end.

To do this, we track which board states we've seen. Once we've seen
the same state twice, we have found a cycle and the state will keep
repeating. From there, we can find the largest multiple of the cycle
length, add it, since that will leave us exactly where we are, and
then run the remaining steps.

Also abuse of zip(*reversed(lines)) to avoid both rotation matrices
and implementing the gravity algorithm for each direction. It's a bit
expensive, but doesn't really hurt us for the limited number of
iterations we need to run.

"""

import copy
import math
import os
from textwrap import dedent

from typing import List, TypeAlias

Data: TypeAlias = List[List[str]]


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> Data:
    return [list(line) for line in data.split("\n")]


def rotate(lines: List[List[str]], n=1):
    for _ in range(n):
        lines = [list(t) for t in zip(*reversed(lines))]
    return lines


def tilt(lines: Data, direction: str) -> Data:
    lines = copy.deepcopy(lines)

    rotations = {"E": 3, "S": 2, "W": 1, "N": 0}

    if direction in rotations:
        lines = rotate(lines, rotations[direction])

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "O":
                for new_y in range(y, 0, -1):
                    if lines[new_y - 1][x] != ".":
                        if new_y != y:
                            lines[new_y][x] = "O"
                            lines[y][x] = "."
                        break
                else:
                    if y != 0:
                        lines[0][x] = "O"
                        lines[y][x] = "."

    if direction in rotations:
        lines = rotate(lines, 4 - rotations[direction])

    return lines


def part1(data: str) -> int:
    lines = parse(data)

    lines = tilt(lines, direction="N")
    total = 0
    for y, line in enumerate(lines):
        for _, char in enumerate(line):
            total += len(lines) - y if char == "O" else 0
    return total


def part2(data: str) -> int:
    lines = parse(data)

    cache = {}
    start_of_cycle = (-1, "")
    target = 1000000000
    rest = 0
    for n in range(target):
        for direction in "NWSE":
            lines = tilt(lines, direction=direction)

        key = "\n".join(["".join(line) for line in lines])
        if key in cache:
            if start_of_cycle[0] < 0:
                start_of_cycle = (n, key)
            elif start_of_cycle[1] == key:
                cycle_length = n - start_of_cycle[0]
                remaining = target - n
                rest = (
                    remaining
                    - cycle_length * (math.floor(remaining / cycle_length))
                    - 1
                )
                break
        else:
            cache[key] = lines

    for _ in range(rest):
        for direction in "NWSE":
            lines = tilt(lines, direction=direction)

    total = 0
    for y, line in enumerate(lines):
        for _, char in enumerate(line):
            total += len(lines) - y if char == "O" else 0
    return total


def test_part1():
    data = dedent(
        """
        O....#....
        O.OO#....#
        .....##...
        OO.#O....O
        .O.....O#.
        O.#..O.#.#
        ..O..#O..O
        .......O..
        #....###..
        #OO..#....
        """
    ).strip()

    assert (part1(data)) == 136


def test_part2():
    data = dedent(
        """
        O....#....
        O.OO#....#
        .....##...
        OO.#O....O
        .O.....O#.
        O.#..O.#.#
        ..O..#O..O
        .......O..
        #....###..
        #OO..#....
        """
    ).strip()

    assert (part2(data)) == 64


if __name__ == "__main__":
    print(part1(read_data()))
    print(part2(read_data()))
