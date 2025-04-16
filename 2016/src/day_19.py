"""Day 19: An Elephant Named Joseph

This is interesting.

Part one is trivially solvable with a standard list. We remove half of
the elves for each full pass arund the ring and since there are only
~3 million elves, we don't need that many total iterations. Since we
always just look at the next index in the list and only leave dead
elves behind us, we can compress the list after a full circle to keep
the next elf lookup constant. We could have used a linked list here
instead, but this turned out to be unneccesary since we only
reallocate the list once we've completed a circle.

The same principle of removing half the elves for each full round
holds for part 2, but now we're removing the other half of the circle
instead of the next elf. This means we need a skip counter to track
the virtual circle while indexing into the uncompressed list. When we
get to the dead half, we can compress, which means we also need to
reset the index correctly.

"""

import math
import os
from dataclasses import dataclass


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


@dataclass
class Elf:
    pos: int
    gifts: int = 1


def part1(num_elves: int) -> int:
    elves = [Elf(pos=1 + i) for i in range(num_elves)]

    while len(elves) > 1:
        for i in range(len(elves)):
            current_elf, next_elf = elves[i], elves[(i + 1) % len(elves)]
            if current_elf.gifts == 0:
                continue

            current_elf.gifts += next_elf.gifts
            next_elf.gifts = 0

        elves = [elf for elf in elves if elf.gifts > 0]
    return elves[0].pos


def part2(num_elves: int) -> int:
    elves = [Elf(pos=1 + i) for i in range(num_elves)]

    skip = 0
    i = 0
    while len(elves) > 1:
        current_elf, next_elf = elves[i], elves[(i + math.floor(num_elves / 2) + skip) % len(elves)]
        # Compress
        if current_elf.gifts == 0:
            while current_elf.gifts == 0:
                i = (i + 1) % len(elves)
                current_elf = elves[i]
            elves = [elf for elf in elves if elf.gifts > 0]
            for i in range(len(elves)):
                if elves[i].pos == current_elf.pos:
                    break
            skip = 0
            continue

        current_elf.gifts += next_elf.gifts
        next_elf.gifts = 0
        num_elves -= 1
        skip += 1

        i = i + 1 if i < (len(elves) - 1) else 0

    return elves[0].pos


def test_part1() -> None:
    assert part1(5) == 3


def test_part2() -> None:
    assert part2(5) == 2


if __name__ == "__main__":
    print(part1(int(read_data())))
    print(part2(int(read_data())))
