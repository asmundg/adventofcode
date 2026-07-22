"""Day 02:"""

import itertools
import os


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def part1(data: str) -> int:
    twos = 0
    threes = 0
    for n in data.split("\n"):
        counts = [len(list(g)) for _, g in itertools.groupby(sorted(n))]
        if 2 in counts:
            twos += 1
        if 3 in counts:
            threes += 1

    return twos * threes


def part2(data: str) -> str:
    s = sorted(data.split("\n"))
    for a, b in zip(s, s[1:]):
        mismatches = 0
        out = ""
        for i in range(len(a)):
            if a[i] == b[i]:
                out += a[i]
            else:
                mismatches += 1
        if mismatches == 1:
            return out

    raise Exception("No solution")


if __name__ == "__main__":
    print(part1(read_data()))
    print(part2(read_data()))
