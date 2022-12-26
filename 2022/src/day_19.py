"""Day 19: Not Enough Minerals

This was way harder than it should have been. At its core, this
another depth-first search with some accumulated state. We simulate
all decisions points until we reach the time quota. The decision is
which robot to build, which might cause waiting for some rounds. Which
is fine, since that is optimal in some cases. Not making a decision in
each round saves us from nonsense paths where we wait randomly.

A major optimization comes from figuring out that since we can only
build one robot per turn, we will never need to produce more resources
than is consumed by construction of the most expensive robot. This
lets us prune a lot of trees.

Similarly, if we cannot possibly produce more geodes in the remaining
rounds, even assuming that we can construct one geode bot per round,
we can also prune the tree.
"""

from dataclasses import dataclass
import os
import re
from typing import Dict, List


def parse(fname: str) -> List[Dict[str, Dict[str, int]]]:
    blueprints: List[Dict[str, Dict[str, int]]] = []
    with open(fname, encoding="utf-8") as handle:
        for line in handle.read().strip().split("\n"):
            match = re.match(
                r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.",
                line,
            )
            if not match:
                raise ValueError(f"Unable to parse line: {line}")

            groups = match.groups()
            blueprints.append(
                {
                    "ore": {"ore": int(groups[1]), "clay": 0, "obsidian": 0},
                    "clay": {"ore": int(groups[2]), "clay": 0, "obsidian": 0},
                    "obsidian": {
                        "ore": int(groups[3]),
                        "clay": int(groups[4]),
                        "obsidian": 0,
                    },
                    "geode": {"ore": int(groups[5]), "obsidian": int(groups[6])},
                }
            )
    return blueprints


def build(template, resources):
    for res, cost in template.items():
        resources[res] -= cost
    return resources


def collect(resources, robots):
    resources = resources.copy()
    for robot, count in robots.items():
        resources[robot] += count
    return resources


@dataclass
class Best:
    value: int


@dataclass
class State:
    time: int
    resources: Dict[str, int]
    robots: Dict[str, int]
    best: Best


def run_plan(blueprint, state: State, target, target_robot):
    if state.time == target:
        if state.resources["geode"] > state.best.value:
            state.best.value = state.resources["geode"]
        return state.resources["geode"]

    if (
        state.robots["geode"] * (target - state.time + 1)
        + sum(range(target - state.time))
        + state.resources["geode"]
        <= state.best.value
    ):
        return 0

    if all(
        state.resources[res] >= cost for res, cost in blueprint[target_robot].items()
    ):
        build(blueprint[target_robot], state.resources)
        new_robots = state.robots.copy()
        new_robots[target_robot] += 1

        plans = []
        for (robot_type, dependency) in (
            ("geode", "obsidian"),
            ("obsidian", "clay"),
            ("clay", "ore"),
            ("ore", ""),
        ):
            if (not dependency or new_robots.get(dependency, 0) > 0) and (
                robot_type == "geode"
                or new_robots[robot_type]
                < max(template.get(robot_type, 0) for template in blueprint.values())
            ):
                plans.append(
                    run_plan(
                        blueprint,
                        State(
                            state.time + 1,
                            collect(state.resources, state.robots),
                            new_robots,
                            state.best,
                        ),
                        target,
                        robot_type,
                    )
                )

        return max(plans)

    # Waiting
    return run_plan(
        blueprint,
        State(
            state.time + 1,
            collect(state.resources, state.robots),
            state.robots,
            state.best,
        ),
        target,
        target_robot,
    )


def solve(fname: str) -> int:
    blueprints = parse(fname)

    score = 0
    for i, blueprint in enumerate(blueprints, 1):
        best = max(
            [
                run_plan(
                    blueprint,
                    State(
                        0,
                        {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0},
                        {"ore": 1, "clay": 0, "obsidian": 0, "geode": 0},
                        Best(0),
                    ),
                    24,
                    target_bot,
                )
                for target_bot in ("ore", "clay")
            ]
        )

        score += i * best

    return score


def solve2(fname: str) -> int:
    blueprints = parse(fname)

    score = 1
    for i, blueprint in enumerate(blueprints[:3], 1):
        best = max(
            [
                run_plan(
                    blueprint,
                    State(
                        0,
                        {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0},
                        {"ore": 1, "clay": 0, "obsidian": 0, "geode": 0},
                        Best(0),
                    ),
                    32,
                    target_bot,
                )
                for target_bot in ("ore", "clay")
            ]
        )

        score *= best

    return score


day = os.path.basename(__file__).split(".")[0].split("_")[1]
base = os.path.join(os.path.dirname(__file__), "input", f"{day}")
print(solve(f"{base}.test"))
print(solve(f"{base}.input"))

print(solve2(f"{base}.test"))
print(solve2(f"{base}.input"))
