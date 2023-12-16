"""Day 16: The Floor Will Be Lava

More instruction-following, but with a search tree this time. To avoid
getting stuck in infinite loops, we need to abort when we start
following a beam that already exists. Which is fine, since they don't
interact and won't produce any new outputs.

We could also solve this using recursion/memoizing for each beam, but
that would make the visualization harder. :P
"""

import os
from textwrap import dedent

from typing import List, Tuple, Set, Dict, TypeAlias, Sequence

Data: TypeAlias = List[str]
Coord: TypeAlias = Tuple[int, int]


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> Data:
    return data.split("\n")


DOWN = (1, 0)
UP = (-1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

MIRRORS: Dict[str, Dict[Coord, Sequence[Coord]]] = {
    "|": {LEFT: (UP, DOWN), RIGHT: (UP, DOWN)},
    "-": {UP: (LEFT, RIGHT), DOWN: (LEFT, RIGHT)},
    "/": {RIGHT: (UP,), DOWN: (LEFT,), LEFT: (DOWN,), UP: (RIGHT,)},
    "\\": {RIGHT: (DOWN,), DOWN: (RIGHT,), LEFT: (UP,), UP: (LEFT,)},
}


def energize(grid: Data, start: Tuple[Coord, Coord]):
    max_y = len(grid)
    max_x = len(grid[0])
    energized: Dict[Coord, Set[Coord]] = {}
    search = [start]
    while search:
        pos, direction = search.pop()
        pos = (pos[0] + direction[0], pos[1] + direction[1])

        # Left grid
        if not (-1 < pos[0] < max_y and -1 < pos[1] < max_x):
            continue

        # Already passed this tile in this direction
        if direction in energized.get(pos, set()):
            continue

        energized.setdefault(pos, set()).add(direction)

        tile = grid[pos[0]][pos[1]]
        if tile in MIRRORS:
            if direction in MIRRORS[tile]:
                for new_beam in MIRRORS[tile][direction]:
                    search.append((pos, new_beam))
                continue

        search.append((pos, direction))

    return energized


def part1(data: str) -> int:
    grid = parse(data)
    return len(energize(grid, ((0, -1), (0, 1))))


def part2(data: str) -> int:
    grid = parse(data)

    largest = 0
    for y in range(len(grid)):
        for x, dx in ((-1, RIGHT), (len(grid[0]), LEFT)):
            energized = len(energize(grid, ((y, x), dx)))
            if energized > largest:
                largest = energized

    for x in range(len(grid[0])):
        for y, dy in ((-1, DOWN), (len(grid), UP)):
            energized = len(energize(grid, ((y, x), dy)))
            if energized > largest:
                largest = energized

    return largest


def p(grid: List[str], energized: Dict[Coord, Set[Coord]]):
    d = {UP: "^", DOWN: "v", LEFT: "<", RIGHT: ">"}
    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            if char == ".":
                if (y, x) in energized:
                    char = (
                        d[list(energized[(y, x)])[0]]
                        if len(energized[(y, x)]) == 1
                        else str(len(energized[(y, x)]))
                    )
            print(char, end="")
        print()
    print()


def test_part1():
    data = dedent(
        """
        .|...\\....
        |.-.\\.....
        .....|-...
        ........|.
        ..........
        .........\\
        ..../.\\\\..
        .-.-/..|..
        .|....-|.\\
        ..//.|....
        """
    ).strip()

    assert (part1(data)) == 46


def test_part2():
    data = dedent(
        """
        .|...\\....
        |.-.\\.....
        .....|-...
        ........|.
        ..........
        .........\\
        ..../.\\\\..
        .-.-/..|..
        .|....-|.\\
        ..//.|....
        """
    ).strip()

    assert (part2(data)) == 51


if __name__ == "__main__":
    print(part1(read_data()))
    print(part2(read_data()))
