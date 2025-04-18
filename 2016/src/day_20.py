"""Day 20: Firewall Rules

We can model this as a set of ranges. If we sort them by start, we
can, for each pair of ranges, determine if they overlap or if there is
a gap. Part 1 requires finding the first gap, part 2 requires finding
all gaps.

We could generalize the gap finding, but the code is small enough that
I don't really care.

"""

import os
from textwrap import dedent


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    for line in data.split("\n"):
        a, b = [int(n) for n in line.split("-")]
        ranges.append((a, b))
    return ranges


def part1(ranges: list[tuple[int, int]]) -> int:
    ranges = sorted(ranges, key=lambda r: r[0])
    if ranges[0][0] > 0:
        return 0

    last = ranges[0][1]
    for a, b in ranges[1:]:
        if a <= last + 1:
            if b > last:
                last = b
        else:
            return last + 1


def part2(ranges: list[tuple[int, int]]) -> int:
    ranges = sorted(ranges, key=lambda r: r[0])
    valid = 0
    if ranges[0][0] > 0:
        valid = +ranges[0][0] - 1

    valid = 0
    last = ranges[0][1]
    for a, b in ranges[1:]:
        if a <= last + 1:
            if b > last:
                last = b
        else:
            valid += a - last - 1
            last = b

    valid += 4294967295 - last
    return valid


def test_part1() -> None:
    data = dedent(
        """
        5-8
        0-2
        4-7
        """
    ).strip()
    assert part1(parse(data)) == 3


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
