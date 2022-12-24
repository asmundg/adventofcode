"""Day 24
"""

import os
from dataclasses import dataclass
from typing import Set, Tuple, TypeAlias

Coordinates: TypeAlias = Set[Tuple[int, int]]


@dataclass
class Blizzards:
    up: Coordinates
    down: Coordinates
    left: Coordinates
    right: Coordinates

    bounds: Tuple[int, int]


@dataclass
class Parameters:
    blizzards: Blizzards
    target: Tuple[int, int]


def parse(fname: str) -> Parameters:
    up, down, right, left = set(), set(), set(), set()
    with open(fname, encoding="utf-8") as handle:
        lines = handle.read().strip().split("\n")
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char in "^v<>":
                    if char == "^":
                        up.add((y, x))
                    elif char == "v":
                        down.add((y, x))
                    elif char == "<":
                        left.add((y, x))
                    else:
                        right.add((y, x))

        return Parameters(
            blizzards=Blizzards(
                up=up,
                down=down,
                left=left,
                right=right,
                bounds=(len(lines), len(lines[0])),
            ),
            target=(len(lines) - 1, lines[-1].index(".")),
        )


def move(blizzards: Blizzards) -> Blizzards:
    new_blizzards = Blizzards(set(), set(), set(), set(), blizzards.bounds)
    for new, old, direction in (
        (new_blizzards.up, blizzards.up, (-1, 0)),
        (new_blizzards.down, blizzards.down, (1, 0)),
        (new_blizzards.left, blizzards.left, (0, -1)),
        (new_blizzards.right, blizzards.right, (0, 1)),
    ):
        for y, x in old:
            new_y, new_x = y + direction[0], x + direction[1]
            if new_y < 1:
                new_y = blizzards.bounds[0] - 2
            elif new_y > blizzards.bounds[0] - 2:
                new_y = 1
            if new_x < 1:
                new_x = blizzards.bounds[1] - 2
            elif new_x > blizzards.bounds[1] - 2:
                new_x = 1
            new.add((new_y, new_x))
    return new_blizzards


def debug(blizzards: Blizzards, elves: Coordinates) -> None:
    for y in range(blizzards.bounds[0]):
        for x in range(blizzards.bounds[1]):
            overlapping = [
                sym
                for sym, coords in zip(
                    "^v<>",
                    (blizzards.up, blizzards.down, blizzards.left, blizzards.right),
                )
                if (y, x) in coords
            ]
            if (y, x) in elves:
                print("E", end="")
            elif len(overlapping) > 1:
                print(len(overlapping), end="")
            elif len(overlapping) > 0:
                print(overlapping[0], end="")
            else:
                print(".", end="")
        print()
    print()


def walk(
    start: Tuple[int, int], target: Tuple[int, int], blizzards=Blizzards
) -> Tuple[int, Blizzards]:
    t = 0
    elves: Set[Tuple[int, int]] = set([start])
    while True:
        t += 1
        blizzards = move(blizzards)
        for elf in set(elves):
            elves.update(
                [
                    (elf[0] + move[0], elf[1] + move[1])
                    for move in ((-1, 0), (1, 0), (0, -1), (0, 1))
                    if (elf[0] + move[0], elf[1] + move[1]) == target
                    or (
                        0 < elf[0] + move[0] < blizzards.bounds[0] - 1
                        and 0 < elf[1] + move[1] < blizzards.bounds[1] - 1
                    )
                ]
            )
        elves = elves - (
            blizzards.up | blizzards.down | blizzards.left | blizzards.right
        )

        if target in elves:
            return t, blizzards


def solve(fname: str) -> int:
    p = parse(fname)
    return walk((0, 1), p.target, p.blizzards)[0]


def solve2(fname: str) -> int:
    p = parse(fname)

    t0, blizzards = walk(start=(0, 1), target=p.target, blizzards=p.blizzards)
    t1, blizzards = walk(start=p.target, target=(0, 1), blizzards=blizzards)
    t2, blizzards = walk(start=(0, 1), target=p.target, blizzards=blizzards)
    return sum((t0, t1, t2))


day = os.path.basename(__file__).split(".")[0].split("_")[1]
base = os.path.join(os.path.dirname(__file__), "input", f"{day}")

print(solve(f"{base}.test"))
print(solve(f"{base}.input"))

print(solve2(f"{base}.test"))
print(solve2(f"{base}.input"))
