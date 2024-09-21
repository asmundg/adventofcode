"""Day 24: It Hangs in the Balance.

This feels like it wants to be a knapsack problem, but it turns out
that we only need to find a valid first group. There might be input
sets where this doesn't work.

We iterate through all permutations of the inputs, in increasing set
sizes, until we find at least one that sums to the target group
size. Then we just sort by the product to find the cheapest grouping
of that number of packages.

"""

import functools
import itertools
import operator
import os
from typing import List
from textwrap import dedent


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> List[int]:
    return [int(line) for line in data.split("\n")]


def find_smallest_group(packages: List[int], groups=3):
    group_size = sum(packages) / groups

    for num in itertools.count(1):
        candidates = [
            p for p in itertools.combinations(packages, num) if sum(p) == group_size
        ]
        if candidates:
            candidates = sorted(
                candidates, key=lambda c: functools.reduce(operator.mul, c, 1)
            )
            return functools.reduce(operator.mul, candidates[0], 1)


def test_part1():
    data = dedent(
        """
        1
        2
        3
        4
        5
        7
        8
        9
        10
        11
        """
    ).strip()

    assert find_smallest_group(parse(data)) == 99


def test_part2():
    data = dedent(
        """
        1
        2
        3
        4
        5
        7
        8
        9
        10
        11
        """
    ).strip()

    assert find_smallest_group(parse(data), 4) == 44


if __name__ == "__main__":
    print(find_smallest_group(parse(read_data())))
    print(find_smallest_group(parse(read_data()), 4))
