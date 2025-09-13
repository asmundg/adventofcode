"""Day 08: I Heard You Like Registers

Once more a parse and process task?

"""

import operator
import os
from dataclasses import dataclass
from textwrap import dedent
from typing import Callable


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


@dataclass(frozen=True)
class Instruction:
    reg: str
    op: tuple[Callable[[int, int], int], int]
    preg: str
    p: tuple[Callable[[int, int], bool], int]

    def predicate(self, val: int) -> bool:
        return self.p[0](val, self.p[1])

    def change(self, val: int) -> int:
        return self.op[0](val, self.op[1])


op_map = {
    ">": operator.gt,
    "<": operator.lt,
    ">=": operator.ge,
    "<=": operator.le,
    "==": operator.eq,
    "!=": operator.ne,
}


def parse(data: str) -> list[Instruction]:
    ins: list[Instruction] = []
    for line in data.split("\n"):
        reg, op, n, _, preg, pop, p = line.split()
        change_op = operator.add if op == "inc" else operator.sub
        ins.append(Instruction(reg=reg, op=(change_op, int(n)), preg=preg, p=(op_map[pop], int(p))))
    return ins


def part1(instructions: list[Instruction]) -> int:
    return solve(instructions)[0]


def part2(instructions: list[Instruction]) -> int:
    return solve(instructions)[1]


def solve(instructions: list[Instruction]) -> tuple[int, int]:
    registers: dict[str, int] = {}
    highest = 0
    for i in instructions:
        if i.predicate(registers.get(i.preg, 0)):
            registers[i.reg] = i.change(registers.get(i.reg, 0))
            highest = max(highest, registers[i.reg])
    return (max(registers.values()), highest)


def test_part1() -> None:
    data = dedent("""
    b inc 5 if a > 1
    a inc 1 if b < 5
    c dec -10 if a >= 1
    c inc -20 if c == 10
    """).strip()
    assert part1(parse(data)) == 1


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
