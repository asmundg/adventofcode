"""Day 16: Reindeer Maze

This is a variant A*. For part 1 we can use a standard DFS where we
abort if we've gotten to a node more cheaply than our current path. As
a bonus, we need to keep direction in mind, since turning has a cost.

The costly turns makes part 2 a bit fiddly, since we then also need to
account for which nodes we passed through on our way to the
goal. Worst case, the optimal paths pass through the same node in
different directions, at different costs.

Since we track the cheapest way to get to a node for each direction,
we can use this information to backtrack from the goal. We know the
cost to the goal, so the cost to any previous tile needs to be
cost(goal) - cost_of_move(node, direction). This lets us build another
search tree where we can strip all nodes we didn't come from. Walking
this tree gets us all nodes visited along all paths.
"""

import heapq
import os
from dataclasses import dataclass
from textwrap import dedent

from common import cartesian
from common.cartesian import Coord


@dataclass(frozen=True)
class World:
    start: Coord
    end: Coord
    walls: set[Coord]


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> World:
    walls: set[Coord] = set()
    start: Coord = (0, 0)
    end: Coord = (0, 0)

    for y, line in enumerate(data.split("\n")):
        for x, char in enumerate(line):
            if char == "#":
                walls.add((y, x))
            elif char == "S":
                start = (y, x)
            elif char == "E":
                end = (y, x)

    return World(start=start, end=end, walls=walls)


def solve(world: World) -> dict[tuple[Coord, Coord], int]:
    cheapest: dict[tuple[Coord, Coord], int] = {}
    search = [(0, world.start, cartesian.RIGHT)]

    while search:
        cost, node, direction = heapq.heappop(search)
        if cheapest.get((node, direction), float("inf")) <= cost:
            continue

        cheapest[(node, direction)] = cost
        if node == world.end:
            continue

        for new_direction, move_cost in (
            (cartesian.LEFT_TURN[direction], 1001),
            (cartesian.RIGHT_TURN[direction], 1001),
            (cartesian.REVERSE[direction], 2001),
            (direction, 1),
        ):
            neighbor = cartesian.move(node, new_direction)
            if neighbor in world.walls:
                continue
            else:
                heapq.heappush(search, (cost + move_cost, neighbor, new_direction))

    return cheapest


def part1(world: World) -> int:
    return int(
        min(
            solve(world).get((world.end, direction), float("inf"))
            for direction in (cartesian.UP, cartesian.RIGHT, cartesian.DOWN, cartesian.LEFT)
        )
    )


def part2(world: World) -> int:
    cheapest = solve(world)
    cost = int(
        min(
            solve(world).get((world.end, direction), float("inf"))
            for direction in (cartesian.UP, cartesian.RIGHT, cartesian.DOWN, cartesian.LEFT)
        )
    )

    seats: set[Coord] = set()
    search = [(cost, world.end)]
    while search:
        cost, node = search.pop()
        seats.add(node)

        for neighbor in cartesian.neighbors(node):
            if neighbor in world.walls:
                continue

            for original_direction in (cartesian.UP, cartesian.RIGHT, cartesian.DOWN, cartesian.LEFT):
                for direction, move_cost in (
                    (cartesian.LEFT_TURN[original_direction], 1001),
                    (cartesian.RIGHT_TURN[original_direction], 1001),
                    (cartesian.REVERSE[original_direction], 2001),
                    (original_direction, 1),
                ):
                    if (
                        node == cartesian.move(neighbor, direction)
                        and cheapest.get((neighbor, original_direction), float("inf")) == cost - move_cost
                    ):
                        search.append((cost - move_cost, neighbor))

    return len(seats)


def test_part1() -> None:
    data = dedent("""
    ###############
    #.......#....E#
    #.#.###.#.###.#
    #.....#.#...#.#
    #.###.#####.#.#
    #.#.#.......#.#
    #.#.#####.###.#
    #...........#.#
    ###.#.#####.#.#
    #...#.....#.#.#
    #.#.#.###.#.#.#
    #.....#...#.#.#
    #.###.#.#.#.#.#
    #S..#.....#...#
    ###############
    """).strip()
    assert part1(parse(data)) == 7036


def test_part2() -> None:
    data = dedent("""
    ###############
    #.......#....E#
    #.#.###.#.###.#
    #.....#.#...#.#
    #.###.#####.#.#
    #.#.#.......#.#
    #.#.#####.###.#
    #...........#.#
    ###.#.#####.#.#
    #...#.....#.#.#
    #.#.#.###.#.#.#
    #.....#...#.#.#
    #.###.#.#.#.#.#
    #S..#.....#...#
    ###############
    """).strip()
    assert part2(parse(data)) == 45


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
