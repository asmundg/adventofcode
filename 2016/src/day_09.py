"""Day 09: Explosives in Cyberspace

This uses a very lightweight recursive descent parser to handle the
nested expressions."""

import os
from collections.abc import Sequence
from typing import Tuple


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> list[str]:
    return data.split("\n")


def decompress(msg: str, v2: bool = False) -> int:
    return parse_sequence(msg, 0, len(msg), v2)[0]


def parse_sequence(msg: str, pos: int, stop: int, v2: bool) -> Tuple[int, int]:
    length = 0
    while pos < stop:
        if msg[pos] == "(":
            sub_length, pos = parse_marker(msg, pos, v2=v2)
            length += sub_length
        else:
            length += 1
            pos += 1
    return length, pos


def parse_marker(msg: str, pos: int, v2: bool) -> Tuple[int, int]:
    assert msg[pos] == "("
    pos += 1

    seq_len, pos = parse_num(msg, pos)

    assert msg[pos] == "x"
    pos += 1

    repeats, pos = parse_num(msg, pos)
    assert msg[pos] == ")"
    pos += 1

    if v2:
        return repeats * parse_sequence(msg, pos, pos + seq_len, v2=True)[
            0
        ], pos + seq_len
    else:
        return seq_len * repeats, pos + seq_len


def parse_num(msg: str, pos: int) -> Tuple[int, int]:
    acc = ""
    while msg[pos] in "1234567890":
        acc += msg[pos]
        pos += 1
    return int(acc), pos


def part1(messages: Sequence[str]) -> int:
    return sum(decompress(message) for message in messages)


def part2(messages: Sequence[str]) -> int:
    return sum(decompress(message, v2=True) for message in messages)


def test_part1() -> None:
    assert decompress("ADVENT") == 6
    assert decompress("A(1x5)BC") == 7
    assert decompress("(3x3)XYZ") == 9
    assert decompress("A(2x2)BCD(2x2)EFG") == 11
    assert decompress("(6x1)(1x3)A") == 6
    assert decompress("X(8x2)(3x3)ABCY") == 18


def test_part2() -> None:
    assert decompress("(3x3)XYZ", v2=True) == 9
    assert decompress("X(8x2)(3x3)ABCY", v2=True) == 20
    assert decompress("(27x12)(20x12)(13x14)(7x10)(1x12)A", v2=True) == 241920
    assert (
        decompress("(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN", v2=True)
        == 445
    )


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
