"""Day 9: 
"""

import itertools
import os
from typing import Dict, Tuple, TypeAlias

Dists: TypeAlias = Dict[Tuple[str, str], int]


def parse(fname: str) -> Dists:
    dists = {}
    with open(fname, encoding="utf-8") as handle:
        for line in handle.read().strip().split("\n"):
            pair, dist = line.split(" = ")
            a, b = pair.split(" to ")
            dists[(a, b)] = int(dist)
            dists[(b, a)] = int(dist)
    return dists


def solve(dists: Dict[Tuple[str, str], int], shortest=True) -> int:
    locations = set([a for a, b in dists.keys()])
    best = 999999 if shortest else 0
    for trail in itertools.permutations(locations):
        total = sum([dists[(a, b)] for a, b in zip(trail, trail[1:])])
        if total < best if shortest else total > best:
            best = total
    return best


day = os.path.basename(__file__).split(".")[0].split("_")[1]
base = os.path.join(os.path.dirname(__file__), "input", f"{day}")
print(solve(parse(f"{base}.test")))
print(solve(parse(f"{base}.input")))

print(solve(parse(f"{base}.test"), shortest=False))
print(solve(parse(f"{base}.input"), shortest=False))
