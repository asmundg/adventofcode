"""Day 22: Monkey Map

Mechanical state manipulation, with some caveats when falling off the
map. In part 1, we just reverse direction until we hit the other
edge. In part 2, we have to figure out rotations. There might be some
clever approach, but I just printed the faces, folded them and defined
the connection for each cube edge.
"""

from dataclasses import dataclass
import os
from typing import Callable, Dict, List, Tuple, Union


def parse(fname: str) -> Tuple[List[str], List[Union[str, int]]]:
    with open(fname, encoding="utf-8") as handle:
        tiles, raw_cmds = handle.read().split("\n\n")
        cmds: List[Union[str, int]] = []
        current_int = ""
        for c in raw_cmds.strip():
            if c in "0123456789":
                current_int += c
            else:
                if current_int:
                    cmds.append(int(current_int))
                    current_int = ""
                cmds.append(c)
        if current_int:
            cmds.append(int(current_int))
        return tiles.split("\n"), cmds


# clockwise rotation, starting right-facing
DIRECTIONS = ((0, 1), (1, 0), (0, -1), (-1, 0))


@dataclass
class Transform:
    tile: Tuple[int, int]
    transform: Callable[[Tuple[int, int]], Tuple[int, int]]
    direction: int


@dataclass
class Folds:
    top: Transform
    left: Transform
    right: Transform
    bottom: Transform


@dataclass
class FoldConfig:
    folds: Dict[Tuple[int, int], Folds]
    panel_size: int


def folds(max_size: int) -> Dict:
    return {
        TOP_TOP: (lambda yx: (0, max_size - yx[1]), 1),
        TOP_BOTTOM: (lambda yx: (max_size, yx[1]), 3),
        TOP_LEFT: (lambda yx: (yx[1], 0), 0),
        TOP_RIGHT: (lambda yx: (yx[1], max_size), 2),
        RIGHT_LEFT: (lambda yx: (yx[1], 0), 0),
        RIGHT_RIGHT: (lambda yx: (max_size - yx[0], max_size), 2),
        RIGHT_BOTTOM: (lambda yx: (max_size, yx[0]), 3),
        RIGHT_TOP: (lambda yx: (0, max_size - yx[0]), 1),
        BOTTOM_BOTTOM: (lambda yx: (max_size, max_size - yx[1]), 3),
        BOTTOM_RIGHT: (lambda yx: (yx[1], max_size), 2),
        BOTTOM_LEFT: (lambda yx: (max_size - yx[1], 0), 0),
        BOTTOM_TOP: (lambda yx: (0, yx[1]), 1),
        LEFT_TOP: (lambda yx: (0, yx[0]), 1),
        LEFT_RIGHT: (lambda yx: (yx[0], max_size), 2),
        LEFT_BOTTOM: (lambda yx: (max_size, max_size - yx[0]), 3),
        LEFT_LEFT: (lambda yx: (max_size - yx[0], 0), 0),
    }


TOP_TOP = "TOP_TOP"
TOP_BOTTOM = "TOP_BOTTOM"
TOP_LEFT = "TOP_LEFT"
TOP_RIGHT = "TOP_RIGHT"
RIGHT_LEFT = "RIGHT_LEFT"
RIGHT_RIGHT = "RIGHT_RIGHT"
RIGHT_TOP = "RIGHT_TOP"
RIGHT_BOTTOM = "RIGHT_BOTTOM"
BOTTOM_BOTTOM = "BOTTOM_BOTTOM"
BOTTOM_LEFT = "BOTTOM_LEFT"
BOTTOM_TOP = "BOTTOM_TOP"
BOTTOM_RIGHT = "BOTTOM_RIGHT"
LEFT_TOP = "LEFT_TOP"
LEFT_RIGHT = "LEFT_RIGHT"
LEFT_BOTTOM = "LEFT_BOTTOM"
LEFT_LEFT = "LEFT_LEFT"

TEST_PANEL_FOLD_DIRECTIONS = folds(3)
TEST_PANEL_FOLDS = {
    (0, 2): Folds(
        top=Transform((1, 0), *TEST_PANEL_FOLD_DIRECTIONS[TOP_TOP]),
        right=Transform((2, 3), *TEST_PANEL_FOLD_DIRECTIONS[RIGHT_RIGHT]),
        bottom=Transform((1, 2), *TEST_PANEL_FOLD_DIRECTIONS[BOTTOM_TOP]),
        left=Transform((1, 1), *TEST_PANEL_FOLD_DIRECTIONS[LEFT_TOP]),
    ),
    (1, 0): Folds(
        top=Transform((0, 2), *TEST_PANEL_FOLD_DIRECTIONS[TOP_TOP]),
        right=Transform((1, 1), *TEST_PANEL_FOLD_DIRECTIONS[RIGHT_LEFT]),
        bottom=Transform((2, 3), *TEST_PANEL_FOLD_DIRECTIONS[BOTTOM_BOTTOM]),
        left=Transform((2, 3), *TEST_PANEL_FOLD_DIRECTIONS[LEFT_BOTTOM]),
    ),
    (1, 1): Folds(
        top=Transform((0, 2), *TEST_PANEL_FOLD_DIRECTIONS[TOP_LEFT]),
        right=Transform((1, 2), *TEST_PANEL_FOLD_DIRECTIONS[RIGHT_RIGHT]),
        bottom=Transform((2, 2), *TEST_PANEL_FOLD_DIRECTIONS[BOTTOM_LEFT]),
        left=Transform((1, 0), *TEST_PANEL_FOLD_DIRECTIONS[LEFT_RIGHT]),
    ),
    (1, 2): Folds(
        top=Transform((0, 2), *TEST_PANEL_FOLD_DIRECTIONS[TOP_BOTTOM]),
        right=Transform((2, 3), *TEST_PANEL_FOLD_DIRECTIONS[RIGHT_TOP]),
        bottom=Transform((2, 2), *TEST_PANEL_FOLD_DIRECTIONS[BOTTOM_TOP]),
        left=Transform((1, 1), *TEST_PANEL_FOLD_DIRECTIONS[LEFT_RIGHT]),
    ),
    (2, 2): Folds(
        top=Transform((1, 2), *TEST_PANEL_FOLD_DIRECTIONS[TOP_BOTTOM]),
        right=Transform((2, 3), *TEST_PANEL_FOLD_DIRECTIONS[RIGHT_LEFT]),
        bottom=Transform((1, 0), *TEST_PANEL_FOLD_DIRECTIONS[BOTTOM_BOTTOM]),
        left=Transform((1, 1), *TEST_PANEL_FOLD_DIRECTIONS[LEFT_BOTTOM]),
    ),
    (2, 3): Folds(
        top=Transform((1, 2), *TEST_PANEL_FOLD_DIRECTIONS[TOP_RIGHT]),
        right=Transform((0, 2), *TEST_PANEL_FOLD_DIRECTIONS[RIGHT_RIGHT]),
        bottom=Transform((1, 0), *TEST_PANEL_FOLD_DIRECTIONS[BOTTOM_LEFT]),
        left=Transform((2, 3), *TEST_PANEL_FOLD_DIRECTIONS[LEFT_RIGHT]),
    ),
}

INPUT_PANEL_FOLD_DIRECTIONS = folds(49)
INPUT_PANEL_FOLDS = {
    (0, 1): Folds(
        top=Transform((3, 0), *INPUT_PANEL_FOLD_DIRECTIONS[TOP_LEFT]),
        right=Transform((0, 2), *INPUT_PANEL_FOLD_DIRECTIONS[RIGHT_LEFT]),
        bottom=Transform((1, 1), *INPUT_PANEL_FOLD_DIRECTIONS[BOTTOM_TOP]),
        left=Transform((2, 0), *INPUT_PANEL_FOLD_DIRECTIONS[LEFT_LEFT]),
    ),
    (0, 2): Folds(
        top=Transform((3, 0), *INPUT_PANEL_FOLD_DIRECTIONS[TOP_BOTTOM]),
        right=Transform((2, 1), *INPUT_PANEL_FOLD_DIRECTIONS[RIGHT_RIGHT]),
        bottom=Transform((1, 1), *INPUT_PANEL_FOLD_DIRECTIONS[BOTTOM_RIGHT]),
        left=Transform((0, 1), *INPUT_PANEL_FOLD_DIRECTIONS[LEFT_RIGHT]),
    ),
    (1, 1): Folds(
        top=Transform((0, 1), *INPUT_PANEL_FOLD_DIRECTIONS[TOP_BOTTOM]),
        right=Transform((0, 2), *INPUT_PANEL_FOLD_DIRECTIONS[RIGHT_BOTTOM]),
        bottom=Transform((2, 1), *INPUT_PANEL_FOLD_DIRECTIONS[BOTTOM_TOP]),
        left=Transform((2, 0), *INPUT_PANEL_FOLD_DIRECTIONS[LEFT_TOP]),
    ),
    (2, 0): Folds(
        top=Transform((1, 1), *INPUT_PANEL_FOLD_DIRECTIONS[TOP_LEFT]),
        right=Transform((2, 1), *INPUT_PANEL_FOLD_DIRECTIONS[RIGHT_LEFT]),
        bottom=Transform((3, 0), *INPUT_PANEL_FOLD_DIRECTIONS[BOTTOM_TOP]),
        left=Transform((0, 1), *INPUT_PANEL_FOLD_DIRECTIONS[LEFT_LEFT]),
    ),
    (2, 1): Folds(
        top=Transform((1, 1), *INPUT_PANEL_FOLD_DIRECTIONS[TOP_BOTTOM]),
        right=Transform((0, 2), *INPUT_PANEL_FOLD_DIRECTIONS[RIGHT_RIGHT]),
        bottom=Transform((3, 0), *INPUT_PANEL_FOLD_DIRECTIONS[BOTTOM_RIGHT]),
        left=Transform((2, 0), *INPUT_PANEL_FOLD_DIRECTIONS[LEFT_RIGHT]),
    ),
    (3, 0): Folds(
        top=Transform((2, 0), *INPUT_PANEL_FOLD_DIRECTIONS[TOP_BOTTOM]),
        right=Transform((2, 1), *INPUT_PANEL_FOLD_DIRECTIONS[RIGHT_BOTTOM]),
        bottom=Transform((0, 2), *INPUT_PANEL_FOLD_DIRECTIONS[BOTTOM_TOP]),
        left=Transform((0, 1), *INPUT_PANEL_FOLD_DIRECTIONS[LEFT_TOP]),
    ),
}


def move(
    tiles: List[str],
    yx: Tuple[int, int],
    direction: int,
    fold_config: Union[FoldConfig, None],
) -> Tuple[Tuple[int, int], int]:
    y, x = yx
    dy, dx = DIRECTIONS[direction]

    next_y, next_x = y, x

    # wrap
    if (
        y + dy < 0
        or x + dx < 0
        or y + dy >= len(tiles)
        or x + dx >= len(tiles[y + dy])
        or tiles[y + dy][x + dx] == " "
    ):
        if fold_config is None:
            while (
                next_y - dy >= 0
                and next_x - dx >= 0
                and next_y - dy < len(tiles)
                and next_x - dx < len(tiles[next_y - dy])
                and tiles[next_y - dy][next_x - dx] != " "
            ):
                next_y -= dy
                next_x -= dx
        else:
            panel = (y // fold_config.panel_size, x // fold_config.panel_size)
            next_panel = (
                fold_config.folds[panel].right,
                fold_config.folds[panel].bottom,
                fold_config.folds[panel].left,
                fold_config.folds[panel].top,
            )[direction]
            next_y, next_x = next_panel.transform(
                (y % fold_config.panel_size, x % fold_config.panel_size)
            )
            next_y += fold_config.panel_size * next_panel.tile[0]
            next_x += fold_config.panel_size * next_panel.tile[1]

            assert 0 <= next_y <= len(tiles)
            assert 0 <= next_x <= len(tiles[next_y])
            return (
                ((next_y, next_x), next_panel.direction)
                if tiles[next_y][next_x] == "."
                else ((y, x), direction)
            )

        return (
            ((next_y, next_x), direction)
            if tiles[next_y][next_x] == "."
            else ((y, x), direction)
        )

    return (
        ((y + dy, x + dx), direction)
        if tiles[y + dy][x + dx] == "."
        else ((y, x), direction)
    )


def debug(tiles: List[str], yx: Tuple[int, int], direction: int):
    for y in range(len(tiles)):
        for x in range(len(tiles[y])):
            print(">v<^"[direction] if (y, x) == yx else tiles[y][x], end="")
        print()
    print()


def solve(fname: str, fold: Union[FoldConfig, None] = None) -> int:
    tiles, cmds = parse(fname)
    direction = 0
    y = 0
    x = tiles[0].index(".")
    for cmd in cmds:
        if isinstance(cmd, str):
            direction = (direction + (1 if cmd == "R" else -1)) % len(DIRECTIONS)
        else:
            for _ in range(cmd):
                (y, x), direction = move(tiles, (y, x), direction, fold)

    return 1000 * (y + 1) + 4 * (x + 1) + direction


day = os.path.basename(__file__).split(".")[0].split("_")[1]
base = os.path.join(os.path.dirname(__file__), "input", f"{day}")

print(solve(f"{base}.test"))
print(solve(f"{base}.input"))

print(solve(f"{base}.test", FoldConfig(TEST_PANEL_FOLDS, 4)))
print(solve(f"{base}.input", FoldConfig(INPUT_PANEL_FOLDS, 50)))
