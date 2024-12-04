"""Day 4: Ceres Search

Classic example of the type of geometry problem where I always
struggle to figure out where I am in the matrix and which direction
I'm moving in.

We just need to generate all possible lines and then remember to check
the reverse order for each of them.
"""

import os
from textwrap import dedent


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str, use_p: bool = False) -> list[str]:
    return data.split("\n")


def found_words(line: str, target: str) -> int:
    return line.count(target) + "".join(reversed(line)).count(target)


def part1(puzzle: list[str]) -> int:
    count = 0

    # horizontal
    for line in puzzle:
        count += found_words(line, "XMAS")

    # vertical
    for col in range(len(puzzle[0])):
        line = "".join([puzzle[row][col] for row in range(len(puzzle))])
        count += found_words(line, "XMAS")

    # diagonal right
    for start_col in range(-len(puzzle), len(puzzle)):
        col = start_col
        row = 0
        line = ""
        while col < len(puzzle[0]) and row < len(puzzle):
            if col >= 0:
                line += puzzle[row][col]
            col += 1
            row += 1

        count += found_words(line, "XMAS")

    # diagonal left
    for start_col in range(2 * len(puzzle), 0, -1):
        col = start_col
        row = 0
        line = ""
        while col >= 0 and row < len(puzzle):
            if col < len(puzzle):
                line += puzzle[row][col]
            col -= 1
            row += 1

        count += found_words(line, "XMAS")

    return count


def part2(puzzle: list[str]) -> int:
    count = 0
    for col in range(1, len(puzzle[0]) - 1):
        for row in range(1, len(puzzle) - 1):
            line_a = puzzle[row - 1][col - 1] + puzzle[row][col] + puzzle[row + 1][col + 1]
            line_b = puzzle[row - 1][col + 1] + puzzle[row][col] + puzzle[row + 1][col - 1]
            if found_words(line_a, "MAS") and found_words(line_b, "MAS"):
                count += 1
    return count


def test_part1() -> None:
    data = dedent("""
    MMMSXXMASM
    MSAMXMSMSA
    AMXSXMAAMM
    MSAMASMSMX
    XMASAMXAMM
    XXAMMXXAMA
    SMSMSASXSS
    SAXAMASAAA
    MAMMMXMMMM
    MXMXAXMASX
    """).strip()
    assert part1(parse(data)) == 18


def test_part2() -> None:
    data = dedent("""
    MMMSXXMASM
    MSAMXMSMSA
    AMXSXMAAMM
    MSAMASMSMX
    XMASAMXAMM
    XXAMMXXAMA
    SMSMSASXSS
    SAXAMASAAA
    MAMMMXMMMM
    MXMXAXMASX
    """).strip()
    assert part2(parse(data)) == 9


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
