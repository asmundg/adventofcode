"""Day 06: Memory Reallocation

Relatively mechanical shuffling of data. We get to be a bit clever
with max finding the max enumerated value (which also happens to break
ties the right way). We also use the state directly as a dict
key. Which doubles as both a cycle detector (state was seen) and cycle
length counter (when did we last see this state).

"""

import os
from textwrap import dedent


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> list[int]:
    return [int(n) for n in data.split()]


def part1_and_2(state: list[int]) -> tuple[int, int]:
    seen: dict[tuple[int, ...], int] = {}
    iterations = 0
    while tuple(state) not in seen:
        seen[tuple(state)] = iterations
        iterations += 1
        i, n = max(enumerate(state), key=lambda pair: pair[1])
        state[i] = 0
        for offset in range(n):
            state[(i + 1 + offset) % len(state)] += 1

    return iterations, iterations - seen[tuple(state)]


def test_part1() -> None:
    data = dedent("""
    0 2 7 0
    """).strip()
    assert part1_and_2(parse(data))[0] == 5


if __name__ == "__main__":
    print(part1_and_2(parse(read_data())))
