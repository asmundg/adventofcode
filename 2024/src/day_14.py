"""Day 14: Restroom Redoubt

Well, that was certainly a break from finding algorithms. Part 1 can
be simulated, but is simpler if we just use modulo to get the position
after moving X steps N times.

Part 2 can be solved in different ways, but if we don't make any
assumptions about what the 'christmas tree' is supposed to look like,
we can leverage the fact that the robots produce a highly random
output, except for the one output in which they form a picture. This
means entropy in the rendered picture is signifantly lower at the
specific point. This is standard crypto analysisa, and we can
trivially get a proxy for the entropy by seeing how well the output
string compresses.

"""

import math
import os
import re
import zlib
from dataclasses import dataclass
from textwrap import dedent

from common.cartesian import Coord


@dataclass(frozen=True)
class Robot:
    start: Coord
    speed: Coord


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> list[Robot]:
    robots: list[Robot] = []
    for robot in data.split("\n"):
        m = re.findall(r"(-?\d+)", robot)
        assert m is not None
        x, y, dx, dy = [int(n) for n in m]
        robots.append(Robot((y, x), (dy, dx)))
    return robots


def move(robot: Robot, max_y: int, max_x: int, steps: int) -> Coord:
    return ((robot.start[0] + steps * robot.speed[0]) % max_y, (robot.start[1] + steps * robot.speed[1]) % max_x)


def part1(robots: list[Robot], max_y: int, max_x: int) -> int:
    # top_left, top_right, bottom_left, bottom_right
    final = {move(robot, max_y, max_x, 100) for robot in robots}
    quads = [0, 0, 0, 0]
    for y, x in final:
        if y < max_y // 2 and x < max_x // 2:
            quads[0] += 1
        elif y < max_y // 2 and x > max_x // 2:
            quads[1] += 1
        elif y > max_y // 2 and x < max_x // 2:
            quads[2] += 1
        elif y > max_y // 2 and x > max_x // 2:
            quads[3] += 1
        else:
            pass
    return quads[0] * quads[1] * quads[2] * quads[3]


def debug(robots: set[Coord], max_y: int, max_x: int):
    s = ""
    for y in range(max_y):
        for x in range(max_x):
            if (y, x) in robots:
                s += "#"
            else:
                s += "."
        s += "\n"
    return s


def part2(robots: list[Robot]) -> int:
    max_y = 103
    max_x = 101
    cycles = []

    # Find the period for all robots to get back to their starting
    # positions. This is is our search space. The robots happen to all
    # have the same cycle, but we calculate the LCM just for
    # completeness.
    for robot in robots:
        i = 1
        while move(robot, max_y, max_x, i) != robot.start:
            i += 1
        cycles.append(i)
    global_cycle = math.lcm(*cycles)
    print("Found global cycle:", global_cycle)

    # Then we produce all outputs in the search space and find the one
    # producing the picture with the highest compression rate.
    outputs = [{move(robot, max_y, max_x, steps) for robot in robots} for steps in range(global_cycle)]
    _, target, output = min(
        (len(zlib.compress(debug(candidate, max_y, max_x).encode())), i, candidate)
        for i, candidate in enumerate(outputs)
    )
    print(debug(output, max_y, max_x))
    return target


def test_part1() -> None:
    data = dedent("""
    p=0,4 v=3,-3
    p=6,3 v=-1,-3
    p=10,3 v=-1,2
    p=2,0 v=2,-1
    p=0,0 v=1,3
    p=3,0 v=-2,-2
    p=7,6 v=-1,-3
    p=3,0 v=-1,-2
    p=9,3 v=2,3
    p=7,3 v=-1,2
    p=2,4 v=2,-3
    p=9,5 v=-3,-3
    """).strip()
    assert part1(parse(data), 7, 11) == 12


if __name__ == "__main__":
    print(part1(parse(read_data()), 103, 101))
    print(part2(parse(read_data())))
