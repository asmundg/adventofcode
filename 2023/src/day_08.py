"""Day 8: Haunted Wasteland

The parts compose neatly today. Part 1 is a simple traversal of the
data structure according to the given instructions. Part 2 does the
same, but now we get multiple paths of different lengths and we need
to determine the number of steps until they all terminate at the same
time.

Maths to the rescue! As opposed to day 6, I actually recognize this
one and didn't bother to test for brute forceability. The earliest
point at which cycles of different length wrap at the same time is the
least common multiple.

Note that it doesn't _have_ to be this easy, since it requires that
the cycle length matches the path length, so that we always start a
new cycle at instruction 0.

"""

import itertools
import math
import os
import re
from textwrap import dedent

from typing import Dict, Tuple


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> Tuple[str, Dict[str, Tuple[str, str]]]:
    head, tail = data.split("\n\n")
    paths = {}
    for line in tail.split("\n"):
        m = re.match(r"^(\w+) = \((\w+), (\w+)\)$", line)
        assert m, line
        node, l, r = m.groups()
        paths[node] = (l, r)
    return head, paths


def part1(data: str, node="AAA", stop="ZZZ") -> int:
    instructions, nodes = parse(data)

    walk = itertools.cycle(instructions)
    count = 0
    while not node.endswith(stop):
        count += 1
        node = nodes[node][0 if next(walk) == "L" else 1]
    return count


def part2(data: str) -> int:
    _, nodes = parse(data)
    starts = [key for key in nodes if key.endswith("A")]
    cycles = []

    for node in starts:
        cycles.append(part1(data, node, "Z"))

    return math.lcm(*cycles)


def test_part1():
    data = dedent(
        """
        RL

        AAA = (BBB, CCC)
        BBB = (DDD, EEE)
        CCC = (ZZZ, GGG)
        DDD = (DDD, DDD)
        EEE = (EEE, EEE)
        GGG = (GGG, GGG)
        ZZZ = (ZZZ, ZZZ)
        """
    ).strip()

    assert part1(data) == 2

    data = dedent(
        """
        LLR

        AAA = (BBB, BBB)
        BBB = (AAA, ZZZ)
        ZZZ = (ZZZ, ZZZ)
        """
    ).strip()

    assert part1(data) == 6


def test_part2():
    data = dedent(
        """
        LR

        11A = (11B, XXX)
        11B = (XXX, 11Z)
        11Z = (11B, XXX)
        22A = (22B, XXX)
        22B = (22C, 22C)
        22C = (22Z, 22Z)
        22Z = (22B, 22B)
        XXX = (XXX, XXX)
        """
    ).strip()

    assert part2(data) == 6


if __name__ == "__main__":
    print(part1(read_data()))
    print(part2(read_data()))
