"""Day 24: Never Tell Me The Odds

Yay, geometry. I had to research this a bit. It turns out that
determining line intersections is pretty trivial. Part 2 reduces to a
system of equations:

fx(t) = tdx + x, ...

where we have a collision when fx_rock(t) == fx_hail(t), ...

Through some convolutions, this results in an expression where the
left hand side purely refers to the rock's coordinates and
speed. Which are constant and means we can substitute in values for
the different hailstones to calculate the 6 unknowns.

Since this is a lot of work, it also turns out that algebraic solvers
are a thing and that they will happily do all of the work for
us. Magic!

"""

import itertools
import os
import re
from textwrap import dedent
import z3


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str):
    hail = []
    for line in data.split("\n"):
        m = re.match(
            r"(\d+),\s+(\d+),\s+(\d+)\s+@\s+(-?\d+),\s+(-?\d+),\s+(-?\d+)", line
        )
        assert m, f"Failed to parse {line}"

        x, y, z, dx, dy, dz = map(int, m.groups())
        hail.append(((x, y, z), (dx, dy, dz)))
    return hail


def intersects(a, b):
    (x1, y1, _), (dx1, dy1, _) = a
    (x2, y2) = (x1 + dx1, y1 + dy1)
    (x3, y3, _), (dx2, dy2, _) = b
    (x4, y4) = (x3 + dx2, y3 + dy2)

    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if den == 0:
        return None

    px = (
        ((x1 * y2) - (y1 * x2)) * (x3 - x4) - (x1 - x2) * ((x3 * y4) - (y3 * x4))
    ) / den
    py = (
        ((x1 * y2) - (y1 * x2)) * (y3 - y4) - (y1 - y2) * ((x3 * y4) - (y3 * x4))
    ) / den

    # Check that the intersection is not in the past
    if dx1 > 0 and px < x1 or dx1 < 0 and px > x1:
        return None
    if dy1 > 0 and py < y1 or dy1 < 0 and py > y1:
        return None
    if dx2 > 0 and px < x3 or dx2 < 0 and px > x3:
        return None
    if dy2 > 0 and py < y3 or dy2 < 0 and py > y3:
        return None

    return (px, py)


def part1(data: str, bounds=(0, 0)) -> int:
    hail = parse(data)
    count = 0
    for a, b in itertools.combinations(hail, 2):
        p = intersects(a, b)
        if (
            p
            and p[0] >= bounds[0]
            and p[0] <= bounds[1]
            and p[1] >= bounds[0]
            and p[1] <= bounds[1]
        ):
            count += 1
    return count


def move(a, n):
    (x, y, z), (dx, dy, dz) = a
    return (x + dx * n, y + dy * n, z + dz * n)


def part2(data: str) -> int:
    hail = parse(data)

    rock_x = z3.Int("rock_x")
    rock_y = z3.Int("rock_y")
    rock_z = z3.Int("rock_z")
    rock_dx = z3.Int("rock_dx")
    rock_dy = z3.Int("rock_dy")
    rock_dz = z3.Int("rock_dz")

    # At collision time t, the rock coordinates will be the same as
    # the coordinates of one hailstone
    solver = z3.Solver()
    for i, ((hx, hy, hz), (hdx, hdy, hdz)) in enumerate(hail):
        t = z3.Int(f"t_{i}")
        solver.add(t > 0)
        solver.add(rock_x + rock_dx * t == hx + hdx * t)
        solver.add(rock_y + rock_dy * t == hy + hdy * t)
        solver.add(rock_z + rock_dz * t == hz + hdz * t)

    assert solver.check() == z3.sat
    m = solver.model()
    return sum(m[v].as_long() for v in (rock_x, rock_y, rock_z))


def test_part1():
    data = dedent(
        """
        19, 13, 30 @ -2,  1, -2
        18, 19, 22 @ -1, -1, -2
        20, 25, 34 @ -2, -2, -4
        12, 31, 28 @ -1, -2, -1
        20, 19, 15 @  1, -5, -3
        """
    ).strip()

    assert part1(data, (7, 27)) == 2


def test_part2():
    data = dedent(
        """
        19, 13, 30 @ -2,  1, -2
        18, 19, 22 @ -1, -1, -2
        20, 25, 34 @ -2, -2, -4
        12, 31, 28 @ -1, -2, -1
        20, 19, 15 @  1, -5, -3
        """
    ).strip()

    assert part2(data) == 47


if __name__ == "__main__":
    print(part1(read_data(), (200000000000000, 400000000000000)))
    print(part2(read_data()))
