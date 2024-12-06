from typing import TypeAlias

Coord: TypeAlias = tuple[int, int]

DOWN = (1, 0)
UP = (-1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

LEFT_TURN = {DOWN: RIGHT, LEFT: DOWN, UP: LEFT, RIGHT: UP}
RIGHT_TURN = {DOWN: LEFT, LEFT: UP, UP: RIGHT, RIGHT: DOWN}


def move(a: Coord, b: Coord) -> Coord:
    return (a[0] + b[0], a[1] + b[1])


def neighbors(p: Coord) -> list[Coord]:
    return [move(p, d) for d in (UP, DOWN, LEFT, RIGHT)]
