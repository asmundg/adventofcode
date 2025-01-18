"""Day 14: One-Time Pad

Batteries included-time. Python provides some great functionality for
iterating, grouping, hashing and caching.

We're a bit slow, but I'm not sure we can trivially speed up the
hashing.

"""

import functools
import hashlib
import itertools


@functools.cache
def find_hash(salt: str, i: int, rounds: int) -> str:
    h = salt + str(i)
    for _ in range(rounds):
        h = hashlib.md5(h.encode("ascii")).hexdigest()
    return h


def part1(salt: str, rounds: int = 1) -> int:
    index = itertools.count()
    pad_idx = itertools.count(1)
    while True:
        i = next(index)
        candidate = find_hash(salt, i, rounds)
        for char, group in itertools.groupby(candidate):
            if len(list(group)) >= 3:
                for next_i in range(i + 1, i + 1001):
                    sub_candidate = find_hash(salt, next_i, rounds)
                    if char * 5 in sub_candidate:
                        if next(pad_idx) == 64:
                            return i
                        break
                break


def part2(salt: str) -> int:
    return part1(salt, rounds=2017)


def test_part1() -> None:
    assert part1("abc") == 22728


def test_part2() -> None:
    assert part2("abc") == 22551


if __name__ == "__main__":
    print(part1("cuanljph"))
    print(part2("cuanljph"))
