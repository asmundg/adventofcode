"""Day 18: Boiling Boulders.

That's it - I'm switching to python. Set operations are so much
simpler than in JS. We could just build the necessary abstractions,
but using different languages is more fun. (At some point I'll redo
these in Haskell).

This can be simply solved by brute force, although the runtime is on
the order of seconds for part 2 and could probably be nicer.

Counting surfaces without removing air bubbles can be done by starting
at 6 and subtracting a surface for each connected neighbour for each
node.

Part 2 is the same, but we additionally find air bubbles by scanning
the complete volume and seeing if we can reach outside from all
points. If we cannot, the point is trapped and we can remove it from
the surface count. Since air bubbles can be larger than one cube, we
need to find the surface of the whole volume before subtracting,
reusing part 1.
"""

import os
from typing import Set, Tuple, TypeAlias

Coord3D: TypeAlias = Tuple[int, int, int]


def parse(fname: str) -> Set[Coord3D]:
    with open(fname, encoding="utf-8") as handle:
        return set(
            [
                tuple([int(num) for num in line.strip().split(",")])
                for line in handle.read().strip().split("\n")
            ]
        )


def neighbours(point: Coord3D) -> Set[Coord3D]:
    (x, y, z) = point
    return set(
        [
            (x, y, z + 1),
            (x, y, z - 1),
            (x, y + 1, z),
            (x, y - 1, z),
            (x + 1, y, z),
            (x - 1, y, z),
        ]
    )


def surfaces(points: Set[Coord3D]) -> int:
    unconnected = {p: 6 for p in points}

    for n in (neighbours(point) for point in points):
        for (x, y, z) in n:
            if (x, y, z) in unconnected:
                unconnected[(x, y, z)] -= 1

    return sum(unconnected.values())


def is_inside(
    point: Coord3D,
    points: Set[Coord3D],
    min_borders: Coord3D,
    max_borders: Coord3D,
    inside: Set[Coord3D],
    outside: Set[Coord3D],
):
    visited = set([point])
    search = neighbours(point)
    while search:
        (x, y, z) = search.pop()
        visited.add((x, y, z))
        if (x, y, z) in points:
            continue
        if (
            (x, y, z) in outside
            or x > max_borders[0]
            or x < min_borders[0]
            or y > max_borders[1]
            or y < min_borders[1]
            or z > max_borders[2]
            or z < min_borders[2]
        ):
            outside.add(point)
            return False
        search.update(neighbours((x, y, z)) - visited)

    inside.update(visited - points)
    return True


def solve1(fname: str) -> int:
    return surfaces(parse(fname))


def solve2(fname: str) -> int:
    points = parse(fname)
    max_x = max([x for (x, y, z) in points])
    min_x = min([x for (x, y, z) in points])
    max_y = max([y for (x, y, z) in points])
    min_y = min([y for (x, y, z) in points])
    max_z = max([z for (x, y, z) in points])
    min_z = min([z for (x, y, z) in points])
    inside: Set[Coord3D] = set()
    outside: Set[Coord3D] = set()
    for point in [
        (x, y, z) for x in range(max_x) for y in range(max_y) for z in range(max_z)
    ]:
        if point not in points:
            is_inside(
                point,
                points,
                (min_x, min_y, min_z),
                (max_x, max_y, max_z),
                inside,
                outside,
            )

    return surfaces(points) - surfaces(inside)


day = os.path.basename(__file__).split(".")[0].split("_")[1]
base = os.path.join(os.path.dirname(__file__), "input", f"{day}")
print(solve1(f"{base}.test"))
print(solve1(f"{base}.input"))

print(solve2(f"{base}.test"))
print(solve2(f"{base}.input"))
