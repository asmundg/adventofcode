"""Day 2: Cube Conundrum

Split, split, split
"""

import functools
import operator
import os
from textwrap import dedent

from typing import Dict, List, TypeAlias

Game: TypeAlias = List[Dict[str, int]]


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> List[Game]:
    games: List[Game] = []
    for line in data.split("\n"):
        tail = line.split(": ")[1]
        rounds = tail.split("; ")
        games.append(
            [
                {
                    entry.split(" ")[1]: int(entry.split(" ")[0])
                    for entry in round.split(", ")
                }
                for round in rounds
            ]
        )
    return games


def solve(games: List[Game]):
    limits = {"red": 12, "green": 13, "blue": 14}

    def filter(game: Game, limit: Dict[str, int]) -> bool:
        return False not in [
            val <= limit[color] for round in game for color, val in round.items()
        ]

    return sum([i for (i, game) in enumerate(games, start=1) if filter(game, limits)])


def solve2(games: List[Game]):
    powers: List[int] = []
    for game in games:
        highest: Dict[str, int] = {}
        for round in game:
            for color, val in round.items():
                if highest.setdefault(color, val) <= val:
                    highest[color] = val
        powers.append(functools.reduce(operator.mul, highest.values()))
    return sum(powers)


def test_part1():
    data = dedent(
        """\
        Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
        Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
        Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
        Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
        Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""
    )

    assert solve(parse(data)) == 8


def test_part2():
    data = dedent(
        """\
        Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
        Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
        Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
        Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
        Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""
    )

    assert solve2(parse(data)) == 2286


if __name__ == "__main__":
    print(solve(parse(read_data())))
    print(solve2(parse(read_data())))
