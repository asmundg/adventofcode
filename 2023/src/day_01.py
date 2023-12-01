"""Day 1: Trebuchet?!

I started by replacing tokens in the string, until I realized that the
words can overlap (eightwo). Just finding the token index and saving
the lo/high indexes was more robust.

"""

import os
from textwrap import dedent

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


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str, parse_words: bool = False) -> List[str]:
    lines: List[str] = []
    for line in data.split("\n"):
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


def test_part1():
    data = dedent(
        """\
        1abc2
        pqr3stu8vwx
        a1b2c3d4e5f
        treb7uchet"""
    )

    assert solve(parse(data)) == 142


def test_part2():
    data = dedent(
        """\
        two1nine
        eightwothree
        abcone2threexyz
        xtwone3four
        4nineeightseven2
        zoneight234
        7pqrstsixteen"""
    )
    assert solve(parse(data, parse_words=True)) == 281


if __name__ == "__main__":
    print(solve(parse(read_data())))
    print(solve(parse(read_data(), parse_words=True)))
