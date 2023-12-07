"""Day 7: Camel Cards

Both parts can be done by sorting with a custom comparator. It took me
a little while to realize that the good old cmp keyword from python2
is gone in python3. cmp_to_key is a really clever replacement though.

"""

from functools import cmp_to_key
import os
from textwrap import dedent

from typing import List, Tuple


CARDS = ("A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2")
ALT_CARDS = ("A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J")
RANKS = ((5,), (1, 4), (2, 3), (1, 1, 3), (1, 2, 2), (1, 1, 1, 2), (1, 1, 1, 1, 1))


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> List[Tuple[str, int]]:
    return [(line.split()[0], int(line.split()[1])) for line in data.split("\n")]


def score(a: str) -> int:
    counts = {card: a.count(card) for card in CARDS}
    return RANKS.index(tuple(v for v in sorted(counts.values()) if v != 0))


def cmp(a: Tuple[str, int], b: Tuple[str, int]):
    diff = score(b[0]) - score(a[0])
    if diff != 0:
        return diff

    for i in range(5):
        diff = CARDS.index(b[0][i]) - CARDS.index(a[0][i])
        if diff != 0:
            return diff

    assert False, (a, b)


def part1(data: str) -> int:
    hands = parse(data)
    sorted_hands = sorted(hands, key=cmp_to_key(cmp))
    return sum((i + 1) * hand[1] for i, hand in enumerate(sorted_hands))


def score2(a: str) -> int:
    counts = {card: a.count(card) for card in CARDS if a.count(card)}
    if "J" in counts.keys():
        js = counts.pop("J")
        if js == 5:
            return RANKS.index((5,))
        # We don't need to be clever about the jokers, since
        # converting them to the card type with the highest occurence
        # always yields the strongest hand
        counts[sorted(counts.keys(), key=lambda k: counts[k])[-1]] += js
    return RANKS.index(tuple(v for v in sorted(counts.values()) if v != 0))


def cmp2(a: Tuple[str, int], b: Tuple[str, int]):
    diff = score2(b[0]) - score2(a[0])
    if diff != 0:
        return diff

    for i in range(5):
        diff = ALT_CARDS.index(b[0][i]) - ALT_CARDS.index(a[0][i])
        if diff != 0:
            return diff

    assert False, (a, b)


def part2(data: str) -> int:
    hands = parse(data)
    sorted_hands = sorted(hands, key=cmp_to_key(cmp2))
    return sum((i + 1) * hand[1] for i, hand in enumerate(sorted_hands))


def test_part1():
    data = dedent(
        """
        32T3K 765
        T55J5 684
        KK677 28
        KTJJT 220
        QQQJA 483
        """
    ).strip()

    assert part1(data) == 6440


def test_part2():
    data = dedent(
        """
        32T3K 765
        T55J5 684
        KK677 28
        KTJJT 220
        QQQJA 483
        """
    ).strip()

    assert part2(data) == 5905


if __name__ == "__main__":
    print(part1(read_data()))
    print(part2(read_data()))
