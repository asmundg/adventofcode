"""Day 3: Gear Ratios

Having a dict keyed on symbol locations means we can easily check if a
range of digits is adjacent to a symbol for part1. For part 2, it's
the same structure, but we now check if there are exactly two numbers
attached to the location.

"""

from dataclasses import dataclass
import os
from textwrap import dedent

from typing import Dict, List, Optional, Set, Tuple, TypeAlias


@dataclass
class Symbol:
    symbol: str
    numbers: List[int]


Symbols: TypeAlias = Dict[Tuple[int, int], Symbol]


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> Symbols:
    symbols: Symbols = {}

    for y, line in enumerate(data.split("\n")):
        for x, char in enumerate(line):
            if not char.isdigit() and char != ".":
                symbols[(y, x)] = Symbol(char, [])

    for y, line in enumerate(data.split("\n")):
        acc = ""
        for x, char in enumerate(line):
            if char.isdigit():
                acc += char
            else:
                coord = adjacent(x - 1, y, len(acc), set(symbols.keys()))
                if coord is not None:
                    symbols[coord].numbers.append(int(acc))
                acc = ""
        else:
            coord = adjacent(x - 1, y, len(acc), set(symbols.keys()))
            if coord is not None:
                symbols[coord].numbers.append(int(acc))

    return symbols


def adjacent(
    last: int, y: int, length: int, symbols: Set[Tuple[int, int]]
) -> Optional[Tuple[int, int]]:
    if length == 0:
        return None

    for y in range(y - 1, y + 2):
        for x in range(last - length, last + 2):
            if (y, x) in symbols:
                return (y, x)
    return None


def solve(symbols: Symbols) -> int:
    return sum([num for symbol in symbols.values() for num in symbol.numbers])


def solve2(symbols: Symbols) -> int:
    return sum(
        [
            symbol.numbers[0] * symbol.numbers[1]
            for symbol in symbols.values()
            if symbol.symbol == "*" and len(symbol.numbers) == 2
        ]
    )


def test_part1():
    data = dedent(
        """\
        467..114..
        ...*......
        ..35..633.
        ......#...
        617*......
        .....+.58.
        ..592.....
        ......755.
        ...$.*....
        .664.598.."""
    )

    assert solve(parse(data)) == 4361


def test_part2():
    data = dedent(
        """\
        467..114..
        ...*......
        ..35..633.
        ......#...
        617*......
        .....+.58.
        ..592.....
        ......755.
        ...$.*....
        .664.598.."""
    )

    assert solve2(parse(data)) == 467835


if __name__ == "__main__":
    print(solve(parse(read_data())))
    print(solve2(parse(read_data())))
