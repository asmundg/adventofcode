"""Day 11: Plutonian Pebbles

Dynamic programming time! The data structure quickly scales out of
control if we try to track all the stones that exist for each
step. Since stones don't affect each other, and we only care about the
number of stones, we can instead figure out how many stones a given
stone will produce after N steps.

The calculation of the number of stones for each (stone, steps
remaining) caches nicely, meaning we'll mostly know immediately how
long of a sequence a given stone expands to, without having to do any
additional calculation.
"""

import os
from functools import cache
from textwrap import dedent


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> list[int]:
    return [int(num) for num in data.split()]


@cache
def process(num: int, steps: int) -> int:
    if steps == 0:
        return 1

    if num == 0:
        return process(1, steps - 1)
    elif len(str(num)) % 2 == 0:
        a = process(int(str(num)[: len(str(num)) // 2]), steps - 1)
        b = process(int(str(num)[len(str(num)) // 2 :]), steps - 1)
        return a + b
    else:
        return process(num * 2024, steps - 1)


def solve(data: list[int], iterations: int) -> int:
    return sum(process(num, iterations) for num in data)


def test_solve() -> None:
    data = dedent("""
    125 17
    """).strip()
    assert solve(parse(data), 25) == 55312


if __name__ == "__main__":
    print(solve(parse(read_data()), 25))
    print(solve(parse(read_data()), 75))
