"""Day 16: Aunt Sue.

This is a basic filter where we remove all lines that contain a
mismatch.
"""

import os

from typing import Dict


GT = {"cats", "trees"}
LT = {"pomeranians", "goldfish"}


def solve(fname: str, target: Dict[str, int]) -> int:
    with open(fname, encoding="utf-8") as handle:
        for i, line in enumerate(handle.read().strip().split("\n"), start=1):
            sue, rest = line.split(": ", 1)
            for thing in rest.split(", "):
                name, count = thing.split(": ")
                if target[name] != int(count):
                    break
            else:
                return i

    raise Exception("oops")


def solve2(fname: str, target: Dict[str, int]) -> int:
    with open(fname, encoding="utf-8") as handle:
        for i, line in enumerate(handle.read().strip().split("\n"), start=1):
            sue, rest = line.split(": ", 1)
            for thing in rest.split(", "):
                name, count = thing.split(": ")
                if name in GT:
                    if int(count) <= target[name]:
                        break
                elif name in LT:
                    if int(count) >= target[name]:
                        break
                elif target[name] != int(count):
                    break
            else:
                return i

    raise Exception("oops")


day = os.path.basename(__file__).split(".")[0].split("_")[1]
base = os.path.join(os.path.dirname(__file__), "input", f"{day}")
print(
    solve(
        f"{base}.input",
        {
            "children": 3,
            "cats": 7,
            "samoyeds": 2,
            "pomeranians": 3,
            "akitas": 0,
            "vizslas": 0,
            "goldfish": 5,
            "trees": 3,
            "cars": 2,
            "perfumes": 1,
        },
    )
)
print(
    solve2(
        f"{base}.input",
        {
            "children": 3,
            "cats": 7,
            "samoyeds": 2,
            "pomeranians": 3,
            "akitas": 0,
            "vizslas": 0,
            "goldfish": 5,
            "trees": 3,
            "cars": 2,
            "perfumes": 1,
        },
    )
)
