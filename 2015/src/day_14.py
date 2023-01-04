"""Day 14: 
"""

from dataclasses import dataclass
import os
import re

from typing import Dict, Tuple


@dataclass
class State:
    speed: int
    rest_time: int
    move_time: int
    moving: bool = True
    count: int = 0
    dist: int = 0
    score: int = 0


def parse(fname: str) -> Dict[str, State]:
    r: Dict[str, State] = {}
    with open(fname, encoding="utf-8") as handle:
        for line in handle.read().strip().split("\n"):
            if m := re.match(
                r"(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.",
                line,
            ):
                name, speed, move_time, rest_time = m.groups()
                r[name] = State(
                    speed=int(speed), move_time=int(move_time), rest_time=int(rest_time)
                )
    return r


def solve(states: Dict[str, State], rounds: int) -> Tuple[int, int]:
    for _ in range(rounds):
        for r in states.values():
            r.count += 1
            if r.moving:
                r.dist += r.speed
                if r.count == r.move_time:
                    r.moving = False
                    r.count = 0
            else:
                if r.count == r.rest_time:
                    r.moving = True
                    r.count = 0
        max_dist = max([e.dist for e in states.values()])
        for r in states.values():
            if r.dist == max_dist:
                r.score += 1

    return max([r.dist for r in states.values()]), max(
        [r.score for r in states.values()]
    )


day = os.path.basename(__file__).split(".")[0].split("_")[1]
base = os.path.join(os.path.dirname(__file__), "input", f"{day}")
print(solve(parse(f"{base}.test"), 1000))
print(solve(parse(f"{base}.input"), 2503))
