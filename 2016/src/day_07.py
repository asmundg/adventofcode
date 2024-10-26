"""Day 07: Internet Protocol Version 7

That got slightly complicated. There is probably some fancy
regex-based way of doing the ABBAs, but I didn't bother figuring
out. Splitting the inner and outer chunks by regex works nicely
though.
"""

import os
import re

from collections.abc import Generator, Sequence


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> list[str]:
    return data.split("\n")


def has_abba(msg: str) -> bool:
    for start in range(len(msg) - 3):
        if (
            msg[start] == msg[start + 3]
            and msg[start] != msg[start + 1]
            and msg[start + 1] == msg[start + 2]
        ):
            return True
    return False


def find_abas(msg: str) -> Generator[str, None, None]:
    for start in range(len(msg) - 2):
        if msg[start] == msg[start + 2] and msg[start] != msg[start + 1]:
            yield msg[start : start + 2]


def has_bab(msg: str, aba: str) -> bool:
    for start in range(len(msg) - 2):
        if msg[start] == aba[1] == msg[start + 2] and msg[start + 1] == aba[0]:
            return True
    return False


def parse_packet(msg: str) -> tuple[list[str], list[str]]:
    outer = re.sub("\\[[^\\]]*\\]", ",", msg).split(",")
    inner = re.findall("\\[([^\\]]*)\\]", msg)
    return (outer, inner)


def tls_valid(msg: str) -> bool:
    outer, inner = parse_packet(msg)
    return any(has_abba(m) for m in outer) and not any(has_abba(i) for i in inner)


def ssl_valid(msg: str) -> bool:
    outer, inner = parse_packet(msg)
    for o in outer:
        for aba in find_abas(o):
            if any(has_bab(i, aba) for i in inner):
                return True
    return False


def part1(msgs: Sequence[str]) -> int:
    return len([m for m in msgs if tls_valid(m)])


def part2(msgs: Sequence[str]) -> int:
    return len([m for m in msgs if ssl_valid(m)])


def test_part1() -> None:
    assert tls_valid("abba[mnop]qrst")
    assert not tls_valid("abcd[bddb]xyyx")
    assert not tls_valid("aaaa[qwer]tyui")
    assert tls_valid("ioxxoj[asdfgh]zxcvbn")


def test_part2() -> None:
    assert ssl_valid("aba[bab]xyz")
    assert not ssl_valid("xyx[xyx]xyx")
    assert ssl_valid("aaa[kek]eke")
    assert ssl_valid("zazbz[bzb]cdb")


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
