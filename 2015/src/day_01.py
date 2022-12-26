"""Day 1: 
"""

import os


def parse(fname: str) -> str:
    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def solve(fname: str) -> int:
    data = parse(fname)
    return data.count("(") - data.count(")")


def solve2(fname: str) -> int:
    pos = 0
    data = parse(fname)
    for i, char in enumerate(data, start=1):
        pos += 1 if char == "(" else -1
        if pos == -1:
            return i


day = os.path.basename(__file__).split(".")[0].split("_")[1]
base = os.path.join(os.path.dirname(__file__), "input", f"{day}")
print(solve(f"{base}.input"))
print(solve2(f"{base}.input"))
