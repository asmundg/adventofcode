"""Day 17: Chronospatial Computer

Well, that took a turn.

Part 1 is a standard computer simulator, with the usual semi-weird
behaviors.

Part 2 requires a bit of reverse engineering to realize that the
program keeps using a as input and then shifting a right by three bits
until it's zero. This means the program is looking at len(program)
triplets of bits. This is made more complicated by the fact that the
comparison it makes to produce output depends on a variable number of
bits.

Still, since we know the termination condition (a == 0), we can work
backwards from the end and find the last three bits of a that produce
tha last part of the program. We can then search by lshifting a by 3
and adding all possible bit triplets. If we prune all values that
don't produce the n-suffix, we can keep going until we get the
complete output, without needing to try 2**48 inputs.
"""

import copy
import os
from dataclasses import dataclass
from textwrap import dedent


@dataclass(frozen=True)
class Instruction:
    op: int
    operand: int


@dataclass(frozen=True)
class Computer:
    registers: list[int]
    program: list[int]
    output: list[int]


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> Computer:
    reg, prog = data.split("\n\n")
    registers: list[int] = []
    for r in reg.split("\n"):
        registers.append(int(r.split(": ")[1]))
    assert len(registers) == 3

    program = [int(n) for n in prog.split(": ")[1].split(",")]
    return Computer(registers, program, [])


def combo(computer: Computer, operand: int) -> int:
    if operand <= 3:
        return operand
    elif operand <= 6:
        return computer.registers[operand - 4]
    else:
        raise ValueError(f"Invalid operand: {operand}")


def step(computer: Computer, ip: int) -> int:
    match (computer.program[ip], computer.program[ip + 1]):
        # adv
        case (0, operand):
            computer.registers[0] = computer.registers[0] // (2 ** combo(computer, operand))
            ip += 2
        # bxl
        case (1, operand):
            computer.registers[1] = computer.registers[1] ^ operand
            ip += 2
        # bst
        case (2, operand):
            computer.registers[1] = combo(computer, operand) % 8
            ip += 2
        # jnz
        case (3, operand):
            if computer.registers[0] == 0:
                ip += 2
            else:
                ip = operand
        # bxc
        case (4, operand):
            computer.registers[1] = computer.registers[1] ^ computer.registers[2]
            ip += 2
        # out
        case (5, operand):
            computer.output.append(combo(computer, operand) % 8)
            ip += 2
        # bdv
        case (6, operand):
            computer.registers[1] = computer.registers[0] // (2 ** combo(computer, operand))
            ip += 2
        # cdv
        case (7, operand):
            computer.registers[2] = computer.registers[0] // (2 ** combo(computer, operand))
            ip += 2

    return ip


def run(computer: Computer) -> Computer:
    ip = 0
    while ip < len(computer.program):
        ip = step(computer, ip)

    return computer


def part1(computer: Computer) -> str:
    run(computer)
    return ",".join(str(i) for i in computer.output)


def part2(computer: Computer) -> int:
    best = float("inf")

    search: list[tuple[int, int]] = []
    for a in range(8):
        search.append((a, 1))

    while search:
        candidate_a, triplet_count = search.pop()

        local_computer = copy.deepcopy(computer)
        local_computer.registers[0] = candidate_a
        run(local_computer)

        if local_computer.output == local_computer.program:
            best = min(best, candidate_a)
            continue

        if local_computer.output == computer.program[-triplet_count:]:
            for new_bits in range(8):
                search.append((candidate_a << 3 | new_bits, triplet_count + 1))

    return int(best)


def test_part1() -> None:
    data = dedent("""
    Register A: 729
    Register B: 0
    Register C: 0
    
    Program: 0,1,5,4,3,0
    """).strip()
    assert part1(parse(data)) == "4,6,3,5,6,3,5,2,1,0"


def test_part2() -> None:
    data = dedent("""
    Register A: 2024
    Register B: 0
    Register C: 0
    
    Program: 0,3,5,4,3,0
    """).strip()
    assert part2(parse(data)) == 117440


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
