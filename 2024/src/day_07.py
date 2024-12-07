"""Day 7: Bridge Repair

Today felt like a nice day for breaking out some Python
batteries-included functionality. Itertools are neat, but I can never
manage to remember which one does what.

We need to test reductions of the calibration inputs with all
permutations of the available operators until we find one that
fits. The itertools.permutations function doesn't support tuples
longer than its input, but product does (I still can't map "repeat" to
"produces N-length tuples" in a meaningful way).

Part 2 is exactly the same thing, with one additional operator. I
failed my reading comprehension test and first implemented a
concatenation with lower precedense than the other operators. Which
worked nicely, but wasn't what we were supposed to do!

"""

import functools
import itertools
import operator
import os
from dataclasses import dataclass
from textwrap import dedent
from typing import Callable, Generator


@dataclass(frozen=True)
class Data:
    target: int
    operands: list[int]


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> list[Data]:
    out: list[Data] = []
    for line in data.split("\n"):
        target, nums = line.split(":")
        out.append(Data(int(target), [int(num) for num in nums.split()]))
    return out


def comp(numbers: list[int], operators: list[Callable[[int, int], int]]) -> Generator[int, None, None]:
    for operator_sequence in itertools.product(operators, repeat=len(numbers) - 1):
        ops = iter(operator_sequence)
        yield functools.reduce(lambda x, y: next(ops)(x, y), numbers)


def part1(data: list[Data]) -> int:
    total = 0
    for calibration in data:
        for candidate in comp(calibration.operands, [operator.add, operator.mul]):
            if candidate == calibration.target:
                total += calibration.target
                break

    return total


def part2(data: list[Data]) -> int:
    total = 0
    for calibration in data:
        for candidate in comp(calibration.operands, [operator.add, operator.mul, lambda x, y: int(str(x) + str(y))]):
            if candidate == calibration.target:
                total += calibration.target
                break

    return total


def test_part1() -> None:
    data = dedent("""
    190: 10 19
    3267: 81 40 27
    83: 17 5
    156: 15 6
    7290: 6 8 6 15
    161011: 16 10 13
    192: 17 8 14
    21037: 9 7 18 13
    292: 11 6 16 20
    """).strip()
    assert part1(parse(data)) == 3749


def test_part2() -> None:
    data = dedent("""
    190: 10 19
    3267: 81 40 27
    83: 17 5
    156: 15 6
    7290: 6 8 6 15
    161011: 16 10 13
    192: 17 8 14
    21037: 9 7 18 13
    292: 11 6 16 20
    """).strip()
    assert part2(parse(data)) == 11387


if __name__ == "__main__":
    print(part1(parse(read_data())))
    print(part2(parse(read_data())))
