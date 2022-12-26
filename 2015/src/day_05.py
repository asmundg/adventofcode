"""Day 5: 
"""

import os
import re
from typing import List


def parse(fname: str) -> List[str]:
    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip().split("\n")


def check(s: str) -> bool:
    a = re.search(r"[aeiou].*[aeiou].*[aeiou]", s)
    b = re.search(r"([a-z])\1", s)
    c = re.search(r"ab|cd|pq|xy", s)
    return a is not None and b is not None and c is None


def check2(s: str) -> bool:
    a = re.search(r"([a-z][a-z]).*\1", s)
    b = re.search(r"([a-z]).\1", s)
    return a is not None and b is not None


def solve(s: List[str]) -> int:
    return len(list(filter(check, s)))


def solve2(s: List[str]) -> int:
    return len(list(filter(check2, s)))


assert check("ugknbfddgicrmopn") is True
assert check("aaa") is True
assert check("jchzalrnumimnmhp") is False
assert check("haegwjzuvuyypxyu") is False
assert check("dvszwmarrgswjxmb") is False

day = os.path.basename(__file__).split(".")[0].split("_")[1]
base = os.path.join(os.path.dirname(__file__), "input", f"{day}")
print(solve(parse(f"{base}.input")))


assert check2("qjhvhtzxzqqjkmpb") is True
assert check2("xxyxx") is True
assert check2("uurcxstgmygtbstg") is False
assert check2("ieodomkazucvgmuy") is False
print(solve2(parse(f"{base}.input")))
