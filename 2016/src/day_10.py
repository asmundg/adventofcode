"""Day 10: Balance Bots

The text puzzle was a bit confusing, but in the end, the trick is that
the input values are only executed at init time. Then the rest of the
instructions can execute sequentially until we get to a stable
state.

The solution is a bit ugly, with a part1/part2 flag, because I
couldn't find a neat way of switching between the eval modes, since
finding the handling bot requires inspecting the state for each
instruction."""

import os
import re
from abc import ABC
from collections.abc import Sequence
from dataclasses import dataclass
from textwrap import dedent
from typing import Optional, Tuple


@dataclass
class Command(ABC):
    pass


@dataclass
class Input(Command):
    val: int
    out: str


@dataclass
class Forward(Command):
    source: str
    lo_out: str
    hi_out: str


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> list[Command]:
    commands: list[Command] = []
    for line in data.split("\n"):
        input = re.match("value ([0-9]+) goes to (bot [0-9]+)", line)
        if input is not None:
            commands.append(Input(val=int(input.group(1)), out=input.group(2)))
        forward = re.match(
            "(bot [0-9]+) gives low to ((?:output|bot) [0-9]+) and high to ((?:output|bot) [0-9]+)",
            line,
        )
        if forward is not None:
            commands.append(
                Forward(
                    source=forward.group(1),
                    lo_out=forward.group(2),
                    hi_out=forward.group(3),
                )
            )
    return commands


def solve(
    instructions: Sequence[Command],
    find_handler_of: Optional[Tuple[int, int]],
) -> int:
    state: dict[str, list[int]] = {}
    for instruction in instructions:
        match instruction:
            case Input(val, out):
                state[out] = state.get(out, []) + [val]

    while True:
        for instruction in instructions:
            match instruction:
                case Forward(source, lo_out, hi_out):
                    if len(state.get(source, [])) == 2:
                        lo, hi = sorted(state[source])
                        if (lo, hi) == find_handler_of:
                            return int(source.split()[1])
                        state[source] = []
                        state[lo_out] = state.get(lo_out, []) + [lo]
                        state[hi_out] = state.get(hi_out, []) + [hi]

        if (
            find_handler_of is None
            and "output 0" in state
            and "output 1" in state
            and "output 2" in state
        ):
            return state["output 0"][0] * state["output 1"][0] * state["output 2"][0]


def test_part1() -> None:
    data = dedent("""
    value 5 goes to bot 2
    bot 2 gives low to bot 1 and high to bot 0
    value 3 goes to bot 1
    bot 1 gives low to output 1 and high to bot 0
    bot 0 gives low to output 2 and high to output 0
    value 2 goes to bot 2
    """).strip()
    assert solve(parse(data), (2, 5)) == 2
    assert solve(parse(data), None) == 5 * 2 * 3


if __name__ == "__main__":
    print(solve(parse(read_data()), (17, 61)))
    print(solve(parse(read_data()), None))
