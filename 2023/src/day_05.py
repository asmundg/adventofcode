"""Day 5: If You Give A Seed A Fertilizer

Part 2 uses vectors to avoid having to iterate over all the numbers
that behave in exactly the same way. Modelling the vector splitting
logic turned out to be a surprisingly hard mental exercise.

"""

from dataclasses import dataclass
import os
import re

from typing import Dict, List, Optional, Tuple, TypeAlias


@dataclass
class Map:
    map_from: Tuple[int, int]
    map_to: Tuple[int, int]


@dataclass
class Transform:
    output: str
    maps: List[Map]


Data: TypeAlias = Tuple[List[int], Dict[str, Transform]]


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> Data:
    transforms = {}

    parts = data.split("\n\n")
    seeds = [int(n) for n in parts[0].split(":")[1].strip().split()]
    for part in parts[1:]:
        lines = part.split("\n")
        head = lines[0]
        m = re.match(r"(\w+)-to-(\w+) map:", head)
        assert m, head

        category_src, category_dst = m.groups()
        transform = Transform(category_dst, [])
        for line in lines[1:]:
            dst, src, length = map(int, line.split())
            transform.maps.append(Map((src, src + length - 1), (dst, dst + length - 1)))

        transform.maps.sort(key=lambda m: m.map_from[0])
        transforms[category_src] = transform

    return seeds, transforms


def solve(data: Data) -> int:
    current_values, transforms = data

    state = "seed"
    while state != "location":
        current_map = transforms[state].maps
        next_values: List[int] = []
        for value in current_values:
            for m in current_map:
                if m.map_from[0] <= value <= m.map_from[1]:
                    next_values.append(m.map_to[0] + value - m.map_from[0])
                    break
            else:
                next_values.append(value)

        current_values = next_values
        state = transforms[state].output

    return min(current_values)


def intersection(a: Tuple[int, int], b: Tuple[int, int]) -> Optional[Tuple[int, int]]:
    if a[0] < b[1] and a[1] > b[0]:
        return max(a[0], b[0]), min(a[1], b[1])

    return None


def solve2(data: Data) -> int:
    vals, transforms = data
    current_ranges = [(a, a + b - 1) for a, b in zip(vals[0::2], vals[1::2])]

    state = "seed"
    while state != "location":
        next_ranges: List[Tuple[int, int]] = []
        for r in current_ranges:
            # The pointer keeps track of the start of the range we're
            # handling
            ptr = r[0]
            for m in transforms[state].maps:
                # Skip if we're before the remap range
                if r[1] < m.map_from[0]:
                    next_ranges.append((ptr, r[1]))
                    break

                i = intersection((ptr, r[1]), m.map_from)
                # Skip if we're after the remap range
                if i is None:
                    continue

                # Add range before intersection
                if ptr < i[0]:
                    next_ranges.append((ptr, i[0] - 1))

                # Remap intersection
                next_ranges.append(
                    (
                        m.map_to[0] + i[0] - m.map_from[0],
                        m.map_to[0] + i[1] - m.map_from[0],
                    )
                )
                ptr = i[1] + 1
                if ptr > r[1]:
                    break
            else:
                # Add remaining range
                next_ranges.append((ptr, r[1]))

        current_ranges = next_ranges
        state = transforms[state].output

    for r in current_ranges:
        assert r[0] < r[1], r
    return min(r[0] for r in current_ranges)


TEST = """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4\
"""


def test_part1():
    data = TEST
    assert solve(parse(data)) == 35


def test_part2():
    data = TEST
    assert solve2(parse(data)) == 46


if __name__ == "__main__":
    print(solve(parse(read_data())))
    print(solve2(parse(read_data())))
