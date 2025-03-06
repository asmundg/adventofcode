"""Day 15: Timing is Everything

Here we need to find the first point at which all cycles in a sequence
of cycles match up in a particular way. This can probably be done
neatly by calculating when the cycles align. But we can also just
brute force, since the LCM, even in part 2, is in the low millions. So
the answer is well before that point.

There's also a sieve-like approach we can take, where successive
matching discs give the minimum interval of start times we can
try. But again, not super tempting when brute force works just fine.

"""

import os
from dataclasses import dataclass
from itertools import count
from textwrap import dedent


@dataclass
class Disc:
    positions: int
    start: int


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> list[Disc]:
    discs: list[Disc] = []
    for line in data.split("\n"):
        elements = line.split()
        discs.append(Disc(positions=int(elements[3]), start=int(elements[11][:-1])))
    return discs


def part1(discs: list[int]) -> int:
    c = count(start=1)
    while True:
        i = next(c)
        for n, disc in enumerate(discs):
            if (disc.start + i + n) % disc.positions != 0:
                break
        else:
            return i - 1


def part2(discs: list[Disc]) -> int:
    return part1(discs + [Disc(positions=11, start=0)])


def test_part1() -> None:
    data = dedent(
        """
        Disc #1 has 5 positions; at time=0, it is at position 4.
        Disc #2 has 2 positions; at time=0, it is at position 1.
        """
    ).strip()
    assert part1(parse(data)) == 5


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
