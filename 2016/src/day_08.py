"""Day 08: Two-Factor Authentication

Mechanical data manipulation. Took the chance to have a look at
Python's pattern matching. Pretty good, but no regex matching yet,
unfortunately. There are apparently some external packages that can
add support for you, which would be super neat.

"""

import os
import re
from textwrap import dedent

from dataclasses import dataclass
from abc import ABC
from collections.abc import Sequence


class Command(ABC):
    pass


@dataclass
class Rect(Command):
    xsize: int
    ysize: int


@dataclass
class RotateRow(Command):
    origin: int
    step: int


@dataclass
class RotateCol(Command):
    origin: int
    step: int


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> list[Command]:
    commands: list[Command] = []
    for line in data.split("\n"):
        rect = re.match(r"rect ([0-9]+)x([0-9]+)", line)
        if rect is not None:
            commands.append(Rect(xsize=int(rect.group(1)), ysize=int(rect.group(2))))
            continue
        rotate_col = re.match(r"rotate column x=([0-9]+) by ([0-9]+)", line)
        if rotate_col is not None:
            commands.append(
                RotateCol(
                    origin=int(rotate_col.group(1)),
                    step=int(rotate_col.group(2)),
                )
            )
            continue
        rotate_row = re.match(r"rotate row y=([0-9]+) by ([0-9]+)", line)
        if rotate_row is not None:
            commands.append(
                RotateRow(
                    origin=int(rotate_row.group(1)),
                    step=int(rotate_row.group(2)),
                )
            )
            continue

    return commands


def debug(pixels: Sequence[Sequence[str]]) -> None:
    for row in pixels:
        print("".join(row))


def part1(commands: Sequence[Command], width: int = 50, height: int = 6) -> int:
    pixels = [["." for _ in range(width)] for _ in range(height)]
    for command in commands:
        match command:
            case Rect(x, y):
                for dy in range(y):
                    for dx in range(x):
                        pixels[dy][dx] = "#"
            case RotateRow(y, step):
                new_row = ["." for _ in range(width)]
                for x in range(width):
                    new_row[(x + step) % width] = pixels[y][x]
                for x in range(width):
                    pixels[y][x] = new_row[x]
            case RotateCol(x, step):
                new_col = ["." for _ in range(height)]
                for y in range(height):
                    new_col[(y + step) % height] = pixels[y][x]
                for y in range(height):
                    pixels[y][x] = new_col[y]

        debug(pixels)
        print()

    count = 0
    for row in pixels:
        count += len([pixel for pixel in row if pixel == "#"])
    return count


def test_part1() -> None:
    data = dedent("""
    rect 3x2
    rotate column x=1 by 1
    rotate row y=0 by 4
    rotate column x=1 by 1
    """).strip()
    assert (part1(parse(data), width=7, height=3)) == 6


if __name__ == "__main__":
    print(part1(parse(read_data())))
