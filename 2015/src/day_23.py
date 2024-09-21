"""Day 23: Opening the Turing Lock.

Super trivial microcomputer. I got slightly thrown by the spec not
defining what happens when the jie/jio predicate fails, but ptr
incrementing is the only thing that makes sense.
"""

import os
from textwrap import dedent
from typing import List, Tuple


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> List[Tuple[str, Tuple[str]]]:
    program: List[Tuple[str, Tuple[str]]] = []
    for line in data.split("\n"):
        instruction, args = line.split(" ", 1)
        args = args.split(", ")
        program.append((instruction, args))
    return program


def comp(program, registers):
    ptr = 0

    while ptr < len(program):
        instruction, args = program[ptr]
        if instruction == "hlf":
            registers[args[0]] /= 2
            ptr += 1
        elif instruction == "tpl":
            registers[args[0]] *= 3
            ptr += 1
        elif instruction == "inc":
            registers[args[0]] += 1
            ptr += 1
        elif instruction == "jmp":
            ptr += int(args[0])
        elif instruction == "jie":
            ptr += int(args[1]) if registers[args[0]] % 2 == 0 else 1
        elif instruction == "jio":
            ptr += int(args[1]) if registers[args[0]] == 1 else 1
        else:
            assert f"Invalid instruction {instruction}"

    return registers


def test_part1():
    data = dedent(
        """
        inc a
        jio a, +2
        tpl a
        inc a
        """
    ).strip()

    assert comp(parse(data), {"a": 0, "b": 0})["a"] == 2


if __name__ == "__main__":
    print(comp(parse(read_data()), {"a": 0, "b": 0}))
    print(comp(parse(read_data()), {"a": 1, "b": 0}))
