"""Day 23: A Long Walk

More maze traversal! Part 1 can be solved with a naive BFS on the
tiles.

Part 2 scales out of control when we do this, due to the forkiness of
the maze. To make it tractable, we can instead build a graph out of
the junction points and find the longest sequence from start to
goal. This makes it easier to only selecting paths that take us
forward, although it's still computationally pretty expensive. There
might be some additional cleverness we can apply to abort earlier.

"""

import copy
import os
from textwrap import dedent
from typing import Tuple, TypeAlias
from common import cartesian

Coord: TypeAlias = Tuple[int, int, int]


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str):
    return data.split("\n")


def part1(data: str) -> int:
    grid = parse(data)

    start = (0, [x for x, tile in enumerate(grid[0]) if tile == "."][0])
    goal = (len(grid) - 1, [x for x, tile in enumerate(grid[-1]) if tile == "."][0])

    path = set()
    search = [(start, path)]
    complete_paths = []

    while search:
        (y, x), visited = search.pop()
        if (y, x) == goal:
            complete_paths.append(visited)
            continue

        slopes = {
            ">": cartesian.RIGHT,
            "<": cartesian.LEFT,
            "^": cartesian.UP,
            "v": cartesian.DOWN,
        }

        possible_next = []
        for direction in [
            cartesian.UP,
            cartesian.DOWN,
            cartesian.LEFT,
            cartesian.RIGHT,
        ]:
            if grid[y][x] in slopes and direction != slopes[grid[y][x]]:
                continue

            neighbor = cartesian.move((y, x), direction)
            if not (0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0])):
                continue
            if grid[neighbor[0]][neighbor[1]] == "#":
                continue
            if neighbor in visited:
                continue

            possible_next.append(neighbor)

        if len(possible_next) == 1:
            visited.add(possible_next[0])
            search.append((possible_next[0], visited))
        else:
            for move in possible_next:
                new_visited = set([move])
                new_visited.update(visited)
                search.append((move, new_visited))

    return max(len(p) for p in complete_paths)


def part2(data: str) -> int:
    grid = parse(data)

    start = (0, [x for x, tile in enumerate(grid[0]) if tile == "."][0])
    goal = (len(grid) - 1, [x for x, tile in enumerate(grid[-1]) if tile == "."][0])

    # We'll start by identifying the graph consisting of all junction
    # points and the distance of each edge.
    # (node, source, visited)
    search = [(start, start, {(0, start[1])})]

    c = 0
    edges = {start: set()}
    visited_nodes = set()
    while search:
        (y, x), src, visited = search.pop()
        if (y, x) == goal:
            continue

        while True:
            possible_next = []
            for direction in [
                cartesian.UP,
                cartesian.DOWN,
                cartesian.LEFT,
                cartesian.RIGHT,
            ]:
                neighbor = cartesian.move((y, x), direction)

                if not (
                    0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0])
                ):
                    continue
                if grid[neighbor[0]][neighbor[1]] == "#":
                    continue
                if neighbor in visited:
                    continue

                possible_next.append(neighbor)

            if len(possible_next) == 1:
                visited.add((y, x))
                (y, x) = possible_next[0]
            else:
                # Found a fork, record the edge length and add the new
                # paths to search
                length = len(visited)
                edges[src].add(((y, x), length))
                if (y, x) not in edges:
                    edges[(y, x)] = set()
                edges[(y, x)].add((src, length))

                if (y, x) not in visited_nodes:
                    for move in possible_next:
                        search.append((move, (y, x), {(y, x)}))
                        visited_nodes.add((y, x))
                break

    # Find the cost of all possible paths
    def all_paths(node, visited, path):
        if node == goal:
            yield path
            return

        for neighbor, length in edges[node]:
            if neighbor in visited:
                continue

            new_visited = copy.copy(visited)
            new_visited.add(neighbor)
            yield from all_paths(neighbor, new_visited, path + length)

    return max(all_paths(start, {start}, 0))


def test_part1():
    data = dedent(
        """
        #.#####################
        #.......#########...###
        #######.#########.#.###
        ###.....#.>.>.###.#.###
        ###v#####.#v#.###.#.###
        ###.>...#.#.#.....#...#
        ###v###.#.#.#########.#
        ###...#.#.#.......#...#
        #####.#.#.#######.#.###
        #.....#.#.#.......#...#
        #.#####.#.#.#########v#
        #.#...#...#...###...>.#
        #.#.#v#######v###.###v#
        #...#.>.#...>.>.#.###.#
        #####v#.#.###v#.#.###.#
        #.....#...#...#.#.#...#
        #.#########.###.#.#.###
        #...###...#...#...#.###
        ###.###.#.###v#####v###
        #...#...#.#.>.>.#.>.###
        #.###.###.#.###.#.#v###
        #.....###...###...#...#
        #####################.#
        """
    ).strip()

    assert part1(data) == 94


def test_part2():
    data = dedent(
        """
        #.#####################
        #.......#########...###
        #######.#########.#.###
        ###.....#.>.>.###.#.###
        ###v#####.#v#.###.#.###
        ###.>...#.#.#.....#...#
        ###v###.#.#.#########.#
        ###...#.#.#.......#...#
        #####.#.#.#######.#.###
        #.....#.#.#.......#...#
        #.#####.#.#.#########v#
        #.#...#...#...###...>.#
        #.#.#v#######v###.###v#
        #...#.>.#...>.>.#.###.#
        #####v#.#.###v#.#.###.#
        #.....#...#...#.#.#...#
        #.#########.###.#.#.###
        #...###...#...#...#.###
        ###.###.#.###v#####v###
        #...#...#.#.>.>.#.>.###
        #.###.###.#.###.#.#v###
        #.....###...###...#...#
        #####################.#
        """
    ).strip()

    assert part2(data) == 154


if __name__ == "__main__":
    print(part1(read_data()))
    print(part2(read_data()))
