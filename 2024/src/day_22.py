"""Day 22: Monkey Market

A bit slow, but within my limits of tolerance. If the number sequences
are properly pseudo-random, there shouldn't be any patterns we can
exploit, so we need to manually check for matching sequences.

That said, we can precompute all prices for all valid sequences for
each monkey. Then we can collect the sum of all prices for each known
sequence in reasonable time.
"""

import os
from textwrap import dedent
from typing import TypeAlias


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> list[int]:
    return [int(line) for line in data.split("\n")]


def evolve(number: int, n: int) -> list[int]:
    evolutions = [number]
    for _ in range(n):
        number = ((number * 64) ^ number) % 16777216
        number = ((number // 32) ^ number) % 16777216
        number = ((number * 2048) ^ number) % 16777216
        evolutions.append(number)
    return evolutions


def part1(secrets: list[int]) -> int:
    return sum(evolve(secret, 2000)[-1] for secret in secrets)


def part2(secrets: list[int]) -> int:
    price_diffs: list[tuple[list[int], list[int]]] = []
    for secret in secrets:
        evolved = evolve(secret, 2000)
        prices = [int(str(e)[-1]) for e in evolved]
        diffs = [b - a for a, b in zip(prices, prices[1:])]
        price_diffs.append((prices[1:], diffs))

    Seq: TypeAlias = tuple[int, int, int, int]
    seq_to_prices: list[dict[Seq, int]] = []

    for prices, diffs in price_diffs:
        local_prices: dict[Seq, int] = dict()
        for i, seq in enumerate(zip(diffs, diffs[1:], diffs[2:], diffs[3:])):
            if seq not in local_prices:
                local_prices[seq] = prices[i + 3]
        seq_to_prices.append(local_prices)

    best = 0
    seqs = set([k for sp in seq_to_prices for k in sp.keys()])
    for seq in seqs:
        total = sum(prices.get(seq, 0) for prices in seq_to_prices)
        best = max(best, total)
    return best


def test_part1() -> None:
    data = dedent("""
    1
    10
    100
    2024
    """).strip()
    assert part1(parse(data)) == 37327623


def test_part2() -> None:
    data = dedent("""
    1
    2
    3
    2024
    """).strip()
    assert part2(parse(data)) == 23


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
