"""Day 03: Squares with Three Sides.


"""

import itertools
import os
from typing import List


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> List[List[int]]:
    sides = []
    for line in data.split("\n"):
        sides.append([int(num) for num in line.split()])
    return sides


def valid(triangles):
    return len([tri for tri in triangles if sum(sorted(tri)[:2]) > sorted(tri)[2]])


def part1(triangles):
    return valid(triangles)


def part2(triangles):
    return valid(
        itertools.batched(
            [tri[0] for tri in triangles]
            + [tri[1] for tri in triangles]
            + [tri[2] for tri in triangles],
            3,
        )
    )


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
