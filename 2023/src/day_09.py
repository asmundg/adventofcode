"""Day 9: Mirage Maintenance

Basic list manipulation. We don't really need to keep all of the
numbers in the middle, since we only care about either the head or the
tail. But part 2 doesn't blow up even if we store everything, and
having the complete data structure makes it easier to verify that
everything's fine.

"""

import os
from textwrap import dedent

from typing import List


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> List[List[int]]:
    seqs = []
    for line in data.split("\n"):
        seqs.append([int(i) for i in line.split()])
    return seqs


def history(seq: List[int]) -> List[List[int]]:
    hs = [seq]
    while [i for i in hs[-1] if i != 0]:
        h = []
        for a, b in zip(hs[-1], hs[-1][1:]):
            h.append(b - a)
        hs.append(h)
    return hs


def part1(data: str) -> int:
    seqs = parse(data)

    total = 0
    for seq in seqs:
        hs = history(seq)
        hs[-1].append(0)
        for i in reversed(range(len(hs) - 1)):
            hs[i].append(hs[i][-1] + hs[i + 1][-1])

        total += hs[0][-1]
    return total


def part2(data: str) -> int:
    seqs = parse(data)

    total = 0
    for seq in seqs:
        hs = history(seq)
        hs[-1].insert(0, 0)
        for i in reversed(range(len(hs) - 1)):
            hs[i].insert(0, hs[i][0] - hs[i + 1][0])

        total += hs[0][0]
    return total


def test_part1():
    data = dedent(
        """
        0 3 6 9 12 15
        1 3 6 10 15 21
        10 13 16 21 30 45
        """
    ).strip()

    assert part1(data) == 114


def test_part2():
    data = dedent(
        """
        0 3 6 9 12 15
        1 3 6 10 15 21
        10 13 16 21 30 45
        """
    ).strip()

    assert part2(data) == 2


if __name__ == "__main__":
    print(part1(read_data()))
    print(part2(read_data()))
