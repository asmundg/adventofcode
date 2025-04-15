"""Day 18: Like a Rogue

This is a simple business logic task, where we just apply the rules
iteratively. Part 2 scales up the number of iterations, but not beyond
what can be feasibly calculated (albeit a bit slowly).

"""

import os
from textwrap import dedent


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


IS_TRAP = set(["^^.", ".^^", "^..", "..^"])


def part1(traps: str, iters: int) -> int:
    prev = traps
    sum_safe = traps.count(".")
    for x in range(iters - 1):
        line = ""
        for i in range(len(prev)):
            left = prev[i - 1] if i > 0 else "."
            center = prev[i]
            right = prev[i + 1] if i < len(prev) - 1 else "."
            line += "^" if left + center + right in IS_TRAP else "."
        sum_safe += line.count(".")
        prev = line
    return sum_safe


def test_part1() -> None:
    data = dedent(
        """
        .^^.^.^^^^
        """
    ).strip()
    assert part1(data, 10) == 38


if __name__ == "__main__":
    print(part1(read_data(), 40))
    print(part1(read_data(), 400000))
