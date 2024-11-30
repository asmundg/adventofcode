"""Day 13: A Maze of Twisty Little Cubicles

Part1 is a standard A* problem, where we just DFS the most promising
paths (defined by shortest distance to target).

In part 2, we want a flood fill instead. We could do this for part 1
as well, but won't bother since we already have a more efficient
solution.

"""

import heapq

from common.cartesian import Coord


def is_open(coord: Coord, magic: int) -> bool:
    x, y = coord
    return bin((x * x + 3 * x + 2 * x * y + y + y * y + magic)).count("1") % 2 == 0


def neighbours(node: Coord) -> list[Coord]:
    return [
        node
        for node in [
            (node[0] - 1, node[1]),
            (node[0], node[1] - 1),
            (node[0] + 1, node[1]),
            (node[0], node[1] + 1),
        ]
        if node[0] >= 0 and node[1] >= 0
    ]


def part1(target: Coord, magic: int) -> int:
    best: dict[Coord, int] = {}
    search: list[tuple[int, int, Coord]] = [(0, 0, (1, 1))]
    while search:
        _, cost, node = heapq.heappop(search)

        for next_node in neighbours(node):
            dist = abs(target[0] - next_node[0]) + abs(target[1] - next_node[1])
            if (
                is_open(next_node, magic)
                and (next_node not in best or best[next_node] > cost + 1)
                and cost + dist < best.get(target, cost + dist + 2)
            ):
                best[next_node] = cost + 1
                heapq.heappush(search, (dist, cost + 1, next_node))
    return best[target]


def part2(magic: int, steps: int) -> int:
    visited: set[Coord] = set([(1, 1)])
    search: list[tuple[int, Coord]] = [(0, (1, 1))]
    while search:
        cost, node = search.pop(0)
        for next_node in neighbours(node):
            if (cost + 1) <= steps and is_open(next_node, magic) and next_node not in visited:
                visited.add(next_node)
                search.append((cost + 1, next_node))
    return len(visited)


def test_part1() -> None:
    assert is_open((3, 2), 10)
    assert not is_open((5, 4), 10)
    assert part1((7, 4), 10) == 11


if __name__ == "__main__":
    print(part1((31, 39), 1358))
    print(part2(1358, 50))
