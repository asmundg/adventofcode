"""Day 2: Red-Nosed Reports

This requires encoding a bit of business logic for checking that the
rules hold for a report (safe_p). Typically not the easiest thing to
get right early in the morning, when reading comprehension hasn't
really activated yet.

The two rules can be implemented using sort and zip. For part 2, we
test all permutations of a report and count it if we find one
acceptable variant.

"""

import os
from textwrap import dedent


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> list[list[int]]:
    reports: list[list[int]] = []
    for line in data.split("\n"):
        reports.append([int(n) for n in line.split()])
    return reports


def safe_p(report: list[int]) -> bool:
    if report != sorted(report) and report != sorted(report, reverse=True):
        return False

    for a, b in zip(report[:-1], report[1:]):
        if abs(a - b) > 3 or a == b:
            return False

    return True


def part1(reports: list[list[int]]) -> int:
    return len([report for report in reports if safe_p(report)])


def part2(reports: list[list[int]]) -> int:
    safe = 0
    for report in reports:
        for remove in range(-1, len(report)):
            test = [n for i, n in enumerate(report) if i != remove]
            if safe_p(test):
                safe += 1
                break
    return safe


def test_part1() -> None:
    data = dedent("""
    7 6 4 2 1
    1 2 7 8 9
    9 7 6 2 1
    1 3 2 4 5
    8 6 4 4 1
    1 3 6 7 9
    """).strip()
    assert part1(parse(data)) == 2


def test_part2() -> None:
    data = dedent("""
    7 6 4 2 1
    1 2 7 8 9
    9 7 6 2 1
    1 3 2 4 5
    8 6 4 4 1
    1 3 6 7 9
    """).strip()
    assert part2(parse(data)) == 4


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
