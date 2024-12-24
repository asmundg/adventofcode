"""Day 24: Crossed Wires

Instant classic. Part 1 is a plain simulation. I have zero idea if
part 2 can be solved programatically, but given that the structure is
a completely standard adder, we can just render the graph and debug it
by hand.

The broken circuits are completely obvious by scanning through the
sequence of adders. There are limited ways in which they are miswired,
and all the broken circuits are inside single adders. Fun!

"""

import os
from dataclasses import dataclass
from textwrap import dedent


@dataclass(frozen=True)
class World:
    wires: dict[str, int]
    gates: dict[str, tuple[str, str, str]]


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> World:
    wire_lines, gate_lines = data.split("\n\n")

    wires = dict()
    for line in wire_lines.split("\n"):
        wire, val = line.split(": ")
        wires[wire] = int(val)

    gates = dict()
    for line in gate_lines.split("\n"):
        a, op, b, _, out = line.split(" ")
        gates[out] = (a, op, b)

    return World(wires, gates)


def evaluate(world: World, bit: str) -> int:
    if bit in world.wires:
        return world.wires[bit]
    a, op, b = world.gates[bit]
    if op == "XOR":
        a_val = evaluate(world, a)
        b_val = evaluate(world, b)
        return a_val ^ b_val
    if op == "AND":
        a_val = evaluate(world, a)
        b_val = evaluate(world, b)
        return a_val & b_val
    if op == "OR":
        a_val = evaluate(world, a)
        b_val = evaluate(world, b)
        return a_val | b_val

    raise ValueError(f"Unknown operation: {op}")


def part1(world: World) -> int:
    return sum(
        evaluate(world, bit) << i for i, bit in enumerate(sorted([k for k in world.gates.keys() if k.startswith("z")]))
    )


def part2(world: World) -> str:
    print("digraph g {")
    for out, (a, op, b) in world.gates.items():
        print(f'  "{a} {op} {b}" -> "{out}"')
        print(f'  "{a}" -> "{a} {op} {b}"')
        print(f'  "{b}" -> "{a} {op} {b}"')
    print("}")
    # knc XOR wcq -> z05 / y05 AND x05 -> gdd
    # jnf XOR wgh -> z09 / kvg OR sgj -> cwt
    # y20 AND x20 -> jmv / y20 XOR x20 -> css
    # vcr XOR nwb -> z37 / vcr AND nwb -> pqt
    return ",".join(sorted(["z05", "gdd", "z09", "cwt", "jmv", "css", "z37", "pqt"]))


def test_part1() -> None:
    data = dedent("""
    x00: 1
    x01: 1
    x02: 1
    y00: 0
    y01: 1
    y02: 0

    x00 AND y00 -> z00
    x01 XOR y01 -> z01
    x02 OR y02 -> z02
    """).strip()
    assert part1(parse(data)) == 4


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
