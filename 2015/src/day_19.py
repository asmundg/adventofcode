"""Day 19: Medicine for Rudolph.

This one is a bit weird. Part 2 doesn't terminate, but still yields
(prints) the correct result. Since trying to construct the molecule
quickly blows up the search space, we instead find the number of steps
to go from the solution to the start point.

This gives a simple DFS, since all inverted replacements makes the
molecule smaller. It also allows pruning of subtrees when we've found
the same molecule through a cheaper path. This still runs for a loong
time, but we're apparently lucky in that we find the cheapest path
fairly early.

"""

import os

from typing import Dict, List, Set, TypeAlias
from textwrap import dedent

Mapping: TypeAlias = Dict[str, List[str]]


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str):
    mappings: Mapping = {}
    maps, molecule = data.split("\n\n")
    for line in maps.split("\n"):
        head, tail = line.split(" => ")
        if head not in mappings:
            mappings[head] = []
        mappings[head].append(tail)

    return mappings, molecule


def permutations(molecule: str, mapping: Mapping) -> Set[str]:
    res = set()
    for i, _ in enumerate(molecule):
        for src, dsts in mapping.items():
            if molecule[i:].startswith(src):
                for dst in dsts:
                    res.add(molecule[:i] + dst + molecule[i + len(src) :])
    return res


def part1(src: str) -> int:
    mappings, start = parse(src)
    return len(permutations(start, mappings))


def invert(mappings: Mapping) -> Mapping:
    res: Mapping = {}
    for k, v in mappings.items():
        for r in v:
            if r not in res:
                res[r] = []
            res[r].append(k)
    return res


def part2(src: str) -> int:
    mappings, target = parse(src)
    mappings = invert(mappings)

    best: Dict[str, int] = {}
    search = [(target, 0)]
    while search:
        molecule, steps = search.pop()

        if molecule == "e":
            print("Found", steps, "best", best[molecule])

        for permutation in permutations(molecule, mappings):
            # can get here more cheaply
            if best.get(permutation, steps + 2) <= steps + 1:
                continue

            best[permutation] = steps + 1
            search.append((permutation, steps + 1))

    return best["e"]


def test_part1():
    data = dedent(
        """
        H => HO
        H => OH
        O => HH

        HOHOHO
        """
    ).strip()

    assert part1(data) == 7


def test_part2():
    data = dedent(
        """
        e => H
        e => O
        H => HO
        H => OH
        O => HH

        HOHOHO
        """
    ).strip()

    assert part2(data) == 6


if __name__ == "__main__":
    print(part1(read_data()))
    print(part2(read_data()))
