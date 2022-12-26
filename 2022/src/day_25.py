"""Day 25: Full of Hot Air

Base conversion. Python might have some built-in mechanism, but just
implementing it felt faster.
"""

import os
from typing import List


def parse(fname: str) -> List[str]:
    with open(fname, encoding="utf-8") as handle:
        return [line.strip() for line in handle.read().strip().split("\n")]


def tobase10(base5: str) -> int:
    total = 0
    for i, char in enumerate(reversed(base5)):
        if char == "=":
            total -= 2 * 5**i
        elif char == "-":
            total -= 5**i
        else:
            total += int(char) * (5**i)
    return total


def tobase5(num: int) -> str:
    s = ""
    while num > 0:
        r = num % 5
        if r == 4:
            s += "-"
            num += 5
        elif r == 3:
            s += "="
            num += 5
        else:
            s += str(r)
        num = num // 5
    return s[::-1]


def solve(fname: str) -> str:
    return tobase5(sum([tobase10(line) for line in parse(fname)]))


day = os.path.basename(__file__).split(".")[0].split("_")[1]
base = os.path.join(os.path.dirname(__file__), "input", f"{day}")

print(solve(f"{base}.test"))
print(solve(f"{base}.input"))
