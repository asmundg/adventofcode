"""Day 23: Safe Cracking

More spec implementation. This implements a multiplier of some sorts
via repeatedly adding one. It seems like some sort of
self-multiplication, and in theory this requires reverse engineering
to avoid exponential scaling going out of control in part 2. However,
the number of iterations is low enough that we can brute force it in
completely reasonable time. I'm conditioned from later years to expect
scaling problems to be completely unfeasible to brute force, so I'm
now torn about accepting that brute-forcable solutions are fine.
"""

import os
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
        instructions.append(Instruction(ins, tuple([int(arg) if arg.lstrip("-").isdigit() else arg for arg in args])))
    return instructions


ONE_ARGS = set(["inc", "dec", "tgl"])
TWO_ARGS = set(["cpy", "jnz"])
REGISTERS = "abcd"


def exec(program: list[Instruction], registers: dict[str, int]) -> dict[str, int]:
    ptr = 0
    while ptr < len(program):
        instruction = program[ptr]
        if instruction.ins == "tgl":
            instruction_address = ptr + registers[str(instruction.args[0])]
            if instruction_address < len(program):
                target = program[instruction_address]
                if target.ins in ONE_ARGS:
                    program[instruction_address] = Instruction("dec" if target.ins == "inc" else "inc", target.args)
                else:
                    program[instruction_address] = Instruction("cpy" if target.ins == "jnz" else "jnz", target.args)
            ptr += 1
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
            offset = instruction.args[1]
            diff = offset if isinstance(offset, int) else registers[offset]
            if p != 0:
                ptr += diff
            else:
                ptr += 1

    return registers


def part1(program: list[Instruction]) -> int:
    return exec(program, registers={"a": 7, "b": 0, "c": 0, "d": 0})["a"]


def part2(program: list[Instruction]) -> int:
    return exec(program, registers={"a": 12, "b": 0, "c": 0, "d": 0})["a"]


def test_part1() -> None:
    data = dedent("""
    cpy 2 a
    tgl a
    tgl a
    tgl a
    cpy 1 a
    dec a
    dec a
    """).strip()
    assert part1(parse(data)) == 3


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
