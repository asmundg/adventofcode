"""Day 09: Stream Processing

This is a pretty basic recursive descent parser.

"""

import os

import pytest


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse_group(pos: int, depth: int, stream: str) -> tuple[int, int, int]:
    score = depth
    garbage_chars = 0
    while stream[pos] != "}":
        if stream[pos] == "{":
            pos, sub_score, sub_garbage = parse_group(pos + 1, depth + 1, stream)
            score += sub_score
            garbage_chars += sub_garbage
        elif stream[pos] == "!":
            pos += 2
        elif stream[pos] == "<":
            pos, sub_garbage = parse_garbage(pos + 1, stream)
            garbage_chars += sub_garbage
        else:
            pos += 1

    return (pos + 1, score, garbage_chars)


def parse_garbage(pos: int, stream: str) -> tuple[int, int]:
    garbage_chars = 0
    while stream[pos] != ">":
        if stream[pos] == "!":
            pos += 2
        else:
            pos += 1
            garbage_chars += 1
    return pos + 1, garbage_chars


def part1(stream: str) -> int:
    assert stream[0] == "{"
    return parse_group(1, 1, stream)[1]


def part2(stream: str) -> int:
    assert stream[0] == "{"
    return parse_group(1, 1, stream)[2]


@pytest.mark.parametrize(
    "data,expected",
    [
        ("{}", 1),
        ("{{{}}}", 6),
        ("{{},{}}", 5),
        ("{{{},{},{{}}}}", 16),
        ("{<a>,<a>,<a>,<a>}", 1),
        ("{{<ab>},{<ab>},{<ab>},{<ab>}}", 9),
        ("{{<!!>},{<!!>},{<!!>},{<!!>}}", 9),
        ("{{<a!>},{<a!>},{<ab>}}", 3),
    ],
)
def test_part1(data, expected) -> None:
    assert part1(data) == expected


@pytest.mark.parametrize(
    "data,expected",
    [
        ("{<>}", 0),
        ("{<random characters>}", 17),
        ("{<<<<>}", 3),
        ("{<{!>}>}", 2),
        ("{<!!>}", 0),
        ("{<!!!>>}", 0),
        ('{<{o"i!a,<{i<a>}', 10),
    ],
)
def test_part2(data, expected) -> None:
    assert part2(data) == expected


if __name__ == "__main__":
    print(part1(read_data()))
    print(part2(read_data()))
