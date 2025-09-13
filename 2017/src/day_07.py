"""Day 07: Recursive Circus

Ok, so part 1 is just finding the program which isn't pointed at by
any other programs. The weights probably mean we actually need the
full data structure for part 2 though.

For part 2, we're looking for a program with >2 supported programs,
where one has a different weight than the others. It needs to be >2,
because there should be exactly one solution. To find the correct one,
we need to start from the leaf nodes and then back up until we find
where the issue is introduced.

"""

import itertools
import os
from dataclasses import dataclass
from functools import cached_property
from textwrap import dedent


@dataclass
class Program:
    id: str
    weight: int
    supports: list["Program"]

    @cached_property
    def total_weight(self) -> int:
        return self.weight + sum(s.total_weight for s in self.supports)


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> Program:
    programs: dict[str, Program] = {}
    supports: dict[str, list[str]] = {}
    supported_by: dict[str, str] = {}

    for line in data.split("\n"):
        p, s = line.split("->") if "->" in line else (line, "")
        program_name, weight = p.split()
        supported = s.strip().split(", ") if s else []
        supports[program_name] = supported
        programs[program_name] = Program(program_name, int(weight[1:-1]), [])

    for program in programs.values():
        program.supports = [programs[key] for key in supports[program.id]]
        for supported_p in program.supports:
            supported_by[supported_p.id] = program.id

    for program in programs.values():
        if program.id not in supported_by:
            return program


def part1(root: Program) -> str:
    return root.id


def find_correction(program: Program) -> int:
    if not program.supports:
        return 0

    for p in program.supports:
        correction = find_correction(p)
        if correction > 0:
            return correction

    if len(program.supports) > 2:
        weights = [p.total_weight for p in program.supports]
        for i, w in enumerate(weights):
            if weights.count(w) == 1:
                for p in program.supports:
                    if p.total_weight == w:
                        return p.weight - (p.total_weight - weights[(i + 1) % len(weights)])

    return 0


def part2(root: Program) -> int:
    return find_correction(root)


def test_part1() -> None:
    data = dedent("""
    pbga (66)
    xhth (57)
    ebii (61)
    havc (66)
    ktlj (57)
    fwft (72) -> ktlj, cntj, xhth
    qoyq (66)
    padx (45) -> pbga, havc, qoyq
    tknk (41) -> ugml, padx, fwft
    jptl (61)
    ugml (68) -> gyxo, ebii, jptl
    gyxo (61)
    cntj (57)
    """).strip()
    assert part1(parse(data)) == "tknk"


def test_part2() -> None:
    data = dedent("""
    pbga (66)
    xhth (57)
    ebii (61)
    havc (66)
    ktlj (57)
    fwft (72) -> ktlj, cntj, xhth
    qoyq (66)
    padx (45) -> pbga, havc, qoyq
    tknk (41) -> ugml, padx, fwft
    jptl (61)
    ugml (68) -> gyxo, ebii, jptl
    gyxo (61)
    cntj (57)
    """).strip()
    assert part2(parse(data)) == 60


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
