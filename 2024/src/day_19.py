"""Day 19: Linen Layout

Dynamic programming again (aka functools.cache time). For a given
offset in the pattern, for each towel we can append and still match
the pattern, we can count how many variations we can get for the
remaining pattern. If the count is zero, we have part 1, for part 2 we
sum all counts.
"""

import functools
import os
from dataclasses import dataclass
from textwrap import dedent


@dataclass(frozen=True)
class World:
    towels: tuple[str, ...]
    patterns: tuple[str, ...]


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> World:
    towels, patterns = data.split("\n\n")
    return World(towels=tuple(towels.split(", ")), patterns=tuple(patterns.split("\n")))


@functools.cache
def valid_permutations(pattern: str, offset: int, world: World) -> int:
    if offset == len(pattern):
        return 1

    count = 0
    for towel in world.towels:
        if pattern[offset : offset + len(towel)] == towel:
            count += valid_permutations(pattern, offset + len(towel), world)
    return count


def part1(world: World) -> int:
    return len([pattern for pattern in world.patterns if valid_permutations(pattern, 0, world) > 0])


def part2(world: World) -> int:
    return sum([valid_permutations(pattern, 0, world) for pattern in world.patterns])


def test_part1() -> None:
    data = dedent("""
    r, wr, b, g, bwu, rb, gb, br
    
    brwrr
    bggr
    gbbr
    rrbgbr
    ubwu
    bwurrg
    brgr
    bbrgwb
    """).strip()
    assert part1(parse(data)) == 6


def test_part2() -> None:
    data = dedent("""
    r, wr, b, g, bwu, rb, gb, br
    
    brwrr
    bggr
    gbbr
    rrbgbr
    ubwu
    bwurrg
    brgr
    bbrgwb
    """).strip()
    assert part2(parse(data)) == 16


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
