"""Day 7: 
"""

import os
import re
from typing import Callable, Dict, List


def parse(fname: str) -> List[str]:
    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip().split("\n")


def convert(a: str, wires: Dict[str, Callable[[], int]]) -> int:
    if re.match("^[0-9]+", a):
        return int(a)
    else:
        res = wires[a]()
        # Cache resolved value
        wires[a] = lambda: res
        return res


def solve(s: List[str], override: Dict[str, int]) -> int:
    wires: Dict[str, Callable[[], int]] = {}
    for cmd in s:
        if m := re.match("^(\w+) -> (\w+)", cmd):
            a, b = m.groups()
            wires[b] = lambda a=a: convert(a, wires)
        elif m := re.match("^(\w+) AND (\w+) -> (\w+)", cmd):
            a, b, c = m.groups()
            wires[c] = lambda a=a, b=b: convert(a, wires) & convert(b, wires)
        elif m := re.match("^(\w+) OR (\w+) -> (\w+)", cmd):
            a, b, c = m.groups()
            wires[c] = lambda a=a, b=b: convert(a, wires) | convert(b, wires)
        elif m := re.match("^(\w+) LSHIFT (\w+) -> (\w+)", cmd):
            a, b, c = m.groups()
            wires[c] = lambda a=a, b=b: convert(a, wires) << convert(b, wires)
        elif m := re.match("^(\w+) RSHIFT (\w+) -> (\w+)", cmd):
            a, b, c = m.groups()
            wires[c] = lambda a=a, b=b: convert(a, wires) >> convert(b, wires)
        elif m := re.match("^NOT (\w+) -> (\w+)", cmd):
            a, b = m.groups()
            wires[b] = lambda a=a: ~convert(a, wires)

    for key, val in override.items():
        wires[key] = lambda val=val: val
    return convert("a", wires)


day = os.path.basename(__file__).split(".")[0].split("_")[1]
base = os.path.join(os.path.dirname(__file__), "input", f"{day}")
print(solve(parse(f"{base}.input"), {}))
print(solve(parse(f"{base}.input"), {"b": solve(parse(f"{base}.input"), {})}))
