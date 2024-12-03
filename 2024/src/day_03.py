"""Day 3: Mull It Over

Regex time!

It took me a little time to remember how re.findall works in terms of
identifying groups for part 2, but the solution extends nicely to look
for 'more stuff' that we can just ignore when in part 1 mode.
"""

import os
import re
from textwrap import dedent


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str, use_p: bool = False) -> list[tuple[int, int]]:
    muls: list[tuple[int, int]] = []
    ignoring: bool = False
    for line in data.split("\n"):
        for a, b, do, dont in re.findall(r"mul\(([0-9]+),([0-9]+)\)|(do\(\))|(don't\(\))", line):
            if do:
                ignoring = False
                continue
            if dont:
                ignoring = True
                continue

            if use_p and ignoring:
                continue

            muls.append((int(a), int(b)))
    return muls


def part1(muls: list[tuple[int, int]]) -> int:
    return sum(a * b for a, b in muls)


def test_part1() -> None:
    data = dedent("""
    xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
    """).strip()
    assert part1(parse(data)) == 161


def test_part2() -> None:
    data = dedent("""
    xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
    """).strip()
    assert part1(parse(data, use_p=True)) == 48


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part1(parse(read_data(), use_p=True)))
