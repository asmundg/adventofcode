"""Day 6: 
"""

import os
from typing import List, Tuple


def parse(data: str) -> List[Tuple[str, List[Tuple[int, int]]]]:
    commands: List[Tuple[str, List[Tuple[int, int]]]] = []
    for command in data.strip().split("\n"):
        if command.startswith("turn on"):
            commands.append(
                (
                    "turn on",
                    [[int(n) for n in s.split(",")] for s in command.split()[2:5:2]],
                ),
            )
        elif command.startswith("turn off"):
            commands.append(
                (
                    "turn off",
                    [[int(n) for n in s.split(",")] for s in command.split()[2:5:2]],
                ),
            )
        else:
            commands.append(
                (
                    "toggle",
                    [[int(n) for n in s.split(",")] for s in command.split()[1:5:2]],
                ),
            )
    return commands


def solve(commands: List[Tuple[str, List[Tuple[int, int]]]], n=1000) -> int:
    state = {}
    for y in range(n):
        for x in range(n):
            state[(y, x)] = False

    for cmd, coords in commands:
        (start_x, start_y), (stop_x, stop_y) = coords
        for y in range(start_y, stop_y + 1):
            for x in range(start_x, stop_x + 1):
                state[(y, x)] = (
                    True
                    if cmd == "turn on"
                    else False
                    if cmd == "turn off"
                    else not state[(y, x)]
                )

    return len([s for s in state.values() if s])


def solve2(commands: List[Tuple[str, List[Tuple[int, int]]]], n=1000) -> int:
    state = {}
    for y in range(n):
        for x in range(n):
            state[(y, x)] = 0

    for cmd, coords in commands:
        (start_x, start_y), (stop_x, stop_y) = coords
        for y in range(start_y, stop_y + 1):
            for x in range(start_x, stop_x + 1):
                state[(y, x)] = max(
                    state[(y, x)]
                    + (1 if cmd == "turn on" else -1 if cmd == "turn off" else 2),
                    0,
                )

    return sum(state.values())


day = os.path.basename(__file__).split(".")[0].split("_")[1]
base = os.path.join(os.path.dirname(__file__), "input", f"{day}")

assert solve(parse("turn on 0,0 through 9,0"), 10) == 10
with open(f"{base}.input", encoding="utf-8") as handle:
    print(solve(parse(handle.read())))

assert solve2(parse("toggle 0,0 through 999,999"), 1000) == 2000000
with open(f"{base}.input", encoding="utf-8") as handle:
    print(solve2(parse(handle.read())))
