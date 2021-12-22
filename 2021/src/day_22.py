"""Again, rather simple idea, very complex implementation.

Visualizing 3D object manipulation is surprisingly hard. This is not
super efficient, but splitting the existing cubes until we can
construct the shape of (A - B) out of cubes is at least grokkable.

We could probably have been more clever about actually joining "on"
cubes that are fully contained in other cubes. Oh well.

"""

import math
import re
import os


def read_data(fname):
    with open(fname, encoding="utf-8") as handle:
        return parse(handle.readlines())


def parse(lines):
    regex = r"(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)"
    parsed = []
    for line in lines:
        m = re.match(regex, line.strip())
        parsed.append(
            (
                m.group(1),
                (
                    (int(m.group(2)), int(m.group(3)) + 1),
                    (int(m.group(4)), int(m.group(5)) + 1),
                    (int(m.group(6)), int(m.group(7)) + 1),
                ),
            )
        )
    return parsed


def is_overlapping(dim_a, dim_b):
    return dim_a[0] < dim_b[1] and dim_a[1] > dim_b[0]


def is_overlapping_cube(cube_a, cube_b):
    return False not in [
        False for i in range(3) if not is_overlapping(cube_a[i], cube_b[i])
    ]


def overlap_segments(dim_a, dim_b):
    points = []
    # b starts before a
    if dim_b[0] <= dim_a[0]:
        if dim_b[1] < dim_a[1]:
            points.append((dim_a[0], dim_b[1]))
            points.append((dim_b[1], dim_a[1]))
        else:
            points.append((dim_a[0], dim_a[1]))
    # b starts inside a
    else:
        points.append((dim_a[0], dim_b[0]))
        if dim_b[1] < dim_a[1]:
            points.append((dim_b[0], dim_b[1]))
            points.append((dim_b[1], dim_a[1]))
        else:
            points.append((dim_b[0], dim_a[1]))

    return points


def without(cube_a, cube_b):
    """cube_a - cube_b"""
    new_cubes = []
    for x in overlap_segments(cube_a[0], cube_b[0]):
        for y in overlap_segments(cube_a[1], cube_b[1]):
            for z in overlap_segments(cube_a[2], cube_b[2]):
                if not is_overlapping_cube((x, y, z), cube_b):
                    new_cubes.append((x, y, z))

    return new_cubes


def carve(cubes, new_cube):
    """Return the set of cubes minus the new cube. This will require
    splitting any overlapping cubes up until we can remove the ones
    that are fully contained by new_cube.
    """
    carved_cubes = []
    for cube in cubes:
        if is_overlapping_cube(cube, new_cube):
            carved_cubes += without(cube, new_cube)
        else:
            carved_cubes.append(cube)
    return carved_cubes


def solve(lines, limit=0):
    cubes = []
    cmd, cube = lines[0]
    for cmd, cube in [
        (cmd, cube)
        for cmd, cube in lines
        if not limit
        or not [1 for i in range(3) if cube[i][0] < (-limit) or cube[i][1] > limit + 1]
    ]:
        cubes = carve(cubes, cube)

        if cmd == "on":
            cubes.append(cube)

    return sum(math.prod(dim[1] - dim[0] for dim in cube) for cube in cubes)


if __name__ == "__main__":
    print(
        solve(
            read_data(os.path.join(os.path.dirname(__file__), "input/22.input")),
            limit=50,
        ),
    )
    print(solve(read_data(os.path.join(os.path.dirname(__file__), "input/22.input"))))
