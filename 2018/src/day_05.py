"""Day 05:"""

import os


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def opposite_polarity(a: str, b: str) -> bool:
    return (a == a.lower() and b == a.upper()) or (a == a.upper() and b == a.lower())


def part1(polymer: str) -> int:
    idx = 0
    p = polymer
    while idx < len(p) - 1:
        if opposite_polarity(p[idx], p[idx + 1]):
            p = p[:idx] + p[idx + 2 :]
            idx = max(idx - 1, 0)
        else:
            idx += 1
    return len(p)


def part2(polymer: str) -> int:
    best = float("inf")
    for remove in "abcdefghijklmnopqrstuvwxyz":
        best = min(part1(polymer.replace(remove.lower(), "").replace(remove.upper(), "")), best)

    return int(best)


def test_part1():
    assert part1("dabAcCaCBAcCcaDA") == 10


def test_part2():
    assert part2("dabAcCaCBAcCcaDA") == 4


if __name__ == "__main__":
    print(part1(read_data()))
    print(part2(read_data()))
