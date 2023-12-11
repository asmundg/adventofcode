"""Day 10: Pipe Maze

This is fairly mechanical, but a bit messy. The main problem was
cognitive load due to using a lot of relative coordinates for part
2. Once I actually named the relative directions, things got way
easier.

Part 1 requires finding the loop, which is straight forward since we
can just follow the pipes until we reach the start again (no inner
loop detection needed).

Part 2 reuses the loop-finding, but now we need to traverse it and
track what is on each side of the pipe (left and right, relative to
the traversal direction). This lets us find the inside and outside of
the loop, which we determine by flood-filling until we exhaust the
search space or escape the bounding box.

"""

from dataclasses import dataclass
import os
from textwrap import dedent

from typing import List, Set, Tuple, Dict, TypeAlias, Sequence

Coord: TypeAlias = Tuple[int, int]


@dataclass
class Sides:
    left: Sequence[Coord]
    right: Sequence[Coord]


BOTTOM = (1, 0)
TOP = (-1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

NEIGHBOURS: Dict[str, Sequence[Coord]] = {
    "|": [TOP, BOTTOM],
    "-": [LEFT, RIGHT],
    "L": [TOP, RIGHT],
    "J": [LEFT, TOP],
    "7": [LEFT, BOTTOM],
    "F": [BOTTOM, RIGHT],
    "S": [TOP, RIGHT, BOTTOM, LEFT],
}


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> Tuple[Coord, Dict[Coord, str]]:
    pipes = {}
    start = None
    for y, line in enumerate(data.split("\n")):
        for x, char in enumerate(line):
            if char in NEIGHBOURS:
                pipes[(y, x)] = char
            if char == "S":
                start = (y, x)

    assert start is not None
    return start, pipes


def add_coord(a: Coord, b: Coord) -> Coord:
    return (a[0] + b[0], a[1] + b[1])


def neigh(node: Coord, pipes: Dict[Coord, str]) -> Sequence[Coord]:
    if node not in pipes:
        return []

    return [add_coord(node, c) for c in NEIGHBOURS[pipes[node]]]


def find_loop(start: Coord, pipes: Dict[Coord, str]) -> Sequence[Coord]:
    for current in neigh(start, pipes):
        if start not in neigh(current, pipes):
            continue

        history: List[Coord] = [start]
        while current != start:
            history.append(current)
            current = [n for n in neigh(current, pipes) if n != history[-2]][0]
        history.append(start)
        return history

    assert False, "Oops"


def part1(data: str) -> int:
    start, pipes = parse(data)

    shortest: Dict[Coord, int] = {}
    history = find_loop(start, pipes)

    for i, node in enumerate(history):
        shortest[node] = min(shortest.get(node, i), i)
    for i, node in enumerate(reversed(history)):
        shortest[node] = min(shortest.get(node, i), i)

    return max(shortest.values())


# For each tile type, for each direction we came into the tile from,
# show what's on the (relative) left and right side when navigating
# the maze.
LR: Dict[str, Dict[Coord, Sides]] = {
    "|": {
        TOP: Sides(left=[RIGHT], right=[LEFT]),
        BOTTOM: Sides(left=[LEFT], right=[RIGHT]),
    },
    "-": {
        LEFT: Sides(left=[TOP], right=[BOTTOM]),
        RIGHT: Sides(left=[BOTTOM], right=[TOP]),
    },
    "L": {
        TOP: Sides(left=[], right=[LEFT, BOTTOM]),
        RIGHT: Sides(left=[BOTTOM, RIGHT], right=[]),
    },
    "J": {
        TOP: Sides(left=[RIGHT, BOTTOM], right=[]),
        LEFT: Sides(left=[], right=[BOTTOM, RIGHT]),
    },
    "7": {
        LEFT: Sides(left=[TOP, RIGHT], right=[]),
        BOTTOM: Sides(left=[], right=[RIGHT, TOP]),
    },
    "F": {
        BOTTOM: Sides(left=[LEFT, TOP], right=[]),
        RIGHT: Sides(left=[], right=[TOP, LEFT]),
    },
}


def part2(data: str) -> int:
    start, pipes = parse(data)

    history = find_loop(start, pipes)
    # Let's not linearly seach the history array when we need to look
    # for walls
    history_lookup = set(history)

    # Traverse the loop, noting which open tiles we see on our left
    # and right sides
    areas: Sequence[Set[Coord]] = [set(), set()]
    for prev, node in zip(history, history[1:-1]):
        coming_from = (prev[0] - node[0], prev[1] - node[1])
        contact = LR[pipes[node]][coming_from]
        for area, lr in [(areas[0], contact.left), (areas[1], contact.right)]:
            area.update(
                {
                    add_coord(node, c)
                    for c in lr
                    if add_coord(node, c) not in history_lookup
                }
            )

    # Find the loop bounding box, so that we can know if a coordinate
    # is clearly outside the loop.
    min_y = min(c[0] for c in history)
    max_y = max(c[0] for c in history)
    min_x = min(c[1] for c in history)
    max_x = max(c[1] for c in history)

    # Flood-fill the left and right tile sets. We abort when we escape
    # the maze (we're on the outside) and return when we exhaust the
    # search space (we're on the inside).
    for side in areas:
        search = side.copy()
        while search:
            node = search.pop()
            if node[0] < min_y or node[0] > max_y or node[1] < min_x or node[1] > max_x:
                break

            for n in [(add_coord(node, c)) for c in [TOP, RIGHT, BOTTOM, LEFT]]:
                if n not in history and n not in side:
                    search.add(n)
                    side.add(n)
        else:
            return len(side)

    assert False, "Oops"


def test_part1_a():
    data = dedent(
        """
        .....
        .S-7.
        .|.|.
        .L-J.
        .....
        """
    ).strip()

    assert part1(data) == 4


def test_part1_b():
    data = dedent(
        """
        ..F7.
        .FJ|.
        SJ.L7
        |F--J
        LJ...
        """
    ).strip()
    assert part1(data) == 8


def test_part2_a():
    data = dedent(
        """
        ...........
        .S-------7.
        .|F-----7|.
        .||.....||.
        .||.....||.
        .|L-7.F-J|.
        .|..|.|..|.
        .L--J.L--J.
        ...........
        """
    ).strip()

    assert part2(data) == 4


def test_part2_b():
    data = dedent(
        """
        ..........
        .S------7.
        .|F----7|.
        .||....||.
        .||....||.
        .|L-7F-J|.
        .|II||II|.
        .L--JL--J.
        ..........
        """
    ).strip()
    assert part2(data) == 4


def test_part2_c():
    data = dedent(
        """
        .F----7F7F7F7F-7....
        .|F--7||||||||FJ....
        .||.FJ||||||||L7....
        FJL7L7LJLJ||LJ.L-7..
        L--J.L7...LJS7F-7L7.
        ....F-J..F7FJ|L7L7L7
        ....L7.F7||L7|.L7L7|
        .....|FJLJ|FJ|F7|.LJ
        ....FJL-7.||.||||...
        ....L---J.LJ.LJLJ...
        """
    ).strip()
    assert part2(data) == 8


def test_part2_d():
    data = dedent(
        """
        FF7FSF7F7F7F7F7F---7
        L|LJ||||||||||||F--J
        FL-7LJLJ||||||LJL-77
        F--JF--7||LJLJ7F7FJ-
        L---JF-JLJ.||-FJLJJ7
        |F|F-JF---7F7-L7L|7|
        |FFJF7L7F-JF7|JL---7
        7-L-JL7||F7|L7F-7F7|
        L.L7LFJ|||||FJL7||LJ
        L7JLJL-JLJLJL--JLJ.L
        """
    ).strip()
    assert part2(data) == 10


if __name__ == "__main__":
    print(part1(read_data()))
    print(part2(read_data()))
