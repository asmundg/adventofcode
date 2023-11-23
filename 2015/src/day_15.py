"""Day 15: Science for Hungry People.

Brute force ftw. The input set is super limited, so we don't need to
be fancy at all.
"""

from dataclasses import dataclass
import os
import re

from typing import Dict, Optional


@dataclass
class Ingredient:
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int


def parse(fname: str) -> Dict[str, Ingredient]:
    r: Dict[str, Ingredient] = {}
    with open(fname, encoding="utf-8") as handle:
        for line in handle.read().strip().split("\n"):
            if m := re.match(
                r"([a-zA-Z]+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)",
                line,
            ):
                name, capacity, durability, flavor, texture, calories = m.groups()
                r[name] = Ingredient(
                    capacity=int(capacity),
                    durability=int(durability),
                    flavor=int(flavor),
                    texture=int(texture),
                    calories=int(calories),
                )
    return r


def mix(ingredients: Dict[str, Ingredient], amounts: Dict[str, int]) -> Ingredient:
    total = Ingredient(capacity=0, durability=0, flavor=0, texture=0, calories=0)
    for name, amount in amounts.items():
        total.capacity += ingredients[name].capacity * amount
        total.durability += ingredients[name].durability * amount
        total.flavor += ingredients[name].flavor * amount
        total.texture += ingredients[name].texture * amount
        total.calories += ingredients[name].calories * amount
    return total


def score(total: Ingredient):
    return (
        max(0, total.capacity)
        * max(0, total.durability)
        * max(0, total.flavor)
        * max(0, total.texture)
    )


def solve(
    ingredients: Dict[str, Ingredient], calorie_limit: Optional[int] = None
) -> int:
    best = 0
    for a in range(101):
        for b in range(101 - a):
            for c in range(101 - a - b):
                for d in range(101 - a - b - c):
                    if sum((a, b, c, d)) != 100:
                        continue

                    candidate = {"Sugar": a, "Sprinkles": b, "Candy": c, "Chocolate": d}
                    total = mix(
                        ingredients,
                        candidate,
                    )

                    new_score = score(total)
                    if (
                        total.calories == calorie_limit
                        if calorie_limit is not None
                        else True
                    ) and new_score > best:
                        best = new_score
    return best


day = os.path.basename(__file__).split(".")[0].split("_")[1]
base = os.path.join(os.path.dirname(__file__), "input", f"{day}")
print(score(mix(parse(f"{base}.test"), {"Butterscotch": 44, "Cinnamon": 56})))
print(solve(parse(f"{base}.input")))
print(solve(parse(f"{base}.input"), 500))
