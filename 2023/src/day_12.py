"""Day 12: Hot Springs

Dynamic programming time!

After a lot of head scratching, it turns out that this is not at all
complicated. We need to find all allowed permutations of gear blocks
and part 2 just ensures that we can't try all possible
combinations.

We can do this recursively: For the first constraint, find all
possible first gear block positions and then recurse on the rest of
the line and the rest of the constraints. Caching the output of the
recursion provides a massive speedup.

"""

from functools import cache
from dataclasses import dataclass
import os
from textwrap import dedent

from typing import List, Sequence


@dataclass
class Data:
    line: str
    constraints: Sequence[int]


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> List[Data]:
    d: List[Data] = []
    for line in data.split("\n"):
        head, tail = line.split()
        d.append(Data(head, tuple(int(x) for x in tail.split(","))))
    return d


@cache
def permutations(line: str, constraints: Sequence[int]) -> int:
    if not constraints:
        if "#" not in line:
            return 1
        return 0

    constraint, rest = constraints[0], constraints[1:]
    variants = 0
    for pos, char in enumerate(line):
        if char in "#?":
            if (
                # There are no gears before the new gear block
                "#" not in line[:pos]
                # We can place the gear block without running out of space
                and pos + constraint <= len(line)
                # We can place the entire gear block
                and all(line[p] in "#?" for p in range(pos, pos + constraint))
                # There are no gears after the new gear block
                and (pos + constraint == len(line) or line[pos + constraint] in ".?")
            ):
                variants += permutations(line[pos + constraint + 1 :], rest)

    return variants


def part1(src: str) -> int:
    data = parse(src)
    count = 0
    for d in data:
        count += permutations(d.line, d.constraints)
    return count


def part2(src: str) -> int:
    data = parse(src)
    count = 0
    for i, d in enumerate(data):
        expanded = Data(
            "?".join([d.line for _ in range(5)]),
            tuple(n for _ in range(5) for n in d.constraints),
        )
        count += permutations(expanded.line, expanded.constraints)
    return count


def test_part1():
    data = dedent(
        """
        ???.### 1,1,3
        .??..??...?##. 1,1,3
        ?#?#?#?#?#?#?#? 1,3,1,6
        ????.#...#... 4,1,1
        ????.######..#####. 1,6,5
        ?###???????? 3,2,1
        """
    ).strip()

    assert part1(data) == 21


def test_part2():
    data = dedent(
        """
        ???.### 1,1,3
        .??..??...?##. 1,1,3
        ?#?#?#?#?#?#?#? 1,3,1,6
        ????.#...#... 4,1,1
        ????.######..#####. 1,6,5
        ?###???????? 3,2,1
        """
    ).strip()

    assert part2(data) == 525152


if __name__ == "__main__":
    print(part1(read_data()))
    print(part2(read_data()))
