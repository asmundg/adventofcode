"""Day 12: 
"""

import json
import os


def parse(fname: str) -> str:
    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def value(j, ignore_val=None) -> int:
    if isinstance(j, list):
        return sum([value(el, ignore_val) for el in j])
    elif isinstance(j, dict):
        if ignore_val in j.values():
            return 0
        else:
            return sum([value(el, ignore_val) for el in j.values()])
    elif isinstance(j, int):
        return j
    else:
        return 0


def solve(s: str, ignore_val=None) -> int:
    return value(json.loads(s), ignore_val)


day = os.path.basename(__file__).split(".")[0].split("_")[1]
base = os.path.join(os.path.dirname(__file__), "input", f"{day}")
print(solve(parse(f"{base}.input")))
print(solve(parse(f"{base}.input"), ignore_val="red"))
