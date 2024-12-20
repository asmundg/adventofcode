"""Day 20: Race Condition

It's off by one-day! Getting this right turned out to be way harder
than it should have. Part 1 and 2 are essentially the same, where we
first find the cost of each position along the track and then find the
cost of all positions reachable by shortcut for each position.
"""

import os
from dataclasses import dataclass
from textwrap import dedent

from common import cartesian
from common.cartesian import Coord


@dataclass(frozen=True)
class World:
    walls: set[Coord]
    start: Coord
    end: Coord


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> World:
    walls: set[Coord] = set()
    for y, line in enumerate(data.split("\n")):
        for x, char in enumerate(line):
            if char == "#":
                walls.add((y, x))
            elif char == "S":
                start = (y, x)
            elif char == "E":
                end = (y, x)
    return World(walls, start, end)


def find_cheats(world: World, cheat_length: int) -> dict[int | float, int]:
    current_cost = 0
    cost: dict[Coord, int] = {world.start: current_cost}
    node = world.start

    while node != world.end:
        for neighbor in cartesian.neighbors(node):
            if neighbor in world.walls or neighbor in cost:
                continue
            node = neighbor
            current_cost += 1
            cost[node] = current_cost
            break

    saved_count: dict[int | float, int] = {}
    for cheat_start, start_cost in cost.items():
        for y in range(cheat_start[0] - cheat_length, cheat_start[0] + cheat_length + 1):
            for x in range(
                cheat_start[1] - cheat_length + abs(y - cheat_start[0]),
                cheat_start[1] + cheat_length - abs(y - cheat_start[0]) + 1,
            ):
                if (y, x) not in cost or cost[(y, x)] <= start_cost:
                    continue

                saved = cost[(y, x)] - start_cost - abs(cheat_start[0] - y) - abs(cheat_start[1] - x)

                if saved > 0:
                    saved_count.setdefault(saved, 0)
                    saved_count[saved] += 1

    return saved_count


def part1(world: World) -> int:
    saves = find_cheats(world, cheat_length=2)
    return sum(v for k, v in saves.items() if k >= 100)


def part2(world: World) -> int:
    saves = find_cheats(world, cheat_length=20)
    return sum(v for k, v in saves.items() if k >= 100)


def test_cheats_part1() -> None:
    data = dedent("""
    ###############
    #...#...#.....#
    #.#.#.#.#.###.#
    #S#...#.#.#...#
    #######.#.#.###
    #######.#.#...#
    #######.#.###.#
    ###..E#...#...#
    ###.#######.###
    #...###...#...#
    #.#####.#.###.#
    #.#...#.#.#...#
    #.#.#.#.#.#.###
    #...#...#...###
    ###############
    """).strip()
    assert find_cheats(parse(data), cheat_length=2) == {
        2: 14,
        4: 14,
        6: 2,
        8: 4,
        10: 2,
        12: 3,
        20: 1,
        36: 1,
        38: 1,
        40: 1,
        64: 1,
    }


def test_cheats_part2() -> None:
    data = dedent("""
    ###############
    #...#...#.....#
    #.#.#.#.#.###.#
    #S#...#.#.#...#
    #######.#.#.###
    #######.#.#...#
    #######.#.###.#
    ###..E#...#...#
    ###.#######.###
    #...###...#...#
    #.#####.#.###.#
    #.#...#.#.#...#
    #.#.#.#.#.#.###
    #...#...#...###
    ###############
    """).strip()
    assert {k: v for k, v in find_cheats(parse(data), cheat_length=20).items() if k >= 50} == {
        50: 32,
        52: 31,
        54: 29,
        56: 39,
        58: 25,
        60: 23,
        62: 20,
        64: 19,
        66: 12,
        68: 14,
        70: 12,
        72: 22,
        74: 4,
        76: 3,
    }


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
