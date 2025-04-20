"""Day 22: Grid Computing

It turns out this one is actually hand solvable (at least for part
2). The crucial insight from part 1 is that there is a single empty
space. This means the task is maneuvering the empty space around until
we have shifted the top-right data into the top-left position.

Since all grid positions are swappable, except for the set of 'wall'
locations, we first move the empty to the top-next-to-right corner,
avoiding the walls, and then start shifting the data leftwards. We
could program this and count the steps, but we can also just print out
the grid and count the moves by hand!

"""

import os
import re
from dataclasses import dataclass


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


@dataclass(frozen=True)
class Node:
    used: int
    avail: int


def parse(data: str) -> dict[tuple[int, int], Node]:
    nodes: dict[tuple[int, int], Node] = {}
    lines = data.split("\n")
    for line in lines[2:]:
        if m := re.match(r"/dev/grid/node-x(\d+)-y(\d+)\s+\d+T\s+(\d+)T\s+(\d+)T.*", line):
            x = int(m.group(1))
            y = int(m.group(2))
            used = int(m.group(3))
            avail = int(m.group(4))
            nodes[(y, x)] = Node(used=used, avail=avail)
        else:
            raise Exception("Oops", line)

    return nodes


def part1(nodes: dict[tuple[int, int], Node]) -> int:
    count = 0
    for a in nodes.values():
        for b in nodes.values():
            if a == b or a.used == 0:
                continue
            if a.used <= b.avail:
                count += 1
    return count


def part2(nodes: dict[tuple[int, int], Node]) -> None:
    debug(nodes)


def debug(nodes: dict[tuple[int, int], Node]) -> None:
    max_x = sorted([k[1] for k in nodes.keys()])[-1]
    max_y = sorted([k[0] for k in nodes.keys()])[-1]

    for y in range(max_y + 1):
        for x in range(max_x + 1):
            print("_" if nodes[(y, x)].used == 0 else "#" if nodes[(y, x)].used > 100 else ".", end="")
        print()


if __name__ == "__main__":
    print(part1(parse(read_data())))
    part2(parse(read_data()))
