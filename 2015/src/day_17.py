"""Day 17: No Such Thing as Too Much.

We can recurse down the list of containers to produce all
permutations, pruning paths where we get too much volume. If we use
the constructed set of containers as our data structure, part2 is just
a matter of counting the set of shortest lists.
"""

import os

from typing import List


def parse(fname: str) -> List[int]:
    with open(fname, encoding="utf-8") as handle:
        return [int(line) for line in handle.read().strip().split("\n")]


def solve(containers: List[int], goal: int, path: List[int]) -> List[List[int]]:
    paths = []
    for n in range(len(containers)):
        if sum(path) + containers[n] == goal:
            paths.append(path + [containers[n]])
        elif sum(path) + containers[n] < goal:
            paths.extend(solve(containers[n + 1 :], goal, path + [containers[n]]))
    return paths


def solve2(paths: List[List[int]]) -> List[int]:
    min_containers = min(len(p) for p in paths)
    return [p for p in paths if len(p) == min_containers]


day = os.path.basename(__file__).split(".")[0].split("_")[1]
base = os.path.join(os.path.dirname(__file__), "input", f"{day}")

print(solve(parse(f"{base}.test"), 25, []))
print(len(solve(parse(f"{base}.input"), 150, [])))

print(solve2(solve(parse(f"{base}.test"), 25, [])))
print(len(solve2(solve(parse(f"{base}.input"), 150, []))))
