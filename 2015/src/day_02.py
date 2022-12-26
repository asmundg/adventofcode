"""Day 2: 
"""

import os
from typing import List, Tuple


def parse(fname: str) -> List[Tuple[int, int, int]]:
    boxes: List[Tuple[int, int, int]] = []
    with open(fname, encoding="utf-8") as handle:
        for box in handle.read().strip().split("\n"):
            nums = tuple([int(num) for num in box.split("x")])
            assert len(nums) == 3
            boxes.append(nums)
    return boxes


def solve(fname: str) -> int:
    boxes = parse(fname)
    total = 0
    for box in boxes:
        l, w, h = box
        total += (2 * l * w) + (2 * w * h) + (2 * h * l) + min(l * w, w * h, h * l)
    return total


def solve2(fname: str) -> int:
    boxes = parse(fname)
    total = 0
    for box in boxes:
        l, w, h = box
        total += min(2 * l + 2 * w, 2 * w + 2 * h, 2 * h + 2 * l) + w * h * l
    return total


day = os.path.basename(__file__).split(".")[0].split("_")[1]
base = os.path.join(os.path.dirname(__file__), "input", f"{day}")
print(solve(f"{base}.test"))
print(solve(f"{base}.input"))

print(solve2(f"{base}.test"))
print(solve2(f"{base}.input"))
