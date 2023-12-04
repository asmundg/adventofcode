"""Day 4: Scratchcards

Part 2 has a Fibonacci-type recursive structure, which might be
expensive to compute naively. So we just start from the end of the
sequence, counting how many copies one instance of the current card
contributes.

"""

from dataclasses import dataclass
import os
import re
from textwrap import dedent

from typing import Dict, List, Set


@dataclass
class Card:
    winning: Set[str]
    numbers: Set[str]


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> List[Card]:
    cards: List[Card] = []

    for line in data.split("\n"):
        m = re.match(r"Card(?: +)[0-9]+:((?: +[0-9]+)+) \|((?: +[0-9]+)+)", line)
        if not m:
            raise Exception("Oops", line)

        win, nums = m.groups()
        cards.append(
            Card(
                winning={w.strip() for w in win.strip().split()},
                numbers={n.strip() for n in nums.strip().split()},
            )
        )

    return cards


def solve(cards: List[Card]) -> int:
    overlaps = [len(card.winning.intersection(card.numbers)) for card in cards]
    return sum(2 ** (overlap - 1) for overlap in overlaps if overlap > 0)


def solve2(cards: List[Card]) -> int:
    copies: Dict[int, int] = {}
    for i, card in reversed(list(enumerate(cards))):
        overlap = len(card.winning.intersection(card.numbers))
        copies[i] = 1 + sum(copies[j] for j in range(i + 1, i + 1 + overlap))

    return sum(copies.values())


def test_part1():
    data = dedent(
        """\
        Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
        Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
        Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
        Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
        Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
        Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""
    )

    assert solve(parse(data)) == 13


def test_part2():
    data = dedent(
        """\
        Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
        Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
        Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
        Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
        Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
        Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""
    )

    assert solve2(parse(data)) == 30


if __name__ == "__main__":
    print(solve(parse(read_data())))
    print(solve2(parse(read_data())))
