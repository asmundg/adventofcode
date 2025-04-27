"""Day 25: Clock Signal

We could try to decompile and reverse-engineer the logic here. Or we
can just brute force numbers until we find one that generates an
apparent cyclic behavior.

"""

import itertools
import os
from dataclasses import dataclass


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


def exec(program: list[Instruction], registers: dict[str, int]) -> int:
    ptr = 0
    out_sequence = []
    while ptr < len(program):
        instruction = program[ptr]
        if instruction.ins == "out":
            src = instruction.args[0]
            value = src if isinstance(src, int) else registers[src]
            out_sequence.append(value)
            if out_sequence != list(itertools.islice(itertools.cycle([0, 1]), len(out_sequence))):
                return -1
            if len(out_sequence) > 100:
                return 0
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

    raise Exception("Oops")


def part1(program: list[Instruction]) -> int:
    for a in itertools.count():
        res = exec(program, registers={"a": a, "b": 0, "c": 0, "d": 0})
        if res == 0:
            return a

    raise Exception("Oops")


if __name__ == "__main__":
    print(part1(parse(read_data())))
