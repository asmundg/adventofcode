"""Day 06: Signals and Noise

Oh hey, we already did the frequency thing on day 4.
"""

import os
from textwrap import dedent
from collections.abc import Sequence


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> list[str]:
    return data.split("\n")


def find_char(msg: Sequence[str], highest_freq: bool = True) -> str:
    chars: dict[str, int] = {}
    for char in msg:
        if char not in chars:
            chars[char] = 0
        chars[char] += 1
    return sorted(chars.keys(), key=lambda c: chars[c], reverse=highest_freq)[0]


def part1(msgs: Sequence[str]) -> str:
    res = ""
    for n in range(len(msgs[0])):
        res += find_char([m[n] for m in msgs])
    return res


def part2(msgs: Sequence[str]) -> str:
    res = ""
    for n in range(len(msgs[0])):
        res += find_char([m[n] for m in msgs], highest_freq=False)
    return res


def test_part1() -> None:
    data = dedent(
        """
        eedadn
        drvtee
        eandsr
        raavrd
        atevrs
        tsrnev
        sdttsa
        rasrtv
        nssdts
        ntnada
        svetve
        tesnvt
        vntsnd
        vrdear
        dvrsen
        enarar
        """
    ).strip()

    assert part1(parse(data)) == "easter"


def test_part2() -> None:
    data = dedent(
        """
        eedadn
        drvtee
        eandsr
        raavrd
        atevrs
        tsrnev
        sdttsa
        rasrtv
        nssdts
        ntnada
        svetve
        tesnvt
        vntsnd
        vrdear
        dvrsen
        enarar
        """
    ).strip()

    assert part2(parse(data)) == "advent"


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
