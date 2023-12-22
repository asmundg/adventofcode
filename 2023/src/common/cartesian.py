from typing import TypeAlias, Tuple

Coord: TypeAlias = Tuple[int, int]

DOWN = (1, 0)
UP = (-1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)


def move(a: Coord, b: Coord) -> Coord:
    return (a[0] + b[0], a[1] + b[1])


def neighbours(p: Coord):
    return [move(p, d) for d in (UP, DOWN, LEFT, RIGHT)]
