"""Day 21: Scrambled Letters and Hash

Mechanical task with a twist. As usual, it took me a while to notice that there were some extra rules attached to the rotate by position instruction. Classic advent of code!

Part 2 _could_ be solved with brute force, since we have a validator
from part 1. But since most of the operations are symmetrical, we can
just run the ops in reverse with a bit of special handling of rotate
by position. Since this op changes what it does based on the input
value, we need to brute force this single step.

"""

import os
import re
from dataclasses import dataclass
from textwrap import dedent


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


@dataclass(frozen=True)
class Op:
    pass


@dataclass(frozen=True)
class SwapPos(Op):
    a: int
    b: int


@dataclass(frozen=True)
class SwapLetter(Op):
    a: str
    b: str


@dataclass(frozen=True)
class Rotate(Op):
    left: bool
    steps: int


@dataclass(frozen=True)
class RotatePos(Op):
    letter: str


@dataclass(frozen=True)
class Reverse(Op):
    start_pos: int
    stop_pos: int


@dataclass(frozen=True)
class Move(Op):
    from_pos: int
    to_pos: int


def parse(data: str) -> list[Op]:
    ops: list[Op] = []
    for line in data.split("\n"):
        if m := re.match(r"swap position (\d+) with position (\d+)", line):
            ops.append(SwapPos(int(m.group(1)), int(m.group(2))))
        elif m := re.match(r"swap letter (\w) with letter (\w)", line):
            ops.append(SwapLetter(m.group(1), m.group(2)))
        elif m := re.match(r"rotate (left|right) (\d+) steps?", line):
            ops.append(Rotate(m.group(1) == "left", int(m.group(2))))
        elif m := re.match(r"rotate based on position of letter (\w)", line):
            ops.append(RotatePos(m.group(1)))
        elif m := re.match(r"reverse positions (\d+) through (\d+)", line):
            ops.append(Reverse(int(m.group(1)), int(m.group(2))))
        elif m := re.match(r"move position (\d+) to position (\d+)", line):
            ops.append(Move(int(m.group(1)), int(m.group(2))))
        else:
            raise Exception("Oops", line)

    return ops


def rotate_left(p: list[str], steps) -> list[str]:
    p = p[:]
    for _ in range(steps):
        p.append(p.pop(0))
    return p


def rotate_right(p: list[str], char: str) -> list[str]:
    p = p[:]
    pos = p.index(char)
    for _ in range(pos + 1 + (0 if pos < 4 else 1)):
        p.insert(0, p.pop())
    return p


def part1(ops: list[Op], pw: str, rev: bool = False) -> str:
    p = list(pw)
    for op in reversed(ops) if rev else ops:
        match op:
            case SwapPos(pos_a, pos_b):
                tmp = p[pos_b]
                p[pos_b] = p[pos_a]
                p[pos_a] = tmp
            case SwapLetter(a, b):
                pos_a, pos_b = p.index(a), p.index(b)
                tmp = p[pos_b]
                p[pos_b] = p[pos_a]
                p[pos_a] = tmp
            case Rotate(left, steps):
                for _ in range(steps):
                    if left ^ rev:
                        p.append(p.pop(0))
                    else:
                        p.insert(0, p.pop())
            case RotatePos(a):
                if rev:
                    for cand_steps in range(len(pw)):
                        if rotate_right(rotate_left(p, cand_steps), a) == p:
                            p = rotate_left(p, cand_steps)
                            break

                else:
                    rotate_right(p, a)

            case Reverse(pos_a, pos_b):
                p = p[:pos_a] + list(reversed(p[pos_a : pos_b + 1])) + p[pos_b + 1 :]
            case Move(pos_a, pos_b):
                char = p.pop(pos_b) if rev else p.pop(pos_a)
                p.insert(pos_a if rev else pos_b, char)

    return "".join(p)


def test_part1() -> None:
    data = dedent(
        """
        swap position 4 with position 0
        swap letter d with letter b
        reverse positions 0 through 4
        rotate left 1 step
        move position 1 to position 4
        move position 3 to position 0
        rotate based on position of letter b
        rotate based on position of letter d
        """
    ).strip()
    assert part1(parse(data), "abcde") == "decab"


if __name__ == "__main__":
    print(part1(parse(read_data()), "abcdefgh"))
    print(part1(parse(read_data()), "fbgdceah", rev=True))
