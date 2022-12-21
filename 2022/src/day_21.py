"""Day 21:
"""

from dataclasses import dataclass
import numpy as np
import os
import re
from typing import Dict, Optional, Tuple


@dataclass
class Node:
    name: str
    op: str
    operands: Tuple["Node", "Node"]
    cached: Optional[int] = None


def parse(fname: str, override: Dict[str, Tuple[int]] = None) -> Dict[str, Node]:
    override = override or {}
    lookup: Dict[str, Node] = {}
    deps: Dict[str, Tuple[str, str]] = {}

    with open(fname, encoding="utf-8") as handle:
        for line in [line.strip() for line in handle.read().strip().split("\n")]:
            m = re.match(r"(\w+): (\w+) ([\+\-\*/]) (\w+)", line)
            if m:
                lookup[m.group(1)] = Node(name=m.group(1), op=m.group(3), operands=None)
                deps[m.group(1)] = (m.group(2), m.group(4))
                continue
            m = re.match(r"(\w+): (\d+)", line)
            if m:
                lookup[m.group(1)] = Node(
                    name=m.group(1),
                    op=None,
                    operands=None,
                    cached=(
                        np.poly1d(
                            [
                                int(
                                    m.group(2),
                                )
                            ]
                        )
                        if m.group(1) not in override
                        else override[m.group(1)]
                    ),
                )
                continue
                continue
            raise Exception("Invalid definition", line)
    for node in lookup.values():
        if node.name in deps:
            node.operands = (lookup[deps[node.name][0]], lookup[deps[node.name][1]])
    return lookup


def calc(node: Node) -> Tuple[int]:
    val = node.cached
    if val is not None:
        return val

    a = calc(node.operands[0])
    b = calc(node.operands[1])

    if node.op == "+":
        val = a + b
    elif node.op == "-":
        val = a - b
    elif node.op == "*":
        val = a * b
    elif node.op == "/":
        val = (a / b)[0]

    node.cached = val
    return val


def solve(fname: str) -> int:
    nodes = parse(fname)
    return int(calc(nodes["root"])[0])


def solve2(fname: str) -> int:
    nodes = parse(fname, override={"humn": np.poly1d([1, 0])})
    a, b = calc(nodes["root"].operands[0]), calc(nodes["root"].operands[1])
    x, comp = (a, b) if len(a) > 0 else (b, a)
    return int(((comp - x[0]) / x[1])[0])


day = os.path.basename(__file__).split(".")[0].split("_")[1]
base = os.path.join(os.path.dirname(__file__), "input", f"{day}")

print(solve(f"{base}.test"))
print(solve(f"{base}.input"))

print(solve2(f"{base}.test"))
print(solve2(f"{base}.input"))
