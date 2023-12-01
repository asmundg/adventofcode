"""Day 1: Trebuchet?!

I started by replacing tokens in the string, until I realized that the
words can overlap (eightwo). Just finding the token index and saving
the lo/high indexes was more robust.

"""

import os

from typing import List

NUMS = [c for c in "0123456789"]
WORDS = [
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]


def parse(fname: str, parse_words: bool = False) -> List[str]:
    lines: List[str] = []
    with open(fname, encoding="utf-8") as handle:
        for line in handle.read().strip().split("\n"):
            tokens = NUMS if not parse_words else NUMS + WORDS
            first = ("", len(line))
            last = ("", -1)
            for token in tokens:
                idx = line.find(token)
                if -1 < idx < first[1]:
                    first = (token if token in NUMS else str(WORDS.index(token)), idx)
                idx = line.rfind(token)
                if idx > last[1]:
                    last = (token if token in NUMS else str(WORDS.index(token)), idx)
            lines.append(first[0] + last[0])
    return lines


def solve(lines: List[str]):
    return sum([int(line[0] + line[-1]) for line in lines])


if __name__ == "__main__":
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    base = os.path.join(os.path.dirname(__file__), "input", f"{day}")
    print(solve(parse(f"{base}.test")))
    print(solve(parse(f"{base}.input")))

    print(solve(parse(f"{base}.test2", parse_words=True)))
    print(solve(parse(f"{base}.input", parse_words=True)))
