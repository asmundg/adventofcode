"""Day 01: Secret Entrance

AoC meta-joke! Turns out part 1 solves part 2 directly if you _didn't_
optimize by just adding all of the steps at once. Of course we can
figure out if we passed 0 (step is larger than the remaining
increments before 0 in the current direction), but I didn't check if
the input contains rotations bigger than 100, which would have
complicated things.

"""

import os
from textwrap import dedent


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> list[int]:
    steps: list[int] = []
    for line in data.split("\n"):
        steps.append((-1 if line[0] == "L" else 1) * int(line[1:]))
    return steps


def part1(steps: list[int]) -> int:
    pos = 50
    count = 0
    for step in steps:
        pos = (pos + step) % 100
        if pos == 0:
            count += 1
    return count


def part2(steps: list[int]) -> int:
    pos = 50
    count = 0
    for step in steps:
        for _ in range(abs(step)):
            pos = (pos + (-1 if step < 0 else 1)) % 100
            if pos == 0:
                count += 1
    return count


def test_part1() -> None:
    data = dedent(
        """
        L68
        L30
        R48
        L5
        R60
        L55
        L1
        L99
        R14
        L82
        """
    ).strip()
    assert part1(parse(data)) == 3


def test_part2() -> None:
    data = dedent(
        """
        L68
        L30
        R48
        L5
        R60
        L55
        L1
        L99
        R14
        L82
        """
    ).strip()
    assert part2(parse(data)) == 6


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
