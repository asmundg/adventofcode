"""Day 17: Clumsy Crucible

Clumsy, indeed! This is a modified A*, with some constraints on which
neighbours we can chose. The constraints also mean that we need to
maintain a superposition of g_scores, since the number of steps you
took to reach a node matters, as well as the direction you entered in.

Absolutely massive difference between CPython and PyPy today.

"""

from dataclasses import dataclass
import heapq
import os
from textwrap import dedent

from typing import Generator, List, Tuple, Set, Dict, TypeAlias

Data: TypeAlias = List[List[int]]
Coord: TypeAlias = Tuple[int, int]


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> Data:
    return [[int(c) for c in line] for line in data.split("\n")]


@dataclass
class Node:
    coord: Coord
    direction: Coord
    length: int

    def __hash__(self):
        return hash((self.coord, self.direction, self.length))

    def __lt__(self, other):
        return self.coord < other.coord


def neighbors_part1(c: Node, max_y: int, max_x: int) -> Generator[Node, None, None]:
    for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        # Can't go out of bounds
        if (
            c.coord[0] + dy < 0
            or c.coord[0] + dy >= max_y
            or c.coord[1] + dx < 0
            or c.coord[1] + dx >= max_x
        ):
            continue

        # Can't go back the way we came
        if (dy and c.direction == (-dy, 0)) or dx and (c.direction == (0, -dx)):
            continue

        # Can't go for more than 3 steps
        if c.length == 3 and c.direction == (dy, dx):
            continue

        yield Node(
            (c.coord[0] + dy, c.coord[1] + dx),
            (dy, dx),
            c.length + 1 if c.direction == (dy, dx) else 1,
        )


def neighbors_part2(c: Node, max_y: int, max_x: int) -> Generator[Node, None, None]:
    for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        # Can't go out of bounds
        if (
            c.coord[0] + dy < 0
            or c.coord[0] + dy >= max_y
            or c.coord[1] + dx < 0
            or c.coord[1] + dx >= max_x
        ):
            continue

        # Can't go back the way we came
        if (dy and c.direction == (-dy, 0)) or dx and (c.direction == (0, -dx)):
            continue

        # Can't go for more than 10 steps
        if c.length == 10 and c.direction == (dy, dx):
            continue

        # Can't go for less than 4 steps before turning
        if c.length < 4 and c.direction != (dy, dx):
            continue

        yield Node(
            (c.coord[0] + dy, c.coord[1] + dx),
            (dy, dx),
            c.length + 1 if c.direction == (dy, dx) else 1,
        )


def astar(data: Data, start: Coord, goal: Coord, neighbors, p2: bool = False) -> int:
    """A* search algorithm.

    https://en.wikipedia.org/wiki/A*_search_algorithm
    """

    def h(c: Coord) -> int:
        return abs(c[0] - goal[0]) + abs(c[1] - goal[1])

    open_set: List[Tuple[int, Node]] = [
        (0, Node(start, (0, 1), 0)),
        (0, Node(start, (1, 0), 0)),
    ]
    came_from: Dict[Node, Node] = {}
    g_score: Dict[Node, int] = {Node(start, (0, 1), 0): 0, Node(start, (1, 0), 0): 0}
    f_score: Dict[Node, int] = {
        Node(start, (0, 1), 0): h(start),
        Node(start, (1, 0), 0): h(start),
    }
    targets: Set[Node] = set()

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current.coord == goal:
            targets.add(current)
            continue

        for neighbor in neighbors(current, len(data), len(data[0])):
            tentative_g_score = (
                g_score[current] + data[neighbor.coord[0]][neighbor.coord[1]]
            )

            if tentative_g_score >= g_score.get(neighbor, tentative_g_score + 1):
                continue

            came_from[neighbor] = current
            g_score[neighbor] = tentative_g_score
            f_score[neighbor] = tentative_g_score + h(neighbor.coord)
            heapq.heappush(open_set, (f_score[neighbor], neighbor))

    if p2:
        t = min(
            (n for n in came_from if n.coord == goal and n.length >= 4),
            key=lambda c: g_score[c],
        )
        return g_score[t]

    return min(g_score[g] for g in targets)


def part1(data: str) -> int:
    grid = parse(data)
    return astar(grid, (0, 0), (len(grid) - 1, len(grid[0]) - 1), neighbors_part1)


def part2(data: str) -> int:
    grid = parse(data)
    return astar(
        grid, (0, 0), (len(grid) - 1, len(grid[0]) - 1), neighbors_part2, p2=True
    )


def test_part1():
    data = dedent(
        """
        2413432311323
        3215453535623
        3255245654254
        3446585845452
        4546657867536
        1438598798454
        4457876987766
        3637877979653
        4654967986887
        4564679986453
        1224686865563
        2546548887735
        4322674655533
        """
    ).strip()

    assert (part1(data)) == 102


def test_part2():
    data = dedent(
        """
        2413432311323
        3215453535623
        3255245654254
        3446585845452
        4546657867536
        1438598798454
        4457876987766
        3637877979653
        4654967986887
        4564679986453
        1224686865563
        2546548887735
        4322674655533
        """
    ).strip()

    assert (part2(data)) == 94

    data = dedent(
        """
        111111111111
        999999999991
        999999999991
        999999999991
        999999999991
        """
    ).strip()

    assert (part2(data)) == 71


if __name__ == "__main__":
    print(part1(read_data()))
    print(part2(read_data()))
