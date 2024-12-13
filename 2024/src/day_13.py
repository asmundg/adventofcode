"""Day 13: Claw Contraption

It's way to early in the morning for doing equations by hand. So
instead, we'll just turn to Z3 to fix the problem for us. The problem
is a linear equation set:

timesA * a_moveX + timesB * b_moveX == prizeX
timesB * b_moveY + timesB * b_moveY == prizeY

which we can solve for timesA and timesB. If there is a solution,
we're done. This obviously scales to large values of timesA and
timesB, unlike a simulation-based solution.
"""

import os
import re
from dataclasses import dataclass
from textwrap import dedent

import z3
from common.cartesian import Coord


@dataclass(frozen=True)
class Machine:
    a: Coord
    b: Coord
    prize: Coord


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> list[Machine]:
    machines: list[Machine] = []
    for machine in data.split("\n\n"):
        parts: list[Coord] = []
        for part in machine.split("\n"):
            m = re.match(r".*: X[+=](\d+), Y[+=](\d+)", part)
            assert m is not None
            x, y = [int(n) for n in m.groups()]
            parts.append((x, y))

        machines.append(Machine(*parts))
    return machines


def solve(machines: list[Machine], offset: int = 0) -> int:
    total = 0

    for machine in machines:
        a = z3.Int("a")
        b = z3.Int("b")
        solver = z3.Solver()
        solver.add(a * machine.a[0] + b * machine.b[0] == machine.prize[0] + offset)
        solver.add(a * machine.a[1] + b * machine.b[1] == machine.prize[1] + offset)
        if solver.check() == z3.sat:
            m = solver.model()
            total += 3 * m[a].as_long() + m[b].as_long()

    return total


def part1(machines: list[Machine]) -> int:
    return solve(machines)


def part2(machines: list[Machine]) -> int:
    return solve(machines, 10000000000000)


def test_part1() -> None:
    data = dedent("""
    Button A: X+94, Y+34
    Button B: X+22, Y+67
    Prize: X=8400, Y=5400
    
    Button A: X+26, Y+66
    Button B: X+67, Y+21
    Prize: X=12748, Y=12176
    
    Button A: X+17, Y+86
    Button B: X+84, Y+37
    Prize: X=7870, Y=6450
    
    Button A: X+69, Y+23
    Button B: X+27, Y+71
    Prize: X=18641, Y=10279
    """).strip()
    assert part1(parse(data)) == 480


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
