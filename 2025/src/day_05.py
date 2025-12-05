"""Day 05: Cafeteria

Ok, so our data structure will be ranges and we'll check for overlaps
by x >= start && x <= end.

This data structure lets us solve part2 as well, since it lets us
merge the ranges. This is necessary to avoid counting valid ids more
than once and because we need to count the range lengths instead of
trying to compute the individual valid ids, as that set would get
really large(?).
"""

import os
from dataclasses import dataclass
from textwrap import dedent


@dataclass
class Problem:
    ranges: set[tuple[int, int]]
    nums: set[int]


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> Problem:
    problem = Problem(set(), set())
    ranges, vals = data.split("\n\n")
    for line in ranges.split("\n"):
        start, stop = line.split("-")
        problem.ranges.add((int(start), int(stop)))
    for line in vals.split("\n"):
        problem.nums.add(int(line))

    r = 0
    while True:
        r += 1
        if r > 10:
            raise Exception("oops")
        next_ranges: set[tuple[int, int]] = set()
        merged = 0
        for range in problem.ranges:
            for r2 in problem.ranges:
                if range == r2:
                    continue
                if range[0] <= r2[1] and range[1] >= r2[0]:
                    next_ranges.add((min(range[0], r2[0]), max(range[1], r2[1])))
                    merged += 1
                    break
            else:
                next_ranges.add(range)

        problem.ranges = next_ranges
        if not merged:
            return problem


def part1(problem: Problem) -> int:
    count = 0
    for val in problem.nums:
        for r in problem.ranges:
            if val >= r[0] and val <= r[1]:
                count += 1
                break

    return count


def part2(problem: Problem) -> int:
    return sum(r[1] - r[0] + 1 for r in problem.ranges)


def test_part1() -> None:
    data = dedent(
        """
        3-5
        10-14
        16-20
        12-18

        1
        5
        8
        11
        17
        32
        """
    ).strip()
    assert part1(parse(data)) == 3


def test_part2() -> None:
    data = dedent(
        """
        3-5
        10-14
        16-20
        12-18

        1
        5
        8
        11
        17
        32
        """
    ).strip()
    assert part2(parse(data)) == 14


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
