"""Day 25: Code Chronicle

And that's a wrap!
"""

import os
from dataclasses import dataclass
from textwrap import dedent


@dataclass(frozen=True)
class World:
    keys: set[tuple[int, ...]]
    locks: set[tuple[int, ...]]


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> World:
    locks: set[tuple[int, ...]] = set()
    keys: set[tuple[int, ...]] = set()

    for block in data.split("\n\n"):
        lines = block.split("\n")
        target = keys if "." in lines[0] else locks
        pins = [sum(1 for y in range(len(lines)) if lines[y][x] == "#") - 1 for x in range(len(lines[0]))]
        target.add(tuple(pins))

    return World(keys=keys, locks=locks)


def part1(world: World) -> int:
    return len([lock for key in world.keys for lock in world.locks if all(a + b <= 5 for a, b in zip(lock, key))])


def test_part1() -> None:
    data = dedent("""
    #####
    .####
    .####
    .####
    .#.#.
    .#...
    .....
    
    #####
    ##.##
    .#.##
    ...##
    ...#.
    ...#.
    .....
    
    .....
    #....
    #....
    #...#
    #.#.#
    #.###
    #####
    
    .....
    .....
    #.#..
    ###..
    ###.#
    ###.#
    #####
    
    .....
    .....
    .....
    #....
    #.#..
    #.#.#
    #####
    """).strip()
    assert part1(parse(data)) == 3


if __name__ == "__main__":
    print(part1(parse(read_data())))
