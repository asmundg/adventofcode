"""Day 13: 
"""

import itertools
import os
import re

from typing import Dict, Tuple


def parse(fname: str) -> Dict[Tuple[str, str], int]:
    pairs: Dict[Tuple[str, str], int] = {}
    with open(fname, encoding="utf-8") as handle:
        for line in handle.read().strip().split("\n"):
            if m := re.match(
                r"(\w+) would (\w+) (\d+) happiness units by sitting next to (\w+).",
                line,
            ):
                a, mode, amount, b = m.groups()
                amount = int(amount) if mode == "gain" else -int(amount)
                pairs[(a, b)] = amount
    return pairs


def solve(pairs: Dict[Tuple[str, str], int]) -> int:
    best = 0
    for variant in itertools.permutations({k for key in pairs.keys() for k in key}):
        total = sum(
            [
                pairs[(a, b)] + pairs[(b, a)]
                for (a, b) in zip(variant, variant[1:] + variant[0:1])
            ]
        )
        if total > best:
            best = total
    return best


def solve2(pairs: Dict[Tuple[str, str], int]) -> int:
    for n in {k for key in pairs.keys() for k in key}:
        pairs[("You", n)] = 0
        pairs[(n, "You")] = 0
    return solve(pairs)


day = os.path.basename(__file__).split(".")[0].split("_")[1]
base = os.path.join(os.path.dirname(__file__), "input", f"{day}")
print(solve(parse(f"{base}.test")))
print(solve(parse(f"{base}.input")))
print(solve2(parse(f"{base}.input")))
