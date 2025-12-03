"""Day 03: Lobby

We need to find the highest number in the subset of the bank starting
from the previous number we found (or the start) and ending at the
spot where we have enough batteries left to complete the sequence. Off
by one errors aplenty when slicing.
"""

import os
from textwrap import dedent


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> list[str]:
    banks: list[str] = []
    for line in data.split("\n"):
        banks.append(line)
    return banks


def solve(banks: list[str], n: int) -> int:
    total = 0
    for bank in banks:
        remaining = bank
        found = [sorted(bank[: -n + 1], reverse=True)[0]]
        for i in range(1, n):
            remaining = remaining[remaining.index(found[-1]) + 1 :]
            tail = (-(n - i) if i < (n - 1) else len(remaining)) + 1
            found.append(sorted(remaining[:tail], reverse=True)[0])
        total += int("".join(found))

    return total


def test_part1() -> None:
    data = dedent(
        """
        987654321111111
        811111111111119
        234234234234278
        818181911112111
        """
    ).strip()
    assert solve(parse(data), 2) == 357


def test_part2() -> None:
    data = dedent(
        """
        987654321111111
        811111111111119
        234234234234278
        818181911112111
        """
    ).strip()
    assert solve(parse(data), 12) == 3121910778619


if __name__ == "__main__":
    print(solve(parse(read_data()), 2))
    print(solve(parse(read_data()), 12))
