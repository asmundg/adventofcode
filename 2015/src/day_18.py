"""Day 18: Like a GIF For Your Yard.

Hello, Game of Life!
"""

import os

from typing import Tuple, Set, TypeAlias

State: TypeAlias = Set[Tuple[int, int]]


def parse(fname: str) -> State:
    state: Set[Tuple[int, int]] = set()
    with open(fname, encoding="utf-8") as handle:
        for y, line in enumerate(handle.read().strip().split("\n")):
            for x, char in enumerate(line):
                if char == "#":
                    state.add((y, x))

    return state


def neighbours(yx: Tuple[int, int], maximum: int) -> Set[Tuple[int, int]]:
    return {
        (yx[0] + dy, yx[1] + dx)
        for dy in range(-1, 2)
        for dx in range(-1, 2)
        if (
            not (dy == 0 and dx == 0)
            and 0 <= yx[0] + dy < maximum
            and 0 <= yx[1] + dx < maximum
        )
    }


def iterate(state: State, maximum: int, corners_on: bool) -> State:
    next_state: State = (
        set([(0, 0), (0, maximum - 1), (maximum - 1, 0), (maximum - 1, maximum - 1)])
        if corners_on
        else set()
    )
    # DRY to get corners
    state = state.union(next_state)

    for coords in state:
        for next_coords in neighbours(coords, maximum).union(set([coords])):
            around = sum(
                [
                    1 if neigh in state else 0
                    for neigh in neighbours(next_coords, maximum)
                ]
            )
            if next_coords in state:
                if 2 <= around <= 3:
                    next_state.add(next_coords)
            elif around == 3:
                next_state.add(next_coords)
    return next_state


def game(state: State, rounds: int, maximum: int, corners_on: bool = False):
    for _ in range(rounds):
        # printer(state, maximum=maximum)
        # print("-------------------")
        state = iterate(state, maximum=maximum, corners_on=corners_on)
    return len(state)


def printer(state: State, maximum: int):
    min_y = 0
    max_y = maximum - 1
    min_x = 0
    max_x = maximum - 1

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (y, x) in state:
                print("#", end="")
            else:
                print(".", end="")
        print()


day = os.path.basename(__file__).split(".")[0].split("_")[1]
base = os.path.join(os.path.dirname(__file__), "input", f"{day}")
print(game(parse(f"{base}.test"), rounds=5, maximum=6))
print(game(parse(f"{base}.input"), rounds=100, maximum=100))

print(game(parse(f"{base}.test"), rounds=5, maximum=6, corners_on=True))
print(game(parse(f"{base}.input"), rounds=100, maximum=100, corners_on=True))
