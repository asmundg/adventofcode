"""Day 8: 
"""

import os
from typing import List


def parse(fname: str) -> List[str]:
    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip().split("\n")


def solve(strs: List[str]) -> int:
    return sum(
        [len(s) - len(bytes(s, "utf-8").decode("unicode_escape")[1:-1]) for s in strs]
    )


def solve2(strs: List[str]) -> int:
    return sum(
        [
            len('"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"') - len(s)
            for s in strs
        ]
    )


day = os.path.basename(__file__).split(".")[0].split("_")[1]
base = os.path.join(os.path.dirname(__file__), "input", f"{day}")
print(solve(parse(f"{base}.test")))
print(solve(parse(f"{base}.input")))

print(solve2(parse(f"{base}.test")))
print(solve2(parse(f"{base}.input")))
