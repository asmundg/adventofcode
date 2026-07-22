"""Day 01:"""

import os


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def part1(data: str) -> int:
    return sum(int(n) for n in data.split("\n"))


def part2(data: str) -> int:
    freq = 0
    seen = set([freq])
    changes = [int(n) for n in data.split("\n")]
    while True:
        for change in changes:
            freq += change
            if freq in seen:
                return freq
            else:
                seen.add(freq)


if __name__ == "__main__":
    print(part1(read_data()))
    print(part2(read_data()))
