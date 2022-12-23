"""Day 22:
"""

import os
from typing import List, Tuple, Union


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


# clockwise rortation, starting left-facing
DIRECTIONS = ((0, 1), (1, 0), (0, -1), (-1, 0))


def move(tiles: List[str], yx: Tuple[int, int], d: Tuple[int, int]) -> Tuple[int, int]:
    y, x = yx
    dy, dx = d

    next_y, next_x = y, x

    # wrap
    if (
        y + dy < 0
        or x + dx < 0
        or y + dy >= len(tiles)
        or x + dx >= len(tiles[y + dy])
        or tiles[y + dy][x + dx] == " "
    ):
        while (
            next_y - dy >= 0
            and next_x - dx >= 0
            and next_y - dy < len(tiles)
            and next_x - dx < len(tiles[next_y - dy])
            and tiles[next_y - dy][next_x - dx] != " "
        ):
            next_y -= dy
            next_x -= dx

        return (next_y, next_x) if tiles[next_y][next_x] == "." else (y, x)

    return (y + dy, x + dx) if tiles[y + dy][x + dx] == "." else (y, x)


def solve(fname: str) -> int:
    tiles, cmds = parse(fname)
    direction = 0
    y = 0
    x = tiles[0].index(".")
    for cmd in cmds:
        if isinstance(cmd, str):
            direction = (direction + (1 if cmd == "R" else -1)) % len(DIRECTIONS)
        else:
            dy, dx = DIRECTIONS[direction]
            for _ in range(cmd):
                y, x = move(tiles, (y, x), (dy, dx))

    return 1000 * (y + 1) + 4 * (x + 1) + direction


day = os.path.basename(__file__).split(".")[0].split("_")[1]
base = os.path.join(os.path.dirname(__file__), "input", f"{day}")

print(solve(f"{base}.test"))
print(solve(f"{base}.input"))

# print(solve2(f"{base}.test"))
# print(solve2(f"{base}.input"))
