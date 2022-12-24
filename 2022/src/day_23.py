"""Day 23
"""

import itertools
import os
from typing import Dict, List, Set, Tuple, TypeAlias

Coordinates: TypeAlias = Set[Tuple[int, int]]


def parse(fname: str) -> Coordinates:
    elves: Set[Tuple[int, int]] = set()
    with open(fname, encoding="utf-8") as handle:
        for y, line in enumerate(handle.read().strip().split("\n")):
            for x, char in enumerate(line):
                if char == "#":
                    elves.add((y, x))
    return elves


def debug(elves):
    min_y = min(elf[0] for elf in elves)
    max_y = max(elf[0] for elf in elves)
    min_x = min(elf[1] for elf in elves)
    max_x = max(elf[1] for elf in elves)
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            print("#" if (y, x) in elves else ".", end="")
        print()
    print()


DIRECTIONS = (
    tuple([(-1, n) for n in range(-1, 2)]),  # up
    tuple([(1, n) for n in range(-1, 2)]),  # down
    tuple([(n, -1) for n in range(-1, 2)]),  # left
    tuple([(n, 1) for n in range(-1, 2)]),  # right
)


def move(elves: Coordinates, round: int) -> Coordinates:
    proposed: Dict[Tuple[int, int], List[Tuple[int, int]]] = {}
    new_elves: Coordinates = set()

    consider_directions = (
        DIRECTIONS[round % len(DIRECTIONS) :] + DIRECTIONS[: round % len(DIRECTIONS)]
    )

    for (elf_y, elf_x) in elves:
        if all(
            (elf_y + dy, elf_x + dx) not in elves
            for dx in range(-1, 2)
            for dy in range(-1, 2)
            if not (dy == 0 and dx == 0)
        ):
            new_elves.add((elf_y, elf_x))
            continue

        for moves in consider_directions:
            if all((elf_y + dy, elf_x + dx) not in elves for (dy, dx) in moves):
                proposed.setdefault(
                    (elf_y + moves[1][0], elf_x + moves[1][1]), []
                ).append((elf_y, elf_x))
                break
        else:
            new_elves.add((elf_y, elf_x))

    for target, candidates in proposed.items():
        if len(candidates) == 1:
            new_elves.add(target)
        else:
            new_elves.update(candidates)

    return new_elves


def solve(fname: str) -> int:
    elves = parse(fname)

    for i in range(10):
        elves = move(elves, i)

    min_y = min(elf[0] for elf in elves)
    max_y = max(elf[0] for elf in elves)
    min_x = min(elf[1] for elf in elves)
    max_x = max(elf[1] for elf in elves)
    return (max_y - min_y + 1) * (max_x - min_x + 1) - len(elves)


def solve2(fname: str) -> int:
    elves = parse(fname)
    r = 0
    for r in itertools.count():
        new_elves = move(elves, r)
        if elves == new_elves:
            return r + 1
        elves = new_elves

    raise Exception("Should not happen")


day = os.path.basename(__file__).split(".")[0].split("_")[1]
base = os.path.join(os.path.dirname(__file__), "input", f"{day}")
print(solve(f"{base}.test"))
print(solve(f"{base}.input"))

print(solve2(f"{base}.test"))
print(solve2(f"{base}.input"))
