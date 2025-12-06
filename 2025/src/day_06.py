"""Day 06: Trash Compactor

Ok, so just iterating by line and stuffing into columns, then reduce?
Where is this going for part 2?

Aah, should have paid attention to the formatting. "The left/right
alignment of numbers within each problem can be ignored" indeed. So a
plain split removes information and we need to actually find the
separator column. Which we can do by just finding the first index
where all rows have a space for each column.

"""

import operator
import os
from dataclasses import dataclass
from functools import reduce
from textwrap import dedent


@dataclass
class Problem:
    nums: list[int]
    op: str


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> list[Problem]:
    lines = data.split("\n")
    problems = [Problem(nums=[], op=op) for op in lines[-1].split()]
    for line in lines[:-1]:
        for i, num in enumerate(line.split()):
            problems[i].nums.append(int(num))
    return problems


def parse2(data: str) -> list[Problem]:
    lines = data.split("\n")
    num_rows = lines[:-1]
    cursor = 0
    problems = [Problem(nums=[], op=op) for op in lines[-1].split()]
    for p in problems:
        start = cursor
        for line in num_rows:
            while cursor < len(line) and line[cursor] != " ":
                cursor += 1

        for c in range(cursor - 1, start - 1, -1):
            num_string = ""
            for line in num_rows:
                if line[c] != " ":
                    num_string += line[c]

            p.nums.append(int(num_string))

        # next column
        cursor += 1

    return problems


def part1(problems: list[Problem]) -> int:
    return sum(reduce(operator.add if problem.op == "+" else operator.mul, problem.nums) for problem in problems)


def test_part1() -> None:
    data = dedent(
        """
        123 328  51 64 
         45 64  387 23 
          6 98  215 314
        *   +   *   +  
        """
    ).strip()
    assert part1(parse(data)) == 4277556


def test_part2() -> None:
    data = dedent(
        """
        123 328  51 64 
         45 64  387 23 
          6 98  215 314
        *   +   *   +  
        """
    ).strip()
    assert part1(parse2(data)) == 3263827


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part1(parse2(read_data())))
