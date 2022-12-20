"""Day 19
"""

import itertools
import os
import re
from typing import Dict, List
from tqdm import tqdm


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


def can_build(template, resources):
    return False not in [resources[res] >= cost for res, cost in template.items()]


def build(template, resources):
    for res, cost in template.items():
        resources[res] -= cost
    return resources


def collect(resources, robots):
    resources = resources.copy()
    for robot, count in robots.items():
        resources[robot] += count
    return resources


def solve(fname: str) -> int:
    blueprints = parse(fname)

    score = 0
    for i, blueprint in enumerate(blueprints, 1):
        print("Blueprint", i)
        bar = 0
        sequences = [
            (
                {"ore": 1, "clay": 0, "obsidian": 0, "geode": 0},
                {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0},
            )
        ]
        for step in range(1, 25):
            print("step", step, len(sequences))
            pruned_sequences = []
            for robots, resources in sequences:
                if robots["geode"] > bar:
                    bar = robots["geode"]
                    print("New bar", bar)
                    pruned_sequences = []
                if robots["geode"] < bar:
                    continue

                for robot, cost in blueprint.items():
                    if can_build(cost, resources):
                        new_robots = robots.copy()
                        new_robots[robot] += 1
                        new_resources = build(cost, collect(resources, robots))
                        if (
                            step < 22
                            or robots["geode"] > 0
                            or (
                                step == 22
                                and (
                                    new_robots["geode"] > 0
                                    or can_build(blueprint["geode"], new_resources)
                                )
                            )
                            or (step == 23 and new_robots["geode"] > 0)
                        ):
                            pruned_sequences.append((new_robots, new_resources))

                # Sequence without builds
                if step < 23 or robots["geode"] > 0:
                    pruned_sequences.append((robots, collect(resources, robots)))
            sequences = pruned_sequences

        best = (
            max([resources["geode"] for robots, resources in sequences])
            if sequences
            else 0
        )
        print(best)
        quality = i * best
        score += quality
        print(i, best, quality, score)

    return score


day = os.path.basename(__file__).split(".")[0].split("_")[1]
base = os.path.join(os.path.dirname(__file__), "input", f"{day}")
print(solve(f"{base}.test"))
print(solve(f"{base}.input"))

# print(solve2(f"{base}.test"))
# print(solve2(f"{base}.input"))
