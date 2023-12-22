"""Day 22: Sand SLabs

Pretty straight forward tetris today. Part 1 and 2 are essentially the
same, requiring us to produce a dependency graph and counting what
happens when we change it.

The part 2 implementation is a bit messy, since it iterates through
the data structure way more than it probably needs to, but it works
and I didn't bother to figure out if there would be issues with a
proper graph representation.
"""

import copy
import os
from textwrap import dedent
from typing import Set, Tuple, TypeAlias

Coord: TypeAlias = Tuple[int, int, int]


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str):
    blocks: Set[Tuple[Coord, Coord]] = set()

    for line in data.split("\n"):
        a, b = line.split("~")
        blocks.add((tuple(map(int, a.split(","))), tuple(map(int, b.split(",")))))

    return blocks


def settle(blocks: Set[Tuple[Coord, Coord]]):
    filled = {}
    resting = {}
    # From lowest to highest
    for i, block in enumerate(sorted(blocks, key=lambda b: b[0][2]), start=1):
        resting[i] = set()
        # Assume first block is lowest
        z = block[0][2]
        blocked = False
        dz = 0
        while not blocked and z - dz > 1:
            for x, y in [
                (x, y)
                for x in range(block[0][0], block[1][0] + 1)
                for y in range(block[0][1], block[1][1] + 1)
            ]:
                if filled.get((x, y, z - (dz + 1)), 0):
                    blocked = True
                    resting[i].add(filled[(x, y, z - (dz + 1))])

            if not blocked:
                dz += 1

        filled.update(
            {
                (x, y, z - dz): i
                for x in range(block[0][0], block[1][0] + 1)
                for y in range(block[0][1], block[1][1] + 1)
                for z in range(block[0][2], block[1][2] + 1)
            }
        )
    return resting


def part1(data: str) -> int:
    blocks = parse(data)
    resting = settle(blocks)

    count = 0
    for i in resting:
        for v in resting.values():
            if v == set([i]):
                break
        else:
            count += 1
    return count


def part2(data: str) -> int:
    blocks = parse(data)
    resting = settle(blocks)

    count = 0
    for i in resting:
        local_resting = copy.deepcopy(resting)
        local_resting.pop(i)
        to_remove = set([i])
        while to_remove:
            r = to_remove.pop()
            for block, rest_set in local_resting.items():
                if r in rest_set:
                    rest_set.discard(r)
                    if len(rest_set) == 0:
                        to_remove.add(block)
                        count += 1
    return count


def test_part1():
    data = dedent(
        """
        1,0,1~1,2,1
        0,0,2~2,0,2
        0,2,3~2,2,3
        0,0,4~0,2,4
        2,0,5~2,2,5
        0,1,6~2,1,6
        1,1,8~1,1,9
        """
    ).strip()

    assert part1(data) == 5


def test_part2():
    data = dedent(
        """
        1,0,1~1,2,1
        0,0,2~2,0,2
        0,2,3~2,2,3
        0,0,4~0,2,4
        2,0,5~2,2,5
        0,1,6~2,1,6
        1,1,8~1,1,9
        """
    ).strip()

    assert part2(data) == 7


if __name__ == "__main__":
    print(part1(read_data()))
    print(part2(read_data()))
