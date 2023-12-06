"""Day 6: Wait For It

I think this is just finding the integral of a linear function, but
instead of doing clever and fast maths, we can also just compute each
value by hand, since even part 2 doesn't contain that many positions
to iterate over.

"""

from dataclasses import dataclass
import os
from textwrap import dedent

from typing import List


@dataclass
class Round:
    time: int
    distance: int


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> List[Round]:
    time, distance = data.split("\n")
    return [
        Round(time=int(z[0]), distance=int(z[1]))
        for z in zip(time.split()[1:], distance.split()[1:])
    ]


def parse2(data: str) -> List[Round]:
    time, distance = data.split("\n")
    return [
        Round(
            time=int(time.split(maxsplit=1)[1].replace(" ", "")),
            distance=int(distance.split(maxsplit=1)[1].replace(" ", "")),
        )
    ]


def part1(data: str) -> int:
    rounds = parse(data)
    return solve(rounds)


def part2(data: str) -> int:
    rounds = parse2(data)
    return solve(rounds)


def solve(rounds: List[Round]) -> int:
    total = 1
    for r in rounds:
        distances = {}
        for n in range(r.time):
            distance = n * (r.time - n)
            if distance not in distances:
                distances[distance] = 0
            distances[distance] += 1

        total *= sum(val for key, val in distances.items() if key > r.distance)
    return total


def test_part1():
    data = dedent(
        """
        Time:      7  15   30
        Distance:  9  40  200
        """
    ).strip()

    assert part1(data) == 288


def test_part2():
    data = dedent(
        """
        Time:      7  15   30
        Distance:  9  40  200
        """
    ).strip()

    assert part2(data) == 71503


if __name__ == "__main__":
    print(part1(read_data()))
    print(part2(read_data()))
