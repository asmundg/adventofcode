"""Day 12: Leonardo's Monorail

This looks like a plain, minimal emulator (again - same as day 23 in
2015)

"""

import os
import re
from dataclasses import dataclass
from textwrap import dedent


@dataclass(frozen=True)
class Instruction:
    ins: str
    args: tuple[str | int, ...]


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> list[Instruction]:
    instructions: list[Instruction] = []
    for line in data.split("\n"):
        ins, *args = line.split()
        instructions.append(Instruction(ins, tuple([int(arg) if arg.isdigit() else arg for arg in args])))
    return instructions


def exec(program: list[Instruction], registers: dict[str, int]) -> dict[str, int]:
    ptr = 0
    while ptr < len(program):
        instruction = program[ptr]
        if instruction.ins == "cpy":
            src = instruction.args[0]
            tgt = str(instruction.args[1])
            registers[tgt] = src if isinstance(src, int) else registers[src]
            ptr += 1
        if instruction.ins == "inc":
            tgt = str(instruction.args[0])
            registers[tgt] = registers[tgt] + 1
            ptr += 1
        if instruction.ins == "dec":
            tgt = str(instruction.args[0])
            registers[tgt] = registers[tgt] - 1
            ptr += 1
        if instruction.ins == "jnz":
            src = instruction.args[0]
            p = src if isinstance(src, int) else registers[str(src)]
            diff = int(instruction.args[1])
            if p != 0:
                ptr += diff
            else:
                ptr += 1

    return registers


def part1(program: list[Instruction]) -> int:
    return exec(program, registers={"a": 0, "b": 0, "c": 0, "d": 0})["a"]


def part2(program: list[Instruction]) -> int:
    return exec(program, registers={"a": 0, "b": 0, "c": 1, "d": 0})["a"]


def test_part1() -> None:
    data = dedent("""
    cpy 41 a
    inc a
    inc a
    dec a
    jnz a 2
    dec a
    """).strip()
    assert part1(parse(data)) == 42


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
