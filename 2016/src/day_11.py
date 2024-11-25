"""Day 11: Radioisotope Thermoelectric Generators

This is a search problem where we can try all possible paths and prune
the ones that produce an invalid state.

The runtime is completely atrocious because we're just BFSing our way
to the shortest path, with no subtree pruning. This is probably better
handled as a dynamic programming problem, where the shortest path is 1
+ min(cost of all outgoing paths).

Alternately, we can do a directed DFS by using an A* heuristic for
finding the most promising candidate (shortest distance of everything
to the top). If we track the cost to get to each seen state, this
should allow us to stop exploring most paths early. We don't need full
A*, since we don't actually care about the path taken, only the cost
to get to each state.

"""

import os
import re
from dataclasses import dataclass
from textwrap import dedent
from typing import Generator


@dataclass(frozen=True)
class Floor:
    rtgs: int
    chips: int


@dataclass(frozen=True)
class State:
    elevator: int
    floors: tuple[Floor, ...]


@dataclass(frozen=True)
class Payload:
    from_floor: int
    to_floor: int
    rtgs: int
    chips: int


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> tuple[State, int]:
    material_lookup: dict[str, int] = {}
    next_material = 1

    floors: list[Floor] = []
    for line in data.split("\n"):
        m = re.match(r"The (\w+) floor contains (.+).", line)
        assert m is not None, f"Failed to parse {line}"

        floor_name, contents = m.groups()
        pieces = re.split(", |, and | and ", contents)
        rtgs = 0
        chips = 0
        if pieces[0] != "nothing relevant":
            for piece in pieces:
                _, material, kind = piece.replace("and ", "").split()
                material = material.split("-")[0]
                if material not in material_lookup:
                    material_lookup[material] = next_material
                    next_material <<= 1
                match kind:
                    case "microchip":
                        chips += material_lookup[material]
                    case "generator":
                        rtgs += material_lookup[material]
        floors.append(Floor(rtgs=rtgs, chips=chips))
    return (State(elevator=0, floors=tuple(floors)), next_material)


def is_valid(state: State) -> bool:
    for floor in state.floors:
        if floor.rtgs == 0:
            continue

        # If there are RTGs and there are any chips without shielding,
        # fail
        for chip in bits(floor.chips):
            if chip & floor.rtgs == 0:
                return False

    return True


def bits(i: int) -> Generator[int, None, None]:
    hi = (1 << i.bit_length() - 1) if i else 0
    while hi > 0:
        if hi & i:
            yield hi
        hi >>= 1


def move_candidates(state: State, steps: int) -> Generator[State, None, None]:
    for next_floor_no in (state.elevator - 1, state.elevator + 1):
        if next_floor_no < 0 or next_floor_no > 3:
            continue

        payloads: set[Payload] = set()
        floor = state.floors[state.elevator]

        for rtg in bits(floor.rtgs):
            payloads.add(Payload(state.elevator, next_floor_no, rtgs=rtg, chips=0))
            for chip in bits(floor.chips):
                payloads.add(Payload(state.elevator, next_floor_no, rtgs=rtg, chips=chip))
            for rtg2 in bits(floor.rtgs):
                if rtg2 != rtg:
                    payloads.add(Payload(state.elevator, next_floor_no, rtgs=rtg + rtg2, chips=0))

        for chip in bits(floor.chips):
            payloads.add(Payload(state.elevator, next_floor_no, rtgs=0, chips=chip))
            for rtg in bits(floor.rtgs):
                payloads.add(Payload(state.elevator, next_floor_no, rtgs=rtg, chips=chip))
            for chip2 in bits(floor.chips):
                if chip2 != chip:
                    payloads.add(Payload(state.elevator, next_floor_no, rtgs=0, chips=chip + chip2))

        for payload in payloads:
            new_state = move(state, payload)
            if is_valid(new_state):
                yield new_state


def move(state: State, payload: Payload) -> State:
    new_floors: list[Floor] = []
    for i, floor in enumerate(state.floors):
        if i == payload.from_floor:
            new_floors.append(Floor(rtgs=floor.rtgs - payload.rtgs, chips=floor.chips - payload.chips))
        elif i == payload.to_floor:
            new_floors.append(Floor(rtgs=floor.rtgs + payload.rtgs, chips=floor.chips + payload.chips))
        else:
            new_floors.append(floor)
    return State(payload.to_floor, tuple(new_floors))


def solve(state: State) -> int:
    search: list[tuple[State, int]] = [(candidate, 1) for candidate in move_candidates(state, 0)]
    seen: set[State] = set()

    while True:
        next_state, steps = search.pop(0)
        if next_state in seen:
            continue

        seen.add(next_state)

        if next_state.elevator == 3 and not any(
            [True for i in range(3) if (next_state.floors[i].chips or next_state.floors[i].rtgs)]
        ):
            return steps

        for candidate in move_candidates(next_state, steps):
            search.append((candidate, steps + 1))


def part2(state: State, next_material: int) -> int:
    new_floors: list[Floor] = [
        Floor(
            rtgs=state.floors[0].rtgs + next_material + (next_material << 1),
            chips=state.floors[0].chips + next_material + (next_material << 1),
        )
    ] + [floor for floor in state.floors[1:]]

    return solve(State(state.elevator, tuple(new_floors)))


def test_part1() -> None:
    data = dedent("""
    The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
    The second floor contains a hydrogen generator.
    The third floor contains a lithium generator.
    The fourth floor contains nothing relevant.
    """).strip()
    assert solve(parse(data)[0]) == 11


if __name__ == "__main__":
    print(solve(parse(read_data())[0]))
    print(part2(*parse(read_data())))
