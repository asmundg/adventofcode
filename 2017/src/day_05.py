"""Day 05: A Maze of Twisty Trampolines, All Alike

This seems fairly mechanical.

"""

import os
from textwrap import dedent


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> list[int]:
    ins: list[int] = []
    for line in data.split("\n"):
        ins.append(int(line))
    return ins


def part1(ins: list[int], modified: bool = False) -> int:
    ptr = 0
    steps = 0
    while 0 <= ptr < len(ins):
        prev = ptr
        ptr += ins[ptr]
        if modified:
            ins[prev] += -1 if ins[prev] >= 3 else 1
        else:
            ins[prev] += 1
        steps += 1

    return steps


def part2(ins: list[int]) -> int:
    return part1(ins, modified=True)


def test_part1() -> None:
    data = dedent("""
    0
    3
    0
    1
    -3
    """).strip()
    assert part1(parse(data)) == 5


def test_part2() -> None:
    data = dedent("""
    0
    3
    0
    1
    -3
    """).strip()
    assert part2(parse(data)) == 10


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
